SLICE: G2a          SCORE: 10/10
ITEMS WORKED: 17 of 17     (I1 I2 I3 J1 J2 J3 J4 J5 K1 K2 K3 K4 K5 K6 K7 K8 K9 — none skipped)

Shape B confirmed: `respident="response"`, idents `answer1` / `choice_1..choice_7`,
no `correct_*` / `wrong_*` naming, all 17 items under 8 choices (not scored as a
defect), one `<respcondition>` per item (37 respconditions across 33 items in the
file, but every item in this slice has exactly 1 — no equivalent-form alternates
land in my range). Package has no checksum and no validation record; every claim
below was worked from the stem, not taken from the cache or the candidate list.

Method note: required/negated re-derived independently with an ElementTree parse
that collects `<varequal>` inside `<not>` into the negated set first, then treats
the remainder as required. Result matched the slice cache on all 17 items.
Worksheet stems settled by rendering page 1 and page 2 of 6thGradeReviewUpdated.pdf
at 160 dpi, not by `pdftotext` order — `-layout` flattens J2 to "35 of 35", K4 to
"Simplify 2736", K6 to "1 34 or (1) 34"; the rendered page shows 3/5 of 35, 27/36,
and 1 3/4 or (1)(3/4).

DEFECTS

  None.

CANDIDATES RULED ON

  "Audit reported I1-I3, K1, K2 clean" -> CONFIRMED. Reworked from scratch:
    I1 9*4 = 36 (key 36); I2 2*(11+3) = 28 (key 28); I3 42/6 = 7 (key 7);
    K1 sole true explanation is choice_1; K2 sole prime factorisation is choice_1.

  K2: "9 x 10, 3^2 x 10, 2 x 45 all equal 90 but are not prime factorisations,
  so non-keying is correct" -> CONFIRMED (candidate ruling upheld; not a defect).
    90 = 2 * 3^2 * 5. choice_3 9*10 = 90 but 9 = 3^2 and 10 = 2*5 are composite;
    choice_4 3^2*10 = 90 but 10 is composite; choice_7 2*45 = 90 but 45 = 3^2*5 is
    composite. The stem's noun is "prime factorizations", so the restrictive
    qualifier excludes all three. These are the weaker "true statement answering a
    different question" case and I say so explicitly: each is a true factorisation,
    none is a prime factorisation. Ruled NOT a defect.
    The two remaining non-keyed numeric choices are plainly false, not weak cases:
    choice_2 2*3*5 = 30 != 90; choice_5 2^2*3*5 = 60 != 90; choice_6 "90 is prime"
    is false (90 = 2*45).

  "Apply the sibling slice's lens to every select-all stem in range" -> APPLIED,
  no defect found. Two select-all-equivalent stems fall in G2a: K2 and K9.
    K2 worked above.
    K9 "Rewrite using the commutative property: 8 + 5 = Enter select all equivalent
    commutative rewrites." key = {choice_1 "5 + 8"}. I checked every one of the six
    non-keyed choices for a second genuine commutative rewrite and there is none:
      choice_2 "8 + 5" — the given expression verbatim; nothing has been rewritten.
      choice_3 "13" — equals 8 + 5, but it is an evaluation, not a rewrite. Weak
        case (true arithmetic, different question). Ruled NOT a defect.
      choice_4 "8 x 5" = 40 != 13. False.
      choice_5 "5 - 8" = -3 != 13. False.
      choice_6 "(8 + 5) + 0" = 13 and choice_7 "8 + (5 + 0)" = 13 — both value-equal,
        but each is an application of the additive identity, not of commutativity.
        Weak cases. Ruled NOT a defect.
    choice_2, choice_3, choice_6, choice_7 are recorded here rather than passed over
    silently: they are value-equivalent to 8 + 5 and would be criterion-2 defects if
    the stem read "select all equivalent expressions". It does not — it reads
    "commutative rewrites", the same restrictive-noun construction that carries K2.
    I apply one standard to both. The companion (K9) confirms the intent: "Switch
    the order of the two addends. Write 5 + 8." Only 5 + 8 qualifies.
    For calibration I read the parallel non-slice items in the same file (K10, K11,
    L1) and their distractors show the author does plant value-equal-but-wrong-
    property forms ("7a + 0", "b + 12", "(b + 9) + 3", "4(2x + 4)"). K9 carries the
    same design; none of K9's plants is itself a commutative rewrite.

CLEAN

  I1 — Rectangle length 9, width 4. Area. 9*4 = 36. Key 36. Worksheet I.1 (rendered)
       reads "Rectangle with length 9 and width 4: Area =". Companion: 36 square
       units. Stem drops "square units" but the stem itself says "the number only".
  I2 — Rectangle length 11, width 3. Perimeter. 2*(11+3) = 2*14 = 28. Key 28.
       Companion: 28 units. Not keyed to 33 (the area trap), correct.
  I3 — Rectangle area 42, width 6. Length. 42/6 = 7. Key 7. Companion: 7 units.
  J1 — 3 hours to minutes. 3*60 = 180. Key 180. Companion: 180 minutes.
  J2 — 3/5 of 35. (3*35)/5 = 105/5 = 21. Key 21. Companion: 21. Rendered worksheet
       confirms the numerator/denominator are 3 and 5, not the extracted "35".
  J3 — 210 miles / 3 hours. 210/3 = 70. Key 70. Companion: 70 miles per hour; the
       stem's "no units" instruction makes bare 70 the right key.
  J4 — 72 inches to yards. 1 yd = 36 in, 72/36 = 2. Key 2. Companion: 2 yards.
       Not 6 (the feet answer), correct.
  J5 — 150 miles / 5 gallons. 150/5 = 30. Key 30. Companion: 30 miles per gallon.
  K1 — Is 8x + 1 linear? Key choice_1 "Yes; x has exponent 1" — true; 8x + 1 has
       form ax + b with x to the first power. Every other choice worked and false:
       choice_2 "No; x exponent is 8" (8 is the coefficient, not the exponent);
       choice_3 "No; constant makes nonlinear" (the b term is permitted in ax + b);
       choice_4 "No; two terms cannot be linear" (ax + b has two terms);
       choice_5 "Yes; because 8 is prime" — right verdict, but 8 = 2^3 is not prime,
       so as an explanation it is false, and the stem asks for explanations;
       choice_6 "Yes; because x is after 8" — right verdict, irrelevant reason,
       not a correct explanation;
       choice_7 "No; because there is addition" (false). No true unkeyed choice.
  K2 — see CANDIDATES. Key choice_1 "2 x 3^2 x 5" = 2*9*5 = 90, all factors prime.
       Companion: 2 * 3^2 * 5. Agrees.
  K3 — GCF(27, 36). 27 = 3^3, 36 = 2^2 * 3^2, shared 3^2 = 9. Key 9. Companion: 9.
  K4 — Simplify 27/36. GCF 9, 27/9 = 3, 36/9 = 4, so 3/4. Key 3/4. Companion: 3/4.
  K5 — 2 2/3 to improper. (2*3)+2 = 8 over 3, so 8/3. Key 8/3. Companion: 8/3.
  K6 — Greater of 1 3/4 and (1)(3/4). 1 3/4 = 7/4 = 1.75; (1)(3/4) = 3/4 = 0.75;
       7/4 > 3/4. Key 7/4. Companion's checked answer is the mixed form 1 3/4 —
       same value, and the stem's own instruction "no spaces or mixed numbers"
       forces the improper form, so the key reproduces the answer key and remains
       producible by a student holding only the worksheet. Not a criterion 4 or 5
       defect.
  K7 — Coefficient of m in m/2. m/2 = (1/2)m, so 1/2. Key 1/2. Companion: 1/2.
       Not keyed to 2, correct.
  K8 — Coefficient of q in q/5. q/5 = (1/5)q, so 1/5. Key 1/5. Companion: 1/5.
  K9 — see CANDIDATES. Key choice_1 "5 + 8". Companion: 5 + 8.

  Structure and markup, all 17: exactly one `<respcondition>` each with
  `<setvar>100</setvar>`; required/negated split coherent (K1/K2/K9 require
  choice_1 and negate choice_2..choice_7, enforcing all-or-nothing; the fill-in
  items carry the answer string as the required value with no negations); no two
  choices share visible text in any item; zero `$` and zero `\(` in the whole
  file, so no delimiter can be unbalanced or interleaved; no `<img>` anywhere in
  the package, so no `$IMS-CC-FILEBASE$` path question arises; the manifest
  declares the one QTI resource plus its assessment_meta dependency and both
  referenced files exist; the XML parses.

  Checked and deliberately NOT raised: the `original_answer_ids` metadata field
  reads `choice_1` on the fill-in items whose response_label ident is `answer1`.
  This is informational round-trip metadata, Canvas rebuilds answer ids on import,
  it does not block import, and it is uniform across every numerical and
  short_answer item in the corpus. Not a defect.
