# ContinuityOps Agent Contract

## Authority order

When sources conflict, use this order:

1. explicit human instruction and signed human approval receipts;
2. `PLAN.md` machine-readable task authority;
3. frozen slice rubric and task policy;
4. `OPERATING_STATE.md` current state and open issues;
5. `RALPHY_ORCHESTRATION.md`;
6. `MASTER_PLAN.md`;
7. other documentation.

Chat history is never authoritative. A new orchestrator must reconstruct state
from durable repository artifacts.

## Model and execution topology

ContinuityOps uses a layered control plane. Model names are explicit runtime
configuration, not inferred aliases. **D-041** splits supervision into chief
and junior. **Actuation** means performing the GitHub/repo action (mention,
merge, label, close); **judgment** means deciding whether that action should
happen.

- **Owner (human):** constitutional gates only — H0–H6, credentials/secrets,
  spend ceilings, destructive/irreversible operations, external-to-repo
  publication. Not an agent seat.
- **Chief supervisor:** one cloud agent session (this seat) owns the integrated
  objective at **stream boundaries and escalations only** (BF-PRE-015 / D-032
  as amended by D-041). It does **not** perform steady-state actuation. It
  replaces the junior supervisor when that seat is context-dead or stuck, and
  may pipe true constitutional crises to the owner. See
  `docs/planning/dispatch/CHIEF_SUPERVISOR.md`.
- **Junior / orch / reviewer / workers / monitor (D-043):** all episodic seats
  use **`cursor-grok-4.5-high`** effective immediately (owner directive). Codex
  App `@codex` / GPT implementation path is **suspended** for product work.
  Chief dispatches Grok subordinates in-session and merges on CI green +
  independent Grok reviewer `verdict: pass`. See
  `docs/planning/dispatch/JUNIOR_SUPERVISOR.zh.md`.
- **Pipeline monitor:** read-only Grok subagent reporting **significant**
  findings only to the **chief supervisor**. See
  `docs/planning/dispatch/MONITOR.zh.md`.
- **Ralphy orchestration (D-043):** Grok episodic rounds. Orchestrator validates
  rounds, advances state up to `review`, owns break/fix, prepares contracts; it
  **emits intents** and never merges/approves PRs. Engagement: **no Opus**.
- **D-037 reviewer (D-043):** independent Grok round per worker PR — apply
  patch, run declared checks, structured `verdict` only. No code edits; no merge.
- **Code execution (D-043):** Grok Cursor cloud/subagent workers implement
  bounded tasks. Codex Cloud Environment (D-026) remains registered but is not
  the default worker carrier while D-043 stands. Workers report
  `context_remaining` every handoff; managerial seats replace low-context workers.
- **Claude execution location:** Claude agents run in cloud environments only
  when used; they do not rely on the owner's laptop shell or local cloud login.

Every dispatch records actual model ID, provider, mode, and role. If a named
model is unavailable, the task stops or uses a human-approved substitution;
agents never invent model availability.

### Dispatch topology

The owner's Windows control-center session (local Claude Code with codex-cli,
`pwsh`, and the machine-local `environments.json` registry) is the **sole
dispatch point** (D-027). The warm gate and every `codex cloud exec` run only
there. Cloud containers and cloud workers are **receive-only**: they never run
the warm gate, never attempt `codex cloud exec`, and never hold Codex
credentials. **`codex login` inside any cloud container is prohibited** — it is
equivalent to the rejected CO-005; the container never authenticates Codex.

Dispatch runs through the Codex GitHub App, triggered by the cloud supervisor
(D-031, amending D-027/D-029):

- **Primary path — `@codex` mention on a queue issue.** The supervisor (or the
  cloud orchestrator via the supervisor's bookkeeping) authors a durable
  `codex-dispatch` GitHub issue carrying the task contract pointer, target
  branch, and constraints, then posts an `@codex` mention to trigger the App.
  A mention is a valid dispatch only on a queue issue authored by the
  supervisor or the owner. Results flow back as Codex-created PRs/branches;
  the supervisor integrates into **stream branches only** — `main` merges and
  all D-012 gates remain human.
- **App publish hard gate (D-034):** every App-path `@codex` prompt must include
  [`docs/planning/dispatch/CODEX_DISPATCH_SNIPPET.zh.md`](docs/planning/dispatch/CODEX_DISPATCH_SNIPPET.zh.md).
  Workers must end with `<!-- continuityops-patch-v1 -->`, `base_branch`,
  `base_sha`, and a full fenced unified diff. GitHub Actions
  `codex-patch-publish` mechanically applies the patch with `GITHUB_TOKEN` and
  opens the PR (primary overnight path). App sandboxes still cannot
  `git push`/`gh` — **D-042** extends the same rule to junior merges/dispatches:
  intent markers → `.github/workflows/junior-actuate.yml`. Platform **Create PR**
  and `scripts/Publish-CodexCloudTask.ps1` are **fallbacks**. **Heartbeat:**
  review PRs / `publish-ok`; re-nudge if bot reply lacks the patch marker; on
  `publish-failed` use fallback (engagement: no Opus). For every worker PR,
  D-037 adds an independent GPT reviewer round. Junior merge signal is **CI
  green + reviewer verdict pass**, actuated via `continuityops-merge-v1`. Repair
  findings go to an independent fixer round, not the reviewer. Never treat
  `make_pr` text alone as complete. Warm-cloud heartbeat: issue #4 stamp; smoke
  when older than ~10h; never dispatch real work into a cold environment.
- **Warm freshness** is cloud-native and evidenced by the most recent Codex
  task timestamp on the keep-warm record (issue #4); the supervisor heartbeat
  posts an `@codex` smoke when the stamp is older than >9h. The
  `%LOCALAPPDATA%` registry and `Invoke-CodexCloudWarm.ps1` warm gate apply only
  to the fallback path.
- **Fallback path — control-center sweep.** The owner's Windows session (codex
  CLI + keychain + registry) runs the classic run sheet (warm gate →
  `codex cloud exec` → diff/apply/push) when the App path is unavailable.

Cross-repo rule: **the worker gets data, not permission** (D-028) — the control
center supplies upstream material per task via context packaging or a read-only
vendored snapshot, never by widening a worker container's repository grants.

### Optional Claude proxy profile

Cloud Claude agents may use the pinned `pxpipe-proxy@0.9.0` profile:

```bash
npx --yes pxpipe-proxy@0.9.0
export ANTHROPIC_BASE_URL=http://127.0.0.1:47821
```

This is an experiment, not a guaranteed quota multiplier. Before activation:

- verify package integrity and repository provenance;
- confirm provider, organization, and security policy permit its use;
- keep credentials out of proxy logs and repository artifacts;
- test direct and proxied health paths;
- measure input-token, latency, failure, and quality effects;
- retain a direct-provider fallback;
- never weaken judge independence or evidence fidelity because context is
  rendered/compressed.

### Language protocol

All worker assignments, updates, retained handoffs, orchestration messages,
supervisor↔orchestrator communication, and all other inter-agent communication
are in **Simplified Chinese only**. External
repository artifacts intended for recruiters—including code comments where
appropriate, README, diagrams, runbooks, evidence indexes, portfolio copy, and
resume wording—remain English.

Required worker handoff field names may stay in English for machine parsing,
but every free-text value must be Simplified Chinese.

## Roles

- **Chief supervisor:** owns integrated intent at stream boundaries and
  escalations only (D-041); replaces junior when needed; does not steady-state
  actuate.
- **Junior supervisor:** owns day-to-day supervision and actuation (D-041);
  reports to chief; replaces orch/reviewer/monitor on low context.
- **Lead orchestrator:** selects ready work, checks dependencies and scopes,
  creates/joins Ralphy streams, prepares dispatch intents, changes
  authoritative state atomically up to `review`, logs break/fix events, and
  assembles gates. It does not merge/approve PRs or self-approve high-risk work.
- **Co-orchestrator:** optional bounded stream co-lead when appointed; no
  authority over other streams or final certification. Engagement: no Opus.
- **Codex implementation worker:** executes the bounded code/test task in `/fast`
  mode within a stream.
- **Rubric setter:** read-only reviewer who freezes a checkable slice rubric
  before implementation.
- **Judge:** independent, read-only scorer. Judges do not see implementation
  transcripts, previous scores, thresholds as targets, or other judge reports.
- **Nixer:** read-only gap analyst who converts failed rubric findings into
  deduplicated, reproducible issue records.
- **Fixer:** bounded implementation worker assigned disjoint issue IDs and a
  narrow write scope.
- **QA reviewer:** independently executes approved checks and preserves raw
  evidence; it does not repair code.
- **Security reviewer:** independently evaluates identities, secrets, supply
  chain, network boundaries, untrusted inputs, and authority expansion.
- **Evidence reviewer:** checks evidence freshness, commit binding, hashes,
  claims, and cross-artifact consistency.
- **Bottleneck subagent:** a short-lived specialist dispatched in the same
  supervisory session for authentication, hosted CI, cloud identity, Kubernetes,
  observability/dashboard, browser, or toolchain blockers. It diagnoses and
  returns a bounded handoff; it does not silently expand authority.

Record actual runtime model identifiers at dispatch. Historical role names such
as Terra/Sol may appear in imported Project A evidence but are not the default
ContinuityOps routing contract.

## Thin-orchestrator prohibitions

The orchestrator must not:

- implement routine task code;
- mint human approval receipts;
- grant itself credentials or expand cloud/GitHub authority;
- weaken validators, delete failing tests, or edit rubrics merely to raise a
  score;
- give untrusted pull-request jobs write tokens, cloud credentials, or secrets;
- permit judges to modify implementation;
- disclose prior judge scores or desired thresholds to a judge;
- combine overlapping fixer scopes;
- claim hosted, cloud, production, rollback, recovery, or security behavior
  without evidence at the required claim level.

## Worker handoff schema

Every worker returns this exact shape. Empty values are empty lists, not omitted.

```yaml
task_id:
role:
status: complete|blocked|waiting_human|failed
candidate_sha:
baseline_sha:
completed: []
modified_files: []
validation_commands: []
validation_results: []
failed_checks: []
remaining_risks: []
issue_ids: []
evidence_paths: []
recommended_next_step: []
requires_escalation: false
context_remaining: percent_or_token_estimate
```

The orchestrator rejects a handoff if:

- a changed path is outside `write_scope`;
- the candidate SHA or baseline SHA is absent;
- a validation result lacks command, exit code, time, and evidence path;
- a blocked/failed result lacks a reproducible failed check;
- an escalation lacks an issue ID;
- secrets or user/customer data appear in evidence;
- the worker directly changed authoritative task state;
- `context_remaining` is absent (the orchestrator uses it to decide whether to
  retire the worker and dispatch a fresh replacement).

## Write and concurrency rules

- Several Ralphy streams may run simultaneously after interfaces and partition
  ownership are frozen. The default ceiling is three implementation streams
  plus the portfolio supervisor; the supervisor may lower it when integration
  risk rises.
- Each individual Ralphy stream is sequential and has one mutation owner.
- Concurrent streams require disjoint partition paths, dependency-safe
  interfaces, isolated branches/workspaces, distinct evidence namespaces, and
  an integration-queue order recorded before dispatch.
- No stream may merge itself. The lead orchestrator validates and serializes
  integration into the candidate branch.
- Independent judges may run concurrently because they are read-only and write
  to distinct report paths.
- QA, security, and evidence reviews may run concurrently only after the exact
  candidate commit is frozen.
- A shared schema, interface, Helm values contract, Terraform output, workflow,
  evidence manifest, or authoritative state edit freezes dependent lanes.
- Workers never communicate directly. The orchestrator mediates through durable
  artifacts and Mandarin-only handoffs.

## Retry, fresh repair, and bottleneck dispatch

A Codex implementation worker gets one implementation and one repair pass on a
normalized error. After two same-class failures, no meaningful diff, 25 active
minutes, scope escape, security ambiguity, or an unreachable tool/control
plane, the lead orchestrator must dispatch a bottleneck subagent or a fresh
replacement worker rather than leaving the user to open a new conversation.

The packet contains only task contract, current diff, failing evidence, issue
IDs, exact checks, allowed paths, and claim ceiling. After a fresh clean-room
judge failure, prior nixers/fixers are retired and a new nixer/fixer cohort is
required.

## Immediate human gates

Stop and request human action for:

- production or shared-account deployment;
- new or changed cloud/GitHub credentials, OIDC trust, role assumption, or
  branch/environment protection;
- destructive data migration, restore over authoritative data, or teardown of
  resources outside the isolated lab;
- cost-cap increase;
- external/customer communication;
- acceptance of residual critical/high security risk;
- any scope or architecture change that materially changes the approved plan.

## Delivery invariants

- Build once; promote an immutable digest. Tags are aliases, never identity.
- Use GitHub OIDC and short-lived cloud credentials for hosted cloud operations.
- Keep development, staging, lab-production, and destructive-test boundaries
  explicit.
- Every repair invalidates earlier candidate-bound evidence and judge results.
- Every remediation is followed by fresh full validation and fresh independent
  judging.
- Backups are not proven until restore is tested.
- Rollback is not proven until digest, health, version, telemetry, and business
  behavior are verified after restoration.
- An agent may recommend a production mutation but may not execute it without a
  protected human approval gate.
- When TypeScript is used, pin stable TypeScript 7.x (initial verified baseline
  `typescript@7.0.2`), use strict type checking, and record any version change
  through an explicit dependency decision and full revalidation.
- Maintain `BREAK_FIX_LOG.md` continuously; no stream or judge loop closes while
  an observed break remains unrecorded.

## Cursor Cloud specific instructions

Durable, non-obvious notes for future cloud agents working in this environment.

- **Repository type:** ContinuityOps governance + in-repo L1 contracts through
  Phases 0–8 on `main` (`portfolio-certified-L1`). Live L4+ cloud apply is not
  performed inside this Cursor cloud VM by default (see Paste / BF-2026-010).
- **Pre-installed runtimes:** Node 22, npm 10, Python 3.12, Go 1.22, and `jq`.
  Install task-specific CLIs (`aws`, `terraform`, `helm`, etc.) only when a
  path that can actually use them is available (GHA OIDC or local bottleneck).
- **Validate:** `node --test tests/`; `node scripts/project.mjs validate <task>`;
  parse standalone `*.json` and fenced ```json blocks in Markdown.
- **Architecture renders:** Mermaid via
  `npx --yes @mermaid-js/mermaid-cli`; committed
  `docs/architecture/continuityops-architecture.{png,svg}` and
  `continuityops.drawio` remain authoritative visuals.
- **No secrets in the Codex/Cursor Environment** for warm cache (D-026). Repo
  work does not require AWS keys in this VM.

### What actually fixed live AWS (2026-07-14/15) — not Cursor STS

| Path | Evidence |
| --- | --- |
| **GitHub OIDC → `project-a-lzlab-gha`** | Role last used **2026-07-15**; successful `landing-zone-lab.yml` runs; live lab evidence under `assumed-role/project-a-lzlab-gha` |
| **`CursorCloudAgent` injection** | Role created Jul 14; **never assumed** (`RoleLastUsed` empty; CloudTrail only `CreateRole` / `AttachRolePolicy`) |

The prior “fix” was **change apply control plane** (GHA OIDC / local bottleneck), **not** finishing Cursor role injection. BF-2026-010 `NoCredentials` in this Cloud seat is real and expected on Pro+.

### Paste for stuck agents

```text
NoCredentials is expected on Pro+ without team External ID. CursorCloudAgent has never been assumed.
Prior fix (2026-07-14/15): GitHub OIDC → project-a-lzlab-gha via landing-zone-lab.yml, or local aws login bottleneck.
Do not block on CURSOR_AWS_ASSUME_IAM_ROLE_ARN. Escalate live AWS to GHA or local; continue repo-only here.
```

Account binding (not a secret): `000000000000` /
`arn:aws:iam::000000000000:root`. Default CI role:
`arn:aws:iam::000000000000:role/project-a-lzlab-gha`. See BF-2026-010.

### AWS injection stop table (Cloud seat)

```bash
env | grep AWS_PROFILE
aws sts get-caller-identity
```

| Observation | Action |
| --- | --- |
| Caller ARN contains `assumed-role/CursorCloudAgent` | Rare on Pro+; only if Teams External ID path was completed. Proceed; record identity (no secrets). |
| `NoCredentials` / `AWS_PROFILE` unset / no `~/.aws/config` | **STOP.** Injection absent — stop; no keys. Do not invent keys or put long-lived keys in Cloud secrets. |
| Live AWS still needed | **1)** GHA OIDC (`gh workflow run landing-zone-lab.yml --repo nathanielecon/cloud -f action=plan|apply` with `AWS_ROLE_ARN_LZ_LAB` / `project-a-lzlab-gha`); **2)** local `aws login` bottleneck (laptop); **3)** Teams External ID + trust update only if insisting on in-pod AWS. Cloud seat continues **repo-only** until (1) or (2) runs. |

Verified 2026-07-18 this seat: `AWS_PROFILE=<unset>`, STS `NoCredentials`, `CURSOR_AWS_ASSUME_IAM_ROLE_ARN` set → **injection absent — stop; no keys.**

Workaround detail (order): (1) proven GHA OIDC; (2) proven local bottleneck; (3) Teams → Settings → **Bedrock IAM Role** → Validate & Save → External ID into `CursorCloudAgent` trust → **new** Cloud Agent pod. Role may trust `arn:aws:iam::289469326074:role/roleAssumer` without External ID condition — Cursor still will not inject without team External ID UI (Pro+ has neither panel).