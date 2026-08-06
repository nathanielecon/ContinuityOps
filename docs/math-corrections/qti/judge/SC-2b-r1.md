SLICE: SC-2b          SCORE: 7/10
ITEMS WORKED: 12 of 12     (Part 2 Questions 1-12; none skipped)

Shape A confirmed: all 12 items are `multiple_answers_question`, `response1`,
one `<respcondition>` each, `maxvalue="100"` / `setvar 100`, 8 choices each,
every `correct_*` bare-required and every `wrong_*` `<not>`-negated, no
duplicate visible choice text, no `$` delimiters, `\(...\)` balanced, no images.
Stems verified against the rendered assignment page 4 (Lesson SC-2, Part 2
column) and keys against the rendered Part 2 solutions page 6 — both read as
images, not by `pdftotext` extraction order.

Exponent values recomputed independently from each stem:
  Q1  2^3 x 2^5 = 2^8 = 256 sq in
  Q2  Part A 3^4/3^2 ; Part B 81/9 = 9
  Q3  (2^4)^2 = 2^8 = 256
  Q4  5^0 = 1
  Q5  5^5/5^2 * 5^0 * 5^-1 = 5^(5-2+0-1) = 5^2 = 25
  Q6  (3^2)^2 * (2*3)^2 / (18/3)^2 = 81 * 36 / 36 = 81
  Q7  2^0 + 2^-3 = 1 + 1/8 = 9/8 = 1 1/8
  Q8  10^5/10^3 = 10^2 = 100
  Q9  (4^2)^2 = 4^4 = 256
  Q10 (2*3)^2 = 6^2 = 36
  Q11 (15/3)^2 = 5^2 = 25
  Q12 5^3 * 5^2 = 5^5 = 3125
All twelve agree with the keyed choice and with the Part 2 solutions PDF.

DEFECTS

  Part 2 Question 4 | criterion 2 | sc_2_part_2_question_4_wrong_7
    found:  "1 exactly"
    why:    5^0 = 1. The choice states the same value as the keyed
            `sc_2_part_2_question_4_correct_1` "1"; there is no arithmetic
            content distinguishing them. It is a true statement about the
            stem, is negated by the scoring key, and under all-or-nothing
            scoring a student who reads it as the answer restated selects it
            and scores 0. This is the rubric's own listed pattern
            ("the same value restated (`1 exactly` vs `1`)").
    fix:    Replace the visible text of sc_2_part_2_question_4_wrong_7 with a
            false value not already present among the choices, e.g.
            `<p>25</p>` (5^0 misread as 5^2). Keying is unchanged: the ident
            stays negated. Do not simply delete the choice — that would drop
            the item to 7 choices.

  Part 2 Question 7 | criterion 4 | respcondition, requires both
                      sc_2_part_2_question_7_correct_1 and _correct_2
    found:  required = {"9/8", "1 1/8"}; Part 2 solutions PDF page 6 reads
            "Question 7 ... Answer: 9/8 or 1 1/8"
    why:    2^0 + 2^-3 = 1 + 1/8 = 9/8 = 1 1/8. The answer key offers the two
            forms disjunctively ("or"), i.e. either single form is a complete
            correct answer. The item requires BOTH under all-or-nothing
            scoring, so a student who wrote 9/8 alone (or 1 1/8 alone) —
            exactly what the key licenses — is marked wrong. Note the tension
            that makes this item unfixable by re-keying alone: if only one of
            the two is keyed, the other becomes a true-but-unkeyed choice
            (criterion 2), which is equally fatal. The only consistent repair
            is to stop offering both forms.
    fix:    Keep sc_2_part_2_question_7_correct_1 `<p>9/8</p>` as the single
            keyed choice (the form the key states first). Change
            sc_2_part_2_question_7_correct_2 to a false distractor and negate
            it: rename the ident to sc_2_part_2_question_7_wrong_7, set its
            text to `<p>1 1/4</p>` (= 5/4, false), move it out of the bare
            `<varequal>` list into a `<not><varequal>` block, and update the
            `original_answer_ids` metadata field to match. Choice count stays
            at 8 and no mixed/improper twin of the key remains on offer.

CANDIDATES RULED ON

  P2Q4 wrong_7 "1 exactly" -> CONFIRMED. 5^0 = 1 recomputed; the text asserts
    the keyed value with no change of meaning, so it is a true-but-unkeyed
    choice under criterion 2.
  P2Q7 keys BOTH 9/8 and 1 1/8 where the solution PDF writes "or" ->
    CONFIRMED. Rendered page 6 of Topic1Part2Solutions.pdf reads
    "Answer: 9/8 or 1 1/8"; both idents sit in the bare `<varequal>` list of
    the single respcondition, so one-form answers score 0. Criterion 4.
  Audit's list of 12 Part 2 stem values (256, 9, 256, 1, 25, 81, 9/8, 100,
    256, 36, 25, 3125) -> CONFIRMED, each recomputed from the stem above and
    cross-checked against the rendered solutions page.

RULED ON, NOT DEFECTS (stated explicitly so the next pass need not redo them)

  Q1 sc_2_part_2_question_1_wrong_1 "256 square feet" — this is NOT the right
    value in different units. The banner area is 256 in^2; 256 ft^2 is a
    different quantity (144x larger), so the statement is false and the
    negation is correct.
  Q1 wrong_2..wrong_7 (-256, 257, 255, 258, 254, 0 square inches) — all false.
  Q2 wrong_1 3^(4+2) = 3^6 = 729 (false); wrong_2 3^2/3^4 = 1/9 (false);
    wrong_3 "Part B: 3" and wrong_4 "Part B: 27" (false; 81/9 = 9);
    wrong_5 -3^4/3^2 (false); wrong_6 4^4/3^2 (false). The key's other
    accepted Part A forms (3^(4-2), 3^2) are not offered as choices, so there
    is no unkeyed-true form and no "or" conflict on this item.
  Q3 / Q9 both evaluate to 256 from different stems ((2^4)^2 and (4^2)^2);
    duplicate value across items is not duplicate text within an item.
  Q3 stem adds "using the power-of-a-power property" where the assignment
    prints "Evaluate: (2^4)^2 =". Part 1 Question 3 carries the identical
    added clause, so it is house phrasing; it names the correct property, adds
    no number, and does not change the answer or answerability. Not a defect.
  Q7 wrong_1 8/9, wrong_2 1 9/8 (= 17/8), wrong_3 9/7, wrong_4 1 7/8 (= 15/8),
    wrong_5 -9/8, wrong_6 10/8 (= 5/4) — all differ from 9/8; correctly negated.
  Q5, Q6, Q8, Q10, Q11, Q12 distractor sets are off-by-one, sign-flipped,
    zero, or trailing-zero variants of the true value; every one recomputed
    and false.
  Markup/import: no `$...$`, no interleaved delimiters, no duplicated
    instruction block, no `<img>` and no media references anywhere in the
    package; manifest declares the QTI resource plus the assessment_meta
    dependency correctly.

CLEAN
  Part 2 Question 1
  Part 2 Question 2
  Part 2 Question 3
  Part 2 Question 5
  Part 2 Question 6
  Part 2 Question 8
  Part 2 Question 9
  Part 2 Question 10
  Part 2 Question 11
  Part 2 Question 12
