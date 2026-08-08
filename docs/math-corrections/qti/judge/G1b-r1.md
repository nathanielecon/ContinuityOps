# G1b — round 1 judge report

SLICE: G1b (6th Grade Review Section 1, items E1-H7)          SCORE: 6/10
ITEMS WORKED: 18 of 18   (E1 E2 E3 E4 F1 F2 F3 F4 F5 F6 G1 H1 H2 H3 H4 H5 H6 H7)

Shape B confirmed: `respident="response"`, idents `choice_1..choice_7` / `answer1`,
7 choices on every multiple-answers item, exactly one `<respcondition>` on all 18
items (no second-respcondition question arises in this slice). Fewer than 8
choices scored as design, not defect, per rubric.

Cache correction: I worked all 18 items from the raw XML at
`/tmp/qtiwork/pkg/6th-grade-review-section-1-accuracy-check-qti/.../sixth_grade_review_section_1_accuracy_check.xml`
before the coordinator's cache-truncation notice, so no verdict here ever rested
on the broken cache. Only H6 was affected in this slice: the old cache carried
`"Graph 6"`, truncated because the tag-stripper ate from the unescaped `<` in
`6 &lt; y` through the `/>` of the trailing `<img>` tag. H3, H4 and H5 survived
intact because their mattext contains no later `>` for the stripper to close on.
I re-read the rebuilt `slices/G1b.json` after the correction and diffed it against
my XML reading: all 18 stems, required/negated lists, respcondition counts and
image lists now agree exactly with the XML. H6's corrected stem is "Graph 6 < y on
a number line. Use the graphic choices. Enter select all correct graph choices.",
which is what I judged it on.

Source of record: `6thGradeReviewUpdated.pdf` page 1, read rendered at 130 dpi
(the built-up fractions in E2 / E4 / H2 transpose under `pdftotext -layout`;
rendered, they read 4/7 = ?/21, 5/6 = x/18, x/4 = 6, matching the QTI stems).

## DEFECTS

  H6 | criterion 7 | `<img src="media/h6-number-line-options.svg">` in the stem
    found:  `&lt;img src="media/h6-number-line-options.svg" alt="Accessible number-line option graphic for H6: correct choice described in text and image." /&gt;`
    why:    No `$IMS-CC-FILEBASE$/` token. Verified corpus-wide: the token occurs
            zero times in all 14 packages, and the only three `src=` attributes in
            the entire corpus are the three SVGs in this package, all plain
            relative. The manifest lists the SVGs as `<file>` entries inside the
            `imsqti_xmlv1p2` resource, and declares no
            `associatedcontent/.../webcontent` resource (grep for `webcontent`
            returns 0). Canvas rewrites `$IMS-CC-FILEBASE$/...` on import; a bare
            relative path is left alone and resolves against the quiz page URL, so
            the graphic 404s. The stem instructs "Use the graphic choices", so the
            item as authored is broken.
    fix:    `src="$IMS-CC-FILEBASE$/media/h6-number-line-options.svg"`, and move
            the three media `<file>` entries into a separate
            `type="associatedcontent/imscc_xmlv1p1/learning-application-resource"`
            (webcontent) resource that the QTI resource depends on.

  H7 | criterion 7 | `<img src="media/h7-number-line-options.svg">` in the stem
    found:  `&lt;img src="media/h7-number-line-options.svg" alt="Accessible number-line option graphic for H7: correct choice described in text and image." /&gt;`
    why:    Identical to H6 above; same manifest, same missing token.
    fix:    `src="$IMS-CC-FILEBASE$/media/h7-number-line-options.svg"` plus the
            same manifest change.

  H6 | criterion 7 (referenced image content) | `media/h6-number-line-options.svg`
    found:  `<text x="20" y="30">H6 number-line choices. Correct: choice A, open circle at 6 with ray right.</text>`
            plus the same sentence in `<title>` and in `aria-label` on `<svg role="img">`
    why:    Rendered independently with headless Chromium at 960x560 and read as a
            bitmap: the sentence is the first visible line of the figure, black
            16px Arial, drawn above choice A. It is a rendered `<text>` element,
            not a comment. The `<title>` shows as a hover tooltip and the
            `aria-label` is announced first by a screen reader, so all three
            surfaces leak the key. The keyed choice is `choice_1` = "Open circle at
            6; ray right", i.e. exactly what the figure names. On an artifact whose
            only purpose is letting a student check their own homework, being told
            the answer before choosing voids the check. Aggravating: the correct
            option is "choice A" in all three figures of this package (A1, H6, H7),
            so the leak also fixes the position.
    fix:    Delete the `<text x="20" y="30">...</text>` element; change `<title>`
            and `aria-label` to a neutral description, e.g. "H6 number-line answer
            choices A through G." (no "Correct:" clause), and shift the option rows
            up by the freed 47px or leave the whitespace.

  H7 | criterion 7 (referenced image content) | `media/h7-number-line-options.svg`
    found:  `<text x="20" y="30">H7 number-line choices. Correct: choice A, open circle at 2 with ray right.</text>`
            plus the same sentence in `<title>` and in `aria-label`
    why:    Same as H6, confirmed on my own render. Keyed choice is `choice_1` =
            "Open circle at 2; ray right", named verbatim by the figure.
    fix:    Same as H6: delete the `<text>` line, neutralise `<title>` and
            `aria-label` to "H7 number-line answer choices A through G."

  H6 | criterion 7 (referenced image content) | `media/h6-number-line-options.svg`
    found:  every option label drawn at `x="20"` while its axis starts at `x="90"`
            (`<text x="20" y="77">A. open circle at 6, ray right</text>`, and the
            same at y=145, 213, 281, 349, 417, 485)
    why:    Confirmed on the render, not inferred from coordinates: the axis
            (`stroke-width:2`) runs through the middle of every label, and on rows
            C and D the 5px ray, drawn leftward from x=454 to x=90, overprints the
            label. "C. open circle at 6, ray left" and "D. closed circle at 6, ray
            left" are close to illegible. A student who cannot read the option
            labels cannot map the figure onto the seven text choices.
    fix:    Give each row its own left gutter: move the axis, ticks, dots and rays
            right by 220px (axis `x1` 90 -> 310, `x2` 505 -> 725; dot `cx` 428/454/480
            -> 648/674/700), or place each label on its own line above its axis
            (`y` of the label = axis `y` - 18) and raise the figure height.

  H7 | criterion 7 (referenced image content) | `media/h7-number-line-options.svg`
    found:  same construction; labels at `x="20"`, axis from `x="90"`
    why:    Same overprint, confirmed on the render. Rows C and D are struck
            through by the leftward ray; on row E the minus sign of
            "open circle at -2" is crossed by the axis.
    fix:    Same 220px right shift of the axis/tick/dot/ray geometry (dot `cx`
            246/350/376 -> 466/570/596), or labels on their own line.

## CANDIDATES RULED ON

  Coordinator: H6/H7 SVGs state their own answer three times (rendered `<text>`,
  `<title>`, `aria-label`) -> **CONFIRMED**, verified independently by reading the
  SVG source and by my own headless-Chromium render of both files; the sentence is
  the first visible line in both bitmaps.

  Coordinator: option labels at x=20 are struck through by the axis at x=90, worse
  in H6/H7 than A1 -> **CONFIRMED** on the render; C and D are the worst rows in
  both files, with the 5px leftward ray over the text.

  Coordinator: no `$IMS-CC-FILEBASE$` token anywhere in the corpus; SVGs declared
  as `<file>` inside the QTI resource, not as webcontent -> **CONFIRMED** by grep
  over all 14 packages (token count 0; only 3 `src=` attributes corpus-wide, all
  plain relative) and by reading `imsmanifest.xml` (no `webcontent` resource).

  Audit: H6 and H7 reference images by plain `src="media/..."`, import-blocking
  -> **CONFIRMED** (same evidence). One qualification the fixer should know: the
  seven `<response_label>` texts do restate every option in words, so the item is
  not literally unanswerable if the image 404s — but the stem tells the student to
  "Use the graphic choices", and an unresolvable referenced image is a criterion-7
  failure on its own terms. The defect stands either way.

  Audit: H5 — `y > -6` and `-6 < y` are implied by but not equivalent to `6 < y`,
  so leaving them unkeyed is correct -> **CONFIRMED** (the audit's ruling is
  right, so this is not a defect). `6 < y` means `y > 6`. `y > 6` implies `y > -6`,
  but `y = 0` satisfies `y > -6` and fails `6 < y`, so the implication is strictly
  one-way and neither choice is an equivalent form. The stem asks for equivalent
  inequalities, so `choice_6` and `choice_7` are correctly negated. Note also that
  `choice_6` "y > -6" and `choice_7` "-6 < y" are the same statement written two
  ways; their visible text differs, so this is not the duplicate-visible-text
  defect of criterion 6, and both are negated consistently.

  Audit: G1-H7 and all fill-ins clean -> **REFUTED for H7** (three defects above:
  image src, answer leak, label overprint). **CONFIRMED for the fill-ins**: E1 E2
  E3 E4 F6 H1 H2 all recomputed and correct; also G1 (the multiple-answers item)
  is clean on the mathematics.

## OBSERVATIONS THAT ARE NOT DEFECTS (ruled explicitly)

  F4 — the QTI stem "To undo x5, use the inverse operation ____." with key
  "divide by 5" matches the named source, `6thGradeReviewUpdated.pdf` F4
  ("Undo x5, use inverse op:"), and is mathematically right. The older
  `6thGradeReview.pdf` and the explanations companion both still pose "To undo
  /5" with checked answer "multiply by 5". That is a stale companion versus the
  updated worksheet, upstream of this package. The QTI is correct against the
  revision it is supposed to track, so no defect is charged here — but a companion
  that contradicts the worksheet on this item is worth an upstream ticket.

  H6/H7 `choice_7` reads "Point only at 6" / "Point only at 2" while the figure
  labels row G "open point only at 6" / "open point only at 2". Wording drift only:
  under either reading the choice is false (a lone point is not the graph of a
  strict inequality) and it is negated, so there is no scoring consequence.

  F3 — the companion writes the key as "subtract 8 (or -8)". The "or" form does
  not create a criterion-4 problem here because the item offers only "subtract 8";
  there is no "-8" choice to require alongside it.

  E3 stem contains a single `$` in "cost $20". It is currency, unpaired, and the
  item carries no math delimiters, so it is not the stray-`$` delimiter fault of
  criterion 7. It matches the worksheet.

## CLEAN

  E1 — 5/8 = 0.625 > 0.61; key "5/8" is the simplified a/b the stem asks for;
       matches worksheet E1 and companion checked answer.
  E2 — 21/7 = 3, 4*3 = 12; key 12.
  E3 — 20/4 = 5 per snack, 7*5 = 35; key 35 (companion "35 dollars"; stem says
       number only, so the bare 35 is right).
  E4 — 18/6 = 3, 5*3 = 15; key 15 (companion "x = 15"; stem says value only).
  F1 — 7 in 7m is the coefficient. Every other choice false: m is the variable;
       7m is not a constant term; there is no exponent, no sum, no inequality;
       "product only" is false of the factor 7.
  F2 — n in n + 8 = 12 is the variable. 8 and 12 are the constants, n is not a
       coefficient, not an operation, not an inequality symbol, not a factor pair.
       "answer only" is a true-ish restatement of a different question (n's value
       is the answer) but is false as a name for n's role; recorded as the weaker
       case and ruled not a defect.
  F3 — inverse of +8 is subtract 8. add 8, x8, /8, subtract 4, add 0 and "change
       the variable" all fail the round trip.
  F4 — inverse of x5 is divide by 5. "multiply by 1/5 then add 5" is the near
       miss: multiply by 1/5 alone would be equivalent, the trailing "add 5"
       breaks it, so it is correctly negated. See the F4 note above.
  F5 — 6y - 2y = (6-2)y = 4y. 8y, 4, 6y - 2, 12y, 3y, y + 4 all false.
  F6 — 5(4) - 3 = 20 - 3 = 17; key 17.
  G1 — 3(y + 6) = 3y + 18. `choice_5` "3(y) + 6" evaluates to 3y + 6, not
       equivalent; 3y + 6, y + 18, 18y, 9y, 3y - 18 all false. No unkeyed-true.
  H1 — x = 18 - 7 = 11; key 11.
  H2 — x = 6*4 = 24; key 24.
  H3 — x + 3 > 8 gives x > 5. x < 5, x >= 5 (admits x = 5, which fails), x > 11,
       x < 11, "5 > x" (= x < 5), x = 5 all non-equivalent and all negated.
  H4 — x - 4 < 2 gives x < 6. x > 6, x <= 6 (admits x = 6), x < -2, x > -2,
       "6 < x" (= x > 6), x = 6 all non-equivalent and all negated.
  H5 — 6 < y is exactly y > 6; key `choice_1`. See the candidate ruling above for
       `choice_6` / `choice_7`.
  H6 — mathematics clean: 6 < y is y > 6, graph is an open circle at 6 with the
       ray to the right = `choice_1`; companion agrees ("Open circle at 6, shade
       to the right (same as y > 6)"). The SVG geometry is also internally
       correct — the axis maps value = (x - 298)/26, so cx=454 is 6, cx=428 is 5,
       cx=480 is 7, and the seven drawn rows match the seven choice texts in order.
       Item is charged only for the three figure/manifest defects above.
  H7 — mathematics clean: x > 2 is an open circle at 2, ray right = `choice_1`;
       companion agrees. SVG geometry correct: cx=350 is 2, cx=246 is -2,
       cx=376 is 3. Charged only for the three figure/manifest defects above.

Structure and markup elsewhere in the slice: XML parses clean, UTF-8 declared,
`>=` / `<=` and `>` / `<` correctly entity-escaped in H3/H4/H5/H6/H7, no math
delimiters and so no unbalanced `\( \)` or `$...$`, no duplicated instruction
block, no two choices with identical visible text in any item, and the
required/negated split is coherent on all eleven multiple-answers items
(one required, six negated, every choice accounted for).
