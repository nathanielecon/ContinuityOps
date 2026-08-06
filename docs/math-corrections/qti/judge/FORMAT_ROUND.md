# Frozen gate — answer-format round

This file is the gate. It does not change between judges or between rounds of
this batch. If you believe it is wrong, say so in your report and score against
it anyway; you do not have authority to relax it, and neither does the
coordinator once the round has started.

## You are a judge

You score. You do **not** edit any file. Editing disqualifies your verdict. A
separate fixer applies changes. Run at high effort.

Read `judge/JUDGE_RUBRIC_QTI.md` first — the seven criteria and the two
structural shapes still hold and are still the rubric. This file adds the rule
that was applied to the corpus in this round and tells you how to score against
it. Where the two conflict, this file wins for the items in your scope only.

## The author's rule, applied this round

> Numeric entry is the default. One part per question. No units in the answer.
> The stem states the format of the number expected. Select-all survives only
> where the answer genuinely is not a number.

Concretely, an item passes the format gate only if **all** of these hold.

**F1 — Type is right for the answer.** If the answer is a single number, the
item is `numerical_question`.

If the answer is an expression, an inequality, an ordering, or a comparison
statement, the deciding question is **whether the accepted set is closed**:

- **Closed** — the stem names the permitted method or methods, and every string
  a student following that stem can produce is in the accepted list. Then
  `short_answer_question` is correct, and forcing select-all would be the
  defect: it puts the answer on screen for an item whose whole point is that the
  student writes it.
- **Open** — the stem admits a family of correct answers it does not delimit
  ("write an expression that uses absolute-value bars"). Then it stays
  `multiple_answers_question`. An open set cannot be enumerated, so short answer
  will mark some correct student wrong, and widening the list is not a fix —
  each widening round only reveals more forms still rejected.

A graph description or a justification is always `multiple_answers_question`;
prose has no closed form.

An item that could be answered by typing one number but is still select-all is a
defect. So is a numeric-entry item whose answer is not a number.

*Amended mid-round — see BF-2026-042.* The original text said every expression
or inequality "stays `multiple_answers_question`", full stop. That rule was
written before this corpus had a third question type, and under it the judge
correctly flagged `H3`/`H4`/`H5` and the two orderings whose accepted sets it had
itself just certified **complete**. Closure, not answer shape, is the property
that actually matters.

**F2 — One part per item.** No item may contain both a "Part A" and a "Part B"
prompt. No item stem may reference a part label at all.

**F3 — No units in the accepted answer.** The scored value is a bare number:
digits, an optional leading `-`, an optional decimal point. No unit word, no
degree sign, no `n =`, no currency symbol, no direction word.

**F4 — The stem states the format.** The accuracy-check paragraph names what
kind of number to type — integer / whole number / decimal, the rounding if any,
and the sign convention if the answer can be negative. A student must be able to
tell from the stem alone what to type.

**F5 — The format statement is true.** This is the criterion most likely to
catch a real defect, so work it rather than skim it. If the stem says "integer"
the keyed value must be an integer. If it says "round to the nearest kilometer"
the keyed value must be that rounding of the true quotient, computed by you from
the stem's own numbers. If it says "use a negative sign for a descent" the keyed
value for a descent must be negative. A sign convention stated in the stem but
contradicted by the key is the worst defect available here, because it fails
precisely the student who read the instruction.

**F6 — Recompute the key.** Do not accept a keyed value because it matches the
choice text it replaced, and do not accept it because it matches the answer key
PDF. Work it yourself from the stem, then check it against the PDF, and report
any disagreement between the three as a defect naming which two agree.

**F7 — Nothing lost in a split.** Where one item became two, every part of the
original stem must survive into exactly one of the halves, each half must be
answerable on its own without the other, and the intro context must appear in
both. A half that cannot be answered without having read its sibling is a defect.

## Scoring

Score /10 on the seven rubric criteria **and** F1-F7 together. No rounding up.
No "10/10 with minor notes" — a note is a defect or it is not.

A slice passes only at **10/10**. Anything less returns to the fixer and is
re-judged; there is no partial acceptance and no "accept with follow-up".

## Read the raw XML

Authoritative source for this round:

- changed corpus: `<WORK>/` (given in your scope)
- pristine pre-change corpus: `<BASE>/` — use it to see exactly what an item
  looked like before, and to confirm nothing was lost

Do not trust any cache or extracted JSON. If you write an extractor, **strip
real HTML tags first, unescape second**, and match only `</?[a-zA-Z][^>]*>` as a
tag — a bare `<` before a space or a digit is text, not markup. Judges have hit
that trap repeatedly on this corpus. Note that these stems are double-escaped:
the mattext body holds `&lt;p&gt;` sequences, so one unescape pass yields HTML
and a second yields text.

## Sources

| What | Where |
|---|---|
| Assignment (Topic 1) | `docs/math-corrections/source/Topic1IndependentPractice.pdf` |
| Part 1 key | `docs/math-corrections/pdf/Topic1Part1Solutions.pdf` |
| Part 2 key | `docs/math-corrections/pdf/Topic1Part2Solutions.pdf` |
| 6th Grade worksheet | `docs/math-corrections/source/6thGradeReviewUpdated.pdf` |

All paths relative to `/home/user/ContinuityOps`.

`pdftotext -layout` **transposes** built-up fractions: a correct `4/7 = ?/21`
extracts as `47 = 21 / ?`. Settle any fraction by rendering the page, never by
extraction order.

## Report format — English only

```
SLICE: <id>          SCORE: n/10
ITEMS WORKED: <count> of <count>     (list any you could not work, and why)

DEFECTS
  <item title> | <criterion: 1-7 or F1-F7> | <ident or location>
    found:  <exact text>
    why:    <the mathematics, worked>
    fix:    <the exact replacement text, or the exact structural change>

CLEAN
  <item titles verified with no defect>
```

Report `SCORE: 10/10` only when every item in your scope is worked and no defect
stands.
