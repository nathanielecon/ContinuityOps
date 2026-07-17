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

## Log

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
