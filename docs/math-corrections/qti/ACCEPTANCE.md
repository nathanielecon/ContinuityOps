# Acceptance ledger — QTI slices

A slice is **accepted** only on two consecutive 10/10 verdicts: one from the
judge that found its defects, re-scoring after repair, and one from a cold judge
reading the slice fresh at high effort.

Slices clean at r1 with no repair have no r2 round — their two reads are r1 and
cold.

| Slice | r1 | r2 | cold | Accepted |
|---|---|---|---|---|
| T1-1 | 6 | 10 | **10** | **yes** |
| T1-2 | 7 | 10 | **10** | **yes** |
| T1-3 | 8 | 10 | **10** | **yes** |
| T1-4 | 9 | 10 | **10** | **yes** |
| T1-5 | 7 | 10 | **10** | **yes** |
| T1-6 | 8 | 10 | **10** | **yes** |
| T1-7+10 | 10 | n/a | **10** | **yes** |
| T1-8 | 5 | 10 | | |
| T1-9 | 10 | n/a | | |
| SC-1 | 5 | 10 | | |
| SC-2a | 7 | 10 | | |
| SC-2b | 7 | 10 | | |
| G1a | 6 | 10 | | |
| G1b | 6 | 9 -> 10 (r3) | **10** | **yes** (content, at pre-format-round state) |
| G2a | 10 | n/a | | |
| G2b | 8 | 10 | | |

## G1b cold read closed the outstanding bottleneck — 10/10

18 of 18 items worked, no defects. It did not ratify: it ruled explicitly on nine
near-misses, and the two that mattered were the ones where a true-but-unkeyed
choice would actually hide — `H3/choice_6` and `H4/choice_6`, where an equivalent
flip (`5 < x` for `x > 5`) would have been a criterion-2 defect. It read the raw
entities to confirm both were the *reversed* form, and therefore false.

**It re-verified the H6/H7 arrowhead fix along three independent paths** rather
than taking r3's word for it: marker source (`markerUnits="userSpaceOnUse"`,
`refX="17"`, so the marker no longer scales with `stroke-width:5`), coordinate
geometry (leftward rays terminate at x=310, value −8, the open end), and a raster
render. Ink means membership and the ink is correct.

**Scope of this acceptance.** The cold read was taken against the corpus *before*
the answer-format round. Its finding is that the mathematics, keys, stems and
figures are sound. The round then changed several of these items — `F1`–`F4` to
short answer, `H3`–`H5` to short answer, `A1`/`H6`/`H7` re-lettered and their
choices permuted — none of which moves a key, but all of which change the
structure. So this row certifies the content, not the post-round file; the
changes are verified separately in the answer-format ledger below.

(An earlier draft of this note said the items became "single-answer multiple
choice". That was the design before the author set the type hierarchy — numeric,
then short answer, then select-all — and no multiple-choice item was ever built.)

## G1b took three rounds

r2 closed the six original defects but opened a seventh: the leftward rays on
rows C and D of H6/H7 put their arrowhead at the circle rather than the open end.
`markerUnits="strokeWidth"` scales the marker by the ray's `stroke-width:5` to
45px, and `refX="9"` pins the tip at the circle, so the body painted a filled
wedge across ~1.73 units of the region the graph must leave blank. On a number
line ink means membership, so both rows depicted something other than what their
label claimed. r3 closed it.

I had recorded that defect as cosmetic and left it. The judge that owns those
items overruled me, quantified the geometry, prototyped the fix in its own
scratchpad and rendered it before recommending. It was right.

## A coordinator error, recorded because it nearly damaged the record

I accused that judge of fabricating a quotation. **The accusation was false and
the judge was right.**

I sent it four messages, not the two I remembered. The second read "Coordinator.
Your ruling stood and I applied your fix. Re-score G1b." and contained the
passage the judge quoted, verbatim. I lost track of having sent it, told the
judge in my third message that the provenance of the SVG write could not be
reconstructed, and in my fourth asserted it had invented the quotation.

The judge refused the amendment I demanded. I had asked it to write that I never
said the fix was applied; it declined on the ground that this would put a false
statement into the record to remove a true one, and restored the verbatim text
instead. That was the correct call, made under pressure from the party
commissioning its report.

The one error that was genuinely its own it had already found and owned before I
raised anything: it put quotation marks around a compressed paraphrase, having
applied a stricter standard to the md5 evidence in the same report than to its
own citation.

**This also resolves the 00:11:34 write, against me.** It was not unattributed.
I dispatched that fix, announced it to the judge, then lost the thread and
reported it as a mystery. The timestamps the judge produced were accurate
throughout.

## An instrument recommendation of mine that was wrong

I told the cold judges to verify delimiter nesting by an ordered scan of `\(`
and `\)` rather than by counting. The T1-5 cold judge tested that against the
known-broken original and found **the ordered scan passes on the broken text
too** — token order `\( \) \( \)` with depth never exceeding 1, while the second
span was actually the prose `C, then drops $1.85^\circ`.

Two checks do discriminate, and both are cleaner:
- **span-content inspection** — extract each `\(...\)` span and reject any
  containing prose or a `$`;
- **`$`/`\(` co-occurrence** — reject any `mattext` block containing both. This
  is the better test: corpus-wide, 39 blocks contain a bare `$` and exactly none
  of them also contains `\(`, so it flags all four original defects with no
  false positive on the legitimate currency stems.

An ordered scan that also tokenises `$` reports a false alarm on the currency
stems, because their `$` counts are odd, and would have sent a correct file back
around.

---

## Answer-format round — judge ledger

A slice is accepted only at **10/10**. No partial acceptance, no "10/10 with
minor notes". Gate: `judge/JUDGE_RUBRIC_QTI.md` + `judge/FORMAT_ROUND.md`,
frozen and identical for every judge, amended only before the round opened.

| Slice | r1 | r2 | final round | Accepted |
|---|---|---|---|---|
| NUMERIC (108 keys) | **10** | — | **10** | needs one more clean read |
| SELECTALL (34 items) | 8 | pending | 9 | |
| AUTHORED (distractors + stems) | 8 | pending | 8 | |
| STRUCT / PERMUTE (177 items) | 9 | pending | 9 | |
| SHORTANS (35 items) | 4 | 5 | 8 | |
| T1-4 cold (14 items, fresh judge) | — | — | 9 | |
| G1b cold (18 items, content) | — | **10** | — | **yes**, at pre-round state |

**No slice is accepted on the final round.** Every finding was applied, but a
score is only evidence about the artifact that was judged, and the artifact
changed underneath all six verdicts. Re-judging is required, and nothing here
should be read as certifying the current build.

The one slice that scored 10/10 — NUMERIC, all 108 keys recomputed from their
own stems — is the closest to accepted, and even it needs a second consecutive
clean read to meet this project's bar.

### What the judges caught that nothing else would have

Every one of these was introduced *by this round*, while trying to improve the
corpus. They are the argument for a gate that cannot be talked down.

- **An instruction that disclosed its own answer.** "Enter one symbol only" on
  `topic-sc-1` Q2 is a mathematical claim: of `< > = ≠`, two distinct numbers
  make exactly two true, so demanding one symbol entails equality — the whole
  question, with no arithmetic. Reverted to select-all.
- **A stem false against its own key.** `F4` promised "one or two words" for a
  three-word answer, steering a correct student to "division", which scored zero.
- **A deleted task verb.** The `H3`/`H4` conversion dropped the worksheet's
  "Solve:", leaving a stem that never said what to do with the inequality.
- **A format line steering toward the wrong answer.** `K6` asks which is greater,
  `1 3/4` or `(1)(3/4)`, then said "no mixed numbers" — pointing away from the
  answer its own key prints, toward the wrong candidate. Pre-existing, never
  checked.
- **The last multi-prompt select-all.** `topic-1-6` Q4 welded the integer `-25`
  to two prose choices under all-or-nothing, in a package whose siblings were
  already numeric.

### A disagreement between judges, resolved by measurement

PERMUTE charged that permuting the choices broke `A1`/`H6`/`H7`; SELECTALL
judged the same items clean. Reading the SVG settled it: each row is drawn as
`"A. open circle at 6, ray right"` — letter **and** description — so matching is
by content and no student can be scored wrong. PERMUTE overstated the harm;
SELECTALL understated the confusion of drawn letters no longer parallel to
checkbox order. Each choice now carries its own row letter, which closes it
either way.

### A judge corrected the coordinator

The brief told judges that 12 of 14 packages are CRLF. It is **2 of 14**. The
false count came from `grep -c $'\r'` in a shell loop where the pattern did not
survive as a carriage return, so an empty pattern matched every line. It had
already been written into `BF-2026-029` as fact. Corrected there.

### Both open questions are now closed — BF-2026-042

- **The twelve `topic-1-4` items stay short answer.** The open family is closed
  by naming the permitted methods in the stem rather than by pinning the operand
  order. Pinning would have closed it too, but at the cost of ruling the answer
  key's own `|-8|+5` method off-form; naming the methods costs nothing and drops
  nothing. The second method is per-item — distances from zero **add** on
  Part 1 Q1, the only item straddling zero, and **subtract** on the other five.
- **`H3`/`H4`/`H5` and the two orderings stay short answer.** F1 was amended to
  turn on whether the accepted set is closed rather than on the answer's shape,
  which is the property that was actually doing the work. Recorded, not silent.

Verified: every accepted string in `topic-1-4` evaluates to its item's true
distance (0 mismatches), and every one falls under a method its own stem names
with every named method reachable (0 closure violations).

### The final round — BF-2026-043 … 046

- **The select-all bar is now enforced as written.** It was `MIN_CHOICES = 7`
  where both the rubric and the plan say seven *distractors*; 26 of 34 items sat
  below the documented bar. 27 distractors authored, gate now counts distractors.
- **A real bug shipped through the gap that hid it** — a `<not>` naming the wrong
  `respident` negates nothing, so 11 new distractors were scored as optional.
  Fixed, and the gate now asserts every non-keyed choice is actually negated.
  Confirmed falsifiable by reintroducing the bug.
- **`topic-1-2` P1Q2** gained its missing integer guard and lost two choices that
  were not outcomes at all.
- **`L1`** now states the completeness criterion it grades against.
- **`verify_canvas_import.py`** makes the import test runnable, with a
  `--dry-run` that proves each assertion fires rather than assuming it does.

### Still open

- **The live Canvas import.** The script exists and self-tests; only running it
  against a real course settles whether conversion preserves meaning. See
  `TEACHER_ACTIONS.md`.
- **`A1`, `H6`, `H7` sit at 6 distractors**, held deliberately until the import
  test confirms their SVGs render. Reported as build warnings, never silent.
- **Two consecutive 10/10 per slice**, this project's acceptance bar, is not yet
  met by any slice.
