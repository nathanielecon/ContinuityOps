#!/usr/bin/env bash
# Bootstrap a fresh container for the math-document work.
#
# Containers are ephemeral: every session starts without these tools. Run this
# FIRST, before dispatching any agent that reads a PDF.
#
#   bash docs/math-corrections/bootstrap.sh
#
# Idempotent. Safe to re-run. Exits non-zero if any required tool is missing at
# the end, so it can gate a run.

set -uo pipefail

log() { printf '\n=== %s\n' "$*"; }
have() { command -v "$1" >/dev/null 2>&1; }

# ---------------------------------------------------------------- 1. apt ----
# GOTCHA: the base image ships a stale apt index. `apt-get install
# poppler-utils` fails with a 404 on the .deb until the index is refreshed.
# Do not interpret that 404 as "package unavailable".
#
# GOTCHA: apt-get update prints a 403 for the ondrej/php PPA through the egress
# proxy. Harmless - the archives we need still resolve. Do not chase it.
if ! have pdflatex || ! have pdftoppm; then
  log "apt-get update (expect a 403 on the ondrej/php PPA - ignore it)"
  apt-get update -qq 2>&1 | tail -2
fi

# --------------------------------------------------------------- 2. LaTeX ----
# GOTCHA: texlive-latex-base does NOT provide lmodern.sty. Without the lmodern
# package the build dies with "File `lmodern.sty' not found".
# texlive-pictures is needed for tikz; texlive-fonts-extra for the rest.
if ! have pdflatex; then
  log "installing TeX Live (several minutes)"
  apt-get install -y --no-install-recommends \
    texlive-latex-base texlive-latex-recommended texlive-latex-extra \
    texlive-fonts-recommended texlive-fonts-extra texlive-pictures \
    lmodern 2>&1 | tail -3
else
  log "pdflatex present: $(pdflatex --version | head -1)"
fi

# -------------------------------------------------------------- 3. poppler ----
# CRITICAL, and the single most expensive thing to get wrong.
#
# pdftoppm backs the Read tool's PDF page rendering. Without it,
# Read(file_path=X.pdf, pages="1-14") fails with
#   "pdftoppm is not installed. Install poppler-utils ..."
# and an agent told to "read the rendered page" will silently fall back to text
# extraction. Text extraction of these documents fuses words across bold/italic
# runs and flattens exponents, so the agent then reports a flood of defects that
# do not exist. On the previous run, ten scanner agents were dispatched before
# poppler was installed and every one had to be corrected mid-flight.
#
# INSTALL THIS BEFORE DISPATCHING ANY AGENT.
if ! have pdftoppm || ! have pdftotext; then
  log "installing poppler-utils (pdftoppm + pdftotext)"
  apt-get install -y poppler-utils 2>&1 | tail -3
else
  log "poppler present: $(pdftotext -v 2>&1 | head -1)"
fi

# --------------------------------------------------------------- 4. python ----
# GOTCHA: the image's Debian-packaged cryptography (41.0.7) has no RECORD file,
# so pip cannot uninstall it, and importing pypdf dies with
#   ModuleNotFoundError: No module named '_cffi_backend'
#   pyo3_runtime.PanicException: Python API call failed
# --ignore-installed sidesteps the un-uninstallable package.
if ! python3 -c "import pypdf" >/dev/null 2>&1; then
  log "repairing cffi/cryptography, then pypdf"
  pip install -q --upgrade --force-reinstall --ignore-installed cffi cryptography 2>&1 | tail -2
  pip install -q pypdf 2>&1 | tail -2
fi
# PyMuPDF: needed for get_drawings() rule detection and glyph-level measurement.
python3 -c "import fitz" >/dev/null 2>&1 || { log "installing PyMuPDF"; pip install -q pymupdf 2>&1 | tail -2; }

# ------------------------------------------------------------------ 5. rtk ----
# Optional. GOTCHA: the egress proxy does not serve GitHub release assets, so
# the prebuilt binary 404s. Build from source (~3 min) or skip.
if ! have rtk && [ -d /workspace/rtk-ai/rtk ]; then
  log "building rtk from source (~3 min; release assets are not reachable)"
  ( cd /workspace/rtk-ai/rtk && cargo build --release >/dev/null 2>&1 \
    && install -m755 target/release/rtk /usr/local/bin/rtk ) || echo "  rtk build skipped/failed - non-fatal"
fi

# --------------------------------------------------------------- 6. verify ----
log "verification"
fail=0
for t in pdflatex pdftotext pdftoppm; do
  if have "$t"; then printf '  OK      %s\n' "$t"; else printf '  MISSING %s\n' "$t"; fail=1; fi
done
for m in pypdf fitz; do
  if python3 -c "import $m" >/dev/null 2>&1; then printf '  OK      python:%s\n' "$m"; else printf '  MISSING python:%s\n' "$m"; fail=1; fi
done
have rtk && printf '  OK      rtk (optional)\n' || printf '  --      rtk (optional, absent)\n'

# End-to-end proof: the shared style must actually compile.
if have pdflatex; then
  d=$(mktemp -d)
  cp "$(dirname "$0")/tex/mathdocs.sty" "$d/" 2>/dev/null && cat > "$d/probe.tex" <<'TEX'
\documentclass[11pt]{article}\usepackage[letterpaper,margin=1in]{geometry}
\usepackage{mathdocs}\begin{document}
\lesson{Lesson 1-1: Probe}\question{Question 1}\blockhead{Question}
Probe $\abs{-9}=9$, $3^2\times3^4=3^6$, \mixed{15}{1}{2}, \money{425}, $13\degF$.
\numline{-4}{4}{2}{0}\finalans{ok}\end{document}
TEX
  ( cd "$d" && pdflatex -interaction=nonstopmode -halt-on-error probe.tex >/dev/null 2>&1 ) \
    && printf '  OK      mathdocs.sty compiles\n' \
    || { printf '  FAILED  mathdocs.sty does not compile\n'; fail=1; }
  rm -rf "$d"
fi

if [ "$fail" -ne 0 ]; then
  printf '\nBOOTSTRAP INCOMPLETE - do not dispatch PDF-reading agents yet.\n'
  exit 1
fi
printf '\nBootstrap complete. Safe to dispatch agents.\n'
