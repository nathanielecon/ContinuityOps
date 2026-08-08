SLICE: T1-9          SCORE: 9/10
ITEMS WORKED: 4 of 4     (none skipped)

Shape A confirmed independently: 4 `multiple_answers_question` items,
`respident="response1"`, `correct_*` / `wrong_*` idents, 8 choices each, exactly
one `<respcondition>` per item with `maxvalue="100"` / `setvar 100`.

Read from the raw XML at
`/tmp/qtiwork/pkg/topic-1-9-independent-practice-accuracy-check-qti/`. No cache
used. The staged artifact
`/tmp/qtiwork/staged/topic-1-9-independent-practice-accuracy-check-qti.zip` was
SHA-256 compared entry-by-entry against the package directory: all three files
MATCH, so what I read is what students receive.

Nothing was repaired in this slice (`FIXES_APPLIED.txt` contains no 1-9 entry),
so every criterion below is scored from scratch.

---

DEFECTS

  Part 1 Question 1 | criterion 1 (stem fidelity) | item `1_9_part_1_question_1`, stem
    found:  "A business owner loses $450.75 as a result of a shipping delay. The
            3 owners of the business have to share the loss equally. Write the
            quotient that represents each person's share of the loss."
    why:    The assignment does not say this. Lesson 1-9 Part 1 Q1, read from a
            400 dpi render of assignment page 3, reads "A business loses $450.75
            due to shipping delay. The 3 owners share the loss equally."
            The subject of the first sentence is the business, not one owner.

            This is not a house-style expansion. This project has already
            formally identified this exact sentence as an error and published the
            correction. `docs/math-corrections/pdf/CorrectionsReport.pdf` carries
            the entry:

              p. 35  Low  inconsistency
              Where: Topic 1-9 Question 1 > Question block
              Found: A business owner loses $450.75 as a result of a shipping
                     delay. The 3 owners of the business have to share the loss
                     equally.
              Corrected to: A business loses $450.75 as a result of a shipping
                     delay. The 3 owners of the business have to share the loss
                     equally.
              Why: The first sentence attributes the whole loss to one owner,
                     then the next sentence says three owners share it; the loss
                     belongs to the business, not to a single owner.

            The correction was applied to the companion:
            `docs/math-corrections/tex/parts/t1e_E.tex` line 10 reads "A business
            loses \$450.75", and the rebuilt
            `docs/math-corrections/pdf/Topic1ExplanationsPart1.pdf` renders "A
            business loses $450.75". Only the QTI still carries the uncorrected
            sentence, so the accuracy check and the explanation companion a
            student reads beside it now disagree on the first line of the same
            question.

            Severity, stated plainly: the mathematics is untouched. $450.75 is
            still split 3 ways under either wording and the keyed answer
            -150.25 is correct. No student is led to a different number. This is
            a wording/consistency defect, not a key defect. I am recording it as
            a defect rather than a note because criterion 1 scores wording as
            well as numbers, the rubric forbids "10/10 with minor notes", and
            this particular wording has an independent documentary record inside
            this project calling it an error and supplying the replacement.

    fix:    In the `<mattext>` of item `1_9_part_1_question_1`, change
              &lt;p&gt;A business owner loses $450.75 as a result of a shipping delay.
            to
              &lt;p&gt;A business loses $450.75 as a result of a shipping delay.
            Two words only. Leave the rest of the stem, all 8 choices and the
            whole `<resprocessing>` block untouched.

  Part 2 Question 1 | criterion 1 (stem fidelity) | item `1_9_part_2_question_1`, stem
    found:  "A business owner loses $625.50 as a result of damaged inventory. The
            5 owners of the business have to share the loss equally. Write the
            quotient that represents each person's share of the loss."
    why:    Same defect, mirrored. The assignment (render of page 3, Part 2
            column) reads "A business loses $625.50 due to damaged inventory. The
            5 owners share the loss equally."

            The CorrectionsReport has no Part 2 entry for this sentence because
            there is no Part 2 explanations companion in the repository — the
            corrections pass only had a Part 1 document to correct. The absence
            of an entry is therefore not evidence that Part 2 is clean; the same
            one-owner/three-owners inconsistency is present, introduced by the
            QTI author templating Part 2 off Part 1. The published correction
            applies unchanged.

            Same severity: the key -125.10 is correct and unaffected.

    fix:    In the `<mattext>` of item `1_9_part_2_question_1`, change
              &lt;p&gt;A business owner loses $625.50 as a result of damaged inventory.
            to
              &lt;p&gt;A business loses $625.50 as a result of damaged inventory.

---

CANDIDATES RULED ON

  r1's candidate D ("the QTI stems are fuller prose than the assignment's terse
  phrasing; REFUTED as house style, and the topic-1-9 stem text matches the Topic
  1 Explanations (Part 1) document verbatim, so it is the sanctioned canonical
  wording rather than drift")
  -> PARTLY OVERTURNED. This is the one r1 ruling I disagree with.

  The general half is right and I confirm it: expansion is house style. topic-1-10
  P1Q1 expands the assignment's hiker line into "Two people are hiking. The first
  person climbs to the top of a peak that is 450 feet above sea level..." and that
  expansion introduces nothing false. Expansion alone is not a defect and I do not
  score it as one anywhere in this slice.

  The supporting half is drawn from a superseded document. r1's verbatim match was
  against
  `/tmp/claude-0/.../scratchpad/Topic1ExplanationsPart1.pdf` (308,307 bytes,
  timestamped 10:02) — the *original, uncorrected* source document, which is what
  the corrections pass was run against. The current companion is
  `docs/math-corrections/pdf/Topic1ExplanationsPart1.pdf` (356,001 bytes, 15:28),
  rebuilt from `tex/parts/t1e_E.tex`, and it reads "A business loses". So the
  stem does not match the sanctioned wording; it matches the wording that was
  sanctioned *against*. r1 read the stale file and drew the opposite conclusion
  from it. The four keyed answers r1 verified are all correct — the overturn is
  confined to candidate D.

  r1's candidate B ("4 rest stops" in P1Q2 and "6 water stations" in P2Q2 are
  right-value/wrong-noun distractors; REFUTED as criterion-2 defects)
  -> CONFIRMED REFUTED, and I reach it by a different route than r1 did.

  This is the trap the assignment brief named, so I worked it directly rather
  than accepting r1's reasoning. Two independent arguments, both of which have to
  fail before the choice becomes true:

  (a) Falsity under both readings. "4 rest stops": rest stops appear only in
      Part 2, where the count is 6. Read against Part 1 the object does not exist
      (the count of rest stops is 0); read against Part 2 the count is 6, not 4.
      "6 water stations": water stations appear only in Part 1, where the count
      is 4. False either way. Neither is true under any reading.

  (b) The noun is load-bearing in this corpus, on the project's own authority.
      `CorrectionsReport.pdf` carries "p. 5 Medium inconsistency / Lesson SC-2
      Question 2 Part B / Found: Part B: 9 cupcakes per friend / Corrected to:
      Part B: 9 muffins per friend / Why: Part 2's assignment item is muffins ...
      cupcakes belongs to the Part 1 item." A correct numeral under the wrong
      noun is treated here as a *Medium* error requiring correction, not as an
      equivalent form. That precedent is the strongest available evidence that
      "4 rest stops" is a genuinely false statement rather than "4" in different
      units, which is what criterion 2 would require.

  A noun swap is not a unit conversion. "5 feet" / "60 inches" name one quantity
  twice; "rest stops" and "water stations" name two different objects, only one of
  which exists in a given item. Not a defect.

  (I also checked the cupcakes/muffins defect itself against the QTI, since it is
  the same class: `topic-sc-2` P1Q2 uses cupcakes throughout and P2Q2 uses muffins
  throughout, both correctly. That defect lives in the solutions PDF only and has
  not leaked into any package. Null result, recorded so it is not re-checked.)

  Self-raised candidate: is "5 water stations" / "7 rest stops" defensibly true,
  i.e. does "and one at the finish line" add a station beyond the interval count?
  -> REFUTED, settled three ways.
    Exact arithmetic: (31/2) / (31/8) = (31/2) x (8/31) = 4, and
    (33/2) / (11/4) = (33/2) x (4/11) = 132/22 = 6. Both are exact integers, so
    the last interval endpoint lands exactly on the finish:
      P1 stations at 31/8, 31/4, 93/8, 31/2 — the 4th IS 15 1/2, the finish.
      P2 stops    at 11/4, 11/2, 33/4, 11, 55/4, 33/2 — the 6th IS 16 1/2.
    Therefore both readings of the QTI's "every ... along the route, and one at
    the finish line" give the same count: 4 route markers including the finish, or
    3 strictly-interior markers plus the finish, is 4 either way; 6 or 5+1 is 6
    either way. Reaching 5 or 7 requires double-counting the finish point.
    Both answer keys gloss it explicitly: Part 1 "Stations at the end of each
    interval (including finish) => 4"; Part 2 "Rest stops at the end of each
    interval (including finish) => 6". The Part 1 explanations document states it
    as a numbered step: "10. Stations are at the end of each interval, including
    the finish line. So there are 4 stations."
    So the ambiguity the QTI's rephrasing might have introduced is harmless: it
    cannot change the count. This is why I do not score the Q2 stems' expansion
    as a criterion-1 defect — unlike the Q1 stems, it introduces nothing false.

  Self-raised candidate: mixed/improper and unsimplified twins, the risk named in
  the assignment brief for a division-with-mixed-numbers lesson.
  -> REFUTED. Both division items resolve to integers (4 and 6), so no
  improper-vs-mixed pair can exist; the distractor sets are {3,5,8,-4,6,2} and
  {5,7,12,-6,8,4}, all plain integers, none equal to the key. Both money items
  resolve to terminating two-place decimals: -450.75/3 = -601/4 = -150.25 and
  -625.50/5 = -1251/10 = -125.10. The forms that would be defects if offered
  (-150 1/4, -601/4, -150.250, bare -150.25 with no noun; -125.1, -125.100,
  -1251/10) appear in no distractor. Every distractor was checked against the key
  as an exact rational, not as a string.

  Self-raised candidate: "the right value in the wrong unit" — `wrong_7`
  "-15025 per owner" (P1Q1) and "-12510 per owner" (P2Q1). In cents these are the
  correct amounts.
  -> REFUTED, recorded explicitly per the brief's warning about wrong-unit
  distractors. Neither choice names a unit. All eight choices in each item are
  bare numerals followed by "per owner", and the stem denominates the loss in
  dollars ($450.75, $625.50), so the implicit unit is dollars throughout and
  -15025 dollars is not -150.25 dollars. Reading one choice in cents while
  reading its seven siblings in dollars is not a reading a student performs.
  These are the standard misplaced-decimal-point distractors.

  Self-raised candidate (weaker case, criterion 2's second category — flagged as
  such rather than merged): `wrong_1` "150.25 per owner" (P1Q1) and "125.10 per
  owner" (P2Q1) are true statements about the *magnitude* of each owner's share.
  -> RULED NOT A DEFECT. The stem asks for "the quotient that represents each
  person's share of the loss", in a lesson titled Divide Rational Numbers. Both
  answer key sources model the loss as negative and give the signed value:
  `Topic1Part1Solutions.tex` `\ans{$-150.25$ (or $-\$150.25$ per owner)}` and
  `Topic1Part2Solutions.tex` `\ans{$-125.10$ (or $-\$125.10$ per owner)}`. The
  Part 1 explanations spell out the modelling step ("1. Write the loss as
  -450.75") and the sign rule ("opposite signs make a negative quotient"). The
  unsigned value is an answer to a different question and is the canonical sign-
  error distractor this lesson exists to test. It answers a different question
  and is therefore not a true-but-unkeyed choice.

  Criterion 4, the "or" trap: both keys write "-150.25 (or -$150.25 per owner)"
  and "-125.10 (or -$125.10 per owner)". These are two spellings of one value, and
  the QTI offers only one of them as a choice — there is no bare "-150.25" or
  "$-150.25" choice anywhere in the item. So the all-or-nothing scoring never
  requires a student to select both forms, and the trap that sank SC-2a/SC-2b does
  not arise here. Checked, not assumed.

---

VERIFICATION OF THE UNSCORED CRITERIA

  Criterion 3 (no false-but-keyed choice) — all four keys recomputed in exact
  rational arithmetic and confirmed against both key PDFs *and* their LaTeX
  sources, which is a path independent of any PDF rendering:
    `Topic1Part1Solutions.tex`: `\know{$\mixed{15}{1}{2} = \tfrac{31}{2}$,
      $\mixed{3}{7}{8} = \tfrac{31}{8}$.}` -> `\ans{$4$ water stations}`
    `Topic1Part2Solutions.tex`: `\know{$\mixed{16}{1}{2} = \tfrac{33}{2}$,
      $\mixed{2}{3}{4} = \tfrac{11}{4}$.}` -> `\ans{$6$ rest stops}`
  The LaTeX `\mixed{15}{1}{2}` settles the built-up fractions with no rendering
  step at all, which is the third path on the value `pdftotext -layout` mangles.
  Keys: -150.25 per owner / 4 water stations / -125.10 per owner / 6 rest stops.
  All four reproduce their answer key exactly. None is false.

  Criterion 5 (answerability) — each item's keyed value is exactly what the
  answer key produces from the assignment's own numbers. The QTI adds no option
  the assignment excludes and keys nothing the assignment cannot reach. The
  criterion-1 defect above does not impair answerability: under either wording the
  student divides the same total by the same number of owners.

  Criterion 6 (structure) — verified by parsing the `<respcondition>` tree with
  ElementTree and collecting `<not>` subtrees *before* reading the bare
  `<varequal>` set, so the negated-varequal trap is structurally avoided rather
  than avoided by luck. All four items: REQUIRED set == the `correct_*` ident set
  exactly; NEGATED set == the `wrong_*` ident set exactly; one respcondition;
  `respident` is `response1` on every varequal; 8 choices; 8 distinct visible
  texts (no duplicates in any item); `original_answer_ids` matches the rendered
  label order exactly in all four items.

  Criterion 7 (markup / import validity) — delimiters checked by walking every
  `\(`, `\)` and `$` in document order and asserting depth, not by counting:
  4 opens, 4 closes, never nested, never interleaved, final depth 0. The four
  math spans are `\(15\dfrac{1}{2}\)`, `\(3\dfrac{7}{8}\)`, `\(16\dfrac{1}{2}\)`,
  `\(2\dfrac{3}{4}\)`. The only two `$` characters are at depth 0 in
  "loses $450.75 as" and "loses $625.50 as" — currency, correctly left as literal
  text, and converting them would be a regression. No `\[`, no `$$`, no
  double-escaped entities. Exactly one "Canvas accuracy check" block per item
  (4 occurrences / 4 items — no duplicated instruction block), and its wording is
  byte-identical to the corpus-canonical block used by 85 of 88 topic items (the
  other 3 being the SC-2 equivalent-forms amendment). No `src=` attribute and no
  media directory anywhere in the package, so the `$IMS-CC-FILEBASE$` trap cannot
  arise. `imsmanifest.xml` declares the assessment resource plus the
  `assessment_meta.xml` dependency and both `href`s resolve to files that exist.
  `assessment_meta.xml` `points_possible` 4.0 matches 4 items at 1 point each.

---

CLEAN

  Part 1 Question 2 — clean on all seven criteria. Stem "A race is
    \(15\dfrac{1}{2}\) miles long ... every \(3\dfrac{7}{8}\) miles ... and one at
    the finish line" carries the assignment's numbers, verified from a 400 dpi
    render of page 3 and cross-checked against `\mixed{15}{1}{2}` /
    `\mixed{3}{7}{8}` in the Part 1 solutions LaTeX. Key "4 water stations"
    reproduces the answer key. All 7 distractors worked and false.

  Part 2 Question 2 — clean on all seven criteria. Stem numbers
    \(16\dfrac{1}{2}\) and \(2\dfrac{3}{4}\) verified by render and by
    `\mixed{16}{1}{2}` / `\mixed{2}{3}{4}` in the Part 2 solutions LaTeX. Key
    "6 rest stops" reproduces the answer key. All 7 distractors worked and false.

  Part 1 Question 1 and Part 2 Question 1 — clean on criteria 2, 3, 4, 5, 6 and 7.
    Keys -150.25 per owner and -125.10 per owner are correct and match both answer
    keys; all 14 distractors worked and false; structure and markup sound. The
    single defect in each is the criterion-1 stem wording recorded above.

---

NOTE, OUT OF RUBRIC — NOT SCORED AGAINST THIS SLICE

  `assessment_meta.xml` sets `<shuffle_answers>false</shuffle_answers>`, and in
  all 4 items of this slice the `correct_*` choices occupy the leading positions.
  I checked whether this is specific to T1-9: across all 88 Shape A items the
  correct choices are always the leading contiguous block (63 items with the key
  at position 0 alone, 11 at 0-1, 11 at 0-2, 3 at 0-3; zero exceptions). With
  shuffling off, "select the first N choices" passes every item in the corpus
  without doing any mathematics.

  This is a property of all 14 packages, not a T1-9 defect, and it is not one of
  the seven rubric criteria — scoring T1-9 down for it would be inconsistent with
  the 10/10 already recorded for T1-7 and T1-10, which share it. Raising it for
  whoever owns the corpus as a whole, since it is invisible from inside any single
  slice and would be closed by one setting.

---

VERDICT

  9/10. Two criterion-1 stem defects stand, in `1_9_part_1_question_1` and
  `1_9_part_2_question_1`. Both are wording-only: no key is wrong, no distractor
  is true, no item is unpassable, and the fix is two words in each of two stems
  with the replacement text supplied verbatim by this project's own published
  corrections report. Everything else in the slice is clean and was worked
  independently.

  I do not ratify r1's 10/10. Its arithmetic is correct and I reproduce all four
  of its keyed values, but its criterion-1 clearance rests on a comparison against
  a superseded revision of the explanations companion, and the current revision
  says the opposite.
