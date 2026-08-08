# Worker roster 2.0 — identity, model, and who holds what

**New rule, versioned 2.0 at creation** so it sits beside the existing role
definitions in `AGENTS.md` and `AGENTS-2.0.md` rather than amending them.

## Why

Two problems, one fix.

**The supervisor could not answer "what model are the workers running?"** It had
been writing "all workers and judges are 5.4 medium" into dispatches on the
author's instruction, without ever verifying it — Codex workers do not volunteer
their model, the task links are unreachable from the session, and the
environment setting was requested but never confirmed. So a repeated claim stood
in for a checked fact. That is the same failure shape recorded twice already
today: **taking a report about a thing for the thing itself.**

**Concurrent lanes became indistinguishable.** Four slices, each with a judge, a
nixer and one or more fixers. The acceptance rule turns on whether the *same*
judge re-scored or a *cold* one read fresh — and with anonymous workers that
distinction lives only in the supervisor's memory, which has already proved
unreliable.

## The identifier

Assigned by the supervisor **in the dispatch**, echoed by the worker verbatim:

```
<LANE>-<ROLE>-<NN>
```

- `LANE` — `SHORTANS`, `NUMERIC`, `SOURCE`, `STRUCT`, or a repair-unit key such
  as `K6`
- `ROLE` — `JUDGE`, `COLDJUDGE`, `NIXER`, `FIXER`
- `NN` — sequence within that lane and role, starting `01`

Examples: `SHORTANS-JUDGE-03` · `K6-FIXER-01` · `STRUCT-NIXER-02` ·
`NUMERIC-COLDJUDGE-01`

**Supervisor-assigned, not self-generated.** A worker is stateless per task and
cannot know it is the third judge on a lane; only the supervisor holds that.
`COLDJUDGE` is a distinct role precisely so the acceptance record can show at a
glance that a cold read happened, rather than requiring someone to reconstruct
it from timestamps.

## The self-report

Every worker's reply opens with exactly four lines:

```
worker_id: SHORTANS-JUDGE-03
model: <the model identifier it is actually running>
reasoning: low|medium|high|unknown
context_remaining: 62%
```

### `unknown` is a correct answer

**If a worker cannot determine its model or reasoning level, it must write
`unknown`.** It must not guess, and must not echo a model named in the dispatch.

This is load-bearing. A worker that reads "all workers are 5.4 medium" in its
brief and reports `model: gpt-5.4` has told the supervisor nothing except that
it can read — and would have laundered an unverified assumption into an
apparently verified record. `unknown` is honest and costs nothing;
a plausible fabrication is the exact defect class this project exists to catch.

## What the supervisor does with it

- **Roster tracking.** Which worker holds which lane, and whether the re-score
  came from the same `NN` or a new one.
- **Retirement.** `context_remaining` decides whether a worker continues or is
  retired and replaced. The successor takes the next `NN`, and the handoff is
  legible in the thread.
- **Model comparison.** With `model` and `reasoning` on the record, lanes become
  a usable testbed — each slice has a frozen rubric and a numeric score, so
  running two lanes on different models against one build gives a real
  comparison of defects-found per round rather than an impression.

## Where it is enforced

`docs/planning/dispatch/CODEX_DISPATCH_SNIPPET.zh 2.0.md`, which is pasted into
every dispatch under the D-034 hard gate. A dispatch without the snippet is the
failure that cost this project eleven rounds of stranded patches; a dispatch
with it now also carries identity.
