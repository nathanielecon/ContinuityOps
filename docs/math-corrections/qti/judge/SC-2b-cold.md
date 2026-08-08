SLICE: SC-2b          SCORE: 10/10
ITEMS WORKED: 12 of 12     (Part 2 Questions 1-12; none skipped)

Cold read. Formed independently from the raw XML at
/tmp/qtiwork/pkg/topic-sc-2-independent-practice-accuracy-check-qti/, the
rendered assignment page and the rendered Part 2 key, before opening
SC-2b-r1.md or SC-2b-r2.md. The slices/*.json caches were not used at any
point. Shape A confirmed.

METHOD

Wrote my own extractor. Tags stripped with `</?[a-zA-Z][^>]*>` first, entities
unescaped second, per the known trap; no stem in this slice contains a bare `<`
so the trap could not have fired here, but the order was kept anyway. Scoring
read by walking the `<conditionvar>` tree with a negation flag that flips on
`<not>` and passes through `<and>`/`<or>` -- not by regex over the item, so
`<varequal>` inside `<not>` is correctly counted as negated.

PDFs read as rendered images, not by extraction. `pdftotext -layout` on the
assignment did transpose the built-up fractions in this very section (Q5 came
out as "552 . 50 . 5-1", Q8 as "10 / 103", Q11 as "15 3"), so every fraction
below is settled from the render:
  assignment  Topic1IndependentPractice.pdf p.4, "Lesson SC-2", Part 2 column
  key         Topic1Part2Solutions.pdf p.5 (Q1-Q8) and p.6 (Q9-Q12)

EXPONENT VALUES RECOMPUTED FROM THE STEMS (all 12, independently)

  Q1   2^3 x 2^5 = 2^(3+5) = 2^8 = 256          -> 256 square inches
  Q2   Part A: 3^4 / 3^2 ; Part B: 3^(4-2) = 3^2 = 81/9 = 9
  Q3   (2^4)^2 = 2^(4*2) = 2^8 = 256
  Q4   5^0 = 1
  Q5   (5^5/5^2) * 5^0 * 5^-1 = 5^(5-2+0-1) = 5^2 = 25
  Q6   (3^2)^2 * (2*3)^2 / (18/3)^2 = 3^4 * 6^2 / 6^2 = 81 * 36 / 36 = 81
  Q7   2^0 + 2^-3 = 1 + 1/2^3 = 1 + 1/8 = 9/8 = 1 1/8
  Q8   10^5 / 10^3 = 10^(5-3) = 10^2 = 100
  Q9   (4^2)^2 = 4^(2*2) = 4^4 = 256
  Q10  (2*3)^2 = 6^2 = 36
  Q11  (15/3)^2 = 5^2 = 25
  Q12  5^3 * 5^2 = 5^(3+2) = 5^5 = 3125

All twelve stems match the rendered assignment's Part 2 column exactly (numbers
and operations). All twelve keyed sets reproduce the rendered key: 256 square
inches; Part A 3^4/3^2 (or equivalent) and Part B 9; 256; 1; 25; 81; 9/8 or
1 1/8; 100; 256; 36; 25; 3125.

Every choice in all 12 items was then parsed to an exact Fraction (mixed
numbers included) and compared to the recomputed truth. Result: zero keyed
choices false, zero non-keyed choices true. Q1's unit-bearing choices were
compared on unit as well as value.

THE CONTESTED CALL -- P2Q7, criterion 4. MY OWN RULING: THE OVERRULE WAS RIGHT.
The amended stem is a genuine cure; the r1 fix would have displaced the defect.

  as it now stands: stem "Simplify \(2^0+2^{-3}\)." followed by "Canvas
    accuracy check: Select every choice that belongs in complete correct
    answer, including every equivalent form of that answer. ..."
    required = {correct_1 "9/8", correct_2 "1 1/8"}; six wrong_* negated.
  key (rendered p.5): "Answer: 9/8 or 1 1/8".

  Why the r1 remedy was wrong. r1 proposed keeping "9/8" keyed and converting
  "1 1/8" into a false distractor. 1 1/8 = 1 + 1/8 = 9/8 exactly; it is the
  mixed form of the key's own first-listed answer, and rubric criterion 2 names
  "a mixed/improper pair" as counting-as-true. Negating it therefore creates a
  true-but-unkeyed choice: the student who simplified to 1 1/8 -- a form the key
  itself licenses -- selects it and, under all-or-nothing scoring, gets zero.
  That is not closing the defect, it is moving it from criterion 4 to criterion
  2, and criterion 2 is the harder failure because it punishes the student who
  reasoned correctly. r1's own text concedes the tension ("if only one of the
  two is keyed, the other becomes a true-but-unkeyed choice ... which is equally
  fatal") and then prescribes exactly that trade anyway. Note also that the r1
  fix as written would have replaced the visible text with "1 1/4"; that is a
  second, unrelated edit of a mathematically true choice into a false one, i.e.
  it destroys a correct answer rather than resolving the ambiguity.

  Why the applied remedy works. Criterion 4's rule is stated together with the
  harm that justifies it: "a student who gives one acceptable form scores zero."
  That harm arises when the item silently asks the student to mark the form they
  wrote. The amended stem changes the task before the student answers: mark
  every equivalent form on offer. Both forms are on offer, so the instruction is
  completable by a student who wrote either one, and no acceptable form is
  punished. Criterion 2's final bullet independently blesses this construction
  -- "for a stem that says 'select all equivalent ...': every algebraically
  equivalent form ... counts as true" -- which is only coherent if such a stem is
  expected to key them all. The applied fix also avoids inventing a preference
  between two forms the key joins with "or", not with "preferably".

  A third route existed and was not taken: drop one form from the choice list
  entirely and key the survivor. That is equally sound and is in fact what
  P2Q2 in this same slice does (see below). Both are correct; the applied one
  is not inferior, and it preserves full key agreement.

  THE NEW-EXPOSURE SWEEP the amendment demands. A stem promising "every
  equivalent form" converts any unkeyed equivalent from a debatable defect into
  a flat criterion-2 violation, so all six distractors were evaluated as exact
  fractions against 9/8:
      wrong_1  8/9    = 8/9      != 9/8   (numerator/denominator swapped)
      wrong_2  1 9/8  = 17/8     != 9/8   (2.125; whole part added to 9/8)
      wrong_3  9/7    = 9/7      != 9/8
      wrong_4  1 7/8  = 15/8     != 9/8   (1.875)
      wrong_5  -9/8   = -9/8     != 9/8
      wrong_6  10/8   = 5/4      != 9/8   (1.25; not 1.125)
  None is equivalent to 9/8. No decimal form (1.125), no unsimplified form
  (18/16), and no "1 + 1/8" appears among the choices. The keyed set is exactly
  the set of equivalent forms present in the item, so the amended stem's promise
  is fully honoured and creates no new exposure. The amendment is safe here --
  but it is safe only because this sweep comes back empty, which is the check
  that had to be run and which I ran independently.

  Consistency check across the package (not scored, reported as corroboration).
  The clause appears on exactly 3 of the 24 items: P1Q7, P1Q11, P2Q7 -- i.e. on
  all three items in the whole package whose key writes two forms and whose
  choice list offers both. The two outside my slice were swept the same way and
  are also exposure-free: P1Q7 keys 46/9 and 5 1/9 (both = 46/9) against
  distractors 46/8, 5 4/9, 5 9/46, 46, -46/9, 47/9 -- none equal 46/9;
  P1Q11 keys 289/36 and 8 1/36 (both = 289/36) against 288/36 (= 8, not
  289/36), 8 1/35, 289/35, 36/289, -289/36, 290/36 -- none equal 289/36. So the
  package teaches one rule rather than a one-off patch, and a student meeting
  the clause on P2Q7 has met it before.

P2Q4 -- "25" VERIFIED AS REQUESTED

  sc_2_part_2_question_4_wrong_7 now reads "25", ident unchanged, still inside
  a `<not><varequal>` block.
  False for the stem: the stem is "Evaluate: \(5^0 =\)" and 5^0 = 1. 25 = 5^2,
  so the choice is the classic "multiply the base by itself regardless of a zero
  exponent" error -- a plausible wrong answer, and in no reading a restatement
  of the key. It is not a true statement answering a different question either;
  it is simply a wrong value for the posed question, so the rubric's weaker
  "true but answers a different question" case does not arise.
  No collision within the item: the eight visible texts are 1, -1, 2, 0, 3, 10,
  5, 25 -- pairwise distinct after whitespace/case normalisation, checked
  programmatically across all 12 items (zero duplicates anywhere in the slice).
  25 is the keyed value of P2Q5 and P2Q11, but those are separate items with
  separate response identifiers and separate scoring trees; nothing carries
  across, and this is not a defect.
  The "1 exactly" text that made this a criterion-2 defect is gone from the
  item; no other choice in the item restates the key.

NOTHING OUTSIDE THE REPAIR MOVED -- verified against the shipped original, not
against the r1 report's account of it

  Diffed the current XML line-by-line against the pristine zip at
  /home/user/ContinuityOps/inbox/Inbox/topic-sc-2-independent-practice-accuracy-check-qti.zip.
  Exactly five lines differ in the whole 2523-line file:
    line  388  P1Q4  wrong_7 "1 exactly" -> "1/7"          (SC-2a's slice)
    line  662  P1Q7  stem gains the equivalent-form clause  (SC-2a's slice)
    line 1080  P1Q11 stem gains the equivalent-form clause  (SC-2a's slice)
    line 1642  P2Q4  wrong_7 "1 exactly" -> "25"            (this slice)
    line 1916  P2Q7  stem gains the equivalent-form clause  (this slice)
  imsmanifest.xml and assessment_meta.xml are byte-identical to the original.
  No `<respcondition>`, `<varequal>`, `<not>`, ident or `original_answer_ids`
  line changed anywhere in the file -- so P2Q7's keying is what shipped
  originally, and P2Q4's fix is a visible-text swap that left the ident negated.
  The staged zip at /tmp/qtiwork/staged/ contains a byte-identical copy of the
  repaired XML, so what ships equals what I judged.

STRUCTURE AND MARKUP -- machine-checked on all 12 items of the current file

  exactly one `<respcondition>` per item, `setvar` action="Set" value 100;
  required ident set == the `correct_*` set and negated ident set == the
  `wrong_*` set on every item, with the union covering all eight choices (no
  choice left out of the scoring tree); 8 choices per item; no duplicate visible
  text within any item; no duplicate idents; `respident="response1"` on every
  `<varequal>` and `<response_lid ident="response1" rcardinality="Multiple">` on
  every item; `original_answer_ids` matches render order on all 12; `\(` and
  `\)` counts balanced in every stem and every choice; zero `$` characters in
  the entire package; no `$$`, no `\[`; exactly one "Canvas accuracy check"
  block per stem; no `<img>` and no `src=` anywhere, so the `media/` vs
  `$IMS-CC-FILEBASE$` question does not arise; all three XML files parse.
  assessment_meta declares points_possible 24.0 for 24 one-point items.

CANDIDATES RULED ON

  P2Q4 wrong_7 "1 exactly" -> CONFIRMED as a defect in the shipped original
    (5^0 = 1 restated verbatim, negated, all-or-nothing) and CLOSED by the
    applied fix: the text is now "25", false for 5^0 and unique in the item.
  P2Q7 keys both 9/8 and 1 1/8 where the key writes "or" -> CONFIRMED as a
    defect in the shipped original and CLOSED by the stem amendment, not by
    re-keying. Re-argued from first principles above; I reach the coordinator's
    conclusion independently and reject r1's proposed fix as a displacement.
  Audit's 12 Part 2 stem values (256, 9, 256, 1, 25, 81, 9/8, 100, 256, 36, 25,
    3125) -> CONFIRMED, recomputed from the stems and cross-read against the
    rendered key pages 5 and 6.

RULED ON, NOT DEFECTS (each is a ruling, not a note)

  Q1 wrong_1 "256 square feet" -- NOT the right value in different units. The
    banner area is 256 in^2 = 256/144 ft^2 = 1.78 ft^2; 256 ft^2 is 144x the
    true area. The statement is false and the negation is correct.
  Q2 the key writes "Part A: 3^4/3^2 (or equivalent)" and lists 3^(4-2) and
    3^2 as alternates, yet the item carries NO equivalent-form clause. Correct
    as is, and deliberately so: neither alternate is on offer among the
    choices, so there is no all-or-nothing "or" conflict to cure and adding the
    clause would promise forms the item does not contain. Q2 solves the same
    problem by offering one form; Q7 solves it by offering both and saying so.
    Both are sound; the apparent inconsistency between them is not a defect.
  Q2 non-keyed set worked: 3^(4+2) = 3^6 = 729 (adds instead of subtracts,
    false); 3^2/3^4 = 1/9 (inverted, false); "Part B: 3" (= 3^1, false, the
    quotient is 3^2); "Part B: 27" (= 3^3, false); -3^4/3^2 (false); 4^4/3^2
    (wrong base, false).
  Q3 stem adds "using the power-of-a-power property" where the assignment
    prints only "Evaluate: (2^4)^2 =". The clause names the correct property,
    introduces no number, and does not change the answer or the answerability;
    P1Q3 carries the identical clause, so it is house phrasing. Not a stem
    fidelity defect.
  Q1 and Q2 stems are narrativised relative to the assignment ("A person is
    designing a rectangular banner ..." for "Banner area is given by ..."). All
    numbers, operations, units and sub-part structure are preserved exactly.
    Not a defect.
  The boilerplate "Part 1 and Part 2 both must be correct when prompt has
    multiple parts" appears on all 24 items including single-part ones, and its
    "Part 1 / Part 2" wording collides with both the assignment's Part 1/Part 2
    columns and Q2's own Part A/Part B labels. I rule this NOT a defect: the
    sentence is conditional, it is unchanged from the shipped original, and on
    no item in this slice does it alter the set of choices a correct student
    must select -- on Q2, the only multi-part item here, it correctly conveys
    that both the Part A and the Part B choice are required.
  Q2 and Q7 choice texts use plain ASCII ("3^4 / 3^2", "9/8", "1 1/8") while
    the stems use `\(...\)`. Not a criterion-7 defect: there are no delimiters
    to be unbalanced or interleaved, nothing renders literally as broken
    markup, and the text is unambiguous as written.
  Q3 and Q9 both evaluate to 256 from different stems; Q5 and Q11 both to 25.
    Cross-item value repetition is not duplicate text within an item.
  Q5, Q6, Q8, Q10, Q11, Q12 non-keyed sets are sign-flips, off-by-one or
    off-by-two neighbours, zero, and trailing-zero variants of the true value.
    Every one evaluated as an exact Fraction; all false.

DEFECTS
  none standing.

CLEAN
  Part 2 Question 1
  Part 2 Question 2
  Part 2 Question 3
  Part 2 Question 4
  Part 2 Question 5
  Part 2 Question 6
  Part 2 Question 7
  Part 2 Question 8
  Part 2 Question 9
  Part 2 Question 10
  Part 2 Question 11
  Part 2 Question 12
