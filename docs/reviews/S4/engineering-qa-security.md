# S4 engineering / QA / security / evidence review

## Scope

Phase 4 slice S4: telemetry/redaction (P4-T01), dashboards/alerts/SLO (P4-T02), signal-path drills (P4-T03).

## Engineering

- OTEL correlation across ingress/app/queue/function.
- Redaction helpers for secrets and tenant-sensitive fields.
- Dashboard/alert JSON schemas; SLO error-budget math module.
- Synthetic signal-path drill fixtures.

## QA

- Unit tests for redaction, SLO math, dashboard/alert schema, signal path.
- Validators wired for P4-T01..T03.

## Security

- Redaction fail-closed unit coverage.
- No live telemetry backend credentials in repo.

## Evidence / claims

| Component | Claim |
| --- | --- |
| Telemetry contracts + unit tests | L1 |
| Live Grafana/CloudWatch fire | not claimed |

## Residual issues

- Live signal-path drills require hosted observability backends.
