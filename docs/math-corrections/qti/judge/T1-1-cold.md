SLICE: T1-1          SCORE: 10/10
SHAPE: A (Topic 1, multiple_answers_question, all-or-nothing)
ITEMS WORKED: 8 of 8     (none skipped)
ROUND: cold independent validation. All 8 items worked from the raw XML and the
rendered sources BEFORE T1-1-r1.md or T1-1-r2.md was opened.

METHOD

  Authoritative read: pkg/topic-1-1-independent-practice-accuracy-check-qti/
  topic_1_1_independent_practice_accuracy_check/*.xml, read in full.
  slices/*.json and corpus.json were never consulted.

  Choice and stem text extracted with a real HTML parser (html.parser,
  convert_charrefs=True) applied to the XML-decoded mattext, i.e. tags stripped
  by a parser and entities resolved second. This is immune to the truncation
  trap: both Q2 stems survive intact through "\(a < 0\)" / "\(q < 0\)".

  Scoring tree parsed as a tree, not by regex: a recursive walk over
  conditionvar that flips polarity on every <not>, so a varequal inside <not> is
  recorded as negated and never as required.

  Assignment page 1 and page 1 of both solution PDFs read RENDERED at 150 dpi,
  not extracted, so no fraction or sign depends on extraction order.

SOURCES CHECKED

  Assignment, Lesson 1-1 grid, rendered: P1 - submarine rises 18 m from a point
  below sea level then descends 18 m; a and b with a < 0, b > 0, a + b = 0;
  Evaluate |-9|; Order from least to greatest -3, 8, -1. P2 - hiker descends
  24 m from a trail marker then climbs 24 m; p and q with p > 0, q < 0,
  p + q = 0; Evaluate |-11|; Order from least to greatest 6, -2, 4.

  Part 1 key, Lesson 1-1, rendered: Q1 "Part A: +18 + (-18) = 0; Part B: equal
  magnitude and opposite signs, so the two changes cancel"; Q2 "|a| = |b| (or
  equivalent)"; Q3 "9"; Q4 "-3, -1, 8".

  Part 2 key, Lesson 1-1, rendered: Q1 "Part A: (-24) + 24 = 0; Part B: equal
  magnitude and opposite signs, so the two changes cancel"; Q2 "|p| = |q| (or
  equivalent)"; Q3 "11"; Q4 "-2, 4, 6".

DEFECTS

  None. No defect stands in this slice.

THE THREE REPLACED DISTRACTORS, WORKED FROM THE STEM AND PROVED FALSE

  This is the stated main exposure. Each was worked from the stem alone, before
  the repair reports were read, and each is false for EVERY assignment of values
  admitted by its stem - not merely for typical values.

  1_1_part_1_question_1_wrong_1  "+18 and +18"
    Stem: a submarine rises 18 m, then descends 18 m; Part A asks for both
    changes as signed numbers. Rise is positive, descent is negative, so the
    pair is (+18, -18) and the sum is 0. The choice asserts the second change is
    +18. Then the sum would be +18 + 18 = +36 != 0, and the submarine would have
    risen twice, contradicting "then descends 18 meters". FALSE.
    It is false on the exact feature the item tests, the sign of a descent, so
    it cannot be reached by correct reasoning.
    The two ways this replacement could have displaced the defect instead of
    closing it were both checked and neither occurred: the text is not
    "18 and -18" (a bare 18 reads as +18, which with -18 would be the key and
    therefore TRUE), and it is not "-18 and +18" (the same two signed numbers
    reordered, defensible as an unordered pair and therefore arguably true).
    The literal bytes in the XML are "+18 and +18". No "+-" survives anywhere in
    the package (0 occurrences), so no un-typeset +/- ambiguity remains.

  1_1_part_1_question_2_wrong_4  "|a| = 2|b|"
    Stem constraints: a < 0, b > 0, a + b = 0. From a + b = 0, a = -b, hence
    |a| = |-b| = |b| = b, and b > 0 so |b| > 0.
    Suppose the choice held: |a| = 2|b|. Substituting |a| = |b| gives
    |b| = 2|b|, so |b| = 0, so b = 0. That contradicts b > 0. Therefore no pair
    (a, b) satisfying the stem satisfies the choice. FALSE, universally over the
    stem's admissible set.
    It is an equation about absolute values, so it is the same species as the
    keyed answer and reads as a plausible distractor rather than an obvious
    throwaway.
    Not equivalent to, and not implied by, any keyed statement. It does imply
    wrong_6 "|a| != |b|", but both are false, so no reasoner can be punished by
    the overlap.
    The r1 defect is genuinely closed, not relocated: the string "a + b = 0"
    does not appear in any response_label anywhere in the package. It appears
    only in the P1Q2 stem, where it belongs as a hypothesis. So the stem-given,
    key-equivalent truth is no longer being negated by the scoring tree.

  1_1_part_2_question_2_wrong_4  "|p| = 2|q|"
    Stem constraints: p > 0, q < 0, p + q = 0. From p + q = 0, q = -p, hence
    |q| = |-p| = |p| = p, and p > 0 so |p| > 0.
    Suppose |p| = 2|q|. Substituting |q| = |p| gives |p| = 2|p|, so |p| = 0, so
    p = 0, contradicting p > 0. FALSE, universally.
    "p + q = 0" likewise appears only in the P2Q2 stem, never as a choice.

  Collision check on all three replacements: none collides with another choice's
  visible text or value. Checked mechanically over all 64 choices in the slice
  after parser-stripping tags and resolving entities - zero duplicate visible
  strings in any item. "|a| = 2|b|" is distinct from "|a| = |b|"; "|p| = 2|q|"
  is distinct from "|p| = |q|"; "+18 and +18" is distinct from "+18 and -18" and
  from all six other choices in P1Q1.

THE FOURTH REPAIR: THE P2Q4 STEM

  1_1_part_2_question_4 stem now reads
    "Order from least to greatest: \(6,\ -2,\ 4\)"
  Package-wide: 18 "\(" and 18 "\)", balanced; 0 "$" characters in the entire
  file. Expected total is 18 (7 in each Q2 stem, 1 each in P1Q3, P1Q4, P2Q3,
  P2Q4), so exactly one pair was added and no other delimiter was disturbed.

  The displacement risk specific to this repair was checked and did not occur.
  A fixer touching this math span could have "helpfully" written the sorted
  sequence, which would make the stem give away its own answer. It did not: the
  span carries 6, -2, 4 - the assignment's presentation order - and NOT the
  key's answer -2, 4, 6. Stem and key remain distinct, and the stem still
  matches the rendered assignment exactly.

NOTHING OUTSIDE THE REPAIR MOVED - VERIFIED INDEPENDENTLY

  I did not take r2's hash on trust; I reproduced the test from the r1 report's
  own record of the pre-fix strings.

  Current XML md5 7f0e265464039ca13110f679acf7b337, 42020 bytes.
  Each of the four post-fix strings occurs EXACTLY ONCE in the file, so no
  search-and-replace could have hit a collateral site.
  Reverting exactly those four strings to the four texts r1 recorded as "found"
  yields md5 10e0265a5295ee7324e876edb7f66bfa - byte-identical to the original
  r1 recorded. Therefore no other byte of the file moved: no stem, no ident, no
  response_label, no respcondition, no metadata field.

  The +3 byte delta is confirmed by independent character arithmetic:
    "+-18 and -18" (12) -> "+18 and +18" (11)          = -1
    "a + b = 0" (9)     -> "|a| = 2|b|" (10)           = +1
    "p + q = 0" (9)     -> "|p| = 2|q|" (10)           = +1
    "$6,\ -2,\ 4$" (11) -> "\(6,\ -2,\ 4\)" (13)       = +2
                                                  net = +3   (matches)

  imsmanifest.xml and assessment_meta.xml both parse and are consistent with the
  item file. staged/topic-1-1-...-qti.zip is byte-identical to the pkg directory
  on all three files, and its sha256
  0333a1b97224049fb7003a9716f54cf3c6b2ec4d33678f85105c08d81f360905 matches the
  recorded line in staged/sha256sums.txt.

CRITERION-BY-CRITERION, ALL RE-ATTACKED COLD

  1. Stem fidelity - all 8 stems match the rendered Lesson 1-1 grid for the part
     named in the title, checked word by word, not only on the numbers:
     P1Q1 18 m submarine rising from below sea level then descending, Parts A
     and B present and in that order; P1Q2 a, b with a < 0, b > 0, a + b = 0,
     asking for an equation about the absolute values; P1Q3 |-9|; P1Q4 -3, 8, -1
     in the assignment's order. P2Q1 24 m hiker descending from a trail marker
     then climbing; P2Q2 p, q with p > 0, q < 0, p + q = 0; P2Q3 |-11|;
     P2Q4 6, -2, 4 in the assignment's order.
     The only wording differences are "18 m" -> "18 meters" and "where a < 0"
     -> "We are told that \(a < 0\)". Neither changes content, a value, or a
     sign. No Part 1 / Part 2 number is crossed over: the 18/24, -9/-11 and
     {-3,8,-1}/{6,-2,4} pairs sit in the correctly titled items.

  2. No true-but-unkeyed choice - every one of the 56 non-keyed choices worked
     individually:
     P1Q1: +18 and +18 (false, above); +19, +17, +20, +16 each paired with -18 -
           every first addend is wrong, sums +1, -1, +2, -2, none is the pair
           (+18, -18). All false.
     P1Q2: |a| > |b| false and |a| < |b| false, since |a| = |b|; a = b false
           since a < 0 < b; |a| = 2|b| false (proved above);
           |a| + |b| = 0 false, since |a| + |b| = 2b > 0; |a| != |b| false.
     P1Q3: -9, 10, 8, 11, 7, 0, 90 - |-9| = 9, none of these is 9.
     P1Q4: 3,-1,8 / -2,-1,8 / -4,-1,8 / -1,-1,8 / -5,-1,8 / 0,-1,8 / -30,-1,8 -
           the required multiset is {-3,-1,8}; none matches, each substitutes a
           value not in the stem's set.
     P2Q1: 24 and +24 (ruled below); -23, -25, -22, -26 each with +24 - every
           first addend is wrong, none is the pair (-24, +24). All false.
     P2Q2: mirror of P1Q2 under p > 0, q < 0; identical rulings, all false.
     P2Q3: -11, 12, 10, 13, 9, 0, 110 - |-11| = 11, none of these is 11.
     P2Q4: 2,4,6 / -1,4,6 / -3,4,6 / 0,4,6 / -4,4,6 / -20,4,6 / 5,4,6 - the
           required multiset is {-2,4,6}; none matches.
     No unsimplified-equivalent, alternative-form, restated-value, different-
     units or bare-value-versus-"n = value" case exists anywhere in the slice;
     every choice in this slice is a bare value, a signed pair, an ordered
     triple, or an (in)equality, and each was compared against the key in the
     key's own form.

  3. No false-but-keyed choice - every keyed choice worked:
     P1Q1 "+18 and -18" (rise +18, descent -18), "sum 0" (+18 + (-18) = 0),
     "equal magnitude and opposite signs" (Part B, |+18| = |-18| = 18, signs
     opposite). P1Q2 "|a| = |b|" (a = -b so |a| = |b|). P1Q3 "9". P1Q4
     "-3, -1, 8" (-3 < -1 < 8). P2Q1 "-24 and +24", "sum 0",
     "equal magnitude and opposite signs". P2Q2 "|p| = |q|". P2Q3 "11".
     P2Q4 "-2, 4, 6" (-2 < 4 < 6). All true.
     No double-signed phrasing anywhere in this slice: no keyed choice pairs a
     negative sign with a direction word, so the "-96 feet below sea level"
     failure mode has no instance here.

  4. Key agreement - each keyed set reproduces its key exactly.
     P1Q1 key "Part A: +18 + (-18) = 0; Part B: equal magnitude and opposite
     signs" decomposes to exactly the three keyed choices, and all three are
     required, which is correct because the key's answer has both parts.
     P2Q1 likewise from "(-24) + 24 = 0".
     P1Q3 9, P2Q3 11, P1Q4 -3, -1, 8, P2Q4 -2, 4, 6 - exact.
     The only "or" in either key is the "(or equivalent)" hedge on Q2 of each
     part. This is an allowance for alternative forms, not two required forms,
     so it does not trigger the criterion-4 both-forms-required defect. I then
     tested the allowance directly: I checked each of the 7 non-keyed choices in
     P1Q2 and in P2Q2 for equivalence to the keyed equation under the stem's
     constraints. None is a true equivalent form. So no equivalent form is being
     negated, and the "(or equivalent)" allowance is no longer contradicted.

  5. Answerability from the assignment - every keyed set is producible by a
     student holding only the assignment. No item offers an option the
     assignment does not support, and no keyed answer depends on anything
     outside the Lesson 1-1 grid.

  6. Structure (Shape A) - re-counted mechanically for all 8 items from the
     parsed tree with <not> blocks separated: exactly one respcondition per item
     (8 total); decvar maxvalue="100" minvalue="0" varname="SCORE";
     setvar Set SCORE 100, continue="No"; respident="response1" on every
     varequal; 8 response_labels per item (64 total, so the >= 8 floor holds
     everywhere); the required set equals the correct_* ident set exactly and
     the negated set equals the wrong_* ident set exactly, on all 8 items; no
     varequal references a nonexistent ident; no choice is omitted from the
     scoring tree; original_answer_ids matches the render_choice order
     ident-for-ident in every item. Zero duplicate visible texts across all 64
     choices.

  7. Markup and import validity - 0 "$" characters in the file; \( and \)
     balanced at 18/18; the only tags used anywhere are <p> and <strong>; the
     one non-ASCII character is U+2260 "!=" appearing twice, legitimately, in
     the two "|a| != |b|" / "|p| != |q|" choices. No <img> and no "media/"
     reference anywhere, so there is no $IMS-CC-FILEBASE$ exposure to check.
     The "Canvas accuracy check" instruction paragraph appears exactly once per
     stem - no duplicated instruction block. All three package files are
     well-formed XML; the manifest's two resource hrefs both resolve to files
     that exist; assessment_meta points_possible 8.0 matches 8 items at 1 point,
     and shuffle_answers is false, so authored choice order is what students
     see.

WEAKER CASES RECORDED AND RULED (per rubric criterion 2, kept separate)

  These are choices that are arguably true statements but answer a different
  question. They are recorded explicitly and ruled, not silently merged with the
  defect list. I reached both rulings before reading r1 or r2.

  P1Q2 wrong_7 and P2Q2 wrong_7  "sign reversed"
    -> NOT A DEFECT. The underlying idea is true of the numbers: the stem gives
       a < 0 and b > 0, so the two do have reversed signs. But the stem asks the
       student to "Write an equation about the absolute values of a and b that
       must be true", and "sign reversed" is neither an equation nor a statement
       about absolute values - it is a bare descriptive fragment. The governing
       instruction is "Select every choice that belongs in complete correct
       answer", and the complete correct answer per the key is "|a| = |b| (or
       equivalent)". Decisively, unlike Q1 this item has no Part B for which a
       verbal characterisation would be an expected answer, so a correct
       reasoner has no route to selecting it. Compare P1Q1/P2Q1, where the
       parallel verbal choice "equal magnitude and opposite signs" IS keyed,
       precisely because Part B asks for it. Ruled harmless.

  P2Q1 wrong_1  "24 and +24"
    -> NOT A DEFECT. For this to be true, the bare "24" would have to denote the
       descent as a signed number, i.e. -24. In mathematical notation a bare 24
       denotes +24, so the choice asserts the pair (+24, +24), whose sum is +48,
       not 0, and which represents two climbs rather than a descent followed by
       a climb. There is no reading under which "24" means "-24". FALSE.
       Recorded as the weaker case because it is the only distractor in the
       slice that is false by an OMITTED sign rather than by an explicitly wrong
       one, which makes it the softest distractor here - a student who wrote the
       descent as "24 m down" in prose could glance at it. The stem's own words
       "with signed numbers" and the key's "(-24)" both close that reading, so
       it stands. Noted, not scored.

  P1Q4 wrong_6 "0, -1, 8" and P2Q4 wrong_4 "0, 4, 6"
    -> NOT DEFECTS. Neither is the stem's number set; 0 appears in neither set.
       The first is not even sorted (0 > -1). False on both counts.

DISAGREEMENTS WITH THE EARLIER JUDGES

  None. I reached the same rulings independently on all four repairs, on both
  weak cases, and on all seven criteria, working from the stems and the rendered
  sources before opening either report. The three replaced distractor texts are
  each false over the whole admissible set of their stems, not merely
  true-but-unkeyed choices swapped for other true ones, and the fourth repair
  did not import the answer into the stem it fixed.

OPERATIONAL NOTES (not package defects, no action taken - I edited nothing)

  1. FIXES_APPLIED.txt records only the T1-6 and T1-8 changes. It contains no
     entry for the four T1-1 changes, even though the hash evidence above proves
     they were applied. The bookkeeping file is incomplete for this slice; the
     package itself is correct. Anyone auditing by that file alone would
     conclude T1-1 was never touched.

  2. slices/T1-1.json remains stale relative to the package and truncates the
     two Q2 stems at their "<" characters. Read the package XML.

CLEAN

  Part 1 Question 1
  Part 1 Question 2
  Part 1 Question 3
  Part 1 Question 4
  Part 2 Question 1
  Part 2 Question 2
  Part 2 Question 3
  Part 2 Question 4

  All 8 items worked. No defect stands. SCORE: 10/10
