# G2b — round 2 judgement (re-score after fix)

SLICE: G2b          SCORE: 10/10
ITEMS WORKED: 16 of 16     (K10, K11, L1, M1-M6, N1-N7 — none skipped)

Re-read from the raw XML after the fixer's edit. The single defect found in
round 1 (L1 / `choice_4`) is closed. Nothing else moved. Nothing new stands.

Item file `sha256[:12]`: **b846df5e84b0** (was `290b0264aaf6` at r1).
Package `zip_sha12` of record: `6210434f25ac`.

---

## WHAT CHANGED — verified, not taken on report

I diffed the current XML against a **pre-fix baseline** rather than trusting the
change description. The baseline is the rebuilt slice cache, which I had already
verified byte-exact against the pre-fix XML for all 16 items in r1 (stems,
choice texts, required/negated lists, respcondition counts). That makes it a
clean witness to the prior state.

Result across all 16 items: **exactly one field on exactly one item differs.**

| item | stem | choices | required | negated | n_respcondition | original_answer_ids |
|---|---|---|---|---|---|---|
| L1 | **CHANGED** | identical | identical | identical | identical | identical |
| K10, K11, M1-M6, N1-N7 | identical | identical | identical | identical | identical | identical |

The L1 stem now reads, verbatim from the file:

`Factor completely by pulling out the GCF: 8x + 16 = Enter select all expressions that are the complete GCF factorization.`

Key untouched: `choice_1` required by a bare `<varequal>`; `choice_2` through
`choice_7` each negated by `<not><varequal>`; one `<respcondition>`;
`original_answer_ids` still `choice_1`. All seven `response_label` idents and
texts unchanged, `4(2x + 4)` still present as `choice_4`.

**The five protected items are untouched.** K10, K11, N5, N6 are byte-identical
to baseline on every field. K9 — out of my slice, but the coordinator asked — is
also unchanged: stem still
`Rewrite using the commutative property: 8 + 5 = Enter select all equivalent commutative rewrites.`
with choices `5 + 8`, `8 + 5`, `13`, `8 × 5`, `5 - 8`, `(8 + 5) + 0`,
`8 + (5 + 0)`.

---

## DOES THE NARROWED STEM GENUINELY EXCLUDE `4(2x + 4)`?

Yes — and on two independent grounds, either of which alone suffices. That
redundancy is what makes the repair robust rather than merely lucky.

The class the stem now defines is: *expressions that are **the complete GCF
factorization** of 8x + 16.*

Compute the GCF from the terms, not from the constants alone. Terms are 8x and
16. Factor each: 8x = 2³·x, 16 = 2⁴. The shared part is 2³ = **8**; x is absent
from the second term, so it is not in the GCF. The complete GCF factorization is
therefore **8(x + 2)**, and it is unique — the residual x + 2 has
gcd(1, 2) = 1, so nothing further can be pulled out.

`4(2x + 4)` fails twice:

1. **Not the GCF.** 4 is a common factor of 8x and 16, but it is not the
   *greatest* — 8 is. The stem now says "pulling out the GCF", singular and
   definite.
2. **Not complete.** The residual 2x + 4 = 2(x + 2) still carries a common
   factor of 2. So even setting the GCF aside, the expression is not
   *completely* factored. The stem now says "Factor **completely**" and "the
   **complete** GCF factorization".

`4(2x + 4)` is still exactly equal to 8x + 16 — that has not changed and cannot
change. What changed is that equivalence is no longer sufficient for membership
in the class the stem asks the student to select. The r1 defect existed because
the old stem's two modifiers ("equivalent", "factored") were **both** satisfied
by `4(2x + 4)`. The new stem's modifiers ("complete", "GCF") are **both**
violated by it. The hole is closed from both sides.

---

## DOES ANY OTHER CHOICE BECOME AMBIGUOUS UNDER THE NEW WORDING?

No. I re-worked all seven from scratch against the new stem, and specifically
stress-tested each for admissibility it did not previously have.

| choice | expands to | equal to 8x + 16? | in the new class? | keyed? | agree |
|---|---|---|---|---|---|
| 1 `8(x + 2)` | 8x + 16 | identically | **yes** — factor 8 is the GCF; residual x + 2 is irreducible | required | ✓ |
| 2 `8(x + 16)` | 8x + 128 | never (128 ≠ 16) | no | negated | ✓ |
| 3 `x(8 + 16)` | 24x | only at x = 1 | no | negated | ✓ |
| 4 `4(2x + 4)` | 8x + 16 | identically | **no** — 4 is not the GCF; 2x + 4 not fully reduced | negated | ✓ |
| 5 `8x(1 + 16)` | 136x | only at x = 1/8 | no | negated | ✓ |
| 6 `24x` | 24x | only at x = 1 | no | negated | ✓ |
| 7 `8 + (x + 16)` | x + 24 | only at x = 8/7 | no | negated | ✓ |

Exactly one choice is in the class, and it is the one keyed. Stress tests on the
three choices that are *products* but not equivalent — the only plausible route
to a new ambiguity:

- `x(8 + 16)`: a student would have to believe x is a common factor of 8x and
  16. It is not; 16 contains no x. And 24x ≠ 8x + 16 identically. Excluded twice.
- `8x(1 + 16)`: 8x is not a common factor of 16, and the product is 136x, not
  8x + 16. The near-miss a student might *want* here is 8(1x + 2); this is not
  that. Excluded twice.
- `24x`: a product, but not equal to 8x + 16 identically. Excluded.

**On the dropped word "equivalent".** The new stem no longer contains it, so I
checked whether anything slipped in through that gap. It did not: a
*factorization of* an expression is by definition a product **equal to** that
expression, and the stem names its referent unambiguously in the same sentence
(`Factor completely by pulling out the GCF: 8x + 16 =`). Equivalence is entailed,
not discarded. And it is entailment that does the excluding work on choices 2, 3,
5, 6 and 7 — every one of them fails to equal 8x + 16 identically, so none can
be a factorization of it under any reading.

**On the singular/plural construction.** "select **all** expressions that are
**the** complete GCF factorization" pairs a plural quantifier with a singular
definite description. This is benign: it means "select every choice which is the
complete GCF factorization", and exactly one is. It keeps the multi-select
machinery intact while making the answer set a singleton — which is already the
norm across this package (K10, K11, N5, N6, N7 all have singleton answer sets
under `rcardinality="Multiple"`). Not a defect.

---

## CRITERION 1 (STEM FIDELITY) — CONSIDERED IN FULL, NOT A DEFECT

I have to rule on this deliberately, because the repair changed the
*worksheet-prompt half* of the stem, not just the appended instruction. The
worksheet reads `L1. Factor: 8x + 16 =`; the QTI now reads
`Factor completely by pulling out the GCF: 8x + 16 =`.

**Not a defect, and consistency with my own r1 rulings requires that verdict.**

This package does not copy worksheet prompts — it *systematically expands terse
prompts into full sentences*, and I already accepted that convention in r1 when
I certified K10, K11 and N6 as faithful:

| worksheet (rendered, page 2) | QTI stem | expansion added |
|---|---|---|
| `10. Commutative: 7 × a =` | `Rewrite using the commutative property: 7 × a =` | names the property |
| `11. Associative: (b + 3) + 9 =` | `Rewrite using the associative property: (b + 3) + 9 =` | names the property |
| `6. Associative: (x + 5) + 8 =` | `Rewrite using the associative property: (x + 5) + 8 =` | names the property |
| `1. 428.5 + 37.26 = (decimal)` | `428.5 + 37.26 = Enter a decimal rounded to two places…` | expands `(decimal)` |
| `1. Factor: 8x + 16 =` | `Factor completely by pulling out the GCF: 8x + 16 =` | names the method |

The L1 edit is the same move as the K10/K11/N6 expansions I passed in r1. If
"Commutative:" → "Rewrite using the commutative property:" is faithful, then
"Factor:" → "Factor completely by pulling out the GCF:" is faithful.

The substantive tests are also all satisfied:

- **Numbers unchanged.** 8x + 16, identical to the worksheet.
- **Task unchanged.** The expansion makes explicit what the assignment's own
  answer key already documents. The companion's L1 entry gives a singular
  `Checked answer: 8(x + 2)` and derives it via `GCF of 8 and 16 is 8`. The
  stem now says out loud what the key always assumed.
- **Criterion 5 (answerability) holds.** A student with only the worksheet
  writes 8(x + 2) — the standard 6th-grade response and the one the companion
  teaches — then finds and selects it. The QTI offers no option the assignment
  excludes and keys no answer the assignment excludes.

And the counterfactual is decisive: the alternative to this edit was leaving a
confirmed criterion-2 defect in place. The rubric ranks criterion 2 as the
primary hunt precisely because a wrong outcome "tells a student who got the
question right that they got it wrong". A slightly more explicit stem that keys
correctly beats a verbatim stem that returns zero to the strongest student.

*Out of scope, recorded for the coordinator, not affecting this score:* the
residual looseness now sits in the **worksheet PDF**, whose bare `Factor:` does
not itself say "completely". A student who wrote `4(2x + 4)` on paper is now
told it is not the answer. That is a question about `6thGradeReviewUpdated.pdf`,
not about this QTI package, and I was not asked to score it. Flagging it only so
it is not lost.

---

## THE REST OF THE SLICE — r1 RULINGS RE-CONFIRMED

All 15 non-L1 items are byte-identical to the verified pre-fix baseline on
stem, choices, required, negated and respcondition count. Every r1 finding
therefore stands unchanged. Restated in one line each:

- **K10, N5** (`7 × a`): key `a × 7`. `7a + 0` and `7 × a` are equal in value
  but are not *commutative rewrites* — one is derived by the additive identity,
  the other is the original verbatim. Correctly negated.
- **K11** (`(b + 3) + 9`), **N6** (`(x + 5) + 8`): keys `b + (3 + 9)` and
  `x + (5 + 8)`. The three equal-valued distractors each fail: one needs
  commutation, one is the evaluated sum, one is the original verbatim.
- **N7**: (12 − 4) − 3 = 5, 12 − (4 − 3) = 11, 5 ≠ 11. Only `No; 5 and 11` is
  true. The near-miss `No; 5 and 9` is false on its second value.
- **M1-M6**: 465.76, 615.65, 220.8, 21.1, 6.3, 9 — all recomputed in exact
  decimal arithmetic, all keys correct. The second `<respcondition>` on
  M3/M4/M5/M6 is a genuine trailing-zero alternate (`220.80`, `21.10`, `6.30`,
  `9.00`) protecting the student who obeys "rounded to two places" literally.
  Good design, not a defect.
- **N1-N4**: 3/4, 1/2, 1/6, 7/2 — recomputed in exact rational arithmetic, all
  keys correct.

**M2 remains the standing trap for any later pass: the key is 615.65 and it is
right.** 700.32 − 84.67 = 615.65. The explanations companion's
`Checked answer: 415.63` belongs to the *previous* worksheet revision, which
asked `700.3 − 284.67`. The companion is dated 2026-07-29; the updated worksheet
2026-08-04. Do not "correct" M2.

---

## STRUCTURE AND MARKUP AFTER THE EDIT

Re-checked, because the fixer wrote to the file:

- All three XML files still **parse as well-formed**:
  `sixth_grade_review_section_2_accuracy_check.xml`, `imsmanifest.xml`,
  `assessment_meta.xml`.
- Item count still 33. `<item>` structure intact.
- New L1 stem: zero `$`, zero `\(`, zero `\)`, zero HTML entities, zero
  non-ASCII characters, and no literal parentheses to unbalance. Nothing that
  could render literally in Canvas.
- The package still contains **zero `&` characters** anywhere, so the
  entity-unescape-before-tag-strip bug that corrupted other slices' caches
  remains structurally impossible here.
- Spelling normalisation verified consistent with the corpus: the file now
  contains `factorization` ×2 and `factorizations` ×1, and zero instances of the
  British `factoris-` form. K2's pre-existing stem
  (`Prime factorization of 90 = Enter select all equivalent prime factorizations.`)
  establishes the US spelling; the fixer's change to my draft wording was
  correct and I adopt it.
- `imsmanifest.xml` unchanged: 4 hrefs, all resolving to the two files present
  on disk. No dangling reference.
- No two choices share visible text in any item. No images referenced anywhere
  in the slice.
- The `= Enter select all` template juncture persists in the new stem. Already
  ruled in r1: uniform house style across the whole package, renders as readable
  text, falls under none of the seven criteria. Not a defect.

---

## VERDICT

**10/10.** Every one of the 16 items is worked and no defect stands.

- The one r1 defect (L1 `choice_4`, criterion 2) is closed at its source, and
  closed twice over — `4(2x + 4)` now fails both "GCF" and "complete"
  independently.
- The repair introduced no new ambiguity: exactly one of L1's seven choices is
  in the class the new stem defines, and it is the one keyed.
- No collateral change: 15 of 16 items byte-identical to the verified pre-fix
  baseline, L1 changed in its stem only, key and idents intact, the five
  protected items and out-of-slice K9 untouched.
- Package still well-formed and importable.

Nothing stands.
