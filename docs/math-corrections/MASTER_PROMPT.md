# Master prompt — math document correction & verification run

Paste this as the opening prompt of a **fresh session launched under pxpipe**.
It encodes everything learned on the previous run, including the mistakes.

---

## 0. Before anything else: sources first

**Do not plan, slice, or dispatch until every authoritative source is in hand.**

Required before work begins:

- Independent Practice **Part 1** and **Part 2** (the assignment)
- The **explanations companion** for each topic
- The **answer key** for each part
- The **worksheet** each companion explains (current revision)
- The **Canvas quizzes** students use to check homework
- The weekly **lesson plan**, if the run touches naming or scheduling

Rationale, from the last run: the two worst errors both came from planning before
the sources arrived. A correction was applied in the wrong direction because the
only evidence available was two answer keys that were wrong in the same way and
therefore corroborated each other. A whole judge loop then certified the wrong
property because the rubric was written before the design was understood.
**Neither would have been fixed by more reasoning effort.** They were missing-input
failures. If a source is missing, say so and stop — do not infer it from
downstream documents.

---

## 1. The three-variant rule (governs everything)

Each lesson question exists in three variants:

| Artifact | Variant | Purpose |
|---|---|---|
| Explanations companion | **C** | fully worked teaching example |
| Independent Practice Part 1 | **A** | student attempt |
| Independent Practice Part 2 | **B** | second attempt, fresh numbers |

Same question *type*, structure and wording pattern. **Different numbers and
different variable letters.**

- Variant C must differ from BOTH A and B, in numbers *and* in the variable
  letters used (Part 1 uses `a, b`; C must not).
- For an item with no numbers to vary (e.g. "Is `8x + 1` a linear expression?"),
  vary the variable.
- Variant C must be **pedagogically equivalent**: same difficulty, same step
  count, same arithmetic character. Do not make a division come out even that was
  meant to leave a remainder, or reduce a two-digit subtraction to one digit.
- Variant C must be used **consistently in every block** of the question — stem,
  Checked answer, worked steps, Final answer, closing paragraph. A stem in one
  variant with working in another is the original defect that started all this.
- **Answer keys are never variant C.** Part 1's key answers A; Part 2's key
  answers B.

> **Open interpretation, confirm before building:** "all numbers in variables" is
> read here as *variant C changes both the numbers and the variable letters* —
> NOT as *replace every number with a symbol*. A fully symbolic explanation cannot
> show a slow worked long division (3 ÷ 8 = 0.375), which is what these companions
> exist to do. If fully symbolic really is wanted, stop and confirm.

### Current status
The companions carry **Part 1's** numbers throughout — as did the originals.
Variant C was never implemented. This is authoring work across ~30 questions
(Topic 1) — not a repair. Author it fresh; the existing documents were not built
to this spec.

---

## 2. Task

1. Author variant C for every question in the explanation companions, per §1.
2. Verify the **Canvas quizzes** against the assignment and keys — students use
   them to check homework, so a wrong quiz answer is worse than a typo. Check
   every quiz item's question and accepted answer against the corresponding
   Part 1 / Part 2 item.
3. Re-run the judge loop (§4) under the corrected rubric.
4. Outstanding from the last run: the worksheet's **navy section banner boxes**
   are not reproduced in the rebuild (plain bold headings instead). Nobody owns
   the worksheet — assign it.

---

## 3. Agent roster and model tiers (measured, not guessed)

| Role | Model | Effort | Why |
|---|---|---|---|
| Coordinator (you) | Opus | **high** on design/adjudication turns, **medium** on dispatch/commit turns | last run's failures were judgment calls — tiebreaking conflicting judges, scoping a rubric — not compute |
| Judges | Opus | high | they catch what fixers and the coordinator miss; do not downgrade |
| Fixers, text substitution | Haiku | low | 11 slices repaired this way, 1 regression, caught |
| Fixers, tikz/geometry/alignment | Sonnet | medium | Haiku on figure coordinates is where silent breakage lives |
| Scanners / transcribers | Sonnet | medium | |
| Planner (§6) | Sonnet | medium | coverage bookkeeping, not judgment |

Do not downgrade judges to save tokens. The graders are what caught the fixers'
false reports.

---

## 4. Judge loop

One dedicated judge per slice. Judges **never edit**; a separate fixer applies.
Loop: score /10 → fixer → same judge re-scores → repeat until 10/10 → then one
**cold adversarial validation round** which must also be 10/10. Two consecutive
10/10 accepts the slice.

Rubric bar — all must hold, no rounding up, no "10/10 with minor notes":
fidelity per §1, arithmetic recomputed (never eyeballed), internal consistency,
corrections applied, typography, no fabrication.

**Assign every artifact an owner, including worksheets and quizzes.** Last run the
worksheet had no owner and its defect is still open — no judge was looking.

**Record acceptances against a build hash.** A rebuild moves page numbers and
glyph coordinates and stales the evidence. A rebuild that changes an accepted
slice's *text* reopens it.

**Expect transcript loss.** Four of eleven slices lost judge memory between
rounds. A judge that finds itself without prior context must say so and read
cold, not pretend continuity.

---

## 5. Instrument failures — verified traps, do not rediscover

Instrument errors outnumbered document defects last run. Every one produced a
confident wrong answer.

| Trap | Correct method |
|---|---|
| `grep -P '[\x{4e00}-...]'` errors, prints nothing, **exits 0** — passes while checking nothing | Python regex; **self-test the detector on a known CJK string first** |
| Same check on a **PDF** false-positives (stream bytes decode as CJK) — 6/6 files | scan text files only; use `pdftotext` output for PDFs |
| `\rule` emits an `l` line primitive, **not** an `re` rectangle — counting `re` reports every answer blank as missing | match **both** `l` and flat `re` |
| `pdftotext -layout` **transposes** built-up fractions — correct `4/7 = ?/21` extracts as `47 = 21 / ?` | settle fractions by glyph **y-coordinates**, never extraction order |

**Standing rule:** when a measurement contradicts a visible fact, suspect the
instrument first, then confirm along a second and third independent path
(coordinates, bitmap render, source).

---

## 6. Planning layer

A planner agent runs beneath the coordinator and produces a **frozen coverage
matrix** before work starts:

- every artifact → an owner
- every check class → an owner
- every slice → its model tier and effort

**Freeze the coverage. Never freeze the findings.** A checklist frozen before the
sources arrived would have locked in last run's wrong correction and made it
harder to overturn.

**Re-plan trigger:** any new authoritative source arriving mid-run forces an
automatic coverage re-derivation. Last run the lesson plan and assignment arrived
late and were reconciled ad hoc.

---

## 7. Token strategy

Launch under **`pxpipe warp -- claude`** — see `PXPIPE_HANDOFF.md`, including the
decision gate for managed gateways and the validation gate before trusting imaged
context on a judge loop.

Measured last run:

- The cost was **input**, not output: judge reports re-entering context, the same
  rubric shipped into 30+ launches, PDFs re-read after every rebuild.
- `rtk`: 64% on `ls -la`; **−17% on `git status`** — it adds bytes to short output.
  Use for `ls`/`grep`/`find`/builds. Never between a judge and evidence it scores.
- `caveman`/wenyan prose compression: **no measurable saving.** Compression hit
  prose; prose was never the cost. Measurement was, and measurement is
  incompressible.
- Cheap fixers + frontier judges: **the one clear win.**
- `cavecrew`: untried, and it targets the actual cost centre (subagent reports
  re-entering the coordinator). **Enable it this run.**

Additional levers, in expected-value order:

1. **Prompt caching** — the rubric, design spec and directives are shipped to
   every agent unchanged. That is the ideal cached prefix. Put all stable
   instructions in one block, ahead of anything per-slice.
2. **Batch API** for the non-interactive fan-out (scanners, first-pass fixers)
   where latency does not matter.
3. **Stop re-reading PDFs after every rebuild.** Extract once per build hash to a
   text/coordinate cache; judges read the cache unless they are scoring geometry.
4. **Slice by artifact boundary, not page range.** Page-range slices caused the
   re-read churn when pagination shifted.
5. Do not pay for verification twice: if a judge verified arithmetic in round N
   and the text did not change, the next round re-verifies **only what moved**.

I cannot verify current per-token prices from this environment — the pricing
article is blocked by network policy. Take live figures from
`~/.pxpipe/events.jsonl` and the provider's own pricing page rather than any
number quoted from memory.
