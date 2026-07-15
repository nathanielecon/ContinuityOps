# ContinuityOps Evidence and Claims Contract

## 1. Evidence model

Evidence is append-only. A failed run remains visible. A later success adds a
superseding event; it never overwrites the historical event.

Each event uses:

```json
{
  "schema_version": "1.0",
  "event_id": "EVT-YYYYMMDD-HHMMSS-UNIQUE",
  "event_type": "validation|hosted_check|cloud_apply|incident|recovery|performance|cost|teardown|judge|approval",
  "task_id": "P0-T01",
  "slice_id": "S0",
  "candidate_sha": "40_HEX",
  "baseline_sha": "40_HEX",
  "upstream_locks_sha256": "64_HEX",
  "partition_sha256": "64_HEX",
  "validator_sha256": "64_HEX",
  "rubric_sha256": "64_HEX_OR_NULL",
  "environment": "local|hosted-pr|staging|recovery-lab|portfolio-demo",
  "execution_identity": "sanitized principal/workload identity",
  "started_at": "ISO-8601",
  "ended_at": "ISO-8601",
  "commands": [
    {"validator_id": "allowlisted-id", "display_command": "redacted safe command", "exit_code": 0, "output_path": "evidence/raw/...", "output_sha256": "64_HEX"}
  ],
  "tool_versions": {},
  "result": "pass|fail|blocked|waiting_human",
  "claim_level": "L0|L1|L2|L3|L4|L5|L6",
  "artifacts": [],
  "redactions": [],
  "supersedes": [],
  "remaining_boundaries": [],
  "created_by": "adapter|named independent role"
}
```

Agentic/orchestration evidence additionally records supervisor, stream ID,
actual model and mode, worker language, cloud/local execution location,
bottleneck profile, saved-versus-fresh council membership, and proxy/direct
transport. Never record provider credentials or raw proxy request contents.

The adapter owns authoritative evidence events for implementation/validation.
Judges own only their distinct judge reports, which the adapter indexes after
schema validation.

## 2. Claim levels

| Level | Meaning | Allowed wording |
| --- | --- | --- |
| L0 | designed only | “designed,” “specified,” “planned” |
| L1 | static validated | “Terraform/Helm/policy/tests validate offline” |
| L2 | locally executed | “ran locally/on kind/Docker with synthetic data” |
| L3 | hosted validated | “GitHub-hosted checks passed/blocked change on run X” |
| L4 | cloud applied | “applied in isolated AWS/Azure lab; resource checks captured” |
| L5 | failure/recovery tested | “injected failure and restored verified behavior in lab” |
| L6 | integrated portfolio proof | “end-to-end lab capability certified on final SHA” |

One component can be L5 while another remains L1. Never assign one blanket
level to the whole project without a component matrix.

### Prohibited inference

- L1 does not imply cloud correctness.
- L2 kind/Docker does not imply managed Kubernetes.
- L3 hosted CI does not imply cloud apply.
- A successful apply does not imply reliable operations.
- Backup creation does not imply restore.
- Reverted configuration does not imply rollback recovery.
- Synthetic lab operations do not imply customer production ownership.
- Azure governance design does not imply ExpressRoute/VPN/Application Gateway
  depth.
- An agent recommendation does not imply safe autonomous production mutation.

## 3. Freshness rules

Evidence is current only if all bindings match:

- candidate SHA;
- upstream lock hash;
- partition hash;
- validator implementation hash;
- relevant rubric hash;
- target environment and execution identity;
- required human receipt;
- post-remediation time.

After any code/config/policy/rubric/upstream fix:

1. earlier affected evidence is marked superseded;
2. narrow and full gates rerun;
3. hosted/cloud steps rerun where the claim needs them;
4. new outputs receive hashes;
5. reviews and judge loops restart on the new SHA;
6. README/status/claims tense is reconciled.

“Historically green” is context, not a current gate.

## 4. Evidence index

The generated summary index contains:

| Field | Purpose |
| --- | --- |
| Evidence ID | stable lookup |
| Capability | Kubernetes/serverless/etc. |
| Claim level | L0–L6 |
| Candidate SHA | exact code identity |
| Environment | where executed |
| Identity | sanitized principal/workload |
| Result | pass/fail/superseded |
| Raw artifact hashes | integrity |
| Related incident/change/issue | operational context |
| Current claim | exact allowed wording |
| Boundary | exact unsupported extension |

The summary is derived from events. It is never the only evidence.

## 5. Required operational evidence

### Kubernetes

- cluster/environment and execution identity;
- image digest, chart version, application SHA/version;
- pod/service/ingress health;
- probes, resources, HPA, non-root, RBAC/workload identity;
- policy-denial evidence;
- rollout and failure/recovery scenarios;
- post-recovery business smoke.

### Serverless

- function/queue/DLQ configuration sanitized;
- identity and IAM negative test;
- correlation trace;
- duplicate/idempotency result;
- retry/timeout/concurrency behavior;
- poison message, alarm, DLQ, replay, verification;
- cost/usage measures.

### Incident

- start/detection/acknowledgment/mitigation/recovery/end timestamps;
- symptom, hypotheses, evidence, decisions, ruled-out causes;
- root cause/contributing factors;
- user impact and communication draft;
- recovery verification and regression control.

### Recovery

- known-good target or first-release decision;
- backup source/time and recovery target;
- data integrity/checksum/record verification;
- restored digest/version/health/telemetry/business behavior;
- measured RTO/RPO;
- cleanup and remaining risk.

### Performance/cost

- repeatable test version and workload;
- before/after p50/p95/p99, errors, saturation, resources;
- root cause and change;
- cost assumptions, actual available usage, budget status;
- inventory and teardown reconciliation.

### Orchestration experiment

- Ralphy stream/partition, isolation and integration order;
- actual Opus/Grok/Codex model IDs and modes;
- Mandarin handoff validation;
- bottleneck dispatch, diagnosis, and bounded resolution;
- saved judge/nixer/fixer cohort rounds;
- fresh council results and escape findings;
- fresh repair cohort after any fresh-judge failure;
- proxy/direct token, latency, failure, and output-quality comparison where
  observable, without promising a quota multiplier.

### Recruiter visual

- draw.io source and exact render hashes;
- Image2 reference and final infographic hash;
- architecture/service/metric/claim parity review;
- root README render/link/alt-text validation;
- final evidence-index version used for all visible copy.

## 6. Initial claim matrix

All capabilities begin at L0 until implementation evidence exists.

| Capability | Initial level | Promotion requirement |
| --- | --- | --- |
| Upstream A/C integration | L0 | pinned contracts and cross-contract tests |
| Terraform cloud foundation | L0 | L1 static, L3 hosted plan, L4 applied |
| Managed Kubernetes | L0 | L2 kind, L4 EKS, L5 failure/recovery |
| Serverless | L0 | L1 tests, L4 live path, L5 DLQ recovery |
| SaaS operations | L0 | implemented lifecycle plus executed drills |
| Observability/SLO | L0 | live correlated signals and alert drills |
| Incident/network/Linux ops | L0 | executed reproducible incidents and recovery |
| Security/governance | L0 | enforced controls and negative tests |
| GitHub agentic workflow | L0 | hosted safe proposal plus rejection/approval proof |
| Backup/DR | L0 | isolated restore with RTO/RPO and business verification |
| Performance/FinOps | L0 | repeatable measurement, improvement, cost/teardown proof |

## 7. Portfolio wording templates

Use only after evidence reaches the stated level.

### L4/L5 Kubernetes and operations

> Deployed a digest-pinned SaaS workload to an isolated managed Kubernetes lab
> with Helm, workload identity, RBAC, network policies, probes, autoscaling, and
> protected GitHub OIDC delivery; injected and recovered from health, resource,
> DNS, and connectivity failures with evidence-linked runbooks.

### L4/L5 serverless and observability

> Operated a correlated Kubernetes-to-queue-to-serverless workflow with
> idempotency, bounded retries, DLQ replay, least-privilege IAM, metrics, logs,
> traces, SLO burn alerts, and tested poison-message recovery.

### L5 recovery/performance/cost

> Measured RTO/RPO through isolated backup restoration and verified data,
> release identity, telemetry, and business behavior; load-tested the service,
> removed a measured bottleneck, and implemented budgets, right-sizing, and
> evidence-preserving teardown controls.

### Agentic operations

> Built a GitHub-hosted incident-assistance workflow that gathers evidence and
> proposes bounded remediation while keeping mutation behind protected human
> approval; tested prompt injection, forged evidence, excessive scope, and
> unsafe-command rejection.

### Mandatory limitations paragraph

> ContinuityOps is an isolated synthetic-data cloud lab. It demonstrates
> implemented and tested engineering behavior described in the evidence index;
> it does not represent customer production tenure, enterprise scale,
> multi-account production ownership, or unimplemented Azure networking depth.
