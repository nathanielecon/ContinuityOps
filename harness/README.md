# ContinuityOps Validation Harness — Sourcing and Run Guide

This directory is the home of the deterministic validation harness that the
orchestrator runs against candidate work before any judge round. This README
closes a cold-start continuity gap: the authoritative task plan (`PLAN.md`)
names validator IDs, but a cold orchestrator working only from this branch could
not locate their implementations or learn how to invoke them. That mapping is
recorded below.

> Status: the harness implementation referenced here is a **candidate**. It has
> not been merged into the authoritative branch through the governed path.
> Formal adoption is the job of tasks **P0-T02** (install the authoritative CLI
> and state contracts) and **P0-T03** (implement validators, routing, and
> evidence adapters) under their human-gated authorization. Until then, treat
> the files below as the reviewed source of truth for *how the validators are
> meant to run*, not as an installed part of this branch.

## Where the implementation lives

The validator implementation is not on this branch. It lives on the candidate
branch:

- **Branch:** `claude/cloud-gpt-ralphy-validation-6m0gkz`
- **Pinned commit:** `2c9026b29e96e37c768db9737e2d9539fdeb7003`

Fetch and check it out (read-only inspection or a throwaway worktree) to run the
harness:

```bash
git fetch origin claude/cloud-gpt-ralphy-validation-6m0gkz
git worktree add ../co-harness 2c9026b29e96e37c768db9737e2d9539fdeb7003
```

## Files that make up the harness

| Concern | Path (on the candidate branch) |
| --- | --- |
| Orchestrator CLI (the run surface) | `scripts/project.mjs` |
| Allowlisted validator registry (fail-closed on unknown IDs) | `harness/lib/validators/registry.mjs` |
| Pinned validator implementations | `harness/lib/validators/impl.mjs` |
| Authoritative task-state store | `harness/state/tasks.json` |
| Partition helpers (unique ownership, coverage, hashing) | `harness/lib/partition.mjs` |
| JSON Schemas | `harness/schemas/*.schema.json` |

No task may supply an arbitrary shell command. Validators are referenced only by
allowlisted ID; an unknown ID fails closed (returns `ok: false`,
`fail_closed: true`). Every validator is check-only and must not mutate the
repository.

## The four P0-T01 validators

`PLAN.md` binds task `P0-T01` to exactly these four validator IDs. Each is
registered in `harness/lib/validators/impl.mjs`.

| Validator ID | What it checks | Reads |
| --- | --- | --- |
| `state_schema` | Task-state store has the required top-level keys and every task has a legal id and lifecycle state | `harness/state/tasks.json` |
| `partition_unique_ownership` | No retained path is owned by more than one slice | `harness/partition-manifest.json` |
| `upstream_pin_schema` | `project_a`/`project_c` carry concrete `repository` + `commit_sha`; Project C `image_digest` is a real `sha256:...` digest **or** the literal `UNAVAILABLE` (the `REQUIRED...` placeholder fails) | `integration/upstreams.lock.json` |
| `clean_tree` | Working tree has no uncommitted changes | `git status --porcelain` |

## Exact run command and exit-code convention

The four validators are not run one-by-one from the shell; they are driven as a
set through the CLI, keyed by task ID. For P0-T01, from a checkout of the
candidate branch (which contains `harness/state/tasks.json` with the `P0-T01`
entry and its `validators` list):

```bash
node scripts/project.mjs validate P0-T01
```

Output shape:

```text
  [PASS] state_schema
  [PASS] partition_unique_ownership
  [PASS] upstream_pin_schema
  [PASS] clean_tree
VALIDATE OK
```

Exit codes:

| Exit | Meaning |
| --- | --- |
| `0` | `VALIDATE OK` — every validator in the task's list passed |
| `1` | `VALIDATE FAIL` — at least one validator returned `ok: false` (also used for a thrown `ERROR:`) |
| `2` | Unknown or missing CLI command |

Related commands (same CLI, same exit convention):

```bash
node scripts/project.mjs validators          # list every registered validator ID
node scripts/project.mjs partition-verify     # unique ownership + coverage over tracked *.mjs
node scripts/project.mjs status               # print plan revision and per-task states
```

`partition-verify` exits `1` on duplicate ownership or an unowned tracked
`*.mjs` file, `0` otherwise.

Runtime: Node 22 (verified with `v22.22.2`), no external dependencies; the CLI
uses only Node built-ins and `git`.

## Where the P0-T01 worker contract actually lives

The finalized P0-T01 worker task contract is **not** on this branch and does not
resolve by a plain path read from here. It is committed on the stream branch:

- **File:** `docs/planning/dispatch/P0-T01.zh.md`
- **Branch:** `origin/stream/S0-baseline-audit`
- **Pinned commit:** `648791d4ec88fde914b0f8c17be8f94cc4da2b62`

Read it with:

```bash
git show origin/stream/S0-baseline-audit:docs/planning/dispatch/P0-T01.zh.md
```

The authoritative *task definition* (id, write scope, validators, evidence path)
remains `PLAN.md` on the authoritative branch; the file above is the dispatched
worker contract in Simplified Chinese.
