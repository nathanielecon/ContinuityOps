# Handoff: wire up pxpipe

**For:** an agent with shell access on the machine that will *launch* Claude Code.
**Not for:** an agent running inside a managed remote Claude Code session — see
"Why this cannot be done from inside a session" before starting.

Goal: cut **input** tokens by routing Claude Code through a local proxy that
renders bulky request context (system prompt, tool docs, older history) as dense
PNGs. Measured basis for doing this at all is in `TOKEN_STRATEGY.md`.

---

## 0. Preconditions — check these first, abort if unmet

```bash
node --version          # >= 20
npx --version
echo "${ANTHROPIC_BASE_URL:-<unset>}"
echo "${HTTPS_PROXY:-<unset>}"
```

**Decision gate:**

- `ANTHROPIC_BASE_URL` **unset** and `HTTPS_PROXY` **unset** → standard case,
  proceed to step 1.
- `ANTHROPIC_BASE_URL` **already set** → you are behind a managed gateway.
  pxpipe routes `api.anthropic.com` by default, not an arbitrary upstream.
  **Do not overwrite the variable.** Go to "Chained upstream" below and treat the
  whole task as experimental.
- `HTTPS_PROXY` set with a custom CA (e.g. `NODE_EXTRA_CA_CERTS`,
  `/root/.ccr/ca-bundle.crt`) → pxpipe's outbound calls must trust that CA too.
  Verify before committing to the change.

Failure mode if you get this wrong is a **dead session**, not a slow one. An
agent that cannot reach the API cannot tell you it broke.

---

## 1. Standard install (local machine, direct to api.anthropic.com)

```bash
npx pxpipe-proxy          # starts on 127.0.0.1:47821, dashboard at /
```

Leave it running. In the session you actually want compressed:

```bash
pxpipe warp -- claude     # PREFERRED
```

Use `warp`, not the bare `ANTHROPIC_BASE_URL=...` form. `warp` preserves
`/remote-control`, claude.ai connectors and first-party gates, which the env-var
form can break.

Verify before trusting it:

1. Dashboard at <http://127.0.0.1:47821/> shows live token counts and every
   text→image conversion side by side.
2. Run one real turn. Confirm the response streams normally — pxpipe compresses
   the *request* only, never output.
3. Confirm the kill switch works. You want to be able to disable it mid-run
   without restarting the session.

---

## 2. Chained upstream (managed gateway already in `ANTHROPIC_BASE_URL`)

Experimental. Only attempt with a way to roll back.

1. Record the current value: `ORIG="$ANTHROPIC_BASE_URL"`.
2. Determine whether pxpipe supports forwarding to a non-default upstream —
   check `src/core/` and the dashboard config, not just the README.
3. If it does: start pxpipe pointed at `$ORIG`, then set `ANTHROPIC_BASE_URL` to
   the pxpipe address **for a new process only**, never globally.
4. Confirm auth still works with a trivial call before running anything real.
   Auth headers, the custom CA, and any first-party gating all have to survive
   the extra hop.
5. If it does not support a custom upstream: **stop.** Report that and use the
   local-CLI path instead. Do not patch pxpipe to make it fit.

---

## 3. Validation gate — required before using it on a verification workload

This matters if the run involves judges, review, or any agent whose conclusions
rest on fine visual detail. On the run that produced this repo, verdicts rested
on glyph x-coordinates to 0.01pt, 600 dpi pixel scans separating a teal leader
line from a black glyph stroke, and superscripts confirmed by baseline offset.

Those were read from *rendered PDF pages* — already images. The open question is
whether pxpipe re-imaging the surrounding context changes how carefully the model
reads them.

**Test:**

1. Pick one slice with a known, previously-confirmed verdict
   (`judge/LOOP_STATE.md` has eleven).
2. Run its validation round twice — once through pxpipe, once direct.
3. Diff the two reports. Compare the *evidence*, not just the score: does the
   pxpipe run still produce coordinates and pixel counts, or does it drift toward
   impressionistic language?

**If they disagree:** keep judges on plain text; image only fixer and scanner
traffic. pxpipe's own demo notes the imaged arm needed a nudge to match a
requested output format — mild instruction-following drift, which is exactly what
a strict report schema is sensitive to.

---

## 4. Measure honestly

Take the number from `~/.pxpipe/events.jsonl` — the per-request `count_tokens`
counterfactual. Do **not** report the README's headline bill reduction: it is
priced at list rates that move, and the durable figure is the token cut.

Report: input tokens before/after, per request class (system prompt, tool docs,
history, per-turn). Expect the win to be concentrated in long sessions with large
static context, which is precisely the orchestration case.

---

## Why this cannot be done from inside a session

A running agent's inference does not originate from a shell in its own container.
Starting a proxy and rewriting an environment variable changes nothing for the
session doing the rewriting, and subagents inherit the same path. pxpipe is a
**launch-time wrapper**, not a runtime toggle.

If you are an agent inside such a session and were asked to "turn on pxpipe":
say this, and hand back the local-CLI instructions. Do not set the variable and
report success — nothing will have changed, and the next measurement will
disagree with you.

---

## Definition of done

- [ ] Preconditions checked; the decision gate produced an explicit branch
- [ ] Proxy running; dashboard reachable; kill switch exercised
- [ ] One real turn completed, response streamed normally
- [ ] Validation gate run if the workload includes judges — verdicts diffed
- [ ] Before/after input tokens taken from `events.jsonl`, not from list prices
- [ ] Rollback documented: exact command to return to the prior configuration
