SLICE: G2a          SCORE: 10/10
ITEMS WORKED: 17 of 17     (I1 I2 I3 J1 J2 J3 J4 J5 K1 K2 K3 K4 K5 K6 K7 K8 K9 — none skipped)

Cold second read. Nothing in this range was repaired; there is no `G2a-r2.md`, and
the package carries no checksum and no prior validation record. I formed every
ruling below from the raw XML and the rendered worksheet before opening
`G2a-r1.md`, which I read last and only to check its claims against mine.

Shape B confirmed independently: `respident="response"` on every item; idents are
`answer1` (fill-in) and `choice_1..choice_7` (select-all); no `correct_*` /
`wrong_*` naming anywhere; all 17 items carry fewer than 8 choices, which per the
rubric is this corpus's design and is NOT scored; exactly one `<respcondition>`
per item in this range, so no second-respcondition question arises here.

METHOD

Parsed with ElementTree, not regex. The scoring tree was walked node by node with
`<not>` subtrees routed into a separate negated list before anything was collected
as required, so no `<varequal>` inside a `<not>` was ever mistaken for a key. Text
was extracted by stripping real tags first (`</?[a-zA-Z][^>]*>` only) and
unescaping second, so a bare `<` before a space or digit stays text. The slice
cache in `/tmp/qtiwork/slices/G2a.json` was not used as a source.

Worksheet stems settled by rendering `6thGradeReviewUpdated.pdf` at 160 dpi, not
by extraction order. This mattered: `pdftotext -layout` flattens J2 to "35 of 35",
K4 to "Simplify 2736", K5 to "Convert 2 23", K6 to "1 34 or (1) 34", K7 to "In
m2", K8 to "In 5". The rendered page shows 3/5 of 35, 27/36, 2 2/3, 1 3/4 or
(1)(3/4), m/2, q/5. Every QTI stem in range agrees with the rendered form.

I also diffed the original `6thGradeReview.pdf` against the updated revision. For
sections I, J and K the mathematics is byte-identical in content; only layout and
phrasing were compacted. The revision's numeric changes (C7 `15% of $80`, M2
`700.32 - 84.67` replacing `700.3 - 284.67`) fall outside this slice, so the
"stale companion" warning does not bite in G2a. The companion's I/J/K pages agree
with the updated worksheet on every value in range.

DEFECTS

  None.

THE K9 / K2 QUESTION — SETTLED INDEPENDENTLY, NOT ADOPTED

The brief asked me to test the earlier ruling rather than inherit it. I reach the
same verdict but by a different and, I think, stronger route.

The earlier judge's formulation was that the modifier constrains the *derivation*,
not the value. That is right for K9 but imprecise for K2, where the constraint is
on the *form* (every factor must be prime), not on how you got there. So I did not
adopt the formulation. I used the rubric's own stated reason for criterion 2
instead: the criterion exists because a true-but-unkeyed choice "punishes precisely
the strongest students" — a student who reasons correctly selects it and scores
zero. That gives a decisive, checkable test: **does the mathematically correct
reasoner select the choice?** If yes, it is a defect. If selecting it requires
ignoring a word in the stem or holding a misconception, it is not.

K2 — "Prime factorization of 90 = Enter select all equivalent prime factorizations."
Key = {choice_1 "2 × 3^2 × 5"} = 2 · 9 · 5 = 90, and 2, 3, 5 are all prime. Correct.

  Non-keyed, each worked:
    choice_2 "2 × 3 × 5"     = 30 ≠ 90.  Plainly false.
    choice_5 "2^2 × 3 × 5"   = 4·3·5 = 60 ≠ 90.  Plainly false.
    choice_6 "90 is prime"   — false; 90 = 2 · 45, so it has more than two factors.
    choice_3 "9 × 10"        = 90, but 9 = 3^2 and 10 = 2 · 5 are both composite.
    choice_4 "3^2 × 10"      = 9 · 10 = 90, but 10 is composite.
    choice_7 "2 × 45"        = 90, but 45 = 3^2 · 5 is composite.

  choice_3, choice_4 and choice_7 are the rubric's explicitly weaker class — a true
  arithmetic statement that answers a different question — and I record them as
  such rather than merging them with the graver class. Each is a true factorisation
  of 90; none is a prime factorisation of 90.

  I considered the strongest argument against this: the rubric's defect list names
  "an alternative valid factorisation", and the stem literally contains the trigger
  phrase "select all equivalent …". Two things defeat it.

  First, uniqueness. By the fundamental theorem of arithmetic the prime
  factorisation of 90 is unique up to order: 2 · 3^2 · 5. There is no *alternative
  valid prime* factorisation, so the "alternative valid factorisation" bullet has
  nothing to attach to here. A reordering or an unexponentiated form (3 × 2 × 3 × 5,
  say) would qualify, and none is offered.

  Second, the decisive test. A student who knows what "prime" means cannot select
  9 × 10. Selecting it requires not knowing that 9 and 10 are composite, which is
  the exact misconception the item is built to catch. Keying it would not protect
  the strong student; it would destroy the item, since the word "prime" would then
  carry no force and the question would collapse into "select all products equal
  to 90". Ruled NOT a defect.

K9 — "Rewrite using the commutative property: 8 + 5 = Enter select all equivalent
commutative rewrites." Key = {choice_1 "5 + 8"}.

  Non-keyed, each worked:
    choice_4 "8 × 5"       = 40 ≠ 13.  Plainly false, and the wrong operation.
    choice_5 "5 - 8"       = -3 ≠ 13.  Plainly false.
    choice_2 "8 + 5"       = 13. The given expression verbatim. Nothing has been
      commuted; a + b -> b + a applied once yields 5 + 8, and applying it twice
      returns the input, which is not a rewrite. Closest call in the slice — see
      below. Ruled NOT a defect.
    choice_3 "13"          = 13. An evaluation, not a rewrite. Weaker class.
    choice_6 "(8 + 5) + 0" = 13. Obtained by the additive identity, not by
      commutativity. Weaker class.
    choice_7 "8 + (5 + 0)" = 13. Additive identity plus regrouping; still not
      commutativity. Weaker class.

  choice_2, choice_3, choice_6 and choice_7 are all value-equal to 8 + 5. I state
  plainly that they *would* be criterion-2 defects if the stem read "select all
  equivalent expressions". It does not. The head noun is "commutative rewrites",
  and "equivalent" modifies it rather than replacing it.

  Decisive test applied: a student who knows the commutative property will not
  select 13 (that is evaluating, not rewriting), will not select (8 + 5) + 0 or
  8 + (5 + 0) (those are the identity property), and will not select 8 + 5
  unchanged. The only students who select them are students confusing evaluation or
  the identity property with commutativity — the precise misconceptions the
  distractor set is built from. The strong student is rewarded here, not punished,
  which is the opposite of the harm criterion 2 exists to prevent.

  Reductio, and it is the same one as for K2: if choice_3 were keyed on value
  equivalence alone, then every expression equal to 13 (20 - 7, 6 + 7, 13 + 0)
  would have equal claim, the answer set would be unbounded, and the word
  "commutative" would be inert. That is not a reading of the stem; it is a refusal
  to read it.

  Cross-check on authorial intent, from the companion (K9): "Switch the order of
  the two addends. Write 5 + 8. … Do not change the operation to multiplication;
  keep addition." Only 5 + 8 qualifies. Calibration against the parallel items in
  the same file (K10 "Commutative: 7 × a", K11 "Associative: (b + 3) + 9", N5, N6)
  shows the author consistently plants value-equal wrong-property forms as
  distractors across all nine select-all items in this package. K9 follows that
  pattern exactly, and none of its plants is itself a commutative rewrite.

  I applied one standard to K2 and K9 and to K1 below. Ruled NOT a defect.

  On choice_2 specifically, the closest call: the rubric lists "a statement given as
  true in the stem itself" as a defect class, and "8 + 5" does appear in the stem.
  It appears there as the operand to be rewritten, not as an assertion offered as
  an answer. The task verb is "rewrite", so reproducing the input unchanged is a
  non-answer rather than a correct one. Ruled NOT a defect, recorded because it is
  the thinnest margin in the slice.

CANDIDATES RULED ON

  "K9 and K2 are correctly keyed; the modifier constrains the derivation, not
  merely the value" (earlier judge's ruling) -> CONFIRMED as to outcome, PARTLY
  REFUTED as to reasoning. The conclusion is right for both items and I reach it
  independently. The stated reason is right for K9 but wrong for K2, where the
  constraint is on the form of the factors, not on the derivation path; I replaced
  it with the uniqueness argument plus the rubric's own strong-student test. No
  change to the score.

  "K2: 9 × 10, 3^2 × 10 and 2 × 45 all equal 90 but are not prime factorisations,
  so non-keying is correct" -> CONFIRMED, and re-derived above from the stem.

  "Audit reported I1-I3, K1, K2 clean" -> CONFIRMED. Reworked from scratch, not
  ratified: I1 9 × 4 = 36; I2 2(11 + 3) = 28; I3 42 ÷ 6 = 7; K1 sole correct
  explanation is choice_1; K2 sole prime factorisation is choice_1.

CLEAN

  I1 — Rectangle length 9, width 4. Area = 9 × 4 = 36. Key 36. Worksheet I.1
       (rendered) "Rectangle with length 9 and width 4: Area =". Companion: 36
       square units; the stem's "the number only, no units" makes bare 36 right.
       Not keyed to 26, the perimeter trap.
  I2 — Rectangle length 11, width 3. Perimeter = 2(11 + 3) = 28. Key 28.
       Companion: 28 units. Not keyed to 33, the area trap. Correct.
  I3 — Rectangle area 42, width 6. Length = 42 ÷ 6 = 7. Key 7. Companion: 7 units.
       Stem drops "sq units" from the worksheet; the answer is a bare number, so
       no information is lost.
  J1 — 3 hours to minutes. 3 × 60 = 180. Key 180. Companion: 180 minutes.
  J2 — 3/5 of 35. (3 × 35)/5 = 105/5 = 21. Key 21. Companion: 21. The rendered
       worksheet confirms numerator 3 and denominator 5; the extraction's "35 of
       35" is the transposition artifact, not the source.
  J3 — 210 miles / 3 hours. 210 ÷ 3 = 70. Key 70. Companion: 70 miles per hour;
       bare 70 is right given the "no units" instruction.
  J4 — 72 inches to yards. 1 yd = 36 in, so 72 ÷ 36 = 2. Key 2. Companion: 2 yards.
       Not 6, the feet answer. Correct.
  J5 — 150 miles / 5 gallons. 150 ÷ 5 = 30. Key 30. Companion: 30 miles per gallon.
  K1 — "Is 8x + 1 a linear expression? Enter select all correct explanations."
       Key choice_1 "Yes; x has exponent 1" — true: 8x + 1 is of the form ax + b
       with x to the first power. Every other choice worked and false:
         choice_2 "No; x exponent is 8" — 8 is the coefficient, not the exponent.
         choice_3 "No; constant makes nonlinear" — the b term is permitted in ax+b.
         choice_4 "No; two terms cannot be linear" — ax + b has two terms.
         choice_5 "Yes; because 8 is prime" — right verdict, false reason, and
           8 = 2^3 is not prime. Weaker class (a true component inside a false
           unit); the stem asks for explanations, and the unit is not one. Ruled
           NOT a defect by the same standard used on K2 and K9.
         choice_6 "Yes; because x is after 8" — right verdict, irrelevant reason.
           Same weaker class, same ruling.
         choice_7 "No; because there is addition" — false.
       No true unkeyed choice.
  K3 — GCF(27, 36). 27 = 3^3; 36 = 2^2 · 3^2; shared prime 3 at the lower power,
       3^2 = 9. Key 9. Confirmed by listing: factors of 27 are 1, 3, 9, 27; of 36
       are 1, 2, 3, 4, 6, 9, 12, 18, 36; largest shared is 9. Companion: 9.
  K4 — Simplify 27/36. Divide both by GCF 9: 27/9 = 3, 36/9 = 4, giving 3/4, in
       lowest terms since gcd(3, 4) = 1. Key "3/4". Companion: 3/4.
  K5 — 2 2/3 to improper. (2 × 3) + 2 = 8 over denominator 3, so 8/3. Key "8/3".
       Companion: 8/3. Already in lowest terms.
  K6 — Greater of 1 3/4 and (1)(3/4). 1 3/4 = 7/4 = 1.75; (1)(3/4) = 3/4 = 0.75;
       7/4 > 3/4, so 1 3/4 is greater. Key "7/4". The companion's checked answer is
       the mixed form 1 3/4 — the same value — and the item's own instruction,
       "Enter a simplified a/b, no spaces or mixed numbers", forces the improper
       form and rules out "1.75" as well, leaving exactly one admissible string.
       So the key reproduces the answer key (criterion 4) and stays producible by a
       student holding only the worksheet (criterion 5). Recorded because it is the
       one place a key and a companion differ in surface form. Not a defect.
  K7 — Coefficient of m in m/2. m/2 = (1/2)m, so 1/2. Key "1/2". Companion: 1/2.
       Not keyed to 2, the reciprocal trap. Correct.
  K8 — Coefficient of q in q/5. q/5 = (1/5)q, so 1/5. Key "1/5". Companion: 1/5.
       Companion's numeric check at q = 10 (10/5 = 2 and (1/5)(10) = 2) agrees.
  K2 — see the section above. Key choice_1 "2 × 3^2 × 5" = 90, all factors prime.
       Companion: 2 · 3^2 · 5. Agrees.
  K9 — see the section above. Key choice_1 "5 + 8". Companion: 5 + 8. Agrees.

STRUCTURE AND MARKUP, ALL 17

  Exactly one `<respcondition continue="No">` per item, each with
  `<setvar action="Set" varname="SCORE">100</setvar>` against a `decvar` of
  maxvalue 100. The required/negated split is coherent: K1, K2 and K9 each require
  `choice_1` and negate `choice_2` through `choice_7`, which is complete
  all-or-nothing coverage of all seven choices with no choice left unconstrained
  and none both required and negated. The fill-in items carry the answer as the
  required value with no negations. The eight `numerical_question` items (I1-I3,
  J1-J5) and K3 use the standard Canvas exact-answer form
  `<or><varequal/><and><vargte/><varlte/></and></or>` with both bounds equal to
  the key, which is a zero-margin exact match and admits equivalent numeric
  spellings such as "2.0". The five `short_answer_question` items (K4-K8) use a
  single `<varequal case="No">`.

  No two choices share visible text in any item in range. No duplicated instruction
  block in any stem. Zero `$` and zero `\(` in the entire file, so no math
  delimiter can be unbalanced or interleaved. No `<img>` anywhere in this package,
  so no `$IMS-CC-FILEBASE$` path question arises in G2a. No HTML entities at all;
  the only non-ASCII characters in the whole file are U+00D7 and U+00F7, and the
  bytes are valid UTF-8 under the declared encoding. The XML parses. The manifest
  declares the one QTI resource plus its `assessment_meta.xml` dependency and both
  referenced files exist on disk. `assessment_meta.xml` declares
  `points_possible` 33, matching 33 items at 1 point each.

OBSERVATIONS — CHECKED, DELIBERATELY NOT SCORED

These are not defects under any of the seven criteria. I record them so a reader
can act on them separately; none of them changes the score.

  1. `original_answer_ids` reads `choice_1` on the fill-in items whose
     `response_label` ident is `answer1`. Canvas rebuilds answer ids on import, it
     does not block import, and it is uniform across all 69 items in both
     6th-grade packages and absent from all 12 Topic packages. House artifact.

  2. The instruction suffix on all three select-all items reads "Enter select all
     …", which is ungrammatical — the type template's leading "Enter" collides
     with the select-all phrasing. This is uniform across all 21 select-all items
     in both 6th-grade packages, not local to G2a. Criterion 7's list is closed
     (delimiters, duplicated instruction blocks, image paths) and does not reach
     grammar, and the meaning is not in doubt. Not scored.

  3. `shuffle_answers` is `false` in `assessment_meta.xml`, and the key is
     `choice_1` — the first listed option — on all three select-all items in range,
     and in fact on all 21 across both 6th-grade packages. A student could score
     every select-all item by always choosing the first option. No criterion covers
     answer-position bias, and the setting appears forced rather than careless:
     section 1's A1, H6 and H7 map their choices to labelled positions in an
     embedded graphic, so shuffling would break them. Worth raising with the author
     as a corpus-level design point; not a defect in this slice and not scored.

  4. The QTI stems in range are lightly condensed paraphrases of the updated
     worksheet (for example I1 "Rectangle length 9, width 4" for "Rectangle with
     length 9 and width 4"). Every number, operation, variable and unit matches
     exactly, and the item labels align one to one, so criterion 1 is met. Some
     stems match the pre-update phrasing more closely than the updated one, but no
     value differs between the revisions anywhere in sections I, J or K.

VERDICT

  10/10. Every one of the 17 items was worked from the stem. No defect stands.
  I confirm the earlier judge's outcome on K9 and K2 while replacing part of its
  reasoning, and I raise no new defect.
