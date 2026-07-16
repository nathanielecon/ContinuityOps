# ContinuityOps Initial Operating State

This file is the planning-package seed. The implementation repository should
split the machine-readable blocks into `STATUS.md`, `ISSUES.md`, and
`DECISIONS.md` and mutate them only through the project CLI.

## Status

```json
{
  "schema_version": "1.0",
  "revision": 3,
  "project": "ContinuityOps",
  "current_phase": 0,
  "authorized_through_phase": 0,
  "current_gate": "phase-0-baseline-audit",
  "running_tasks": [],
  "blocked_tasks": [],
  "waiting_human": ["H0-after-P0-T04"],
  "completed_gates": [],
  "next_actions": [
    "Record candidate baseline and upstream SHAs in integration/upstreams.lock.json",
    "Run P0-T01 inventory and partition audit",
    "Install harness CLI contracts (P0-T02)",
    "Do not authorize Phase 1 until S0 and H0 pass"
  ],
  "completed_bootstrap": [
    "Created ContinuityOps GitHub repository home",
    "Copied planning package into docs/planning/",
    "Installed root contracts and architecture assets"
  ],
  "verified_baseline": [],
  "unverified": [
    "All ContinuityOps implementation and runtime capabilities"
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
| D-014 | Grok 4.5 High Fast handles Ralphy orchestration/councils; Codex 5.4 CLI Cloud Agents `/fast` implement | superseded by D-022 | Actual model/mode recorded on dispatch |
| D-015 | All worker communication is Simplified Chinese; recruiter artifacts are English | accepted | Machine fields may stay English, free text is Mandarin |
| D-016 | Up to three disjoint simultaneous Ralphy streams, sequential internally | accepted | Integration queue serializes merges and shared interfaces freeze dependents |
| D-017 | Saved judge/nixer/fixer cohort repairs until provisional pass; fresh judges certify | accepted | Fresh failure requires fresh nixer/fixer cohort and another fresh council |
| D-018 | Claude agents are cloud-only; pinned pxpipe proxy is optional and measured | accepted | No local-session dependency or guaranteed quota multiplier |
| D-019 | Stable TypeScript 7.x is mandatory where TypeScript is used | accepted | Initial pinned baseline `7.0.2`; upgrades require full review |
| D-020 | Final codebase is logically repartitioned and recertified | accepted | Construction ownership does not define final certification boundaries |
| D-021 | Root README begins with an evidence-constrained draw.io/Image2 infographic | accepted | Recruiter comprehension and visual honesty are final gates |
| D-022 | Lead Ralphy orchestrator is Claude Opus 4.8 (cloud); Codex 5.4 CLI Cloud workers implement in default mode — not `/fast`, not `/high` (human instruction 2026-07-16, supersedes D-014) | accepted | Actual model/mode still recorded on every dispatch; council model routing unchanged unless separately amended |
| D-023 | Codex workers run in warm pre-provisioned Codex Cloud environments per `nathanielecon/cloud-tools` (cached environment state; Block A prepended per dispatch, Block B on cold cache, Block C post-setup warm-up) | accepted | Workers are sub-subagents under the orchestrator, which retains discretion to reassign or retire workers |
| D-024 | Every worker handoff must report remaining context (`context_remaining`); the orchestrator may retire a low-context worker and dispatch a fresh one | accepted | Handoffs missing `context_remaining` are rejected |
| D-025 | Supervisor reviews stream branches event-driven only — on the orchestrator's explicit branch-complete signal, never by polling | accepted | Mechanism defined in `docs/orchestration/SUPERVISION_PROTOCOL.md` and logged as BF-PRE-015 |

## Initial issue ledger

```json
{
  "schema_version": "1.0",
  "revision": 1,
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
