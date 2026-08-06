SLICE: SC-1          SCORE: 5/10
ITEMS WORKED: 4 of 4     (none skipped)

Shape A confirmed: 4 multiple_answers_question items, idents `..._correct_N` /
`..._wrong_N`, one `<respcondition>` each with `maxvalue="100"`, 8 choices each,
`respident="response1"`.

NOTE ON THE SLICE CACHE: the cache in /tmp/qtiwork/slices/SC-1.json is truncated
at `<` characters. It shows `correct_1` as "10.4" and `wrong_5` as "-10.4"; the
raw XML has `10.4 &lt; 10.6` and `-10.4 &lt; 10.6`. It also shows the Q2 stem
symbol list as `\(= \qquad \qquad \leq ...\)` with the `<` and `>` dropped, and
`wrong_1` as empty string (it is `&lt;`). All scoring below is from the raw XML,
not the cache.

DEFECTS

  Part 1 Question 2 | 5 (also 1 and 4) | stem symbol list + correct_2, correct_3
    found:  stem: `\(= \qquad &lt; \qquad &gt; \qquad \leq \qquad \geq \qquad \neq\)`
            keyed choices: `=` (correct_1), `≤` (correct_2), `≥` (correct_3)
    why:    3/4 = 0.75 exactly, so in the abstract `=`, `≤` and `≥` are all true
            and `<`, `>`, `≠` are all false. But the assignment does not offer
            `≤` or `≥`. Read off the rendered page 2 of
            Topic1IndependentPractice.pdf (not extracted text), Lesson SC-1
            Part 1 Q2 ends: "Select all symbols that appropriately relate the
            two numbers (<, >, =, ≠)." Four symbols. Confirmed a second way by
            the rendered page 2 of Topic1Part1Solutions.pdf: "We Solve: 3/4 =
            0.75 exactly, so of the four symbols offered (<, >, =, ≠) only = is
            true. Answer: = (only)." Confirmed a third way by
            Topic1Part2Solutions.pdf page 2, same sentence.
            A student holding only the assignment can produce exactly `=`.
            Under all-or-nothing scoring that student fails the required
            `<varequal>` on correct_2 and correct_3 and scores zero. The QTI
            stem manufactures the two extra options itself by listing six
            symbols where the assignment lists four, so the item is neither
            answerable from the assignment (criterion 5), faithful to the
            assignment's wording (criterion 1), nor in agreement with the
            answer key (criterion 4: keyed set {=, ≤, ≥} vs key "= (only)").
    fix:    (a) Replace the stem's symbol paragraph
              from: `&lt;p&gt;\(= \qquad &lt; \qquad &gt; \qquad \leq \qquad \geq \qquad \neq\)&lt;/p&gt;`
              to:   `&lt;p&gt;\(&lt; \qquad &gt; \qquad = \qquad \neq\)&lt;/p&gt;`
            (b) Delete the `≤` and `≥` choices outright — do not merely
            re-label them as `wrong_*`, because `3/4 ≤ 0.75` and `3/4 ≥ 0.75`
            are true and would then become true-but-unkeyed distractors
            (criterion 2). Remove `<response_label ident="sc_1_part_1_question_2_correct_2">`
            and `<response_label ident="sc_1_part_1_question_2_correct_3">`.
            (c) Add two false symbol distractors to hold the count at 8, e.g.
            `&lt;p&gt;≪&lt;/p&gt;` and `&lt;p&gt;≫&lt;/p&gt;` as
            `sc_1_part_1_question_2_wrong_6` and `..._wrong_7` (both false:
            3/4 is neither much less than nor much greater than 0.75).
            (d) In `<respcondition>`, drop the two bare
            `<varequal>sc_1_part_1_question_2_correct_2</varequal>` and
            `..._correct_3</varequal>` lines, leaving `..._correct_1` as the
            only bare `<varequal>`, and add `<not><varequal respident="response1">`
            blocks for the two new `wrong_6` / `wrong_7` idents.
            (e) Update `original_answer_ids` to
            `sc_1_part_1_question_2_correct_1,sc_1_part_1_question_2_wrong_1,sc_1_part_1_question_2_wrong_2,sc_1_part_1_question_2_wrong_3,sc_1_part_1_question_2_wrong_4,sc_1_part_1_question_2_wrong_5,sc_1_part_1_question_2_wrong_6,sc_1_part_1_question_2_wrong_7`

  Part 2 Question 2 | 5 (also 1 and 4) | stem symbol list + correct_2, correct_3
    found:  stem: `\(= \qquad &lt; \qquad &gt; \qquad \leq \qquad \geq \qquad \neq\)`
            keyed choices: `=` (correct_1), `≤` (correct_2), `≥` (correct_3)
    why:    Identical defect with the Part 2 numbers. 2/5 = 0.4 exactly, so
            `=`, `≤`, `≥` are true in the abstract and `<`, `>`, `≠` false.
            Rendered page 2 of Topic1IndependentPractice.pdf, Lesson SC-1
            Part 2 Q2: "Select all symbols that appropriately relate the two
            numbers (<, >, =, ≠)." Four symbols, no `≤` and no `≥`. Rendered
            page 2 of Topic1Part2Solutions.pdf: "We Solve: 2/5 = 0.4 exactly,
            so of the four symbols offered (<, >, =, ≠) only = is true.
            Answer: = (only)." A student who selects `=` alone, the only set
            the assignment permits and the only set the key records, scores
            zero.
    fix:    Same five-part change as Part 1 Question 2, with the
            `sc_1_part_2_question_2_*` idents:
            (a) stem paragraph to `&lt;p&gt;\(&lt; \qquad &gt; \qquad = \qquad \neq\)&lt;/p&gt;`
            (b) delete the `≤` (`..._correct_2`) and `≥` (`..._correct_3`)
                response_labels
            (c) add `&lt;p&gt;≪&lt;/p&gt;` / `&lt;p&gt;≫&lt;/p&gt;` as
                `sc_1_part_2_question_2_wrong_6` / `..._wrong_7`
            (d) leave `..._correct_1` as the only bare `<varequal>`; add
                `<not>` blocks for `..._wrong_6` and `..._wrong_7`
            (e) `original_answer_ids` becomes
            `sc_1_part_2_question_2_correct_1,sc_1_part_2_question_2_wrong_1,sc_1_part_2_question_2_wrong_2,sc_1_part_2_question_2_wrong_3,sc_1_part_2_question_2_wrong_4,sc_1_part_2_question_2_wrong_5,sc_1_part_2_question_2_wrong_6,sc_1_part_2_question_2_wrong_7`

WEAKER CASES RECORDED AND RULED (not counted as defects)

  Part 1 Question 1 / Part 2 Question 1 | `wrong_5` = `-10.4 &lt; 10.6` and
  `-9.3 &lt; 9.8`. Both are true arithmetic statements. Ruled NOT a defect,
  and ruled explicitly rather than merged with the criterion-2 list: the stem
  asks for statements that "compare the weight of the cat and the rabbit"
  (resp. dog and cat), and the cat weighs +10.4 lb, not -10.4 lb. The
  statement is true arithmetic answering a different question, which the
  rubric names as the weaker case. It is also unkeyed, so the strongest
  student, who reads the stem, does not select it.

  Part 1 Question 2 / Part 2 Question 2 | `wrong_4` = `~` and `wrong_5` = `≡`.
  Ruled NOT defects. `~` denotes similarity or asymptotic relation, not an
  asserted numeric equality; the standard approximate-equality glyph is `≈`.
  `≡` denotes identical equality or congruence, undefined at this grade and
  absent from the assignment. Neither appears in the assignment's four
  offered symbols, so no student working from the assignment can be lured
  into selecting them, and both are unkeyed. Recording them because `≡` is
  the nearest thing in this slice to a genuine true-but-unkeyed reading; it
  does not rise to a defect.

CANDIDATES RULED ON

  P1Q2 / P2Q2 keyed `<=` and `>=` (correct_2, correct_3), criterion 5
    -> CONFIRMED. Verified independently: the assignment's rendered symbol
    list is four symbols and both solution PDFs read "Answer: = (only)", so
    the keyed set is unreachable from the assignment and disagrees with the
    key even though `≤` and `≥` are true of 3/4 vs 0.75 and 2/5 vs 0.4.

  P1Q2 / P2Q2 stem lists six symbols `= < > <= >= !=`; assignment lists four
    -> CONFIRMED. Raw XML stem carries `\leq` and `\geq`; rendered assignment
    page 2 carries `(<, >, =, ≠)` in both Part 1 and Part 2. Same root cause
    as the candidate above and fixed by the same edit.

  P1Q1 / P2Q1 distractors `-10.4 < 10.6` and `-9.3 < 9.8`
    -> REFUTED as defects. True as bare inequalities, but they do not state a
    comparison of the two given weights, they are unkeyed, and under
    all-or-nothing scoring a student reasoning correctly from the stem leaves
    them unselected. Recorded above as the rubric's weaker case.

CLEAN

  Part 1 Question 1 — stem matches assignment Part 1 (cat 10.4 lb, rabbit
    10.6 lb, symbols `<` and `>`). Keyed `10.4 < 10.6` and `10.6 > 10.4`
    reproduce Topic1Part1Solutions.pdf "Answer: 10.4 < 10.6 and 10.6 > 10.4
    (pounds OK)" exactly, both parts of the "and" keyed, no "or" split.
    Non-keyed choices all worked: `10.4 > 10.6` false; `10.6 < 10.4` false;
    `10.4 = 10.6` false; `10.4 ≤ 10.6 and 10.6 ≤ 10.4` false, since the second
    conjunct fails; `11.4 < 10.6` false; `-10.4 < 10.6` ruled above. Eight
    distinct choices, one respcondition, all `correct_*` bare and all
    `wrong_*` negated, `\(...\)` delimiters balanced, no `$`, no duplicated
    instruction block, no images.

  Part 2 Question 1 — stem matches assignment Part 2 (dog 9.3 lb, cat 9.8 lb).
    Keyed `9.3 < 9.8` and `9.8 > 9.3` reproduce Topic1Part2Solutions.pdf
    "Answer: 9.3 < 9.8 and 9.8 > 9.3 (pounds OK)". Non-keyed choices worked:
    `9.3 > 9.8` false; `9.8 < 9.3` false; `9.3 = 9.8` false; `9.3 ≥ 9.8 and
    9.8 ≥ 9.3` false, since the first conjunct fails; `10.3 < 9.8` false;
    `-9.3 < 9.8` ruled above. Structure and markup as above, all clean.

  Part 1 Question 2 and Part 2 Question 2 are clean on criteria 6 and 7
    (one respcondition, 8 distinct choices, correct/wrong split matches the
    scoring tree, balanced `\(...\)`, no stray `$`, no images) but fail
    criteria 1, 4 and 5 as recorded under DEFECTS.
