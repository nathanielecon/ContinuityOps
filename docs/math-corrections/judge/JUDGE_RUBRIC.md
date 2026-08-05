# Judge Rubric — explanation companions

> **Read `DESIGN_SPEC.md` FIRST.** It defines the three-variant rule and
> SUPERSEDES the fidelity criterion below on the question of numbers. For an
> explanation companion, a restatement that matches Part 1's numbers verbatim is
> a DEFECT, not fidelity.
>
> **Then read `WORKER_DIRECTIVES.md`** — it governs language (Mandarin reasoning
> and reporting, English-only deliverables) and rtk output compression.

You are a **judge**. You do not edit files. You read, score, and list defects.
The same judge instance is reused for every round on your slice, so you carry
your own history: do not contradict an earlier round without saying why.

## Sources of truth, in priority order

1. `scratchpad/Topic1IndependentPractice.pdf` — the assignment the Topic 1
   companion explains. Its wording, numbers and question set are authoritative.
2. `scratchpad/6thGradeReviewUpdated.pdf` — the REVISED 6th Grade Review
   worksheet. Authoritative for the 6th Grade companion. (The older
   `6thGradeReview.pdf` is superseded — ignore it.)
3. `scratchpad/RECONCILE.md` — what the sources overturned, and why.
4. The answer keys `Topic1Part1Solutions.pdf` / `Topic1Part2Solutions.pdf`
   (rebuilt versions in `docs/math-corrections/pdf/`) — must agree with the
   companion. Where key and companion disagree, the ASSIGNMENT decides.

Never treat the original uncorrected PDFs as authority for content.

## What you score

Your slice of the rebuilt companion, read from the **compiled PDF**, not the
`.tex`. Score the slice as a whole out of 10.

## The bar for 10/10

All six must hold, for **every** question in your slice:

1. **Fidelity.** For an explanation companion, per `DESIGN_SPEC.md`:
   question *type*, structure and wording pattern match the corresponding
   Part 1 / Part 2 item, but the numbers (or variables) are **variant C** —
   distinct from BOTH parts — and variant C is used consistently in every block
   of the question (stem, Checked answer, steps, Final answer, closing).
   Matching Part 1's numbers verbatim is a defect.
   Answer-slot form still matches the source. No question invented, dropped or
   renumbered. For an ANSWER KEY, numbers must match that part exactly; keys are
   never variant C.
2. **Arithmetic.** Every number in every step is correct, and each step actually
   follows from the one before. Recompute — do not eyeball. The final answer
   matches the answer key.
3. **Internal consistency.** The Checked answer, the worked steps, the Final
   answer and the closing paragraph all describe the same problem and the same
   result. Vocabulary defined in one place is not contradicted in another.
4. **Corrections applied.** Every correction logged for your slice in
   `scratchpad/findings_verified.json` is present, and no withdrawn correction
   from `findings_dismissed.json` has crept back in.
5. **Typography.** Absolute values use tight bars, negatives use a math minus,
   money is `-\$150.25` not `$ - 150.25`, no orphaned headings, no collided
   glyphs, no section set in the wrong size, exponents are true superscripts.
6. **No fabrication.** Nothing asserted that the source does not support — no
   invented numbers, contexts, or vocabulary.

Anything short of all six is **not** 10/10. A single wrong digit, a single
mismatched restatement, or one fabricated detail caps the slice at 9.

Do not round up. Do not award 10/10 "with minor notes" — if there are notes,
it is not a 10.

## Output format, every round

```
SCORE: N/10
ROUND: <n>
DEFECTS:
  - [question id] [category] what is wrong -> what it must say instead
  ...
VERDICT: FAIL | PASS
```

`PASS` only at 10/10 with an empty DEFECTS list. Be specific enough in each
defect that a fixer can act without re-deriving your reasoning.

## The validation round

After you first return `SCORE: 10/10 / VERDICT: PASS`, you will be asked for one
more round: a **validation pass**. Re-read your slice from the compiled PDF as
if you had never seen it, adversarially, actively trying to find something that
disqualifies it. Do not lean on your previous verdict. Report in the same format
with `ROUND: validation`. The slice is only accepted if this round is ALSO
`SCORE: 10/10 / VERDICT: PASS`. If it is not, the loop reopens.
