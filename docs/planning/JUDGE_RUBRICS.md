# ContinuityOps Frozen Judge Rubric Pack

Copy each slice section into a separate immutable file under
`harness/rubrics/` during Phase 0 and record its SHA-256. A rubric setter may
clarify exact repository paths and commands before freeze, but must preserve the
capability and claim boundaries below.

## Universal scoring contract

Every judge scores only the exact committed candidate SHA and supplied evidence
manifest.

### Universal must-haves

`U1` Candidate SHA, rubric hash, evidence manifest hash, upstream pins, and
partition hash agree.  
`U2` All required deterministic and hosted checks pass on the candidate.  
`U3` No secret, long-lived credential, sensitive synthetic payload, or
untrusted-PR credential exposure.  
`U4` No open critical/high security issue affecting the slice.  
`U5` Claims distinguish designed, static-validated, local-runtime,
hosted-validated, cloud-applied, and recovery-tested states.  
`U6` Negative/failure behavior is tested where the slice requires it.  
`U7` Evidence is fresh after the last fix and includes commands, exit codes,
time, environment, identity, tool versions, and hashes.  
`U8` Write scopes, approvals, and upstream preservation rules were obeyed.  
`U9` Break/fix history records every observed failure and verified repair.  
`U10` Documentation, diagrams, status, evidence, and README tense agree.

`U11` Every worker handoff and inter-agent message uses Simplified Chinese while
external recruiter artifacts remain English.  
`U12` Concurrent Ralphy streams are disjoint, sequential internally, and merged
only through the integration queue.  
`U13` Saved remediation councils are separated from authoritative fresh judges;
fresh-judge failures receive fresh nixers/fixers.  
`U14` Every observed failure is present in the break/fix log before closure.

Any failed or unproven universal must-have forces `merge_ready: no` regardless
of numeric score.

### Universal dimensions

Each slice has ten weighted points. Score each dimension from 0 to its maximum.

- `Correctness and completeness` — 2.0
- `Security and authority boundaries` — 1.5
- `Failure/recovery depth` — 1.5
- `Deterministic test quality` — 1.0
- `Live/runtime evidence quality` — 1.0
- `Operability and troubleshooting` — 1.0
- `Evidence/claim integrity` — 1.0
- `Maintainability and handoff` — 0.5
- `Cost/performance realism` — 0.5

Judges must cite evidence for every scored dimension. File presence alone is not
proof.

### Exit rule

- three independent judges;
- all universal and slice must-haves pass for all judges;
- mean score ≥9.5;
- no judge score <9.0;
- all three return `merge_ready: yes`.

## S0 — Authority and harness

### Must-haves

`S0-M1` Every retained path has exactly one slice owner; shared interfaces and
dependency invalidation are explicit.  
`S0-M2` CLI enforces legal lifecycle, revision checks, and authorized phase.  
`S0-M3` Current authorized phase succeeds and next phase is rejected.  
`S0-M4` Validator IDs are allowlisted/pinned; unknown IDs fail closed.  
`S0-M5` Validators are check-only and completion reconciliation catches late
scope/isolation violations.  
`S0-M6` Workers cannot mint receipts or adapter evidence.  
`S0-M7` Plan, execution, validator, rubric, and partition hashes are bound.  
`S0-M8` Concurrent disjoint streams, sequential in-stream execution, Codex
worker replacement, and bottleneck dispatch are demonstrated on harmless
fixtures.  
`S0-M9` Judge isolation and output schema are tested.  
`S0-M10` H0 is bound to exact bundle and no cloud call occurred.

`S0-M11` Opus/Grok/Codex model roles, actual IDs, cloud-only Claude location,
Mandarin protocol, and bottleneck profiles are enforced.  
`S0-M12` The optional pinned Claude proxy has integrity/policy/credential checks,
measurement, direct fallback, and no guaranteed multiplier claim.  
`S0-M13` TypeScript usage is pinned to stable 7.x and strict validation.

### 10/10 indicators

- hermetic cross-platform harness fixtures;
- tampered evidence/approval/hash tests;
- crash/resume and atomic-write recovery tests;
- deterministic error normalization;
- fresh-machine bootstrap parity.

## S1 — Cloud foundation and hosted delivery

### Must-haves

`S1-M1` A/C pins and consumed contracts are verified; upstream repos remain
unmodified.  
`S1-M2` Terraform state is remote, encrypted, versioned, locked, and separated
by environment.  
`S1-M3` OIDC trust and least-privilege roles are explicit and negatively tested.  
`S1-M4` PR jobs have no deployment credentials; actions are pinned.  
`S1-M5` Mutation requires protected environment and human receipt.  
`S1-M6` Network/data/trust boundaries and cost drivers are inspectable.  
`S1-M7` Harmless invalid change is blocked by hosted validation.  
`S1-M8` Hosted pass evidence is tied to candidate SHA.  
`S1-M9` Drift and teardown paths exist but do not grant unauthorized deletion.  
`S1-M10` Local validation is not described as live cloud proof.

### 10/10 indicators

- plan review identifies identity and cost changes;
- OIDC conditions bind repository/ref/environment;
- state recovery and lock contention are tested safely;
- runner/tool parity and pinned scanner paths are reproducible.

## S2 — Managed Kubernetes

### Must-haves

`S2-M1` Immutable image digest and release identity are verified.  
`S2-M2` Probes, resource requests/limits, PDB, topology behavior, and HPA are
implemented and tested.  
`S2-M3` Workload identity, RBAC, secrets, non-root runtime, and network policies
are least privilege and negatively tested.  
`S2-M4` Helm/schema/policy/static gates pass.  
`S2-M5` Local kind proof and managed EKS proof are clearly separated.  
`S2-M6` Managed runtime shows digest, health, version, identity, rollout, and
scaling on candidate SHA.  
`S2-M7` CrashLoop, readiness, scheduling/resource, DNS, and network-denial
failures are reproduced.  
`S2-M8` Every failure is reset and business behavior is reverified.  
`S2-M9` Ingress/TLS/load-balancer boundary is accurate.  
`S2-M10` Cluster cost and teardown implications are explicit.

### 10/10 indicators

- measurable autoscaling behavior under load;
- disruption/rollout behavior across failure;
- policy admission blocks unsafe workload;
- pressure-usable operator steps with diagnostic evidence.

## S3 — Serverless and SaaS operations

### Must-haves

`S3-M1` End-to-end Kubernetes request→queue→function→result correlation exists.  
`S3-M2` Idempotency, duplicate safety, bounded retry/backoff, visibility timeout,
concurrency, and timeout behavior are tested.  
`S3-M3` DLQ alarm, poison-message capture, safe replay, and post-replay
verification are executed.  
`S3-M4` Function IAM is least privilege with negative tests.  
`S3-M5` Tenant boundary and isolation assumptions match implementation.  
`S3-M6` Onboarding, configuration, migration, support, suspension, export, and
deprovisioning have safe operating contracts.  
`S3-M7` Severity, ownership, escalation, maintenance, and communication paths
are usable.  
`S3-M8` Event payloads and logs are redacted.  
`S3-M9` Per-event/idle cost and scaling limits are described accurately.  
`S3-M10` “SaaS operations” is not overstated beyond the lab evidence.

### 10/10 indicators

- race/duplicate and partial-failure tests;
- replay audit trail;
- tenant quota/abuse behavior;
- measured latency/cost consequences of retry and concurrency choices.

## S4 — Observability and SLOs

### Must-haves

`S4-M1` A request is traceable across ingress, application, queue, and function.  
`S4-M2` Structured logs, metrics, traces, and alerts use consistent correlation.  
`S4-M3` Dashboards answer service, Kubernetes, serverless, dependency, and cost
questions rather than display vanity metrics.  
`S4-M4` Alerts include owner, severity, runbook, condition, deduplication, and
recovery condition.  
`S4-M5` SLIs/SLOs, windows, burn rates, error budget, and maintenance exclusions
are mathematically coherent.  
`S4-M6` Signal redaction tests prevent secrets/tenant payload leakage.  
`S4-M7` Missing telemetry, noisy alert, and trace discontinuity are tested.  
`S4-M8` At least one investigation moves from misleading symptom to root cause.  
`S4-M9` Alert fire and resolution are live-evidenced.  
`S4-M10` Telemetry retention and cost tradeoffs are explicit.

### 10/10 indicators

- multi-window burn alert validation;
- telemetry failure does not silently mask service failure;
- quantified alert quality/noise improvement;
- dashboard/runbook navigation tested by an independent operator.

## S5 — Incident, Linux, and network operations

### Must-haves

`S5-M1` All eight required incident drills exist and are reproducible.  
`S5-M2` At least two begin with misleading symptoms.  
`S5-M3` Each drill records timeline, hypotheses, evidence, ruled-out causes, root
cause, recovery choice, and verification.  
`S5-M4` Linux/process/log/config/permission diagnosis is demonstrated safely.  
`S5-M5` DNS, TLS, load-balancer, route, flow-log, security boundary, and app-vs-
network isolation logic are demonstrated.  
`S5-M6` Runbooks provide first-five-minute steps, exact commands, escalation,
rollback triggers, and “do not do this yet” cautions.  
`S5-M7` Rollback/remediation/failover/restore/rebuild choices are distinguished.  
`S5-M8` Every scenario resets and passes post-recovery business smoke.  
`S5-M9` Postmortems add regression controls rather than blame.  
`S5-M10` Independent operator dry-run succeeds.

### 10/10 indicators

- concurrent/multi-layer failure isolation;
- measured detection/acknowledgment/recovery timeline;
- one initially plausible diagnosis is disproven with evidence;
- runbook safely limits blast radius under pressure.

## S6 — Security, governance, and agentic operations

### Must-haves

`S6-M1` IAM/RBAC/workload identities are least privilege and negatively tested.  
`S6-M2` Secrets are managed, rotatable, redacted, and absent from source/evidence.  
`S6-M3` SBOM and source/dependency/image/IaC scanning are reproducible; findings
are triaged, not hidden.  
`S6-M4` Unsafe cloud/Kubernetes changes are policy-blocked.  
`S6-M5` Azure governance controls are concrete and implemented-versus-designed
claims are explicit.  
`S6-M6` Agent workflow is read-mostly by default and has no uncontrolled
production mutation.  
`S6-M7` Mutation requires protected human approval and short-lived credentials.  
`S6-M8` Prompt injection, untrusted text, forged/stale evidence, malicious
command, excessive scope, and secret request are rejected.  
`S6-M9` Agent decisions/actions are auditable and rollback-aware.  
`S6-M10` No critical/high security issue remains.

### 10/10 indicators

- explicit threat model and attacker paths;
- artifact attestation/signature verification;
- policy enforcement at multiple layers without conflicting authority;
- agent cannot convert diagnostic permissions into mutation authority.

## S7 — Resilience, performance, and FinOps

### Must-haves

`S7-M1` RTO/RPO are justified and measured.  
`S7-M2` Backup is restored into isolation and data integrity is verified.  
`S7-M3` Rollback verifies digest, health, version, telemetry, and business
behavior; first-release behavior is explicit.  
`S7-M4` Dependency and infrastructure failure recovery is safely executed.  
`S7-M5` Load profile is repeatable with p50/p95/p99, errors, saturation, scaling
lag, and resource measures.  
`S7-M6` One bottleneck is root-caused and the improvement is quantified.  
`S7-M7` Cost model, budgets, alerts, tags, right-sizing, idle detection, and
anomaly response exist.  
`S7-M8` Actual lab cost is captured where available and estimates state their
assumptions.  
`S7-M9` Teardown inventory/reconciliation proves expected removal without
destroying evidence.  
`S7-M10` Reliability-versus-cost tradeoff is explicit.

### 10/10 indicators

- recovery under partial dependency failure;
- data-consistency checks beyond “endpoint returns 200”;
- statistically sensible performance comparison;
- cost/performance/reliability decision ties to measured evidence.

## S8 — Integrated delivery

### Must-haves

`S8-M1` Every slice remains valid on final integrated SHA.  
`S8-M2` Append-only evidence events reconcile to summary manifests with no
unexplained drift.  
`S8-M3` All local and hosted required checks pass on final SHA.  
`S8-M4` Architecture, runbooks, evidence, status, costs, teardown, and claims
agree.  
`S8-M5` Every portfolio claim maps to evidence IDs and claim level.  
`S8-M6` Simulated, local, hosted, applied, recovered, and torn-down components
are distinguished.  
`S8-M7` Operator quick start and demo can be followed without chat history.  
`S8-M8` Break/fix log and process deviations are complete.  
`S8-M9` Final judges have clean contexts with no prior scores/transcripts.  
`S8-M10` Human H6 owns merge and publication.

`S8-M11` Final code was logically repartitioned from its dependency graph and
every partition passed saved-remediation plus fresh-judge certification.  
`S8-M12` Editable draw.io source, exact render, and polished 16:9 infographic
agree with the final architecture and evidence.  
`S8-M13` Root README is resume-ready, visual-first, recruiter-scannable in under
60 seconds, and links claims/metrics to evidence.  
`S8-M14` Infographic footer and README clearly distinguish synthetic lab proof
from sustained customer-production ownership.

### 10/10 indicators

- one coherent end-to-end narrative from infrastructure to recovery;
- evidence navigation is fast and content-addressed;
- an independent reviewer can reproduce core validation;
- limitations increase credibility rather than hiding gaps.
