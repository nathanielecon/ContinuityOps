SLICE: G1a          SCORE: 10/10
ITEMS WORKED: 18 of 18     (A1, B1-B6, C1-C7, D1-D4 — none skipped)

Cold read. I formed this verdict from the raw XML, the rendered SVG bitmap, the
rendered worksheet pages and the pristine pre-repair package before opening
G1a-r1.md or G1a-r2.md. I did not use `slices/G1a.json` or `corpus.json` for any
judgement. Where I reach the same conclusion as the earlier judges I say so and
say by what independent path; two checks below are ones neither judge performed.

Shape B confirmed: `respident="response"` on all 18; idents `choice_1..choice_7`
(A1) and `answer1` (the other 17); no `correct_*` / `wrong_*` naming; every item
under 8 choices; two `<respcondition>` blocks on D3 and D4. Per the rubric's
Shape B section, choice count and the second respconditions are NOT defects, and
I inspected both second blocks before accepting them (see below).

DEFECTS

  None. No defect stands in this slice.

THE THREE A1 REPAIRS — VERIFIED INDEPENDENTLY

I recovered the pristine pre-repair package from the repository itself
(`/home/user/ContinuityOps/inbox/Inbox/6th-grade-review-section-1-accuracy-check-qti.zip`,
md5 of its item XML `00e41350bcbbe438393a4bde028e840d`) and diffed it against the
package under test. That gives me a real before/after, not a reconstruction.

  1. Answer leak in `media/a1-number-line-options.svg` -> CLOSED, all three vectors.

     Pre-repair the string "A1 number-line choices. Correct: choice A, closed
     point at 4." occupied all three places:
       - `<text x="20" y="30">` — a painted element, black on the white backing
         `<rect>`, no `display:none` / `opacity` / `fill:none` in the `<style>`;
       - `<title>` — the tooltip;
       - `aria-label` on `role="img"` — what a screen reader announces first.

     Post-repair: the `<text>` element is deleted; `<title>` and `aria-label` both
     read "A1 number-line answer choices A through G." Both accessibility hooks
     are still present and non-empty — `role="img"` retained, `aria-label`
     retained, `<title>` retained — which was the stated constraint.

     Confirmed by rendering, not by reading source: I rasterised the current SVG
     with cairosvg and read the bitmap. The image opens on row A; there is no text
     line above it. Residual scan of the SVG for `correct`, `answer is`, `key`,
     `solution`, `choice A`, XML comments, `<desc>` and `<metadata>`: zero hits on
     every one.

     Fourth vector, closed too: the QTI stem's `alt` said "correct choice
     described in text and image" pre-repair and now says "answer choices
     described in text and image". All three `alt` attributes in the package
     (A1, H6, H7) carry the neutral wording. The only match for "correct choice"
     left in the XML is inside A1's own instruction "Enter select all correct
     choices", which is not a leak.

  2. Label/axis collision -> CLOSED, and the geometry survives the shift.

     Pre-repair every axis began at x=90 while every label sat at x=20; the
     pre-repair render shows the axis striking through the tail of all seven
     labels, worst on "F. point at 4.5" and "B. point at -4" (the struck minus
     sign being the one glyph that distinguishes choice B from choice A).

     Post-repair: axes x1 90->150, x2 505->565, every tick and every dot +60,
     `width` 960->1020. In the rendered bitmap the longest label ends near x=99
     (SVG units) against an axis start of x=150. No row collides.

  GEOMETRY RE-DERIVED FROM THE BITMAP — not taken from the source, and not on trust

     I rendered at 2x and derived the map from the tick marks themselves, reading
     tick stems in a horizontal band above the axis line so the axis stroke could
     not be mistaken for a tick, and isolating the dots with a tight colour mask
     on the fill `#075985` so that antialiased label glyphs could not enter the
     dot centroid. (A loose colour mask does pull in label antialiasing — my first
     pass did exactly that and returned nonsense values such as row G "reporting"
     a dot at -11.3 where the image plainly shows none. Instrument at fault, not
     the SVG; I tightened the mask rather than believing the number.)

     Ticks: 17 per row, perfectly uniform, max residual against a linear fit 0.00px.
       x(v) = 715.5 + 52.0 v  (2x scale)  ==  x(v) = 357.75 + 26.0 v  (SVG units)

     Dot centre taken as the midpoint of the strict-colour mask's extent, which
     cancels antialias bias symmetrically:

       row A  label "point at 4"     span 902..945   centre 923.5  -> value +4.0000
       row B  label "point at -4"    span 486..529   centre 507.5  -> value -4.0000
       row C  label "point at 0"     span 694..737   centre 715.5  -> value  0.0000
       row D  label "point at 3"     span 850..893   centre 871.5  -> value +3.0000
       row E  label "point at 5"     span 954..997   centre 975.5  -> value +5.0000
       row F  label "point at 4.5"   span 928..971   centre 949.5  -> value +4.5000
       row G  label "no point"       no dot pixels                 -> none

     Every dot sits on the value its own label claims. Six dots, six distinct
     values, no two rows showing the same value — so exactly one row (A) shows a
     point at 4, and A1 has exactly one true choice.

     Cross-check that the shift preserved rather than accidentally corrected:
     the pre-repair SVG mapped x(v) = 298 + 26v with dots at 402, 194, 298, 376,
     428, 415.0 -> 4, -4, 0, 3, 5, 4.5. Correct before, correct after, every dot
     moved by exactly +60 (402->462, 194->254, 298->358, 376->436, 428->488,
     415.0->475). Scale unchanged at 26.0 px/unit. A uniform translation is what
     the residuals show: the tick fit residual is 0.00 and all six dots land on
     exact values, whereas a per-dot slip would show as scattered residuals.

  3. `$IMS-CC-FILEBASE$/` token and the `webcontent` resource -> APPLIED.

     Stem `src` is now `$IMS-CC-FILEBASE$/media/a1-number-line-options.svg`.
     In the manifest the three media `<file>` entries have been moved out of the
     `associatedcontent/.../learning-application-resource` resource and into a new
     `type="webcontent"` resource, and the `imsqti_xmlv1p2` resource now declares a
     `<dependency>` on it. Both `identifierref`s resolve to declared resources;
     every manifest `<file href>` exists on disk (0 missing); the manifest, the
     item XML and all three SVGs parse as well-formed XML.

     See FLAGGED RESIDUAL RISK below for the one aspect of this repair I could not
     settle by execution, which neither earlier judge examined.

NOTHING OUTSIDE THE REPAIR MOVED — proved by diff, not by recollection

Diffing the pristine original against the package under test, the entire item XML
differs on exactly three lines, and all three are A1/H6/H7's `src` and `alt`
strings. Every stem, every choice label, every `<respcondition>`, every
`<setvar>` and every keyed value in the file is byte-identical to the original —
including all 18 items in my range. B1-B6, C1-C7 and D1-D4 were never touched by
any fixer, so their content is the original author's and I verified it on its own
merits below rather than as a re-check of someone's edit. The manifest differs
only by the media-resource restructure. The SVG is the only other changed file.

MATHEMATICS — all 18 worked from the stem, against the updated worksheet

Source of truth: `6thGradeReviewUpdated.pdf` page 1, read as a 400dpi render, not
via `pdftotext` (the built-up fractions and true superscripts in sections B and C
are exactly what extraction transposes). Cross-checked against the explanations
companion's "Checked answer" lines. The companion's stale spot is F4 ("To undo
÷5 ... multiply by 5", where the updated worksheet says "Undo ×5" and the QTI
correctly keys "divide by 5") — that is outside my range, and every companion
entry inside my range agrees with the updated worksheet.

  A1  Worksheet: "Plot the point 4 on the number line below:" with a 0-5 line.
      Keyed choice_1 "Point at 4" — true, and bitmap-confirmed as the figure's
      row A. Every other choice worked from the stem and found FALSE:
        choice_2 "Point at -4"    -4 != 4
        choice_3 "Point at 0"      0 != 4
        choice_4 "Point at 3"      3 != 4
        choice_5 "Point at 5"      5 != 4
        choice_6 "Point at 4.5"  4.5 != 4
        choice_7 "No point shown"  plotting nothing is not plotting 4
      No equivalent-form trap among them: no "4.0", no "four", no restatement of
      4 in another form. All seven visible texts distinct.
  B1  8 + 3 x 4: multiply before add, 3 x 4 = 12, 8 + 12 = 20.        Key 20      OK
  B2  (21 - 4) x 3 = 17 x 3 = 51.                                     Key 51      OK
  B3  2^4 + 1 = 16 + 1 = 17.                                          Key 17      OK
  B4  (5 + 1)^2 = 6^2 = 36.                                           Key 36      OK
  B5  3(2^2) = 3 x 4 = 12.                                            Key 12      OK
  B6  (3 x 2)^2 = 6^2 = 36.                                           Key 36      OK
      B5 and B6 are the pair the worksheet sets up to be confused; the keys do
      differ (12 vs 36) and each matches its own grouping.
  C1  82.731 = 8 tens, 2 ones, 7 tenths, 3 hundredths, 1 thousandth.  Key 7       OK
  C2  314.70 + 29.58: 0.70+0.58 = 1.28, 314+29 = 343, total 344.28.   Key 344.28  OK
  C3  81.50 - 7.94: 81.50 - 8.00 = 73.50, +0.06 = 73.56.              Key 73.56   OK
  C4  0.32 x 100 = 32, so 0.32 = 32%. Stem says omit the % symbol.    Key 32      OK
  C5  65% = 65/100 = 0.65.                                            Key 0.65    OK
  C6  0.8 = 8/10, gcd(8,10) = 2, = 4/5; 4 and 5 coprime so simplest.  Key 4/5     OK
      Companion's built-up fraction read from the render, not extraction order.
  C7  15% of 80 = 0.15 x 80 = 12.                                     Key 12      OK
  D1  9 x 6 = 54.                                                     Key 54      OK
  D2  63 / 9 = 7.                                                     Key 7       OK
  D3  2.4 x 1.5: 24 x 15 = 360, two decimal places, 3.60 = 3.6.  Keys 3.6, 3.60   OK
  D4  5.6 / 0.8 = 56 / 8 = 7.                                    Keys 7, 7.00     OK

STRUCTURE AND MARKUP

  Scoring trees parsed as trees, never by flat regex: I walked each
  `<conditionvar>` recursively and assigned each `<varequal>` to required or
  negated by `<not>` nesting parity, so a `<varequal>` inside a `<not>` can never
  be counted as required.
    A1  required {choice_1}; negated {choice_2, choice_3, choice_4, choice_5,
        choice_6, choice_7}. Coherent, and it covers all seven choices exactly
        once — no choice left unconstrained, none constrained twice.
    17 fill-ins: one block each of `or(varequal V, and(vargte V, varlte V))`.
    Every `<setvar>` is 100; every `respident` is `response`.

  D3 and D4 second `<respcondition>` — inspected before accepting. D3's is
  3.6 / 3.60 and D4's is 7 / 7.00: the same value in a trailing-zero form, not a
  different value. They are load-bearing rather than cosmetic, because both stems
  say "Enter a decimal rounded to two places", so the compliant student types
  3.60 / 7.00. Traced both paths: an answer of "3.60" already satisfies block 1
  numerically via `vargte`/`varlte`, and "3.6" satisfies it via `varequal`; the
  second block is belt-and-braces. There is no input a correct student can give
  that scores 0, and `continue="No"` only halts after a match. Good design, not a
  defect, per the rubric's Shape B rule.

  No two choices in any item share visible text (checked across the whole file,
  not just my range).

  Math delimiters: 0 occurrences of `\(` or `\)` anywhere in the package, and the
  only `$` characters in my 18 items are the two in `$IMS-CC-FILEBASE$`. Both sit
  inside an `src` attribute, not in text content — strip the tags and A1's
  rendered text contains zero `$`, so there is no stray `$...$` pair for Canvas to
  render literally, and the token is substituted at import in any case.

  No duplicated instruction block: each of the 18 stems carries exactly one
  trailing format instruction.

  All four package files parse as well-formed XML. `points_possible` is 36,
  matching 36 items at 1 point.

CHECKS NEITHER EARLIER JUDGE PERFORMED

  1. `shuffle_answers` — and it matters for A1 specifically. The figure letters
     its rows A through G positionally, and the QTI choices are authored in the
     matching order (choice_1 "Point at 4" <-> row A, and so on). If Canvas
     shuffled the choices, "Point at 4" could display as option C while the
     figure's row A still showed the dot at 4, desynchronising the graphic from
     the list a student is choosing from. `assessment_meta.xml` sets
     `<shuffle_answers>false</shuffle_answers>`, so the ordering holds. Not a
     defect — but it is a live dependency of A1's design and it was unexamined.

  2. The `$IMS-CC-FILEBASE$` path depth. See below.

FLAGGED RESIDUAL RISK — recorded, ruled NOT a defect, unverifiable here

  The A1 `src` is `$IMS-CC-FILEBASE$/media/a1-number-line-options.svg`, while the
  file's manifest href is
  `sixth_grade_review_section_1_accuracy_check/media/a1-number-line-options.svg`.
  The token stands for the root of the package's imported web content; Canvas's
  own exports place that content under `web_resources/`. On that reading the token
  resolves to `media/a1-number-line-options.svg`, one path segment short of where
  the file actually sits, and the image would import as a broken link. Round 2
  checked that stripping the token and rejoining under the quiz folder finds a
  file on disk, which assumes the mapping rather than testing it.

  I rule this NOT a defect, for three reasons, and I am recording it rather than
  smoothing it because it is the one claim in the slice I could not settle by
  execution:
    - The rubric's criterion 7 states normatively that "Canvas expects
      `$IMS-CC-FILEBASE$/media/...`". That is exactly the form present, and it is
      the form COORD-figures.md and G1b-r1.md prescribed corpus-wide. Scoring it
      down would be scoring against a convention this project has already settled.
    - I have no second or third independent confirmation path — no Canvas to
      import into and no reference export in the repo. The standing rule says to
      suspect the instrument before the artifact, and here my only instrument is
      recollection of Canvas's importer.
    - Severity, on the rubric's own qualifier, is low. Criterion 7 calls a bad
      path import-blocking "wherever the image IS the question". For A1 it is not:
      all seven options are given verbatim as text choices ("Point at 4",
      "Point at -4", ...), so a student can answer A1 correctly with the image
      entirely absent, and the scoring is unaffected. A missing file yields a
      migration warning, not a failed import or a wrong key.

  If the coordinator wants it closed rather than flagged, the remedy is to move
  the three SVGs to `web_resources/media/` in the package and point the manifest
  `<file href>` entries there, leaving the `src` strings unchanged. The same
  question applies verbatim to H6 and H7 in slice G1b.

CANDIDATES RULED ON

  "Shape B; fewer than 8 choices is design, not a defect."
    -> CONFIRMED as design. All 18 items carry under 8 choices and I scored none
       of them for it.

  "The second `<respcondition>` on D3/D4 is a deliberate trailing-zero alternate."
    -> CONFIRMED, and inspected rather than assumed: 3.6/3.60 and 7/7.00 are the
       same value, both `<setvar>` 100, and both stems ask for two decimal places
       so the alternates are load-bearing.

  "This package had no checksum and no validation record before this run."
    -> CONFIRMED as context. I treated every prior claim as unverified and
       recomputed all 18 items from the stem and the rendered worksheet.

  Round-1 defect 1, answer leak in the SVG (text, title, aria-label)
    -> CONFIRMED as having been real, and CONFIRMED CLOSED. Verified against the
       pristine original, and closed on all three vectors plus the `alt` fourth.

  Round-1 defect 2, plain `src="media/..."` with no `webcontent` resource
    -> CONFIRMED as having been real, and CONFIRMED REMEDIATED, subject to the
       flagged residual risk above.

  Round-1 defect 3, label/axis collision
    -> CONFIRMED as having been real, and CONFIRMED CLOSED, with the value-to-
       pixel mapping re-derived from the bitmap and every dot on its claimed value.

  Round 2's verdict of 10/10
    -> I reach 10/10 independently, not by ratifying it. My dot measurements used
       a different method from round 2's (strict-colour extent midpoint against a
       tick fit, versus colour centroid against a fitted origin) and agree: round 2
       reports a uniform +0.0014 on all six dots, which is its centroid-versus-
       origin bias, and my method returns exact values. Two methods, same answer.

OBSERVATIONS RULED NOT DEFECTS

  C7 stem drops the dollar sign. Worksheet (updated) reads "15% of $80 ="; the QTI
  reads "15% of 80 =". The number and the key (12) are unchanged, the stem says
  "no units or symbols", and the older worksheet revision and the companion both
  write it without the "$". No student is scored differently. Not a criterion-1
  defect.

  A1 stem wording tracks the older revision. Updated worksheet: "Plot the point 4
  on the number line below:" with a printed 0-5 line. QTI: "Plot the point 4 on a
  number line. Use the graphic choices." The change is forced by the conversion to
  a select-all item with seven candidate figures — the QTI cannot say "the line
  below" when it offers seven. The number 4 and the mathematics are identical.
  Not a criterion-1 defect.

  A1's figure spans -8 to 8 while the worksheet's line spans 0 to 5, so the
  distractors "Point at -4" and "Point at 4.5" are off the worksheet's own line.
  Not a criterion-5 defect: both are false and neither is keyed, so no correctly
  reasoning student is punished, and the keyed choice is producible from the
  worksheet alone.

  `original_answer_ids` is `choice_1` on all 36 items, including the 17 fill-ins
  whose actual `<response_label ident>` is `answer1`. This is uniform across the
  package and is a corpus-wide authoring convention, not something this repair
  introduced; the field is advisory in Canvas's importer and no scoring depends on
  it. Not scored.

  The SVG canvas is 1020 wide while the drawing ends at x=566, leaving a 454px
  empty right margin. Pre-existing: the original was 960 wide with the identical
  454px margin, so the widening tracked the shift exactly and the fill fraction
  slightly improved. Not a regression and not a defect.

CLEAN

  A1, B1, B2, B3, B4, B5, B6, C1, C2, C3, C4, C5, C6, C7, D1, D2, D3, D4.

  All 18 worked. Nothing stands. 10/10.
