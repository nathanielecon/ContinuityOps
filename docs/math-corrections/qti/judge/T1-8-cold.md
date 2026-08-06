SLICE: T1-8          SCORE: 10/10          (cold, independent second read)
ITEMS WORKED: 8 of 8     (none skipped; all worked from the raw XML at
                          /tmp/qtiwork/pkg/topic-1-8-independent-practice-accuracy-check-qti/,
                          not from any cache)

Shape A confirmed before scoring: 8 `multiple_answers_question` items,
`correct_*`/`wrong_*` idents, exactly one `<respcondition>` per item,
`maxvalue="100"`, 8 choices per item.

METHOD

  I formed my view from the sources before opening T1-8-r1.md or T1-8-r2.md.

  Sources, read rendered at 200 dpi (not by `pdftotext -layout`) wherever a
  value depends on layout:
  - Assignment, Lesson 1-8, page 3 rendered. The two Q4 proportions are
    built-up fractions and extract transposed; settled by render:
    P1 Q4 is `-18/6 = n/-4`, P2 Q4 is `-24/8 = n/-3`.
  - Part 1 key, page 4 and 5 rendered.
  - Part 2 key, page 4 and 5 rendered.

  Scoring parsed as a tree, not by regex: for each `<respcondition>` I
  collected `<varequal>` nodes reachable under `<not>` into a negated set
  first, then treated only the remaining `<varequal>` nodes as required. A
  flat regex would have reported all 8 choices as required in every item.

  Extraction order per the brief: strip real HTML tags first with
  `</?[a-zA-Z][^>]*>`, unescape second. This slice contains no bare `<`
  before a space or digit, so the truncation trap does not arise here; I
  confirmed that separately by comparing the pre-repair broken-extractor
  stems against the live stems (all 8 identical, so T1-8 was not among the
  89 truncated stems).

DEFECTS

  None. No defect stands in this slice.

THE SWAP — VERIFIED CORRECT WAY ROUND (Part 1 Question 1)

  Sign convention derived from the stem and the key, not assumed:

    Stem: "A submarine starts at sea level, 0 feet. It descends to \(-168\)
    feet in 7 minutes at a steady rate." Part A asks for the unit rate of
    descent as an integer; Part B asks the position relative to sea level
    after 4 minutes.

    Part 1 key, Lesson 1-8 Question 1, verbatim from the rendered page:
      "Part A: Unit rate = (-168) / 7 = -24 feet per minute.
       Part B: (-24) x 4 = -96 feet (96 feet below sea level).
       Answer: Part A: -24; Part B: -96 feet (below sea level)"

    So descent is negative. The same convention is stated outright in the
    Part 1 key one lesson earlier: Lesson 1-6 Q1, "Part A: Descent is
    negative: -15 feet per minute."

    Rate = (-168) / 7 = -24 ft/min.  Position after 4 min = (-24)(4) = -96 ft.

    Phrase convention, which is what the defect turned on: "d feet below sea
    level" denotes elevation -d; "d feet above sea level" denotes elevation
    +d. A sign written in front of the magnitude is therefore a second
    negation, and "-96 feet below sea level" asserts -(-96) = +96, i.e. 96
    feet ABOVE. The rubric fixes this reading explicitly at criterion 3.

  Which choice is keyed NOW (read off the parsed scoring tree, not the
  ident labels alone — though the two agree):

    REQUIRED  1_8_part_1_question_1_correct_1 = "Part A: -24"
              -> (-168)/7 = -24. TRUE. Matches the key's "Part A: -24".
    REQUIRED  1_8_part_1_question_1_correct_2 = "Part B: 96 feet below sea level"
              -> elevation -(96) = -96 ft, the submarine's actual position.
              TRUE. Correctly keyed.
              This string is a verbatim lift of the key's own directional
              phrase, "(96 feet below sea level)" — unsigned magnitude
              carrying the direction word.
    NEGATED   1_8_part_1_question_1_wrong_4 = "Part B: -96 feet below sea level"
              -> elevation -(-96) = +96 ft, while the submarine is at -96 ft.
              FALSE. Correctly negated.

  VERDICT: the swap landed the right way round. The keyed Part B is the
  true statement and the double-signed form sits on the distractor. A
  backwards swap would have left correct_2 reading "-96 feet ... " and
  wrong_4 reading "-96 feet above sea level"; neither is the case.

  Third independent confirmation of the phrase convention, beyond the rubric
  and the key: the sibling package T1-6 had the identical defect and its
  fixer repaired it the other way, rewriting its keyed choice from
  "Part B: -180 feet below sea level" to "Part B: -180 feet (below sea
  level)" — i.e. the project itself treats the unparenthesised compound as
  false and adds parentheses to make the gloss reading explicit. Under that
  same convention T1-8's unparenthesised wrong_4 is false. Three paths agree.

  WARNING ABOUT THE FIX LOG — the applied text is right, its stated reason
  is wrong. /tmp/qtiwork/FIXES_APPLIED.txt records the two P1Q1 edits
  correctly, then annotates them:

      "Note: These two choices TRADED PLACES as required. After swap:
         - correct_2 is now false (96 feet above = not below)
         - wrong_4 is now false (-96 feet below = same as correct_1 result)"

  Both bullets are wrong and the first is self-contradictory: it asserts the
  keyed choice is false, and it describes correct_2 as "96 feet above" when
  the text actually written is "96 feet below sea level". correct_1 is
  "Part A: -24", so the second bullet's comparison is meaningless too. I
  verified the applied text against the raw XML rather than the log; the XML
  is correct. Anyone auditing this slice from the fix log alone would either
  reject a good package or, worse, learn the wrong convention and mis-repair
  the next one. Recommend the note be corrected or struck.

  No other choice in P1Q1 is true:
    wrong_1 "Part A: +24"   — descent must be negative (key: "-24"; Lesson
                              1-6 key: "Descent is negative"). FALSE.
    wrong_2 "Part A: -23"   — (-168)/7 = -24, not -23. FALSE.
    wrong_3 "Part B: 96 feet above sea level" — elevation +96, actual -96. FALSE.
    wrong_5 "Part B: -24 feet below sea level" — elevation +24; and -24 is the
                              rate, not the 4-minute position. FALSE on either
                              reading of the phrase.
    wrong_6 "Part B: -168 feet below sea level" — elevation +168; and -168 is
                              the 7-minute endpoint, not the 4-minute
                              position. FALSE on either reading.
  Three distinct strings "96 feet below", "96 feet above", "-96 feet below";
  no duplicate visible text in the item.

"n = 72" IN BOTH Q4 ITEMS — GENUINELY FALSE, AND COLLIDES WITH NOTHING

  Part 1 Question 4. Stem `\(\dfrac{-18}{6} = \dfrac{n}{-4}\)`, matching the
  rendered assignment `-18/6 = n/-4`.
    Solve: -18/6 = -3, so n/(-4) = -3 and n = (-3)(-4) = 12. The equation is
    linear in n, so the solution is unique; keyed "n = 12" is right and
    matches the Part 1 key's "Answer: n = 12".
    Test the replacement directly rather than by elimination:
    substitute n = 72 into the right-hand side: 72/(-4) = -18. The left-hand
    side is -3. -18 != -3, so n = 72 does not satisfy the equation. FALSE.
    Collision check — the eight visible texts are
      {n = 12, n = -12, n = 6, n = -6, n = 72, n = 13, n = 11, n = 14}:
    eight distinct strings, eight distinct values, all in "n = " form. 72
    equals no other choice's value, equals no value shown in the stem
    (-18, 6, -4), and is not the keyed answer. No collision.

  Part 2 Question 4. Stem `\(\dfrac{-24}{8} = \dfrac{n}{-3}\)`, matching the
  rendered assignment `-24/8 = n/-3`.
    Solve: -24/8 = -3, so n/(-3) = -3 and n = (-3)(-3) = 9. Keyed "n = 9"
    matches the Part 2 key's "Answer: n = 9".
    Substitute n = 72: 72/(-3) = -24, and -24 != -3. FALSE.
    Collision check — {n = 9, n = -9, n = 3, n = -3, n = 72, n = 10, n = 8,
    n = 11}: eight distinct strings and values; 72 appears in no other choice
    and in no stem value (-24, 8, -3). No collision.

  Why 72 is the right distractor, and why that does not make it true. Both
  answer keys work these by the butterfly method and both produce 72 as the
  cross product: Part 1, "(-18)(-4) = 6n, so 72 = 6n and n = 12"; Part 2,
  "(-24)(-3) = 8n, so 72 = 8n and n = 9". So "n = 72" is exactly the value a
  student lands on if they cross-multiply and stop before dividing — a live,
  attractive wrong answer. It is not a true statement answering a different
  question either: the choice asserts "n = 72", and n is 12 and 9
  respectively, so the assertion is simply false in both items.

  Each replacement also closed, rather than displaced, the original defect.
  Per FIXES_APPLIED.txt the old texts were the bare "12" and bare "9" — the
  rubric's enumerated criterion-2 case, a bare value where the key writes
  "n = value", duplicating the keyed answer. Both are gone and neither
  replacement reintroduces a true choice.

  Incidental, not a defect: the value 72 also appears in Part 1 Question 3's
  stem, "(-72) / (-9)". Different item, different choice list; choices are
  scored per item, so there is no interaction. Noted only so it is not
  rediscovered as a collision.

NOTHING OUTSIDE THE REPAIR MOVED — VERIFIED TWO WAYS

  1. The pre-repair snapshot (corpus_BROKEN.json, package sha 7e1a3b340ff7)
     compared choice-by-choice against the live XML (sha 57e9e375f962) shows
     exactly four differing choice texts and no others:
       P1Q1 correct_2 "-96 feet below sea level" -> "96 feet below sea level"
       P1Q1 wrong_4   "-96 feet above sea level" -> "-96 feet below sea level"
       P1Q4 wrong_4   "12" -> "n = 72"
       P2Q4 wrong_4   "9"  -> "n = 72"
     All 8 stems are byte-identical pre- and post-repair. Every `required`
     and `negated` set is unchanged. No fifth edit hides anywhere.
  2. The item XML is 41898 bytes, and the four edits predict exactly the
     +8-byte delta from the pre-repair 41890 (-1, 0, +4, +5). imsmanifest.xml
     (2192 B) and assessment_meta.xml (3520 B) are byte-identical to the
     staged copies.

  The staged zip /tmp/qtiwork/staged/topic-1-8-...zip diffs clean against
  /tmp/qtiwork/pkg/ on all three files, so the staged artefact is the
  repaired one and is consistent with what I scored.

CANDIDATES AND ROUND-1/ROUND-2 CLAIMS RULED ON

  Read only after forming my own view. My reading was reached independently
  and agrees with r2 on every substantive point; I did not find r1 or r2
  wrong on any mathematical claim.

  P1Q1 correct_2 keyed "-96 feet below sea level" was false (r1) -> CONFIRMED
    Double-signed; asserted +96 while the submarine is at -96.
  P1Q1 wrong_4 "-96 feet above sea level" was true-but-unkeyed (r1) -> CONFIRMED
    Asserted elevation -96, the true position, while negated. Together these
    two made the item unpassable for a student applying the sign convention.
  Both -> RESOLVED by the repair, and resolved in the correct direction.
  P1Q4 wrong_4 bare "12" (r1) -> CONFIRMED, RESOLVED.
  P2Q4 wrong_4 bare "9" (r1) -> CONFIRMED, RESOLVED.
  P1Q1 correct_1 "Part A: -24" alleged double-signed -> REFUTED, as in r1.
    Not double-signed; it is the key's own "Part A: -24". (-168)/7 = -24.
  P1Q1 stem "descends to \(-168\) feet" vs assignment "descends to 168 ft"
    -> REFUTED (criterion 1). "Descends to" and the negative endpoint agree
    rather than contradict; the magnitude (168), the time (7 minutes) and the
    answer are unchanged, and the Part 1 key itself writes "(-168) / 7 = -24",
    so the signed form is the key's own. A student working only from the
    assignment produces the same keyed set.
  r2's process note that /tmp/qtiwork/slices/T1-8.json was stale
    -> NOW RESOLVED. I re-checked: the slice cache has since been rebuilt and
    its 8 records match the live XML choice-for-choice. It no longer carries
    the four old texts. I scored from the raw XML regardless.

NON-DEFECTS EXAMINED AND RULED ON EXPLICITLY

  P2Q1 correct_1 "Part A: +28" against the Part 2 key's "Part A: 28 (or +28)".
    Criterion 4's two-forms trap does NOT fire. The trap requires that both
    "or" forms appear as choices and that all-or-nothing scoring demands both,
    penalising a student who supplies one. Here the item offers no bare
    "Part A: 28" choice at all, so the "or" is never split across a
    keyed/negated pair and no acceptable form is scored wrong. Ruled not a
    defect — recorded explicitly because this is the criterion most easily
    passed over.

  P2Q1 wrong_5 "Part B: 28 feet above sea level" and wrong_6 "Part B: 140
    feet above sea level". The weaker "true arithmetic, different question"
    class, recorded as such per the rubric rather than merged with the true
    ones. 28 is the rate and the 1-minute position; 140 is the 5-minute
    position stated in the stem. Both choices are prefixed "Part B:", and
    Part B asks specifically for the position after 3 minutes, where the value
    is 84. Bound to the question actually posed, both are false. Ruled not
    defects. The same reasoning disposes of P1Q1 wrong_5 (-24, the rate) and
    wrong_6 (-168, the 7-minute endpoint), which are additionally false on
    their sign.

  P2Q1 wrong_4 "Part B: -84 feet above sea level" asserts elevation -84 while
    the drone is at +84. FALSE. This is the double-signed construction working
    as designed, and it is the exact mirror of P1Q1 wrong_4 post-repair.

  P1Q1 wrong_1 "Part A: +24". Both keys state the convention (descent
    negative; the Part 2 key writes the ascent rate positive as "28 (or
    +28)"). FALSE. Not a true-but-unkeyed alternative form.

KEY AGREEMENT (criterion 4), all 8 items against the rendered keys

  P1Q1 {Part A: -24, Part B: 96 feet below sea level}
       vs "Answer: Part A: -24; Part B: -96 feet (below sea level)"     agree
  P1Q2 {-12} vs "(-96) / 8 = -12. Answer: -12"                          agree
  P1Q3 {8}   vs "(-72) / (-9) = 8. Answer: 8"                           agree
  P1Q4 {n = 12} vs "Answer: n = 12"                                     agree
  P2Q1 {Part A: +28, Part B: 84 feet above sea level}
       vs "Answer: Part A: 28 (or +28); Part B: 84 feet above sea level" agree
  P2Q2 {-9} vs "(-81) / 9 = -9. Answer: -9"                             agree
  P2Q3 {8}  vs "(-56) / (-7) = 8. Answer: 8"                            agree
  P2Q4 {n = 9} vs "Answer: n = 9"                                       agree

STRUCTURE AND MARKUP (criteria 6 and 7), all 8 items

  8 items; exactly one `<respcondition>` each; `maxvalue="100"` on all 8;
  every `correct_*` required by a bare `<varequal>` and every `wrong_*`
  inside `<not>`, checked as set equality per item from the parsed tree;
  `respident="response1"` on all 64 `<varequal>` nodes; 8 choices per item;
  `original_answer_ids` matches the rendered choice order in every item; no
  ident appears in scoring that is absent from the choices and no choice is
  left unscored; no duplicate visible text in any item; zero "$" characters;
  9 `\(` and 9 `\)`, balanced and consistent, no interleaving; the Canvas
  instruction block appears exactly once per stem (8 occurrences, 8 items);
  no `<img>` and no `src=` anywhere, no media directory, so there is nothing
  to resolve against `$IMS-CC-FILEBASE$`; all three XML files parse; the
  manifest declares the assessment plus its assessment_meta dependency and
  both referenced files exist; assessment_meta `points_possible` 8.0 matches
  8 one-point items, and `shuffle_answers` is false so the Part A / Part B
  choice grouping is stable on import.

CLEAN

  Part 1 Question 1, Part 1 Question 2, Part 1 Question 3, Part 1 Question 4,
  Part 2 Question 1, Part 2 Question 2, Part 2 Question 3, Part 2 Question 4.
  All eight worked in full — stem against the rendered assignment, keyed set
  against the rendered answer key, every non-keyed choice worked from the
  stem — with no defect standing.

OUT-OF-SCOPE OBSERVATIONS FOR THE COORDINATOR (not scored here, no defect
claimed against T1-8)

  1. The same defect family was repaired inconsistently across packages.
     T1-8 P1Q1 was fixed by dropping the sign ("96 feet below sea level");
     T1-6 P1Q1 was fixed by adding parentheses ("-180 feet (below sea
     level)"). Both are true under the convention, so neither is a defect,
     but T1-6 is now internally mixed as well — its P1Q1 keyed Part B is
     signed-with-parentheses while its P2Q1 keyed Part B is the unsigned
     "180 feet above sea level". Worth normalising to one house form across
     the corpus so that students who import several packages are not taught
     two different reading rules for a signed value next to a direction word.
     Flagged for T1-6's judge; I did not score it.
  2. FIXES_APPLIED.txt's rationale note on the T1-8 P1Q1 swap is wrong in
     both bullets, as detailed above, even though the edit it describes is
     correct. It should not be used as an audit trail in its current state.
