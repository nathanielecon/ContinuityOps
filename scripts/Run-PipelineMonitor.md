# Pipeline monitor re-dispatch (chief)

Periodic Grok (or equivalent) read-only sweep. Contract:
`docs/planning/dispatch/MONITOR.zh.md`.

## When

- Align with ~3–4h chief heartbeat, or
- After junior escalates / STREAM_COMPLETE, or
- When chief suspects silent stall

## How

Dispatch a Cursor Task / subagent with model `cursor-grok-4.5-high` (or current
Grok equivalent), prompt pointing at `MONITOR.zh.md`, write
`evidence/slices/S0/MONITOR-REPORT-latest.json`.

Chief reads the report only if `severity` is `significant` or `critical`.
`quiet` → no chief action.

Monitor never actuates. Junior clears ordinary bottlenecks; chief only if
junior fails or escalation fires.
