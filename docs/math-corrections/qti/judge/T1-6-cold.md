SLICE: T1-6          SCORE: 10/10
ITEMS WORKED: 8 of 8     (none skipped)

Cold read. Shape A confirmed. Everything below was worked from the raw XML at
/tmp/qtiwork/pkg/topic-1-6-independent-practice-accuracy-check-qti/ and from the
rendered source PDFs, before opening T1-6-r1.md or T1-6-r2.md. Where I reached
the same conclusion as an earlier round I say so, but each conclusion here is
arrived at independently, not inherited.

SOURCES USED
  Assignment: Topic1IndependentPractice.pdf, Lesson 1-6 "Multiply Integers",
    page 3, read RENDERED at 200 dpi (the two built-up fractions extract as
    "4 12" / "3 12" under pdftotext -layout; rendered they are 4 1/2 and 3 1/2).
  Part 1 key: Topic1Part1Solutions.pdf page 4, read rendered.
  Part 2 key: Topic1Part2Solutions.pdf page 4, read rendered.
  Extractor: ElementTree, tags stripped with /<\/?[a-zA-Z][^>]*>/ FIRST and
    html.unescape SECOND; <not> blocks walked with a polarity flag rather than
    regexed, so negated varequals never enter the required list.

===============================================================================
THE REPAIRED CHOICE -- 1_6_part_1_question_1_correct_2
===============================================================================

Current text in the package:
    <p>Part B: -180 feet (below sea level)</p>

RULING: the repair genuinely resolves the defect. It does not paper over it, and
it agrees with the answer key exactly. Three independent paths, per the standing
rule.

The failure mode is real and I reconstructed it on its own terms first. In a bare
noun phrase, "-180 feet below sea level" makes "below sea level" a postmodifier
predicated of the signed quantity -180 feet. Sign and direction phrase then
compose: a displacement of -180 measured in the "below" direction is +180, i.e.
180 feet ABOVE sea level -- the exact opposite of the true position. Under
all-or-nothing scoring that keys a false statement (criterion 3).

Path 1 -- grammar. Parentheses change the part of speech the direction words
occupy. "-180 feet (below sea level)" sets them off as an appositive gloss on the
value, not as a second operator applied to it. The string then carries exactly one
direction assertion (the minus sign) and one annotation naming what that sign
already means. Nothing composes, nothing contradicts. This is a substantive
change, not cosmetic: it moves the phrase out of the operator position.

Path 2 -- the answer key, read rendered. Topic1Part1Solutions.pdf p.4 prints:
    Part B: (-15) x 12 = -180 feet (180 feet below sea level).
    Answer: Part A: -15; Part B: -180 feet (below sea level)
The repaired choice is character-identical to the key's Answer line (ASCII
hyphen-minus for the PDF's typographic minus, which is this package's uniform
convention: -15, -1 kilometer, -25, -36). The key's working line is the stronger
evidence: it expands the parenthetical to "(180 feet below sea level)", a full
restatement of the quantity. A parenthetical that restates the whole quantity is
by construction a gloss, not a modifier composing with it. Criterion 4 key
agreement is now exact, not approximate.

Path 3 -- the package's own internal convention, which settles the reading
without appeal to grammar. Part 1 Q2 offers "-1 kilometer (nearest km; descent)"
as the KEYED choice and "-1 kilometer (nearest km; ascent)" as a WRONG choice.
That pairing is only coherent if the parenthetical annotates and must AGREE with
the sign. If the parenthetical instead composed with the sign, the keyed choice
would be false (a negative value in the descent direction is an ascent) and
"1 kilometer (nearest km; descent)" would be the true one. The key rules that
branch out. The same annotate-and-agree convention applied to
"-180 feet (below sea level)" makes it true.

Arithmetic re-derived, not inherited: rate -15 ft/min, 12 min,
(-15) x 12 = -180 ft. Position -180 ft, i.e. 180 ft below sea level. The keyed
choice states that. TRUE.

Collision check: the repaired string is the only "Part B:" choice in the item;
the other seven are all "Part A:" followed by a bare integer (-15, 15, -14, -16,
-13, -17, 0). No duplicate visible text anywhere in the slice (checked all 8
items, 64 choices).

Scoring tree after the repair, re-parsed with <not> handled structurally: item
1_6_part_1_question_1 has exactly one <respcondition continue="No">,
<decvar maxvalue="100" minvalue="0" varname="SCORE">,
<setvar action="Set" varname="SCORE">100</setvar>, all respident="response1".
Required = {correct_1, correct_2}, both as bare <varequal> inside the <and>;
negated = {wrong_1 ... wrong_6}, each inside its own <not>. The edited ident is
unchanged and still sits in the required position. original_answer_ids still
lists all 8 idents in presentation order.

===============================================================================
THE PART 1 / PART 2 PHRASING ASYMMETRY -- RULED NOT A DEFECT
===============================================================================

The two parts do phrase the same construction differently:
  P1Q1 correct_2:  "Part B: -180 feet (below sea level)"   signed + parenthetical
  P2Q1 correct_2:  "Part B: 180 feet above sea level"      unsigned + prose

I checked both, and the asymmetry is sourced from the answer keys themselves.
Topic1Part2Solutions.pdf p.4 prints "Part B: 20 x 9 = 180 feet above sea level"
and "Answer: Part A: 20 (or +20); Part B: 180 feet above sea level". The QTI
choice is verbatim.

Critically, the double-sign failure mode CANNOT arise in the Part 2 form: the
numeral is unsigned, so there is only one direction assertion in the string to
begin with. "180 feet above sea level" = +180. TRUE. There is nothing for the
parenthetical device to fix there, which is why the two parts legitimately differ.

Criterion 1 asks for fidelity to the part named in the item title, not for
cross-part uniformity. Forcing either string into the other's shape would break
its agreement with its own key. House style, not a defect.

===============================================================================
ALL EIGHT ITEMS -- WORKED
===============================================================================

Part 1 Question 1 -- hiker, 15 ft/min descent, 12 min. Assignment p.3 Part 1
  column confirms 15 and 12. Part A: descent is negative, -15. Part B:
  (-15) x 12 = -180 ft. Keyed: "Part A: -15" and "Part B: -180 feet (below sea
  level)" -- both match the Part 1 key verbatim.
  Non-keyed, each worked: "Part A: 15" false (positive 15 would represent ascent;
  the key requires the negative for a descent -- note Part 2's key does permit an
  unsigned positive for an ascent, which is the mirror case, not this one);
  -14, -16, -13, -17, 0 all false. 8 choices, no Part B distractor offered, which
  is not a rubric violation.

Part 1 Question 2 -- RC plane, 250.50 m/s descent, 4 1/2 s (rendered page
  confirms the built-up fraction). (-250.50) x 4.5 = -1127.25 m = -1.12725 km,
  rounds to -1 km. Key: "-1 kilometer (nearest km; descent)". Keyed choice
  matches character for character.
  Non-keyed: "-1 meters (nearest km; descent)" false (the change is -1127.25 m,
  not -1 m); "-1 kilometer (nearest km; ascent)" false (annotation contradicts
  the sign); "1 kilometer (nearest km; descent)" -- WEAKER CASE, recorded and
  ruled below; "0 kilometer" false (1.12725 rounds to 1, not 0); "-2", "-3",
  "-10 kilometer" all false.

Part 1 Question 3 -- (-5)^2 = (-5)(-5) = 25. Key: 25. Keyed "25".
  Non-keyed -25, 26, 24, 27, 23, 0, 250 all false.

Part 1 Question 4 -- -5^2 = -(5^2) = -25. Key: -25, plus the Difference line
  "parentheses square the negative; without them, square first, then make
  negative". The three keyed choices are "-25", "Parentheses square negative
  base.", "Without parentheses, square first, then make negative." -- together
  they reproduce the key's value and both halves of its Difference sentence. The
  two halves are joined by a semicolon in the key, not by "or", so requiring both
  does not engage criterion 4's or-clause rule.
  Non-keyed: "25" false for -5^2 (it is Q3's value, and it is a bare numeral, not
  a true statement about a different question); "(-5)^2 = -25" false (equals 25);
  "-5^2 = 25" false (equals -25); "Square first in both expressions." -- WEAKER
  CASE, ruled below; "-24" false.

Part 2 Question 1 -- climber, 20 ft/min ascent, 9 min. Part A: +20. Part B:
  20 x 9 = 180 ft above sea level. Keyed "Part A: +20" and "Part B: 180 feet
  above sea level", both matching the Part 2 key.
  Non-keyed: "Part A: +-20" false (see candidate ruling below); +21, +19, +22,
  +18, +0 all false.

Part 2 Question 2 -- hot-air balloon, 180.25 m/s ascent, 3 1/2 s (rendered
  confirms). 180.25 x 3.5 = 630.875 m = 0.630875 km, rounds to 1 km. Key:
  "1 kilometer (nearest km; ascent)" -- exact match.
  Non-keyed: "1 meters" false; "1 kilometer (nearest km; descent)" false
  (annotation contradicts an ascent); "-1 kilometer (nearest km; ascent)" false;
  "2" false; "0 kilometer (nearest km; ascent)" false (0.630875 rounds to 1 --
  this is the truncation-error distractor and it is correctly wrong); "3", "10"
  false.
  Note for the record: the Part 2 key's "We Need" line says "Height after 3.5
  minutes" where the assignment says seconds. That is a slip in the key's prose
  only; its arithmetic and answer are right, and the QTI stem says seconds,
  matching the assignment. Not a QTI defect.

Part 2 Question 3 -- (-6)^2 = 36. Key: 36. Non-keyed -36, 37, 35, 38, 34, 0, 360
  all false.

Part 2 Question 4 -- -6^2 = -(6^2) = -36, plus the same two-part Difference
  statement. Non-keyed: 36, "(-6)^2 = -36", "-6^2 = 36", "Square first in both
  expressions.", -35 all false.

===============================================================================
STRUCTURE, MARKUP, IMPORT VALIDITY (criteria 6 and 7)
===============================================================================

Re-parsed independently, all 8 items:
  exactly 1 <respcondition> each; maxvalue="100"; setvar Set 100;
  respident="response1" on every varequal; 8 choices each (>= 8 satisfied);
  required set == correct_* set and negated set == wrong_* set on all 8, with
  <not> blocks walked structurally rather than regexed;
  original_answer_ids == the response_label ident list, in order, on all 8;
  no duplicate visible choice text within any item.

Markup: 0 "$" characters in the whole file; 6 "\(" and 6 "\)", balanced, one pair
per stem in Q2/Q3/Q4 of each part; every stem's mattext internally balanced. No
<img>, no src= attribute, no media directory, so the IMS-CC-FILEBASE question
does not arise. The instruction block "Canvas accuracy check: ..." appears
exactly once per stem (no duplication). imsmanifest.xml resolves both the QTI
resource and the assessment_meta dependency; both files exist. assessment_meta
points_possible 8.0 for 8 one-point items.

Shipping artifact: the staged zip
/tmp/qtiwork/staged/topic-1-6-independent-practice-accuracy-check-qti.zip is
byte-identical to the pkg directory on all three files (sha256 match each), so
what ships is what I judged.

===============================================================================
NOTHING OUTSIDE THE REPAIR MOVED
===============================================================================

FIXES_APPLIED.txt records exactly one T1-6 change (correct_2, "Part B: -180 feet
below sea level" -> "Part B: -180 feet (below sea level)"). I verified the claim
rather than accepting it: every one of the other 63 choice texts and all 8 stems
in the current XML match the texts enumerated in the r1 report's item-by-item
record, and the seven untouched items' idents, required/negated sets and
respcondition counts are unchanged. /tmp/qtiwork/slices/T1-6.json is post-fix
(it contains the parenthesised string) and agrees with the package, so it is no
longer usable as a pre-fix baseline -- I did not rely on it for the diff.

===============================================================================
CANDIDATES AND WEAKER CASES RULED ON
===============================================================================

  1_6_part_1_question_1_correct_2 "-180 feet ... below sea level" as originally
    written -> the underlying defect is CONFIRMED as having been real, and the
    applied repair is CONFIRMED as genuinely closing it (not displacing it).
    Reasoning above; the repaired text is the key's own text and is true under
    the package's own established annotation convention.

  P2Q1 wrong_1 "Part A: +-20" -> REFUTED as a defect.
    The rubric's "+-18" example bites only when the key's answer IS the
    plus-or-minus pair. The Part 2 key reads "Part A: 20 (or +20)", a single
    positive integer. A steady climber's unit rate is not plus-or-minus 20, so
    this is false and is a legitimate sign-confusion distractor. It contains no
    math delimiter, so criterion 7 is not engaged.

  P2Q1 criterion 4 or-clause test -> REFUTED as a defect.
    The key offers two acceptable forms, "20 (or +20)". Requiring both would be a
    defect. The item requires only "+20", and bare "20" is not offered as a
    choice at all, so no student holding an acceptable form is forced to a zero.

  WEAKER CASE (true arithmetic statement answering a different question):
    P1Q2 wrong_3 "1 kilometer (nearest km; descent)" -> NOT A DEFECT.
    Read as free prose, "a descent of 1 kilometer" is approximately true -- the
    plane descends 1.127 km. Ruled false because the stem asks for the CHANGE in
    height, which is signed, and because within this item the "(nearest km;
    <direction>)" string is a fixed annotation appended verbatim to all 8 choices
    and copied from the key's own answer line; the signed numeral carries the
    answer. "1 kilometer" is +1 km, and the change is -1 km. Recording it
    explicitly rather than merging it with the criterion-2 list, per the rubric.
    The symmetric case P2Q2 wrong_3 "-1 kilometer (nearest km; ascent)" is false
    for the mirror reason.

  WEAKER CASE: P1Q4 wrong_4 / P2Q4 wrong_4 "Square first in both expressions."
    -> NOT A DEFECT.
    On a hyper-literal reading the exponentiation is the first operation resolved
    in both (-5)^2 and -5^2. Ruled false because the item defines its own
    vocabulary in keyed choice 3, "Without parentheses, square first, then make
    negative" -- "square first" there means squaring the bare numeral before the
    sign is applied. Under that reading the sentence is false of (-5)^2, where
    the negative is part of the base, and it is exactly the no-difference
    misconception the stem asks students to refute.

  NOT SCORED, recorded: the boilerplate "Part 1 and Part 2 both must be correct
    when prompt has multiple parts" says Part 1 / Part 2 where these items label
    sub-parts Part A / Part B, and where the item titles use Part 1 / Part 2 for
    the assignment's two columns. I grepped the corpus: this exact sentence
    appears 88 times, i.e. on every Shape A item in all 14 packages. It is shared
    template text, not a T1-6 authoring fault; it duplicates nothing within a
    stem and leaves every item answerable. Ruled NOT a defect here; it belongs to
    whoever owns the template.

  NOT SCORED, recorded: the Q4 choices write exponents in ASCII ("(-5)^2 = -25")
    while the stems use \((-5)^{2}\). There are no math delimiters in those
    strings at all, so nothing renders as broken markup in Canvas and criterion 7
    is not engaged. Legible and unambiguous as plain text. Ruled NOT a defect.

===============================================================================
CLEAN
===============================================================================

  Part 1 Question 1 (post-repair), Part 1 Question 2, Part 1 Question 3,
  Part 1 Question 4, Part 2 Question 1, Part 2 Question 2, Part 2 Question 3,
  Part 2 Question 4.

All 8 items worked from the raw XML and re-derived against the rendered
assignment and both rendered answer keys. All 8 keyed sets reproduce their part's
key. All 56 non-keyed choices worked individually and every one is false. No
defect stands.

AGREEMENT WITH EARLIER ROUNDS: I reach the same verdict as r2 (10/10) and the
same reading of the repair, but by an independent route -- in particular the
Path-3 argument from the Q2 "(nearest km; ascent)" pairing, which forces the
annotate-and-agree convention from inside the package rather than from the key
alone, and the observation that the Part 2 form is immune to the double-sign
failure because its numeral is unsigned. I found no claim in r1 or r2 that does
not hold, and no defect that either round missed.

SCORE: 10/10
