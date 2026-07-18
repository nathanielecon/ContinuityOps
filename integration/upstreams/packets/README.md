# Upstream context packets (D-028 / CO-006)

Control-center packages pinned Project A/C excerpts so workers get **data, not
permission**. Do not widen worker GitHub tokens to private upstreams.

## Refresh

```bash
node scripts/package-upstream-context.mjs
```

Optional: `PACKET_ID=YYYY-MM-DD-a-c`.

## Current packet (`2026-07-18-a-c`)

| Field | Value |
| --- | --- |
| Project A pin | `f688065c7705ab7d3febcd9ec2842bea4d8bed87` |
| Project C pin | `376b7e18c5cc94e67ff180ca2f42b8eb05535be3` |
| Project C digest | `sha256:bffa93adcbe247be118de0726842f673e14310052b3fdcd6ddaa853fbc05c229` |
| Registry | `283077380808.dkr.ecr.us-east-1.amazonaws.com/project-c-delivery-api` |
| Rollback | `none proven` |
| A2 option | 2 (re-pin to digest-proven deploy SHA; phase-9 evidence overlay) |

See `manifest.json` and `CO-004.txt`.
