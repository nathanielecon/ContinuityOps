# ContinuityOps Break/Fix Log

This log is append-only and orchestrator-owned. Record the break before the next
judge round. Preserve failed evidence and link the superseding verification.

## Prevention rules inherited from Projects A and C

These are plan-time controls derived from observed failures. They are not
ContinuityOps incidents yet.

### BF-PRE-001 — Claims tense must follow evidence state

- Observed risk: documents can say “cloud-validated” before apply, or retain
  “pending apply” after successful evidence.
- Control: component-level claim matrix; automated tense/status consistency;
  evidence/claims review after every live operation or repair.

### BF-PRE-002 — Do not chase the wrong credential control plane

- Observed risk: a Cloud Agent session may not receive newly configured role
  credentials, causing repeated `NoCredentials` attempts.
- Control: prefer GitHub OIDC CI for hosted cloud changes; fail fast on missing
  identity; dispatch a bottleneck diagnostic early; never fall back to long-lived
  keys.

### BF-PRE-003 — Authorization changes and boundary tests are one contract

- Observed risk: the plan authorizes Phase N while harness tests still expect
  Phase N to be rejected.
- Control: every authorization update must atomically trigger a narrow test that
  accepts N and rejects N+1, followed by the full harness.

### BF-PRE-004 — Evidence must postdate remediation

- Observed risk: retained test evidence can show a pre-fix failure while status
  claims a post-fix pass.
- Control: every fix invalidates candidate-bound evidence; rerun all approved
  checks; add superseding events; evidence reviewer confirms freshness.

### BF-PRE-005 — Hosted runner parity must be explicit

- Observed risk: local validation succeeds because a tool exists locally while
  the hosted runner lacks it, or hosted environment variables trigger false
  credential findings.
- Control: pinned tool bootstrap; hermetic fixtures; record runner environment;
  allowlist only benign runner variables with regression tests; reproduce the
  exact merge SHA where possible.

### BF-PRE-006 — Pin unstable scanning paths

- Observed risk: installer instability creates long CI repair cycles unrelated
  to product defects.
- Control: use maintained pinned container/checksum paths for scanners; separate
  scanner-infrastructure failure from a vulnerability finding.

### BF-PRE-007 — Safe failure proof belongs in an isolated lane

- Observed risk: teams either lack blocked-change evidence or create an unsafe
  production-impacting demonstration.
- Control: use harmless lint/policy fixtures or isolated draft PRs; never mix a
  deliberate failure with deployment credentials.

### BF-PRE-008 — Completion reconciliation catches late artifacts

- Observed risk: forbidden worktrees/isolation directories or files can appear
  after the main validator scan.
- Control: adapter compares pre/post tree after worker exit and before commit.

### BF-PRE-009 — Frozen rubrics must exist before implementation

- Observed risk: reconstructing rubrics mid-stream weakens confidence and allows
  acceptance criteria to drift toward the candidate.
- Control: Phase 0 freezes and hashes every rubric before Phase 1 authorization.

### BF-PRE-010 — Bottleneck mode does not replace full councils

- Observed risk: repeated single-judge repairs can be mistaken for full slice
  certification.
- Control: bottleneck clearance always returns to a fresh three-judge slice
  round and final clean-room council.

### BF-PRE-011 — Parallel streams must not overlap

- Risk: several Ralphy streams can create merge races, schema drift, or evidence
  collisions.
- Control: partition ownership and interface hashes before dispatch; sequential
  work within streams; isolated evidence namespaces; integration queue owns
  merge; shared-interface change freezes dependents.

### BF-PRE-012 — Saved councils can anchor

- Risk: retained judges/nixers/fixers may converge on their own assumptions and
  miss a new defect.
- Control: saved cohort can award only provisional pass; three fresh judges are
  authoritative; a fresh failure retires the repair cohort and triggers fresh
  nixers/fixers plus another fresh council.

### BF-PRE-013 — Proxy benefit is unverified

- Risk: a context-rendering proxy may introduce latency, fidelity loss,
  credential/log exposure, or policy conflict despite reducing input tokens.
- Control: pin `pxpipe-proxy@0.9.0`, verify provenance/policy, sanitize logs,
  test direct fallback, measure outcomes, and never promise 2–3× quota.

### BF-PRE-014 — Recruiter visual must follow evidence

- Risk: Image2 may beautify the diagram by adding nonexistent services, arrows,
  metrics, or production claims.
- Control: exact draw.io source, evidence-locked prompt, visual parity review,
  required honest footer, and regeneration after architecture/evidence drift.

## Entry template

```markdown
## YYYY-MM-DD — CO-XXX — Short title

- **Slice/task:**
- **Baseline SHA:**
- **Candidate SHA at break:**
- **Environment/identity:**
- **Symptom:**
- **Exact failed check and exit:**
- **Raw failure evidence:**
- **Attempts:**
- **Root cause:**
- **Why earlier gates missed it:**
- **Blast radius:**
- **Decision:**
- **Fix and files changed:**
- **Regression control added:**
- **New candidate SHA:**
- **Fresh verification commands/results:**
- **Hosted/cloud verification:**
- **Superseded evidence:**
- **New evidence:**
- **Claim/status changes:**
- **Judge round impact:**
- **Remaining risk/follow-up:**
- **Verified by:**
```

## Log

## 2026-07-15 — CO-005 — CODEX_AUTH_JSON_GZB64 injected but unusable

- **Slice/task:** preflight before P0-T01 (no P0 dispatch)
- **Baseline SHA:** `39eaf03f749ec828c39d2e3da75efaf3392be2e8`
- **Candidate SHA at break:** n/a (no implementation candidate)
- **Environment/identity:** Cursor Cloud Agent `bc-1f545fcc-c315-41f3-bafb-2c151b1991ad` (“P0 start conditions”); model `cursor-grok-4.5-high-fast`; GitHub App installation scoped to `nathanielecon/ContinuityOps` only
- **Symptom:** `CODEX_AUTH_JSON_GZB64` is set (len=37, path-like `/tmp/...`) but the referenced path does not exist; no `~/.codex/auth.json`; no usable Codex auth material
- **Exact failed check and exit:** path resolve / auth decode → fail (missing file; cannot gunzip+JSON-parse auth)
- **Raw failure evidence:** env present=`true`; path_resolves=`false`; installation cannot stage Codex CLI auth
- **Attempts:** inspect env, `/proc/self/environ`, path existence, `/tmp` CODEX* glob, `~/.codex`
- **Root cause:** secret name injected without a resolvable payload/file in this run’s filesystem
- **Why earlier gates missed it:** first live Cloud Agent preflight for Codex worker auth
- **Blast radius:** blocks all Codex `/fast` implementation workers; P0 must not start
- **Decision:** stop; escalate to human; do not dispatch P0
- **Fix and files changed:** none (human credential injection required)
- **Regression control added:** OPERATING_STATE `preflight.codex_auth_json_gzb64` + issue CO-005
- **New candidate SHA:** n/a
- **Fresh verification commands/results:** recheck after human injects usable auth
- **Hosted/cloud verification:** n/a
- **Superseded evidence:** n/a
- **New evidence:** this log entry; OPERATING_STATE revision 3
- **Claim/status changes:** `current_gate=preflight-codex-auth-and-ac-visibility`; all P0 tasks blocked
- **Judge round impact:** none (pre-implementation)
- **Remaining risk/follow-up:** human must inject real gzip+base64 auth JSON or create the referenced file before recheck
- **Verified by:** orchestrator preflight (failed closed)

## 2026-07-15 — CO-006 — Project A/C repos not visible to Cloud Agent installation

- **Slice/task:** preflight before P0-T01 (no P0 dispatch)
- **Baseline SHA:** `39eaf03f749ec828c39d2e3da75efaf3392be2e8`
- **Candidate SHA at break:** n/a
- **Environment/identity:** same Cloud Agent run; `GET /installation/repositories` → only `nathanielecon/ContinuityOps`
- **Symptom:** pinned A/C repos and legacy names all 404 / “Repository not found” for API and `git ls-remote`; pin commits unreachable
- **Exact failed check and exit:** `gh api repos/<A|C>` → HTTP 404; `git ls-remote` → fatal repository not found
- **Raw failure evidence:** checked `nathanielecon/aws-landing-zone-lab`, `nathanielecon/local-first-governed-cicd`, `nathanielecon/cloud`, `nathanielecon/project-c-cloud`; `visible_repos=[]`; `pin_commits_reachable=false`
- **Attempts:** REST metadata, commit fetch for lock pins, ls-remote, installation repo list, repo search
- **Root cause:** GitHub App/installation lacks access to private Project A/C repositories (or repos are absent under those names for this principal)
- **Why earlier gates missed it:** lockfile pins were updated in `39eaf03` without a Cloud Agent visibility recheck in this environment
- **Blast radius:** P0-T01 upstream pin/inventory and all A/C consumption tasks blocked
- **Decision:** stop; escalate to human; do not dispatch P0
- **Fix and files changed:** none (human must grant installation read access or correct pin identity)
- **Regression control added:** OPERATING_STATE `preflight.project_ac_visibility` + issue CO-006
- **New candidate SHA:** n/a
- **Fresh verification commands/results:** after access grant, `gh api repos/<pin>` and commit fetch must succeed
- **Hosted/cloud verification:** n/a
- **Superseded evidence:** n/a
- **New evidence:** this log entry; OPERATING_STATE revision 3
- **Claim/status changes:** P0 dispatch remains forbidden until A/C visibility passes
- **Judge round impact:** none
- **Remaining risk/follow-up:** README/MASTER_PLAN still cite legacy `cloud` / `project-c-cloud` names while lockfile uses renamed paths — human should confirm canonical identity when granting access
- **Verified by:** orchestrator preflight (failed closed)

## 2026-07-16 — CO-006 — A/C visibility recheck still fail (no secret rotate from agent)

- **Slice/task:** preflight recheck on human claim that A/C permission was granted
- **Baseline SHA:** `39eaf03f749ec828c39d2e3da75efaf3392be2e8`
- **Candidate SHA at break:** n/a
- **Environment/identity:** same Cloud Agent; `ghs_` installation token; `repository_selection=selected`; repos=`ContinuityOps` only
- **Symptom:** `nathanielecon/aws-landing-zone-lab` and `nathanielecon/local-first-governed-cicd` still HTTP 404 / git not found
- **Exact failed check and exit:** `gh api repos/<A|C>` → 404; `/installation/repositories` total_count=1
- **Raw failure evidence:** OPERATING_STATE `preflight.checked_at=2026-07-16T00:16:52Z`
- **Attempts:** API, ls-remote, installation list; no Cursor secret-admin API; `gh secret list` 403/404
- **Root cause:** access is installation-scoped, not fixed by ContinuityOps Actions secrets; agent cannot delete/create Cursor dashboard secrets or add repos to the GitHub App install
- **Decision:** escalate to human immediately; do not invent or mint credentials
- **Remaining risk/follow-up:** human must add A+C to the Cursor GitHub App installation (or provide a permitted PAT secret and a new agent run that injects it); separately replace broken `CODEX_AUTH_JSON_GZB64`
- **Verified by:** orchestrator recheck (failed closed)
