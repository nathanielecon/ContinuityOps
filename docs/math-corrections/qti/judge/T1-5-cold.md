SLICE: T1-5          SCORE: 10/10
ITEMS WORKED: 6 of 6     (none skipped)

Cold read. Formed independently from the raw XML, the rendered assignment page and
both answer key PDFs before either T1-5-r1.md or T1-5-r2.md was opened. I reached
the same verdict as r2, but by a different route, and I disagree with one of r2's
methodological claims. That disagreement is recorded below under INSTRUMENT
FINDING because it affects how other slices are being verified, even though it
does not change this slice's score.

File under judgement:
  /tmp/qtiwork/pkg/topic-1-5-independent-practice-accuracy-check-qti/
    topic_1_5_independent_practice_accuracy_check/
      topic_1_5_independent_practice_accuracy_check.xml
  md5 2f8105d7959a90b724c3a7fe51589cd2, 643 lines.
  All three package files parse with ElementTree; every mattext's inner HTML is
  independently well-formed. No images, no media/ references, so the
  $IMS-CC-FILEBASE$ rule does not apply. The only non-ASCII character in the file
  is U+00B0 DEGREE SIGN, 16 occurrences (the 8 choices of each Q2 item).

Shape A confirmed: 6 multiple_answers_question items, idents _correct_N /
_wrong_N, respident="response1", 8 choices each.

Caches were not used. The rebuilt /tmp/qtiwork/slices/T1-5.json was never read.


DEFECTS

  None. No defect stands on any of the six items on any of the seven criteria.


THE TWO EXPOSURES I WAS ASKED TO TEST

1. Interleaved delimiters whose \( and \) counts balance

  Current state, ordered scan of \( and \) over each stem in document order
  (depth counter; require depth 0 before every \(, never negative, ends at 0):

    P1Q2  \( \) \( \) \( \)   pass   spans: -3.75^\circ | 2.4^\circ | 1.85^\circ
    P2Q2  \( \) \( \) \( \)   pass   spans: -4.6^\circ  | 1.35^\circ | 2.05^\circ
    P1Q3  \( \) \( \)         pass   spans: 2\dfrac{1}{2} | 1.75
    P2Q3  \( \) \( \)         pass   spans: 3\dfrac{1}{4} | 2.5

  Whole file: 10 \( and 10 \), depth never exceeds 1, closes at 0. The only
  letter sequences appearing anywhere inside a math span are \circ (6) and
  \dfrac (2); no prose and no $ is captured inside any span. Every quantity a
  student needs sits alone in its own span. \dfrac is standard MathJax.

  Rendered result is correct: \(-3.75^\circ\)C gives "-3.75 degrees C" with the
  C outside the span and no inserted space, matching the assignment's typography.

2. Bare currency $ deliberately left alone

  22 bare $ remain, and I recovered every one with its token text rather than
  counting them:

    P1Q1 stem   $200.  $15.00  $250.
    P2Q1 stem   $180.  $12.00  $200.
    P1Q1 choices $140 $-140 $141 $139 $142 $138 $0 $1400
    P2Q1 choices $120 $-120 $121 $119 $122 $118 $0 $1200

  None acts as a delimiter, on four independent grounds:
    - No mattext block in this file contains both $ and \(. The two items holding
      currency (P1Q1, P2Q1) contain zero \( tokens; the four items holding \(
      contain zero $. The separation is total.
    - Corpus-wide the same holds: across all 14 packages, 39 mattext blocks
      contain a bare $ and exactly 0 of them also contain \(. This is uniform
      design, not a T1-5 accident.
    - Each choice block holds exactly one $, so no $...$ pair can form in a
      choice at all.
    - Canvas's MathJax enables \(...\) and does not enable single-$ inline math.

  None was wrongly converted. Diffing the current file against the untouched
  original at inbox/Inbox/topic-1-5-independent-practice-accuracy-check-qti.zip
  shows exactly 4 changed lines, all four of them the <presentation><material>
  stem of a math item. The $ tokens the repair removed were exactly these 8:

    $2.4^\circ\(C,    $1.85^\circ\)C.     (P1Q2)
    $1.75$                                (P1Q3, two $)
    $1.35^\circ\(C,   $2.05^\circ\)C.     (P2Q2)
    $2.5$                                 (P2Q3, two $)

  Every one was a degree or a mileage quantity. Not one was money. Zero $ tokens
  were added. All 22 money tokens are byte-identical to the original and match
  the assignment ($200 / $15.00 / $250 / $180 / $12.00 / $200) and the answer
  keys ($140, $120). 30 pre-fix minus 8 removed equals 22 post-fix; that
  arithmetic closes.

  Considered and dismissed: the P1Q1 and P2Q1 stems each hold three $, an odd
  count, so under a hypothetical $-enabled renderer $200 and $15.00 would pair
  and swallow the prose between them. This is not a defect here. The count is
  odd so no complete pairing exists, Canvas does not enable the delimiter, the
  assignment itself writes these as currency, and the identical pattern is
  corpus-wide. Converting them would be the regression, not leaving them.


INSTRUMENT FINDING - the stated verification method is not sufficient

  I was told to verify nesting by an ordered scan rather than by counting, and
  T1-5-r2 reports that its ordered scan "failed on the broken version". I tested
  that claim directly by running scans against the known-broken original.

  A counting check passes on both broken and fixed text, as stated. But an
  ordered scan restricted to \( and \) ALSO passes on the broken text:

    broken P1Q2  ...\(-3.75^\circ\)C. It drops $2.4^\circ\(C, then drops
                 $1.85^\circ\)C...
                 token order \( \) \( \)  -- depth never exceeds 1, ends at 0.
                 ORDERED SCAN PASSES. The text is nonetheless broken: the
                 second span is `C, then drops $1.85^\circ`, prose typeset as
                 mathematics, with $2.4^\circ left outside as literal characters.

    broken P1Q3  ...\(2\dfrac{1}{2}\) miles... $1.75$ miles...
                 token order \( \) $ $ -- passes an ordered scan even when $ is
                 included as a toggle token. Also broken.

  So neither counting nor an ordered scan of \( and \) discriminates here, and
  adding $ as a toggle token catches P1Q2/P2Q2 but still misses P1Q3/P2Q3. Two
  checks do discriminate, and both pass on the current file:

    (a) span-content inspection - extract each \(...\) span and reject any span
        containing prose or a $. On the broken file this returns
        `C, then drops $1.85^\circ` and `C, then drops $2.05^\circ`. On the
        current file it returns nothing.
    (b) co-occurrence - reject any mattext block containing both $ and \(. On
        the broken file this flags all four math stems, including the two an
        ordered scan misses. On the current file it flags none.

  Check (b) is the clean one: it is the only test that flags all four original
  defects with no false positive on the legitimate currency stems. An ordered
  scan with $ treated as a toggle reports "ends at depth 1" on P1Q1 and P2Q1
  both before and after the repair, purely because currency $ counts are odd -
  a false alarm that would send a correct file back around.

  Recommendation for the remaining slices: verify by (a) and (b), not by an
  ordered scan of \( and \) alone. The verdict on T1-5 is unaffected; the file
  passes every one of these tests. But r2's statement that its ordered scan
  failed on the broken version is only true for the variant that tokenises $ as
  well, and even that variant would have passed the broken P1Q3 and P2Q3.


MATHEMATICS, WORKED FROM SCRATCH

  Sources: assignment page 3 rendered as an image at 160 dpi (pdftoppm), not
  extracted, because the mixed numbers are built up and pdftotext -layout
  flattens 2 1/2 to "2 12". Cross-checked against Topic1Part1Solutions.pdf and
  Topic1Part2Solutions.pdf, Lesson 1-5 on page 3 of each.

  P1Q1  Assignment: account starts $200, bank charges $15.00 each month if the
        balance is below $250, no other activity, balance after 4 months.
        200 < 250, so the fee applies in month 1; the balance only falls, so it
        stays below 250 and the fee applies every month.
        200-15=185, 185-15=170, 170-15=155, 155-15=140.
        Keyed: $140. Part 1 key: "Answer: $140". Agrees.
        Non-keyed $-140, $141, $139, $142, $138, $0, $1400 are all false. The
        balance is positive so $-140 is false; no reading of the fee condition
        stops the charge early, so no near-miss is reachable by correct
        reasoning; intermediate balances 185/170/155 are not offered, so there
        is no true-answering-a-different-question distractor. No restated or
        equivalent form of 140 appears.

  P1Q2  Assignment: 6:00 PM, temperature -3.75 C, drops 2.4 C, then drops
        1.85 C.  Two drops are two negative changes.
        3.75 + 2.4 = 6.15; 6.15 + 1.85 = 8.00; so -3.75 - 2.4 - 1.85 = -8.00.
        Keyed: -8 C. Part 1 key: "Answer: -8 C". Agrees.
        Non-keyed 8, -7, -9, -6, -10, 0, -80 all false. The single-drop value
        -6.15 is not offered. No "-8.00 C" trailing-zero variant is offered, so
        the added rounding instruction cannot create a second true form.

  P1Q3  Assignment: lookout 2 1/2 miles above sea level, mountain base 1.75
        miles below.  2 1/2 = 2.5, so positions are +2.5 and -1.75.
        Vertical distance = |2.5 - (-1.75)| = 4.25.
        Keyed: 4.25 miles. Part 1 key: "Answer: 4.25 miles". Agrees.
        Non-keyed -4.25, 5.25, 3.25, 6.25, 2.25, 0.00, 425 all false. -4.25 is
        the signed difference taken the other way, but the stem asks for a
        vertical distance and the key takes an absolute value, so a negative
        distance is false, not an alternative form. 0.75, the value if both
        points were above sea level, is not offered. No mixed-number form
        (4 1/4 miles) is offered, so there is no equivalent-form defect.

  P2Q1  Assignment: account starts $180, $12.00 each month if below $200, after
        5 months.  180 < 200 and the balance only falls: 168, 156, 144, 132,
        120.  Keyed: $120. Part 2 key: "Answer: $120". Agrees.
        Non-keyed $-120, $121, $119, $122, $118, $0, $1200 all false;
        intermediates 168/156/144/132 not offered.

  P2Q2  Assignment: 4:00 PM, -4.6 C, drops 1.35 C, then drops 2.05 C.
        1.35 + 2.05 = 3.40; 4.6 + 3.40 = 8.00; so -4.6 - 1.35 - 2.05 = -8.00.
        Keyed: -8 C. Part 2 key: "Answer: -8 C". Agrees.
        Non-keyed 8, -7, -9, -6, -10, 0, -80 all false; -5.95 not offered.

  P2Q3  Assignment: radio tower 3 1/4 miles above, canyon floor 2.5 miles below.
        3 1/4 = 3.25; |3.25 - (-2.5)| = 5.75.
        Keyed: 5.75 miles. Part 2 key: "Answer: 5.75 miles". Agrees.
        Non-keyed -5.75, 6.75, 4.75, 7.75, 3.75, 0.00, 575 all false. 3.75 here
        is not the P1Q2 temperature restated in disguise; against this stem it
        answers nothing. 0.75 not offered.

  Mixed numbers settled along three independent paths that agree: the rendered
  assignment image shows 2 1/2 and 3 1/4 as built-up fractions; both solution
  PDFs write "2 12 = 2.5" and "3 14 = 3.25" in their We Solve lines, which
  resolves the flattening; and the QTI writes 2\dfrac{1}{2} and 3\dfrac{1}{4}.

  Criterion 4: neither answer key writes any Lesson 1-5 answer with an "or"
  alternative, so the all-or-nothing single-key structure cannot punish an
  acceptable variant form on any of these six.


STRUCTURE (criterion 6), RE-DERIVED

  Parsed the respcondition tree with ElementTree, collecting varequal inside
  <not> separately from bare varequal, so the flat-regex trap does not apply.
  On all six items: exactly one <respcondition>, decvar maxvalue="100"
  minvalue="0", setvar Set SCORE 100, 8 response_labels, the sole correct_1
  required by a bare varequal, all 7 wrong_N negated by <not><varequal>, no
  varequal unaccounted for, respident="response1" throughout, no duplicate
  visible choice text within any item, no duplicate idents, and
  original_answer_ids matching the render order exactly. Every item: OK.

  assessment_meta.xml: points_possible 6.0 for 6 items, shuffle_answers false,
  allowed_attempts 1. Checked against all 12 Topic packages - identical
  settings pattern throughout, so nothing here is a T1-5 anomaly.


NOTHING OUTSIDE THE REPAIR MOVED

  Verified by diff against the original zip rather than against r1's prose
  record. Exactly 4 lines differ, all four the stem mattext of P1Q2, P1Q3, P2Q2,
  P2Q3. All 48 choice texts, all 6 respconditions, all idents, all
  original_answer_ids, imsmanifest.xml and assessment_meta.xml are byte-
  identical to the original. imsmanifest.xml and assessment_meta.xml still carry
  their 2026-01-01 mtime. The staged zip at
  /tmp/qtiwork/staged/topic-1-5-...-qti.zip is byte-identical to the pkg tree.

  Because no choice text and no varequal changed, the repair cannot have
  displaced a defect into the answer set - the class of failure this round
  exists to catch is structurally impossible for this slice's repair, and I
  confirmed that from the diff rather than assuming it.


CANDIDATES RULED ON

  P1Q2 / P2Q2 interleaved delimiters -> CONFIRMED as an original defect, now
  RESOLVED. I reproduced the broken text from the original zip and showed the
  second span was `C, then drops $1.85^\circ` / `C, then drops $2.05^\circ`.

  P1Q3 / P2Q3 $1.75$ and $2.5$ mixed into \(...\) stems -> CONFIRMED as an
  original defect, now RESOLVED. Both are now \(1.75\) and \(2.5\).

  "Audit reported arithmetic clean ($140, -8 C, 4.25 mi / $120, -8 C, 5.75 mi)"
  -> CONFIRMED, re-derived above from the assignment and both keys without
  consulting the audit. All 6 keyed values right; all 42 non-keyed choices false.


ALSO CONSIDERED, NOT DEFECTS

  "Another bank account starts with $200" where the assignment says "An account
  starts with $200". Not a defect. Lesson 1-3 Q3 of the same assignment is
  itself a bank-account problem ("A bank account starts with $500", verified on
  the rendered page 2), and the corresponding T1-3 QTI stem uses the same
  "If there are no other deposits or withdrawals" phrasing. "Another" is a
  deliberate back-reference within one assignment, not copied residue. The
  phrase occurs nowhere else in the corpus, which is consistent with a
  back-reference and not with a template artefact. All numbers match: 200 /
  15.00 / 250 / 4 months and 180 / 12.00 / 200 / 5 months.

  "Round to two decimals only if needed." is added by the QTI and is not in the
  assignment. Not a defect. Both Q2 answers are exactly -8.00, so the
  instruction is inert, and no "-8.00 C" choice exists for a student to be
  steered toward. Criteria 1 and 5 hold.

  "but only if the balance is below $250" with only emphasised, where the
  assignment writes "if the balance is below $250". Not a defect. Semantically
  identical, and the balance never rises above the threshold under any reading,
  so the conditional never fires differently.

  Choice text "$-140" and "$-120" places the minus after the dollar sign rather
  than before. Unconventional typography, but both are non-keyed and false
  either way, and no rubric criterion covers it.


CLEAN

  Part 1 Question 1
  Part 1 Question 2
  Part 1 Question 3
  Part 2 Question 1
  Part 2 Question 2
  Part 2 Question 3

  All six clean on every criterion 1 through 7.


SCORE REASONING

  Every one of the six items was worked from the assignment and both answer keys
  independently of the r1 and r2 reports. All six keyed values are correct and
  match the answer key PDFs. All 42 non-keyed choices are false, with no
  equivalent fraction, unit variant, trailing-zero restatement, bare-versus-
  labelled pair or alternative expression among them. The scoring tree matches
  the ident labels on all six items under a proper tree parse. The four
  delimiter repairs are genuinely closed, verified by span-content inspection
  and by $/\( co-occurrence rather than by a scan that would have passed the
  broken file. The retained currency $ are all money, all untouched, and none
  can act as a delimiter. Nothing outside the four repaired stems moved.

  10/10.
