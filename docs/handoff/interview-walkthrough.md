# Interview walkthrough

Recruiter-facing path aligned to the root README and [`docs/claims/matrix.json`](../claims/matrix.json) (engagement **A3**). Do not overclaim beyond those ceilings.

## 60-second scan

| Step | Open | Say (claim-safe) |
| --- | --- | --- |
| 1 | Root [README](../../README.md) + [infographic](../portfolio/continuityops-infographic.png) | ContinuityOps is a governed cloud-ops lab: OIDC delivery, K8s/serverless contracts, drills, recovery fixtures, agentic proposals behind a protected gate. |
| 2 | [`docs/claims/matrix.json`](../claims/matrix.json) | **Ceiling:** scoped **AWS lab L4** via `continuityops-gha` (apply + lab drill/RTO + teardown). A3: security-sbom **L2**, agentic-workflow **L3**, upstream **L2**, performance **L1**, Azure live **out**. |
| 3 | [`evidence/hosted/`](../../evidence/hosted/) | Lab proof tip-inherited from recorded runs — not re-applied on every tip. |
| 4 | README **Explicit non-claims** | Close with the same non-claims as the README (below). |

## 5-minute demo script

Follow this order. Keep language identical to the README ceilings.

### 1. README infographic (~45s)

1. Open the root README hero image: `docs/portfolio/continuityops-infographic.png`.
2. One sentence: protected GitHub OIDC is the cloud control plane; agents propose remediation and do not hold default mutation authority.
3. Point at **Current claim ceiling: scoped AWS lab L4** via GitHub OIDC → `continuityops-gha`.

### 2. Claims matrix — A3 ceilings (~60s)

1. Open `docs/claims/matrix.json`.
2. State `max_claim_level` / `max_claim_scope`: AWS lab staging via `continuityops-gha` (apply + lab drill/RTO + teardown); not production; not Azure.
3. Call out `engagement_ceilings_A3` only:
   - `lab_stack`: **L4**
   - `security_sbom`: **L2**
   - `agentic_workflow`: **L3**
   - `upstream_integration`: **L2**
   - `performance`: **L1**
   - `azure_live`: **out**
4. Do **not** say every component is L1. Component levels differ under A3.

### 3. Hosted lab evidence (~2 min)

Open files under `evidence/hosted/` (names match README “Results at a glance”):

| Story | File | What to say |
| --- | --- | --- |
| Elevation apply (EKS / Lambda / SQS / VPC) | [`cloud-apply-staging-elevation-2026-07-18.json`](../../evidence/hosted/cloud-apply-staging-elevation-2026-07-18.json) | Live staging apply via OIDC → `continuityops-gha` (apply run recorded in the elevation artifact). |
| Lab drill / RTO | [`lab-drill-rto-29645042815.json`](../../evidence/hosted/lab-drill-rto-29645042815.json) | Lab incident drill only — measured lab RTO; not a production/customer drill. |
| Teardown | Same elevation artifact (`runs.teardown_staging`) — README binds teardown to the elevation / FinOps L4 row | `terraform destroy` staging via `continuityops-gha` (teardown run recorded alongside apply/drill). |

Emphasize: hosted apply / drill / teardown evidence is **tip-inherited** from those recorded runs.

### 4. Agentic hosted-control — D-034 / D-042 (~60s)

1. Open [`agentic-workflow-2026-07-18.json`](../../evidence/hosted/agentic-workflow-2026-07-18.json).
2. Claim level **L3**: GitHub-hosted control plane only.
   - **D-034** — patch-in-comment publisher (`codex-patch-publish`): App workers ship a marker + unified diff; GHA applies and opens the PR.
   - **D-042** — junior actuation intents (`junior-actuate`): judgment stays in the App; merge/dispatch actuation is marker-gated GHA, not sandbox `git push` / `gh`.
3. Explicit: **not** in-pod / CursorCloudAgent AWS credentials. Cloud mutation for the lab stack remains OIDC → `continuityops-gha`.

### 5. Explicit non-claims (match README) (~45s)

Close with the README list — do not invent softer wording:

- No **production** (customer) incident drills — lab drills only
- No CursorCloudAgent / in-pod AWS credentials (OIDC control plane by design)
- No live **Azure** apply — ContinuityOps AWS-lab ceiling (D-046)
- No ContinuityOps known-good **rollback** digest proven
- Performance remains **L1** (no live load proof)
- Azure governance is designed/static (no ExpressRoute depth)
- Hosted lab apply/drill/teardown evidence is **tip-inherited** from recorded runs (not re-applied on every tip)

## Quick truth table (if challenged)

| Topic | Correct A3 statement |
| --- | --- |
| Lab stack | Scoped AWS lab **L4** via `continuityops-gha` |
| Performance | **L1** — honest; no live load proof |
| Azure | Live apply **out** |
| Rollback | **None** proven as a ContinuityOps known-good digest |
| Hosted evidence | Tip-inherited from recorded apply / drill / teardown runs |
| Agentic | **L3** hosted-control (D-034 / D-042), not in-pod AWS |
