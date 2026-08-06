SLICE: SC-2a          SCORE: 7/10
ITEMS WORKED: 12 of 12     (none skipped)

Shape A confirmed for all 12: `multiple_answers_question`, exactly one
`<respcondition>` with `maxvalue="100"`, `respident="response1"`, 8 choices
each, every `correct_*` required by a bare `<varequal>`, every `wrong_*`
negated inside `<not>`, no unresolved ident references, no duplicate visible
choice text within any item, zero `$` delimiters, zero images, all `\(...\)`
pairs balanced in stems and choices. Structure and markup (criteria 6 and 7)
are clean on every item.

Stem fidelity (criterion 1) verified against the rendered assignment page 4,
Lesson SC-2, Part 1 column (not extracted text — the built-up fractions in
Q5/Q7/Q8/Q11 transpose under `pdftotext -layout`). All 12 stems reproduce the
Part 1 numbers exactly, and none has been contaminated by the Part 2 column
(Part 2 uses 2^3 x 2^5, 3^4 muffins among 3^2, (2^4)^2, 5^0, 5^5/5^2, 18/3,
2^0+2^-3, 10^5/10^3, (4^2)^2, (2*3)^2, (15/3)^2, 5^3*5^2 — none of which
appears here).

Exponent values recomputed independently from each stem:
  Q1  3^2 x 3^4 = 3^6 = 729 square inches
  Q2  Part A 2^4/2^2 ; Part B 2^2 = 4
  Q3  (4^3)^2 = 4^6 = 4096
  Q4  7^0 = 1
  Q5  4^5/4^2 * 4^0 * 4^-1 = 4^3 * 1 * 4^-1 = 4^2 = 16
  Q6  (2^3)^2 * (3*2)^2 / (12/2)^2 = 64 * 36 / 36 = 64
  Q7  5^0 + 3^-2 + 2^(6+3-7) = 1 + 1/9 + 4 = 46/9
  Q8  7^4/7^2 * 7^0 = 7^2 = 49
  Q9  (3^2)^3 = 3^6 = 729
  Q10 (2*5)^3 = 10^3 = 1000
  Q11 6^-2 + (8/4)^3 = 1/36 + 8 = 289/36
  Q12 3^4 * 3^2 = 3^6 = 729
Every one agrees with the Part 1 solutions PDF, page 6 (Q12 on page 7), read
rendered.

DEFECTS

  Part 1 Question 4 | criterion 2 | sc_2_part_1_question_4_wrong_7
    found:  <p>1 exactly</p>   (negated by <not><varequal>)
    why:    7^0 = 1. "1 exactly" denotes the identical value as the keyed
            choice sc_2_part_1_question_4_correct_1 `1`. It is not a near
            miss and not a different question: it is the same number restated,
            the exact case the rubric enumerates. Under all-or-nothing a
            student who evaluates 7^0 correctly and reads "select every choice
            that belongs in complete correct answer" has every reason to tick
            both, and scores zero for being right.
    fix:    Change the visible text of sc_2_part_1_question_4_wrong_7 from
            <p>1 exactly</p> to <p>1/7</p>
            (1/7 = 7^-1, false for 7^0, and distinct from the existing
            distractors -1, 2, 0, 3, 10, 7). Ident and the <not> wrapper stay
            as they are; no scoring change needed.

  Part 1 Question 7 | criterion 4 | required set {sc_2_part_1_question_7_correct_1, sc_2_part_1_question_7_correct_2}
    found:  both <p>46/9</p> and <p>5 1/9</p> are required by bare <varequal>
            in the single maxvalue="100" respcondition
    key:    Part 1 solutions p.6, Question 7 — "Answer: 46/9 or 5 1/9"
    why:    The key offers the two forms disjunctively. Requiring both under
            all-or-nothing inverts that: a student whose homework says 46/9
            ticks 46/9, leaves the mixed number alone, and scores zero on an
            answer the key calls correct. The symmetric student who wrote
            5 1/9 fails the same way. The generic trailing instruction does
            not rescue it — "Select every choice that belongs in complete
            correct answer. Part 1 and Part 2 both must be correct when prompt
            has multiple parts" is boilerplate about multi-part prompts (it is
            byte-identical on all 12 items, including the ten with a single
            keyed value), and it nowhere tells the student that two spellings
            of one number must both be ticked.
    ruling on the compatibility question: keying both forms is NOT compatible
            with an "or" key as the item currently stands. But simply
            de-keying one form is not a fix either — 5 1/9 = 46/9 exactly, so
            an unkeyed 5 1/9 sitting in the choice list becomes a
            true-but-unkeyed choice and trades a criterion 4 defect for a
            criterion 2 defect. Only two repairs close both holes.
    fix (preferred, keeps both forms visible):  make the stem say what the
            scoring requires. In the stem mattext of Part 1 Question 7,
            replace
              &lt;strong&gt;Canvas accuracy check:&lt;/strong&gt; Select every choice that belongs in complete correct answer.
            with
              &lt;strong&gt;Canvas accuracy check:&lt;/strong&gt; Select every choice that belongs in complete correct answer, including every equivalent form of that answer.
            Leave the key as it is. This is the "select all equivalent" stem
            the rubric contemplates, and it makes the two-form requirement
            derivable from the assignment alone.
    fix (alternative, single-form key): delete choice
            sc_2_part_1_question_7_correct_2 and its <varequal> from the
            respcondition, and add a new eighth choice
            ident="sc_2_part_1_question_7_wrong_7" with text <p>9/46</p>
            negated by <not><varequal>, to hold the count at 8. Do not simply
            drop the choice — that leaves 7 and breaks criterion 6.

  Part 1 Question 11 | criterion 4 | required set {sc_2_part_1_question_11_correct_1, sc_2_part_1_question_11_correct_2}
    found:  both <p>289/36</p> and <p>8 1/36</p> are required by bare
            <varequal> in the single maxvalue="100" respcondition
    key:    Part 1 solutions p.6, Question 11 — "Answer: 289/36 or 8 1/36"
    why:    Identical to Q7. 8 1/36 = (8*36+1)/36 = 289/36, so the two choices
            are one number; the key joins them with "or"; all-or-nothing
            demands both. A correct single-form answer scores zero.
    fix (preferred):  same stem amendment as Q7 — in the Part 1 Question 11
            stem mattext replace
              Select every choice that belongs in complete correct answer.
            with
              Select every choice that belongs in complete correct answer, including every equivalent form of that answer.
            and leave the key unchanged.
    fix (alternative): delete choice sc_2_part_1_question_11_correct_2 and its
            <varequal>, and add ident="sc_2_part_1_question_11_wrong_7" with
            text <p>8 2/36</p> negated by <not><varequal>, holding the count
            at 8. (8 2/36 = 8 1/18 = 145/18, false.)

    Whichever repair is chosen, apply the same one to Q7 and Q11 — they are
    the same defect and a split treatment would teach two different rules.

CANDIDATES RULED ON

  P1Q4 wrong_7 "1 exactly" -> CONFIRMED. 7^0 = 1; the choice restates the
    keyed value verbatim in words, so a correct reasoner selects it and scores
    zero under all-or-nothing. Recorded above as a criterion 2 defect.

  P1Q7 and P1Q11 key both the improper fraction and its mixed twin while the
    solutions PDF writes them with "or" -> CONFIRMED, with a correction to the
    candidate's reasoning. Confirmed that the key uses "or" (verified on the
    rendered page 6, not on extracted text). Confirmed that requiring both is
    a criterion 4 defect. The candidate's added claim that the improper
    fraction is "the form the assignment's directions ask for" is REFUTED —
    the assignment says only "Simplify", it does not prescribe a form, and the
    solution's own worked line ends at 5 1/9 before the Answer line lists
    46/9 first. So neither form is privileged, which is exactly why de-keying
    one is the weaker repair and the stem amendment is preferred.

  Audit's verified stem-value list (729, 4, 4096, 1, 16, 64, 46/9, 49, 729,
    1000, 289/36, 729) -> CONFIRMED. Independently recomputed from each stem
    and matched to the solutions PDF. One incompleteness worth noting, not a
    defect: Q2's answer is a pair, expression 2^4/2^2 together with Part B 4,
    and the list records only the 4.

  Not defects, checked and cleared explicitly:
   - Q1 wrong_1 "729 square feet" is not the right value in different units.
     729 square inches = 5.0625 square feet, so 729 square feet is a genuinely
     false quantity. Correct distractor.
   - Q2: the key's alternate Part A forms 2^(4-2) and 2^2 are not offered as
     choices, so no true-but-unkeyed choice arises; the keyed pair reproduces
     the key's "Part A: 2^4/2^2 (or equivalent); Part B: 4".
   - Q11 wrong_1 "288/36" equals 8, which is the value of (8/4)^3 alone. That
     is a true arithmetic quantity answering a different question, not an
     answer to the stem, and it is unkeyed. Recorded as the weaker case and
     ruled a non-defect: the stem asks for 6^-2 + (8/4)^3, and 8 is not it.
   - Q7 wrong_1 "46/8" = 5.75, wrong_2 "5 4/9" = 49/9, wrong_3 "5 9/46",
     wrong_4 "46", wrong_5 "-46/9", wrong_6 "47/9" — all distinct from 46/9.
   - Q11 wrong_2 "8 1/35", wrong_3 "289/35", wrong_4 "36/289", wrong_5
     "-289/36", wrong_6 "290/36" = 8 2/36 — all distinct from 289/36.
   - Q9 and Q12 carry identical choice lists, but they are separate items with
     the same true answer 729; duplicate text within a single item is what
     criterion 6 forbids, and there is none.

CLEAN

  Part 1 Question 1
  Part 1 Question 2
  Part 1 Question 3
  Part 1 Question 5
  Part 1 Question 6
  Part 1 Question 8
  Part 1 Question 9
  Part 1 Question 10
  Part 1 Question 12

  Defective: Part 1 Question 4 (criterion 2), Part 1 Question 7 (criterion 4),
  Part 1 Question 11 (criterion 4).
