# ContinuityOps Initial Operating State

This file is the planning-package seed. The implementation repository should
split the machine-readable blocks into `STATUS.md`, `ISSUES.md`, and
`DECISIONS.md` and mutate them only through the project CLI.

## Status

```json
{
  "schema_version": "1.0",
  "revision": 6,
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
    "Control center: run the warm gate for nathanielecon/ContinuityOps, then dispatch P0-T01 on stream/S0-baseline-audit via codex cloud exec (env 6a594ee667608191ab53cae15202815e)",
    "Worker: produce changes only within the P0-T01 write_scope, never run git, report context_remaining on handoff",
    "Orchestrator: on worker completion apply the diff to stream/S0-baseline-audit, run validators, commit STREAM_COMPLETE.json with preflight_ok, and notify the supervisor",
    "Do not authorize Phase 1 until S0 and H0 pass"
  ],
  "completed_bootstrap": [
    "Created ContinuityOps GitHub repository home",
    "Copied planning package into docs/planning/",
    "Installed root contracts and architecture assets",
    "Merged .codex Codex Cloud Environment scripts to the default branch",
    "Created, registered, and first-warmed the ContinuityOps Codex Cloud Environment (env 6a594ee667608191ab53cae15202815e, zero secrets)"
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
| D-022 | Claude Opus 4.8 is the lead orchestrator and absorbs all council roles (judges, nixers, fixers, bottleneck reasoning); a Claude 5 cloud session is portfolio supervisor | accepted | Supersedes the Grok 4.5 portion of D-014; supervisor↔orchestrator communication is Simplified Chinese |
| D-023 | Code executors are warm Codex CLI 5.4 cloud workers in default mode (not /high, not /fast) with environments pre-set-up before work begins | accepted | Supersedes the `/fast` portion of D-014 |
| D-024 | Workers report remaining context on every handoff; the orchestrator may retire a low-context worker and dispatch a fresh replacement | accepted | Handoff schema gains a `context_remaining` field |
| D-025 | The supervisor operates minimal-intervention and reviews a stream branch only upon the orchestrator's durable completion signal | accepted | Branch-check protocol documented as BF-PRE-015 in BREAK_FIX_LOG.md |
| D-026 | Adopt the warm-start Codex Cloud specification in full: one Codex Cloud Environment per repo (cache On), the two in-repo scripts `.codex/cloud-setup.sh` and `.codex/cloud-maintenance.sh` are the only content pasted into the Environment, zero credentials in the container, a warm gate before every dispatch, and `codex cloud exec --env <ENV_ID> --branch <branch>` dispatch where the task never touches git and the orchestrator owns integration | accepted | Acceptance red lines: adding a secret to the Environment, editing the setup scripts ad hoc, or bypassing the warm gate are all out of bounds; warmth is a per-Environment toolchain cache (~12h), not credential material |
| D-027 | The owner's Windows control-center session (local Claude Code with codex-cli, pwsh, and the machine-local `environments.json` registry) is the sole dispatch point; cloud containers and cloud workers are receive-only and never run the warm gate, attempt `codex cloud exec`, or hold Codex credentials | accepted | A cloud orchestrator that needs a Codex cloud task must either request it in its report to the control center or leave a durable GitHub marker (issue/comment) as a dispatch backlog the control center polls |
| D-028 | Cross-repo material follows "the worker gets data, not permission": the control center supplies upstream context per task by priority (1) context packaging, default, control-center gh extracts the needed files/logs/contracts into the prompt or pre-committed; (2) read-only vendored snapshot of a standing dependency with recorded source SHA; (3) submodule/multi-repo authorization, unverified, must be smoke-verified before reliance and is second choice even if it works; (4) local-lane exception, a control-center worktree subagent inherits the owner gh login for multi-repo read-heavy tasks | accepted | Cloud worker containers clone only their own Environment repo and hold no environment credentials; the Cursor variant of this workflow is superseded |

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
