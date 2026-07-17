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

No ContinuityOps execution failures have been recorded. The project is still at
candidate-plan stage.
