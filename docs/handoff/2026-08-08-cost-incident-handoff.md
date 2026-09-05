# Handoff — cloud cost incident, 2026-08-08

Complete state of the ContinuityOps cost investigation and the cross-project work it
pulled in. Written so a fresh operator or agent can continue without re-deriving
anything. Ledger detail lives in `BREAK_FIX_LOG.md` as BF-2026-029 … BF-2026-033.

---

## 1. What happened

A ~$300 AWS overrun in account `000000000000`, caused by ContinuityOps' own CI.

**Timeline, reconstructed from repo evidence and billing data:**

| When (UTC) | Event |
| --- | --- |
| 2026-07-18 12:45 | Full apply — VPC, IAM, Lambda/SQS, EKS `cops-staging` 1.32 + node group (run `29644662492`) |
| 2026-07-18 13:02 | **Correct teardown** (run `29645052414`) |
| 2026-07-18 13:16:29 | **Rebuilt** — 14 minutes later, to close an evidence-hierarchy task (run `29645813983`) |
| 2026-07-18 19:41 | `2ab4f2e` merged — a **whitespace-only `terraform fmt` commit**, 32 insertions / 32 deletions, zero semantic change |
| 2026-07-18 → 2026-08-08 | **491.7 hours** running, unnoticed |
| 2026-08-08 01:00:47 | Torn down (run `31231087928`) — 26 resources destroyed |

**Two independent causes, both required:**

1. **Auto-apply on push to `main`.** `continuityops-terraform.yml` applied on any push
   touching `terraform/**`. Environment `continuityops` had no required reviewers and
   no wait timer, so a formatting commit provisioned infrastructure unreviewed. Path
   filters cannot distinguish `terraform fmt` from a real change.
2. **Extended-support pricing.** `cluster_version = "1.32"` left EKS standard support
   on 2026-03-23, so the control plane billed **$0.60/cluster/hour, not $0.10** — 6×
   the repository's own cost model. `BF-2026-012` bumped 1.29 → 1.32 to clear an apply
   failure and walked straight into it. Nothing in the repo could detect this.

Nothing caught it because the cost plane was documentation: `operations/finops/budgets.json`
was never deployed as an AWS Budget, `scripts/teardown/inventory-dry-run.mjs` returns a
hardcoded fixture, and `scripts/teardown/reconcile.mjs` **throws** if a live teardown is
reported — while `docs/claims/matrix.json` carried `finops-teardown` at **L4**.

**Verified stopped.** Cost Explorer, EKS line by day: `$14.40` (Aug 6) → `$14.40`
(Aug 7) → **`$0.582`** (Aug 8). $0.582 ÷ $0.60 = 0.97 hours, matching the 01:00:47Z
teardown to within four minutes.

---

## 2. Account state now

**ContinuityOps: $0/day.** `eks list-clusters` empty. State bucket and lock table
retained deliberately (cents/month) so the lab stays re-appliable.

**Guardrails live** (run `31272877386`, root `terraform/envs/account`, never destroyed
by `teardown.yml` by design):

- AWS Budget `continuityops-monthly`, **$100/month**, alerts at 50 / 80 / 100% actual
  plus **100% forecasted** — the forecast alert is the one that would have caught this
  around day three
- Budget **action** at 100%: attaches `continuityops-budget-deny-provisioning` to
  `continuityops-gha`. **Denies creates, never deletes** — denying deletes on breach
  would trap the account in the expensive state the guard exists to escape
- `continuityops-agent-ro` + `ContinuityOpsAgentReadOnly` — read-only cost/inventory
  identity with an explicit `Deny` on `s3:GetObject`, DynamoDB item reads, `kms:Decrypt`,
  Secrets Manager, SSM parameters and CloudWatch log events. Created to replace **root
  access keys**, which the AWS connector was authenticating with
- `ContinuityOpsGhaFinOpsAddon` — attached to the deploy role **by role name**, so the
  role was never imported and its OIDC trust policy never touched

**Still billing ≈ $46/month, none of it ContinuityOps:**

| Owner | Resource | $/day |
| --- | --- | --- |
| Project C | ALB `project-c-stg` | 0.540 |
| Project C | Fargate `project-c-delivery-api` (1 task) | 0.296 |
| shared | Public IPv4 × 3 | 0.360 |
| Project A | CloudTrail × 2 | 0.222 |
| Project A | KMS × 3 CMKs | 0.097 |
| Project A | S3 + ECR | 0.011 |

All in `us-east-1`. Nothing hidden in another region (`us-west-2` = $0.00002).

---

## 3. Delivered, by repository

### `nathanielecon/ContinuityOps` — branch `claude/cloud-bill-investigation-7lp3g0`

15 commits, `8e5e1d6` … `9800f5f`. Tests 94 → **121**, all passing.

- **`8e5e1d6`** — apply is `workflow_dispatch`-only. Removed the `push:` trigger
  entirely rather than gating the job: a gated-but-present trigger still creates runs,
  and `lab-drill-rto.yml` chains off this workflow's `workflow_run` success. Rewrote
  the `AGENTS.md` contract, which *mandated* the removed behaviour — leaving that text
  is how it regresses.
- **`9d44cb4`** — guardrails as code: `terraform/envs/account` (separate state key, so
  the budget guard is not destroyed by the teardown it polices), EKS support-calendar
  guard, `TeardownPolicy` tags, nightly scheduled teardown with `COPS_LAB_KEEP_ALIVE`
  escape hatch, `cluster_version` 1.32 → **1.34**.
- **`794a003`** — the no-op guard reads `terraform show -json`, not an exit code.
  `setup-terraform`'s wrapper swallowed `plan -detailed-exitcode`'s exit 2, so a plan
  of "10 to add" read as "no changes" and the job went green having done nothing —
  worse than the bug it replaced. `terraform_wrapper: false` added everywhere exit
  status matters, including `teardown.yml`, where the same behaviour could report a
  **failed destroy as success**.
- **`1fad34f`** — alert email is a masked **secret**, scoped to the apply job. A
  repository *variable* would have printed the address into public Actions logs, and
  workflow-level `env` would have handed it to the PR-triggered plan job.
- **`e349843`** — `scripts/teardown/aws-cost-teardown.sh`, the first thing in that
  directory that touches real resources.
- **`9800f5f`** — `evidence/hosted/cloud-teardown-staging-2026-08-08.json`, recovered
  from the run log before its ~90-day expiry.
- **`5bb4ffe`** — corrected upstream repo names (see §7).

### `nathanielecon/local-first-governed-cicd` (Project C) — branch `claude/pre-teardown-evidence-2026-08-08`

- **`f88b7f9`** — `evidence/phase-9/20260808T191039Z-*`: live smoke of all four
  endpoints, the served OpenAPI spec, AWS resource state, and a manifest. The
  load-bearing item is `GET /version` returning `git_sha 376b7e18…`, byte-identical to
  the `commit_sha` pinned in `app-contract/release-contract.json` — proving the running
  service *was* the claimed commit, which a screenshot cannot establish.
- **`40a10ab`** — `docs/dispatch/P10-lambda-migration-handoff.md`, the Codex dispatch
  for moving the app to Lambda (see §5).

### `nathanielecon/aws-landing-zone-lab` (Project A) — branch `claude/duplicate-trail-cost-finding-2026-08-08`

- **`1459ac3`** — ledger entry for the duplicate CloudTrail finding, in the repo's own
  Break/Fix bullet style.

---

## 4. Open work, in priority order

### 4.1 Execute the teardown — ~$36/month

`scripts/teardown/aws-cost-teardown.sh` (dry-run by default; `--apply` to execute).

**Do not use `terraform destroy` for this.** Neither stack's state is reachable from a
clone — Project C's `.gitignore` excludes `infra/terraform/*.tfstate`, and
`platform/sandbox/aws-proof` has no backend block. A destroy from a checkout finds
empty state, destroys nothing, and **exits 0**. If the original `.tfstate` still exists
on the machine that applied these, prefer `terraform destroy` there.

Order (encoded in the script): drain service → delete service → delete ALB → **wait for
deletion** → delete target groups → delete cluster → stop and delete
`project-a-sandbox-trail` → delete ALB security group.

Safety properties, all test-covered in `tests/terraform/teardown-script.test.mjs`:
aborts if `project-a-lzlab-trail` is absent; resolves target groups by name prefix, not
LB association (which vanishes with the load balancer); never invokes
`schedule-key-deletion`, `delete-bucket`, `delete-repository` or `delete-vpc`.

**Which trail, and why** — evidence-based, not preference. Both trails come from the
same `platform/terraform/audit` module instantiated twice with different `name_prefix`.
`aws-proof/EVIDENCE.md` documents everything that root proves, including KMS key
`cd27223d-5d4a-432e-8f71-7eb2b3462781` (verified still matching live), and Project A's
`evidence/README.md` designates `landing-zone-lab` as the live lab. So the sandbox root
is the superseded one and its claim is already captured.

**Verify 2–3 days after** (Cost Explorer lags ~1 day): ELB and ECS at exactly `$0.00`,
VPC down ~$0.36/day, CloudTrail roughly halved. Reduced-but-nonzero means something
survived.

### 4.2 Commit the screenshots — do before teardown

The owner captured `/docs` (with address bar, `Not secure`, `/version` expanded) and
`/version`. They exist only in a chat transcript, which is not an artifact store.

→ `nathanielecon/local-first-governed-cicd`, branch
`claude/pre-teardown-evidence-2026-08-08`, as
`evidence/phase-9/20260808T191039Z-screenshot-docs.png` and
`…-screenshot-version.png`, then append both to the manifest's `evidence` array.

**The ALB hostname is released with the load balancer and cannot be recreated.**

### 4.3 Wire the anomaly subscription

Currently reports `NOT WIRED` rather than implying coverage that doesn't exist.

AWS permits exactly **one** dimensional (SERVICE) anomaly monitor per account and this
one already has one — the create failed with `ValidationException: Limit exceeded`, not
AccessDenied. So detection is already active account-wide; only alert routing is
missing.

```
aws ce get-anomaly-monitors --query 'AnomalyMonitors[].[MonitorArn,MonitorDimension]'
```
then apply `terraform/envs/account` with `TF_VAR_existing_anomaly_monitor_arn=<arn>`.
`ce:GetAnomalyMonitors` is in the addon, so the deploy role can read it.

### 4.4 Delete the root access keys

The AWS connector authenticated as `arn:aws:iam::000000000000:root`. `continuityops-agent-ro`
exists to replace it, but **the scoped user is not a control while root keys still
exist**. Console → account menu → Security credentials → delete; confirm MFA on root
while there.

Root credentials were found in **three independent places**: this connector, Project A's
`aws-proof/EVIDENCE.md` ("IAM root session via `aws login`"), and Project C's
`governing-manifest.json`. That is a habit, not an incident.

### 4.5 Refund case — ~$309

Free on Basic Support: Console → Support → Create case → **Account and Billing** →
Billing → Payment/Dispute. Only the *API* needs Business/Enterprise.

Amount: EKS control plane $295.02 (491.7 h × $0.60) + node $10.23 + public IP $2.46 +
EBS $1.06. **Exclude** the ALB, ECS, CloudTrail and KMS charges — they belong to
different projects and asking for them weakens the request.

Sequence: teardown → **update the expired payment method** → then file. Arrears weaken a
goodwill request, and unpaid balances escalate to suspension.

Draft text and the evidence timeline were provided as files in-session.

---

## 5. Deferred by decision

- **`enable_eks` / `enable_serverless`** still hardcoded `true` in
  `terraform/envs/staging/main.tf` — a dispatched apply rebuilds the full stack.
- **One role still holds plan + apply + destroy.** Splitting `continuityops-gha` needs
  new OIDC trust conditions, and a wrong trust policy locks CI out of the account.
  Reserved for the owner per `AGENTS.md` "Immediate human gates".
- **`docs/claims/matrix.json`** still carries `finops-teardown` at **L4** against
  dry-run-only evidence. Claim levels deliberately untouched — elevation requires fresh
  run URLs bound into evidence, which is its own exercise.
- **P10 Lambda migration** — `docs/dispatch/P10-lambda-migration-handoff.md` in Project
  C. Moves the app to a Lambda Function URL: permanent hostname, ≈$0 (the 1M request /
  400,000 GB-second free tier is perpetual), versus $25/month to keep the ALB alive.
  ~1.5–2.5 hours. The `Dockerfile` already runs uvicorn on port 8080, the Lambda Web
  Adapter's default, so it is one `COPY` line and **no application code change**.
  Owner decision at dispatch: Function URL (default) or API Gateway, if a custom domain
  is plausibly wanted later.

---

## 6. Environment constraints hit repeatedly

Relevant because they shaped what could be done, and will shape the next session.

- **AWS connector was unavailable for most of the session** — `enabledInChat: false`
  most of the time, and when it did return late on it came back **documentation-only**
  (`call_aws` and `run_script` absent). All AWS *writes* went through GitHub Actions
  OIDC instead, which worked reliably throughout.
- **`workflow_dispatch` requires the workflow on the default branch.** `cost-inventory.yml`
  returns 404 until merged. Dispatching an *existing* workflow with `ref=<branch>` does
  work — that is how `envs/account` was applied from the feature branch.
- **The `plan` job cannot assume the OIDC role** (no `environment: continuityops`).
  Correct by design: it also runs on pull requests, and `AGENTS.md` forbids giving PR
  jobs cloud credentials. The credentialed plan happens inside the apply job's no-op
  guard.
- **No browser-control tooling**, and `cdn.jsdelivr.net` / `unpkg.com` return `000`, so
  `/docs` cannot render headlessly and `/version` (JSON) downloads rather than renders.
  Headless captures also carry no address bar. Hence 4.2 is owner-only.
- **`registry.terraform.io` is blocked**, so `terraform validate` never ran locally.
  `terraform fmt -check` passed on the pinned 1.5.7; CI now validates every env root.

---

## 7. Found while working, not asked for

- **`README.md` and `SOURCE_ANALYSIS.md` linked to repositories that do not exist** —
  `nathanielecon/cloud` and `nathanielecon/project-c-cloud`. Real names are
  `aws-landing-zone-lab` and `local-first-governed-cicd`. Every upstream link was a 404
  on a portfolio front page. Fixed in `5bb4ffe`.
- **`tests/index.mjs` is a hand-maintained manifest** and `node --test tests/` runs
  *that*. A new test file not registered there **silently never executes** — proven with
  a throwaway probe. Any future test file has the same trap.
- **The test suite mutates tracked evidence.** Running it rewrites
  `evidence/slices/S2/runtime/kind-preflight.json`, stripping tip-bind fields and
  downgrading `claim_level` L4 → L1. Reverted rather than committed, every time. Anyone
  running tests then `git add -A` silently regresses the claims matrix. **Unfixed** —
  worth pointing `kind-preflight.mjs` at a gitignored path.
- **`teardown.yml` already runs `terraform state list`** and nobody preserves the
  output. Uploading it as an artifact would make every future teardown self-evidencing
  rather than depending on someone remembering.

---

## 8. The portfolio angle

This incident is a better story than the project it happened to. A CI misconfiguration
silently re-provisioned a cluster after a successful teardown, triggered by a
whitespace-only commit; it ran 491.7 hours undetected; the unit cost was 6× the
documented model because a pinned Kubernetes version had quietly entered extended
support; it was diagnosed from billing data — two independent service lines agreeing on
the same uptime window to within an hour — remediated at the root cause, and the
guardrails that replaced it were themselves found broken in a silent direction and
fixed.

Interviewers cannot easily distinguish a polished lab from a real system. They can
always tell whether someone has debugged a live cost incident. It is already in the
ledger as BF-2026-029 … BF-2026-033.
