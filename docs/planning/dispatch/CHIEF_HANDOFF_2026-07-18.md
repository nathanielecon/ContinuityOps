# Chief Supervisor Handoff — ContinuityOps LIVE AWS (2026-07-18)

> **Audience:** next Cursor Cloud **chief supervisor** seat.  
> Machine field names English; free-text Mandarin per D-015.  
> Chat history is **not** authoritative — reconstruct from this file + paths below.

---

## 0. Owner paste (start new Cloud Agent with this)

```text
You are ContinuityOps CHIEF SUPERVISOR (D-041). Read and follow in order:
1) docs/planning/dispatch/CHIEF_HANDOFF_2026-07-18.md (this handoff)
2) docs/planning/dispatch/CHIEF_SUPERVISOR.md
3) AGENTS.md (Live AWS + authority order)
4) OPERATING_STATE.md + PLAN.md + BREAK_FIX_LOG.md (BF-2026-010, BF-2026-011)

FIRST COMMANDS:
  node scripts/assert-cloud-seat-gh-token.mjs   # must PASS
  git fetch origin main && git checkout main && git pull origin main && git rev-parse HEAD

Doctrine: Live AWS = GHA OIDC → continuityops-gha. NoCredentials for aws sts EXPECTED.
No AWS keys. No Cursor STS / CursorCloudAgent. No project-a-lzlab-gha.
D-044: no more human gates. D-045: GPT junior/orch/reviewer/workers; Grok monitor only. No Opus.
Job: Terraform PR → plan green → merge main → confirm apply green → evidence → elevate claims only with run URLs.
```

---

## 1. Role disambiguation（角色辨析）

| Seat | Who | Owns | Does **not** own |
| --- | --- | --- | --- |
| **Owner (human)** | `nathanielecon` | Constitutional crises, secrets minting agent cannot create, spend ceilings, external publication | Day-to-day merge/dispatch (D-044 cleared phase gates) |
| **Chief supervisor (YOU)** | This Cursor Cloud session | Stream-boundary verdicts (BF-PRE-015); escalations; replace stuck junior; monitor intake; **currently also** drive live-AWS loop because junior App path is secondary under D-043 | In-pod AWS apply; inventing keys; minting H0–H6; Opus |
| **Junior supervisor** | `cursor-grok-4.5-high` episodic | Steady-state judgment; D-042 intent markers for App actuation | Direct `gh` in App sandbox; other streams’ authority |
| **Orchestrator** | Grok episodic | Ready work, scopes, break/fix log, intents — **never merges** | Implementation code; self-approval of high risk |
| **D-037 reviewer** | Independent Grok | Apply patch @ `base_sha`, run checks, `verdict` only | Code edits; merge |
| **Workers** | Grok cloud/subagent | Bounded `write_scope` implementation + tests | Authoritative state; credentials |
| **Monitor** | Grok read-only | Significant-only reports **to chief** | Actuation |

**Actuation vs judgment:** judgment = decide; actuation = `gh`/merge/label/workflow. Chief may actuate when junior path is unavailable (this engagement: chief has `GH_TOKEN` and git push).

**Engagement overrides still in force:**
- **D-043:** all episodic seats = `cursor-grok-4.5-high`; Codex `@codex` product path **suspended**
- **D-044:** no more human phase gates; `authorized_through_phase: 8`
- **No Opus** under any circumstances
- Inter-agent free text: **Simplified Chinese**; recruiter artifacts English

---

## 2. Subordinates & how to dispatch（下属与派遣）

| Role | Carrier | How chief uses them |
| --- | --- | --- |
| Junior | Grok subagent / App (receive-only) | Appoint when needed; D-042 intents → `junior-actuate.yml` if App cannot `gh` |
| Orchestrator / workers / reviewer | In-session Grok Task/subagent **or** repo PR workflow | Prefer: chief opens Terraform/docs PRs directly when faster; use Grok for bounded implementation |
| Monitor | Read-only Grok | Significant bottlenecks only → chief |

**Default live-AWS execution (current objective):** chief (or worker) edits `terraform/**` → PR → confirm **ContinuityOps Terraform** plan green → merge `main` → confirm **apply** green → write evidence. Do **not** wait on Cursor STS.

---

## 3. Dependencies（依赖 — 已满足 / 缺口）

### 3.1 LIVE control plane（满足）

| Dependency | Status | Proof |
| --- | --- | --- |
| IAM role `continuityops-gha` | LIVE | `arn:aws:iam::000000000000:role/continuityops-gha` |
| Repo id trust | LIVE | `1301990908` (never LZ lab `1296742987`) |
| Workflow | LIVE | `.github/workflows/continuityops-terraform.yml` |
| GitHub Environment `continuityops` | LIVE | no required reviewers / wait timer |
| OIDC plan | GREEN | https://github.com/nathanielecon/ContinuityOps/actions/runs/29642718513 |
| OIDC apply | GREEN | https://github.com/nathanielecon/ContinuityOps/actions/runs/29643569047 |
| Remote state | LIVE | bucket `continuityops-tfstate-000000000000`, lock `continuityops-tf-locks` |
| Staging smoke resource | LIVE | `/continuityops/staging/live-marker` (CloudWatch log group) |
| Evidence file | On main | `evidence/hosted/cloud-apply-staging-2026-07-18.json` |

### 3.2 GitHub seat token（关键 — 开席必验）

| Check | Command / expectation |
| --- | --- |
| Assert | `node scripts/assert-cloud-seat-gh-token.mjs` → **PASS** |
| On FAIL | **Stop.** Tell owner: restart Cloud Agent after Cursor Secret `GH_TOKEN` refresh. Do **not** chase AWS. |
| Secret | Cursor Secrets → `GH_TOKEN` = fine-grained PAT, All repositories; Contents/PRs/Issues/Actions/Workflows R/W |
| Identity | `gh api user -q .login` → `nathanielecon` (PAT), not only App `ghs_` |

### 3.3 Explicitly NOT dependencies

- `CURSOR_AWS_ASSUME_IAM_ROLE_ARN` / `CursorCloudAgent` (never assumed; Pro+ no team External ID)
- Long-lived AWS keys in Cloud secrets
- `project-a-lzlab-gha` / `landing-zone-lab.yml` (Project A / other repo only)
- In-pod `aws sts get-caller-identity` success (`NoCredentials` **expected**)

### 3.4 Optional / non-blocking

- `REPO_SETTINGS_ADMIN_TOKEN`, PR #20 (settings-as-code) — tooling, not constitutional stop (D-044)
- Codex warm env `6a594ee667608191ab53cae15202815e` — registered; not default worker under D-043

---

## 4. Catch-up file index（必读顺序）

Read in this order; do not invent from chat:

1. **This handoff** — `docs/planning/dispatch/CHIEF_HANDOFF_2026-07-18.md`
2. **Chief charter** — `docs/planning/dispatch/CHIEF_SUPERVISOR.md`
3. **Authority / live AWS** — `AGENTS.md` (authority order + Live AWS section + stuck paste)
4. **Machine state** — `OPERATING_STATE.md` (revision ≥39; `authorized_through_phase: 8`)
5. **Task authority** — `PLAN.md` (all P0–P8 verified at L1; elevate with evidence)
6. **Break/fix** — `BREAK_FIX_LOG.md` → **BF-2026-010**, **BF-2026-011** (and BF-PRE-002 if needed)
7. **Claims** — `docs/claims/matrix.json` (`terraform-scaffold` + `hosted-ci-stubs` = **L4 smoke**; portfolio gate still `portfolio-certified-L1`)
8. **Apply evidence** — `evidence/hosted/cloud-apply-staging-2026-07-18.json`
9. **Terraform** — `terraform/README.md`, `terraform/envs/staging/`, `terraform/ci-bootstrap/`
10. **Junior/monitor (when used)** — `JUNIOR_SUPERVISOR.zh.md`, `MONITOR.zh.md`, `JUNIOR_ACTUATE_SNIPPET.zh.md`

**Repo / tip (verify on start):**
- Repo: `nathanielecon/ContinuityOps`
- Expected main tip at handoff authoring: `c947de10f15fc161cac13761cdc99b2b2bf91eb6`
- Account (not secret): `000000000000`

---

## 5. Session break/fix log（本会话关键 BF）

| ID | What happened | Resolution |
| --- | --- | --- |
| **BF-2026-010** | Agents blocked on Cloud `NoCredentials` + set `CURSOR_AWS_ASSUME_IAM_ROLE_ARN` | **Not** Cursor STS. Pro+ lacks team External ID. Fix = change control plane to GHA OIDC. `CursorCloudAgent` **never assumed**. |
| **Control plane switch** | Early docs pointed at `project-a-lzlab-gha` / `landing-zone-lab.yml` | **Wrong for ContinuityOps.** Use `continuityops-gha` + `continuityops-terraform.yml` only. |
| **PR #50** | OIDC workflow + bootstrap | Landed on `main` (`20266d3`) via fast-forward push (Merge API was 403 on old PAT) |
| **PR #51** | Remote state + staging live-marker | Landed (`21299f9`); OIDC **plan** green `29642718513`; `terraform-pr` static was red |
| **Static red** | `node --test tests/terraform/` MODULE_NOT_FOUND on Node 22 | Fixed: `node --test tests/terraform/*.mjs` |
| **BF-2026-011** | First main apply `29643490577` failed — DynamoDB lock table create race | OIDC OK. Re-dispatch apply **green** `29643569047`. `ensure-tfstate.sh` hardened for `ResourceInUseException` / bucket race (`c947de1`) |
| **GH_TOKEN** | Actions/merge 403 on fine-grained PAT lacking Actions | Owner refreshed Cursor Secret (repo+workflow). **New seat must assert PASS.** Old pods keep old token until restart. |
| **Assert script** | Added `scripts/assert-cloud-seat-gh-token.mjs` | Gate for Actions/merge autonomy |

**Doctrine phrase:** injection absent — stop; no keys.  
**Stuck paste:** see `AGENTS.md` § Paste for stuck ContinuityOps agents.

---

## 6. Current objective & completion definition（目标与完成标准）

### Objective
Drive ContinuityOps **live AWS** elevation through the GHA OIDC loop; keep claims honest; never block on Cursor STS.

### Loop (no human after bootstrap)
```text
edit terraform/** → open PR → ContinuityOps Terraform PLAN green
  → merge main → auto APPLY green → record evidence (run URL + sha)
  → update docs/claims/matrix.json only for scopes actually proven
```

Fallback only:
```bash
gh workflow run continuityops-terraform.yml --repo nathanielecon/ContinuityOps \
  -f action=plan -f environment=staging
# apply:
gh workflow run continuityops-terraform.yml --repo nathanielecon/ContinuityOps \
  -f action=apply -f environment=staging
```

### Done when (near-term)
1. `assert-cloud-seat-gh-token.mjs` **PASS** on this seat  
2. Next Terraform mutations (beyond live-marker) have **plan + apply** green run URLs in `evidence/hosted/`  
3. Claims elevated **only** for proven scope; non_claims stay honest (no fake EKS/Lambda/RTO)  
4. `BREAK_FIX_LOG.md` updated for any new break  
5. `OPERATING_STATE.md` revision bumped; `next_actions` accurate  

### Portfolio honesty
- Gate label may remain `portfolio-certified-L1` until broader recert  
- Component L4 smoke ≠ full platform L4+  

---

## 7. Immediate runbook（开席 15 分钟）

```bash
# 1) Token gate
node scripts/assert-cloud-seat-gh-token.mjs
# FAIL → stop; owner restarts seat. Do not chase AWS.

# 2) Sync
git fetch origin main && git checkout main && git pull origin main
git rev-parse HEAD   # note tip

# 3) Confirm last apply (API)
gh api repos/nathanielecon/ContinuityOps/actions/runs/29643569047 \
  --jq '{conclusion,head_sha,html_url}'

# 4) Confirm AWS still NoCredentials here (expected)
aws sts get-caller-identity 2>&1 || true
# Expect NoCredentials / unable to locate credentials

# 5) Choose next Terraform elevation (examples — pick one bounded PR)
#    - enable staging network module (guarded) OR
#    - add tagged lab S3 / IAM interface resources with enable flags OR
#    - wire recovery-lab marker similarly
# Open PR → wait ContinuityOps Terraform plan → merge → confirm apply

# 6) Evidence
# Write evidence/hosted/cloud-apply-<env>-<date>.json with run URLs + candidate_sha
# Update docs/claims/matrix.json only for that scope
```

### Branch / PR rules
- Feature branches: `cursor/<descriptive>-7c3d`
- Prefer PR → plan → merge (auto apply). If Merge API fails but Contents push works, fast-forward `main` only with owner doctrine / D-044 and record in BF log.
- Never put AWS keys in repo or Cursor secrets for apply.

---

## 8. Worker handoff shape（若派遣 Grok worker）

Reject if missing fields. Free-text values **简体中文**:

```yaml
task_id:
role: worker|reviewer|orchestrator|junior
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

---

## 9. Predecessor seat note

- Predecessor chief main tip at handoff write: `c947de1`  
- Predecessor recorded LIVE loop, BF-2026-010/011, claims L4 smoke, assert script  
- Predecessor often used **git push fast-forward** when Merge/Actions API 403  
- After owner token permission update, assert may PASS without new pod — **still re-run assert** on every new chief start  

---

## 10. Absolute prohibitions

1. Do not invent AWS access keys or root session tokens  
2. Do not block on `CURSOR_AWS_ASSUME_IAM_ROLE_ARN` / CursorCloudAgent  
3. Do not use `project-a-lzlab-gha` / `landing-zone-lab.yml` for ContinuityOps  
4. Do not claim L4+ for EKS/Lambda/Azure/RTO without matching apply evidence  
5. Do not use Opus  
6. Do not `codex login` in cloud containers  
7. Do not delete failing tests / weaken validators to raise scores  

---

*End of handoff. Reconstruct only from durable artifacts; bump this file when control plane or tip materially changes.*
