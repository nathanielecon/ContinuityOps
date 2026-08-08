SLICE: T1-4          SCORE: 10/10          (cold, independent second read)
ITEMS WORKED: 8 of 8     (none unworkable)

Shape A confirmed from the raw XML at
`/tmp/qtiwork/pkg/topic-1-4-independent-practice-accuracy-check-qti/topic_1_4_independent_practice_accuracy_check/topic_1_4_independent_practice_accuracy_check.xml`:
8 `multiple_answers_question` items, `..._correct_N` / `..._wrong_N` idents, one
`<respcondition>` per item at `maxvalue="100"` with `setvar` 100, 8 choices per
item. I did not read `/tmp/qtiwork/slices/*.json` or `corpus.json` as evidence.
Choice and stem text were taken by stripping real HTML tags first
(`</?[a-zA-Z][^>]*>`) and unescaping second. Both answer keys were read from
rendered pages (Part 1 p.3, Part 2 p.3, 160 dpi) and the assignment from a
rendered page (p.2, 150 dpi), not from `pdftotext` ordering.

DEFECTS

  None. Nothing stands.

MATHEMATICS WORKED

Criterion 2 is the primary hunt here and this lesson has more surface for it
than anywhere else in the corpus: six of the eight items key multiple
alternative expressions, and both keys close every "Valid:" list with "any
correct distance expressions", i.e. the lists are explicitly non-exhaustive. So
any offered non-keyed choice that is *also* a correct distance expression is a
defect even though the key does not name it. I evaluated all 64 choices from the
stem, not from the ident label.

  P1Q1 — 5 F at 6:00 PM, -8 F at midnight. Distance = |5 - (-8)| = 13.
    keyed (4):   |5 - (-8)| = 13 T
                 |-8 - 5| = |-13| = 13 T
                 5 - (-8) = 13 T           (bar-free, comes out positive)
                 |-8| + 5 = 8 + 5 = 13 T   (valid because the pair straddles 0:
                                            8 below zero plus 5 above zero)
    non-keyed (4): |5 - 8| = |-3| = 3 F
                   |-8 + 5| = |-3| = 3 F
                   -8 - 5 = -13 F   (negative; a distance is not -13)
                   5 + (-8) = -3 F
    No unkeyed true form. Specifically checked for the forms that would be true
    and are NOT offered, so cannot be a defect: 5 + |-8|, |5| + |-8|, |-8 - 5|
    duplicates. None present.
    Key (rendered): "Valid expressions include |5 - (-8)|, |-8 - 5|, 5 - (-8),
    |-8| + 5." Keyed set == key list, exactly, including the fourth form.

  P1Q2 — Bird A 150 ft, Bird B 120 ft, both above sea level. Distance = 30.
    keyed (3):   |150 - 120| = 30 T; |120 - 150| = |-30| = 30 T; 150 - 120 = 30 T
    non-keyed (5): 120 - 150 = -30 F
                   |150 + 120| = 270 F; 150 + 120 = 270 F
                   |150 - (-120)| = |270| = 270 F
                   |120 - (-150)| = |270| = 270 F
    The two "- (-120)" / "- (-150)" distractors are the sign-flip trap; both
    values are positive in the stem, so negating one is not a valid reading.
    Key: "Valid: |150 - 120|, |120 - 150|, 150 - 120." Exact match.

  P1Q3 — Fish A -25 ft, Fish B -40 ft. Distance = 15.
    keyed (3):   |-25 - (-40)| = |15| = 15 T; |-40 - (-25)| = |-15| = 15 T;
                 40 - 25 = 15 T
    non-keyed (5): |-25 - 40| = |-65| = 65 F; |-40 - 25| = |-65| = 65 F;
                   25 - 40 = -15 F; -25 + (-40) = -65 F; |-25 + (-40)| = 65 F
    Checked the shape that is keyed in Q1 and would be true here if offered: a
    bare `-25 - (-40)` = 15 is NOT among the choices, and `|-40| - |-25|` = 15 is
    NOT among the choices. Nothing true is left unkeyed.
    Key: "Valid: |-25 - (-40)|, |-40 - (-25)|, 40 - 25." Exact match.

  P1Q4 — elevator -3 -> 8 -> -1. Legs |8 - (-3)| = 11 and |-1 - 8| = 9;
         total 11 + 9 = 20.
    keyed (1):   20 floors T
    non-keyed (7): 20 feet, -20 floors, 21, 19, 22, 18, 0 floors — all F.
      -20 floors: a total travelled distance cannot be negative.
      0 floors: false under a net reading too, since net = |-1 - (-3)| = 2.
      19 / 21 floors: off-by-one on either leg; 18 / 22: off-by-two.
    Key: "|8 - (-3)| = 11 and |-1 - 8| = 9; 11 + 9 = 20. Answer: 20 floors."

  P2Q1 — 3 F at 7:00 AM, 12 F at noon. Distance = 9.
    keyed (3):   |12 - 3| = 9 T; |3 - 12| = |-9| = 9 T; 12 - 3 = 9 T
    non-keyed (5): 3 - 12 = -9 F; |12 + 3| = 15 F; 12 + 3 = 15 F;
                   |12 - (-3)| = 15 F; |3 - (-12)| = 15 F
    Asymmetry with P1Q1 checked deliberately: P1Q1 keys a fourth form (|-8| + 5)
    because that pair straddles zero. Here both temperatures are positive, so
    |12| + |3| = 15 is not the distance — and no such choice is offered anyway.
    Nothing true is left unkeyed.
    Key: "Valid: |12 - 3|, |3 - 12|, 12 - 3." Exact match.

  P2Q2 — Plane A 280 ft, Plane B 210 ft, both above sea level. Distance = 70.
    keyed (3):   |280 - 210| = 70 T; |210 - 280| = |-70| = 70 T; 280 - 210 = 70 T
    non-keyed (5): 210 - 280 = -70 F; |280 + 210| = 490 F; 280 + 210 = 490 F;
                   |280 - (-210)| = 490 F; |210 - (-280)| = 490 F
    Key: "Valid: |280 - 210|, |210 - 280|, 280 - 210." Exact match.

  P2Q3 — Submarine A -18 ft, Submarine B -45 ft. Distance = 27.
    keyed (3):   |-18 - (-45)| = |27| = 27 T; |-45 - (-18)| = |-27| = 27 T;
                 45 - 18 = 27 T
    non-keyed (5): |-18 - 45| = |-63| = 63 F; |-45 - 18| = 63 F; 18 - 45 = -27 F;
                   -18 + (-45) = -63 F; |-18 + (-45)| = 63 F
    Key: "Valid: |-18 - (-45)|, |-45 - (-18)|, 45 - 18." Exact match.

  P2Q4 — elevator -5 -> 6 -> -2. Legs |6 - (-5)| = 11 and |-2 - 6| = 8;
         total 11 + 8 = 19.
    keyed (1):   19 floors T
    non-keyed (7): 19 feet, -19 floors, 20, 18, 21, 17 floors, 0 floors — all F.
      0 floors is false under a net reading too: net = |-2 - (-5)| = 3.
      "20 floors" here is the correct answer to P1Q4, a different item; within
      P2Q4 it is 1 too many and correctly negated.
    Key: "|6 - (-5)| = 11 and |-2 - 6| = 8; 11 + 8 = 19. Answer: 19 floors."

  Criterion 3 (false-but-keyed): all 21 keyed choices evaluated above; every one
  equals the distance the key states. No double-signed phrasing anywhere in this
  slice — "beneath the water" is paired with a negative elevation and "above sea
  level" with a positive one on every item, so no stem asserts the opposite of
  its number.

WEAKER CASES RECORDED AND RULED ON EXPLICITLY

  "20 feet" (P1Q4 wrong_1) and "19 feet" (P2Q4 wrong_1) -> NOT a defect.
  These are the right *number* in a different unit, which the rubric's criterion
  2 list flags. Ruling: that bullet requires the alternate unit to be genuinely
  equivalent (3 ft / 36 in). Here it is not. Neither stem nor assignment gives a
  floor height, so "the elevator travels 20 feet" is not a restatement of "20
  floors" — it is a distinct and underdetermined claim, true only if a floor were
  exactly 1 ft. False, and a legitimate distractor. I reached this independently
  before reading r1, which rules the same way.

  Bar-free reversed differences kept as distractors (120 - 150, 3 - 12, 25 - 40,
  18 - 45, 210 - 280) -> NOT a defect. Each evaluates to the negative of the
  distance, and each key explicitly lists only the bracketed form plus the
  positive bar-free form. Consistent with the key, item by item.

CRITERION 4 AND 5 — the judgment call this slice turns on

  The assignment asks the student to "write at least two expressions"; the QTI
  requires selecting all 3 (or 4) valid ones under all-or-nothing. I considered
  ruling this a criterion-4 defect by analogy with the rubric's "or" trap, and I
  reject that reading on three grounds:
    (a) The keys do not join alternatives with "or". They write "Valid: A, B, C"
        and answer "any correct distance expressions" — all listed forms hold
        simultaneously; they are not competing renderings of one answer.
    (b) Criterion 2's own last bullet requires that for a select-all-equivalent
        stem *every* equivalent form be keyed. Keying only two of four would
        itself be the defect. The two criteria only cohere if all valid forms
        are keyed, which is what this package does.
    (c) The retained instruction block resolves the student's ambiguity
        directly: "Select every choice that belongs in complete correct answer."
  Criterion 5 answerability: a student holding only the assignment can evaluate
  each of the eight offered expressions and identify all valid ones; nothing in
  the keyed set requires information the assignment withholds. The two Q4 stems
  add "Floors above ground are positive and floors below ground are negative",
  which the assignment omits — this pins the reading the key already uses and
  removes an ambiguity rather than introducing an option the assignment excludes.
  Not a defect.

CRITERION 1 — stem fidelity, checked against the rendered assignment

  Assignment page 2, rendered, shows Lesson 1-4 as a two-column table. Column
  assignment verified visually so that no Part 1 / Part 2 transposition is
  possible: Part 1 carries 5 / -8, 150 / 120, -25 / -40, -3 / 8 / -1; Part 2
  carries 3 / 12, 280 / 210, -18 / -45, -5 / 6 / -2. Every QTI stem matches the
  part named in its own title. Wording differences are paraphrase only:
  "it dropped to -8 F" -> "the temperature was -8 F"; "it rose to 12 F" ->
  "the temperature was 12 F"; "Fish A is 25 ft below sea level (-25 ft)" ->
  "Fish A's elevation is -25 feet relative to sea level"; "ft" -> "feet"; added
  scene lead-ins ("Two birds are flying in the sky"). No numeric or semantic
  change in any of the eight.

CRITERION 6 — structure, parsed as a tree

  I walked `<conditionvar>` recursively and collected `<varequal>` into required
  vs negated by whether an enclosing `<not>` was crossed, rather than regexing
  the item — the trap the brief names. Result on all 8 items: exactly one
  `<respcondition>`; required set == the `correct_*` ident set; negated set ==
  the `wrong_*` ident set; 8 choices; no two choices with identical visible text
  within an item; `original_answer_ids` lists exactly the 8 idents in document
  order. Arithmetic cross-check on raw counts: 64 `<varequal>` = 21 required
  (4+3+3+1+3+3+3+1) + 43 negated (4+5+5+7+5+5+5+7), and the file holds exactly
  43 `<not>` elements. `points_possible` 8.0 in assessment_meta == 8 items x 1.

CRITERION 7 — markup and import validity

  8 "Canvas accuracy check" blocks for 8 items — exactly one per item. Zero
  occurrences of the deleted sentence "part of a correct solution" remain, in
  this package or anywhere in `/tmp/qtiwork/pkg/`. No empty `<p></p>` left by
  the removal. Delimiters: 14 `\(` and 14 `\)`, balanced per item; zero `$`,
  zero `\[` / `\]`; no `<img>`, no `media/` reference anywhere, so the
  `$IMS-CC-FILEBASE$` question does not arise. Zero non-ASCII bytes in the XML.
  All three package files parse as well-formed XML; the manifest declares the
  QTI resource plus the assessment_meta dependency and both hrefs resolve.
  The degree-symbol markup is stylistically uneven (`5\(^\circ\)F` keeps the
  numeral outside the math span, `\(-8^\circ\)F` puts it inside) but both are
  balanced `\(...\)` and both render as intended. Not a defect.

REPAIR AUDIT — did the fix displace the defect rather than close it?

  I verified this against a pre-repair baseline rather than against the r1/r2
  narrative. `/tmp/qtiwork/corpus_BROKEN.json` predates the fix and carries, per
  item, the full choice list, the `required` and `negated` ident lists,
  `n_respcondition`, `n_choices` and `images`. Diffing the repaired XML against
  it, item by item, all 8:
    - stem_new == stem_old with the duplicated block removed exactly once: TRUE
      on all 8 (on P1Q4 and P2Q4 the block was never present, so their stems are
      byte-unchanged — confirming they were not touched).
    - choice ident list and choice visible text: IDENTICAL on all 8. Nothing was
      replaced, so the brief's traps 1 and 2 (is a replacement genuinely false;
      does a replacement collide) have no surface in this slice — there are no
      replacements to attack.
    - `required` and `negated` lists: IDENTICAL on all 8, in order. The scoring
      tree did not move.
    - `n_respcondition` 1 -> 1 on all 8.
  Corroborated by mtime: only the assessment XML carries a post-fix timestamp;
  `imsmanifest.xml` and `assessment_meta.xml` are untouched. The repair was
  confined to deleting one paragraph from six stems and did nothing else.

CANDIDATES RULED ON

  r1's single defect — duplicated "Canvas accuracy check" instruction block on
  P1Q1, P1Q2, P1Q3, P2Q1, P2Q2, P2Q3 (criterion 7) -> CONFIRMED as having been
  real, and CONFIRMED RESOLVED. The pre-repair baseline still contains both
  paragraphs verbatim in those six stems and one paragraph in the two Q4 stems,
  exactly as r1 described; the repaired file has one block per item with no
  residue.

  r1's choice of which paragraph to keep -> CORRECT, verified independently.
  Counting the block across all 14 packages gives 85 items carrying "Select every
  choice that belongs in complete correct answer. Part 1 and Part 2 both must be
  correct when prompt has multiple parts. Select no incorrect choices." and 3
  carrying a longer "including every equivalent form" variant. The retained block
  is the corpus majority form; the deleted one occurred nowhere else.

  Original audit candidate "no mathematical defect despite this being a priority
  lesson" -> CONFIRMED independently. I worked all 64 choices from the stems and
  read both keys' "Valid:" lines from rendered pages before opening r1 or r2.

  r2's verdict of 10/10 -> AGREED, on my own evidence. I found no claim in r2
  that my own reading contradicts.

NON-SCORING OBSERVATIONS (recorded so they are not lost; neither is a rubric
defect and neither affects the score)

  1. `shuffle_answers` is false in `assessment_meta.xml`, and in every item the
     `correct_*` choices are listed before the `wrong_*` choices. A student
     therefore sees the keyed choices occupying the first 1-4 positions on all
     8 items. This is a position tell, not a correctness fault, it is corpus-wide
     rather than specific to T1-4, and it falls outside the seven criteria.
  2. The retained instruction block reads "belongs in complete correct answer",
     missing an article ("in a complete correct answer"). Corpus-wide across all
     85 instances; grammar, not a criterion-7 markup fault.

CLEAN

  Part 1 Question 1 — verified, no defect.
  Part 1 Question 2 — verified, no defect.
  Part 1 Question 3 — verified, no defect.
  Part 1 Question 4 — verified, no defect.
  Part 2 Question 1 — verified, no defect.
  Part 2 Question 2 — verified, no defect.
  Part 2 Question 3 — verified, no defect.
  Part 2 Question 4 — verified, no defect.

  All 8 items worked. Every keyed choice is true and reproduces the answer key's
  "Valid:" list exactly; every one of the 43 non-keyed choices is false; the
  scoring tree matches the ident sets on all 8; the repair removed only the
  duplicated paragraph and moved nothing else. No defect stands. 10/10.
