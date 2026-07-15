# ContinuityOps — Cloud Reliability and Recovery Platform

![ContinuityOps architecture and evidence story](docs/portfolio/continuityops-infographic.png)

> A governed cloud-operations lab that moves an immutable workload through
> protected GitHub OIDC delivery, managed Kubernetes and serverless runtime,
> correlated observability, reproducible incidents, and verified recovery.
>
> **Current evidence level:** replace this sentence from the final component
> claim matrix. Do not publish target-state wording as completed fact.

## Results at a glance

Replace every bracketed item only with a current evidence ID.

| Result | Verified outcome | Evidence |
| --- | --- | --- |
| Delivery | `[hosted checks / blocked unsafe change]` | `[EVIDENCE_ID]` |
| Kubernetes | `[managed runtime / scaling / failure recovery]` | `[EVIDENCE_ID]` |
| Serverless | `[retry / idempotency / DLQ replay]` | `[EVIDENCE_ID]` |
| Operations | `[detection / root cause / recovery metric]` | `[EVIDENCE_ID]` |
| Recovery | `[measured RTO/RPO / restore verification]` | `[EVIDENCE_ID]` |
| Performance/Cost | `[before-after / budget / teardown]` | `[EVIDENCE_ID]` |

## Architecture

ContinuityOps separates agentic code construction from live cloud authority.
Opus supervises the program; Grok-controlled Ralphy streams coordinate bounded
work; Codex CLI Cloud Agents implement; protected GitHub Actions OIDC performs
approved cloud changes. The runtime combines managed Kubernetes with a queued
serverless path. Metrics, logs, and traces drive SLO alerts, incident runbooks,
and recovery verification. Agent-assisted remediation has no default mutation
authority and routes changes through the protected human gate.

- [Editable draw.io source](docs/architecture/continuityops.drawio)
- [Exact architecture render](docs/architecture/continuityops-architecture.png)
- [Architecture decisions](docs/decisions/)

## What I engineered

- **Governed delivery:** `[evidence-backed implementation statement]`
- **Kubernetes operations:** `[evidence-backed implementation statement]`
- **Serverless + SaaS:** `[evidence-backed implementation statement]`
- **Observability + incidents:** `[evidence-backed implementation statement]`
- **Security + agentic safety:** `[evidence-backed implementation statement]`
- **Recovery + performance + FinOps:** `[evidence-backed implementation statement]`

## Failure and recovery proof

| Initial symptom | Root cause | Decision and verified recovery | Evidence |
| --- | --- | --- | --- |
| `[misleading symptom]` | `[root cause]` | `[rollback/remediation/restore + business verification]` | `[INCIDENT_ID]` |
| `[network/Linux symptom]` | `[root cause]` | `[bounded recovery]` | `[INCIDENT_ID]` |
| `[serverless/data symptom]` | `[root cause]` | `[DLQ/restore/replay verification]` | `[INCIDENT_ID]` |

## Five-minute recruiter demo

1. Open the [evidence index](docs/evidence-index.md).
2. Run the credential-free validation entry point: `[SAFE_COMMAND]`.
3. Inspect one hosted passing run and one harmless blocked-change run.
4. Follow one incident from alert through root cause and recovery.
5. Compare one performance or recovery result before and after remediation.

The demo must not require cloud credentials or mutate resources.

## Evidence map

- [Hosted delivery](evidence/hosted/)
- [Kubernetes runtime and scenarios](evidence/slices/S2/)
- [Serverless and SaaS operations](evidence/slices/S3/)
- [Observability and SLOs](evidence/slices/S4/)
- [Incident and network/Linux drills](evidence/slices/S5/)
- [Security and agentic workflow](evidence/slices/S6/)
- [Recovery, performance, and cost](evidence/slices/S7/)
- [Post-build partition certification](evidence/postbuild/)
- [Final clean-room council](evidence/judges/S8/)
- [Break/fix history](BREAK_FIX_LOG.md)

## Technology

Populate only technology actually present and verified.

| Layer | Technology |
| --- | --- |
| Cloud/IaC | `[AWS, Terraform, GitHub OIDC]` |
| Runtime | `[EKS, Helm, Kubernetes, serverless, queue]` |
| Application | `[language/framework; TypeScript 7.x only if used]` |
| Delivery | `[GitHub Actions, registry, immutable digest]` |
| Observability | `[metrics/logs/traces/SLO tooling]` |
| Security | `[IAM/RBAC/secrets/policy/scanners/SBOM]` |
| Verification | `[tests, incident drills, saved/fresh councils]` |

## Key decisions and tradeoffs

1. **GitOps over Cloud Agent credentials:** live changes use protected OIDC;
   agents edit source but do not become the cloud apply identity.
2. **Concurrent but disjoint:** several Ralphy streams increase throughput while
   sequential in-stream ownership and an integration queue control conflicts.
3. **Saved repair, fresh certification:** continuity accelerates repair; fresh
   judges limit anchoring.
4. **Evidence before claims:** every resume statement maps to a commit-bound
   evidence ID.
5. **Synthetic lab boundaries:** recovery depth is demonstrated without
   implying sustained customer-production ownership.

## Claim boundary

ContinuityOps is an isolated synthetic-data cloud lab. It demonstrates only the
implemented and tested behaviors linked in the evidence index. It does not
represent sustained customer-production SRE tenure, enterprise scale,
multi-account production ownership, or Azure networking features that were not
separately implemented and evidenced.
