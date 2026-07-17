# ContinuityOps Initial Operating State

This file is the planning-package seed. The implementation repository should
split the machine-readable blocks into `STATUS.md`, `ISSUES.md`, and
`DECISIONS.md` and mutate them only through the project CLI.

## Status

```json
{
  "schema_version": "1.0",
  "revision": 16,
  "project": "ContinuityOps",
  "current_phase": 0,
  "authorized_through_phase": 0,
  "current_gate": "phase-0-baseline-audit",
  "running_tasks": [],
  "blocked_tasks": ["P0-T02", "P0-T03", "P0-T04", "P0-T05"],
  "waiting_human": [
    "H0-after-P0-T04"
  ],
  "codex_cloud_environment": {
    "repo": "nathanielecon/ContinuityOps",
    "env_id": "6a594ee667608191ab53cae15202815e",
    "cache": "on",
    "registered": true,
    "first_warm": true,
    "secrets": "none"
  },
  "completed_gates": [],
  "next_actions": [
    "D-034 smoked: issue #12 → GHA apply/push → PR #13; rerun idempotent publish-skipped; keep Actions create-PR permission on",
    "Supervisor heartbeat: review PRs / publish-ok; re-nudge if bot lacks continuityops-patch-v1; Create PR / Publish-CodexCloudTask.ps1 are fallbacks only",
    "Integrate GitHub-visible PRs into stream/orchestrator branches; do not treat make_pr text as complete",
    "Keep-warm: supervisor-authored @codex on issue #4 ~9h; GHA bot keepwarm stays disabled",
    "Do not authorize Phase 1 until S0 and H0 pass"
  ],
  "completed_bootstrap": [
    "Created ContinuityOps GitHub repository home",
    "Copied planning package into docs/planning/",
    "Installed root contracts and architecture assets",
    "Merged .codex Codex Cloud Environment scripts to the default branch",
    "Created, registered, and first-warmed the ContinuityOps Codex Cloud Environment (env 6a594ee667608191ab53cae15202815e, zero secrets)",
    "Rotated the orchestrator seat per D-024: predecessor retired at ~17% context_remaining; successor Opus 4.8 reconstructed state from durable artifacts only",
    "D-033: platform Create PR publish path verified (2026-07-17) after App sandbox self-publish failed (PRs #8–#11)",
    "D-034: patch-in-comment GHA publisher smoked (issue #12 → PR #13; Actions create-PR permission required)"
  ],
  "verified_baseline": [],
  "unverified": [
    "All ContinuityOps implementation and runtime capabilities",
    "Cross-repo Project A/C context packaging by the control center (CO-006)"
  ]
}
```

## Decision register

| ID | Decision | Status | Consequence |
| --- | --- | --- | --- |
| D-001 | Rename Project F to ContinuityOps — Cloud Reliability and Recovery Platform | accepted | Portfolio uses a descriptive professional identity |
| D-002 | Preserve Projects A and C as pinned upstream references | accepted | Integration adapters live only in ContinuityOps |
| D-003 | Use completed-code partition certification | accepted | Existing files are candidates until their slice passes |
| D-004 | Use sequential execution inside each Ralphy stream with fresh-worker/bottleneck replacement | superseded by D-014/D-016 | Preserves one mutation owner per stream while permitting disjoint concurrency |
| D-005 | Use three independent fresh judges per slice | accepted | No transcript/score leakage; strict exit rule |
| D-006 | Require average ≥9.5, no judge <9.0, all must-haves, and three merge-ready verdicts | accepted | Quality bar is explicit and not disclosed as judge target |
| D-007 | Prefer GitHub Actions OIDC for cloud control plane | accepted | Short-lived credentials and hosted evidence |
| D-008 | Use append-only evidence events with derived manifests | accepted | Repair history and promotion events cannot overwrite one another |
| D-009 | Use isolated synthetic-data lab environments only | accepted | No customer/production claims |
| D-010 | Managed Kubernetes proof requires live EKS; kind is local-only | accepted | Local runtime cannot earn cloud-applied claim |
| D-011 | Agentic workflow is read-mostly and human-gated for mutation | accepted | Modern automation without uncontrolled production authority |
| D-012 | Human owns cloud authority, destructive drills, cost increases, teardown, merge, and publication | accepted | Agents cannot silently expand authority |
| D-013 | Opus 4.8 cloud supervisor may appoint Sonnet/Opus cloud co-orchestrators | accepted | Global intent and per-stream authority remain separate |
| D-014 | Grok 4.5 High Fast handles Ralphy orchestration/councils; Codex 5.4 CLI Cloud Agents `/fast` implement | superseded by D-022/D-023 | Actual model/mode recorded on dispatch |
| D-015 | All worker communication is Simplified Chinese; recruiter artifacts are English | accepted | Machine fields may stay English, free text is Mandarin |
| D-016 | Up to three disjoint simultaneous Ralphy streams, sequential internally | accepted | Integration queue serializes merges and shared interfaces freeze dependents |
| D-017 | Saved judge/nixer/fixer cohort repairs until provisional pass; fresh judges certify | accepted | Fresh failure requires fresh nixer/fixer cohort and another fresh council |
| D-018 | Claude agents are cloud-only; pinned pxpipe proxy is optional and measured | accepted | No local-session dependency or guaranteed quota multiplier |
| D-019 | Stable TypeScript 7.x is mandatory where TypeScript is used | accepted | Initial pinned baseline `7.0.2`; upgrades require full review |
| D-020 | Final codebase is logically repartitioned and recertified | accepted | Construction ownership does not define final certification boundaries |
| D-021 | Root README begins with an evidence-constrained draw.io/Image2 infographic | accepted | Recruiter comprehension and visual honesty are final gates |
| D-022 | Claude Opus 4.8 is the lead orchestrator and absorbs all council roles (judges, nixers, fixers, bottleneck reasoning); a Claude 5 cloud session is portfolio supervisor | accepted, amended by D-030 | Supersedes the Grok 4.5 portion of D-014; supervisor↔orchestrator communication is Simplified Chinese. Amended by D-030: the resident Opus 4.8 orchestrator becomes the reserve seat while episodic GPT rounds are the default orchestration carrier |
| D-023 | Code executors are warm Codex CLI 5.4 cloud workers in default mode (not /high, not /fast) with environments pre-set-up before work begins | accepted | Supersedes the `/fast` portion of D-014 |
| D-024 | Workers report remaining context on every handoff; the orchestrator may retire a low-context worker and dispatch a fresh replacement | accepted | Handoff schema gains a `context_remaining` field |
| D-025 | The supervisor operates minimal-intervention and reviews a stream branch only upon the orchestrator's durable completion signal | accepted | Branch-check protocol documented as BF-PRE-015 in BREAK_FIX_LOG.md |
| D-026 | Adopt the warm-start Codex Cloud specification in full: one Codex Cloud Environment per repo (cache On), the two in-repo scripts `.codex/cloud-setup.sh` and `.codex/cloud-maintenance.sh` are the only content pasted into the Environment, zero credentials in the container, a warm gate before every dispatch, and `codex cloud exec --env <ENV_ID> --branch <branch>` dispatch where the task never touches git and the orchestrator owns integration | accepted | Acceptance red lines: adding a secret to the Environment, editing the setup scripts ad hoc, or bypassing the warm gate are all out of bounds; warmth is a per-Environment toolchain cache (~12h), not credential material |
| D-027 | The owner's Windows control-center session (local Claude Code with codex-cli, pwsh, and the machine-local `environments.json` registry) is the sole dispatch point; cloud containers and cloud workers are receive-only and never run the warm gate, attempt `codex cloud exec`, or hold Codex credentials | accepted | A cloud orchestrator that needs a Codex cloud task must either request it in its report to the control center or leave a durable GitHub marker (issue/comment) as a dispatch backlog the control center polls |
| D-028 | Cross-repo material follows "the worker gets data, not permission": the control center supplies upstream context per task by priority (1) context packaging, default, control-center gh extracts the needed files/logs/contracts into the prompt or pre-committed; (2) read-only vendored snapshot of a standing dependency with recorded source SHA; (3) submodule/multi-repo authorization, unverified, must be smoke-verified before reliance and is second choice even if it works; (4) local-lane exception, a control-center worktree subagent inherits the owner gh login for multi-repo read-heavy tasks | accepted | Cloud worker containers clone only their own Environment repo and hold no environment credentials; the Cursor variant of this workflow is superseded |
| D-029 | Codex dispatch runs through a repository queue polled by the control-center supervisor lane, not by human copy-paste: (1) the cloud orchestrator emits intent only, as a durable GitHub issue labeled `codex-dispatch` (or titled `[codex-dispatch] ...`) carrying the full run sheet (warm command, `codex cloud exec` text, target branch, ENV_ID, contract path); (2) the control-center Claude Code lane (codex CLI + keychain + registry co-located) polls the queue, runs the warm gate then `codex cloud exec`, comments the returned task ID, relabels to `dispatched`, and after diff/apply/push comments the result and closes; (3) results flow back through the repo (diff applied to the stream branch and pushed, visible to the cloud); (4) `codex login` inside any cloud container is prohibited (equivalent to the rejected CO-005); a Codex GitHub App + @codex mention + scheduled keep-warm Action is recorded but NOT enabled — it requires moving the warm stamp out of `%LOCALAPPDATA%` and a CODEOWNERS-style gate on who may trigger dispatch, and is reserved as a fallback for when the supervisor lane is unavailable | accepted | Cloud emits intent, the local lane executes, credentials never move; the container never authenticates Codex |
| D-030 | The orchestrator seat moves from a resident Claude session to **episodic GPT rounds** to conserve Anthropic quota (human decision, verbatim "stick with GPT orchestrator"). Each orchestration round is carried by a Codex 5.4 Cloud task dispatched through the `codex-dispatch` queue; the ORCH-SMOKE-01 smoke (issue #3) and the P0-T01 validation round are its acceptance steps. Amends D-022: the resident Opus 4.8 orchestrator is retained as the **reserve seat** (cold-start is losslessly reconstructable from durable artifacts, enabled when a GPT round is unavailable or fails). The supervisor may publish the queue issue that carries an orchestration round's intent (this is bookkeeping, not an orchestration decision); episodic rounds hold zero credentials, return work as a diff applied to the branch, and have their bookkeeping/intent output executed by the on-station sweep lane. The actual model ID of every round is still recorded at dispatch | accepted | Default orchestration is episodic GPT via the queue; Opus 4.8 is reserve; credentials never move; per-round model IDs recorded |
| D-031 | **Activate the Codex GitHub App dispatch path** (human decision, verbatim "go with A — app installed"): dispatch is now an `@codex` mention posted **by the cloud supervisor via its existing GitHub MCP authority** on a supervisor-authored `codex-dispatch` queue issue. Amends D-027/D-029: the Windows control-center ceases to be the sole dispatch point; the manual sweep becomes the fallback path. Gating: dispatch mentions are valid only on queue issues authored by the supervisor or the owner (this private repo has no other commenters); any other mention is not a dispatch. Results flow back as Codex-created PRs/branches; the supervisor integrates into **stream branches only** via MCP — merges to `main` and all D-012 gates remain human. Warm stamp leaves `%LOCALAPPDATA%`: warm freshness is now evidenced by the timestamp of the most recent Codex task on the keep-warm record (issue-based), maintained by the supervisor's scheduled self-checks posting an `@codex` smoke roughly every 9 hours; a scheduled GitHub Action is a documented backup pending verification that the App responds to bot-authored mentions. App platform behavior (branch targeting, PR flow) is unproven until the first dispatch — ORCH-SMOKE-01 doubles as that platform smoke | accepted | Fully autonomous dispatch loop with zero new credentials; human retains only D-012 constitutional gates; first App dispatch is itself the platform smoke |
| D-032 | **Post-smoke supervisor economy** (human directive, effective when ORCH-SMOKE-01 passes): (1) supervisor verdicts (`SUPERVISOR_VERDICT.json`) certify at **stream boundaries only** — one BF-PRE-015 review per `STREAM_COMPLETE.json`, never per orchestration round; (2) actuation of orchestrator-emitted intents (mentions, merges, labels, issue closes) **batches** into evented wakes (ref-watcher) plus the 3–4h fallback heartbeat — no per-intent wakes; (3) **per-round checking stays with the deterministic validators** run inside the episodic rounds — the supervisor does not re-execute or shadow them | accepted | Supervisor token spend reduces to stream-boundary verdicts + batched actuation; deterministic gates remain the per-round quality floor |
| D-033 | **App-path publish hard gate** (overnight unblock, empirically revised): `@codex` App execution is proven (bot replies + task diffs). Codex UI `make_pr` is metadata-only. In-container `git push`/`gh pr create` **failed** on ContinuityOps App tasks (no `gh`; GitHub `CONNECT tunnel failed, response 403`). Unattended publish therefore requires the **cloud supervisor** (or control-center when on-station) to actuate **platform Create PR** on the task page, or `codex cloud apply`+push+`gh pr create` locally — not worker-side git. Heartbeat advances only on an open GitHub PR URL. On bot-only-without-PR: one re-nudge; then platform Create PR actuation; if still blocked, diagnosis + Opus reserve (reasoning-only). `github-actions[bot]` `@codex` keepwarm mentions are **not** a verified warm carrier. Amends D-031. | superseded-by-D-034 | Overnight App path = mention → worker → supervisor/platform Create PR → GitHub PR (laptop optional) |
| D-034 | **Patch-in-comment GHA publisher** (primary overnight publish): App workers must end replies with `<!-- continuityops-patch-v1 -->`, `base_branch`, `base_sha` (40-hex), and a full fenced unified diff (chunked if needed). Workflow `.github/workflows/codex-patch-publish.yml` runs on `chatgpt-codex-connector[bot]` `issue_comment` for `codex-dispatch` issues, applies the patch with ephemeral `GITHUB_TOKEN`, opens a PR, comments `publish-ok` + URL. Denies `.github/**`, secret/.env paths, binaries. Idempotent on existing `codex/issue-<N>-*` PRs. Platform Create PR and `scripts/Publish-CodexCloudTask.ps1` are fallbacks. Supervisor heartbeat reviews PRs / re-nudges missing markers / handles `publish-failed`. Amends D-033. | accepted | Fully in-cloud publish with no new secrets; supervisor reviews PRs only |

## Initial issue ledger

```json
{
  "schema_version": "1.0",
  "revision": 4,
  "issues": [
    {
      "id": "CO-001",
      "phase": 0,
      "severity": "blocking",
      "category": "baseline",
      "summary": "The ContinuityOps repository, baseline SHA, and partition manifest do not yet exist.",
      "status": "open",
      "owner": "P0-T01",
      "resolution_criterion": "Repository created; every retained path classified and content-addressed."
    },
    {
      "id": "CO-002",
      "phase": 0,
      "severity": "blocking",
      "category": "integration",
      "summary": "Exact Project A and C commits and consumable contracts are not yet pinned.",
      "status": "open",
      "owner": "P0-T01/P1-T01",
      "resolution_criterion": "upstreams.lock.json validates and cross-contract tests identify all supported and missing capabilities."
    },
    {
      "id": "CO-003",
      "phase": 1,
      "severity": "blocking",
      "category": "authority",
      "summary": "Cloud account, OIDC role, regions, state ownership, cost cap, and protected environments are not approved.",
      "status": "open",
      "owner": "human H1/H2",
      "resolution_criterion": "Hash-bound human receipts approve the exact identities, environments, plans, cost, and teardown controls."
    },
    {
      "id": "CO-004",
      "phase": 1,
      "severity": "blocking",
      "category": "artifact",
      "summary": "Project C immutable image digest and known-good rollback status must be verified; current plan must not assume them.",
      "status": "open",
      "owner": "P1-T01",
      "resolution_criterion": "A verified digest/rollback contract is consumed, or a clearly labeled ContinuityOps lab artifact and first-release policy are established."
    },
    {
      "id": "CO-005",
      "phase": 0,
      "severity": "blocking",
      "category": "credential",
      "summary": "Prior assumption that a CODEX_AUTH_JSON_GZB64 secret must be injected to dispatch workers. Rejected: no auth material is ever injected. Codex Cloud is authenticated through the platform under the owner ChatGPT account; warmth is only a toolchain cache and a secret would invalidate that cache.",
      "status": "rejected-by-human",
      "owner": "human decision (D-026/D-027)",
      "resolution_criterion": "N/A. Superseded by the receive-only dispatch topology; no credential is placed in any cloud Environment or container."
    },
    {
      "id": "CO-006",
      "phase": 0,
      "severity": "blocking",
      "category": "integration",
      "summary": "Upstream Project A/C material must reach a worker as data, not permission. The Cursor App framing is void. The control center supplies A/C context per task via packaging or a read-only vendored snapshot (D-028); readability of the pinned SHAs is a control-center capability, not a worker-container grant.",
      "status": "open",
      "owner": "control-center (per-task context supply, D-028)",
      "resolution_criterion": "The first task that needs A/C is served a validated context package or vendored snapshot with recorded source SHAs; closed after that first packaging is verified."
    },
    {
      "id": "CO-007",
      "phase": 0,
      "severity": "blocking",
      "category": "environment",
      "summary": "The ContinuityOps Codex Cloud Environment (env 6a594ee667608191ab53cae15202815e) is created in the Codex UI (cache On, the two .codex scripts pasted, zero secrets), registered in the machine-local registry, and first-warmed via -Force. Warm gate can now run before dispatch.",
      "status": "resolved",
      "owner": "human H-codex-env-create (creation) + control-center (register/warm)",
      "resolution_criterion": "Environment created (cache On, two scripts, zero secrets), registered, and -Force first warm stamped lastWarmUtc. Confirmed by the owner on 2026-07-16."
    }
  ]
}
```

## Human receipt schema

```json
{
  "schema_version": "1.0",
  "gate_id": "H0",
  "decision": "approve|reject|defer",
  "candidate_sha": "40_HEX",
  "plan_bundle_sha256": "64_HEX",
  "execution_bundle_sha256": "64_HEX",
  "validator_sha256": "64_HEX",
  "rubric_bundle_sha256": "64_HEX",
  "partition_manifest_sha256": "64_HEX",
  "changed_paths_sha256": "64_HEX",
  "validation_digest": "64_HEX",
  "environment": "repo-only|staging|recovery-lab|portfolio-demo",
  "cost_cap_usd": null,
  "approver": "human identity",
  "approved_at": "ISO-8601",
  "expires_at": "ISO-8601_OR_NULL",
  "conditions": []
}
```

Receipts should live outside worker-write scope. Agents cannot generate or edit
them.
