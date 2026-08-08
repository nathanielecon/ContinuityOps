# Source Analysis and Design Rationale

## Repositories reviewed

### Project A

- [`PROJECT_A_PLAN.md`](https://github.com/nathanielecon/aws-landing-zone-lab/blob/main/project-a/PROJECT_A_PLAN.md)
- [`PROJECT_A_ADDITIONS.md`](https://github.com/nathanielecon/aws-landing-zone-lab/blob/main/project-a/PROJECT_A_ADDITIONS.md)
- [`orchestration.md`](https://github.com/nathanielecon/aws-landing-zone-lab/blob/main/project-a/docs/architecture/orchestration.md)
- [`BREAK_FIX_LOG.md`](https://github.com/nathanielecon/aws-landing-zone-lab/blob/main/BREAK_FIX_LOG.md)
- commit [`spec: add Project A gap-closure requirements`](https://github.com/nathanielecon/aws-landing-zone-lab/commit/5bd4fc0e2a3bbddb895412c05c2d8dcd9e31ac72)

### Project C

- [`PLAN.md`](https://github.com/nathanielecon/local-first-governed-cicd/blob/main/PLAN.md)
- [`AGENTS.md`](https://github.com/nathanielecon/local-first-governed-cicd/blob/main/AGENTS.md)
- [`docs/orchestration.md`](https://github.com/nathanielecon/local-first-governed-cicd/blob/main/docs/orchestration.md)
- [`STATUS.md`](https://github.com/nathanielecon/local-first-governed-cicd/blob/main/STATUS.md)
- [`ISSUES.md`](https://github.com/nathanielecon/local-first-governed-cicd/blob/main/ISSUES.md)
- [`DECISIONS.md`](https://github.com/nathanielecon/local-first-governed-cicd/blob/main/DECISIONS.md)
- Phase 2–4 retrospectives under [`docs/retrospectives/`](https://github.com/nathanielecon/local-first-governed-cicd/tree/main/docs/retrospectives)

The connected repositories are private. Links require repository access.

## Patterns retained

| Source pattern | ContinuityOps application |
| --- | --- |
| Project A sequential `A-001 -> A-007` Ralphy stream | One mutation-owning Ralphy controller with bounded task order |
| Terra first, Sol takeover thresholds | Adapted into one Codex implementation/repair pass followed by fresh-worker or bottleneck replacement with a compact evidence-only packet |
| Frozen per-slice rubrics | All S0–S8 rubrics frozen and hashed in Phase 0 |
| Three independent judges preferred | Exactly three fresh judges required for every slice and final council |
| Nixer/fixer/rejudge | Formal loop with issue IDs, fresh evidence, repinning, and new SHA |
| Bottleneck judge mode | Narrow CI clearance, then mandatory return to full council |
| Project A hash-bound approvals | Plan/execution/validator/rubric/partition hashes and human receipts |
| Project C authoritative JSON task plan | Machine-readable legal state transitions and phase authorization |
| Project C independent change/QA/security/evidence gates | Required before each slice council |
| Narrow write scopes and model routing | Task policy assigns risk, owner, scope, validators, evidence, and gate |
| Local-versus-external boundaries | Component-level L0–L6 evidence levels |
| Issue ledger and retrospectives | Append-only issues, break/fix log, and root-cause follow-ups |
| Attached standing AGENTS addendum | In-session bottleneck dispatch, cloud-agent/GitOps separation, Mandarin handoffs, and honest portfolio visual requirements |

## Problems explicitly designed out

### Rubrics restored after implementation

Project A disclosed that some rubrics were recreated mid-stream. ContinuityOps
freezes all rubrics before Phase 1 and invalidates certification if a rubric
must change.

### Single-judge rejudges treated as slice closure

Project A disclosed frequent single-judge rejudges during closeout. ContinuityOps
uses single-judge bottleneck mode only as a temporary diagnostic; a fresh
three-judge round is always required.

### Transcript leakage and score anchoring

Project A’s clean rejudge benefited from durable-artifact-only contexts.
ContinuityOps makes that the default for every judge and the final council.

### Claims tense drift

Project A’s live lab moved between `PENDING_APPLY` and `APPLIED`, and judges
caught stale language. ContinuityOps uses component claim levels plus automated
consistency review after any state-changing evidence.

### Credential/control-plane mismatch

Project A lost time attempting a Cloud Agent path without injected credentials,
then succeeded through GitHub OIDC. ContinuityOps selects GitHub OIDC as the
primary hosted control plane and fails fast on identity absence.

### Authorization-test drift

Project C repeatedly found the plan’s authorized phase and harness expectation
out of sync. ContinuityOps treats authorization update plus N/N+1 regression as
an atomic gate.

### Stale evidence after a fix

Project C’s Phase 2 retained a pre-remediation failing report while current code
passed. ContinuityOps invalidates evidence on any affected change and uses
append-only supersession.

### Local success mistaken for hosted/runtime success

Both projects maintained explicit offline/local/hosted/cloud boundaries.
ContinuityOps extends this to managed Kubernetes, serverless, recovery, and
agentic workflows.

### Hosted tool instability

Project C’s Trivy install path caused repeated hosted failure until replaced by
a maintained container path. ContinuityOps pins action/container/checksum
sources and distinguishes infrastructure failures from product/security
failures.

### Incomplete rollback and evidence history

Project C still records open future blockers for append-only release evidence,
authorization, and verified rollback. ContinuityOps does not assume those are
complete upstream; it creates explicit integration issues and requires digest,
health, version, data, telemetry, and business verification before claiming
recovery.

## Why the name ContinuityOps

The project is broader than monitoring or incident response. Its core hiring
signal is continuous operational ownership across deployment, runtime,
observation, failure, recovery, security, performance, and cost. “ContinuityOps”
is descriptive, portfolio-appropriate, and avoids implying an Azure Sentinel or
commercial security product.

## Deliberate differences from the examples

- The new plan certifies already-completed code partitions instead of assuming
  file presence equals completion.
- Judges require average ≥9.5, no judge <9.0, all must-haves, and three
  merge-ready verdicts.
- Evidence is event-based and append-only from the beginning.
- Upstream Projects A and C are immutable inputs, preventing a final-project
  scope explosion.
- Managed Kubernetes, serverless, SaaS operations, agentic workflow safety,
  recovery, performance, cost, and teardown are first-class judged slices.
- “10/10 preparedness” remains job-specific and cannot be manufactured by the
  rubric when employer-specific experience is absent.
- ContinuityOps permits several disjoint simultaneous Ralphy streams while each
  stream remains sequential; this explicitly overrides the Project A-specific
  single-stream rule for the new repository.
- A saved remediation council is experimentally retained until provisional pass,
  but fresh judges remain authoritative and fresh failures receive fresh repair
  cohorts.
- Claude cloud supervision, Grok council/orchestration roles, Codex 5.4 CLI
  `/fast` execution, Mandarin worker communication, optional pinned proxy, and
  TypeScript 7 are explicit project-level contracts.
- The final repository includes a draw.io-to-Image2, evidence-constrained,
  recruiter-first architecture visual instead of treating graphics as optional
  packaging.
