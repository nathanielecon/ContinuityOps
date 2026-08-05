# Token strategy — what was measured, and how to apply pxpipe next time

Written after a long orchestration run (deep scan → LaTeX rebuild → 11-slice
adversarial judge loop over five documents). Numbers here are measured on that
run, not quoted from tool READMEs.

## What actually cost tokens

The run's cost was **input**, not output:

- judge reports re-entering the coordinator's context (30+ agents, 80k–206k each)
- the same rubric, directives and findings shipped into every agent launch
- PDFs re-read after every rebuild, because a rebuild voids prior coordinates
- a long system prompt paid on every turn of a very long session

Output was never the bottleneck. That matters, because two of the four tools
tried compress output.

## Measured results

| Tool | Targets | Result on this run |
|---|---|---|
| `rtk` | bash output | 64% on `ls -la` (1995B→719B); **−17% on `git status`** (160B→187B). Real but narrow: it *adds* bytes to short output. |
| `caveman` / wenyan | agent prose | **No measurable saving.** Round-1 English judges averaged ~113k tokens; wenyan rounds ran 97k–206k, averaging higher. |
| cheap fixers | model tier | **The one clear win.** 11 slices repaired on Haiku/Sonnet instead of Opus, including both hard geometry fixes. One regression, caught by a judge. |
| `cavecrew` | subagent output re-entering context | Never exercised. Second-best lever — it hits the actual cost centre. |

The wenyan comparison is confounded — later rounds did far heavier work (glyph
coordinates, 600 dpi scans, 69-item audits). But that is the point: **compression
applied to prose, and prose was never the cost. The cost was measurement, and
measurement is incompressible.**

## pxpipe — the correctly-aimed tool

`https://github.com/teamchong/pxpipe` (cloned at `/workspace/teamchong/pxpipe`).

A local proxy that renders bulky *request* context — system prompt, tool docs,
older history — into dense PNGs before the request leaves the machine. An
image's token cost is fixed by pixel dimensions, not by the text packed inside
(~3.1 chars/image-token vs ~1 char/text-token). It compresses the request only,
never the model's output.

That is the same set of things this run paid for repeatedly.

### Where it works today: local CLI

```bash
pxpipe warp -- claude          # also: cursor-agent, codex
# or
npx pxpipe-proxy                                   # 127.0.0.1:47821
ANTHROPIC_BASE_URL=http://127.0.0.1:47821 claude
```

Prefer `warp`: it keeps `/remote-control`, claude.ai connectors and first-party
gates working, which the bare env-var form can break.

For heavy orchestration runs like this one, run them from the **local CLI under
`warp`** rather than from the web environment. That is the whole adoption story
in one line.

### Where it does NOT work: this remote environment

`ANTHROPIC_BASE_URL` is already set here, pointing at a managed gateway, and
requests additionally traverse an agent proxy (`HTTPS_PROXY`,
`NODE_EXTRA_CA_CERTS`, `/root/.ccr/ca-bundle.crt`). Two blockers:

1. **Mid-session is impossible in principle.** The running agent's inference does
   not originate from a shell in this container. Starting a proxy and rewriting
   an env var changes nothing about the session doing the rewriting, and
   subagents inherit the same path.
2. **Chaining is unvalidated.** In principle an environment setup script could
   start pxpipe and point `ANTHROPIC_BASE_URL` at it, with pxpipe forwarding to
   the gateway that variable currently holds. Its README documents routing
   `api.anthropic.com` by default, not an arbitrary upstream behind a
   corporate-style proxy with a custom CA. Treat as experimental: it can break
   auth for the whole environment, and a failure mode here is a dead session,
   not a slow one.

## Guardrail specific to this workload

Before trusting pxpipe on a judge loop, **validate that imaged context does not
degrade fine-detail reading.** This run's verdicts depended on evidence that is
exactly the kind imaging might blur:

- glyph x-coordinates to 0.01pt (decimal-column alignment)
- 600 dpi pixel scans distinguishing teal leader lines from black glyph strokes
- true-superscript checks by baseline offset

Note these were read from *rendered PDF pages*, which are already images — the
question is whether pxpipe's re-imaging of surrounding context changes how
carefully the model reads them. Cheap test: run one slice's validation round
with and without pxpipe and diff the verdicts. If they disagree, keep judges on
plain text and image only the fixer and scanner traffic.

Its own demo notes the imaged arm needed a nudge to match a requested output
format — consistent with mild instruction-following drift, which matters for
agents held to a strict report schema like the judge rubric.

## Recommended configuration for the next run

1. Launch from local CLI under `pxpipe warp`.
2. Enable `cavecrew` for subagent delegation — compresses reports re-entering
   the coordinator, the largest single input cost measured here.
3. Keep cheap fixers (Haiku for text substitution, Sonnet for geometry/tikz),
   frontier models for judges. Proven.
4. Keep `rtk` for `ls`/`grep`/`find`/build output. Skip it for short commands
   and never between a judge and evidence it is scoring.
5. Skip prose-compression modes unless the run is prose-heavy. This one was not.
6. Take the real number from `~/.pxpipe/events.jsonl` (per-request
   `count_tokens` counterfactual), not from list-price bill estimates.
