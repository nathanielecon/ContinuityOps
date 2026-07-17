# ContinuityOps Initial Operating State

This file is the planning-package seed. The implementation repository should
split the machine-readable blocks into `STATUS.md`, `ISSUES.md`, and
`DECISIONS.md` and mutate them only through the project CLI.

## Status

```json
{
  "schema_version": "1.0",
  "revision": 21,
  "project": "ContinuityOps",
  "current_phase": 0,
  "authorized_through_phase": 0,
  "current_gate": "phase-0-baseline-audit",
  "running_tasks": [],
  "blocked_tasks": ["P0-T04", "P0-T05"],
  "waiting_human": [
    "issues:write-restore-or-owner-@codex-keepwarm",
    "REPO_SETTINGS_ADMIN_TOKEN",
    "PR-20",
    "H0-after-P0-T04",
    "D-039-write-scope-human-veto-window"
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
    "Revision note: status revision 19 was attempted via issue #29 (ORCH-ROUND-06) but publish-failed (D-034); this revision 20 lands the same governance via supervisor git-push fallback plus post-#29 reality updates",
    "Cursor supervisor App seat lacks issues:write (CO-011) — owner must grant Issues permission on the App/token OR personally post @codex / keep-warm on issue #4; App @codex dispatch/keep-warm is unavailable from this seat until restored (D-040)",
    "#29 ORCH-ROUND-06 governance repaired via supervisor git-push fallback at 679f808: lands D-037/D-038/D-039/D-040, BF-2026-004/005, Watch-CodexRefs",
    "P0-T03 fixer restaged as draft PR #32 (branch cursor/p0-t03-fixer-d039-2d6f @ fd8c8c3); local validate green under D-039; D-037 re-review + merge blocked on CO-011",
    "Supervisor heartbeat armed via scripts/supervisor-heartbeat.sh (3.5h ls-remote); keep-warm @codex on #4 still requires owner/issues:write",
    "#31 D-037 reviewer verdict fail SCOPE-001 on PR #30; PR #30 was accidentally merged during a permissions probe then reverted at 94f4e33 (BF-2026-005 / CO-012); do not re-merge #30 content until write_scope is expanded (D-039) and a new fixer/reviewer cycle runs after issues:write is restored",
    "Owner pending: REPO_SETTINGS_ADMIN_TOKEN, PR #20, H0 after P0-T04; do not authorize Phase 1 until S0 and H0 pass",
    "P0-T03 is ready (deps P0-T02 verified; write_scope expanded per D-039); next dispatch after issues:write restore: fixer for P0-T03 → D-037 re-review → P0-T04 → H0",
    "Keep-warm: cloud-native issue #4 warm stamp; until issues:write returns, owner/control-center must post trivial @codex smokes; local Invoke-CodexCloudWarm.ps1 remains fallback-lane only",
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
    "D-034: patch-in-comment GHA publisher smoked (issue #12 → PR #13; Actions create-PR permission required)",
    "P0-T01 verified; P0-T02 verified with condition CO-010; ORCH-ROUND-06 governance landed via supervisor git-push fallback after #29 publish-failed"
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
| D-035 | **Adopt the dailydigits warm-cloud worker flow, cloud-native, execution delegated to the supervisor** (human directive 2026-07-17). Branch-and-merge execution authority is delegated to the cloud supervisor, amending the merge clause of D-012; the human retains only H0, credentials/secrets, spend ceilings, destructive/irreversible operations, and external-to-repo publication, and every merge carries evidence in the PR body. Keep-warm is cloud-native: warm stamp = latest Codex task timestamp on keep-warm issue #4, with no local registry; dispatch-time gate checks the stamp and, if older than ~10h, posts a trivial `@codex` smoke first and stamps on its reply; never dispatch real work into a cold environment; supervisor heartbeat posts smoke at >9h; local `Invoke-CodexCloudWarm.ps1` is fallback-lane only. Dispatch discipline follows the dailydigits DEC-014 pattern: each `@codex` mention carries one atomic task contract with one objective, explicit allowed paths, exact in-container validation commands to run before finishing, a two-strike stop condition, no lockfile commits, and concise Simplified Chinese worker messages with code/identifiers in English. Fleet discipline follows the DEC-021/022 pattern: lane tiering uses the default cheap worker lane for tight-contract tasks and escalates to a high-judgment lane only for high-judgment slices; parallelism is path-disjoint only; dispatches are batched rather than many small ones; bottleneck-fixer procedure triggers on task >2× budget, repeated failure class, or queue starvation and may fix flow but never product/constitutional behavior. | accepted | Cloud supervisor can execute branch-and-merge work within evidence-bound repo gates; warmth and dispatch are issue-native; human gates narrow to constitutional/credential/spend/destructive/external-publication decisions |
| D-037 | **Per-PR GPT reviewer rounds** (human verbatim "go", effective next supervisor session): every worker PR is independently verified by a GPT reviewer round dispatched through the `codex-dispatch` queue. The reviewer applies that PR's patch at the declared `base_sha` inside the sandbox, personally runs the declared validation commands, and reports a structured verdict comment. The reviewer does not modify implementation; findings route to an independent fixer round. Supervisor merge signal = CI green + reviewer verdict pass. Guards: reviewer and worker are different round instances; actual model ID is recorded for every round; the supervisor's stream-boundary verdicts and final P8 review retain cross-model-family checking. | accepted | Per-PR validation moves out of the supervisor session while preserving independent review, CI, model-recording, and boundary-verdict controls |
| D-038 | **Orchestrator model escalation ladder** (human directive): the orchestration seat defaults to Codex 5.4, using the same engine family as workers but with role isolation and with the orchestrator remaining the orchestrator. If **3 cumulative defects attributable to orchestration rounds** occur (excluding publisher/CI or other supervisor-side infrastructure defects; current orchestration-round attribution count: 0), escalate to **GPT-5.6 Sol medium**; if defects continue after escalation, escalate again to **GPT-5.6 Sol high**. Every escalation records the triggering defect list and actual model ID; downgrade requires human approval. | accepted | Orchestration stays on the cheap/default GPT lane until three attributed defects justify escalation; downgrade is human-gated |
| D-039 | **Supervisor ratifies P0-T03 write_scope expansion** to match owner-authored issue #28 dispatch + CO-010 repair surface: add `scripts/project.mjs`, `tests/index.mjs`, `tests/package.json`, and the exact evidence file `evidence/slices/S0/validator-contract.json` (not the whole `evidence/slices/` tree). Material plan amendment recorded in `PLAN.md` and `docs/planning/dispatch/P0-T03.zh.md`; human may veto. Until ratification stands and a new fixer/reviewer cycle runs after issues:write restore, do not re-merge PR #30 content (D-037 SCOPE-001 fail still stands). | accepted | P0-T03 write_scope matches the owner dispatch contract; SCOPE-001 is addressable by a fresh fixer after D-039; human veto remains open |
| D-040 | **Cursor cloud App token can push/merge but not Issues**: until `issues:write` is restored for the supervisor App seat, the App `@codex` path is unavailable from this seat for dispatch and keep-warm. Control-center / owner comments on queue issues (including keep-warm #4) are required. Amends the practical actuation of D-031/D-034/D-035 for this seat only; does not change the constitutional App-path design. | accepted | Supervisor git-push fallback remains viable; Issues-gated actuation must be owner/control-center until permission restored |

## Initial issue ledger

```json
{
  "schema_version": "1.0",
  "revision": 6,
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
    },
    {
      "id": "CO-008",
      "phase": 0,
      "severity": "conditional",
      "category": "baseline",
      "summary": "P0-T01 audit classification and partition manifest were computed against the main tree visible to the App container (base 7e8a525), while baseline_sha is recorded as 6ed243564ddb46f4a46608496d6f05db53c93788; the two trees are not identical. Raised as a condition on the supervisor approve verdict for candidate ea2c27513305badfeafe98500e8fefe603bc97cb.",
      "status": "open",
      "owner": "P0-T01 refresh (post-baseline-freeze)",
      "resolution_criterion": "After the setup branch is merged to main and the authoritative baseline is frozen, refresh the scaffold classification and partition manifest against the frozen baseline and re-run full validation; a changed binding invalidates candidate-bound evidence and must be regenerated."
    },
    {
      "id": "CO-009",
      "phase": 0,
      "severity": "conditional",
      "category": "environment",
      "summary": "The Codex GitHub App container clones only the default branch (main) and has no origin remote, so it cannot read non-default-branch material (e.g. a stream-branch task contract) and cannot publish outbound from inside the sandbox. Observed during the P0-T01 App round (PR #6) and the ORCH-SMOKE-01/PREP rounds.",
      "status": "open",
      "owner": "orchestrator dispatch discipline (BF-PRE-019)",
      "resolution_criterion": "Any round needing non-default-branch material supplies it via issue-body context packaging or waits for a main merge; publication is actuated by the owner (platform Create PR) or the control center (codex cloud apply + push), never from inside the App sandbox."
    },
    {
      "id": "CO-011",
      "phase": 0,
      "severity": "blocking",
      "category": "credential",
      "summary": "Cursor supervisor App seat lacks issues:write. Issues API returns 403; this seat cannot author/comment on codex-dispatch queue issues or post @codex / keep-warm on issue #4. Blocks App-path dispatch and cloud-native keep-warm from this seat (D-040).",
      "status": "open",
      "owner": "human (GitHub App/token permissions)",
      "resolution_criterion": "Owner grants issues:write to the supervisor App/token, or owner/control-center posts @codex and keep-warm comments until the seat is restored; first successful Issues write from this seat closes the issue."
    },
    {
      "id": "CO-012",
      "phase": 0,
      "severity": "conditional",
      "category": "authority",
      "summary": "BF-2026-005: accidental merge of PR #30 during a permissions probe (merge-API call with message probe-should-fail-dry) despite D-037 reviewer fail SCOPE-001. Reverted at 94f4e33. Prevention: never call the merge API for permission probes; use OPTIONS/dry-run or inspect-only; merge only on CI green + D-037 pass.",
      "status": "open",
      "owner": "supervisor actuation discipline",
      "resolution_criterion": "Prevention control recorded in BREAK_FIX_LOG (BF-2026-005); any future merge of P0-T03 content requires CI green + D-037 pass after D-039 write_scope expansion and a fresh fixer/reviewer cycle."
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
