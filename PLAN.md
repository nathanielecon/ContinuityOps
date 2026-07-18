# Authoritative ContinuityOps Task Plan

The JSON block is the task authority. Workers never edit it directly. The
project CLI/orchestrator performs revision-checked atomic state transitions.
Initial authorization stops at Phase 0.

```json
{
  "schema_version": "1.0",
  "plan_id": "continuityops-cloud-reliability-v1",
  "revision": 13,
  "authorized_through_phase": 0,
  "baseline_sha": "UNSET_UNTIL_BOOTSTRAP",
  "execution_profile": {
    "portfolio_supervisor": "claude-5-cloud-supervisor",
    "optional_co_orchestrators": [
      "claude-sonnet-cloud",
      "claude-opus-cloud"
    ],
    "ralphy_orchestrator_and_council": "codex-5.4-cloud-episodic-orchestrator (gpt); claude-opus-4.8-cloud (reserve)",
    "code_executor": "codex-5.4-cli-cloud-warm-default-mode",
    "worker_language": "zh-CN",
    "external_artifact_language": "en",
    "max_parallel_ralphy_streams": 3,
    "stream_rule": "sequential_within_stream_disjoint_across_streams",
    "typescript": "7.0.2",
    "claude_proxy": {
      "package": "pxpipe-proxy@0.9.0",
      "base_url": "http://127.0.0.1:47821",
      "status": "experimental_policy_and_integrity_gate_required"
    }
  },
  "tasks": [
    {
      "id": "P0-T01",
      "phase": 0,
      "slice": "S0",
      "title": "Audit and freeze the completed candidate baseline",
      "state": "verified",
      "note": "Verified by the reserve orchestrator (Opus 4.8) validation round; candidate ea2c27513305badfeafe98500e8fefe603bc97cb; supervisor verdict approve (evidence/slices/S0/SUPERVISOR_VERDICT.json on stream/S0-baseline-audit) with conditional issues CO-008 and CO-009 tracked in OPERATING_STATE.md.",
      "depends_on": [],
      "owner": "baseline-audit-worker",
      "risk": "medium",
      "write_scope": [
        "docs/scaffold-audit.md",
        "integration/upstreams.lock.json",
        "harness/partition-manifest.json"
      ],
      "acceptance": [
        "Every file is classified",
        "Baseline and upstream SHAs are recorded",
        "Each retained path has one primary slice",
        "Shared interfaces are explicit"
      ],
      "validators": [
        "state_schema",
        "partition_unique_ownership",
        "upstream_pin_schema",
        "clean_tree"
      ],
      "evidence": [
        "evidence/slices/S0/baseline-audit.json"
      ]
    },
    {
      "id": "P0-T02",
      "phase": 0,
      "slice": "S0",
      "title": "Install authoritative multi-stream CLI and state contracts",
      "state": "verified",
      "note": "Supervisor stream-boundary verdict approve with condition CO-010 (evidence/slices/S0/SUPERVISOR_VERDICT-P0-T02.json); candidate f9b698add11d63c10d7cc547b384b6ed78fa91ad.",
      "depends_on": [
        "P0-T01"
      ],
      "owner": "harness-worker",
      "risk": "high",
      "write_scope": [
        "scripts/project*",
        "tests/harness/",
        "PLAN.md",
        "STATUS.md",
        "ISSUES.md",
        "DECISIONS.md"
      ],
      "acceptance": [
        "Atomic revision-checked state changes",
        "Legal lifecycle enforced",
        "Current phase accepted and next phase rejected",
        "Workers cannot mark verified/done",
        "Up to three disjoint Ralphy streams are isolated and sequential internally",
        "Integration queue serializes candidate merges"
      ],
      "validators": [
        "harness_unit",
        "authorization_boundary",
        "state_reconciliation",
        "stream_isolation",
        "integration_queue",
        "scope"
      ],
      "evidence": [
        "evidence/slices/S0/harness.json"
      ]
    },
    {
      "id": "P0-T03",
      "phase": 0,
      "slice": "S0",
      "title": "Implement validators, model routing, bottleneck dispatch, and evidence adapters",
      "state": "verified",
      "note": "Verified 2026-07-17: PR #36 landed on main via supervisor git merge after CI contracts success + D-037 issue #38 verdict pass (human-directed redo; PR #32 superseded).",
      "depends_on": [
        "P0-T02"
      ],
      "owner": "validator-worker",
      "risk": "high",
      "write_scope": [
        "harness/",
        "scripts/validators/",
        "scripts/orchestration/",
        "scripts/project.mjs",
        "tests/validators/",
        "tests/orchestration/",
        "tests/index.mjs",
        "tests/package.json",
        "evidence/schema/",
        "evidence/slices/S0/validator-contract.json"
      ],
      "acceptance": [
        "Unknown validator IDs fail closed",
        "Validators cannot mutate repository",
        "Worker cannot forge adapter evidence",
        "Late-created forbidden paths are detected",
        "Evidence freshness is SHA-bound",
        "Actual model/mode is recorded",
        "Mandarin-only worker communication enforced",
        "Bottleneck profiles dispatch in-session",
        "Claude proxy is pinned, policy-gated, credential-safe, measured, and has direct fallback",
        "TypeScript is pinned to stable 7.x when present"
      ],
      "validators": [
        "validator_contract",
        "evidence_schema",
        "secret_scan",
        "forbidden_operations",
        "mutation_isolation",
        "model_routing",
        "worker_language",
        "bottleneck_dispatch",
        "claude_proxy_profile",
        "typescript_7"
      ],
      "evidence": [
        "evidence/slices/S0/validator-contract.json"
      ],
      "candidate_sha": "15234664b41af9e1a99db0cffd6b010233493af0"
    },
    {
      "id": "P0-T04",
      "phase": 0,
      "slice": "S0",
      "title": "Freeze rubrics and pin execution bundles",
      "state": "verified",
      "depends_on": [
        "P0-T01",
        "P0-T03"
      ],
      "owner": "rubric-controller",
      "risk": "high",
      "write_scope": [
        "harness/rubrics/",
        "harness/approvals/",
        "docs/reviews/rubric-review.md"
      ],
      "acceptance": [
        "One frozen rubric per slice",
        "Plan/execution/validator/rubric/partition hashes pinned",
        "Rubric mutation policy tested"
      ],
      "validators": [
        "rubric_schema",
        "bundle_hashes",
        "approval_binding"
      ],
      "evidence": [
        "evidence/slices/S0/rubric-freeze.json",
        "harness/approvals/H0.binding.json"
      ],
      "human_gate": "H0",
      "note": "Verified: H0 human receipt bound from issue #42 comment 5008633820 (candidate_sha 28bfb64). Receipt not agent-minted. See evidence/slices/S0/H0_PACKAGE.md.",
      "candidate_sha": "28bfb64ca5c12659d2e109091e8b6a7ec2143745"
    },
    {
      "id": "P0-T05",
      "phase": 0,
      "slice": "S0",
      "title": "Prove concurrent streams, worker replacement, saved/fresh councils, and Phase 0 certification",
      "state": "ready",
      "depends_on": [
        "P0-T02",
        "P0-T03",
        "P0-T04"
      ],
      "owner": "orchestrator",
      "risk": "medium",
      "write_scope": [
        "evidence/slices/S0/",
        "BREAK_FIX_LOG.md"
      ],
      "acceptance": [
        "Three disjoint smoke streams run while each remains sequential",
        "Failed task dispatches a fresh Codex worker or bottleneck specialist",
        "Saved remediation council reaches provisional pass",
        "Fresh judges independently validate without saved context",
        "Three-judge S0 exit passes",
        "Phase 1 remains rejected"
      ],
      "validators": [
        "harness_smoke",
        "stream_isolation",
        "worker_replacement",
        "bottleneck_dispatch",
        "saved_fresh_council",
        "full_repository",
        "judge_result_schema"
      ],
      "evidence": [
        "evidence/slices/S0/integrated-gate.json",
        "evidence/judges/S0/"
      ]
    },
    {
      "id": "P1-T01",
      "phase": 1,
      "slice": "S1",
      "title": "Verify and adapt Project A and Project C contracts",
      "state": "planned",
      "depends_on": [
        "P0-T05"
      ],
      "owner": "integration-worker",
      "risk": "high",
      "write_scope": [
        "integration/",
        "app-contract/",
        "docs/architecture/integration.md",
        "tests/integration/"
      ],
      "acceptance": [
        "A/C remain unmodified",
        "Consumed contracts match pinned SHAs",
        "Missing capabilities remain explicit",
        "Cross-contract tests pass"
      ],
      "validators": [
        "upstream_pin",
        "integration_contract",
        "claims"
      ],
      "evidence": [
        "evidence/slices/S1/upstream-integration.json"
      ]
    },
    {
      "id": "P1-T02",
      "phase": 1,
      "slice": "S1",
      "title": "Implement Terraform state, environments, IAM, and network composition",
      "state": "planned",
      "depends_on": [
        "P1-T01"
      ],
      "owner": "cloud-foundation-worker",
      "risk": "high",
      "write_scope": [
        "terraform/",
        "docs/architecture/cloud-foundation.md",
        "tests/terraform/"
      ],
      "acceptance": [
        "Remote state is isolated, versioned, encrypted, and locked",
        "Staging and recovery-lab are separated",
        "Least-privilege OIDC roles and network boundaries are tested",
        "Cost drivers and teardown are explicit"
      ],
      "validators": [
        "terraform_fmt",
        "terraform_validate",
        "terraform_test",
        "tflint",
        "policy",
        "iam_negative",
        "network_negative"
      ],
      "evidence": [
        "evidence/slices/S1/terraform.json"
      ]
    },
    {
      "id": "P1-T03",
      "phase": 1,
      "slice": "S1",
      "title": "Implement hosted PR, plan, apply, drift, evidence, and teardown workflows",
      "state": "planned",
      "depends_on": [
        "P1-T02"
      ],
      "owner": "github-control-plane-worker",
      "risk": "high",
      "write_scope": [
        ".github/workflows/",
        "scripts/ci/",
        "tests/workflows/",
        "docs/operations/hosted-delivery.md"
      ],
      "acceptance": [
        "Actions pinned",
        "PR jobs read-only and credential-free",
        "Cloud jobs use OIDC",
        "Protected environments gate mutations",
        "Safe blocked-change demonstration retained"
      ],
      "validators": [
        "workflow_permissions",
        "workflow_pins",
        "untrusted_pr",
        "oidc_trust",
        "hosted_required_checks"
      ],
      "evidence": [
        "evidence/slices/S1/hosted-ci.json"
      ]
    },
    {
      "id": "P1-T04",
      "phase": 1,
      "slice": "S1",
      "title": "Run S1 engineering, QA, security, evidence, and judge gates",
      "state": "planned",
      "depends_on": [
        "P1-T01",
        "P1-T02",
        "P1-T03"
      ],
      "owner": "s1-gate-controller",
      "risk": "high",
      "write_scope": [
        "docs/reviews/S1/",
        "evidence/slices/S1/",
        "evidence/judges/S1/",
        "ISSUES.md",
        "BREAK_FIX_LOG.md"
      ],
      "acceptance": [
        "All S1 deterministic and hosted checks pass",
        "Three-judge S1 exit passes",
        "Live mutation remains human-gated"
      ],
      "validators": [
        "full_repository",
        "evidence_freshness",
        "claim_consistency",
        "judge_exit"
      ],
      "evidence": [
        "evidence/slices/S1/integrated-gate.json",
        "evidence/judges/S1/"
      ],
      "human_gate": "H1"
    },
    {
      "id": "P2-T01",
      "phase": 2,
      "slice": "S2",
      "title": "Implement Helm-based Kubernetes workload contract",
      "state": "planned",
      "depends_on": [
        "P1-T04"
      ],
      "owner": "kubernetes-contract-worker",
      "risk": "high",
      "write_scope": [
        "kubernetes/chart/",
        "kubernetes/policies/",
        "tests/kubernetes/"
      ],
      "acceptance": [
        "Digest-pinned image",
        "Probes/resources/PDB/spread/HPA",
        "RBAC/workload identity/secrets",
        "Ingress/TLS and network-policy boundaries"
      ],
      "validators": [
        "helm_lint",
        "helm_template",
        "kubeconform",
        "kubernetes_policy",
        "kubernetes_negative"
      ],
      "evidence": [
        "evidence/slices/S2/chart-contract.json"
      ]
    },
    {
      "id": "P2-T02",
      "phase": 2,
      "slice": "S2",
      "title": "Validate locally and apply to managed Kubernetes",
      "state": "planned",
      "depends_on": [
        "P2-T01"
      ],
      "owner": "kubernetes-runtime-worker",
      "risk": "critical",
      "write_scope": [
        "kubernetes/scenarios/",
        "scripts/kubernetes/",
        "evidence/slices/S2/runtime/"
      ],
      "acceptance": [
        "kind preflight clearly labeled local",
        "Protected EKS apply uses OIDC",
        "Digest/identity/health/version/non-root evidence",
        "Live scaling and rolling update evidence"
      ],
      "validators": [
        "kind_runtime",
        "managed_cluster_preflight",
        "kubernetes_smoke",
        "release_identity",
        "autoscaling_runtime"
      ],
      "evidence": [
        "evidence/slices/S2/runtime/"
      ],
      "human_gate": "H2"
    },
    {
      "id": "P2-T03",
      "phase": 2,
      "slice": "S2",
      "title": "Execute Kubernetes failure and recovery matrix",
      "state": "planned",
      "depends_on": [
        "P2-T02"
      ],
      "owner": "kubernetes-failure-worker",
      "risk": "high",
      "write_scope": [
        "kubernetes/scenarios/",
        "operations/incidents/kubernetes/",
        "evidence/slices/S2/scenarios/"
      ],
      "acceptance": [
        "CrashLoop/readiness/scheduling/resource/DNS/network-policy failures reproduced",
        "Every scenario resets",
        "Business behavior verified after recovery"
      ],
      "validators": [
        "scenario_schema",
        "scenario_reset",
        "recovery_smoke",
        "evidence_freshness"
      ],
      "evidence": [
        "evidence/slices/S2/scenarios/"
      ]
    },
    {
      "id": "P2-T04",
      "phase": 2,
      "slice": "S2",
      "title": "Certify S2 Kubernetes slice",
      "state": "planned",
      "depends_on": [
        "P2-T01",
        "P2-T02",
        "P2-T03"
      ],
      "owner": "s2-gate-controller",
      "risk": "high",
      "write_scope": [
        "docs/reviews/S2/",
        "evidence/slices/S2/",
        "evidence/judges/S2/",
        "ISSUES.md",
        "BREAK_FIX_LOG.md"
      ],
      "acceptance": [
        "QA/security/evidence gates pass",
        "Three-judge S2 exit passes"
      ],
      "validators": [
        "full_repository",
        "managed_runtime_claims",
        "judge_exit"
      ],
      "evidence": [
        "evidence/slices/S2/integrated-gate.json",
        "evidence/judges/S2/"
      ]
    },
    {
      "id": "P3-T01",
      "phase": 3,
      "slice": "S3",
      "title": "Implement queue-driven serverless worker",
      "state": "planned",
      "depends_on": [
        "P2-T04"
      ],
      "owner": "serverless-worker",
      "risk": "high",
      "write_scope": [
        "serverless/",
        "terraform/modules/serverless/",
        "tests/serverless/"
      ],
      "acceptance": [
        "Retry/backoff/DLQ/idempotency/concurrency/timeouts",
        "Least-privilege IAM",
        "Correlation and cost telemetry",
        "Malformed/duplicate/poison tests"
      ],
      "validators": [
        "serverless_unit",
        "event_contract",
        "idempotency",
        "iam_negative",
        "dlq_replay"
      ],
      "evidence": [
        "evidence/slices/S3/serverless.json"
      ]
    },
    {
      "id": "P3-T02",
      "phase": 3,
      "slice": "S3",
      "title": "Define and test SaaS operating lifecycle",
      "state": "planned",
      "depends_on": [
        "P3-T01"
      ],
      "owner": "saas-operations-worker",
      "risk": "medium",
      "write_scope": [
        "operations/saas/",
        "tests/saas/",
        "docs/architecture/tenant-boundary.md"
      ],
      "acceptance": [
        "Tenant assumptions and isolation explicit",
        "Onboarding/config/migration/support/suspension/export/deprovision documented and tested where automatable",
        "Severity and escalation ownership defined"
      ],
      "validators": [
        "tenant_boundary",
        "lifecycle_contract",
        "claims"
      ],
      "evidence": [
        "evidence/slices/S3/saas-operations.json"
      ]
    },
    {
      "id": "P3-T03",
      "phase": 3,
      "slice": "S3",
      "title": "Run live serverless negative paths and certify S3",
      "state": "planned",
      "depends_on": [
        "P3-T01",
        "P3-T02"
      ],
      "owner": "s3-gate-controller",
      "risk": "high",
      "write_scope": [
        "operations/incidents/serverless/",
        "docs/reviews/S3/",
        "evidence/slices/S3/",
        "evidence/judges/S3/",
        "ISSUES.md",
        "BREAK_FIX_LOG.md"
      ],
      "acceptance": [
        "End-to-end request/event/result trace",
        "DLQ alarm and replay tested",
        "QA/security/evidence gates pass",
        "Three-judge S3 exit passes"
      ],
      "validators": [
        "serverless_runtime",
        "dlq_runtime",
        "full_repository",
        "judge_exit"
      ],
      "evidence": [
        "evidence/slices/S3/integrated-gate.json",
        "evidence/judges/S3/"
      ]
    },
    {
      "id": "P4-T01",
      "phase": 4,
      "slice": "S4",
      "title": "Instrument end-to-end telemetry and redaction",
      "state": "planned",
      "depends_on": [
        "P3-T03"
      ],
      "owner": "telemetry-worker",
      "risk": "high",
      "write_scope": [
        "observability/otel/",
        "app-contract/telemetry/",
        "tests/observability/"
      ],
      "acceptance": [
        "Correlation across ingress/app/queue/function",
        "Structured logs",
        "RED/USE metrics",
        "Secret/tenant payload redaction"
      ],
      "validators": [
        "telemetry_contract",
        "trace_continuity",
        "log_redaction",
        "metrics_schema"
      ],
      "evidence": [
        "evidence/slices/S4/telemetry.json"
      ]
    },
    {
      "id": "P4-T02",
      "phase": 4,
      "slice": "S4",
      "title": "Implement dashboards, alerts, SLIs, SLOs, and error budget",
      "state": "planned",
      "depends_on": [
        "P4-T01"
      ],
      "owner": "sre-signals-worker",
      "risk": "high",
      "write_scope": [
        "observability/dashboards/",
        "observability/alerts/",
        "operations/slo/",
        "tests/observability/"
      ],
      "acceptance": [
        "Actionable owned alerts with runbooks",
        "Burn-rate/error-budget definitions",
        "Noisy/missing signal tests",
        "Symptom-to-root-cause navigation"
      ],
      "validators": [
        "dashboard_schema",
        "alert_contract",
        "slo_math",
        "alert_negative",
        "runbook_links"
      ],
      "evidence": [
        "evidence/slices/S4/signals.json"
      ]
    },
    {
      "id": "P4-T03",
      "phase": 4,
      "slice": "S4",
      "title": "Run signal-path drills and certify S4",
      "state": "planned",
      "depends_on": [
        "P4-T01",
        "P4-T02"
      ],
      "owner": "s4-gate-controller",
      "risk": "high",
      "write_scope": [
        "operations/incidents/observability/",
        "docs/reviews/S4/",
        "evidence/slices/S4/",
        "evidence/judges/S4/",
        "ISSUES.md",
        "BREAK_FIX_LOG.md"
      ],
      "acceptance": [
        "Synthetic request follows all signals",
        "Alert fires and resolves correctly",
        "QA/security/evidence gates pass",
        "Three-judge S4 exit passes"
      ],
      "validators": [
        "signal_path_runtime",
        "alert_runtime",
        "full_repository",
        "judge_exit"
      ],
      "evidence": [
        "evidence/slices/S4/integrated-gate.json",
        "evidence/judges/S4/"
      ]
    },
    {
      "id": "P5-T01",
      "phase": 5,
      "slice": "S5",
      "title": "Build pressure-usable Linux, Kubernetes, and network runbooks",
      "state": "planned",
      "depends_on": [
        "P4-T03"
      ],
      "owner": "runbook-worker",
      "risk": "high",
      "write_scope": [
        "operations/runbooks/",
        "scripts/diagnostics/",
        "tests/runbooks/"
      ],
      "acceptance": [
        "First-five-minute checks",
        "Exact safe commands",
        "Stop/escalation and do-not-do-yet cautions",
        "App-versus-network isolation logic"
      ],
      "validators": [
        "runbook_schema",
        "command_safety",
        "runbook_links",
        "diagnostic_tests"
      ],
      "evidence": [
        "evidence/slices/S5/runbooks.json"
      ]
    },
    {
      "id": "P5-T02",
      "phase": 5,
      "slice": "S5",
      "title": "Execute eight incident and recovery drills",
      "state": "planned",
      "depends_on": [
        "P5-T01"
      ],
      "owner": "incident-drill-worker",
      "risk": "critical",
      "write_scope": [
        "operations/incidents/",
        "operations/postmortems/",
        "operations/drills/",
        "evidence/slices/S5/drills/"
      ],
      "acceptance": [
        "Eight required scenarios",
        "Two misleading symptoms",
        "Timeline/hypotheses/ruled-out causes/root cause",
        "Recovery and business verification",
        "Regression controls"
      ],
      "validators": [
        "incident_schema",
        "scenario_reset",
        "recovery_smoke",
        "postmortem_contract"
      ],
      "evidence": [
        "evidence/slices/S5/drills/"
      ],
      "human_gate": "H3"
    },
    {
      "id": "P5-T03",
      "phase": 5,
      "slice": "S5",
      "title": "Independently certify incident decision quality and S5",
      "state": "planned",
      "depends_on": [
        "P5-T01",
        "P5-T02"
      ],
      "owner": "s5-gate-controller",
      "risk": "high",
      "write_scope": [
        "docs/reviews/S5/",
        "evidence/slices/S5/",
        "evidence/judges/S5/",
        "ISSUES.md",
        "BREAK_FIX_LOG.md"
      ],
      "acceptance": [
        "Independent operators can follow runbooks",
        "Recovery decisioning is evidence-based",
        "Three-judge S5 exit passes"
      ],
      "validators": [
        "runbook_dry_run",
        "incident_consistency",
        "full_repository",
        "judge_exit"
      ],
      "evidence": [
        "evidence/slices/S5/integrated-gate.json",
        "evidence/judges/S5/"
      ]
    },
    {
      "id": "P6-T01",
      "phase": 6,
      "slice": "S6",
      "title": "Harden identity, secrets, policy, and software supply chain",
      "state": "planned",
      "depends_on": [
        "P5-T03"
      ],
      "owner": "security-platform-worker",
      "risk": "critical",
      "write_scope": [
        "kubernetes/policies/",
        "terraform/policies/",
        "security/",
        "tests/security/",
        "docs/architecture/security.md"
      ],
      "acceptance": [
        "Least privilege and negative tests",
        "Managed secrets/rotation/redaction",
        "SBOM and triage",
        "Unsafe deployments blocked"
      ],
      "validators": [
        "secret_scan",
        "sbom",
        "vulnerability_policy",
        "iam_negative",
        "rbac_negative",
        "admission_negative"
      ],
      "evidence": [
        "evidence/slices/S6/security.json"
      ]
    },
    {
      "id": "P6-T02",
      "phase": 6,
      "slice": "S6",
      "title": "Implement evidence-backed Azure governance companion",
      "state": "planned",
      "depends_on": [
        "P6-T01"
      ],
      "owner": "azure-governance-worker",
      "risk": "high",
      "write_scope": [
        "azure/",
        "docs/architecture/azure-governance.md",
        "tests/azure/"
      ],
      "acceptance": [
        "Policy/tag/naming/RBAC/log/cost/network controls",
        "Blocked-change examples",
        "Implemented-versus-designed boundary",
        "No false Azure networking depth"
      ],
      "validators": [
        "azure_static",
        "azure_policy_negative",
        "claims"
      ],
      "evidence": [
        "evidence/slices/S6/azure-governance.json"
      ]
    },
    {
      "id": "P6-T03",
      "phase": 6,
      "slice": "S6",
      "title": "Implement human-gated GitHub agentic operations workflow",
      "state": "planned",
      "depends_on": [
        "P6-T01"
      ],
      "owner": "agentic-workflow-worker",
      "risk": "critical",
      "write_scope": [
        "agentic/",
        ".github/workflows/agentic-*",
        "tests/agentic/",
        "operations/runbooks/agentic.md"
      ],
      "acceptance": [
        "Evidence gathering and remediation proposal",
        "No default mutation authority",
        "Protected human gate",
        "Prompt-injection/unsafe-command/forged-evidence/stale-runbook tests"
      ],
      "validators": [
        "agent_permission",
        "prompt_injection",
        "unsafe_proposal",
        "evidence_forgery",
        "workflow_permissions"
      ],
      "evidence": [
        "evidence/slices/S6/agentic.json"
      ],
      "human_gate": "H4"
    },
    {
      "id": "P6-T04",
      "phase": 6,
      "slice": "S6",
      "title": "Run independent security council and certify S6",
      "state": "planned",
      "depends_on": [
        "P6-T01",
        "P6-T02",
        "P6-T03"
      ],
      "owner": "s6-gate-controller",
      "risk": "critical",
      "write_scope": [
        "docs/reviews/S6/",
        "evidence/slices/S6/",
        "evidence/judges/S6/",
        "ISSUES.md",
        "BREAK_FIX_LOG.md"
      ],
      "acceptance": [
        "No open critical/high finding",
        "Unsafe identity and agent paths blocked",
        "Three-judge S6 exit passes"
      ],
      "validators": [
        "full_security",
        "full_repository",
        "claim_consistency",
        "judge_exit"
      ],
      "evidence": [
        "evidence/slices/S6/integrated-gate.json",
        "evidence/judges/S6/"
      ]
    },
    {
      "id": "P7-T01",
      "phase": 7,
      "slice": "S7",
      "title": "Implement backup, restore, rollback, and failure recovery contracts",
      "state": "planned",
      "depends_on": [
        "P6-T04"
      ],
      "owner": "recovery-worker",
      "risk": "critical",
      "write_scope": [
        "operations/recovery/",
        "scripts/recovery/",
        "tests/recovery/",
        "evidence/slices/S7/recovery/"
      ],
      "acceptance": [
        "Justified RTO/RPO",
        "Isolated restore",
        "Digest/health/version/data/business verification",
        "No rollback without known-good target or first-release decision"
      ],
      "validators": [
        "backup_contract",
        "restore_runtime",
        "rollback_runtime",
        "data_integrity",
        "rto_rpo"
      ],
      "evidence": [
        "evidence/slices/S7/recovery/"
      ]
    },
    {
      "id": "P7-T02",
      "phase": 7,
      "slice": "S7",
      "title": "Run performance baseline, bottleneck repair, and capacity proof",
      "state": "planned",
      "depends_on": [
        "P7-T01"
      ],
      "owner": "performance-worker",
      "risk": "high",
      "write_scope": [
        "performance/",
        "operations/capacity/",
        "evidence/slices/S7/performance/"
      ],
      "acceptance": [
        "Repeatable load profile",
        "p50/p95/p99/errors/saturation/scaling",
        "One root-cause repair",
        "Quantified before/after"
      ],
      "validators": [
        "load_profile",
        "performance_result_schema",
        "before_after",
        "capacity_claims"
      ],
      "evidence": [
        "evidence/slices/S7/performance/"
      ]
    },
    {
      "id": "P7-T03",
      "phase": 7,
      "slice": "S7",
      "title": "Implement FinOps controls and execute approved teardown",
      "state": "planned",
      "depends_on": [
        "P7-T01",
        "P7-T02"
      ],
      "owner": "finops-worker",
      "risk": "critical",
      "write_scope": [
        "operations/finops/",
        "scripts/teardown/",
        "evidence/slices/S7/cost/"
      ],
      "acceptance": [
        "Budget/alerts/tags/right-sizing/idle detection",
        "Estimated and available actual cost",
        "Inventory before teardown",
        "Expected resources removed and evidence retained"
      ],
      "validators": [
        "cost_model",
        "budget_policy",
        "resource_inventory",
        "teardown_reconciliation"
      ],
      "evidence": [
        "evidence/slices/S7/cost/"
      ],
      "human_gate": "H5"
    },
    {
      "id": "P7-T04",
      "phase": 7,
      "slice": "S7",
      "title": "Certify S7 resilience, performance, and cost slice",
      "state": "planned",
      "depends_on": [
        "P7-T01",
        "P7-T02",
        "P7-T03"
      ],
      "owner": "s7-gate-controller",
      "risk": "critical",
      "write_scope": [
        "docs/reviews/S7/",
        "evidence/slices/S7/",
        "evidence/judges/S7/",
        "ISSUES.md",
        "BREAK_FIX_LOG.md"
      ],
      "acceptance": [
        "Recovery/performance/cost evidence agrees",
        "Three-judge S7 exit passes"
      ],
      "validators": [
        "recovery_consistency",
        "performance_consistency",
        "cost_consistency",
        "full_repository",
        "judge_exit"
      ],
      "evidence": [
        "evidence/slices/S7/integrated-gate.json",
        "evidence/judges/S7/"
      ]
    },
    {
      "id": "P8-T01",
      "phase": 8,
      "slice": "S8",
      "title": "Rebuild integrated evidence and claims index",
      "state": "planned",
      "depends_on": [
        "P7-T04"
      ],
      "owner": "evidence-assembly-worker",
      "risk": "high",
      "write_scope": [
        "evidence/manifests/",
        "docs/claims/",
        "docs/architecture/",
        "docs/evidence-index.md"
      ],
      "acceptance": [
        "Append-only events reconcile",
        "Every claim maps to evidence IDs",
        "Tense/status consistent",
        "Superseded evidence explicit"
      ],
      "validators": [
        "evidence_chain",
        "evidence_freshness",
        "claim_consistency",
        "architecture_consistency"
      ],
      "evidence": [
        "evidence/slices/S8/evidence-index.json"
      ]
    },
    {
      "id": "P8-T02",
      "phase": 8,
      "slice": "S8",
      "title": "Create recruiter-ready front page, architecture visual, operator, portfolio, and interview handoff",
      "state": "planned",
      "depends_on": [
        "P8-T01"
      ],
      "owner": "delivery-worker",
      "risk": "medium",
      "write_scope": [
        "README.md",
        "docs/architecture/continuityops.drawio",
        "docs/architecture/continuityops-reference.png",
        "docs/portfolio/continuityops-infographic.png",
        "docs/operator/",
        "docs/portfolio/",
        "docs/handoff/"
      ],
      "acceptance": [
        "Editable draw.io source and exact render",
        "Image2-generated 16:9 infographic matches architecture/evidence",
        "README is recruiter-scannable in under 60 seconds with visual first",
        "One-command safe entry points",
        "Demo and interview walkthrough",
        "Claim-safe bullets",
        "Explicit non-claims and current teardown status"
      ],
      "validators": [
        "drawio_schema",
        "diagram_render_freshness",
        "infographic_parity",
        "readme_recruiter_gate",
        "links",
        "operator_dry_run",
        "claim_consistency",
        "secret_scan"
      ],
      "evidence": [
        "evidence/slices/S8/delivery.json"
      ]
    },
    {
      "id": "P8-T03",
      "phase": 8,
      "slice": "S8",
      "title": "Logically repartition the completed codebase and certify every final partition",
      "state": "planned",
      "depends_on": [
        "P8-T01",
        "P8-T02"
      ],
      "owner": "postbuild-partition-controller",
      "risk": "critical",
      "write_scope": [
        "harness/postbuild-partition-manifest.json",
        "harness/rubrics/postbuild/",
        "docs/reviews/postbuild/",
        "evidence/postbuild/",
        "ISSUES.md",
        "BREAK_FIX_LOG.md"
      ],
      "acceptance": [
        "Final dependency graph creates logical capability partitions",
        "Shared interfaces have integration rubrics",
        "Every partition completes a saved remediation council",
        "Every provisional pass is validated by fresh judges",
        "Fresh failure receives fresh nixers and fixers",
        "All partition breaks are logged"
      ],
      "validators": [
        "postbuild_partition_unique_ownership",
        "shared_interface_map",
        "saved_fresh_council",
        "full_repository",
        "judge_exit"
      ],
      "evidence": [
        "evidence/postbuild/"
      ]
    },
    {
      "id": "P8-T04",
      "phase": 8,
      "slice": "S8",
      "title": "Run clean-room integrated certification council",
      "state": "planned",
      "depends_on": [
        "P8-T03"
      ],
      "owner": "final-council-controller",
      "risk": "critical",
      "write_scope": [
        "docs/reviews/final/",
        "evidence/slices/S8/",
        "evidence/judges/S8/",
        "ISSUES.md",
        "BREAK_FIX_LOG.md"
      ],
      "acceptance": [
        "Fresh durable-context-only orchestration",
        "Full local and hosted validation on final SHA",
        "Three clean judges pass all exit rules",
        "Recruiter infographic and README match final evidence",
        "Process deviations disclosed"
      ],
      "validators": [
        "full_repository",
        "full_security",
        "hosted_required_checks",
        "evidence_chain",
        "claim_consistency",
        "readme_recruiter_gate",
        "judge_exit"
      ],
      "evidence": [
        "evidence/slices/S8/integrated-gate.json",
        "evidence/judges/S8/"
      ],
      "human_gate": "H6"
    }
  ]
}
```

## State-transition invariants

- No task moves directly to `done`.
- Later phases remain unauthorized until a human changes
  `authorized_through_phase` and the authorization regression passes.
- A task’s evidence is valid only for its recorded candidate SHA, upstream pins,
  partition hash, validator hash, environment, and approval receipt.
- Any changed binding returns affected verified tasks to review and invalidates
  dependent slice certification.
- Judge tasks are read-only and cannot satisfy implementation acceptance by
  writing code.
- External blockers freeze dependent lanes, not unrelated read-only planning or
  review lanes.
