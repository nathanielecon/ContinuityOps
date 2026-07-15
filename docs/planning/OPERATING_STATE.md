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
  "current_gate": "preflight-codex-auth-and-ac-visibility",
  "running_tasks": [],
  "blocked_tasks": ["P0-T01", "P0-T02", "P0-T03", "P0-T04", "P0-T05"],
  "waiting_human": [
    "H-preflight-CODEX_AUTH_JSON_GZB64",
    "H-preflight-AC-visibility",
    "H0-after-P0-T04"
  ],
  "completed_gates": [],
  "next_actions": [
    "Human: inject usable CODEX_AUTH_JSON_GZB64 (payload or resolvable auth file) into this Cloud Agent environment",
    "Human: grant GitHub App/installation read access to pinned Project A and C repos",
    "Orchestrator: re-verify both preflight gates; only then dispatch P0-T01",
    "Do not authorize Phase 1 until S0 and H0 pass"
  ],
  "completed_bootstrap": [
    "Created ContinuityOps GitHub repository home",
    "Copied planning package into docs/planning/",
    "Installed root contracts and architecture assets"
  ],
  "verified_baseline": [],
  "unverified": [
    "All ContinuityOps implementation and runtime capabilities",
    "CODEX_AUTH_JSON_GZB64 usable Codex auth material",
    "Project A/C repository visibility from this Cloud Agent installation"
  ],
  "preflight": {
    "checked_at": "2026-07-15T21:50:00Z",
    "baseline_sha": "39eaf03f749ec828c39d2e3da75efaf3392be2e8",
    "codex_auth_json_gzb64": {
      "env_present": true,
      "env_value_len": 37,
      "looks_like_path": true,
      "path_resolves": false,
      "usable_auth_material": false,
      "verdict": "fail"
    },
    "project_ac_visibility": {
      "installation_repo_count": 1,
      "installation_repos": ["nathanielecon/ContinuityOps"],
      "checked_repos": [
        "nathanielecon/aws-landing-zone-lab",
        "nathanielecon/local-first-governed-cicd",
        "nathanielecon/cloud",
        "nathanielecon/project-c-cloud"
      ],
      "visible_repos": [],
      "pin_commits_reachable": false,
      "verdict": "fail"
    },
    "p0_dispatch_allowed": false
  }
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
| D-014 | Grok 4.5 High Fast handles Ralphy orchestration/councils; Codex 5.4 CLI Cloud Agents `/fast` implement | accepted | Actual model/mode recorded on dispatch |
| D-015 | All worker communication is Simplified Chinese; recruiter artifacts are English | accepted | Machine fields may stay English, free text is Mandarin |
| D-016 | Up to three disjoint simultaneous Ralphy streams, sequential internally | accepted | Integration queue serializes merges and shared interfaces freeze dependents |
| D-017 | Saved judge/nixer/fixer cohort repairs until provisional pass; fresh judges certify | accepted | Fresh failure requires fresh nixer/fixer cohort and another fresh council |
| D-018 | Claude agents are cloud-only; pinned pxpipe proxy is optional and measured | accepted | No local-session dependency or guaranteed quota multiplier |
| D-019 | Stable TypeScript 7.x is mandatory where TypeScript is used | accepted | Initial pinned baseline `7.0.2`; upgrades require full review |
| D-020 | Final codebase is logically repartitioned and recertified | accepted | Construction ownership does not define final certification boundaries |
| D-021 | Root README begins with an evidence-constrained draw.io/Image2 infographic | accepted | Recruiter comprehension and visual honesty are final gates |

## Initial issue ledger

```json
{
  "schema_version": "1.0",
  "revision": 2,
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
      "summary": "CODEX_AUTH_JSON_GZB64 is present as an env name but does not resolve to usable Codex auth material (path-like value, target missing).",
      "status": "open",
      "owner": "human H-preflight-CODEX_AUTH_JSON_GZB64",
      "resolution_criterion": "Env injects gzip+base64 auth JSON or a resolvable file path whose contents decode to a usable Codex auth.json; orchestrator recheck passes."
    },
    {
      "id": "CO-006",
      "phase": 0,
      "severity": "blocking",
      "category": "integration",
      "summary": "Pinned Project A/C repositories are not visible to this Cloud Agent GitHub installation (only ContinuityOps is installed).",
      "status": "open",
      "owner": "human H-preflight-AC-visibility",
      "resolution_criterion": "Installation can read nathanielecon/aws-landing-zone-lab and nathanielecon/local-first-governed-cicd at the pinned commits (or human updates pins to visible canonical repos); gh api/git fetch succeed."
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
