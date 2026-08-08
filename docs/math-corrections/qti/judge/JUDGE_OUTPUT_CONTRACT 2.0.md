# Judge output contract 2.0 — machine-routable verdicts

**Supersedes:** nothing. This is a new rule, versioned 2.0 at creation so it
sits alongside the 1.x prose contracts in `JUDGE_BRIEF.md`, `COLD_BRIEF.md` and
`MASTER_PROMPT.md` rather than amending them. Those remain in force and
unedited; this adds a machine-readable channel beside the prose.

**Why it exists.** `pipeline-zero-hop.yml` (D-047) already automates every
routing decision the supervisor has been making by hand — `publish-ok` opens the
D-037 reviewer, a `fail` verdict opens a fixer, two same-class failures page the
chief and stop auto-fixing, judge evidence marked `merge_ready: no` opens the
nixer. **None of it fired**, because judges emit prose and the routers parse
structure.

Concretely: `scripts/pipeline/parse-verdict.mjs` looks for `"verdict": "pass"` or
a line beginning `verdict: pass`. A judge writing *"Score: 6.0/10 — FAIL"*
matches neither. `scripts/pipeline/extract-merge-ready.mjs` looks for
`merge_ready` in a file under `evidence/judges/**`. A judge writing a PR comment
produces no such file.

Two additions close both.

---

## 1. Every judge comment ends with a verdict line

Exactly this, at the start of a line, in the judge's own comment:

```
verdict: fail
```

`pass` or `fail` only. This is the routing signal, not the score.

## 2. Every judge emits an evidence file

Path: `evidence/judges/qti/<SLICE>-<build7>.json`, delivered in the judge's
`continuityops-patch-v1` block like any other patch.

```json
{
  "slice": "SHORTANS",
  "build": "247ae86e286f20db",
  "verdict": "fail",
  "merge_ready": "no",
  "score": 6.0,
  "items_in_slice": 74,
  "items_worked": 5,
  "items_worked_idents": ["g6_s1_f1", "g6_s1_f2"],
  "rules": [{"rule": "R5", "checked": 5, "pass": 0, "fail": 5, "not_checked": 69}],
  "findings": [
    {
      "ident": "g6_s1_f1",
      "rules": ["R5", "R13"],
      "rejected_correct_string": "multiplier",
      "accepted_set": ["coefficient", "numerical coefficient"],
      "harm": "a student who reads 7m as 7 multiplied by m types `multiplier` and scores 0"
    }
  ],
  "not_checked": ["source PDFs", "R8 scoring-tree binding"]
}
```

`merge_ready` takes `yes`, `no` or `provisional` — those three exactly; anything
else parses as null and routes nowhere.

---

## 3. The judge does not set the threshold, and is not told it

**This is the load-bearing rule and it is easy to get wrong.**
`RALPHY_ORCHESTRATION.md` §12 states plainly: *do not tell the judge the
threshold.* A judge told its target scores toward it. The supervisor violated
this repeatedly by putting "the bar is 10/10, non-negotiable" into dispatches.

So the division is:

- **The judge** reports `score` and `findings` from the rubric, and sets
  `verdict` on whether the slice meets the rubric **as written** — not against a
  number it was given.
- **The supervisor** holds the thresholds (≥9.5 general, 10/10 on mathematical
  accuracy and answer format) and derives `merge_ready` from the score before
  the evidence file lands.

A judge that asks what the bar is should be told: *report what you find; the bar
is not yours to apply.*

## 4. The prose is still the deliverable

The JSON routes; **the prose is the artifact.** `COLD_BRIEF.md` demands an
independently formed view and the gate demands *found / why / fix* with the
mathematics worked in full. Every finding in the JSON must correspond to a
worked finding in the prose. **A judge that emits only JSON has not judged.**

Judges do not compress. That is unchanged and not negotiable.

## 5. Coverage honesty is part of the contract

`items_worked` and `items_worked_idents` must be what was actually opened.
`not_checked` must be complete. An evidenced partial verdict is worth more than
an unevidenced whole one and will not be counted against a slice; claimed
coverage that was not performed is the only thing that will.

This has already paid: a judge reporting *"83 of 125 recomputed, zero coverage
on R8 and R9"* produced eight real defects, where an earlier unevidenced
"125 of 125, zero exceptions" produced none and had to be recorded as an
unverified claim.

---

## What this turns on

| Job in `pipeline-zero-hop.yml` | Needs | Now supplied by |
|---|---|---|
| `d037-verdict` | `verdict: pass\|fail` from the bot | §1 |
| `judge-merge-ready-no` (auto-nixer) | `merge_ready` in `evidence/judges/**` | §2 |
| `nixer-to-fixer` | nixer `publish-ok` on a NIXER-titled issue | already works |
| `publish-failed-renudge` | `publish-failed` comment | already works |

Two conditions remain outside this contract and are supervisor duties:

- **Dispatch on an issue, never a PR.** `classify-comment` requires
  `github.event.issue.pull_request == null`. Every dispatch made on a PR routes
  nowhere, which is why none of the above ran on its first day.
- **Main merges stay human.** The machine merges a pass to
  `candidate/portfolio-<7sha>` and never to `main`. Per the author's ruling the
  supervisor brings main merges for approval. Zero-hop means zero hops *within*
  a round, with the main merge as the deliberate gate at the end.
