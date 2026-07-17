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
configuration, not inferred aliases.

- **Portfolio supervisor:** one Claude 5 cloud agent supervises the complete
  program under a minimal-intervention policy, maintains the integrated
  objective, approves stream creation/closure, and may appoint Claude Sonnet
  or Opus co-orchestrators for bounded streams. It reviews a stream branch
  only upon the orchestrator's durable completion signal (BF-PRE-015), and
  certifies at **stream boundaries only** — per-round checking belongs to the
  deterministic validators inside orchestration rounds, and actuation of
  orchestrator intents batches into evented wakes plus a 3–4h heartbeat
  (D-032). It does not replace deterministic gates or human approvals.
- **Ralphy orchestration and council reasoning:** the default carrier is an
  **episodic GPT round** — a Codex 5.4 Cloud task dispatched through the
  `codex-dispatch` queue that plays the lead orchestrator (and council roles:
  judges, nixers, fixers, bottleneck analysts) for one bounded round, returning
  work as a diff and holding zero credentials. Claude Opus 4.8 is retained as
  the **reserve seat**, enabled when a GPT round is unavailable or fails; a cold
  orchestrator reconstructs state losslessly from durable artifacts. The actual
  model ID of every round is recorded at dispatch, and the supervisor may record
  a task-specific exception (amends D-022; supersedes the earlier Grok 4.5 High
  Fast assignment; see D-030).
- **Code execution:** warm Codex 5.4 CLI Cloud Agents in default mode (not
  `/high`, not `/fast`) implement the project code and tests through bounded
  Ralphy tasks. "Warm" is a per-Environment toolchain cache (~12h), never
  credential material. The concrete specification (D-026):
  - one Codex Cloud Environment per repository, created in the Codex UI with
    caching On;
  - the two in-repo scripts `.codex/cloud-setup.sh` (Setup) and
    `.codex/cloud-maintenance.sh` (Maintenance) are the *only* content pasted
    into the Environment; they live in the repo and are change-controlled;
  - zero credentials in the container — adding any environment variable or
    secret to the Environment invalidates the ~12h cache and is out of bounds;
  - a warm gate (`scripts/Invoke-CodexCloudWarm.ps1`, control-center only) runs
    before every dispatch and re-warms via a smoke task when `lastWarmUtc` is
    missing or older than ~10h;
  - dispatch is `codex cloud exec --env <ENV_ID> --branch <branch> "<task>"`;
    the task never runs git itself, and the orchestrator owns integration.
  Warmth is isolated per Environment/repo and does not carry across repos.
  Workers report remaining context on every handoff; the orchestrator may
  retire a low-context worker and dispatch a fresh replacement. They edit
  repositories; they are not the live cloud apply control plane.
- **Claude execution location:** Claude agents run in cloud environments only.
  They do not rely on the user's laptop shell, browser session, cookies, or
  local cloud login.

The supervisor records the actual model ID, provider, mode, and role for every
dispatch. If a named model is unavailable, the task stops or uses a
human-approved substitution; agents never invent model availability.

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
- **App publish hard gate (D-033, empirically revised):** every App-path
  `@codex` prompt must include the completion contract from
  `docs/planning/dispatch/QUEUE.md`. Completion means a **GitHub-visible open
  PR URL**. Stopping at Codex UI `make_pr` / bot summaries is **incomplete**.
  App **sandboxes cannot publish** (`gh` missing; `git` to GitHub often
  `CONNECT 403`). The proven publish surfaces are: (1) Codex task-page
  **Create PR** (platform, outside sandbox) actuated by the cloud supervisor
  heartbeat, or (2) control-center `codex cloud apply` + push + `gh pr create`.
  Supervisor advances only on an observable PR; otherwise one re-nudge, then
  diagnose + Opus reserve (reasoning-only). Do not treat GHA `@codex` keepwarm
  as verified — App ignored `github-actions[bot]` mentions in smoke.
- **Warm freshness** is evidenced by the most recent Codex task timestamp on
  the keep-warm record (issue-based); the supervisor's scheduled self-checks
  post an `@codex` smoke roughly every 9 hours. The `%LOCALAPPDATA%` registry
  and `Invoke-CodexCloudWarm.ps1` warm gate apply only to the fallback path.
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

- **Portfolio supervisor:** owns integrated intent, stream topology, cross-stream
  dependencies, and final convergence.
- **Lead orchestrator:** selects ready work, checks dependencies and scopes,
  creates/joins Ralphy streams, dispatches roles, changes authoritative state
  atomically, logs break/fix events, and assembles gates. It does not self-
  approve high-risk work.
- **Co-orchestrator:** a Sonnet/Opus cloud agent appointed to one named stream;
  it has no authority over other streams or final certification.
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

- **Repository type:** This is a planning/governance repository at Phase 0
  bootstrap. There is no application service, no dependency manifest
  (`package.json`/`requirements.txt`/`go.mod`), and no committed build/test/lint
  configuration. The "deliverables" are the Markdown governance docs, the
  machine-readable JSON contracts (`PLAN.md` task authority, `OPERATING_STATE.md`
  state/issues, `integration/upstreams.lock.json` upstream pins), and the
  architecture assets in `docs/architecture/`. Do not fabricate a build system or
  claim runtime capability; implementation begins only when a human advances
  `authorized_through_phase` per `PLAN.md`.
- **Pre-installed runtimes (no install needed):** Node 22, npm 10, Python 3.12,
  Go 1.22, and `jq`. The update script is intentionally a near no-op because
  there are no dependencies to install yet; it only installs deps if a manifest
  later appears.
- **Validate the contracts (the closest thing to a test suite):** parse every
  standalone `*.json` and every fenced ```json block embedded in the Markdown
  (all 12 currently parse). This is the core "does the repo still hold together"
  check. `python3 -c "import json"` is sufficient; no framework is installed.
- **Expected Phase-0 link gaps:** internal Markdown links to `evidence/*`
  subdirectories (hosted/slices/postbuild/judges) and the root-relative links
  inside `docs/planning/REPO_README_TEMPLATE.md` do NOT resolve yet by design —
  those namespaces/assets are created in later phases. Only `evidence/README.md`
  exists today. Treat these as known-not-yet-created, not as regressions.
- **Render the architecture diagram (build/run demo):** the README Mermaid block
  renders with `npx --yes @mermaid-js/mermaid-cli -i <file>.mmd -o out.png`; its
  bundled Chromium works headless in this VM with no extra system libs. The
  committed renders (`docs/architecture/continuityops-architecture.{png,svg}`,
  `continuityops.drawio`) are valid and the drawio XML is well-formed.
- **No secrets required** for planning/validation work in this environment.
