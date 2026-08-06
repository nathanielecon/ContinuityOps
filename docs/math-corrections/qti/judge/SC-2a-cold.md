# SC-2a — cold validation

SLICE: SC-2a (topic-sc-2, Part 1 items only)          SCORE: 10/10
ITEMS WORKED: 12 of 12     (none skipped)

Read cold from the raw XML at
`/tmp/qtiwork/pkg/topic-sc-2-independent-practice-accuracy-check-qti/topic_sc_2_independent_practice_accuracy_check/topic_sc_2_independent_practice_accuracy_check.xml`.
The slice cache was not opened. `r1`/`r2` were read only after the twelve items,
both source PDFs and the full pre/post diff had been worked; the rulings below
were reached before that reading and two of them correct the prior record.

Shape A confirmed on all 12.

---

## METHOD

Extractor written per the brief: real tags stripped with `</?[a-zA-Z][^>]*>`
only, entity unescaping second, so no stem could be truncated at a bare `<`.
Cross-checked: the file contains zero `&amp;lt;`, zero `&amp;gt;`, zero `$`,
zero non-ASCII bytes, so the entity trap has no purchase here in either
ordering. Scoring was read by parsing each `<respcondition>` tree and lifting
`<not>` blocks out *before* collecting bare `<varequal>`, never by a flat regex.

Both PDFs were read **rendered**, not extracted. `pdftotext -layout` does
transpose the built-up fractions in this document — assignment Q5 extracts as
`Simplify: 442 · 40 · 4−1` and key Q7 extracts as `Answer: 46 1 / 9 or 5 9` —
so every fraction below is settled from the rendered page:

- assignment `Topic1IndependentPractice.pdf` page 4, Lesson SC-2, **Part 1
  column** (Part 2 column read too, to prove no contamination)
- key `docs/math-corrections/pdf/Topic1Part1Solutions.pdf` page 6 (Q1–Q11) and
  page 7 (Q12)

Choice values were compared as exact `Fraction`s, never as decimals.

Baseline for "nothing else moved": the untouched original package in the repo,
`/home/user/ContinuityOps/inbox/Inbox/topic-sc-2-independent-practice-accuracy-check-qti.zip`,
diffed line-for-line against the repaired file. That diff is reproduced below
and is the authority for what the three repairs actually are.

CJK detector self-tested against a known Han/Kana/Hangul string (it returned
True) before any clean result from it was trusted; Python regex over the
decoded text file, not the zip. The package file is clean of CJK, and this
report is English only.

---

## THE THREE REPAIRS, AS THE DIFF ACTUALLY SHOWS THEM

Full-file diff of original vs. repaired. In Part 1 there are exactly three
changed lines, and nothing else in the file's Part 1 region differs:

1. `sc_2_part_1_question_4_wrong_7`  `<p>1 exactly</p>` -> `<p>1/7</p>`
2. Part 1 Question 7 stem: `...complete correct answer.` ->
   `...complete correct answer, including every equivalent form of that answer.`
3. Part 1 Question 11 stem: the same clause inserted.

Two further changes exist outside this slice and are SC-2b's to score:
`sc_2_part_2_question_4_wrong_7` `1 exactly` -> `25`, and the same clause added
to the Part 2 Question 7 stem. `assessment_meta.xml` and `imsmanifest.xml` are
byte-identical to the original. No ident, no `<respcondition>`, no
`original_answer_ids`, no choice count anywhere in the file was altered.

---

## THE VALUES, RECOMPUTED FROM THE STEMS

Worked from the QTI stem text independently, then matched against the rendered
key. Every one agrees.

| Q | stem (from the QTI) | worked | key p.6/7 |
|---|---|---|---|
| 1  | \(3^{2}\times 3^{4}\) sq in | 3^(2+4) = 3^6 = 729 | 729 square inches |
| 2  | 2^4 cupcakes among 2^2 friends | A: 2^4/2^2 ; B: 16÷4 = 4 | Part A: 2^4/2^2 (or equivalent); Part B: 4 |
| 3  | \((4^{3})^{2}\) | 4^(3·2) = 4^6 = 4096 | 4096 |
| 4  | \(7^{0}\) | 1 | 1 |
| 5  | \(\frac{4^5}{4^2}\cdot 4^0\cdot 4^{-1}\) | 4^3·1·4^-1 = 4^2 = 16 | 16 |
| 6  | \((2^3)^2(3\cdot2)^2\div(\frac{12}{2})^2\) | 64·36÷36 = 64 | 64 |
| 7  | \(5^0+3^{-2}+\frac{2^6\cdot2^3}{2^7}\) | 1 + 1/9 + 2^2 = 1+1/9+4 = **46/9** | 46/9 or 5 1/9 |
| 8  | \(\frac{7^4}{7^2}\cdot 7^0\) | 7^2·1 = 49 | 49 |
| 9  | \((3^2)^3\) | 3^6 = 729 | 729 |
| 10 | \((2\cdot5)^3\) | 10^3 = 1000 | 1000 |
| 11 | \(6^{-2}+(\frac{8}{4})^3\) | 1/36 + 8 = 1/36 + 288/36 = **289/36** | 289/36 or 8 1/36 |
| 12 | \(3^4\cdot 3^2\) | 3^(4+2) = 3^6 = 729 | 729 |

**Criterion 1.** All 12 stems carry the Part 1 numbers. No Part 2 value
(2^3×2^5, 3^4 muffins among 3^2, (2^4)^2, 5^0, 5^5/5^2, (18/3)^2, 2^0+2^-3,
10^5/10^3, (4^2)^2, (2·3)^2, (15/3)^2, 5^3·5^2) appears in any Part 1 item.

Ruled on explicitly, because neither prior report addressed it: three Part 1
stems are prose expansions of the assignment's terse wording rather than
verbatim copies — Q1 ("A person is designing a rectangular poster…" for "Poster
area is given by 3^2 × 3^4 in²"), Q2, and Q3, which adds "using the
power-of-a-power property" to a bare "Evaluate: (4^3)^2 =". **Non-defect.**
Numbers, units and the task asked are preserved exactly in all three; Q3's added
clause names the property the key itself applies (4^{3·2}) and changes neither
the question nor the answer. Criterion 1 governs wording *and numbers for the
right Part*; the numbers are exact and the wording is an expansion, not a
substitution.

**Criteria 2 and 3, mechanically.** Every choice on all 12 items parsed to an
exact `Fraction` and compared against the truth recomputed from the stem, then
"value equals truth" compared against "ident is in the required set". Zero
mismatches: no keyed choice is false, no unkeyed choice is true. The only
value collisions in the whole slice are Q7 `46/9`=`5 1/9` and Q11
`289/36`=`8 1/36`, and in both cases **both** members are keyed — so no
equivalent form sits unkeyed anywhere in the slice.

**Criterion 6, structurally.** All 12: exactly one `<respcondition>`,
`respident="response1"`, `rcardinality="Multiple"`, 8 choices, required set ==
the `correct_*` idents, negated set == the `wrong_*` idents, `<not>` wrapper on
every `wrong_*` and on nothing else, `original_answer_ids` matching the
`response_label` sequence exactly in order and count, no duplicate visible text
within any item.

*Correction to the record:* both r1 and r2 describe the respcondition as
carrying `maxvalue="100"`. It does not. The respcondition carries
`<setvar action="Set" varname="SCORE">100</setvar>`; `maxvalue="100"` lives on
`<decvar>` in `<resprocessing><outcomes>`. This is a misdescription in the two
reports, not a fault in the package: the corpus is uniform on this at 163/163
`setvar action="Set" varname="SCORE"` across all 14 packages, and the all-or-
nothing semantics the rubric describes are exactly what the tree implements.
I record it because a later reader grepping for `maxvalue` inside
`<respcondition>` will find nothing and may misread that as a structural defect.

**Criterion 7.** `\(...\)` balanced in every single `<mattext>` (checked per
element, not per item); zero `$`; zero `\[`/`\]`; exactly one "Canvas accuracy
check" instruction block per item, so no duplicated instruction block; zero
image references, so the `$IMS-CC-FILEBASE$` hazard cannot arise. File parses
under ElementTree; 24 items, 24 respconditions, 192 response_labels. Manifest
declares both resources with matching hrefs and a well-formed dependency.

---

## THE CONTESTED REPAIR — Q7 and Q11

The key writes `46/9 or 5 1/9` and `289/36 or 8 1/36`. Both forms appear as
choices and **both are required** by bare `<varequal>` in the single
all-or-nothing respcondition. The repair did not touch the key; it amended the
stem to "…complete correct answer, **including every equivalent form of that
answer**."

**Ruling: the amendment CLOSES the defect. It is not a relabel.**

I did not take that on the fixer's argument. Here is the argument tested.

### Test 1 — does de-keying one form really create a true-but-unkeyed choice?

Yes, and this is not a rhetorical move. Suppose `sc_2_part_1_question_7_correct_2`
were moved into a `<not>`. `5 1/9 = (5·9+1)/9 = 46/9` exactly — the identical
rational, not an approximation. A student who simplifies to 46/9, converts, and
ticks both then scores zero. That is criterion 2's **first enumerated bullet**,
"an equivalent or unsimplified fraction, or a mixed/improper pair", verbatim.
And it is the more likely failure of the two, because the key's own worked line
*ends* at `5 1/9` ("Thus 1 + 1/9 + 4 = 5 1/9") before the Answer line lists
`46/9` first — a student following the solution's own reasoning arrives at the
mixed number last. So the argument holds: de-keying alone trades a criterion-4
defect for a criterion-2 defect. It does not close anything.

Note this holds independently of ident bookkeeping. Renaming the de-keyed ident
to `wrong_7` (free on both items) would preserve the corpus-wide
`key == correct_*` invariant, but the visible text would still be a true value,
so the criterion-2 defect stands either way.

### Test 2 — were the other repair routes actually available?

- **Accept either form via a second `<respcondition>`.** This is the mechanism
  the rubric blesses elsewhere ("deliberate trailing-zero or equivalent-form
  alternates (3.6 / 3.60). That is good design") — but that blessing is written
  for Shape B. Shape A's criterion 6 requires *exactly one* respcondition, so
  taking this route would itself score a structural defect. Route closed.
- **Delete one form from the choice list.** Drops the item to 7 choices,
  breaking "≥8 choices", so it requires inventing a replacement distractor.
  r1 proposed one for each: `9/46` for Q7 (which is in fact safe — 9/46 ≈ 0.1957,
  no collision) and **`8 2/36` for Q11, which is defective**. 8 2/36 = 8 + 1/18
  = 145/18 = 290/36, and `290/36` is already present as
  `sc_2_part_1_question_11_wrong_6`. That alternative would have created two
  choices with the same value in one item. r1 even states the equality at its
  own line 148 and proposed the fix anyway. It was never applied, so this is
  not a package defect — but it is direct evidence that the "delete a form"
  route carried live risk and that the route taken was the safer one.

So the amendment was not one option among several equals; it was the only route
that satisfies all seven criteria at once.

### Test 3 — does the amendment change the question, or only the label?

It changes the question. The pre-amendment stem, "Select every choice that
belongs in complete correct answer", is genuinely ambiguous about whether a
second spelling of one number "belongs". The amended stem is not. That converts
the item from "state the answer" — where the key's "or" makes either form
sufficient and demanding both is unfair — into "identify every listed choice
equal to the answer", where two choices belong and selecting both is simply
following the instruction.

That second question is legitimate for this instrument and is already what every
other item asks. On Q2 a student who computes Part A and Part B correctly but
ticks only Part A scores zero, and nobody calls that a defect, because the stem
told them to select every choice that belongs. Q7 and Q11 are now structurally
identical to Q2: two choices belong, and the stem says so.

The honest caveat, stated rather than smoothed over: after the amendment a
student who ticks only `46/9` still scores zero. The harm is not abolished, it
is made derivable and therefore deserved. I judge that sufficient — criterion 5
asks that the keyed set be *producible* by a student holding only the
assignment, not that every partial response earn credit — and the conversion the
item now also demands (improper ↔ mixed) is a grade-4/5 skill, well below this
lesson, performed by the solution PDF itself. Answerable.

The key's "or" is honoured in the only sense that survives translation to a
select-all instrument: it governs what the student may have *written* on their
homework, and both writers are now routed to the same full-credit selection.

### Test 4 — does the amended stem create NEW exposure?

This is the sharpest question the brief raises, and it is the right one: a stem
promising "every equivalent form" makes any unkeyed equivalent a far worse
defect than before, because the stem now *invites* the student to look for one.
Checked exhaustively with exact rational arithmetic on both items.

**Q7, answer 46/9.** Unkeyed choices and their exact values:

| choice | exact value | vs 46/9 |
|---|---|---|
| 46/8 | 23/4 = 5.75 | 46·4=184 vs 23·9=207 — unequal |
| 5 4/9 | 49/9 | unequal |
| 5 9/46 | 239/46 | 239·9 = 2151 vs 46·46 = 2116 — unequal |
| 46 | 46 | unequal |
| -46/9 | -46/9 | unequal (sign) |
| 47/9 | 47/9 | unequal |

**Q11, answer 289/36.** Unkeyed choices:

| choice | exact value | vs 289/36 |
|---|---|---|
| 288/36 | 8 | unequal |
| 8 1/35 | 281/35 | 281·36 = 10116 vs 289·35 = 10115 — unequal by 1/1260 |
| 289/35 | 289/35 | unequal |
| 36/289 | 36/289 | unequal (reciprocal) |
| -289/36 | -289/36 | unequal (sign) |
| 290/36 | 145/18 | unequal |

No unkeyed equivalent exists on either item. The new exposure is real in
principle and empty in fact. The `8 1/35` case is the one that mattered: it is
unequal by 1/1260, and a decimal check to three places (8.0286 vs 8.0278) is
uncomfortably close to a false positive — settled here by cross-multiplication,
not by float.

Sweeping wider, since the clause makes equivalence the live question: the exact-
Fraction pass over all 96 Part 1 choices found value collisions on exactly two
items, Q7 and Q11, and on both the colliding pair is entirely inside the keyed
set. There is no unkeyed equivalent anywhere in the slice.

### Test 5 — is the targeted application (2 items amended, 10 not) a defect?

No. The clause is owed only where a second form of the keyed value is actually
in the choice list. Q7 and Q11 are the only two Part 1 items where that is true
— established by the collision sweep above, not by inspection. Adding the clause
to the other ten would promise a selection that does not exist there. The
differential wording does mildly cue that Q7 and Q11 have more than one correct
choice; that is a test-craft observation, not one of the seven criteria, and it
is harmless on a self-check instrument.

---

## THE Q4 REPLACEMENT — `1/7`

Confirmed on both halves of the question the brief poses.

**False for 7^0: yes.** 7^0 = 1 by the zero-exponent property (key p.6: "We
Solve: 7^0 = 1 / Answer: 1"). 1/7 = 7^{-1} ≈ 0.142857. 1/7 ≠ 1. Note this is
not even the weaker "true statement answering a different question" case that
criterion 2 asks to be recorded separately: the choice is a bare value, not a
statement, and as a value it is simply not the answer. It is a clean false
distractor, and a well-chosen one — 7^{-1} is the precise misconception a
student confusing the zero and negative exponent rules produces at this lesson.

**Collides with nothing: confirmed.** Q4's eight choices are `1`, `-1`, `2`,
`0`, `3`, `10`, `7`, `1/7` — eight distinct visible strings and, as exact
rationals, eight distinct values (1, -1, 2, 0, 3, 10, 7, 1/7). No duplicate
text, no duplicate value. In particular 1/7 does not collide with `7` or with
`1`, the two it sits closest to typographically.

**And the defect it replaced was real.** The original text was `1 exactly`,
against a keyed `1`. Criterion 2 lists "the same value restated (`1 exactly`
vs `1`)" as a defect by name. The string `1 exactly` now occurs zero times in
the file.

---

## DEFECTS

None. All three repairs close what they were meant to close, and no repair
displaced a defect rather than closing it.

## CANDIDATES RULED ON

- **Q7/Q11 both forms keyed against an "or" key; repaired by stem amendment
  rather than by changing the key** -> **CLOSED.** The amendment changes what
  the item asks, and the changed ask is answerable from the assignment alone and
  consistent with the key. De-keying one form would have created the criterion-2
  mixed/improper defect (Test 1); the accept-either route is barred by Shape A's
  one-respcondition rule (Test 2); the new exposure the clause opens is checked
  exhaustively and empty on both items (Test 4). Not a relabel.
- **`1/7` false for 7^0 and colliding with nothing** -> **CONFIRMED**, both
  halves, above.
- **All 12 exponent values recomputed from the stems** -> **CONFIRMED**: 729,
  {2^4/2^2, 4}, 4096, 1, 16, 64, 46/9, 49, 729, 1000, 289/36, 729. Each matches
  the rendered key.
- **r1's alternative fix for Q11 (`8 2/36`)** -> **REFUTED as a safe
  alternative.** 8 2/36 = 145/18 = 290/36, already present as
  `..._question_11_wrong_6`. Never applied; recorded so it is not revived.
- **r1 and r2's `maxvalue="100"` on the respcondition** -> **REFUTED as a
  description.** It is `setvar SCORE 100`; `maxvalue` is on `<decvar>`. No
  package defect; corpus-uniform at 163/163.
- **r2's out-of-slice note on P2Q7 (2^0 + 2^-3 = 9/8 = 1 1/8, both keyed, no
  unkeyed equivalent)** -> arithmetic **CONFIRMED**, but it is SC-2b's to score
  and carries no weight here.

Checked and cleared explicitly, so they are not rediscovered:

- Q1 `729 square feet` is **not** the right value in other units. 729 in² =
  5.0625 ft², and no choice reads 5.0625; 729 ft² = 104,976 in² is a genuinely
  different quantity. Correct distractor.
- Q2: the key's alternate Part A forms 2^{4-2} and 2^2 are not offered as
  choices, so the "or equivalent" in the key exposes nothing. `Part A: 2^4/2^2`
  is the only correct Part A expression present.
- Q11 `288/36` = 8 is the value of (8/4)^3 taken alone — a true quantity
  answering a different question. Recorded as the weaker case per criterion 2
  and **ruled a non-defect**: the stem asks for 6^{-2} + (8/4)^3 = 289/36, and 8
  is not it, nor is it an equivalent form of it under the amended stem.
- Q9 and Q12 carry identical choice lists. Both have true answer 729 and are
  separate items; criterion 6 forbids duplicate text *within* an item, and there
  is none.
- `shuffle_answers` is `false` and the keyed choices are authored first in every
  item. Out of rubric, corpus-wide, and appropriate for a self-check instrument
  whose results are hidden — noted, not scored.

## CLEAN

Part 1 Question 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 — all twelve worked, all
twelve clean. Q4, Q7 and Q11 verified as repaired, not merely as changed.

**SCORE: 10/10.**
