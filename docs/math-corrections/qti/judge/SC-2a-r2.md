SLICE: SC-2a          SCORE: 10/10
ITEMS WORKED: 12 of 12     (none skipped; re-worked from the amended raw XML,
not from the r1 notes and not from the slice cache, which predates the fix)

VERDICT: all three r1 defects are closed. No new defect was introduced. No
previously clean item moved.

WHAT THE FIX ACTUALLY CONTAINS (read from the amended XML, byte level)

  File mtime moved to 2026-08-06 00:01:49, size 123650 -> 123781 bytes
  (+131 = the two Part 1 stem insertions plus the one in Part 2, minus the
  Q4 choice-text delta). `assessment_meta.xml` and `imsmanifest.xml` are
  untouched at their original 2026-01-01 timestamps. Both files still parse
  as XML; the assessment still holds 24 items.

  1. sc_2_part_1_question_4_wrong_7 visible text is now `<p>1/7</p>`.
  2. Part 1 Question 7 and Part 1 Question 11 stems now read
     "Select every choice that belongs in complete correct answer, including
     every equivalent form of that answer."
  3. The clause occurs exactly 3 times in the file: P1Q7, P1Q11, P2Q7.
     The other 21 items retain the unmodified boilerplate.

CHECK 1 — does the amended stem make the two-form requirement derivable by a
student holding only the assignment? YES.

  The student computes 5^0 + 3^-2 + 2^(6+3-7) = 1 + 1/9 + 4 = 46/9 from the
  assignment alone. The selection rule now lives in the stem itself: it names
  "every equivalent form of that answer" as belonging. 46/9 and 5 1/9 are the
  same number, both are visible in the list, so the student ticks both and
  scores 100. Nothing outside the assignment is required — and the conversion
  between improper and mixed form is not an extra demand, it is the step the
  solution PDF itself performs ("Thus 1 + 1/9 + 4 = 5 1/9" before the Answer
  line writes "46/9 or 5 1/9"). Same for Q11: 1/36 + 8 = 289/36 = 8 1/36.

  Criterion 4 is now satisfied in both directions. A student whose homework
  says 46/9 and a student whose homework says 5 1/9 both hold an answer the
  key calls correct, and both are now instructed to a full-credit selection.
  Neither scores zero. The key's "or" is honoured: it governs what the
  student may have written, while the stem governs what they tick.

  The clause also cannot cause over-selection. "Equivalent" is a decidable
  arithmetic test, and every near miss in these two lists fails it by a
  checkable margin (below).

CHECK 2 — is `1/7` false for 7^0, and does it collide with anything in Q4?
YES false, NO collision.

  7^0 = 1 by the zero-exponent property. 1/7 = 7^-1, a different quantity;
  1/7 != 1. The stem asks only for 7^0, so 1/7 is not even a true statement
  answering a different question — it is a bare false value, the cleanest
  kind of distractor.
  Q4's eight choice values are 1, -1, 2, 0, 3, 10, 7, 1/7 — eight distinct
  rationals, so no duplicate visible text and no duplicate value. 1/7 is
  also pedagogically apt: it catches the student who confuses 7^0 with 7^-1,
  which is the live misconception at this lesson. The replaced string
  "1 exactly" no longer appears anywhere in the file.

CHECK 3 — did the nine clean items move? NO.

  All nine retain the original boilerplate verbatim and their original choice
  text. Re-verified structurally on every one of the 12: exactly one
  `<respcondition>`, `maxvalue="100"`, `respident="response1"`, 8 choices,
  required set == the `correct_*` idents, negated set == the `wrong_*` idents,
  `original_answer_ids` still lists all 8 ids on every item, no duplicate
  visible text, `\(...\)` balanced, zero `$` anywhere in the file, zero
  non-ASCII bytes, no images.

  Independent second path on criteria 2 and 3: I parsed every choice string
  on the 11 single-value items into an exact `Fraction` and compared it to the
  truth I recomputed from the stem, then compared "value equals truth" against
  "ident is in the required set". Mismatches: NONE on all 11. That means
  simultaneously that no keyed choice is false and no unkeyed choice is true —
  criteria 3 and 2 confirmed mechanically as well as by hand. Q2 is the
  multi-part item and was checked by hand: keyed `Part A: 2^4 / 2^2` and
  `Part B: 4`; the key's alternate Part A forms 2^(4-2) and 2^2 are not
  present as choices, so no equivalent form is exposed.

  Margins on the two near misses that most needed exact arithmetic:
    Q7  5 9/46 = 239/46, and 46/9 = 46/9. 239*9 = 2151 vs 46*46 = 2116. Unequal.
    Q11 8 1/35 = 281/35, and 289/36. 281*36 = 10116 vs 289*35 = 10115.
        Unequal by exactly 1/1260 — close enough that a decimal check to three
        places (8.0286 vs 8.0278) could mislead; the exact rational comparison
        settles it. Correctly unkeyed.
    Q11 290/36 = 145/18 = 8 2/36, unequal to 289/36. Correctly unkeyed.
    Q11 288/36 = 8, the value of (8/4)^3 alone — a true quantity answering a
        different question, still correctly unkeyed, and now explicitly safe
        under the amended stem because 8 is not an equivalent form of 289/36.

CHECK 4 — does the mixed stem wording (2 amended, 10 unamended in Part 1)
create an inconsistency defect? NO, and I want this on the record so the cold
judge does not have to rediscover it.

  The clause is only owed where an equivalent form is actually in the choice
  list. I swept all 12 Part 1 items for that condition: Q7 and Q11 are the
  only two where any choice is an alternate spelling of the keyed value. On
  the other ten, every non-keyed choice is a distinct number (or, in Q1, a
  distinct quantity — 729 square inches is 5.0625 square feet, so "729 square
  feet" is genuinely false, not the right value in other units). Adding the
  clause there would promise a selection that does not exist. The targeted
  application is correct, not inconsistent.

OUT-OF-SLICE OBSERVATION (reported, not scored — P2Q7 belongs to SC-2b)

  One correction to the record: I did not ask for the P2Q7 edit. My r1 report
  asked only that Q7 and Q11 be treated alike, both being Part 1 items. I flag
  this only so the decision trail stays accurate.

  Having said that, I checked the edit rather than assume it: P2Q7 is
  2^0 + 2^-3 = 1 + 1/8 = 9/8 = 1 1/8. It keys both `9/8` and `1 1/8`, and its
  unkeyed choices are 8/9, 1 9/8 = 17/8, 9/7, 1 7/8 = 15/8, -9/8, 10/8 = 5/4 —
  none equal to 9/8. So the amended stem there is both warranted (it is a
  genuine two-form key) and safe (it exposes no unkeyed equivalent). The edit
  does no harm to this package. SC-2b should still score it independently.

DEFECTS

  None. All three r1 defects are closed:
    Part 1 Question 4  | criterion 2 | CLOSED — `1 exactly` replaced by `1/7`,
      false for 7^0, distinct from all seven other choices.
    Part 1 Question 7  | criterion 4 | CLOSED — the stem now makes selecting
      both equivalent forms the derivable instruction, so no student holding
      either of the key's "or" forms can score zero.
    Part 1 Question 11 | criterion 4 | CLOSED — same, for 289/36 and 8 1/36.

CANDIDATES RULED ON

  P1Q4 wrong_7 "1 exactly"  -> CONFIRMED in r1, now REMEDIED and re-verified.
  P1Q7 / P1Q11 both-forms-keyed against an "or" key -> CONFIRMED in r1, now
    REMEDIED by stem amendment and re-verified in both directions.
  Audit stem-value list -> CONFIRMED in r1, re-confirmed here against the
    amended file: 729, 4, 4096, 1, 16, 64, 46/9, 49, 729, 1000, 289/36, 729.

CLEAN

  Part 1 Question 1
  Part 1 Question 2
  Part 1 Question 3
  Part 1 Question 4   (remediated, re-verified)
  Part 1 Question 5
  Part 1 Question 6
  Part 1 Question 7   (remediated, re-verified)
  Part 1 Question 8
  Part 1 Question 9
  Part 1 Question 10
  Part 1 Question 11  (remediated, re-verified)
  Part 1 Question 12

  All 12 of 12 clean. Nothing stands.

NOTE FOR THE PIPELINE (not a defect in the package)

  /tmp/qtiwork/slices/SC-2a.json is the pre-fix cache: it still carries
  `1 exactly` for sc_2_part_1_question_4_wrong_7 and the unamended Q7/Q11
  stems. It was correct when built and I did not touch it, but any downstream
  reader should re-parse the package rather than trust the cache. I scored
  this round off the raw XML for exactly that reason.
