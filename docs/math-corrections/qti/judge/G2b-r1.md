# G2b — round 1 judgement

SLICE: G2b          SCORE: 8/10
ITEMS WORKED: 16 of 16     (K10, K11, L1, M1-M6, N1-N7 — none skipped)

Shape B. Package `6th-grade-review-section-2-accuracy-check-qti`,
`zip_sha12 6210434f25ac`. All 16 items are the last 16 of 33 in
`sixth_grade_review_section_2_accuracy_check.xml`. Source matched against the
**updated** worksheet (`6thGradeReviewUpdated.pdf`, page 2), read **rendered**
at 160 dpi, not by text extraction, because sections K and N carry built-up
fractions that `pdftotext -layout` transposes.

Shape B allowances applied as the rubric directs: 7 choices per item is **not**
scored as a defect; the second `<respcondition>` on M3/M4/M5/M6 is **not**
scored as a defect (each is a genuine trailing-zero alternate — see below).

---

## CACHE-TRUNCATION BUG — re-read after correction, slice provably unaffected

The coordinator reported that the original extractor unescaped HTML entities
*before* stripping tags, so an escaped `&lt;` became a real `<` and the
tag-stripper ate everything up to the next `>`, silently truncating 89 of 157
cached stems. This matters more here than anywhere: my central question is
whether a stem promises "all equivalent" forms, and a truncated stem is exactly
what could make me misread that promise.

**I re-read `/tmp/qtiwork/slices/G2b.json` after the rebuild and re-verified
against the raw XML. No finding in this report changes.**

Three checks, each independent:

1. **Rebuilt cache vs. authoritative XML, all 16 items.** I re-extracted each
   `<presentation><material><mattext>` payload from the raw XML non-greedily and
   decoded entities **last** (the correct order), and re-extracted every
   `<response_label>` text the same way. All 16 stems and all 35 choice texts
   match the rebuilt cache exactly — 16/16 OK, zero diffs.
2. **The bug could not have fired here at all.** The item file
   `sixth_grade_review_section_2_accuracy_check.xml` contains **zero `&`
   characters** — no `&lt;`, no `&amp;`, no numeric references, nothing. So
   does `imsmanifest.xml`. There is no escaped content in this package for the
   extractor to mis-order. The escaped comparison operators live in stems with
   inequalities; Section 2 (items I1-N7: geometry, units, factors, decimals,
   fractions) contains no comparison operator in any stem. Section 2 was immune.
3. **My own reading never went through the cache.** Every ruling above was
   worked from a verbatim dump of the raw `<item>` elements, and the
   required/negated split was re-derived by parsing the `<respcondition>` tree
   with `<not>` blocks stripped first — re-run after the rebuild, 16/16
   agreement with the corrected cache.

Item file `sha256[:12] = 290b0264aaf6` at time of judging; package
`zip_sha12 = 6210434f25ac`.

This is the standing rule firing correctly: the instrument was at fault, not
the artifact. Worth recording that it cuts the other way too — the same
suspicion applied to the *packages* would have been wrong here. The packages
are fine.

---

## DEFECTS

**L1 | criterion 2 (true-but-unkeyed choice) | `g6_s2_l1`, `choice_4`**

found:  stem `Factor: 8x + 16 = Enter select all equivalent factored expressions.`
        choice_4 `4(2x + 4)`, currently negated:
        `<not><varequal respident="response">choice_4</varequal></not>`

why:    4(2x + 4) = 4·2x + 4·4 = 8x + 16. It is **exactly** equal to the given
        expression for every x, and it is unambiguously a *factored expression*
        — a whole number multiplied by a sum, i.e. a product. It therefore
        satisfies **both** modifiers the stem imposes ("equivalent" and
        "factored"), and the stem's quantifier is "select **all**". The word
        the stem is missing is "completely" / "using the GCF". Under
        all-or-nothing scoring a student who knows what factoring is, reads
        "select all equivalent factored expressions", and correctly identifies
        4(2x + 4) as a second valid factorisation is marked **zero**. The
        rubric's criterion-2 list names "an alternative valid factorisation"
        explicitly.

        Corroborating the narrow intent: the companion
        (`6thGradeReviewExplanations.pdf`, L1) gives a singular
        `Checked answer: 8(x + 2)` and works it via `GCF of 8 and 16 is 8`.
        But its own definition of the operation is
        `To factor means write a sum as a product (pull out a shared factor)` —
        which 4(2x + 4) satisfies. The intent is GCF factoring; the stem does
        not say so.

fix:    **Narrow the stem, do not key the extra form.** Replace the stem
        `<mattext>` text with:

        `Factor completely by pulling out the GCF: 8x + 16 = Enter select all expressions that are the complete GCF factorisation.`

        Leave the key as `choice_1` required, `choice_2`-`choice_7` negated.
        Under the narrowed stem 4(2x + 4) is correctly excluded: 4 is not the
        GCF of 8 and 16, and the residual 2x + 4 still carries a common factor
        of 2, so the expression is not completely factored.

---

## THE REPAIR DIRECTION — key the extra forms, or narrow the stem?

**Narrow the stem. Do not key additional forms.** This is a corpus-level
ruling, and it applies to every "select all equivalent …" item in this slice.

Three independent reasons:

1. **Criterion 5 (answerability from the assignment).** The worksheet items
   behind this cluster are single-blank fill-ins — `L1. Factor: 8x + 16 = ____`,
   `K10. Commutative: 7 × a = ____`. One blank, one answer. A student working
   from the assignment produces exactly one form.

2. **Criterion 4 (key agreement).** The companion writes a singular
   `Checked answer:` for every one of these (`8(x + 2)`, `a × 7`,
   `b + (3 + 9)`, `x + (5 + 8)`), never an "or" list.

3. **Keying the extra form would create a worse defect than it cures.** These
   are all-or-nothing multi-selects. If `4(2x + 4)` were added to the required
   set, the student who wrote the assignment's own answer `8(x + 2)` and
   selected only that would score **zero**. That converts a defect that
   punishes over-thorough students into one that punishes every ordinary
   student. Narrowing the stem costs nothing and removes the ambiguity at its
   source.

---

## THE FOUR PROPERTY ITEMS — why K10, K11, N5, N6 are NOT defects

The candidate file alleges unkeyed equivalents on all four. I refute all four,
on a principled distinction that also explains why L1 *is* a defect. State it
plainly so the cold judge can test it:

> A modifier that names the **operation used to derive** the rewrite constrains
> the derivation. A modifier that names a **property of the resulting form**
> constrains only the form.

- `select all equivalent **commutative rewrites**` / `**associative rewrites**`
  — "commutative"/"associative" names the derivation. A choice must be
  (a) equivalent, (b) a *rewrite* (something must actually change), and
  (c) obtained by *that* property. Every unkeyed equal-valued choice fails
  (b) or (c).
- `select all equivalent **factored expressions**` — "factored" names a
  property of the result: being written as a product. `4(2x + 4)` has that
  property. Nothing in the stem constrains how it was derived. It is in the
  class. Hence the L1 defect and only the L1 defect.

Worked, choice by choice.

**K10 and N5** — identical items, stem `7 × a`, key `choice_1`. (Both exist in
the source: the worksheet carries `K10. Commutative: 7 × a` *and*
`N5. Commutative: 7 × a` as two separate questions. The duplication is
source-faithful, not a packaging error.)

| choice | value | ruling |
|---|---|---|
| 1 `a × 7` | 7a | KEYED. Correct: factors exchanged. |
| 2 `7 + a` | 7 + a | False. At a = 1: 8 vs 7. Correctly negated. |
| 3 `7a + 0` | 7a | Equal in value, but derived by the **additive identity**, not by commuting factors. Not a commutative rewrite. Correctly negated. |
| 4 `7 × a` | 7a | The given expression verbatim. Nothing is rewritten, so it is not a *rewrite* under any reading. Correctly negated. |
| 5 `a ÷ 7` | a/7 | False (equal only at a = 0). |
| 6 `7 ÷ a` | 7/a | False (equal only at a = ±1; undefined at a = 0). |
| 7 `7(a + 1)` | 7a + 7 | False. |

**K11** — stem `(b + 3) + 9`, key `choice_1`. Original value b + 12.

| choice | value | ruling |
|---|---|---|
| 1 `b + (3 + 9)` | b + 12 | KEYED. Correct: parentheses moved, order preserved. |
| 2 `(b + 9) + 3` | b + 12 | Equal, but reaching it requires **commuting** 3 and 9. Associativity alone cannot produce it. Correctly negated. |
| 3 `b + 12` | b + 12 | Equal, but this is the evaluated sum, not a regrouping. Correctly negated. |
| 4 `(b + 3) + 9` | b + 12 | The original verbatim. Not a rewrite. Correctly negated. |
| 5 `b × (3 + 9)` | 12b | False (equal only at b = 12/11). |
| 6 `(b - 3) + 9` | b + 6 | False. |
| 7 `b + (3 × 9)` | b + 27 | False. |

**N6** — stem `(x + 5) + 8`, key `choice_1`. Original value x + 13. Structurally
identical to K11: `(x + 8) + 5` = x + 13 needs commutation; `x + 13` is the
evaluated sum; `(x + 5) + 8` is the original verbatim; `x × (5 + 8)` = 13x
(false, equal only at x = 13/12); `(x - 5) + 8` = x + 3 (false);
`x + (5 × 8)` = x + 40 (false). Key correct, all six negations correct.

The companion states this intent outright and even anticipates the objection:
K11 — `Writing 9 + (b + 3) would also equal the same value, but the standard
associative rewrite keeps order and only moves parentheses`; N6 —
`Associative moves only the parentheses. Do not reorder into 8 + (x + 5)`.
The distractor sets are built precisely around the order-vs-regroup teaching
point plus an evaluate-it-instead trap. That is deliberate design.

**N7** — the candidate asks me to test the earlier clean ruling. I confirm it
independently. (12 − 4) − 3 = 8 − 3 = **5**. 12 − (4 − 3) = 12 − 1 = **11**.
5 ≠ 11, so subtraction is not associative.

| choice | ruling |
|---|---|
| 1 `No; 5 and 11` | KEYED. Both the conclusion and both values are right. |
| 2 `Yes; both equal 5` | False on conclusion and on the second value. |
| 3 `Yes; both equal 11` | False on conclusion and on the first value. |
| 4 `No; 9 and 5` | Conclusion right, **both** values wrong. Not selectable. |
| 5 `No; 5 and 9` | Conclusion right, first value right, second value wrong (9 ≠ 11). A near-miss distractor, correctly negated — it is not a true statement. |
| 6 `Yes; subtraction is commutative` | False twice over. |
| 7 `No; multiplication used` | False reason; no multiplication appears. |

N7 is clean. The earlier ruling holds.

---

## M2 — A STALE COMPANION, NOT A KEY ERROR. DO NOT "FIX" THIS.

Flagging this prominently because it is a live trap for the next pass.

The QTI stem is `700.32 - 84.67 =` and the key is `615.65`. The companion
`6thGradeReviewExplanations.pdf` (M2) reads
`Question 700.3 − 284.67 = (decimal)` / `Checked answer: 415.63`.

The companion is stale, not the QTI. Confirmed along two independent paths:

1. The **previous** worksheet revision `6thGradeReview.pdf` reads
   `2. 700.3 − 284.67 = (decimal)`; the **updated** revision
   `6thGradeReviewUpdated.pdf` reads `2. 700.32 − 84.67 = (decimal)`. The
   companion is dated 2026-07-29; the updated worksheet 2026-08-04. The
   companion predates the revision.
2. Direct computation: 700.32 − 84.67 = 615.65 (exact, verified in decimal
   arithmetic). The brief names the **updated** worksheet as the source of
   truth, and the QTI matches it.

Changing M2's key to 415.63 would be a serious regression. It stays 615.65.

---

## REMAINING ITEMS — worked

Every value recomputed independently in exact arithmetic (`decimal.Decimal`
and `fractions.Fraction`, not floating point), and every stem checked against
the rendered page 2 of the updated worksheet.

| item | stem (worksheet, rendered) | computed | keyed | ruling |
|---|---|---|---|---|
| M1 | 428.5 + 37.26 | 465.76 | 465.76 | correct |
| M2 | 700.32 − 84.67 | 615.65 | 615.65 | correct (see above) |
| M3 | 18.4 × 12 | 220.8 | 220.8, 220.80 | correct |
| M4 | 168.8 ÷ 8 | 21.1 | 21.1, 21.10 | correct |
| M5 | 4.2 × 1.5 | 6.3 | 6.3, 6.30 | correct |
| M6 | 7.2 ÷ 0.8 | 9 | 9, 9.00 | correct |
| N1 | 1/2 + 1/4 | 3/4 | 3/4 | correct |
| N2 | 5/6 − 1/3 | 3/6 = 1/2 | 1/2 | correct |
| N3 | 5/8 × 4/15 | 20/120 = 1/6 | 1/6 | correct |
| N4 | 7/8 ÷ 1/4 | 7/8 × 4/1 = 28/8 = 7/2 | 7/2 | correct |

On the second `<respcondition>` blocks (M3, M4, M5, M6): each is a
trailing-zero alternate of the first, and each exists for a real reason — the
stem instructs `Enter a decimal rounded to two places`, so a student obeying
the instruction literally types `220.80`, `21.10`, `6.30`, `9.00`. Without the
alternate that obedient student could be marked wrong. This is the good design
the rubric describes, not a defect. M1 and M2 need no alternate because their
answers already carry two decimal places.

On N4: the key is the improper `7/2` and the stem says
`no spaces or mixed numbers`, so `3 1/2` is correctly excluded by the stem's
own instruction rather than silently. Consistent.

---

## STRUCTURE AND MARKUP (criteria 6 and 7) — all 16 items

- `respident="response"` throughout, as Shape B expects. `rcardinality="Multiple"`
  on the five multi-answer items, `Single` on the fill-ins.
- required/negated split is coherent on all five multi-answer items:
  `choice_1` required by a bare `<varequal>`, `choice_2`-`choice_7` each negated
  by `<not><varequal>`. Parsed from the `<respcondition>` tree with `<not>`
  blocks stripped — not by regex over the item, which is the trap that inverts
  this reading.
- No two choices share visible text in any item.
- **Zero** math delimiters of any kind: no `$`, no `\(`, no `\)` in any of the
  16 stems. Operators are literal Unicode `×` and `÷`. Nothing to unbalance.
- No images referenced anywhere in the slice, so the
  `$IMS-CC-FILEBASE$/media/…` hazard does not arise.
- `imsmanifest.xml` carries 4 hrefs, all resolving to the two files that exist
  on disk (`…_accuracy_check.xml`, `assessment_meta.xml`). No dangling
  reference.
- No duplicated instruction block in any stem.

**Considered and explicitly NOT scored as a defect:** the stems read
`… = Enter select all equivalent commutative rewrites.` The `= Enter select all`
juncture is ungrammatical, an artifact of a template joining
`<worksheet prompt> = ` + `Enter ` + `<answer-format instruction>`. It is
uniform across the whole package (K1, K2, K9, K10, K11, L1, N5, N6, N7 all
carry it, as do the `Enter a decimal rounded to two places` fill-ins). It
renders as readable text in Canvas and falls under none of the seven criteria.
House style, not a defect.

---

## CANDIDATES RULED ON

- **K9** (`5 + 8`; `8 + 5`, `13`, `(8 + 5) + 0`, `8 + (5 + 0)` unkeyed) ->
  **OUT OF SLICE.** K9 is item 17 of 33; G2b is the last 16, beginning at K10.
  Not mine to rule on. I note only that the same
  derivation-modifier-vs-form-modifier test set out above should decide it, and
  that under that test `8 + 5` is the *correct* commutative rewrite of `5 + 8`
  while `13` and the `+ 0` forms are not commutative rewrites.

- **K10 / N5** — `7 × a` and `7a + 0` unkeyed -> **REFUTED.** Both are equal in
  value to 7a, but neither is a *commutative rewrite*: `7 × a` is the given
  expression unchanged (no rewrite occurred), and `7a + 0` is derived by the
  additive identity, not by exchanging factors. The stem's modifier
  "commutative" constrains the derivation and excludes both.

- **K11** — `(b + 9) + 3`, `b + 12`, `(b + 3) + 9` unkeyed -> **REFUTED.** All
  equal b + 12, none is an associative rewrite: the first needs commutation of
  3 and 9, the second is the evaluated sum, the third is the original verbatim.
  The companion states this constraint explicitly.

- **N6** — `(x + 8) + 5`, `x + 13`, `(x + 5) + 8` unkeyed -> **REFUTED.**
  Same three failure modes as K11, with x, 5, 8.

- **L1** — `4(2x + 4)` = 8x + 16, a valid non-GCF factorisation, unkeyed ->
  **CONFIRMED.** The single standing defect in this slice. Unlike the property
  items, the stem's modifier "factored" describes the *form* of the result, and
  `4(2x + 4)` is a product, so it is squarely inside the class the stem says to
  select all of. Repair by narrowing the stem, not by keying the form.

- **N7 ruled clean; test that ruling** -> **CONFIRMED CLEAN.** Recomputed
  independently: 5 and 11. Only `choice_1` is a true statement. The near-miss
  `No; 5 and 9` gets the conclusion and the first value right but the second
  value wrong, so it is false as a whole and correctly negated.

---

## CLEAN

K10, K11, M1, M2, M3, M4, M5, M6, N1, N2, N3, N4, N5, N6, N7 — 15 of 16 items
verified with no defect standing: stems match the updated worksheet rendered,
every keyed value recomputed and correct, every non-keyed choice worked and
false (or outside the class the stem defines), structure and markup clean.

L1 carries the one defect.

---

## SCORE JUSTIFICATION

8/10. One confirmed criterion-2 defect (L1 / `choice_4`). It is the gravest
defect class in the rubric — under all-or-nothing scoring it returns zero to
precisely the student who understands factoring best, and it is invisible to
anyone who checks only that the keyed choice is right. That is not roundable
away. The remaining 15 items are correct on the mathematics, faithful to the
updated worksheet, and structurally sound, so the slice does not fall further.
