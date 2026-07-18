# Evidence index

Commit-bound evidence pointers for ContinuityOps. Claim levels below match
[`docs/claims/matrix.json`](claims/matrix.json) component rows under engagement
**A3** (scoped AWS lab ceiling via `continuityops-gha`). Hosted lab apply /
drill / teardown evidence is **tip-inherited** from recorded runs — not
re-applied on every tip.

| Component | Claim | Primary evidence | Notes |
| --- | --- | --- | --- |
| upstream-integration | **L2** | `evidence/slices/S1/upstream-integration.json` · `integration/upstreams.lock.json` · `evidence/hosted/upstream-d028-2026-07-18.json` | D-028 packet + digest pin; no ContinuityOps known-good rollback claim |
| terraform-scaffold | **L4** | `evidence/slices/S1/terraform.json` · `evidence/hosted/cloud-apply-staging-*.json` | Lab stack apply via OIDC → `continuityops-gha` (tip-inherited) |
| hosted-ci-stubs | **L4** | `evidence/slices/S1/hosted-ci.json` · elevation hosted artifact | Protected GHA / OIDC delivery path (tip-inherited) |
| kubernetes-chart | **L4** | `evidence/slices/S2/chart-contract.json` · elevation hosted artifact | Lab EKS apply then destroyed in teardown (tip-inherited) |
| serverless-worker | **L4** | `evidence/slices/S3/serverless.json` · elevation hosted artifact | Lab Lambda + SQS apply (tip-inherited) |
| observability | **L4** | `evidence/slices/S4/telemetry.json` · elevation hosted artifact | CloudWatch lab signals (tip-inherited) |
| runbooks-drills | **L4** | `evidence/slices/S5/runbooks.json` · `evidence/hosted/lab-drill-rto-29645042815.json` | Lab incident drill only — not production |
| security-sbom | **L2** | `evidence/slices/S6/security.json` · `evidence/hosted/security-sbom-2026-07-18.json` | Reproducible repo SBOM; no live IAM / vuln hosted claim |
| azure-governance | **L1** | `evidence/slices/S6/azure-governance.json` | Live Azure apply out of ceiling (D-046) |
| agentic-workflow | **L3** | `evidence/slices/S6/agentic.json` · `evidence/hosted/agentic-workflow-2026-07-18.json` | Hosted-control evidence only; no in-pod AWS credentials |
| recovery | **L4** | `evidence/slices/S7/recovery/` · lab-drill-rto hosted artifact | Lab RTO wall-clock from drill recorder (tip-inherited) |
| performance | **L1** | `evidence/slices/S7/performance/` | Honest L1 — no live load proof |
| finops-teardown | **L4** | `evidence/slices/S7/cost/` · elevation hosted artifact | Live `terraform destroy` staging (tip-inherited) |
| portfolio-delivery | **L4** | `evidence/slices/S8/` · `evidence/portfolio/tip-bind-2026-07-18.json` · fresh judges | A3-scoped portfolio gate + tip-bind |

## Slice folder map

| Slice | Holds |
| --- | --- |
| S0 | Harness / validators / H0 |
| S1 | Upstream (L2) · terraform (L4) · hosted CI (L4) |
| S2 | Kubernetes chart + lab apply evidence (L4) |
| S3 | Serverless contracts + lab apply evidence (L4) |
| S4 | Observability / telemetry (L4) |
| S5 | Runbooks + lab drills (L4) |
| S6 | Security SBOM (L2) · Azure (L1) · agentic (L3) |
| S7 | Recovery (L4) · performance (L1) · FinOps teardown (L4) |
| S8 | Portfolio delivery / claims gate (L4) |

Authority: root [`README.md`](../README.md) + [`docs/claims/matrix.json`](claims/matrix.json).
Non-claims and demo script: [`docs/handoff/interview-walkthrough.md`](handoff/interview-walkthrough.md).
