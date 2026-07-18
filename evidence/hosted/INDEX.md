# Hosted evidence index

This index closes the hosted-evidence discoverability gap for the current
ContinuityOps L4-lab claim set. It does not raise any claim by itself; claim
levels remain governed by `docs/claims/matrix.json` and candidate-bound
verification records.

| Evidence | Bound run / SHA | Supports | Notes |
| --- | --- | --- | --- |
| `cloud-apply-staging-2026-07-18.json` | plan run `29642718513`; apply run `29643569047`; main tip `23c7d2303ba92aa0a941c3be8c11245cfcb3b631` | Hosted OIDC smoke apply, remote state, staging live marker | Smoke scope only; CursorCloudAgent and in-pod AWS remain non-claims. |
| `cloud-apply-staging-elevation-2026-07-18.json` | plan `29644515314`; fixed plan `29644639098`; apply `29644662492`; teardown `29645052414`; candidate `f059ffa3d2b73e26fb61c849f2a6bfeebdd0259a` | AWS lab VPC/IAM/SQS/Lambda/EKS resources and teardown evidence | Partial failed apply `29644551841` is retained and superseded by BF-2026-012. |
| `lab-drill-rto-29645042815.json` | drill run `29645042815` | Synthetic lab restore drill timing | Lab-only evidence; not a production customer incident or production RTO claim. |

## Index invariants

- Add every new hosted `*.json` evidence file here in the same PR that adds it.
- Keep failed or partial runs visible; mark the superseding run and BF entry
  instead of deleting evidence.
- Do not claim EKS/Lambda/Azure/RTO levels beyond the exact run URLs and
  environments listed in the matrix.
