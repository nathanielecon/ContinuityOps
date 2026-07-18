# Evidence index

Commit-bound evidence pointers for ContinuityOps. All rows are **L1** unless noted.

| Slice | Artifact | Claim | Notes |
| --- | --- | --- | --- |
| S0 | `evidence/slices/S0/` | L1 | Harness / validators / H0 |
| S1 | `evidence/slices/S1/` | L1 | Upstream / terraform / hosted CI stubs |
| S2 | `evidence/slices/S2/` | L1 | Helm chart; no managed cluster apply |
| S3 | `evidence/slices/S3/` | L1 | Serverless contracts; no live Lambda |
| S4 | `evidence/slices/S4/` | L1 | Synthetic signal path |
| S5 | `evidence/slices/S5/` | L1 | Runbooks + synthetic drills |
| S6 | `evidence/slices/S6/` | L1 | Security/Azure/agentic fixtures |
| S7 | `evidence/slices/S7/` | L1 | Recovery/perf/finops synthetic |
| S8 | `evidence/slices/S8/` | L1 | Claims index + portfolio gate |

See also [`docs/claims/matrix.json`](claims/matrix.json).
