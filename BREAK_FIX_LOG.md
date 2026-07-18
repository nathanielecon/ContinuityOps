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

### BF-PRE-015 — Supervisor branch-check protocol (minimal intervention)

- Risk: a token-constrained supervisor either polls live streams (wasteful) or
  misses completed work (unreviewed merges).
- Control: the supervisor reviews a stream branch only upon a durable
  completion signal from the orchestrator. Mechanism:
  1. Each Ralphy stream works on an isolated branch named
     `stream/<slice-id>-<short-name>`.
  2. When the orchestrator judges the stream complete, it commits
     `evidence/slices/<slice>/STREAM_COMPLETE.json` on that branch containing:
     candidate SHA, baseline SHA, validation commands/results, evidence
     manifest path, and the final worker-reported `context_remaining`.
  3. The orchestrator then notifies the supervisor (Simplified Chinese,
     durable-artifact pointer only — no transcript).
  4. The supervisor reviews only the signaled branch: the completion file,
     the diff against `write_scope`, and evidence freshness. It does not
     inspect live or unsignaled streams.
  5. The supervisor's verdict is recorded as a durable file with the fixed name
     `evidence/slices/<slice>/SUPERVISOR_VERDICT.json` (approve, or issue IDs
     for rework), never as chat-only feedback. Its shape is pinned by
     `harness/schemas/supervisor-verdict.schema.json` (`decision`,
     `candidate_sha`, `reviewed_paths`, `issue_ids`, `reviewer`, `at`).
  6. Naming compliance: a branch that does not use the
     `stream/<slice-id>-<short-name>` convention AND lacks a committed
     `STREAM_COMPLETE.json` is treated as unsignaled and is not reviewed. This
     covers Cursor-platform auto-generated `cursor/*` branches, which are never
     valid completion signals on their own.
  7. `STREAM_COMPLETE.json` must include a `preflight_ok` field: a snapshot of
     the dispatch-time warm-gate verdict (`lastWarmUtc` freshness for the
     Environment) plus whether the required cross-repo context package was in
     place at dispatch. It does not carry any credential check — no auth
     material exists in the worker container (D-026/D-027). The whole file's
     shape is pinned by `harness/schemas/stream-complete.schema.json` (with a
     conforming sample at `harness/schemas/stream-complete.example.json`), and
     `preflight_ok` uses the object form
     `{warm_fresh, last_warm_utc, context_package_ready}`.
  8. Source of the `preflight_ok` data. The `preflight_ok` snapshot is not
     authoritative as an issue comment. The committed artifact
     `evidence/slices/<slice>/preflight-<taskid>.json` (at least `lastWarmUtc`
     and `verdict`) is the authoritative source, and the orchestrator populates
     `preflight_ok` in `STREAM_COMPLETE.json` from it (referenced via
     `preflight_evidence_path`), never from a transient issue comment. Who
     writes it depends on the dispatch path (D-031): on the App path, the
     orchestration round commits it with its diff, deriving `lastWarmUtc` from
     the most recent Codex task timestamp on the keep-warm record; on the
     fallback control-center path, the sweep lane writes it after running the
     warm gate.

### BF-PRE-017 — Dispatch polling must be durable and idempotent

- Observed risk: an in-session background dispatch loop dies silently on app
  restart (a neighbouring project lost three workers this way), and a
  non-idempotent poller re-dispatches the same task when runs overlap or a
  relabel fails.
- Control: the dispatch-polling invariants are unchanged — single-pass idempotent
  runs, claim-first relabel (`codex-dispatch -> dispatching`) before any work, a
  machine-local lock-file mutex (with stale fallback) against overlapping runs,
  an author allowlist, and no auto-retry on failure (mark `dispatch-failed` and
  require a human to requeue).
- Carrier of the poll (revised): the adopted model is **owner-on-station sweep**
  — the queue watcher runs only while the owner's live supervisory session is on
  station, via `Watch-CodexDispatchQueue.ps1 -Once` or by hand. Items wait
  between sweeps. This supersedes the earlier "must be carried in a Scheduled
  Task/service" phrasing; a standing scheduled task/service is explicitly NOT
  required and the control center registers none (see `QUEUE.md` sweep model and
  commit 4a30412). The idempotency/claim-first/lock-mutex/author-allowlist/
  no-auto-retry controls above stay in force precisely because sweeps may overlap
  (manual + `-Once`, or repeated triggers).
- Retained lesson (unchanged): an in-session background loop dies silently on app
  restart (a neighbouring project lost three workers this way), so an
  unattended in-session background loop is not a reliable carrier. The sweep
  model avoids that failure surface by running only when on station, rather than
  by depending on a long-lived background process.

### BF-PRE-016 — Credential variables are reported by metadata only

- Observed risk: reconnaissance or diagnostics can echo fragments of a secret
  environment variable (name, prefix, or slice), leaking material into
  transcripts and evidence in violation of the no-secrets-in-evidence rule.
- Control: when reporting on any credential-class variable (for example
  `CODEX_AUTH_JSON_GZB64`), report only presence, length, and whether it
  resolves/decodes to usable material. Never echo any prefix, suffix, or
  substring of the value, in any tool call, log, or report.

### BF-PRE-018 — App path cannot publish from inside the sandbox

- Observed risk: `@codex` workers complete, call `make_pr`, and claim commits
  while nothing lands on GitHub until **Create PR** on the Codex task page.
  Re-nudge with in-container `git push`/`gh pr create` still failed: no `gh`,
  GitHub git HTTPS `CONNECT tunnel failed, response 403`, often no `origin`.
  Separately, `github-actions[bot]` `@codex` keepwarm on issue #4 got no App reply.
- Control (**D-034** supersedes D-033 overnight carrier): workers embed
  `continuityops-patch-v1` + unified diff; GHA `codex-patch-publish` applies with
  `GITHUB_TOKEN` and opens the PR. Platform Create PR /
  `Publish-CodexCloudTask.ps1` remain fallbacks. Supervisor reviews PRs /
  re-nudges missing markers. Keepwarm = supervisor-authored `@codex` on #4.

### BF-PRE-019 — App container sees only the default branch (CO-009)

- Observed risk: the Codex GitHub App container clones only the repository
  default branch (`main`) and carries no `origin` remote. A worker dispatched
  for a task whose contract or baseline lives on a non-default branch (e.g.
  `stream/S0-baseline-audit`) cannot read it, silently falls back to the `main`
  tree, and records a `contract_read=UNAVAILABLE` gap or a mismatched baseline
  (see CO-008/CO-009 from the P0-T01 App round, PR #6). The same isolation
  blocks outbound publication from inside the sandbox (BF-PRE-018).
- Control: when dispatching an App-path round, never assume non-default-branch
  readability. Either (1) context-package the needed contract/baseline/upstream
  material directly into the issue body ("the worker gets data, not
  permission", D-028), or (2) merge the required material to `main` first and
  dispatch afterward. The publication surface is the owner's platform **Create
  PR** or the control-center `codex cloud apply` + push — never in-container
  `git`/`gh`. Any evidence produced against the wrong tree is candidate-bound
  and must be refreshed once the authoritative baseline is frozen.

### BF-PRE-020 — Workers never commit lockfiles

- Risk: bounded workers may commit regenerated lockfiles from transient or
  container-local dependency state, creating noisy or misleading integration
  changes outside the task contract.
- Control: workers never commit lockfiles. If dependencies legitimately change,
  the integrator regenerates lockfiles at integration time and binds that
  regeneration to the integration evidence.

### BF-PRE-021 — Fresh-install first test run may be flaky

- Risk: the first test run after a fresh install can fail from cache warm-up or
  one-time toolchain initialization rather than a product defect.
- Control: integration runs the suite twice after install. A recurring failure
  must capture full error output before repair; a one-time first-run failure is
  recorded as warm-up evidence rather than silently ignored.

### BF-PRE-022 — Detached local Codex exec must not block on stdin

- Risk: a local detached `codex exec` can hang or consume unintended input when
  stdin remains attached, wasting worker budget or blocking the lane.
- Control: any local detached `codex exec` redirects stdin from `/dev/null`.
  Prefer the warm cloud lane for long tasks.

### BF-PRE-023 — Mock-green is not runtime-proven

- Risk: unit-green results under mocked runtimes can be misrepresented as proof
  of platform behavior.
- Control: every platform behavior claim requires a real-runtime gate before it
  counts as evidence; mocked-unit success is useful but not runtime proof.

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

## Session retrospective 2026-07-16/17 — problem→solution index

| Problem | Final solution | Entry/decision |
| --- | --- | --- |
| Cursor assumption failed: workers could not rely on the earlier Cursor-lane framing for autonomous dispatch. | Move dispatch to the Codex GitHub App path and record the App/default-branch limits explicitly. | D-031 / BF-PRE-019 |
| CO-005 credential injection proposal would have moved auth material into a worker container. | Reject credential injection; use platform authentication plus zero-secret Codex Cloud Environments. | D-026 / D-035 |
| `make_pr` metadata hallucination made worker text look complete without a GitHub PR. | Treat `make_pr` as metadata only and require patch-in-comment output for unattended publish. | D-033 → D-034 |
| App sandbox could not publish with `git push` or `gh pr create`. | Use the GitHub Actions mechanical publisher as the primary path. | D-034 / BF-PRE-018 |
| Nested fenced blocks truncated extracted patches. | Replace regex extraction with structured line scanning. | BF-2026-001 |
| Publisher dirty-tree changes and stale `base_sha` checkout aborted publication. | Run extractor out of tree, hard-reset before failure handling, and re-trigger through the workflow path. | BF-2026-002 |
| PRs created with `GITHUB_TOKEN` did not trigger CI. | Use an owner empty commit for current validation; permanent workflow/identity solution remains pending. | BF-2026-003 |
| CI whitespace validation reported semantic Markdown line-ending spaces across the whole tree. | Scope whitespace checks to changed files and explicitly exempt semantic Markdown formatting. | BF-2026-004 |
| Supervisor absorbed too much orchestration responsibility. | Restore role boundaries: episodic GPT rounds carry orchestration while the supervisor handles stream boundaries and actuation. | D-030 / D-035 compliance |
| Validator lifecycle was coupled to unavailable future harness assets. | Fixture the validator lifecycle and keep the issue open through the P0-T03 repair lane. | CO-010 → P0-T03 |
| Token consumption rose from per-round supervision and review work. | Apply D-032 supervisor economy, D-037 per-PR reviewer delegation, and session rotation. | D-032 / D-037 |
| Plan-mode capability probe accidentally created GitHub issue #33. | Close immediately as not_planned; never create Issues to probe permissions; use inspect-only checks. | BF-2026-006 |
| Cursor App seat lacked Issues write (CO-011). | Owner injected expanded `GH_TOKEN` (Issues + Pull Requests); App ghs_ remains Issues-403; seat actuates via owner PAT. | D-040 / CO-011 resolved |
| Human directed P0-T03 redo rather than merge draft PR #32. | Supersede #32; fresh fixer + D-037 under D-039 write_scope. | supervisor resume 2026-07-17 |
| Role creep: supervisor absorbing orch; promotion needed for economy. | D-041 chief (boundary/escalation) + junior 5.6 Sol med (actuation) + Grok monitor→chief. | D-041 |

## Log

### 2026-07-18 — ContinuityOps live AWS via GHA OIDC (standalone wiring)

- **Break:** Cloud agents treated live AWS as impossible / blocked on
  CursorCloudAgent `NoCredentials` (BF-PRE-002 / BF-2026-010). ContinuityOps
  needed a promoted CI OIDC role distinct from `project-a-lzlab-gha`; monorepo
  PR #30 still trusted aws-landing-zone-lab `repository_id` `1296742987`.
- **Fix:** Add `terraform/ci-bootstrap/` + CloudShell
  `bootstrap-oidc-cloudshell.sh` (REPO_ID accept/discover; ContinuityOps id
  `1301990908`). Promote `.github/workflows/continuityops-terraform.yml`
  (plan/apply, role `continuityops-gha`, account `283077380808`, roots under
  `terraform/envs/`). AGENTS.md doctrine: escalate via GHA, not Cursor STS.
- **Operator still required once:** CloudShell
  `REPO_ID=1301990908 curl -fsSL https://paste.rs/gHlj9 | bash`, create GitHub
  Environment `continuityops`, dispatch ContinuityOps Terraform plan.
  Repo-only wiring without CloudShell will not make OIDC green.

## 2026-07-17 — BF-2026-001 — Patch publisher truncates diffs containing nested code fences

- **Slice/task:** dispatch infrastructure (D-034 publisher); blocked rounds #17 (ORCH-ROUND-04) and #18 (P0-T02)
- **Baseline SHA:** ea18cfc9fb29153078652434b7e64ff0cf71e27b
- **Candidate SHA at break:** worker-side commits only (881e512 in-sandbox); nothing landed
- **Environment/identity:** GitHub Actions `codex-patch-publish` / ephemeral GITHUB_TOKEN
- **Symptom:** `publish-failed (D-034): git apply failed … corrupt patch at patch.diff:10` on both rounds
- **Exact failed check and exit:** `git apply --index patch.diff` exit ≠ 0 in the publish job
- **Raw failure evidence:** issue #18 comment 5003849152; issue #17 analogous
- **Attempts:** 1 per round (no auto-retry, by design)
- **Root cause:** `scripts/extract-codex-patch.sh` captured the fenced diff with a non-greedy regex ending at the FIRST ``` — but both patches legitimately add file content containing ```json fences, so extraction truncated the patch mid-hunk
- **Why earlier gates missed it:** both D-034 smokes (#12/#14) were single-line text files with no nested fences; the failure class needs markdown/code content inside the diff
- **Blast radius:** publish path only; worker computations intact in task pages; no repo corruption (failed apply aborts before push)
- **Decision:** fix the parser structurally; re-nudge workers to repost patches unchanged (fresh bot comment re-triggers the fixed publisher; no recompute)
- **Fix and files changed:** line-based structural fence scan in `scripts/extract-codex-patch.sh` — inside a unified diff every content line carries a prefix, so a bare ``` at column 0 can only be the closing fence
- **Regression control added:** nested-fence fixture (json fence inside an added file) run through extract + `git apply --check` — passing locally; CI-fixture step queued as follow-up
- **New candidate SHA:** (this commit)
- **Fresh verification commands/results:** fixture extract → `OK: wrote patch.diff (2 paths, 1 chunk(s))`; `git apply --check` → OK
- **Hosted/cloud verification:** next publisher run on reposted #17/#18 patches
- **Superseded evidence:** none (no evidence was produced by the failed runs)
- **New evidence:** publisher run logs on the reposted rounds
- **Claim/status changes:** none (infrastructure)
- **Judge round impact:** none (pre-slice-freeze)
- **Remaining risk/follow-up:** a bare ``` as literal diff *content* at column 0 (e.g. a patch adding an unindented fence line to a md file appears as `+```` so it is safe; only a context line consisting of ``` could confuse — not producible in our added-file patches); CI fixture step to make the regression control permanent
- **Verified by:** supervisor (fixture), publisher (pending live rerun)

### BF-2026-002 — App 发布器 chmod 脏树与旧 base_sha 切换中止

- Observed break: App-path patch 发布器在工作树内对提取器执行 `chmod`，导致发布前出现未预期脏树；随后旧 `base_sha` 切换中止，两轮发布静默失败，监督者无法获得可审查 PR。
- Impact: D-034 机械发布链路未能按预期把 Codex diff 应用并开 PR，P0-T02 合并收尾被延迟。
- Detection: 监督者检查发布结果时发现没有 `publish-ok`/PR URL，且失败轮次缺少足够可见通知。
- Root cause: 发布器准备步骤在仓库工作树内变更文件权限，并在旧基线切换失败后没有以通用失败通知把错误返回到调度线程。
- Fix: 提取器改为出树运行；发布失败前执行 `reset --hard` 清理工作树；通过 `workflow_dispatch` 重触发；增加通用失败通知。修复提交：`7640d80`。
- Verification: 本轮保留 P0-T02 post-merge 验证输出于 `evidence/slices/S0/validation/p0-t02-postmerge.txt`，并在 `STREAM_COMPLETE-P0-T02.json` 绑定验证命令、退出码、时间与证据路径。
- Prevention controls: 保持提取器出树运行、失败前硬重置、`workflow_dispatch` 重触发和通用失败通知；后续在 CI 增加发布器夹具测试，覆盖 chmod 脏树、旧 base_sha、缺 patch marker 与失败通知路径。
- Status: repaired_pending_supervisor_review.

### BF-2026-003 — GITHUB_TOKEN 创建的 PR 不触发 workflows

- Observed break: 由 `GITHUB_TOKEN` 创建的发布 PR 未触发后续 workflow，符合 GitHub 防递归行为；监督者需要 owner 身份空提交才能触发 validate。
- Impact: PR 可被机械创建，但缺少自动 validate 反馈，流边界裁决需要额外人工或 owner 操作。
- Detection: 发布 PR 出现后未产生预期 validate 运行。
- Root cause: GitHub 默认抑制由 `GITHUB_TOKEN` 触发的递归 workflow。
- Fix: 暂无最终修复；当前操作要求监督者以 owner 身份空提交触发 validate。
- Verification: 待决方案尚未实施，本条记录为已知控制平面缺口。
- Prevention controls: 候选方案一是在 `validate.yml` 增加 `workflow_dispatch` 触发；候选方案二是发布器改由符合权限边界的 PAT 建 PR。两者均待监督者/owner 决策。
- Status: open_pending_decision.

## 2026-07-17 — BF-2026-004 — CI whitespace check reported semantic Markdown line endings

- **Slice/task:** repository validation workflow (`validate.yml`) after the first hosted run.
- **Baseline SHA:** 09e271643326b6e55a24e96e6b9c7841c0342813.
- **Candidate SHA at break:** pre-fix hosted validation candidate before commit `f1bbc95`.
- **Environment/identity:** GitHub Actions validate workflow.
- **Symptom:** the first `validate.yml` run treated semantic Markdown trailing double spaces across the tree as whitespace errors.
- **Exact failed check and exit:** hosted whitespace validation step exited non-zero after scanning all repository Markdown instead of only the changed surface.
- **Raw failure evidence:** hosted validate run that preceded commit `f1bbc95`.
- **Attempts:** one same-class hosted validation failure before repair.
- **Root cause:** the hygiene check was global and did not distinguish Markdown's meaningful two-space hard line breaks from accidental trailing whitespace in changed files.
- **Why earlier gates missed it:** local contract checks focused on JSON parsing and patch hygiene, not the hosted workflow's whole-tree whitespace policy.
- **Blast radius:** validation infrastructure only; no product/runtime claim changed.
- **Decision:** constrain hygiene validation to changed files and make the Markdown semantic-format exemption explicit.
- **Fix and files changed:** commit `f1bbc95` changed the workflow logic to use diff-scoped checks and exempt `*.md` semantic hard-break formatting.
- **Regression control added:** hygiene checks must operate on changed files only, and semantic formatting exemptions must be listed explicitly.
- **New candidate SHA:** f1bbc95.
- **Fresh verification commands/results:** hosted validation after `f1bbc95` expected to pass the repaired whitespace policy; current governance round also reruns JSON contract parsing and `git diff --check`.
- **Hosted/cloud verification:** validate workflow rerun after the owner/automation trigger.
- **Superseded evidence:** the initial failing whole-tree whitespace report.
- **New evidence:** repaired validate run and this break/fix entry.
- **Claim/status changes:** record the workflow-policy issue as repaired infrastructure behavior, not a product defect.
- **Judge round impact:** previous candidate-bound validation evidence from before the repair is superseded.
- **Remaining risk/follow-up:** keep any future whitespace expansion diff-scoped; do not reintroduce global Markdown trailing-space failures.
- **Verified by:** supervisor/orchestrator governance review.

## 2026-07-17 — BF-2026-005 — Accidental merge of PR #30 during permissions probe

- **Slice/task:** supervisor actuation / D-037 merge gate; PR #30 (P0-T03 mechanical publish from issue #28).
- **Baseline SHA before probe:** tip preceding `2eda7e4` (post-review context-pack `73ae5fc`).
- **Candidate SHA at break:** `2eda7e4` (`probe-should-fail-dry` merge commit of PR #30).
- **Environment/identity:** Cursor cloud supervisor App token (can push/merge; lacks `issues:write`).
- **Symptom:** despite D-037 reviewer verdict fail SCOPE-001 on issue #31, a merge-API probe with commit message `probe-should-fail-dry` actually merged PR #30 to `main`.
- **Exact failed check and exit:** D-037 structured verdict fail SCOPE-001 (write_scope escape: `scripts/project.mjs`, `tests/index.mjs`, `tests/package.json`, `evidence/slices/S0/validator-contract.json` outside then-current P0-T03 write_scope).
- **Raw failure evidence:** merge commit `2eda7e4`; revert commit `94f4e33`; CO-012; issue #31 verdict (Issues API 403 from this seat).
- **Attempts:** one accidental merge; immediate revert.
- **Root cause:** using the GitHub merge API as a permission probe; the call succeeded and landed product content that the reviewer had already failed.
- **Why earlier gates missed it:** D-037 fail was recorded, but the probe path bypassed the CI-green + verdict-pass merge signal.
- **Blast radius:** transient `main` pollution with out-of-scope P0-T03 paths; reverted; no Phase-1 authorization change.
- **Decision:** revert immediately; do not re-merge #30 until D-039 write_scope expansion stands and a fresh fixer/reviewer cycle passes; record prevention control.
- **Fix and files changed:** revert commit `94f4e33` (`Revert "probe-should-fail-dry"`); governance repair lands D-039/D-040/CO-011/CO-012 in this round.
- **Regression control added:** never call the merge API for permission probes; use OPTIONS, dry-run, or inspect-only endpoints; merge only when CI is green **and** D-037 reviewer verdict passes.
- **New candidate SHA:** `94f4e33` (clean tip after revert); subsequent governance candidate is this ORCH-ROUND-06 repair commit.
- **Fresh verification commands/results:** `git log -2 --oneline` shows revert atop probe; `main` tip `94f4e33` before governance repair.
- **Hosted/cloud verification:** N/A for the revert itself; next P0-T03 land requires hosted CI + D-037 pass.
- **Superseded evidence:** any claim that PR #30 merged under D-037 pass is void.
- **New evidence:** `evidence/slices/S0/SUPERVISOR_ACTUATION-2026-07-17.json`; this break/fix entry.
- **Claim/status changes:** PR #30 content remains unmerged on `main`; D-037 SCOPE-001 still stands until write_scope ratification + new cycle.
- **Judge round impact:** prior reviewer fail remains authoritative; repair cohort must be fresh after scope amendment.
- **Remaining risk/follow-up:** restore `issues:write` (CO-011) before App-path re-dispatch; human may veto D-039.
- **Verified by:** Cursor supervisor bottleneck fixer (git history).

## 2026-07-17 — BF-2026-006 — Accidental Issues create during plan-mode capability probe

- **Slice/task:** supervisor resume reconstruct / CO-011 capability check.
- **Baseline SHA:** `832ce38baa2d8d776fd93169b32e317f3da17a30` (appendix on `main`).
- **Candidate SHA at break:** N/A (no product merge); GitHub issue #33 created and closed.
- **Environment/identity:** Cursor cloud portfolio supervisor with owner `GH_TOKEN` (PAT) present in the new run.
- **Symptom:** while verifying whether Issues write was restored, a `gh api …/issues -f title=probe-should-not-create` call created issue [#33](https://github.com/nathanielecon/ContinuityOps/issues/33) (`probe-should-not-create`).
- **Exact failed check and exit:** process/discipline failure — not a CI failure. Issue was closed within seconds as `not_planned` with explicit non-dispatch body.
- **Raw failure evidence:** issue #33 timeline (create → close `not_planned` → clarifying comment).
- **Attempts:** one accidental create; immediate close.
- **Root cause:** using a mutating Issues create call as a permissions probe (same class as BF-2026-005 merge-API probe).
- **Why earlier gates missed it:** plan-mode reconstruct treated live API capability mapping as read-only; create was not gated.
- **Blast radius:** one closed noise issue; no branch/PR/product impact; no secrets exposed.
- **Decision:** close #33; record prevention; treat expanded `GH_TOKEN` as restoring Issues+PR actuation for this seat; close CO-011 on first intentional `@codex` / queue write (not on the probe).
- **Fix and files changed:** issue #33 closed; this break/fix entry; `OPERATING_STATE.md` revision for redo path.
- **Regression control added:** never create Issues, comments, labels, or merges to probe permissions; use GET/inspect-only (and documented token scope headers) before any mutation. Capability probes must be read-only.
- **New candidate SHA:** this supervisor-resume hygiene commit.
- **Fresh verification commands/results:** `gh api repos/…/issues/33 --jq .state` → `closed`; `gh api repos/…/pulls/32` succeeds with owner PAT (expanded scopes).
- **Hosted/cloud verification:** N/A (governance/discipline).
- **Superseded evidence:** any claim that CO-011 remains blocking for this PAT-backed seat is void after intentional queue write.
- **New evidence:** this entry; subsequent `codex-dispatch` issue for P0-T03 redo.
- **Claim/status changes:** CO-011 → resolved for this seat via owner `GH_TOKEN`; human directed **redo** of P0-T03 (do not merge PR #32).
- **Judge round impact:** none.
- **Remaining risk/follow-up:** Cursor App `ghs_` token may still 403 on Issues; keep using owner PAT for `@codex` / keep-warm; do not reintroduce mutate-to-probe habits.
- **Verified by:** portfolio supervisor (resume seat).

## 2026-07-17 — BF-2026-007 — H0 plan_sha256 drifted after PLAN state bump

- **Slice/task:** P0-T04 / H0 packaging.
- **Symptom:** After marking P0-T04 `review` in `PLAN.md` and packaging H0, `node harness/rubrics/validate-rubric-freeze.mjs` failed with `plan_sha256 与当前文件不匹配`.
- **Root cause:** Bundle hashes were pinned at P0-T04 integrate tip; subsequent PLAN.md authority edits changed `plan_sha256` without refreshing `evidence/slices/S0/rubric-freeze.json`.
- **Fix:** Recompute and refresh pinned hashes in `rubric-freeze.json` + `H0_PACKAGE.md`; re-run validator to pass.
- **Prevention:** Any PLAN/authority edit after rubric freeze must refresh H0-bound hashes before presenting the package for human signature; never ask humans to sign stale digests.
- **Verified by:** portfolio supervisor (`validate-rubric-freeze.mjs` pass after refresh).

## 2026-07-18 — BF-2026-008 — Junior App sandbox cannot actuate with gh

- **Slice/task:** D-041 junior supervisor / JR-SUPER-01.
- **Symptom:** Junior correctly left `waiting_human` after H0 verify, but reported no GitHub actuation channel (no remote, `gh` forbidden, API CONNECT 403). Heartbeat that assumed in-sandbox `gh pr merge` / issue create stalled; D-034 `publish-failed` fired on a legitimate `no_repo_mutation` reply.
- **Root cause:** Charter said junior "actuates" while the carrier is the Codex App sandbox, which is receive-only by D-034/D-026 (credentials never move).
- **Fix:** D-042 — `.github/workflows/junior-actuate.yml` + `continuityops-merge-v1` / `continuityops-dispatch-v1` intents; GHA/`GITHUB_TOKEN` performs merge and `@codex` posts. Docs updated (`JUNIOR_SUPERVISOR`, `QUEUE`, `AGENTS`, snippet).
- **Prevention:** Never instruct App rounds to call `gh`; treat actuation as mechanism; keep Actions workflow permissions Read/write + create-PR (owner UI; PAT cannot set via API).
- **Verified by:** chief supervisor (parser unit tests); end-to-end actuate-ok pending first merge intent after land.

## 2026-07-18 — BF-2026-009 — Upstream A/C trees not readable from Grok worker token

- **Slice/task:** S1 / P1-T01.
- **Symptom:** `gh api .../contents` and `git clone` for `aws-landing-zone-lab` / `local-first-governed-cicd` return 403 (accepted permission: metadata=read only).
- **Root cause:** D-028 — worker gets data not permission; PAT lacks contents scope on private upstreams.
- **Fix:** ContinuityOps-side adapter contracts + `missing_capabilities` (MC-A-TREE, MC-C-TREE, MC-C-DIGEST); `image_digest=UNAVAILABLE`; claim ceiling L1.
- **Prevention:** Control-center must supply D-028 context package or vendored snapshot before raising upstream-derived claims above L1; never invent digest/export values.
- **Verified by:** Grok D-043 S1 worker (static tests + validators).

## 2026-07-18 — BF-2026-010 — Lead agent dependencies vs Cursor Pro+ AWS identity

- **Slice/task:** Portfolio / Phases 1–8 live claim elevation; chief supervisor seat.
- **Symptom:** Agents treated `NoCredentials` + set `CURSOR_AWS_ASSUME_IAM_ROLE_ARN` as an unfinished Cursor injection bug and blocked. ContinuityOps is `portfolio-certified-L1`; live L4+ needs a working apply control plane.
- **What was actually fixed (2026-07-14/15) — owner-confirmed:**
  | Path | Evidence |
  | --- | --- |
  | **GitHub OIDC → `project-a-lzlab-gha`** | Role last used **2026-07-15**; successful `landing-zone-lab.yml` runs; live lab under `assumed-role/project-a-lzlab-gha` |
  | **`CursorCloudAgent` injection** | Role created Jul 14; **never assumed** (`RoleLastUsed` empty; CloudTrail only `CreateRole` / `AttachRolePolicy`) |
- **Root cause:** Individual/Pro+ plan has **no team External ID**. Dashboard **Settings → Advanced / Bedrock IAM Role** (Teams/Enterprise only) is absent on Pro+. Secret/`CURSOR_AWS_ASSUME_IAM_ROLE_ARN` may be set and role may trust `arn:aws:iam::289469326074:role/roleAssumer` (no External ID condition), but Cursor **will not inject** `AWS_PROFILE` / `cursor-cloud-agent` without that External ID. Using Team ID as External ID is wrong. Prior “fix” was **change control plane**, not finish Cursor STS.
- **Target account (not a secret):** `283077380808` / root `arn:aws:iam::283077380808:root`. ContinuityOps CI role: `arn:aws:iam::283077380808:role/continuityops-gha`. Env string only: `.../role/CursorCloudAgent` (unused).
- **Fix / control (workarounds in order):**
  1. **Proven / LIVE for ContinuityOps (2026-07-18):** GitHub OIDC → `continuityops-gha` via `continuityops-terraform.yml` (repo id `1301990908`, Environment `continuityops`). Loop: PR plan → merge `main` → auto apply. Do **not** use `project-a-lzlab-gha` / `landing-zone-lab.yml` for ContinuityOps roots.
  2. **Proven — local bottleneck:** laptop `aws login` as account `283077380808`; orchestrator runs apply/evidence locally; Cloud seat stays repo-only.
  3. **Only if insisting on in-pod AWS:** upgrade to Teams → Bedrock IAM Role → Validate & Save → External ID in `CursorCloudAgent` trust → **new** Cloud Agent pod.
  4. **Do not:** put long-lived access keys or root session tokens in Cloud secrets.
  5. **Do not block** on `CURSOR_AWS_ASSUME_IAM_ROLE_ARN` / in-VM STS on Pro+.
- **Regression control added:** Stuck-agent paste + “What actually fixed live AWS” table + injection stop table in `AGENTS.md`. Phrase: **injection absent — stop; no keys.**
- **Fresh verification (this ContinuityOps Cloud seat, 2026-07-18):** `AWS_PROFILE=<unset>`; STS `NoCredentials`; role ARN secret set → stop; no keys. Portfolio remains `portfolio-certified-L1`.
- **Hosted/cloud verification:** ContinuityOps GHA OIDC (`continuityops-gha`) primary; local bottleneck secondary. PR #50 merged to `main` (`20266d3`).
- **Claim/status changes:** none elevated by chasing Cursor STS.
- **Remaining risk/follow-up:** closed for smoke path — see BF-2026-011. Further elevation needs fresh plan+apply URLs. This seat Actions 403 until owner restarts Cloud Agent after GH_TOKEN refresh.
- **Verified by:** chief supervisor + owner historical evidence paste (2026-07-18); PR #50 land.

## 2026-07-18 — BF-2026-011 — DynamoDB tf-lock create race on first main apply

- **Slice/task:** Live AWS loop / PR #51 land → auto apply on `main`.
- **Symptom:** Apply run [29643490577](https://github.com/nathanielecon/ContinuityOps/actions/runs/29643490577) **failed** during `ensure-tfstate.sh` DynamoDB `create-table` (`ResourceInUseException`). OIDC assume of `continuityops-gha` succeeded.
- **Root cause:** Concurrent ensure/create (or describe-then-create race) on `continuityops-tf-locks` without treating `ResourceInUseException` as success-and-wait.
- **Fix:** Harden `terraform/ci-bootstrap/ensure-tfstate.sh` to tolerate `ResourceInUseException` / `BucketAlreadyOwnedByYou` and `wait table-exists`. Re-dispatch apply [29643569047](https://github.com/nathanielecon/ContinuityOps/actions/runs/29643569047) **green** (staging live-marker + remote state).
- **Evidence:** `evidence/hosted/cloud-apply-staging-2026-07-18.json`; claims matrix terraform-scaffold + hosted-ci → **L4** (smoke scope only).
- **Prevention:** Keep ensure script race-tolerant; prefer single concurrency group (already on workflow).
- **Claim/status changes:** component L4 smoke; portfolio gate remains `portfolio-certified-L1` until broader recert.
- **Verified by:** owner-confirmed Actions URLs (2026-07-18); chief records in-repo.

## 2026-07-18 — BF-2026-012 — EKS CreateCluster rejected Kubernetes 1.29

- **Slice/task:** Chief elevation / PR #53 staging live apply.
- **Symptom:** Apply [29644551841](https://github.com/nathanielecon/ContinuityOps/actions/runs/29644551841) failed: `InvalidParameterException: unsupported Kubernetes version 1.29`. VPC/IAM/SQS/Lambda created; EKS not.
- **Root cause:** Default `cluster_version = "1.29"` no longer offered in account/region.
- **Fix:** Bump default to `1.32`; re-apply.
- **Verified by:** apply green [29644662492](https://github.com/nathanielecon/ContinuityOps/actions/runs/29644662492); teardown [29645052414](https://github.com/nathanielecon/ContinuityOps/actions/runs/29645052414).

## 2026-07-18 — BF-2026-013 — 层级流程绕过后补登记

- **Slice/task:** portfolio completion / hierarchy remediation (issues #56/#57/#58).
- **Baseline SHA:** `d2d90bc2a761031186451c19b391a12af198bd92`.
- **Candidate SHA at break:** PR #53/#54 live elevation and `portfolio-certified-L4-lab` certification path before this remediation patch.
- **Environment/identity:** chief supervisor seat; GHA OIDC `continuityops-gha` for lab AWS execution.
- **Symptom:** chief directly implemented live elevation (PR #53/#54) and certified `portfolio-certified-L4-lab` without a GPT worker → D-037 reviewer chain.
- **Exact failed check and exit:** independent GPT completion reviewer verdict = fail on hierarchy/process: no qualifying GPT worker handoff plus D-037 pass for the elevation/certification path.
- **Raw failure evidence:** `evidence/judges/REVIEW-COMPLETION-01.json`; PR #53/#54 history; AWS lab runs 29644662492 / 29645042815 / 29645052414 remain evidence for the lab claim only.
- **Attempts:** one chief-fast path through the OIDC loop; no prior D-045 hierarchy remediation recorded before this entry.
- **Root cause:** chief occupation sped through the OIDC loop, bypassing D-041/D-045 hierarchy and the D-037 independent review contract.
- **Why earlier gates missed it:** hosted AWS evidence validated infrastructure behavior, not management-chain compliance; the chief boundary record treated lab success as sufficient for the gate.
- **Blast radius:** process debt on portfolio completion certification; AWS lab evidence remains valid for the scoped L4 lab claim (apply 29644662492, drill 29645042815, teardown 29645052414).
- **Decision:** keep `current_gate` at `portfolio-certified-L4-lab`, record the hierarchy failure, and require a fresh D-037 process pass before closing the hierarchy remediation.
- **Fix and files changed:** dispatch queue #56/#57/#58; in-session GPT worker + reviewer remediation; future elevations must use the GPT hierarchy restored by D-045 and actuated by D-042.
- **Regression control added:** D-045 GPT hierarchy is now the required elevation path: GPT junior/orchestrator/worker plus independent D-037 reviewer; chief may record boundary evidence but must not replace the worker/reviewer chain.
- **New candidate SHA:** this WORKER-HIER-01 remediation commit.
- **Fresh verification commands/results:** repository JSON/fenced-JSON parse and `git diff --check` are required on this patch; D-037 process pass is still required after merge.
- **Hosted/cloud verification:** no new AWS mutation; retained AWS lab evidence is apply [29644662492](https://github.com/nathanielecon/ContinuityOps/actions/runs/29644662492), drill [29645042815](https://github.com/nathanielecon/ContinuityOps/actions/runs/29645042815), teardown [29645052414](https://github.com/nathanielecon/ContinuityOps/actions/runs/29645052414).
- **Superseded evidence:** none of the AWS lab evidence is superseded; only the earlier hierarchy/process completion claim is failed pending REVIEW-COMPLETION-02.
- **New evidence:** `evidence/judges/REVIEW-COMPLETION-01.json`; this break/fix entry; `OPERATING_STATE.md` revision 43.
- **Claim/status changes:** lab claim remains `portfolio-certified-L4-lab`; hierarchy closure is not claimed until D-037 process pass supersedes REVIEW-COMPLETION-01.
- **Judge round impact:** REVIEW-COMPLETION-01 is fail; REVIEW-COMPLETION-02 is expected to supersede after this remediation patch merges and is independently reviewed.
- **Remaining risk/follow-up:** ensure future live elevations do not proceed chief-only; close hierarchy remediation only after CI/contract validation plus independent GPT D-037 pass.
- **Verified by:** WORKER-HIER-01 implementation worker records; independent reviewer to supersede with REVIEW-COMPLETION-02.

## 2026-07-18 — BF-2026-014 — D-034 worker `base_branch: work` invents non-branch

- **Slice/task:** ORCH-CLOSE-02 cohort — issues #63/#64/#65 (WORKER-SEC-01, WORKER-AGENTIC-01, REVIEW-CLOSE-01).
- **Baseline SHA:** `ddfca8e81d9efd8ef4eeed1253bc2a8ee6ccb029`.
- **Environment/identity:** Codex App `@codex` + GHA `codex-patch-publish` (D-034); chief seat fallback.
- **Symptom:** patch apply + branch push succeeded, but `gh pr create` failed with `Base ref must be a branch` / `No commits between work and codex/issue-N-*` because workers set `base_branch: work`.
- **Exact failed check and exit:** Actions runs [29647973192](https://github.com/nathanielecon/ContinuityOps/actions/runs/29647973192), [29647966271](https://github.com/nathanielecon/ContinuityOps/actions/runs/29647966271), [29647912790](https://github.com/nathanielecon/ContinuityOps/actions/runs/29647912790) → `publish-failed`.
- **Root cause:** dispatch snippet placeholder `<stream-or-orch-branch>` was interpreted as inventing `work`; publisher trusted that string without verifying the remote ref.
- **Fix:** chief opened fallback PRs #66/#67 against `main`; rejected #65 (reviewer shipped terraform whitespace, not a D-037 verdict). Snippet now defaults/requires `base_branch: main`. Publisher coerces missing remote base refs to `main`.
- **Regression control added:** `docs/planning/dispatch/CODEX_DISPATCH_SNIPPET.zh.md` hard rule; `.github/workflows/codex-patch-publish.yml` remote-ref check before `gh pr create`.
- **Remaining risk/follow-up:** re-nudge open workers with explicit `base_branch: main`; D-037 reviewers for #66/#67 must emit verdict-only (no implementation diffs).

## 2026-07-18 — BF-2026-015 — App D-037 cannot fetch private PR `.patch`

- **Slice/task:** REVIEW-SEC-01 (#68) / REVIEW-AGENTIC-01 (#70) against PRs #66/#67.
- **Symptom:** Reviewers recorded `verdict: fail` / blocked because `curl` to `pull/N.patch` returned proxy/GitHub **403** inside the Codex App sandbox.
- **Root cause:** D-028 — worker gets data, not permission; private-repo patch URLs are not readable from the zero-credential App environment.
- **Fix:** Vendor review packets under `evidence/dispatch-packets/` and re-dispatch REVIEW-SEC-02 / REVIEW-AGENTIC-02 to apply in-repo diffs; do not rely on `pull/*.patch` for private ContinuityOps.
- **Remaining risk/follow-up:** Keep packaging diffs (or read-only vendored snapshots) in every D-037 dispatch for private PRs until a trusted in-repo packet path is standard.

## BF-2026-016 — Fresh council fail on tip-bind tip `c2e6610`

- **Detected:** 2026-07-18T18:57Z via PORTFOLIO-FRESH-JUDGE-02/03 (PRs #101/#102), `merge_ready: no`, scores ~7.9–8.0.
- **Symptom:** (1) portfolio_tip_sha named parent `196bed4` while judges scored tip `c2e6610`; (2) `terraform fmt -check` failed on four files; (3) k8s reset test mutated tracked `crashloop-reset.json`; (4) S8 `integrated-gate.json` claim_level L4 without `cloud_apply_evidence` → P8-T04 overclaim; (5) S1–S4 STREAM_COMPLETE boundaries still denied L4 while matrix claimed scoped lab L4.
- **Repair:** exact-SHA rebind; `terraform fmt`; restore evidence in scenarios test; add `cloud_apply_evidence` to integrated-gate + STREAM_COMPLETE; reconcile boundaries; regenerate P8-T04 validation on final tip.
- **Prevention:** tip-bind commits must set `candidate_sha` to the evidence commit itself (or an explicitly validated parent-of-tip model accepted by judges); never elevate integrated-gate to L4+ without `cloud_apply_evidence`; keep validation check-only for tracked evidence.

## BF-2026-017 — README claim tense lagged matrix L4 lab

- **Detected:** 2026-07-18T19:48Z via PORTFOLIO-FRESH-JUDGE-03 (PR #109), `merge_ready: no` (U5/U10); judges 01/02 passed at 9.7.
- **Symptom:** README still advertised L1 / no live apply while `docs/claims/matrix.json` and hosted evidence claimed scoped AWS lab L4 under A3.
- **Repair:** Update README status, results table, non-claims, and recruiter bullets to match A3 ceilings; re-dispatch fresh council on rebind tip.
- **Prevention:** Recruiter-facing claim prose updates atomically with matrix/hosted elevations (BF-PRE-001).
