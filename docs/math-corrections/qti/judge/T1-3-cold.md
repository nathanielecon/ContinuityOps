# T1-3 — cold validation

SLICE: T1-3          SCORE: 10/10
ITEMS WORKED: 8 of 8     (none skipped)

Shape A confirmed before scoring: all 8 items are `multiple_answers_question`,
idents are `1_3_part_N_question_M_correct_K` / `_wrong_K`, `respident="response1"`,
one `<respcondition>` per item with `maxvalue="100"` and `<setvar action="Set">100`,
8 choices per item. Shape A criteria applied.

## Method

Read the raw XML at
`/tmp/qtiwork/pkg/topic-1-3-independent-practice-accuracy-check-qti/topic_1_3_independent_practice_accuracy_check/topic_1_3_independent_practice_accuracy_check.xml`
directly. Did not use `/tmp/qtiwork/slices/T1-3.json` for any stem or choice text.
Own extractor: stripped real tags first with `</?[a-zA-Z][^>]*>`, unescaped second,
so a bare `<` before a space or digit stays text. (No `<` of that kind occurs in
this slice, but the order was applied anyway.)

Scoring tree parsed with ElementTree, not regex: for each `<respcondition>` the
set of `<varequal>` inside any `<not>` was collected first and subtracted from the
full `<varequal>` set, so a `<varequal>` under `<not>` is never counted as required.

Sources read **rendered**, not extracted:
- assignment page 2 (`Topic1IndependentPractice.pdf`, Lesson 1-3 table, both columns)
- `Topic1Part1Solutions.pdf` page 2, Lesson 1-3 section
- `Topic1Part2Solutions.pdf` page 2, Lesson 1-3 section

The rendered assignment page confirms the two-column split is not transposed:
the left column (Part 1) carries 10/4/8, 15/20/3, $500 / $12.50 / 6 months,
`-12 + 19`; the right column (Part 2) carries 12/5/9, 18/4/25, $400 / $8.75 /
8 months, `-8 + 14`. Each QTI item was checked against the column its title names.

Formed my own view on all eight items and on the repair diff before opening
`T1-3-r1.md` and `T1-3-r2.md`.

## DEFECTS

None. No defect stands.

## Mathematics, worked independently — every keyed and every non-keyed choice

**Part 1 Question 1** — stem 10, then lose 4, then lose 8. `10 + (-4) + (-8) = -2`.
- keyed `correct_1` "Start at 0; move right 10, left 4, then left 8." — true; a loss is a leftward move.
- keyed `correct_2` "10 + (-4) + (-8)" — true, and the key PDF's own expression.
- keyed `correct_3` "After the first two turns, the point is at 6." — true; `10 - 4 = 6`.
- keyed `correct_4` "The final point and final score are -2." — true.
- non-keyed `wrong_1` "Start at 0; move right 10, right 4, then left 8." — describes `10 + 4 - 8 = 6`; the 4 is a loss, so **false**.
- non-keyed `wrong_2` "10 - (-4) + (-8)" — `10 + 4 - 8 = 6`, not `-2`, and it does not represent the scenario. **False**.
- non-keyed `wrong_3` "After the first two turns, the point is at 14." — `14 = 10 + 4`, wrong sign on the second move. **False**.
- non-keyed `wrong_4` "The final point and final score are 2." — **false**.
- Key PDF Part 1 Q1 (rendered): "Part A: Start at 0. Move right 10, left 4, left 8. / Part B: 10 + (-4) + (-8) = -2". Keyed set reproduces it exactly. No "or" alternative in the key, so all-or-nothing keying excludes no acceptable form.

**Part 1 Question 2** — `15 + (-20) + 3 = -2`. Keyed `-2`.
- non-keyed 2, -1, -3, 0, -4, -20, 15 — every one differs from -2. `-20` and `15` are stem quantities, not the final score; neither is a true answer to the question asked. Key PDF: `-2`.

**Part 1 Question 3** — `6 x 12.50 = 75`; `500 - 75 = 425`. Keyed `$425`.
- non-keyed $-425, $426, $424, $427, $423, $0, $4250 — all differ. `$-425` is a sign error, not a restatement or alternate format of the true value, so it is not a criterion-2 case. `$4250` is a decimal-place error. Key PDF: `$425` (confirmed rendered: "Fee $12.50 each month; 6 x $12.50 = $75. $500 - $75 = $425").

**Part 1 Question 4** — `-12 + 19 = 7`. Keyed `7`.
- non-keyed -7, 8, 6, 9, 5, 0, 70 — all differ. Key PDF: `7`.

**Part 2 Question 1** — stem 12, then lose 5, then lose 9. `12 + (-5) + (-9) = -2`.
- keyed `correct_1` "Start at 0; move right 12, left 5, then left 9." — true.
- keyed `correct_2` "12 + (-5) + (-9)" — true.
- keyed `correct_3` "After the first two moves, the point is at 7." — true; `12 - 5 = 7`.
- keyed `correct_4` "The final point and final score are -2." — true.
- non-keyed `wrong_1` "Start at 0; move right 12, right 5, then left 9." — gives 8. **False**.
- non-keyed `wrong_2` "12 - (-5) + (-9)" — `12 + 5 - 9 = 8`, not -2. **False**.
- non-keyed `wrong_3` "After the first two moves, the point is at 17." — `17 = 12 + 5`. **False**.
- non-keyed `wrong_4` "The final point and final score are 2." — **false**.
- Key PDF Part 2 Q1 (rendered): "Start at 0. Move right 12, left 5, left 9. / 12 + (-5) + (-9) = -2". Exact match.

**Part 2 Question 2** — `18 + 4 + (-25) = -3`. Keyed `-3`.
- non-keyed 3, -2, -4, -1, -5, 0, -30 — all differ. `-2` is the answer to Part 1 Question 2, not to this item, so it is false here. Key PDF: `-3`.

**Part 2 Question 3** — `8 x 8.75 = 70`; `400 - 70 = 330`. Keyed `$330`.
- non-keyed $-330, $331, $329, $332, $328, $0, $3300 — all differ. Key PDF: `$330` (rendered: "Fee $8.75 each month; 8 x $8.75 = $70. $400 - $70 = $330").

**Part 2 Question 4** — `-8 + 14 = 6`. Keyed `6`.
- non-keyed -6, 7, 5, 8, 4, 0, 60 — all differ. Key PDF: `6`.

**Criterion 2 (true-but-unkeyed) — clean.** I worked all 50 non-keyed choices.
None is an equivalent or unsimplified fraction, a mixed/improper pair, a bare
value where the key writes `n = value`, a restated value, an alternative valid
expression, a right value in different units, a `+-` form of a `+ and -` key, or
a statement given as true in the stem. Every distractor in this slice is either a
distinct numeric value or a materially different number-line description. There
is also no weaker "true statement answering a different question" case: `-20`,
`15` (P1Q2) and `-2` (P2Q2) are numbers that appear elsewhere in the slice or
stem but none of them is asserted as true by its own choice text — each choice
is a bare value offered as the answer to the question asked, and each is wrong
for that question.

**Criterion 3 (false-but-keyed) — clean.** All 14 keyed choices worked above.
No double-signed phrasing of the `-96 feet below sea level` kind occurs: the two
number-line descriptions state direction words ("right", "left") explicitly and
without a competing sign, and the four bare-value keys carry a single sign.

## Other criteria

**1 Stem fidelity.** All eight stems match the rendered assignment page 2 on every
quantity, operation and question asked, each against the column its title names.
The QTI paraphrases the assignment's wording ("In the first round of a board game"
for "In round 1 of a game"; "board game" / "card game" added to distinguish the
two parts; "If there are no other deposits or withdrawals" for "With no other
activity"). No number, no operation and no question is altered by the paraphrase,
so I do not score it. `\(-12 + 19 =\)` and `\(-8 + 14 =\)` reproduce the
assignment's `-12 + 19 =` and `-8 + 14 =`.

**4 Key agreement.** Verified item by item above against the rendered key pages.
Both key PDFs state exactly one answer per question for Lesson 1-3, with no "or"
alternative anywhere in the section, so requiring the full keyed set under
all-or-nothing scoring cannot zero a student who gave an acceptable alternative form.

**5 Answerability.** Every keyed choice is producible from the assignment alone.
The one place worth testing is `correct_3` on both Q1 items, which keys an
intermediate position ("after the first two turns / moves") that the assignment
does not name. I rule it answerable: Part A of the assignment explicitly asks the
student to explain the change on a number line, so the position after the first
two moves is a direct product of the work the assignment demands, and the
statement is unambiguously true once those moves are drawn. Not a defect.

**6 Structure.** Verified programmatically over all 8 items and all 64
`<response_label>` elements, with the `<respcondition>` tree parsed and `<not>`
blocks resolved:
- exactly one `<respcondition>` per item, `maxvalue="100"`, `<setvar action="Set">100`;
- required set equals the `correct_*` ident set on all 8 items (14 required total);
- negated set equals the `wrong_*` ident set on all 8 items (50 negated total);
- 14 + 50 = 64 = every choice accounted for; `respident="response1"` on all 64 `<varequal>`;
- 8 choices per item, meeting the `>=8` floor;
- no two choices within any item share visible text (checked on the post-strip,
  post-unescape text of all 64 labels);
- `original_answer_ids` matches the `<response_label>` order and content on every item;
- no duplicate idents.
`imsmanifest.xml` and `assessment_meta.xml` are well formed and internally
consistent; `points_possible` 8.0 matches 8 one-point items; the manifest's
resource and dependency hrefs both resolve to files present in the package.

**7 Markup and import validity.** Exactly one instruction block per stem —
`Canvas accuracy check` occurs once in each of the 8 stems, and the old
`Select every choice that is part of a correct solution.` paragraph occurs
0 times in the file. Math delimiters: `\(` appears twice and `\)` twice, forming
the two balanced spans `\(-12 + 19 =\)` and `\(-8 + 14 =\)`; those are the only
math spans in the package. No `$...$` math delimiter anywhere — I checked for
paired `$` explicitly and found none. The `$` characters in `$500`, `$12.50`,
`$425`, `$400`, `$8.75`, `$330` and the money distractors are currency in plain
HTML in blocks that contain no `\(`, so there is no interleaved
`$...\(...\)...$` and nothing for Canvas to mis-delimit. The inner HTML of all
72 `<mattext>` payloads parses with balanced tags. The file is pure ASCII
(0 bytes above 0x7F), so no smart quote or dash was introduced. No `<img>` and
no `src=` attribute exists anywhere in the package, so there is no
`$IMS-CC-FILEBASE$` exposure and nothing image-blocking to resolve.

## The repair — attacked directly

The brief flags a repair for a duplicated instruction block on two items. I did
not take the r1/r2 account of it on trust; I diffed the current package against
the untouched original at
`/home/user/ContinuityOps/inbox/Inbox/topic-1-3-independent-practice-accuracy-check-qti.zip`.

The diff is exactly two lines, both `<mattext>` stems — `1_3_part_1_question_1`
and `1_3_part_2_question_1` — and in each the sole change is the deletion of the
paragraph

`<p><strong>Canvas accuracy check:</strong> Select every choice that is part of a correct solution. Select no incorrect choices.</p>`

No other line in the XML differs. `imsmanifest.xml` and `assessment_meta.xml` are
byte-identical to the original. Testing the brief's five specific failure modes:

1. **No choice was replaced.** The repair touched only stem instruction text; all
   64 choice texts, values and signs are identical to the original. There is no
   swapped distractor to re-derive, so the "true-for-true swap" failure mode
   cannot apply here — and I worked all 50 distractors from the stem anyway, above.
2. **No collision introduced.** Duplicate-visible-text check passes on all 8 items.
3. **Scoring tree still matches the idents.** Re-parsed with `<not>` resolved:
   required == `correct_*` and negated == `wrong_*` on all 8 items. The
   `<resprocessing>` blocks are untouched by the diff.
4. **Nothing outside the repair moved.** Established by the two-line diff against
   the original zip, not by re-reading r1's list of untouched items.
5. **The criterion the earlier judge did not score.** r1 scored this slice on
   markup and treated the mathematics as a pass. I have now worked all 8 items,
   all 14 keyed and all 50 non-keyed choices, from the stems and from both
   rendered key pages, independently. It holds.

**The right paragraph was kept.** A corpus-wide sweep of all 88 Shape A items
across the 12 `topic-*` packages finds only two distinct trailing instruction
blocks: the canonical one on 85 items, and a deliberate variant on 3
`topic-sc-2` items that adds "including every equivalent form of that answer"
for equivalent-form questions. Zero Shape A items now carry a doubled block. All
8 T1-3 stems carry the canonical 85-item form. Keeping the second paragraph and
deleting the first was the correct direction: the deleted text said "part of a
correct solution", which reads as partial credit and contradicts the
all-or-nothing rule the `<respcondition>` actually implements.

## CANDIDATES RULED ON

- **"Audit reported all 8 items clean"** -> **REFUTED as to the package as
  delivered to r1; now moot.** The first-pass audit was wrong: two items carried
  a doubled instruction block, a criterion 7 defect it missed by reading only the
  mathematics. On the repaired package in front of me the eight items are in fact
  clean, on the mathematics and on the markup, but that is a different claim about
  a different file and does not retroactively validate the audit.

## Rulings on the earlier reports (read after forming my own view)

- **r1's two criterion 7 defects** -> **agreed, independently.** The doubled block
  is present in the original zip on exactly the two items r1 named, and its two
  paragraphs do conflict in scope.
- **r1's clean rulings on criteria 1-6** -> **agreed, independently.** I reworked
  every item from the sources rather than checking r1's arithmetic. My values
  match: -2, -2, $425, 7 / -2, -3, $330, 6.
- **r2's byte-delta argument** (-310 bytes = 2 x 155) -> **sound, but I did not
  rely on it.** A byte-count identity is consistent with other compensating edits;
  the direct diff against the original zip is the stronger check and it confirms
  the same conclusion.
- **r2's stale-cache note** -> **now resolved.** `/tmp/qtiwork/slices/T1-3.json`
  has been rebuilt: it carries `zip_sha12` `13391c98ddcf`, which matches
  `sha256sum` of the current staged zip and the entry in
  `/tmp/qtiwork/staged/sha256sums.txt`, and the doubled-block text occurs 0 times
  in it. The staged zip is also byte-for-byte identical to
  `/tmp/qtiwork/pkg/topic-1-3-independent-practice-accuracy-check-qti/`.
  I scored from the raw XML regardless.
- I found **nothing that r1 or r2 missed**, and I have **no overturn to record**.

## CLEAN

- Part 1 Question 1 — no defect
- Part 1 Question 2 — no defect
- Part 1 Question 3 — no defect
- Part 1 Question 4 — no defect
- Part 2 Question 1 — no defect
- Part 2 Question 2 — no defect
- Part 2 Question 3 — no defect
- Part 2 Question 4 — no defect

All 8 items worked. No defect stands. **10/10.**
