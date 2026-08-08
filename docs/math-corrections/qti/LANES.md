# QTI lanes — live board

Generated 2026-08-08 19:07 UTC by `lanes.py`. **Do not hand-edit.** Re-run the
script; a board someone maintains by hand is how `ACCEPTANCE.md`
went stale for a whole corpus revision.

**Build under test:** `2eea45c03ca61ddf`

## Lanes

| slice | issue | worker | model | ctx | rounds | verdict | score | bar | last |
|---|---|---|---|---|---|---|---|---|---|
| **NUMERIC** | [#184](https://github.com/nathanielecon/ContinuityOps/issues/184) | `NUMERIC-JUDGE-02` | GPT-5.6 Sol | 90% | 1 | fail | — | 10.0 | 18:53 |
| **SHORTANS** | [#181](https://github.com/nathanielecon/ContinuityOps/issues/181) | `SHORTANS-FIXER-02` | GPT-5.6 Sol | 80% | 3 | - | 9.2 | 10.0 | 18:38 |
| **SOURCE** | [#185](https://github.com/nathanielecon/ContinuityOps/issues/185) | `SOURCE-JUDGE-02` | GPT-5.6 Sol | 92% | 1 | fail | — | 10.0 | 18:53 |
| **STRUCT** | [#186](https://github.com/nathanielecon/ContinuityOps/issues/186) | `STRUCT-FIXER-02` | GPT-5.6 Sol | 90% | 1 | - | — | 9.5 | 18:52 |

`verdict` and `score` are the latest a worker reported. **No slice is
accepted until it clears its bar twice — once from the judge that found
its defects, re-scoring after repair, and once from a cold judge reading
fresh.** A single pass is not acceptance.

## Opened by the routers, not by hand

- `ISS` [#189](https://github.com/nathanielecon/ContinuityOps/issues/189) 18:53 — [codex-dispatch] JR-EXCEPTION-d037-missing-pr
- `ISS` [#188](https://github.com/nathanielecon/ContinuityOps/issues/188) 18:53 — [codex-dispatch] JR-EXCEPTION-d037-missing-pr
- `PR ` [#187](https://github.com/nathanielecon/ContinuityOps/issues/187) 18:39 — codex-dispatch #181: mechanical publish (D-034)
- `PR ` [#183](https://github.com/nathanielecon/ContinuityOps/issues/183) 17:52 — codex-dispatch #180: mechanical publish (D-034)
- `PR ` [#182](https://github.com/nathanielecon/ContinuityOps/issues/182) 17:07 — codex-dispatch #180: mechanical publish (D-034)
- `PR ` [#176](https://github.com/nathanielecon/ContinuityOps/issues/176) 11:56 — codex-dispatch #165: mechanical publish (D-034)

Each of these is a hop the supervisor did not perform. That is the
measure of zero-hop: not that the wiring looks right, but that
downstream work appears without a human trigger.

