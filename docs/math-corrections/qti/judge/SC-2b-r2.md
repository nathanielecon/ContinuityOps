SLICE: SC-2b          SCORE: 10/10
ITEMS WORKED: 12 of 12     (Part 2 Questions 1-12; none skipped)
Round 2, re-scored against the package as it now stands on disk
(topic_sc_2_independent_practice_accuracy_check.xml, md5
2770dc03a1f7d56f34d4530a8ff6e2a8, 123781 bytes).

WHAT WAS ACTUALLY APPLIED (verified by diff against the pristine zip at
/home/user/ContinuityOps/inbox/Inbox/topic-sc-2-independent-practice-accuracy-check-qti.zip,
not by trusting the change note)

The whole file differs from the shipped original in exactly five places:
  1. Part 1 Q4 wrong_7  "1 exactly" -> "1/7"                (SC-2a's slice)
  2. Part 1 Q7  stem instruction gains ", including every equivalent form
                of that answer"                              (SC-2a's slice)
  3. Part 1 Q11 stem instruction gains the same clause        (SC-2a's slice)
  4. Part 2 Q4 wrong_7  "1 exactly" -> "25"                   (my slice)
  5. Part 2 Q7  stem instruction gains the same clause        (my slice)
Byte accounting closes exactly: 3 x (+48) for the clause, -7 for
"1 exactly"->"25", -6 for "1 exactly"->"1/7" = +131; 123650 + 131 = 123781.
Nothing else in Part 2 was touched: all twelve stems, choice texts, idents,
respconditions and `original_answer_ids` are byte-identical to what I worked
in r1, so the r1 mathematics stands unchanged. The clause was applied to all
three affected items across both parts, so the corpus teaches one rule, not
two.

RULING ON THE OVERRULE — P2Q7, criterion 4: DEFECT CLOSED. I do not maintain
my r1 finding.

  now reads: stem "Simplify \(2^0+2^{-3}\)." + "Canvas accuracy check: Select
             every choice that belongs in complete correct answer, including
             every equivalent form of that answer. ... Select no incorrect
             choices."
             required = {sc_2_part_2_question_7_correct_1 "9/8",
                         sc_2_part_2_question_7_correct_2 "1 1/8"}
  mathematics: 2^0 + 2^-3 = 1 + 1/8 = 9/8 = 1 1/8. Part 2 solutions PDF p.6:
             "Answer: 9/8 or 1 1/8".
  why it closes: criterion 4's defect is not the bare fact that two forms are
             both required — it is the harm it names, "a student who gives one
             acceptable form scores zero". That harm existed because the item
             silently asked the student to mark the single form they had
             written. The amended stem changes the task before the student
             answers: it is now "mark every correct form on offer", which is a
             task the student can complete no matter which form they wrote at
             home. Nothing the key licenses is punished.
             The rubric independently endorses this shape. Criterion 2's last
             bullet says that for a stem asking for equivalent forms, EVERY
             algebraically equivalent form counts as true — i.e. such a stem is
             expected to key them all. De-keying one (my r1 fix) would have
             produced the criterion-2 defect I flagged in r1 as the reason the
             item could not be repaired by re-keying alone; the coordinator's
             route removes the tension from the other side, and it does so
             without inventing a preference between two forms the key itself
             treats as interchangeable ("or", not "preferably").
  checked for the new exposure the amendment creates: with an explicit
             "every equivalent form" instruction, any unkeyed equivalent form
             would now be a much sharper criterion-2 defect. There is none.
             Against 9/8 = 1.125: 8/9 = 0.888..., 1 9/8 = 17/8 = 2.125,
             9/7 = 1.2857..., 1 7/8 = 15/8 = 1.875, -9/8 = -1.125,
             10/8 = 5/4 = 1.25. All six differ from 9/8; all six stay negated.
             The keyed set is exactly the set of equivalent forms present.
  criterion 1/5 unaffected: the amendment sits in the Canvas instruction
             block, not the math prompt; "Simplify \(2^0+2^{-3}\)" still
             matches the assignment (rendered p.4, Part 2 column) verbatim, and
             a student holding only the assignment can produce 9/8 or 1 1/8 and
             then recognise both on screen. One instruction block, not two;
             `<p>` tags balanced; the clause appears once.

P2Q4 FIX CONFIRMED, criterion 2 defect closed

  now reads: sc_2_part_2_question_4_wrong_7 = "25", still negated, ident
             unchanged, `original_answer_ids` still lists all 8 idents in
             render order.
  "25" is false for the stem: 5^0 = 1, not 25. 25 = 5^2, so it is the exact
  error of multiplying the base by the exponent-free reading (or of confusing
  5^0 with 5^2) — a plausible wrong answer, not a restatement of the key.
  No collision inside the item: the eight visible texts are
  1, -1, 2, 0, 3, 10, 5, 25 — all distinct, and "25" duplicates none of them.
  (25 is the keyed value of Part 2 Q5 and Q11, but those are separate,
  independently scored items with different stems; nothing carries across.)
  The "1 exactly" restatement that made this a defect in r1 is gone from the
  item entirely.

STRUCTURE AND MARKUP, RE-VERIFIED ON THE CURRENT FILE (all 12 items)
  exactly one `<respcondition>` per item; maxvalue="100" with setvar 100;
  required set == the `correct_*` ident set and negated set == the `wrong_*`
  ident set on every item; `original_answer_ids` matches the render order on
  every item; 8 choices per item; no duplicate visible text within any item;
  respident="response1" throughout; no `$` anywhere, `\(` and `\)` counts
  balanced per item; one instruction block per stem; no `<img>` and no media
  references; manifest unchanged and well formed.

MATHEMATICS, RECOMPUTED AGAIN FROM THE CURRENT STEMS (unchanged from r1)
  Q1 2^3 x 2^5 = 2^8 = 256 sq in     Q7  2^0 + 2^-3 = 9/8 = 1 1/8
  Q2 3^4/3^2 ; 81/9 = 9              Q8  10^5/10^3 = 10^2 = 100
  Q3 (2^4)^2 = 2^8 = 256             Q9  (4^2)^2 = 4^4 = 256
  Q4 5^0 = 1                         Q10 (2*3)^2 = 36
  Q5 5^(5-2+0-1) = 5^2 = 25          Q11 (15/3)^2 = 5^2 = 25
  Q6 81 * 36 / 36 = 81               Q12 5^3 * 5^2 = 5^5 = 3125
Every keyed choice is true, every non-keyed choice is false, and each keyed
set reproduces the Part 2 answer key (rendered p.6 of Topic1Part2Solutions.pdf).

DEFECTS
  none standing.

CANDIDATES RULED ON
  P2Q4 wrong_7 "1 exactly" -> CONFIRMED in r1, now REMEDIED: the text is "25",
    false for 5^0 and unique within the item.
  P2Q7 both 9/8 and 1 1/8 keyed against a key that writes "or" -> CONFIRMED in
    r1, now REMEDIED by stem amendment rather than by re-keying. I have
    re-argued it on the merits above and agree the harm criterion 4 names no
    longer occurs; keying both is now the instructed and only consistent
    behaviour.
  Audit's 12 Part 2 stem values (256, 9, 256, 1, 25, 81, 9/8, 100, 256, 36,
    25, 3125) -> CONFIRMED, recomputed a second time from the current file.

RULED ON, NOT DEFECTS
  Q1 wrong_1 "256 square feet" — not the right value in other units; 256 ft^2
    is 144x the banner's 256 in^2, so the statement is false.
  Q2 non-keyed set: 3^(4+2) = 729, 3^2/3^4 = 1/9, "Part B: 3", "Part B: 27",
    -3^4/3^2, 4^4/3^2 — all false. The key's other accepted Part A forms
    (3^(4-2), 3^2) are not on offer, so this item needs no equivalent-form
    clause and correctly did not get one.
  Q3 stem's added "using the power-of-a-power property" — house phrasing,
    identical on Part 1 Q3, names the correct property, changes no number.
  The generic "Part 1 and Part 2 both must be correct when prompt has multiple
    parts" boilerplate on single-part items is pre-existing corpus house text,
    present in the shipped original and unchanged by this fix round.
  Q5, Q6, Q8, Q10, Q11, Q12 distractors are off-by-one, sign-flipped, zero or
    trailing-zero variants; each recomputed and false.

CLEAN
  Part 2 Question 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 (all twelve)
