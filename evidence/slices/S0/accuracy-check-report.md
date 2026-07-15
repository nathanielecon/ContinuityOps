# S0 Ralphy Accuracy-Check Report

**Slice:** S0 (Phase-0 orchestration + validation harness)
**Certified candidate SHA:** `a750fad`
**Method:** post-build logical partition + fresh independent judge councils
(RALPHY_ORCHESTRATION.md §9–10, §18), adversarial "code accuracy / bug absence".
**Judges:** independent Claude subagents, recorded model id `claude-opus-4-8`.
*(The plan's Codex/Grok topology is not invokable in this environment; workers
and judges are Claude, recorded truthfully — see docs/scaffold-audit.md.)*

## Partitions checked

The final codebase was repartitioned by capability and each partition was judged
independently on a committed SHA (never a worktree):

| Partition | Files |
| --- | --- |
| S0-CLI / state | state, lifecycle, authorization, streams, CLI, task-state schema |
| S0-VALIDATE | validator registry + impls, evidence adapter, partition, hashing, model-id |
| integration | whole-repo: tests non-vacuous, CLI↔library parity, cross-file consistency, claim honesty |

## Result

Four councils were run. Each code/doc change invalidated prior scores and a
fully fresh council re-judged the new candidate. Defects found were repaired via
a nixer/fixer loop with one regression test added per fixed class.

| Round | SHA | Scores | Defects | Max severity | Outcome |
| --- | --- | --- | --- | --- | --- |
| 1 | `68c1c29` | 0.70 / 0.82 / 0.58 | 11 | medium | fail → fix |
| 2 | `7d2d896` | 0.72 / 0.85 / 0.90 | 4 | high (self-inflicted regression) | fail → fix |
| 3 | `443747f` | 0.92 / 0.96 / 0.82 | 4 | medium | fail → fix |
| 4 (cert) | `a750fad` | **0.97 / 0.98 / 0.92** | 1 (doc off-by-one) | low | **pass** |

**Certification:** the round-4 fresh council returned three `merge_ready: yes`
verdicts, mean 0.957 (≥0.95), minimum 0.92 (≥0.90), no critical/high finding —
meeting the fresh-council exit thresholds in RALPHY_ORCHESTRATION.md §10. The
single low finding (a "+4 vs +3" regression-test miscount in STATUS/BF-003) was
corrected in the certification commit; it is documentation-only and changed no
judged code.

## What was actually proven

- 27 → 39 harness tests, all passing, verified non-vacuous by an independent judge.
- 19 real defects found and fixed across rounds, each with a regression test.
- Live runtime guards (via the `project` CLI, not just unit tests): unauthorized
  phase rejected, `NaN` authorization rejected, worker evidence-forgery blocked,
  aspirational model-id rejected, partition coverage enforced.

## Honest boundaries

- This certifies the **Phase-0 harness only** — the machinery that partitions and
  accuracy-checks the codebase. Phases 1–8 (Terraform/EKS/serverless/recovery)
  are unbuilt, unauthorized (`authorized_through_phase = 0`), and human-gated.
- No live cloud resource was created; no cloud evidence is claimed.
- Judge scores are LLM-council judgments, not a formal proof; they are recorded
  with the exact model id and are reproducible against the committed SHA.
