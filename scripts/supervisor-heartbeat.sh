#!/usr/bin/env bash
# ContinuityOps supervisor heartbeat (~3.5h) + ls-remote single-shot (D-032).
# Keep-warm @codex on issue #4 requires issues:write (CO-011) — this script only
# polls refs and logs; it does not post GitHub comments.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG="${ROOT}/.codex-warm/heartbeat.log"
mkdir -p "$(dirname "$LOG")"
INTERVAL_SEC="${HEARTBEAT_INTERVAL_SEC:-12600}" # 3.5h
while true; do
  ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  {
    echo "===== heartbeat ${ts} ====="
    "${ROOT}/scripts/Watch-CodexRefs.sh" --once || true
    echo "note: keep-warm @codex on #4 requires owner/issues:write (CO-011)"
  } | tee -a "$LOG"
  sleep "$INTERVAL_SEC"
done
