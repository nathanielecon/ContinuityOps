SLICE: G1a          SCORE: 6/10
ITEMS WORKED: 18 of 18     (A1, B1-B6, C1-C7, D1-D4 — none skipped)

Shape B confirmed: `respident="response"`, idents `choice_1..choice_7` / `answer1`,
no `correct_*` / `wrong_*` naming, all items under 8 choices, two respconditions on
D3 and D4. Choice count and the second respconditions are NOT scored as defects.
Package carries no checksum and no validation record; every claim below is my own
recomputation from the stem and the source worksheet, not inherited.

All 18 keys are mathematically correct and all 18 stems match the 6th Grade Review
worksheet (updated revision), verified against the rendered page 1, not against
`pdftotext` output. All three defects below are in a single item, A1, and all three
are in its figure.

CACHE REBUILD — RE-READ AND RE-VERIFIED

The coordinator reported that the extractor which built `slices/*.json` unescaped
HTML entities before stripping tags, silently truncating 89 of 157 cached stems,
and rebuilt `slices/G1a.json`. I re-read the rebuilt cache. Findings for this slice:

  - G1a is substantively unchanged by the rebuild. No stem in my range lost any
    mathematics, and my verdict and score are unaffected.
  - Exactly one item in my range carries escaped entities at all: A1, which holds
    `&lt;img …/&gt;`. B1-B6, C1-C7 and D1-D4 contain zero entities in their stems,
    their choice labels and their keyed values, so the bug could not have touched
    them. I checked this mechanically rather than by eye.
  - For A1 the two extraction orders differ by exactly the `<img …/>` tag and
    nothing else, because the tag is the last token in the stem — so nothing after
    it was swallowed. Both the old and the rebuilt extractor drop the tag from the
    prose stem and record the file in `images[]`, which is the wanted behaviour for
    a prose stem. A1's stem prose is intact in both.
  - The bug's mechanism corroborates defect 2 below rather than weakening it. The
    single layer of XML escaping is what makes A1's `<img>` a *live* HTML tag: the
    XML parse of `mattext texttype="text/html"` yields the literal string
    `<img src="media/…" />`, which Canvas then renders as an actual image. It is a
    real image reference, and it really does need the `$IMS-CC-FILEBASE$/` token.

  I did not rely on the cache for any judgement in this report. I read all 18 stems
  from the raw XML before the rebuild notice arrived, and after it I re-derived the
  scoring truth independently: parsing the `<respcondition>` tree with ElementTree
  and assigning each `<varequal>` to required or negated by `<not>` nesting depth
  parity, so a hypothetical double negation could not be miscounted. All 18 items
  reproduce the rebuilt cache's `required` / `negated` lists exactly, every
  `<setvar>` is 100, and every `respident` is `response`. The cache and the XML now
  agree along two independent paths.

DEFECTS

  A1 | 7 (referenced image content) | media/a1-number-line-options.svg
    found:  <text x="20" y="30">A1 number-line choices. Correct: choice A, closed point at 4.</text>
            <title>A1 number-line choices. Correct: choice A, closed point at 4.</title>
            <svg ... role="img" aria-label="A1 number-line choices. Correct: choice A, closed point at 4.">
    why:    The string occurs three times in the file (grep count for "Correct:" = 3).
            The `<text>` occurrence is a rendered element, not a comment and not
            metadata: it sits at (20,30) inside the 960x560 viewport, the `<style>`
            block sets only `font-family` and `font-size` for `text` (no `fill:none`,
            no `display:none`, no `opacity`), and the background is `<rect
            width="100%" height="100%" fill="white"/>`, so it paints black on white.
            I rasterised the SVG independently with cairosvg (a different renderer
            from the coordinator's headless Chromium) and read the bitmap: the
            sentence is the first visible line of the graphic, above choice A.
            Second path: the same string is the `<title>`, which is the browser
            tooltip. Third path: the same string is the `aria-label` on
            `role="img"`, which a screen reader announces before any choice.
            A1's keyed choice is `choice_1` = "Point at 4"; the figure names it.
            The artifact exists so a student can find out whether their homework
            answer was right — an item that prints its own answer cannot do that,
            and it silently converts A1 into a free point for everyone.
    fix:    Delete the `<text x="20" y="30">…</text>` element entirely. Replace the
            `<title>` text and the `aria-label` value with a description that does
            not name the answer, e.g.
            "A1 number-line choices A through G: seven number lines from -8 to 8,
            each with one point plotted, or none for choice G."

  A1 | 7 (import validity) | presentation/material/mattext, `<img src>`
    found:  &lt;img src="media/a1-number-line-options.svg" alt="Accessible number-line option graphic for A1: correct choice described in text and image." /&gt;
    why:    Canvas rewrites in-quiz image paths only when they carry the
            `$IMS-CC-FILEBASE$/` token. I grepped the whole extracted corpus myself:
            `IMS-CC-FILEBASE` appears 0 times in any of the 14 packages, there are
            exactly 3 `src=` attributes corpus-wide (a1, h6, h7) and all 3 are bare
            `media/…` paths. `imsmanifest.xml` compounds it: the three SVGs are
            declared as `<file href="…/media/*.svg" />` entries *inside* the
            `type="imsqti_xmlv1p2"` resource, and `type="webcontent"` appears 0 times
            in the corpus, so the files are never published to a resolvable course
            path. On import the bare path resolves relative to the quiz page URL and
            404s. A1's stem says "Use the graphic choices", so the image IS the
            question: with it missing, a student sees seven bare text labels and no
            graphic to choose among. Import-blocking per criterion 7.
            (Note the `alt` text also asserts "correct choice described in text and
            image", which is a fourth place the answer is hinted; the `alt` at least
            does not name choice A, so I do not score it separately.)
    fix:    Change the `src` to `src="$IMS-CC-FILEBASE$/media/a1-number-line-options.svg"`
            and declare the media files in a companion resource:
            `<resource identifier="…_media" type="webcontent" href="sixth_grade_review_section_1_accuracy_check/media/a1-number-line-options.svg">`
            with `<file href="…"/>` for each SVG, rather than listing them inside the
            `imsqti_xmlv1p2` resource. Apply the same change to h6 and h7 (slice G1b).

  A1 | 7 (referenced image content) | media/a1-number-line-options.svg, all 7 rows
    found:  <text x="20" y="77">A. point at 4</text>  … <text x="20" y="417">F. point at 4.5</text>
            <line class="axis" x1="90" y1="70" x2="505" y2="70"/>  (and rows at y=138,206,274,342,410,478)
    why:    Every choice label is drawn at x=20 while every axis line starts at
            x=90. At `font-size:16px` Arial, "A. point at 4" is roughly 104px wide
            and so runs to about x=124, overrunning the axis start by ~34px. My
            cairosvg render confirms the collision on all seven rows: the axis
            strikes through the tail of each label. Worst cases are "F. point at 4.5"
            (the "4.5" is overprinted by the axis and the first tick) and
            "B. point at -4" (the "-4" is struck through, and a struck-through minus
            sign is exactly the character a student must read to tell choice B from
            choice A). This is a legibility defect in the graphic that the stem
            directs the student to use.
    fix:    Move each axis right and shorten the number line, or move the labels to
            their own line above each axis. Minimal edit: change every
            `<line class="axis" x1="90" …>` to `x1="150"`, change every tick `<line
            x1="…">` and tick `<text x="…">` by +60, change every `<circle class="dot"
            cx="…">` by +60 (so 402→462, 194→254, 298→358, 376→436, 428→488,
            415.0→475.0), extend the axis `x2` from 505 to 565, and widen the SVG
            `width` from 960 to 1020.

CANDIDATES RULED ON

  "Shape B. No checksum, no validation record, never checked by anyone."
    -> CONFIRMED (context, not a defect). No checksum or validation artefact exists
       for this package; I treated every prior claim as unverified and recomputed
       all 18 items from the stem and the worksheet.

  "A1 references `src=\"media/a1-number-line-options.svg\"` as a plain path, not
   Canvas's `$IMS-CC-FILEBASE$/` token. The image IS the question here, so this is
   import-blocking. Check every image reference in your slice the same way."
    -> CONFIRMED. Verified in the raw XML, and extended: 0 occurrences of the token
       and 0 `webcontent` resources corpus-wide, with the SVGs mis-declared inside
       the QTI resource. A1 is the only image reference in slice G1a; h6 and h7 have
       the identical defect but fall in slice G1b.

  "Audit reported the Section 1 select-all items (A1, F1-F5) clean and every fill-in
   answer correct. Verify independently."
    -> REFUTED for A1, CONFIRMED for the fill-ins in this slice. A1 is not clean:
       its figure leaks the answer and its label geometry is broken (above), on top
       of the import defect the audit itself raised — so "clean" was wrong even by
       the audit's own list. F1-F5 are outside slice G1a. Every fill-in key in G1a
       (B1-B6, C1-C7, D1-D4) is independently correct; see CLEAN.

OBSERVATIONS RULED NOT DEFECTS

  C7 stem wording. Worksheet reads "15% of $80 =" ; the QTI stem reads "15% of 80 =",
  dropping the dollar sign. Not a criterion-1 defect: the number is unchanged, the
  keyed value 12 is unchanged, the QTI instruction is "Enter the number only, no
  units or symbols", and the explanations companion restates the question the same
  way ("15% of 80 ="). No student can be scored differently because of it.

  D3 and D4 second respconditions. D3 keys 3.6 then 3.60; D4 keys 7 then 7.00. Both
  are trailing-zero equivalent-form alternates, which is exactly the Shape B pattern
  the rubric says not to flag — and here they are load-bearing, because both stems
  say "Enter a decimal rounded to two places", so a compliant student types 3.60 /
  7.00 and the second block is what accepts them. Good design, not a defect.

  A1 distractor "Point at -4" and "Point at 4.5" are off the worksheet's own number
  line (worksheet A1 shows only 0 through 5). Not a criterion-5 defect: both are
  false and neither is keyed, so no correctly reasoning student can be punished.

CLEAN

  B1  8 + 3 x 4: multiply first, 3 x 4 = 12, 8 + 12 = 20. Key 20. Correct.
  B2  (21 - 4) x 3: 17 x 3 = 51. Key 51. Correct.
  B3  2^4 + 1: 16 + 1 = 17. Key 17. Correct. (Worksheet shows a true superscript;
      confirmed on the rendered page, not from extraction order.)
  B4  (5 + 1)^2: 6^2 = 36. Key 36. Correct.
  B5  3(2^2): 3 x 4 = 12. Key 12. Correct. Distinct from B6 as the worksheet
      intends: 3(2^2) = 12 but (3 x 2)^2 = 36, and the two keys do differ.
  B6  (3 x 2)^2: 6^2 = 36. Key 36. Correct.
  C1  82.731: 8 tens, 2 ones, 7 tenths, 3 hundredths, 1 thousandth. Tenths = 7.
      Key 7. Correct.
  C2  314.70 + 29.58 = 344.28. Key 344.28. Correct.
  C3  81.50 - 7.94 = 73.56. Key 73.56. Correct.
  C4  0.32 x 100 = 32, so 0.32 = 32%. Key 32, and the stem says to omit the % sign,
      so the bare 32 is the right form. Correct.
  C5  65 / 100 = 0.65. Key 0.65. Correct.
  C6  0.8 = 8/10 = 4/5 (gcd 2); 4 and 5 are coprime so 4/5 is simplest. Key 4/5,
      matching the companion's built-up fraction, which I read from the rendered
      page rather than trusting extraction order. Correct. Single respcondition,
      `case="No"`, and the stem forbids spaces and mixed numbers, so the one keyed
      string is the only form the stem permits.
  C7  15% of 80 = 0.15 x 80 = 12. Key 12. Correct.
  D1  9 x 6 = 54. Key 54. Correct.
  D2  63 / 9 = 7. Key 7. Correct.
  D3  2.4 x 1.5: 24 x 15 = 360, two decimal places, = 3.60 = 3.6. Keys 3.6 and 3.60.
      Correct, both forms accepted.
  D4  5.6 / 0.8 = 56 / 8 = 7. Keys 7 and 7.00. Correct, both forms accepted.

  Structure and markup across all 18: `respident="response"` throughout; A1's
  required/negated split is coherent (choice_1 required, choice_2..choice_7 each
  negated, and I confirmed each negated choice is genuinely false by measuring the
  SVG dot positions — axis origin x=90 at -8 with 26px per unit, so cx 402=4,
  194=-4, 298=0, 376=3, 428=5, 415=4.5, row G no dot, matching the seven labels);
  no two choices share visible text; 0 `$` characters and 0 `\(` sequences in any
  stem in the slice, so no mixed or unbalanced math delimiters; exactly one
  instruction sentence per stem, no duplicated instruction block.
