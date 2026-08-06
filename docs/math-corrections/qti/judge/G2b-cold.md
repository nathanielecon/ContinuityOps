# G2b — cold validation judgement (independent second read)

SLICE: G2b          SCORE: 10/10
ITEMS WORKED: 16 of 16     (K10, K11, L1, M1-M6, N1-N7 — none skipped)

Shape B. Package `6th-grade-review-section-2-accuracy-check-qti`, items 18-33 of
33 in `sixth_grade_review_section_2_accuracy_check.xml`.

Method: every ruling below was worked from the raw XML with my own extractor
(real tags stripped first via `</?[a-zA-Z][^>]*>`, entities unescaped second) and
from the **rendered** updated worksheet at 160 and 400 dpi. I did not read
`/tmp/qtiwork/slices/*.json` at any point. I formed every ruling before opening
`G2b-r1.md` and `G2b-r2.md`.

Shape B allowances applied as the rubric directs: 7 choices per item is not a
defect; the second `<respcondition>` on M3-M6 is not a defect.

---

## THE THREE QUESTIONS PUT TO ME

### 1. L1 — does the narrowed stem genuinely exclude `4(2x + 4)`?

**Yes, on two independent grounds, and it makes no other choice ambiguous.**

Current stem, verbatim from the file:

    Factor completely by pulling out the GCF: 8x + 16 = Enter select all
    expressions that are the complete GCF factorization.

The GCF, computed from the terms and not the constants alone: 8x = 2^3 · x and
16 = 2^4. The shared factor is 2^3 = **8**; x does not appear in the second term
so it is not in the GCF. The complete GCF factorization is **8(x + 2)**, and it
is unique — the residual x + 2 has gcd(1, 2) = 1, so nothing further comes out.

`4(2x + 4)` = 8x + 16 identically. That is true and it stays true. It fails the
new stem twice:

1. **Not the GCF.** 4 is a common factor of 8x and 16 but it is not the
   greatest; 8 is. The stem says "pulling out **the** GCF" — singular, definite.
2. **Not complete.** The residual 2x + 4 = 2(x + 2) still carries a common
   factor of 2, so the expression is not completely factored. The stem says
   "Factor **completely**" and "the **complete** GCF factorization".

Either ground alone excludes it. That redundancy is what makes the repair robust
rather than lucky: the old stem's two modifiers ("equivalent", "factored") were
both *satisfied* by `4(2x + 4)`; the new stem's two modifiers are both
*violated* by it.

**No other choice becomes newly ambiguous.** Narrowing can only shrink the
admitted class, and I re-worked all seven from scratch against the new wording:

| choice | expands to | equal to 8x + 16 identically? | in the new class? | keyed |
|---|---|---|---|---|
| 1 `8(x + 2)` | 8x + 16 | yes | **yes** — 8 is the GCF, x + 2 irreducible | required |
| 2 `8(x + 16)` | 8x + 128 | no | no | negated |
| 3 `x(8 + 16)` | 24x | no (only at x = 1) | no | negated |
| 4 `4(2x + 4)` | 8x + 16 | yes | **no** — see above | negated |
| 5 `8x(1 + 16)` | 136x | no (only at x = 1/8) | no | negated |
| 6 `24x` | 24x | no (only at x = 1) | no | negated |
| 7 `8 + (x + 16)` | x + 24 | no (only at x = 8/7) | no | negated |

The only route to a new ambiguity would be a choice that is a *product* but was
previously excluded by "equivalent". There are three products among the
distractors (3, 5, 6) and every one of them fails equality with 8x + 16
identically, so none can be a factorization of it under any reading. Exactly one
choice is in the class and it is the one keyed.

I also checked the gap left by dropping the word "equivalent": nothing slipped
through it. A *factorization of* an expression is by definition a product equal
to that expression, and the stem names its referent in the same sentence
(`… : 8x + 16 =`). Equivalence is entailed, not discarded.

**Is narrowing faithful under criterion 1?** Yes — but I reach that verdict on
narrower ground than r2 did, and the difference matters enough to record.

I rendered **both** worksheet revisions. The relevant fact is that this package's
expanded property-item stems are **not** authored expansions at all — they are
the *original* worksheet's own wording, which the update abbreviated:

| item | original worksheet (2026-07-29) | updated worksheet (2026-08-04) | QTI stem |
|---|---|---|---|
| K10 | `Rewrite using the commutative property: 7 × a =` | `Commutative: 7 × a =` | matches **original** verbatim |
| K11 | `Rewrite using the associative property: (b + 3) + 9 =` | `Associative: (b + 3) + 9 =` | matches **original** verbatim |
| N5 | `Rewrite using the commutative property: 7 × a =` | `Commutative: 7 × a =` | matches **original** verbatim |
| N6 | `Rewrite using the associative property: (x + 5) + 8 =` | `Associative: (x + 5) + 8 =` | matches **original** verbatim |
| N7 | `Is subtraction associative? Compare (12 − 4) − 3 and 12 − (4 − 3).` | same | matches both verbatim |
| L1 | `Factor: 8x + 16 =` | `Factor: 8x + 16 =` | **expanded — in neither revision** |

So r2's argument ("the L1 edit is the same move as the K10/K11/N6 expansions I
passed in r1") does not hold as stated: those were never expansions the package
made, they are source text the *worksheet* later shortened. L1 is the only stem
in this slice whose wording appears in no revision of the source. The
consistency argument is therefore unavailable, and the L1 narrowing has to
stand on its own merits.

It does stand, on four grounds:

- **Numbers identical.** `8x + 16`, unchanged from both revisions.
- **The added words state what the source's own key already requires.** The
  companion's L1 entry gives a singular `Checked answer: 8(x + 2)` and derives
  it in step 2 as `GCF of 8 and 16 is 8. (Variable x is only in the first term,
  so it is not part of the GCF.)` The narrowed stem says out loud what the
  answer key always assumed. It narrows *toward* the source's key, not away.
- **Criterion 5 holds.** The worksheet section is `L. Distributive Property And
  Factoring` and L1 is its only item. A student with only the worksheet produces
  8(x + 2) — the answer the companion teaches — then finds and selects it. The
  QTI offers no option the assignment excludes and keys no answer it excludes.
- **The counterfactual is worse both ways.** Keying `4(2x + 4)` alongside
  `8(x + 2)` under all-or-nothing scoring would fail every student who gave the
  assignment's own singular answer — that is criterion 4's "or"-forms defect,
  strictly worse than the defect it cures. Replacing `4(2x + 4)` with a false
  expression would work, but would destroy the single most valuable distractor
  in the item (incomplete factoring is *the* classic error at this level).
  Narrowing closes the hole and keeps the pedagogy.

Ruling: the narrowing is sound, complete, and faithful. Not a defect.

*Recorded, out of scope, not scored:* the residual looseness now sits in
`6thGradeReviewUpdated.pdf`, whose bare `Factor:` still does not say
"completely". A student who wrote `4(2x + 4)` on paper is told by the QTI it is
not the answer. That is a question about the worksheet PDF, not this package.

### 2. K10, K11, N5, N6 — does "the property constrains the derivation" hold?

**It holds. I tested it three ways and it survives all three. Four items, ten
equal-valued unkeyed choices, no defect.**

The reasoning under test is that "commutative rewrite" / "associative rewrite"
constrains how the form was *derived*, not merely what it *equals*. If it fails,
these four items carry true-but-unkeyed choices.

**Test 1 — does the source itself make this distinction?** Decisively yes, and
in the very place it would matter. The companion's own closing remarks:

- K11: `Associative changes grouping, not order. Writing 9 + (b + 3) would also
  equal the same value, but the standard associative rewrite keeps order and
  only moves parentheses.`
- N6: `Associative regroups; it does not reorder. Writing 8 + (x + 5) equals the
  same sum, but the required associative rewrite keeps order and only moves
  parentheses.`
- K10: `This is not the associative property (associative only regroups
  parentheses; commutative switches order).`
- K11 step 2: `List the three addends in order: b, then 3, then 9. Keep that
  order.`

This is the author, inside the answer key, ruling explicitly that value-equality
is **not sufficient** — that an equal-valued alternate is not the required
rewrite. That is the reasoning under test, asserted by the source. It directly
disposes of `(b + 9) + 3` and `(x + 8) + 5`, which are exactly the order swaps
the companion names.

**Test 2 — the governing stem wording.** Under criterion 1 the worksheet is what
governs, and the updated worksheet says only `Commutative: 7 × a = ____` and
`Associative: (b + 3) + 9 = ____`. There is no word "equivalent" in the source at
all. The source asks for a named-property transformation into a single blank —
nothing more. So the strict reading of the QTI's boilerplate "select all
equivalent …" cannot be the governing reading; it would make the words
"commutative" and "associative" inert, which the source's own key forbids.

I considered the rubric's criterion-2 bullet — *for a stem that says "select all
equivalent …": every algebraically equivalent form counts*. It does not bite
here. In that bullet the quantified class is unrestricted. Here the head noun is
restricted: "commutative **rewrites**", "associative **rewrites**". "Equivalent"
is a filter *on* that class, not the class itself.

**Test 3 — the harm model, choice by choice.** Criterion 2's defect is real when
"a student who reasons correctly selects it and scores zero". I worked each of
the ten equal-valued unkeyed choices against that test.

K10 / N5 — stem `7 × a`, key `choice_1` `a × 7`:

| choice | value | ruling |
|---|---|---|
| 1 `a × 7` | 7a | KEYED. Factors exchanged. Correct. |
| 2 `7 + a` | 7 + a | False (at a = 1: 8 vs 7). |
| 3 `7a + 0` | 7a | Equal, but derived by the **additive identity**, not by commuting factors. No correct reasoner offers it as a commutative rewrite. Correctly negated. |
| 4 `7 × a` | 7a | The given expression verbatim. Nothing was rewritten, so it is not a *rewrite* under any reading. Correctly negated. |
| 5 `a ÷ 7` | a/7 | False (equal only at a = 0). |
| 6 `7 ÷ a` | 7/a | False (equal only at a = ±1; undefined at a = 0). |
| 7 `7(a + 1)` | 7a + 7 | False. |

K11 — stem `(b + 3) + 9`, key `choice_1` `b + (3 + 9)`; N6 — stem `(x + 5) + 8`,
key `choice_1` `x + (5 + 8)`. Structurally identical, worked separately:

| choice (K11 / N6) | value | ruling |
|---|---|---|
| 1 `b + (3 + 9)` / `x + (5 + 8)` | b + 12 / x + 13 | KEYED. Parentheses moved, order preserved. Correct. |
| 2 `(b + 9) + 3` / `(x + 8) + 5` | b + 12 / x + 13 | Equal, but reaching it requires **commuting** the two constants. Associativity alone cannot produce it, and the companion names this exact move as not the required rewrite. This is the designed misconception trap. Correctly negated. |
| 3 `b + 12` / `x + 13` | b + 12 / x + 13 | Equal, but this is the **evaluated sum**, not a regrouping. See below. Correctly negated. |
| 4 `(b + 3) + 9` / `(x + 5) + 8` | b + 12 / x + 13 | The original verbatim. Not a rewrite. Correctly negated. |
| 5 `b × (3 + 9)` / `x × (5 + 8)` | 12b / 13x | False (equal only at b = 12/11, x = 13/12). |
| 6 `(b − 3) + 9` / `(x − 5) + 8` | b + 6 / x + 3 | False. |
| 7 `b + (3 × 9)` / `x + (5 × 8)` | b + 27 / x + 40 | False. |

**The close call, stated plainly rather than smoothed over: `b + 12` and
`x + 13`.** This is the only one of the ten that a strong student might
genuinely reach and then select, because it *is* what the keyed regrouping
equals, and it is reachable by applying associativity and then adding. I ruled
it not a defect on three grounds, in order of weight:

1. **The accuracy check's job is to reproduce the assignment's verdict.**
   Students import these "to check their own homework against the Independent
   Practice assignment". A student who wrote `b + 12` on the worksheet would be
   marked against the companion's `Final answer: b + (3 + 9)` too. The QTI
   agreeing with the paper key is the artifact working, not failing.
2. **The companion shows the evaluation as a *check*, not the answer.** Its
   steps 4-5 compute `(2 + 3) + 9 = 14` and `2 + (3 + 9) = 14` and label them
   `Numeric check` / `Check works`; the answer line stops at the regrouped form.
3. **The counterfactual repair is worse.** Keying `b + 12` would contradict the
   companion's singular checked answer (criterion 4) and, under all-or-nothing
   scoring, fail every student who gave only the regrouped form. Replacing it
   would delete the "the answer is a number, not a rearrangement" distractor —
   the misconception this section exists to teach against — and break the
   parallel structure across all four items.

Applying the rubric's weaker class explicitly, as instructed: `b + 12` and
`x + 13` are *true statements of value that answer a different question* (what
does it equal) than the one asked (what is the associative rewrite). I record
them as that weaker class and rule them **not defects**.

**Conclusion: the reasoning does not fail. No true-but-unkeyed choice stands on
K10, K11, N5 or N6.**

*Verified, not assumed:* K10 and N5 are byte-identical items — same stem, same
seven choices, same key. This is **source-faithful**, not a packaging error: the
updated worksheet genuinely asks the same question twice, as `K10. Commutative:
7 × a = ____` and `N5. Commutative: 7 × a = ____`, and the companion carries two
separate entries for them. Confirmed on the rendered page and in the companion.

### 3. M2 — which is stale, the QTI or the companion?

**The companion is stale. The QTI key 615.65 is correct. Do not change it.**
Settled along four independent paths, none of them assumed:

1. **Rendered source, 400 dpi.** The updated worksheet, page 2, section M reads
   `2. 700.32 − 84.67 = ______ (decimal)`. Read as an image, not extracted.
2. **The companion reproduces the stale *question*, not merely a stale answer.**
   Its M2 entry reads `Question 700.3 − 284.67 = (decimal)` — the arithmetic
   there is not wrong, it is a *different problem*. 700.3 − 284.67 = 415.63
   exactly, so the companion is internally consistent and simply obsolete.
3. **Revision history.** The previous worksheet `6thGradeReview.pdf` reads
   `2. 700.3 − 284.67 = (decimal)` — exactly the companion's text. The
   companion and that revision carry the **identical** creation timestamp,
   `2026-07-29 18:51:49 UTC`, i.e. the same build; the updated worksheet is
   `2026-08-04 20:20:40 UTC`. The companion documents the superseded revision.
   M2 is the only item in section M whose numbers changed between revisions.
4. **Direct computation.** 700.32 − 84.67 = 615.65 exactly. The key matches the
   updated worksheet, which the brief names as the source of truth.

Changing M2 to 415.63 would be a serious regression.

---

## DEFECTS

None. No defect stands in this slice.

---

## INDEPENDENT VERIFICATION THAT NOTHING OUTSIDE THE REPAIR MOVED

I did not verify this against a cache. I diffed the current package XML against a
**true pre-fix artifact** — `/home/user/ContinuityOps/inbox/Inbox/6th-grade-review-section-2-accuracy-check-qti.zip`,
mtime 2026-08-05 21:12:26, predating the 2026-08-06 00:01:41 edit — after
normalising line endings and inter-tag whitespace. This covers all 33 items, not
just my 16.

Result: **exactly two changed lines, one removal and one insertion, both the L1
stem.**

    - <mattext texttype="text/html">Factor: 8x + 16 = Enter select all equivalent factored expressions.</mattext>
    + <mattext texttype="text/html">Factor completely by pulling out the GCF: 8x + 16 = Enter select all expressions that are the complete GCF factorization.</mattext>

Nothing else in the file differs: not a choice text, not an ident, not a
`<respcondition>`, not an `original_answer_ids`, not a stem on any of the other
32 items — including out-of-slice K9 and the four protected property items. This
independently confirms r2's central claim by a different instrument than r2 used.

Two further checks:

- The staged zip `/tmp/qtiwork/staged/6th-grade-review-section-2-accuracy-check-qti.zip`
  is **byte-identical** to the package I judged (sha256 `0794528a068af45f…`), so
  what ships is what I read.
- `/home/user/ContinuityOps/docs/math-corrections/qti/zips/…` is already
  identical to the repaired package (zero changed lines), so the repair has
  propagated to the repo copy. Recorded for the coordinator; not a scoring
  matter.

Seeing the pre-fix stem also confirms the original defect was real rather than
inferred: under `select all equivalent factored expressions`, `4(2x + 4)` was
both equivalent and a factored expression, so it satisfied both modifiers under
a "select all" quantifier. The narrowing closes exactly that hole.

---

## MATHEMATICS — ALL 16 ITEMS RE-WORKED FROM THE STEM

Every value computed by me from the stem, then checked against the rendered
updated worksheet and against the companion's `Checked answer`.

| item | stem (updated worksheet, rendered) | my computation | keyed | ruling |
|---|---|---|---|---|
| K10 | Commutative: 7 × a | a × 7 | `choice_1` | correct |
| K11 | Associative: (b + 3) + 9 | b + (3 + 9) | `choice_1` | correct |
| L1 | Factor: 8x + 16 | 8(x + 2) | `choice_1` | correct |
| M1 | 428.5 + 37.26 | 428.50 + 37.26 = 465.76 | 465.76 | correct |
| M2 | 700.32 − 84.67 | 700.32 − 84.67 = 615.65 | 615.65 | correct |
| M3 | 18.4 × 12 | 216 + 4.8 = 220.8 | 220.8, 220.80 | correct |
| M4 | 168.8 ÷ 8 | 21 + 0.1 = 21.1 | 21.1, 21.10 | correct |
| M5 | 4.2 × 1.5 | 6.3 | 6.3, 6.30 | correct |
| M6 | 7.2 ÷ 0.8 | 72 ÷ 8 = 9 | 9, 9.00 | correct |
| N1 | 1/2 + 1/4 | 2/4 + 1/4 = 3/4 | 3/4 | correct |
| N2 | 5/6 − 1/3 | 5/6 − 2/6 = 3/6 = 1/2 | 1/2 | correct |
| N3 | 5/8 × 4/15 | 20/120 = 1/6 | 1/6 | correct |
| N4 | 7/8 ÷ 1/4 | 7/8 × 4/1 = 28/8 = 7/2 | 7/2 | correct |
| N5 | Commutative: 7 × a | a × 7 | `choice_1` | correct |
| N6 | Associative: (x + 5) + 8 | x + (5 + 8) | `choice_1` | correct |
| N7 | Is subtraction associative? | (12−4)−3 = 5; 12−(4−3) = 11; 5 ≠ 11 → No | `choice_1` `No; 5 and 11` | correct |

N4's `7/2` was settled by **rendering** the companion page (p.50), not by text
extraction, because a built-up 7-over-2 is exactly the fraction the instrument
transposes. The render confirms `Final answer: 7/2`, and the companion's own
aside `7/2 = 3½` is closed off by the QTI stem's `no mixed numbers`, so the
mixed-number alternate is excluded by instruction rather than silently.

**N7, all seven choices worked** (the candidate file asked for this ruling to be
retested; I recomputed rather than inherited it):

| choice | ruling |
|---|---|
| 1 `No; 5 and 11` | KEYED. Conclusion and both values correct. |
| 2 `Yes; both equal 5` | False on the conclusion and on the second value. |
| 3 `Yes; both equal 11` | False on the conclusion and on the first value. |
| 4 `No; 9 and 5` | Conclusion right, both values wrong. False as a whole. |
| 5 `No; 5 and 9` | Conclusion right, first value right, second wrong (9 ≠ 11). False as a whole. Near-miss, correctly negated. |
| 6 `Yes; subtraction is commutative` | False twice over. |
| 7 `No; multiplication used` | Conclusion right, reason false — no multiplication appears. False as a whole. |

Choices 4, 5 and 7 pair a correct verdict with a false justification. I ruled
them false because all seven choices share the form `verdict; justification`, so
the justification is part of the claim, and the stem asks for `correct
conclusions`. A fully correct option (`choice_1`) is available, so no correct
reasoner is forced onto a partially-true one.

---

## STRUCTURE AND MARKUP (criteria 6 and 7)

- Scoring trees parsed from the `<respcondition>` element with `<not>` blocks
  stripped **before** collecting `<varequal>`, not by flat regex. On all five
  multi-answer items the split is coherent: `choice_1` required by a bare
  `<varequal>`, `choice_2`-`choice_7` each negated inside `<not>`.
  `respident="response"` throughout, matching `<response_lid ident="response">` /
  `<response_str ident="response">`.
- `rcardinality="Multiple"` on the five multi-answer items, `Single` on the ten
  fill-ins. `render_fib fibtype="Decimal"` on M1-M6, `"String"` on N1-N4.
- No two choices share visible text in any item.
- All three XML files parse as well-formed (ElementTree): item file, manifest,
  `assessment_meta.xml`. 33 `<item>` elements. `points_possible` 33 = 33 × 1.
- `imsmanifest.xml` declares two resources and both hrefs resolve to files
  present on disk. No dangling reference.
- Zero math delimiters anywhere in the package: no `$`, no `\(`, no `\)`. Zero
  `&` characters, so zero HTML entities — the unescape-before-strip trap is
  structurally impossible here. The only non-ASCII characters in the entire file
  are `×` and `÷`. No images referenced, so the `$IMS-CC-FILEBASE$/media/…`
  hazard does not arise. No duplicated instruction block in any stem.

**Examined and ruled NOT defects** — stated so a later pass does not rediscover
them and misfile them:

- **The second `<respcondition>` on M3-M6** is a trailing-zero alternate
  (`220.80`, `21.10`, `6.30`, `9.00`), as the rubric describes. I inspected the
  full condition tree rather than the count: each block is
  `<or><varequal>v</varequal><and><vargte>v</vargte><varlte>v</varlte></and></or>`.
  Because the numeric `vargte`/`varlte` range is present, Canvas already matches
  trailing-zero variants numerically, so these second blocks are **redundant
  rather than load-bearing** — a slightly weaker claim than r1/r2 made, but the
  ruling is the same and stronger for it: they are harmless defensive
  duplication, and they close the apparent gap that M6 keys `9` and `9.00` but
  not `9.0` (the range matches it).
- **`original_answer_ids` is `choice_1` on all fifteen numerical and nine
  short-answer items, while the actual `<response_label>` ident is `answer1`.**
  Neither earlier report examined this. It is not import-blocking and does not
  affect scoring: `original_answer_ids` is a Canvas export round-trip hint and
  Canvas mints fresh answer IDs on import, while scoring runs off
  `<respcondition>` against `respident="response"`, which resolves correctly. It
  is uniform across the whole package. Not a defect.
- **The `= Enter select all …` template juncture** is ungrammatical, an artifact
  of joining `<worksheet prompt> = ` + `Enter ` + `<answer-format instruction>`.
  It is uniform across all 33 items in this package and across the companion
  package, predates the repair, renders as readable text in Canvas, and falls
  under none of the seven criteria. House style, not a defect.
- **The singular/plural construction** in L1's new stem — "select **all**
  expressions that are **the** complete GCF factorization" — pairs a plural
  quantifier with a singular definite description. Benign: it means "select every
  choice which is the complete GCF factorization", and exactly one is. Singleton
  answer sets under `rcardinality="Multiple"` are already the norm here (K10,
  K11, N5, N6, N7 all have them). Not a defect.

---

## CANDIDATES RULED ON

- **K10 / N5** — `7 × a` and `7a + 0` unkeyed -> **REFUTED.** Both equal 7a, but
  neither is a commutative rewrite: `7 × a` is the given expression unchanged, and
  `7a + 0` is derived by the additive identity. The property name constrains the
  derivation, and the companion asserts that constraint itself.
- **K11** — `(b + 9) + 3`, `b + 12`, `(b + 3) + 9` unkeyed -> **REFUTED.** All
  equal b + 12; the first requires commuting 3 and 9, the second is the evaluated
  sum, the third is the original verbatim. The companion names the first of these
  explicitly as not the required rewrite.
- **N6** — `(x + 8) + 5`, `x + 13`, `(x + 5) + 8` unkeyed -> **REFUTED.** Same
  three failure modes, worked separately with x, 5, 8.
- **L1** — `4(2x + 4)` = 8x + 16, a valid non-GCF factorisation, unkeyed ->
  **CONFIRMED as a defect against the pre-fix stem, CLOSED by the repair.** I
  verified the pre-fix stem from the inbox artifact rather than taking the r1
  report's word for it; under `select all equivalent factored expressions` the
  choice satisfied both modifiers and the defect was real. Under the current stem
  it fails both "GCF" and "complete". Closed at source.
- **N7 ruled clean; test that ruling** -> **CONFIRMED CLEAN.** Recomputed from
  the stem: 5 and 11. Only `choice_1` is true as a whole statement.
- **K9** -> **OUT OF SLICE** (item 17 of 33; G2b begins at K10). I confirmed only
  that it is byte-unchanged from the pre-fix artifact.

## DISAGREEMENTS WITH THE EARLIER REPORTS

Both r1 and r2 reach conclusions I independently reached, and I overturn neither
verdict. One argument I do correct:

- **r2's criterion-1 argument for L1 is not sound as written.** It justifies the
  L1 stem expansion by consistency with the K10/K11/N6 expansions it passed in
  r1. But those are not expansions this package made — they are the *original*
  worksheet's own wording, which the 2026-08-04 revision shortened. L1's
  `Factor: 8x + 16 =` is identical in **both** revisions, so the L1 stem is the
  only one in the slice with no source attestation, and the consistency argument
  is unavailable. The verdict (faithful, not a defect) survives on the four
  independent grounds set out in section 1 above, so the score is unaffected —
  but the reasoning needed replacing, not ratifying.
- **r1 and r2 describe M3-M6's second `<respcondition>` as protecting the student
  who types `220.80`.** The `vargte`/`varlte` numeric range in the *first* block
  already does that. The blocks are redundant, not protective. Same ruling, more
  accurate basis, and it disposes of the `9` / `9.00` / no-`9.0` asymmetry on M6.

---

## CLEAN

K10, K11, L1, M1, M2, M3, M4, M5, M6, N1, N2, N3, N4, N5, N6, N7 — all 16 items
verified with no defect standing.

Every stem checked against the rendered updated worksheet; every keyed value
recomputed from the stem; every one of the 35 non-keyed choices worked and found
false, or found outside the class the stem defines with the exclusion argued;
structure parsed from the response-processing tree; markup and manifest clean;
the whole 33-item file diffed against a true pre-fix artifact.

## SCORE

**10/10.** Every item in the slice was worked and no defect stands. The one
repair in this package's history closes its defect at the source rather than
displacing it, introduces no new ambiguity in the repaired item, and touches
nothing else in the file.
