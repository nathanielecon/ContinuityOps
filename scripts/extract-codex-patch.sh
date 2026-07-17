#!/usr/bin/env bash
# Extract continuityops-patch-v1 metadata + unified diff from a Codex bot comment.
# Usage: extract-codex-patch.sh <comment-body-file> <outdir>
# Writes: outdir/base_branch, outdir/base_sha, outdir/context_remaining, outdir/patch.diff
# Exit 0 on success; non-zero with message on stderr.
set -euo pipefail

BODY_FILE="${1:?comment body file required}"
OUTDIR="${2:?outdir required}"

if [[ ! -f "$BODY_FILE" ]]; then
  echo "ERROR: missing body file: $BODY_FILE" >&2
  exit 2
fi

mkdir -p "$OUTDIR"
MARKER='<!-- continuityops-patch-v1'
if ! grep -qF "$MARKER" "$BODY_FILE"; then
  echo "ERROR: missing continuityops-patch-v1 marker" >&2
  exit 3
fi

# Metadata: first occurrence of base_branch / base_sha after any v1 marker.
base_branch="$(grep -E '^base_branch:[[:space:]]*' "$BODY_FILE" | head -n1 | sed -E 's/^base_branch:[[:space:]]*//;s/[[:space:]]*$//')"
base_sha="$(grep -E '^base_sha:[[:space:]]*' "$BODY_FILE" | head -n1 | sed -E 's/^base_sha:[[:space:]]*//;s/[[:space:]]*$//')"
context_remaining="$(grep -E '^context_remaining:[[:space:]]*' "$BODY_FILE" | head -n1 | sed -E 's/^context_remaining:[[:space:]]*//;s/[[:space:]]*$//' || true)"

if [[ -z "$base_branch" ]]; then
  echo "ERROR: missing base_branch:" >&2
  exit 4
fi
if [[ ! "$base_sha" =~ ^[0-9a-fA-F]{40}$ ]]; then
  echo "ERROR: base_sha must be 40 hex chars (got: ${base_sha:-empty})" >&2
  exit 5
fi

# Collect fenced diff blocks. Prefer blocks immediately after part markers when present.
# Part markers: <!-- continuityops-patch-v1 part=K/N -->
# If no part markers, concatenate all ```diff ... ``` (or ```) blocks that contain "diff --git".
python3 - "$BODY_FILE" "$OUTDIR/patch.diff" <<'PY'
import re, sys
from pathlib import Path

body = Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
out = Path(sys.argv[2])

part_re = re.compile(
    r"<!--\s*continuityops-patch-v1\s+part=(\d+)/(\d+)\s*-->\s*"
    r"```(?:diff)?\s*\n(.*?)```",
    re.DOTALL | re.IGNORECASE,
)
fence_re = re.compile(r"```(?:diff)?\s*\n(.*?)```", re.DOTALL)

parts = part_re.findall(body)
chunks = []
if parts:
    # Validate contiguous 1..N
    parsed = [(int(k), int(n), text) for k, n, text in parts]
    n = parsed[0][1]
    if any(p[1] != n for p in parsed):
        print("ERROR: inconsistent part totals", file=sys.stderr)
        sys.exit(6)
    by_k = {k: text for k, _, text in parsed}
    if set(by_k) != set(range(1, n + 1)):
        print(f"ERROR: expected parts 1..{n}, got {sorted(by_k)}", file=sys.stderr)
        sys.exit(7)
    chunks = [by_k[i] for i in range(1, n + 1)]
else:
    for m in fence_re.finditer(body):
        text = m.group(1)
        if "diff --git" in text:
            chunks.append(text)

if not chunks:
    print("ERROR: no unified diff fenced blocks found", file=sys.stderr)
    sys.exit(8)

patch = "".join(chunks)
if not patch.endswith("\n"):
    patch += "\n"

# Denylist: .github/**, *secret*, .env*, binary git markers
deny_patterns = [
    re.compile(r"(^|/)(\.github)(/|$)", re.I),
    re.compile(r"secret", re.I),
    re.compile(r"(^|/)\.env(\.|$|/)", re.I),
]
paths = set()
for line in patch.splitlines():
    if line.startswith("diff --git "):
        # diff --git a/path b/path
        m = re.match(r"diff --git a/(.+?) b/(.+)$", line)
        if m:
            paths.add(m.group(1))
            paths.add(m.group(2))
    if line.startswith("Binary files ") or line.startswith("GIT binary patch"):
        print("ERROR: binary patches are refused", file=sys.stderr)
        sys.exit(9)

for p in sorted(paths):
    if p == "/dev/null":
        continue
    for rx in deny_patterns:
        if rx.search(p):
            print(f"ERROR: denylisted path in patch: {p}", file=sys.stderr)
            sys.exit(10)

if "diff --git " not in patch:
    print("ERROR: patch missing diff --git headers", file=sys.stderr)
    sys.exit(11)

out.write_text(patch, encoding="utf-8")
print(f"OK: wrote {out} ({len(paths)} paths, {len(chunks)} chunk(s))")
PY

printf '%s\n' "$base_branch" >"$OUTDIR/base_branch"
printf '%s\n' "$base_sha" >"$OUTDIR/base_sha"
printf '%s\n' "${context_remaining:-n/a}" >"$OUTDIR/context_remaining"

echo "OK: base_branch=$base_branch base_sha=$base_sha"
