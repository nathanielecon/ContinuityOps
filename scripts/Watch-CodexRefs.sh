#!/usr/bin/env bash
# Watch-CodexRefs.sh — single-shot ls-remote ref watcher (D-032 evented wake aid)
#
# Compares `git ls-remote origin 'refs/heads/*'` to a stamp file under
# `.codex-warm/last-refs.txt`, prints newly appeared or changed refs, and always
# exits 0 (informational; never a hard gate).
#
# Heartbeat usage (supervisor / control-center):
#   Run about every 3.5h as a cheap wake signal between the 3–4h fallback
#   heartbeat and evented PR/publish wakes. Example:
#     ./scripts/Watch-CodexRefs.sh --once
#   Changed refs are printed to stdout; no secrets are read or written.
#
# Default mode is --once (single shot). The stamp directory is local-only and
# should be gitignored (`.codex-warm/`).

set -euo pipefail

ONCE=1
STAMP_DIR=".codex-warm"
STAMP_FILE="${STAMP_DIR}/last-refs.txt"

usage() {
  cat <<'EOF'
Usage: Watch-CodexRefs.sh [--once]

  --once   Single-shot compare (default). Print changed/new refs vs stamp, then
           update the stamp file and exit 0.

Requires a configured `origin` remote. Creates `.codex-warm/last-refs.txt` on
first run (all current refs are treated as baseline; nothing is printed).
EOF
}

for arg in "$@"; do
  case "$arg" in
    --once) ONCE=1 ;;
    -h|--help) usage; exit 0 ;;
    *)
      echo "Unknown argument: $arg" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "error: not inside a git work tree" >&2
  exit 2
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  echo "error: remote 'origin' is not configured" >&2
  exit 2
fi

tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT
current="${tmpdir}/current-refs.txt"

# Sort for stable diff; format: <sha>\t<ref>
git ls-remote origin 'refs/heads/*' | awk '{print $1 "\t" $2}' | sort -k2,2 >"$current"

mkdir -p "$STAMP_DIR"

if [[ ! -f "$STAMP_FILE" ]]; then
  cp "$current" "$STAMP_FILE"
  echo "Watch-CodexRefs: initialized stamp at ${STAMP_FILE} ($(wc -l <"$current" | tr -d ' ') refs); no prior baseline."
  exit 0
fi

# Changed or new: lines in current not present in stamp (sha+ref pair).
# Also report refs whose SHA changed (same ref name, different sha).
changed=0
while IFS=$'\t' read -r sha ref; do
  [[ -z "${ref:-}" ]] && continue
  prev_sha=$(awk -v r="$ref" -F'\t' '$2 == r { print $1; exit }' "$STAMP_FILE" || true)
  if [[ -z "${prev_sha:-}" ]]; then
    echo "NEW  ${ref}  ${sha}"
    changed=1
  elif [[ "$prev_sha" != "$sha" ]]; then
    echo "CHANGED  ${ref}  ${prev_sha} -> ${sha}"
    changed=1
  fi
done <"$current"

# Deleted refs (present in stamp, absent in current)
while IFS=$'\t' read -r sha ref; do
  [[ -z "${ref:-}" ]] && continue
  if ! awk -v r="$ref" -F'\t' '$2 == r { found=1; exit } END { exit !found }' "$current"; then
    echo "DELETED  ${ref}  (was ${sha})"
    changed=1
  fi
done <"$STAMP_FILE"

if [[ "$changed" -eq 0 ]]; then
  echo "Watch-CodexRefs: no ref changes vs ${STAMP_FILE}"
fi

cp "$current" "$STAMP_FILE"
exit 0
