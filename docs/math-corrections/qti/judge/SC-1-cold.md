SLICE: SC-1          SCORE: 8/10
ITEMS WORKED: 4 of 4     (none skipped)

Cold read. Shape A confirmed from the raw XML: 4 `multiple_answers_question`
items, idents `..._correct_N` / `..._wrong_N`, one `<respcondition>` per item
with `maxvalue="100"` and `setvar 100`, 8 choices each, `respident="response1"`,
`shuffle_answers=false`, `points_possible 4.0` = 4 x 1.

METHOD

  Authoritative source only:
  `/tmp/qtiwork/pkg/topic-sc-1-independent-practice-accuracy-check-qti/`.
  Scoring read by walking the `<respcondition>` element tree with an XML parser,
  tracking `<not>` nesting depth, not by regex over the item. Choice text
  extracted by stripping real tags first (`</?[a-zA-Z][^>]*>`) and unescaping
  second, so `&amp;lt;` survives as `<` instead of being eaten. Slice and corpus
  JSON caches were used only to reconstruct history, never to score.

  Non-ASCII glyphs read by codepoint off the parsed file, not by shape:
  U+2264 (x2), U+2265 (x2), U+2260 (x2), U+2261 (x2), U+226A (x2), U+226B (x2).
  The tilde in both Question 2 items is U+007E ASCII TILDE, not U+223C.

  Assignment and both keys read from rendered pages at 300 dpi, cropped on the
  SC-1 block, never from `pdftotext` ordering. Rendered assignment page 2, both
  columns: Part 1 Q2 "Compare the fraction 3/4 (built up, 3 over 4) with the
  decimal 0.75. Select all symbols that appropriately relate the two numbers
  (<, >, =, !=)." Part 2 Q2 the same with 2/5 (2 over 5) and 0.4. Four symbols,
  in the order <, >, =, !=, in both columns. Rendered page 2 of both solution
  PDFs: "of the four symbols offered (<, >, =, !=) only = is true. Answer: =
  (only)."

  Repair scope established independently of the r1/r2 reports, by full-file diff
  of the pristine pre-repair package
  `/home/user/ContinuityOps/inbox/Inbox/topic-sc-1-...-qti.zip`
  (sha256 4f5f46845aa4) against the current package (sha256 9b19f165ffba, same
  as `staged/`). This is a stronger check than r1's prose record of untouched
  items.

THE THREE QUESTIONS PUT TO ME, SETTLED

  1. Could a student working from the assignment ever produce the original keyed
     set {=, <=, >=}?  NO.
     Read off the rendered page, the assignment's own symbol list for both
     Question 2 items is exactly (<, >, =, !=). `<=` and `>=` appear nowhere in
     the assignment. Both keys state the answer space explicitly ("of the four
     symbols offered") and both answer "= (only)". The pre-repair stem
     manufactured the extra options itself: it read
     `\(= \qquad < \qquad > \qquad \leq \qquad \geq \qquad \neq\)` - six symbols
     where the assignment gives four. So the original was a genuine criterion 5
     defect compounded by criteria 1 and 4, and it is correctly closed: the stem
     now reads `\(< \qquad > \qquad = \qquad \neq\)`, matching the assignment
     symbol-for-symbol and in the same order, in both items.

  2. Are the `<=` and `>=` choices gone entirely, not renamed?  YES, DELETED.
     The diff shows whole `<response_label>` elements removed. The idents
     `sc_1_part_1_question_2_correct_2`, `..._correct_3`,
     `sc_1_part_2_question_2_correct_2`, `..._correct_3` do not occur anywhere
     in the current file - not as a label, not in `original_answer_ids`, not in
     the scoring tree. Their two bare `<varequal>` lines were removed from the
     `<and>` rather than wrapped in `<not>`. Byte search over the whole file
     finds U+2264 and U+2265 exactly twice each, and both pairs live in the
     Question 1 items (`..._question_1_wrong_4`), which the diff proves were not
     touched by the repair. So no glyph was relocated into a neighbouring item.

  3. Are the replacements genuinely false, and is the scoring tree consistent?
     The two ADDED choices are genuinely false. But the parent brief's premise
     about which two were added is not what the diff shows, and the two that
     were left alone are the problem.

     Added by the repair: `<<` (U+226A, wrong_6) and `>>` (U+226B, wrong_7).
     Both entail strict inequality. 3/4 = 0.75 exactly and 2/5 = 0.4 exactly, so
     "much less than" and "much greater than" are false under every reading for
     both pairs. These are correct, well-chosen distractors.

     NOT added by the repair, and never removed: `~` (U+007E, wrong_4) and
     `=` with three bars, U+2261 (wrong_5). Both are present verbatim in the
     pristine pre-repair zip at the same idents. They are the defect recorded
     below.

     Scoring tree: internally consistent on all four items. Parsed with `<not>`
     depth tracked, required set equals the `correct_*` ident set and negated
     set equals the `wrong_*` ident set on every item, the two sets are disjoint
     and together cover all eight choices, every referenced ident exists, and
     `original_answer_ids` reproduces the eight idents in document order in all
     four items. One `<respcondition>` each. No duplicate visible text.

DEFECTS

  Part 1 Question 2 | criterion 2 | sc_1_part_1_question_2_wrong_5
  Part 2 Question 2 | criterion 2 | sc_1_part_2_question_2_wrong_5
    found:  <p>&#8801;</p>   (U+2261, rendered as the three-bar equals)
    why:    U+2261's own Unicode name is IDENTICAL TO, and its standard
            mathematical reading is "is identically equal to". 3/4 and 0.75 are
            two written forms of one rational number: 3 divided by 4 is 0.75
            exactly, with no remainder and no rounding, so they are identical,
            and the assertion is TRUE. Part 2 is the same: 2 divided by 5 is 0.4
            exactly, so 2/5 identical-to 0.4 is TRUE.
            I tried to find any reading under which it is false and could not.
            The only other standard reading is congruence, a = b (mod n). That
            reading needs a modulus the item does not supply, but supplying one
            does not rescue it: 3/4 - 0.75 = 0, and 0 is divisible by every n,
            so 3/4 = 0.75 (mod n) holds for every n. Likewise 2/5 - 0.4 = 0.
            There is therefore no completion of either standard reading that
            makes this choice false, while the rubric's criterion 2 requires me
            to "confirm it is false". I cannot. It is the rubric's enumerated
            case "the same value restated" - the `=` relation written in a
            second notation - sitting under a `<not>` block. A student who knows
            the symbol selects it, and under all-or-nothing scoring earns zero
            for reasoning correctly.
            This is precisely the harm that forced the deletion of `<=` and
            `>=` rather than their re-labelling. The r1 report's own words:
            delete them, "do not merely re-label them as `wrong_*`, because
            3/4 <= 0.75 and 3/4 >= 0.75 are true and would then become
            true-but-unkeyed distractors (criterion 2)." Note that r1 said this
            as part of a fix that simultaneously narrowed the stem's symbol list
            to four - so r1 held, correctly, that being outside the stem's
            enumerated space does not license leaving a true choice in place.
            r2 then saved `~` and the three-bar equals by invoking exactly the
            protection r1 had just rejected: "the stem now enumerates the answer
            space ... so a student is directed to a four-symbol space in which
            they do not sit." The package is now built on the strict standard
            for `<=` / `>=` and the lenient one for these two. Only one of those
            can be the corpus standard. The rubric supplies no out-of-scope
            exemption in criterion 2, and the deletion has already been paid
            for, so the strict standard governs and these two choices fail it.
            I also record that r2's mathematics here does not hold: r2 names
            "identical equality of expressions" as a reading and then concludes
            the choice asserts nothing - but 3/4 and 0.75 ARE two expressions,
            and under that named reading the assertion is true.
    fix:    Replace the visible text of `sc_1_part_1_question_2_wrong_5` and
            `sc_1_part_2_question_2_wrong_5` with U+2262, NOT IDENTICAL TO:
              <p>&#8802;</p>
            False under the identity reading (they ARE identical) and false
            under every congruence completion (the difference is 0), for both
            3/4 vs 0.75 and 2/5 vs 0.4. Text-only change: ident unchanged,
            `original_answer_ids` unchanged, `<respcondition>` unchanged, choice
            count stays 8, no collision with any other choice's text.
            Equally acceptable alternative: U+2271 NOT GREATER-THAN OR EQUAL TO
            (`&#8817;`), false because 3/4 >= 0.75 does hold.

  Part 1 Question 2 | criterion 2 | sc_1_part_1_question_2_wrong_4
  Part 2 Question 2 | criterion 2 | sc_1_part_2_question_2_wrong_4
    found:  <p>~</p>   (U+007E ASCII TILDE)
    why:    Recorded explicitly as the weaker of the two and ruled separately,
            per the rubric's instruction not to merge cases silently. This one
            is "cannot be confirmed false" rather than "demonstrably true".
            Readings, worked:
              - asymptotic equivalence, a ~ b: for two nonzero constants this
                holds exactly when a/b = 1. 0.75/0.75 = 1 and 0.4/0.4 = 1, so
                TRUE for both pairs. r2 cites this reading and then asserts it
                "asserts no numeric equality"; for constants it asserts exactly
                numeric equality, so r2's stated ground is inverted.
              - the everyday student reading, `~` as the keyboard stand-in for
                "approximately equal": exact equality entails approximate
                equality, so TRUE. The glyph here is U+007E, the plain keyboard
                tilde, not the mathematical U+223C, which makes the everyday
                reading the more likely one for a 7th-grade reader, not less.
              - geometric similarity: a category error applied to numbers, so
                undefined, not false.
            No reading yields FALSE. Criterion 2 asks me to confirm falsity and
            I cannot, so it fails the same test as the choice above, at lower
            confidence and lower real-world risk.
    fix:    Replace the visible text of `sc_1_part_1_question_2_wrong_4` and
            `sc_1_part_2_question_2_wrong_4` with U+2249, NOT ALMOST EQUAL TO:
              <p>&#8777;</p>
            False for both pairs, since the numbers are exactly equal and
            therefore certainly approximately equal. Text-only change, same
            no-collision and no-structural-change properties as above.
            Alternative: U+2270 NOT LESS-THAN OR EQUAL TO (`&#8816;`).

  Severity, stated plainly so the coordinator can weigh it: the closed defect
  would have zeroed essentially every student who answered correctly. This one
  will be selected by almost nobody, because almost no 7th grader knows either
  glyph. It stands anyway, because criterion 2's protected class is expressly
  "precisely the strongest students", the rubric forbids "10/10 with minor
  notes", and the fix is four characters with no structural consequence. If the
  coordinator prefers the lenient standard, the honest consequence is that the
  `<=` / `>=` deletion was never required either, and that should be stated
  rather than left as an unexamined split.

WEAKER CASES RECORDED AND RULED - NOT DEFECTS

  Part 1 Question 1 `wrong_5` = `-10.4 < 10.6`, Part 2 Question 1 `wrong_5` =
  `-9.3 < 9.8`. Both are true bare inequalities. Ruled NOT defects, and ruled
  rather than merged: the stem asks for statements comparing the two given
  weights, the cat weighs +10.4 lb and the dog +9.3 lb, and no weight in either
  stem is negative. These are true arithmetic answering a different question -
  the rubric's named weaker case. Independent of r1, same conclusion.

  Part 1 Question 1 `wrong_4` = `10.4 <= 10.6 and 10.6 <= 10.4`. FALSE as a
  whole: first conjunct true, second conjunct false (10.6 <= 10.4 fails), so the
  conjunction fails. Correctly negated. Part 2 Question 1 `wrong_4` =
  `9.3 >= 9.8 and 9.8 >= 9.3`: first conjunct false (9.3 >= 9.8 fails), so the
  conjunction fails. Correctly negated. Neither is a relocated remnant of the
  deleted Question 2 choices - the diff proves both items are byte-identical to
  the pre-repair package.

  Bare `<` in the stems after XML unescaping (`\(<\)`, `\(< \qquad > ...\)`)
  where the choice labels use the doubly-escaped `&amp;lt;`. NOT a defect. In
  HTML a `<` followed by a space or a backslash is not a tag open and is emitted
  as a literal character, so both spellings reach MathJax as `<`. The asymmetry
  is corpus-wide house style, present in the pristine package and in the two
  Question 1 stems, and outside this repair. Recorded so it is on the record,
  not scored.

CANDIDATES RULED ON

  P1Q2 / P2Q2 keyed `<=` and `>=` (correct_2, correct_3), criterion 5
    -> CONFIRMED as an original defect, and now RESOLVED. Verified along three
    independent paths: rendered assignment page lists four symbols; both
    rendered solution pages read "Answer: = (only)"; the current keyed set is
    {=} alone in both items.

  P1Q2 / P2Q2 stem lists six symbols where the assignment lists four
    -> CONFIRMED as an original defect, and now RESOLVED. Pre-repair stem
    carried `\leq` and `\geq`; current stem is `\(< \qquad > \qquad = \qquad
    \neq\)`, an exact match to the rendered assignment including order.

  P1Q1 / P2Q1 distractors `-10.4 < 10.6` and `-9.3 < 9.8`
    -> REFUTED as defects, for the reason recorded above.

CLAIMS FROM r1 / r2 ATTACKED

  r1 "delete, do not re-label" -> UPHELD, and verified as executed.
  r2 "`<<` and `>>` are false under any reading" -> UPHELD, worked independently.
  r2 "stem now matches the assignment's four symbols, including order"
    -> UPHELD, checked against a fresh 300 dpi render of both columns.
  r2 "nothing outside the repair moved" -> UPHELD, and upgraded from prose to a
    full-file diff against the pristine pre-repair zip. Only the two Question 2
    items changed; the two Question 1 items, `imsmanifest.xml` and
    `assessment_meta.xml` are byte-identical.
  r2 "`~` and the three-bar equals are not defects" -> OVERTURNED. See DEFECTS.
    The stated mathematical grounds are inverted in both cases, and the
    scope-based ground is the one r1 rejected for `<=` and `>=`.
  r2 score 10/10 -> OVERTURNED to 8/10.

CLEAN

  Part 1 Question 1 - stem numbers match the assignment (cat 10.4, rabbit 10.6);
    keyed {10.4 < 10.6, 10.6 > 10.4} reproduces Topic1Part1Solutions.pdf
    "Answer: 10.4 < 10.6 and 10.6 > 10.4 (pounds OK)", both conjuncts keyed, no
    "or" split to over-require. Every non-keyed choice worked and false or ruled
    above. 8 distinct choices, one respcondition, required = `correct_*`,
    negated = `wrong_*`, `original_answer_ids` in document order, `\(` and `\)`
    balanced 2 and 2, no `$`, one instruction block, no images.

  Part 2 Question 1 - same, with dog 9.3 and cat 9.8; keyed set reproduces
    Topic1Part2Solutions.pdf "Answer: 9.3 < 9.8 and 9.8 > 9.3 (pounds OK)".

  Part 1 Question 2 and Part 2 Question 2 - clean on criteria 1, 3, 4, 5, 6 and
    7 after the repair (stem faithful to the rendered assignment, keyed set {=}
    reproduces "= (only)", scoring tree consistent with the idents and
    `original_answer_ids`, 8 distinct choices, one respcondition, delimiters
    balanced, no images). They fail criterion 2 only, on `wrong_4` and
    `wrong_5`, as recorded.
