# G1b — round 2 judge report (re-score after fixer)

SLICE: G1b (6th Grade Review Section 1, items E1-H7)          SCORE: 9/10
ITEMS WORKED: 18 of 18   (all re-checked; H6 and H7 re-derived from scratch)
PREVIOUS: 6/10, six defects, all on H6/H7 figures and the manifest.

Six defects verified fixed. One new defect stands, on the rows C and D arrowheads
of both figures — the extra item the coordinator asked me to rule on. My ruling is
below, with the render that settles it and a fix I tested before proposing.

## RULING ON THE EXTRA ITEM: leftward-ray arrowhead placement — DEFECT

  H6 | criterion 7 (referenced image content) | `media/h6-number-line-options.svg`, rows C and D
  H7 | criterion 7 (referenced image content) | `media/h7-number-line-options.svg`, rows C and D
    found:  `<line class="ray" x1="674" y1="206" x2="310" y2="206" style="marker-end:none;marker-start:url(#arrow)"/>`
            and the same at y=274; H7 the same with x1=570.
    why:    Two independent failures, both confirmed on my own 1180x560 render of
            each file, not inferred from the attributes.

            (a) Ink on the excluded side. The marker is
            `markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"
            markerUnits="strokeWidth"` with path `M0,0 L0,6 L9,3 z`, and `.ray` is
            `stroke-width:5`. `markerUnits="strokeWidth"` scales the 9x6 path by 5
            to 45x30 px. `refX="9"` puts the reference point at the tip, and
            `marker-start` pins that reference point to the first vertex, x=674.
            `orient="auto"` aligns local +x with the path direction, which here is
            leftward, so the body extends 45px in global +x, from 674 to 719. On
            the verified mapping below that is values 6 to 7.73. Rows C and D are
            labelled "ray left" from 6, i.e. the set y < 6 and y <= 6, so the
            figure paints a solid filled wedge across (6, 7.73] — an interval the
            graph must leave blank. On a number line, ink on the line means
            membership. The row contradicts its own label. H7 is the same with the
            wedge across (2, 3.73].

            (b) No arrowhead at the unbounded end. `marker-end:none` strips the
            marker from x=310 (value -8), so the ray terminates in a bare butt end
            and reads as a bounded segment [-8, 6] rather than an unbounded ray.
            Rows A, B, E and F in the same figure do carry a terminal arrowhead at
            the far end. So one figure runs two contradictory conventions, and the
            arrowhead stops being a cue the student can rely on while comparing
            seven graphs side by side.

            Severity, stated plainly: scoring is unaffected. The key is choice A in
            both items, C and D are negated, and a student who misreads C or D
            still cannot be credited for them. This is not a wrong-key defect and
            it is nothing like the answer leak. But criterion 7 covers whether a
            referenced figure reads correctly, the whole task in H6/H7 is "compare
            seven number-line graphs", and two of the seven do not depict what they
            claim. That is a defect, so the slice cannot take 10/10.

            Pre-existing, not a regression: confirmed, the same
            `marker-end:none;marker-start:url(#arrow)` construction sits in the
            original at x1=454, x2=90. The fixer shifted coordinates and preserved
            the attributes, exactly as instructed. No blame attaches to the fix.
    fix:    Delete the whole attribute `style="marker-end:none;marker-start:url(#arrow)"`
            from both lines in each file — four lines total, two per figure. No
            other change. The `.ray` class then supplies `marker-end:url(#arrow)`,
            which pins the marker to the last vertex (x=310) with `orient="auto"`
            still pointing leftward: tip at 310, body back to 355, entirely inside
            the shaded region, and the same convention rows A/B/E/F already use.

            I did not guess at that. I copied `h6-number-line-options.svg` to my
            own scratchpad, applied exactly that deletion there, and rendered it at
            1180x560. Result read off the bitmap: rows C and D now carry a
            leftward arrowhead at the far-left end of the ray, there is no ink to
            the right of the open/closed circle at 6, and all seven rows use one
            convention. The package itself was not touched — the edited copy lives
            at `.../scratchpad/g1bjudge/h6_fixtest.svg`, outside the package tree.

## THE SIX EARLIER DEFECTS — RE-VERIFIED

  Value-to-pixel mapping re-derived from the new files, not carried over from the
  shift. Tick labels in H6/H7 run from `<text x="306" y="97">-8</text>` to
  `<text x="722" y="97">8</text>`, ticks at x=310 + 26k, and the label glyph sits
  4px left of its tick, so tick(0) = x=518 and **value = (x - 518)/26**. Sanity
  check on the whole axis: value(310) = -8, value(726) = +8, both exact. The old
  origin was 518 - 220 = 298, consistent with a uniform +220 shift, but the
  mapping above stands on its own reading of the new tick labels.

  1. H6 answer leak -> FIXED. `Correct:` returns zero hits corpus-wide. `<title>`
     and `aria-label` both read "H6 number-line answer choices A through G.", the
     `<text x="20" y="30">` element is gone, and my render's first visible line is
     row A, not a sentence. Stem `alt` now reads "...answer choices described in
     text and image."
  2. H7 answer leak -> FIXED. Same three surfaces, same evidence, same render.
  3. H6 label overprint -> FIXED. Labels still at x=20, but the axis now starts at
     x=310, so nothing crosses them. On the render "C. open circle at 6, ray left"
     and "D. closed circle at 6, ray left" are fully legible, as are all seven.
  4. H7 label overprint -> FIXED. Same, including row E where the minus sign of
     "open circle at -2" is now clear of the axis.
  5. H6 image src -> FIXED. `src="$IMS-CC-FILEBASE$/media/h6-number-line-options.svg"`.
  6. H7 image src -> FIXED. `src="$IMS-CC-FILEBASE$/media/h7-number-line-options.svg"`.
     A1 was fixed at the same time (not my slice). The manifest now carries
     `<resource identifier="..._media" type="webcontent" href=".../media/a1-number-line-options.svg">`
     listing all three SVGs, with a matching `<dependency identifierref="..._media"/>`
     added to the QTI resource, and the media `<file>` entries removed from the QTI
     resource. That is the structure Canvas needs for the token to resolve.

  Dot placement re-checked against my own mapping, independent of the labels:
  H6 cx 674/674/674/674/648/700/674 -> 6, 6, 6, 6, 5, 7, 6.
  H7 cx 570/570/570/570/466/596/570 -> 2, 2, 2, 2, -2, 3, 2.
  Both agree with the seven choice texts, in order, and with the fills
  (white = open, #075985 = closed) on rows A/B and C/D.

  No collateral damage: all five XML/SVG files still parse well-formed; all 18
  stems, keys, negated sets, choice counts (7 or 1) and respcondition counts (1)
  are byte-identical to round 1; the seven `<response_label>` texts in H6 and H7
  are unchanged.

## OBSERVATION RULED NOT A DEFECT

  H6 row F, "open circle at 7, ray right". Its ray is `x1="700" x2="725"`, only
  25px, while the marker body is 45px, so the arrowhead's base overshoots
  backwards to x=680 = value 6.23 and paints (6.23, 7) — outside "x > 7". Visible
  on the render as the triangle's left edge sitting left of the circle. Same root
  cause as rows C/D, and I am charging C/D, so I have to say why this one is not.
  It is not, because the overshoot does not misplace or remove the convention cue:
  the arrowhead is at the correct end, pointing the correct way, the circle at 7 is
  drawn after the ray and stays legibly open on top of it, and the row still reads
  as "open circle at 7 with the ray going right". The same 45px overshoot exists on
  rows A, B and E of both figures, where it falls inside the shaded set and is
  invisible; row F is the only place it pokes out, and only by 0.77 of a unit. It
  is a cosmetic artifact, not a row that depicts the wrong set. Optional polish if
  the fixer is in the file anyway: extend the axis and ticks to +9 and end row F's
  ray at that tick, which gives the marker room. Not required.

  Carried forward unchanged from round 1, still ruled not defects: the F4
  worksheet-versus-companion mismatch (QTI matches the updated worksheet and is
  correct; the stale companion is an upstream ticket), the "Point only at 6" versus
  "open point only at 6" wording drift between choice text and figure label, the
  "subtract 8 (or -8)" companion phrasing, and the currency `$` in E3.

## CANDIDATES RULED ON

  Coordinator: rows C and D put the arrowhead at the circle end rather than the
  far end, because `marker-start` pins it to the path's start vertex ->
  **CONFIRMED**, and **ruled a defect** on both H6 and H7, for the two reasons
  above. The coordinator's reading of the mechanism is exactly right; I add the
  quantified consequence, that the filled marker paints 1.73 units of the excluded
  side, and a fix verified by render.

  Coordinator: pre-existing in the original zip, not a fixer regression ->
  **CONFIRMED** against the original construction (x1=454, x2=90, same attributes).

  Coordinator: scoring unaffected because C and D are distractors and the key is
  choice A -> **CONFIRMED**. Charging the defect does not change any key.

  Coordinator: leak gone, C and D legible, dots on 6, 6, 6, 6, 5, 7, 6 ->
  **CONFIRMED** independently, by my own render and my own re-derived mapping.

## CLEAN

  All 18 items still clean on the mathematics; nothing in the fix touched a stem,
  a key or a choice. Carried forward from round 1 and re-confirmed against the
  post-fix XML: E1 (5/8 = 0.625 > 0.61), E2 (12), E3 (35), E4 (15), F1
  (coefficient), F2 (variable), F3 (subtract 8), F4 (divide by 5, matching the
  updated worksheet's "Undo x5"), F5 (4y), F6 (17), G1 (3y + 18), H1 (11), H2 (24),
  H3 (x > 5), H4 (x < 6), H5 (y > 6, with `y > -6` and `-6 < y` correctly left
  unkeyed as one-way implications), H6 (open circle at 6, ray right), H7 (open
  circle at 2, ray right). No true-but-unkeyed choice anywhere in the slice; no
  false-but-keyed choice; every key agrees with the explanations companion's
  checked answer.
