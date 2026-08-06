SLICE: SC-1          SCORE: 10/10
ITEMS WORKED: 4 of 4     (none skipped)

Second cold read, independent. I formed my view of all four items from the raw
XML, the rendered assignment and both rendered answer keys BEFORE opening
SC-1-r1.md, -r2.md, -r3.md or -cold.md. Where I reach the same conclusion as an
earlier reader I say so, but every conclusion below was reached first and
checked against theirs second.

Shape A confirmed from the raw XML: 4 `multiple_answers_question` items, idents
`..._correct_N` / `..._wrong_N`, `respident="response1"`, exactly one
`<respcondition>` per item carrying `setvar Set SCORE 100`, `maxvalue="100"` on
`<decvar>` in `<resprocessing><outcomes>` (correct location, not a defect),
8 choices per item, `points_possible 4.0` = 4 x 1, `shuffle_answers false`.

METHOD

  Authoritative source only:
  `/tmp/qtiwork/pkg/topic-sc-1-independent-practice-accuracy-check-qti/`.
  Scoring read by walking the `<respcondition>` element tree with an XML parser,
  toggling a negation flag on each `<not>` and recursing through `<and>`, never
  by regex over the item. Choice text extracted by stripping real HTML tags
  first (`</?[a-zA-Z][^>]*>`) and unescaping second, so the source `&amp;lt;`
  survives as `<` rather than being eaten by the tag stripper. The slice and
  corpus JSON caches were not read at all.

  Every non-ASCII glyph read by codepoint with its Unicode name resolved, never
  by shape. Full byte census of the shipping item XML:
    U+2249 NOT ALMOST EQUAL TO        x2
    U+2260 NOT EQUAL TO               x2
    U+2262 NOT IDENTICAL TO           x2
    U+2264 LESS-THAN OR EQUAL TO      x2
    U+2265 GREATER-THAN OR EQUAL TO   x2
    U+226A MUCH LESS-THAN             x2
    U+226B MUCH GREATER-THAN          x2
  No other non-ASCII character occurs anywhere in the file, and there are no
  numeric character references at all. U+007E and U+2261 occur ZERO times in the
  whole file, including metadata fields, so neither survives anywhere.

  Assignment and both keys read from RENDERED pages, cropped and zoomed on the
  SC-1 block at 200-900 dpi, never from `pdftotext` ordering. This mattered:
  `pdftotext -layout` renders the assignment's built-up fractions as `34` and
  `25`, renders the key's as `34`/`43` and `52`/`25` inconsistently within a
  single sentence, and renders the fourth symbol as `6=`. All four are
  extraction artefacts. The rendered pages settle them.

  Repair scope established by full-file diff against the pristine pre-repair
  package `/home/user/ContinuityOps/inbox/Inbox/topic-sc-1-...-qti.zip`, and by
  per-item canonical hashing of the serialised `<item>` elements.

SOURCES, READ OFF RENDERED PAGES

  Topic1IndependentPractice.pdf page 2, Lesson SC-1, both columns:
    Part 1 Q1  cat 10.4 lbs, friend's rabbit 10.6 lbs, "Write two different
               statements using the less than (<) and greater than (>) symbols
               that compare the weights."
    Part 2 Q1  dog 9.3 lbs, neighbor's cat 9.8 lbs, same wording.
    Part 1 Q2  fraction 3 over 4 (built up), decimal 0.75, "Select all symbols
               that appropriately relate the two numbers (<, >, =, ≠)."
    Part 2 Q2  fraction 2 over 5 (built up), decimal 0.4, same wording.
  THE ASSIGNMENT'S SYMBOL LIST IS EXACTLY FOUR SYMBOLS, in the order
  <, >, =, ≠ , in both columns. Read at 900 dpi cropped on the parenthesised
  list itself in each column. No ≤, ≥, ~, three-bar equals (U+2261), ≪, or ≫
  appears anywhere in the assignment.

  Topic1Part1Solutions.pdf page 2, rendered:
    Q1 "We Need: Two comparisons of 10.4 and 10.6." / "Answer: 10.4 < 10.6 and
       10.6 > 10.4 (pounds OK)"
    Q2 "We Solve: 3/4 = 0.75 exactly, so of the four symbols offered
       (<, >, =, ≠) only = is true." / "Answer: = (only)"
  Topic1Part2Solutions.pdf page 2, rendered: the same two entries with 9.3/9.8
  and with 2/5 and 0.4.

  Note for criterion 4: the Q1 key joins its two statements with "and", not
  "or". Requiring both under all-or-nothing scoring is therefore correct and is
  not the rubric's over-requiring case. I checked this specifically because
  criterion 4 makes an "or" split a defect.

THE FOUR QUESTIONS PUT TO ME, SETTLED INDEPENDENTLY

1. ARE `≉` (U+2249) AND `≢` (U+2262) GENUINELY FALSE FOR BOTH PAIRS?  YES.

   Both number pairs are pairs of equal numbers: 3 divided by 4 is 0.75 exactly,
   terminating, no remainder and no rounding; 2 divided by 5 is 0.4 exactly.
   So each choice must be evaluated as a relation asserted between a number and
   itself.

   U+2262 NOT IDENTICAL TO. I worked every reading of U+2261 that I could
   construct and negated each:
     - "is identically equal to": 3/4 and 0.75 are two spellings of one
       rational number, so they ARE identically equal, so "not identically
       equal" is FALSE. Same for 2/5 and 0.4.
     - congruence modulo m: the item supplies no modulus, so strictly this is
       not a proposition. Supplying one does not rescue it in the other
       direction either — the difference is 0 and every m divides 0, so the
       congruence holds for every m and the non-congruence is FALSE for every m.
       This reading strengthens the case rather than weakening it.
     - "is defined as": a definition, not a truth claim; yields no true reading.
     - logical equivalence: a relation between propositions, not numbers; a
       category error, undefined, not true.
   I also pressed the one reading that could make it true — U+2261 as
   "syntactically identical", under which 3/4 and 0.75 are different strings and
   so "not identical" would be TRUE. This does not stand. The stem asks for
   symbols that relate "the two NUMBERS", so value semantics govern, not glyph
   semantics. And it is self-defeating: under glyph semantics the keyed `=`
   would fail too, yet both answer keys say `=` is the answer. No student can
   coherently hold that `=` is true and U+2262 is also true. FALSE under every
   applicable reading.

   U+2249 NOT ALMOST EQUAL TO. The negation of U+2248. Under the standard
   convention `≈` is a tolerance relation — `a ≈ b` iff |a - b| is within
   tolerance — and it is reflexive, since |a - a| = 0 lies within every
   tolerance. So `3/4 ≈ 0.75` is TRUE and `3/4 ≉ 0.75` is FALSE; likewise for
   2/5 and 0.4.

   I was asked to TEST the previous judge's rejection of the strained reading
   rather than adopt it, so I state the strained reading at its strongest and
   then dismantle it. Strongest form: "almost" in ordinary English is
   exclusive ("almost finished" implies not finished), so `≈` could be read as
   "approximately but NOT exactly equal"; under that reading `3/4 ≈ 0.75` fails
   and `3/4 ≉ 0.75` comes out TRUE. Four independent grounds defeat it:

     (a) It requires `≈` to be IRREFLEXIVE. No standard defines it that way.
         Approximate equality is universally introduced as a reflexive and
         symmetric (non-transitive) tolerance relation; reflexivity is its
         defining first property. There is no source that makes `a ≈ a` false.
     (b) U+2249 is defined as the plain negation of U+2248, exactly as
         `\napprox` is of `\approx`. A negation holds precisely when the base
         relation fails. With the difference at 0, the base relation is
         satisfied in its most extreme case, so the negation fails.
     (c) The reading is foreclosed by the answer keys, which scope the question
         explicitly: "of the four symbols offered (<, >, =, ≠) only = is true."
         U+2249 is not among the four under any reading.
     (d) The decisive test, and the one I would apply to any candidate defect
         here: WHICH DIRECTION DOES THE HARM GRADIENT RUN? Criterion 2's
         protected class is "precisely the strongest students". The strained
         reading requires MORE sophistication than the plain one, and any
         student sophisticated enough to know U+2249 at all knows that `≈` is
         reflexive. So the stronger the student, the LESS likely they select it.
         That is distractor behaviour, not defect behaviour. The contrast with
         the three-bar equals that was removed is exact and it runs the other
         way: the stronger the student, the MORE likely they selected that one.

   The rejection holds. Both replacements are genuinely false, not merely
   different. The repair closed the defect rather than displacing it.

2. ARE `≪` (U+226A) AND `≫` (U+226B) FALSE FOR BOTH PAIRS?  YES.

   `a ≪ b` entails `a < b` under every reading — the usual reading adds a
   magnitude condition on top of strict inequality, which only makes it harder
   to satisfy. 3/4 < 0.75 is false because they are equal, so `3/4 ≪ 0.75` is
   false. `≫` entails `>`, and 3/4 > 0.75 is false, so `≫` is false. 2/5 and
   0.4 are equal, so both fail identically. No reading of "much less than"
   or "much greater than" is satisfied by a number and itself, since the gap
   is 0. FALSE for both pairs.

3. THE SEAM: `-10.4 < 10.6` AND `-9.3 < 9.8`. I PRESSED IT. THE DISTINCTION
   HOLDS, AND THESE ARE NOT DEFECTS.

   State the problem honestly first. `-10.4 < 10.6` is a TRUE inequality, full
   stop, and it sits under a `<not>` block. If the standard that convicted the
   three-bar equals is "every offered checkbox must be false on its own merits",
   then this one fails that standard and Q1 carries a true-but-unkeyed choice in
   both parts. That is the strongest form of the objection and it deserves an
   answer, not an assertion.

   The answer is that the two cases differ STRUCTURALLY, not in strictness, and
   the difference is in what a choice supplies to the proposition:

     In Question 2 the choice supplies THE RELATION and the stem supplies BOTH
     OPERANDS. A bare symbol has no truth value; to evaluate any Q2 checkbox at
     all you must plug it into the frame `3/4 __ 0.75`, and that frame is fixed
     by the stem. So EVERY Q2 checkbox is necessarily a candidate answer to the
     exact question posed, and there is no way to evaluate one that is not
     answering that question. Truth is therefore necessary AND SUFFICIENT for
     membership in Q2's answer set. Any true Q2 choice is a defect, always.

     In Question 1 the choice supplies A WHOLE STATEMENT, operands included.
     `-10.4 < 10.6` is self-contained; you do not need the stem to evaluate it.
     But membership in Q1's answer set requires two properties, not one:
     (a) the statement is true, and (b) its operands ARE the cat's weight and
     the rabbit's weight. `-10.4 < 10.6` has (a) and fails (b). Truth is
     necessary but NOT sufficient in Q1.

   Constraint (b) is not a judge's post-hoc rescue. It is in the answer key
   verbatim: "We Need: Two comparisons OF 10.4 AND 10.6." It is in the
   assignment: "statements ... that compare the weights", the weights being the
   cat's and the rabbit's. And it is in the QTI stem: "compare the weight of the
   cat and the rabbit." The cat weighs +10.4 pounds. -10.4 is not any object's
   weight in this problem, and weight is not a negative quantity.

   Two tests confirm (b) is load-bearing rather than convenient:

     REDUCTIO. If (b) were not a constraint, then any true inequality whatever
     would "belong in the complete correct answer" — `1 < 2`, `0 < 100`,
     `11.4 > 10.6`. Every numeric distractor in a "write a statement" item that
     happened to be true of some other numbers would become a defect, and the
     item type would be unbuildable. Dropping the analogous constraint in Q2
     collapses nothing, because Q2's operands are already pinned by the stem.
     So the asymmetry is forced by the item structure, not chosen.

     TWIN DISTRACTOR. `11.4 < 10.6` is the same family — operand perturbed
     rather than relation perturbed — and it happens to be false. Had the author
     written `11.4 > 10.6`, which is true, nobody would call it a defect,
     because 11.4 is not the cat's weight. That shows (b) does independent work.

   HARM GRADIENT, the same test I applied in (1). Would a strong student select
   `-10.4 < 10.6`? No — a strong student knows the cat weighs 10.4 pounds and
   recognises the leading minus as the sign error the distractor is testing. The
   stronger the student, the less likely they select it. The three-bar equals ran
   the opposite way: only a student who knew the symbol could select it, and
   knowing it made selection MORE likely. The two gradients point in opposite
   directions, which is the sharpest available discriminator, and it is decisive.

   Recorded explicitly, as criterion 2's closing paragraph requires, as the
   weaker "true arithmetic statement that answers a different question" case,
   ruled separately and not merged with the enumerated true-choice cases.
   REFUTED as a defect. I reach this independently and agree with the earlier
   readers, but on the structural ground above rather than on assertion.

4. IS A THIRD PAIR STILL GETTING THE LENIENT TREATMENT?  NO. THERE IS ONE
   CANDIDATE AND IT CLEARS.

   I swept all 32 choices across the 4 items, not only the repaired ones. Exactly
   one further place in the slice has a TRUE sub-statement sitting inside an
   unkeyed choice, and it is the pair the repair did not touch:

     Part 1 Q1 wrong_4  `10.4 ≤ 10.6 and 10.6 ≤ 10.4`  (U+2264 twice)
     Part 2 Q1 wrong_4  `9.3 ≥ 9.8 and 9.8 ≥ 9.3`      (U+2265 twice)

   Worked. Part 1: first conjunct 10.4 ≤ 10.6 is TRUE; second conjunct
   10.6 ≤ 10.4 is FALSE because 10.6 > 10.4; the conjunction is FALSE.
   Part 2: first conjunct 9.3 ≥ 9.8 is FALSE because 9.3 < 9.8; second conjunct
   9.8 ≥ 9.3 is TRUE; the conjunction is FALSE. Note the two are built with
   the false conjunct in opposite positions, so neither is a copy-paste of the
   other and both were checked separately.

   The residual risk is real and I name it: each contains a visible true clause
   (`10.4 ≤ 10.6` compares exactly the cat's and the rabbit's weights and is
   true). But the choice is one checkbox whose visible text is a conjunction
   joined by "and", not "or", and selecting it asserts both conjuncts. Under the
   ordinary reading it is false, so correct reasoning rejects it. It is also
   independently out of scope, since both stems restrict the student to `<` and
   `>`. NOT a defect.

   This pair is, in my reading, the interesting one: it is the SAME ≤ / ≥
   glyphs that had to be deleted from Q2, and here the author neutralised them
   by conjoining each with a false clause instead of deleting them. That is the
   strict standard applied, not the lenient one — the glyphs were made false
   rather than left true. So the slice is now uniform: every unkeyed choice in
   all four items is either outright false, or (in the one `-10.4 < 10.6` /
   `-9.3 < 9.8` pair) true of numbers the question does not name. There is no
   third pair.

REPAIR SCOPE — NOTHING OUTSIDE THE REPAIR MOVED

  Full-file diff and per-item hashing against the pristine pre-repair package:
    sc_1_part_1_question_1   3fc501dd5f5ae033 -> 3fc501dd5f5ae033   identical
    sc_1_part_1_question_2   92c7a730a97628c1 -> 5f19b79b857f1429   CHANGED
    sc_1_part_2_question_1   2462bcc08dee6d49 -> 2462bcc08dee6d49   identical
    sc_1_part_2_question_2   5d705c63786263b3 -> a345c3c60a02f6b4   CHANGED
  `imsmanifest.xml` and `assessment_meta.xml` byte-identical to pristine.
  So the two Question 1 items — including the -10.4 / -9.3 distractors I ruled
  on above — are original and were never touched by any of the three repair
  rounds. No glyph was relocated out of Question 2 into a neighbouring item:
  U+2264 occurs only in `sc_1_part_1_question_1_wrong_4` and U+2265 only in
  `sc_1_part_2_question_1_wrong_4`, both pre-existing.

  The changed region is exactly: the two Q2 stems' symbol paragraphs (six
  symbols -> four), deletion of the `correct_2` / `correct_3` response_labels
  and of their two bare `<varequal>` lines, addition of `wrong_6` / `wrong_7`
  with their `<not>` blocks, replacement of the `wrong_4` and `wrong_5` visible
  text, and the corresponding `original_answer_ids` rewrite. Choice count held
  at 8 throughout.

  Shipping artefact verified: `staged/topic-sc-1-...-qti.zip` unpacks
  byte-identical to `pkg/`. Item XML sha256 c6385a16d13da9fc...

SCORING TREE, PARSED PROPERLY

  Walked the element tree with a negation flag toggled at each `<not>`, so
  `<varequal>` inside `<not>` is never counted as required. All four items:
    required set   == the `correct_*` ident set exactly
    negated set    == the `wrong_*` ident set exactly
    the two sets are disjoint and together cover all 8 response_labels
    no label unmentioned, no mentioned ident missing from the labels
    `original_answer_ids` reproduces the 8 idents in document order
    exactly one `<respcondition>`, `continue="No"`, `setvar Set SCORE 100`
    `<decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>`
  Per-item keyed sets: Q1s {correct_1, correct_2}; Q2s {correct_1}.

CRITERION-BY-CRITERION

  1 Stem fidelity. All numbers match the correct part: 10.4 / 10.6 in Part 1 Q1,
    9.3 / 9.8 in Part 2 Q1, 3/4 and 0.75 in Part 1 Q2, 2/5 and 0.4 in Part 2 Q2,
    all confirmed against the rendered page. Part 1 and Part 2 are not
    transposed. "lbs" rendered as "pounds" and "compare the weights" expanded to
    "compare the weight of the cat and the rabbit" are faithful, and the
    expansion is if anything more explicit about the referents. Both Q2 stems
    reproduce the assignment's four symbols in the assignment's own order.
  2 No true-but-unkeyed choice. 32 choices in the slice, 6 keyed, so 26
    non-keyed, all worked individually. 24 are outright false. The remaining 2
    are the `-10.4 < 10.6` / `-9.3 < 9.8` pair, ruled above as the rubric's
    named weaker category. PASSES.
  3 No false-but-keyed choice. 10.4 < 10.6 TRUE; 10.6 > 10.4 TRUE;
    9.3 < 9.8 TRUE; 9.8 > 9.3 TRUE; 3/4 = 0.75 TRUE; 2/5 = 0.4 TRUE. No
    double-signed phrasing anywhere in this slice.
  4 Key agreement. Q1 keyed pairs reproduce "10.4 < 10.6 and 10.6 > 10.4" and
    "9.3 < 9.8 and 9.8 > 9.3"; the key says "and", so requiring both is right,
    not over-requiring. Q2 keyed {=} reproduces "= (only)" in both parts.
  5 Answerability. A student holding only the assignment sees four symbols,
    computes 3/4 = 0.75 exactly, and produces `=` alone — which scores 100. For
    Q1 they produce the two comparisons and score 100. No keyed answer lies
    outside what the assignment offers. The four extra symbols offered as
    checkboxes lie outside the assignment's list, but they are all false, so
    they cannot mislead a correct reasoner in either direction; they are
    distractors, not manufactured options the student must adjudicate.
  6 Structure. Exactly one `<respcondition>` per item; every `correct_*`
    required by a bare `<varequal>`; every `wrong_*` negated; 8 choices per item
    (meets the >= 8 bar); 8 distinct visible texts per item, verified by
    codepoint — the Q2 sets are U+003D, U+003C, U+003E, U+2260, U+2249, U+2262,
    U+226A, U+226B, eight distinct characters with no collision. `≠`, `≉` and
    `≢` share a family resemblance but are three different codepoints, so the
    duplicate-visible-text bar is not touched; and since all three are unkeyed
    and all three are false, a student who confused them still selects none.
  7 Markup. `\(` count equals `\)` count in every stem; no `$` anywhere in the
    file; one "Canvas accuracy check" instruction block per stem, none
    duplicated; no images, so nothing to resolve to `$IMS-CC-FILEBASE$`.

RECORDED, EXAMINED, NOT SCORED

  The Q1 and Q2 stems carry a bare `<` after XML unescaping (`\(<\)` and
  `\(< \qquad > ...\)`) while the choice labels use the doubly-escaped
  `&amp;lt;`. I checked whether this is an SC-1 anomaly and it is not: a raw `<`
  that does not open a tag appears in the stems of `topic-1-1` (`\(a < 0\)`,
  `\(q < 0\)`) and of `6th-grade-review-section-1` (H4, H5, H6), and in seven
  choice labels in `6th-grade-review-section-1`. It is corpus-wide house style,
  it predates the repair, and it renders: in HTML a `<` followed by a character
  that is not a letter, `/`, `!` or `?` is emitted as a literal character rather
  than opening a tag, so both spellings reach MathJax as `<`. NOT a defect.

CANDIDATES RULED ON

  P1Q2 / P2Q2 keyed `≤` and `≥` (correct_2, correct_3), criterion 5
    -> CONFIRMED as an original defect, now RESOLVED. Verified three ways:
    rendered assignment lists four symbols; both rendered keys read "= (only)";
    current keyed set is {=} alone and the two idents are absent from labels,
    `original_answer_ids` and the scoring tree alike.
  P1Q2 / P2Q2 stem listed six symbols where the assignment lists four
    -> CONFIRMED as an original defect, now RESOLVED. Diff shows the stem
    changed from `\(= \qquad < \qquad > \qquad \leq \qquad \geq \qquad \neq\)`
    to `\(< \qquad > \qquad = \qquad \neq\)`, an exact match to the rendered
    assignment including order. `\leq` and `\geq` occur zero times in the file.
  P1Q1 / P2Q1 distractors `-10.4 < 10.6` and `-9.3 < 9.8`
    -> REFUTED as defects, on the structural ground worked in section 3.

EARLIER RULINGS ATTACKED

  cold "the three-bar equals (U+2261) is true and must go" -> UPHELD, worked
    independently. I could construct no reading making it false, and the one
    reading that could (glyph identity rather than value identity) is
    self-defeating because it would also convict the keyed `=`.
  cold "U+007E tilde cannot be confirmed false" -> UPHELD. Under both the
    asymptotic reading (a/b = 1 for equal nonzero constants) and the everyday
    "approximately equal" reading it comes out true, so it could not stand.
  cold "the package applied a strict standard to one pair and a lenient one to
    the other" -> UPHELD as a description of the pre-repair state, and now
    RESOLVED. The strict standard is applied uniformly in the current file.
  cold's ruling that `-10.4 < 10.6` is NOT a defect -> UPHELD, but I reached it
    on my own structural ground (which property a choice supplies to the
    proposition, plus the reductio and the harm-gradient test) rather than by
    adopting its predicate argument. Having pressed it as instructed, I find the
    predicate argument sound but incompletely defended in the earlier reports;
    the reductio and the harm-gradient test are what make it safe.
  r3 "U+2249 is false under the standard and the everyday reading" -> UPHELD in
    conclusion. One correction to its reasoning, which does not change the
    outcome: r3 argues the strained reading is held "only by a student who
    simultaneously holds the everyday reading and its negation". That is not
    quite right — the strained reading is a different, exclusive reading of
    `≈`, not a contradiction. The rejection stands on the firmer grounds I set
    out in section 1 (irreflexivity is unattested, U+2249 is the plain negation
    of U+2248, the keys scope the answer space to four symbols, and the harm
    gradient runs the safe way).
  r3 score 10/10 -> UPHELD, independently.

CLEAN

  Part 1 Question 1 — stem numbers match the assignment (cat 10.4, rabbit 10.6);
    keyed {10.4 < 10.6, 10.6 > 10.4} reproduces Topic1Part1Solutions.pdf
    "Answer: 10.4 < 10.6 and 10.6 > 10.4 (pounds OK)", key joins with "and" so
    both are properly required; all six non-keyed choices worked, five false and
    one ruled as the weaker category; 8 distinct choices, one respcondition,
    required set = `correct_*`, negated set = `wrong_*`, `original_answer_ids`
    in document order, delimiters balanced, no `$`, one instruction block, no
    images. Byte-identical to the pristine package.

  Part 2 Question 1 — the same with dog 9.3 and cat 9.8; keyed set reproduces
    Topic1Part2Solutions.pdf "Answer: 9.3 < 9.8 and 9.8 > 9.3 (pounds OK)".
    Byte-identical to the pristine package.

  Part 1 Question 2 — stem faithful to the rendered assignment including the
    four-symbol list and its order; keyed {=} reproduces "= (only)"; all seven
    non-keyed choices (U+003C, U+003E, U+2260, U+2249, U+2262, U+226A, U+226B)
    worked and FALSE for 3/4 vs 0.75 under every reading tested; structure and
    markup sound.

  Part 2 Question 2 — the same for 2/5 vs 0.4; all seven non-keyed choices FALSE
    under every reading tested; keyed {=} reproduces "= (only)".

  No defect stands. The repair closed the defect the first cold judge found
  rather than displacing it, and it did not introduce a new one.
