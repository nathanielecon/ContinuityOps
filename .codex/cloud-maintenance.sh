#!/usr/bin/env bash
#
# ContinuityOps — Codex Cloud Environment MAINTENANCE / warm-refresh script.
#
# CHANGE CONTROL (D-026): this file and cloud-setup.sh are the ONLY content
# pasted into the Codex Cloud Environment. Editing them ad hoc is out of bounds.
# Never add secrets or environment variables to the Environment.
#
# Purpose: keep the container warm and prove the repo still holds together.
# Runs on cache refresh and as the warm-gate smoke step. Fast, idempotent, and
# credential-free. Exit non-zero if any JSON contract fails to parse.
#
# Note for the owner: written to the described dailydigits warm-start pattern;
# pending owner cross-check against the dailydigits reference.

set -euo pipefail

need_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "MAINTENANCE FAIL: required command not found: $1" >&2
    exit 1
  fi
}

need_cmd python3

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$repo_root"

echo "[maint] validating JSON contracts under $repo_root"

python3 - <<'PY'
import json, glob, re, sys

ok = True

# Standalone *.json files.
for f in glob.glob('**/*.json', recursive=True):
    if '/.git/' in f:
        continue
    try:
        with open(f) as fh:
            json.load(fh)
        print(f"OK   json  {f}")
    except Exception as e:
        ok = False
        print(f"FAIL json  {f}: {e}")

# Fenced ```json blocks embedded in Markdown.
for f in glob.glob('**/*.md', recursive=True):
    if '/.git/' in f:
        continue
    with open(f) as fh:
        txt = fh.read()
    for i, m in enumerate(re.finditer(r'```json\s*\n(.*?)```', txt, re.S)):
        try:
            json.loads(m.group(1))
            print(f"OK   block {f}#{i+1}")
        except Exception as e:
            ok = False
            print(f"FAIL block {f}#{i+1}: {e}")

print("ALL PASS" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)
PY

echo "[maint] contracts valid — container warm"
