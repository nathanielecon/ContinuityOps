# Supervisor–Orchestrator Branch Review Protocol

Status: active (D-025). Audience: the lead Ralphy orchestrator (Claude Opus
4.8, cloud) and any co-orchestrators. This document is the supervisor's
standing communication of the review mechanism; the orchestrator must load it
as part of the durable-context read set.

## Roles

- **Portfolio supervisor:** Claude cloud session operating on branch
  `claude/orchestrator-supervision-wuw01a`. Minimal-intervention policy: the
  supervisor does not review individual worker handoffs and does not poll.
- **Lead orchestrator:** owns streams, task state, worker dispatch/retirement,
  and the completion signal defined below.

## Stream branches

- One branch per Ralphy stream: `ralphy/<slice>-<stream>` (e.g. `ralphy/s0-a`).
- A stream branch has one mutation owner and is sequential internally, per
  `AGENTS.md`. Branches of concurrent streams must own disjoint partition
  paths.

## Completion signal (the only supervisor trigger)

The supervisor fetches and reviews a stream branch **only after the
orchestrator declares it complete**. To declare completion, the orchestrator:

1. Ensures the branch tree is clean and all adapter-owned evidence is
   committed.
2. Commits, as the branch's final commit, a completion manifest at
   `integration/queue/<branch-slug>.json`:

```json
{
  "schema_version": "1.0",
  "branch": "ralphy/s0-a",
  "task_ids": ["P0-T01"],
  "baseline_sha": "40_HEX",
  "candidate_sha": "40_HEX",
  "validators_run": [],
  "validation_digest": "64_HEX",
  "evidence_paths": [],
  "worker_dispatches": [
    {"role": "", "model_id": "", "mode": "default", "context_remaining": null}
  ],
  "declared_complete_at": "ISO-8601"
}
```

3. Signals the supervisor (message into the supervision session, or via the
   human) with exactly: branch name and manifest path.

## Supervisor review procedure (single fetch, no polling)

On signal, the supervisor runs:

```bash
git fetch origin <branch>
git show origin/<branch>:integration/queue/<branch-slug>.json
git diff --stat origin/main...origin/<branch>
```

and reviews the manifest, diff footprint versus the declared `write_scope`,
and evidence linkage. Outcome is one of: pass to integration queue, return to
orchestrator with findings, or escalate to the human. The supervisor never
merges; the integration queue serializes merges per `AGENTS.md`.

## Cost rationale

One fetch plus one manifest read per completed stream keeps supervisor token
and network cost proportional to completed work, not elapsed time. Recorded as
prevention rule BF-PRE-015 in `BREAK_FIX_LOG.md`.
