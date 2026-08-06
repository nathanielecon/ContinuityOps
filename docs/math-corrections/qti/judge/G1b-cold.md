# G1b — cold validation judge report

SLICE: G1b (6th Grade Review Section 1, items E1-E4, F1-F6, G1, H1-H7)   SCORE: 9/10
ITEMS WORKED: 18 of 18   (E1 E2 E3 E4 F1 F2 F3 F4 F5 F6 G1 H1 H2 H3 H4 H5 H6 H7)
SHAPE: B. Fewer than 8 choices per item is this corpus's design and is not scored
as a defect. Every item in this slice carries exactly one `<respcondition>`, so the
"second respcondition" allowance never applies here.

One defect stands: **H6, figure row F**. It is the same defect class, on the same
criterion, in the same file, that r2 charged against rows C and D and that r3
declined to charge here. I overturn r3's ruling, and I do so on measurement, not
on taste. Everything else in the slice is clean, including all 18 items'
mathematics, which I reworked from the source before reading any prior report.

Files read as authoritative:
`/tmp/qtiwork/pkg/6th-grade-review-section-1-accuracy-check-qti/` (XML, manifest,
both SVGs; XML mtime 00:03, both SVGs 00:11 — unchanged since r3 scored them).
Source: `6thGradeReviewUpdated.pdf`, read **rendered at 300 dpi**, not extracted.
Companion `6thGradeReviewExplanations.pdf` used only to corroborate keys.

---

## DEFECTS

### H6 | criterion 7 (referenced image content) | `media/h6-number-line-options.svg`, row F

**found:**

```
.ray{stroke:#075985;stroke-width:5;marker-end:url(#arrow)}
<marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3"
        orient="auto" markerUnits="strokeWidth">
  <path d="M0,0 L0,6 L9,3 z" fill="#075985"/></marker>
...
<text x="20" y="417">F. open circle at 7, ray right</text>
<line class="ray" x1="700" y1="410" x2="725" y2="410"/>
<circle class="dot" cx="700" cy="410" r="9" fill="white"/>
```

**why:**

*Mapping, re-derived from the current tick labels, not assumed.* The 17 tick lines
in every row sit at x = 310, 336, … 726 for values -8 … +8. Spacing 26 px/unit,
zero at x = 518. Check at both ends: (310-518)/26 = -8.000, (726-518)/26 = +8.000.
So **value = (x - 518)/26**.

*Marker size.* `markerUnits="strokeWidth"` scales the marker's 9x6 path by the
ray's `stroke-width:5`, giving a filled triangle **45 px long and 30 px tall**.
`refX="9"` puts the reference point at the tip, and `marker-end` pins that tip to
the last vertex. So the triangle's **base** sits 45 px back from the line's end
point, whatever the line's length.

*Row F's ray is 25 px long* (x1=700 -> x2=725). 45 > 25, so the base overshoots
backwards past the open circle by 45 - 25 = 20 px, landing at x = 680 = value
**6.23**. The circle it is supposed to start from is at x = 700 = value **7.000**.

*Measured, not inferred.* I rendered the package SVG at 1x and again at 4x and read
the bitmaps. Leftmost pixel of ray-colour ink (#075985) in row F, both renders:

| row | ink spans (value) | what bounds the ink on the excluded side |
|---|---|---|
| A "open circle at 6, ray right" | +5.577 … +7.923 | its own open circle at 6 (radius 11 px = 0.423 u) |
| B "closed circle at 6, ray right" | +5.577 … +7.923 | its own circle at 6 |
| C "open circle at 6, ray left" | -8.000 … **+6.385** | its own circle at 6 |
| D "closed circle at 6, ray left" | -8.000 … **+6.385** | its own circle at 6 |
| E "open circle at 5, ray right" | +4.577 … +7.923 | its own circle at 5 |
| **F "open circle at 7, ray right"** | **+6.038** … +7.923 | **nothing — ink starts 0.962 units left of its circle** |
| G "open point only at 6" | +5.577 … +6.385 | the circle itself |

Every row in the figure has its ink bounded by its own circle. Row F alone does
not. Its inked region begins at value **+6.038**, and it begins there at the
arrowhead's **maximum** width (28 px of the 30 px triangle height in a 27 px
sampling band) — the fat base, not a taper. The circle's outer left edge is at
x = 689 = value 6.577, so **14 px (0.538 units) of solid, fully exposed triangle
lies to the left of the circle**, plus the wedge above and below the circle from
6.577 to 7.000. Total ink in the region "x > 7" requires to be blank: **0.962
units**.

*Confirmed on three independent paths*, per the standing rule:
1. Geometry from the SVG source: base at 725 - 45 = 680, value 6.231.
2. cairosvg raster at 1x: leftmost row-F ink at x = 675, value 6.038.
3. cairosvg raster at 4x: identical, value 6.0385, full arrowhead height from the
   first inked column.
The 5 px disagreement between path 1 and paths 2-3 is the renderer's marker
reference rounding; it moves the finding in the more severe direction and does not
affect it.

*Why this is a defect and not polish.* r3's test was the right test: "does the row
still depict what its label claims?" Applied honestly to row F, the answer is no.
Row F claims the set (7, ∞). It draws solid ink over [6.04, 7.92] with a white ring
punched at 7.0. On a number line, ink on the line means membership. The open circle
has stopped functioning as the boundary of the region and has become an interior
hole — a graph that reads as "shaded from about 6, with 7 removed", which is not a
set any choice in this item names.

r3's specific defence was that the segment to the left of the wedge is the thin
2 px #111 axis rather than the 5 px ray, so "a reader sees 'fat arrowhead', not
'the set starts at 6.2'". That defence concedes the ink and then argues about how
it reads. The magnified render settles the reading: **the wedge's base lands
squarely on the tick for 6**, and the open circle sits inside the wedge rather than
at its edge. I have attached nothing, but the crop is reproducible in one command
from the package file.

*And this item is the worst possible place for it.* H6 asks the student to graph
`6 < y`. The correct answer, row A, is a region shaded from 6 rightward. Row F —
the distractor for "open circle at 7" — is **also** shaded from ≈6 rightward; its
ink begins at 6.038, which is 0.19 units **further left** than where row A's own
arrowhead begins (6.23). The stem instructs "Use the graphic choices." A student
who correctly derives y > 6 and then picks graphs by where the shading starts sees
two rows shaded from 6 and can select both. Under all-or-nothing scoring that
student takes zero. That is criterion 2's harm — the defect that punishes the
strongest students — arriving through the figure instead of through the choice
text.

I record the boundary of the charge precisely, because it matters: **choice_6's
text, "Open circle at 7; ray right", is unambiguously false for `6 < y`, and it is
correctly negated.** Criterion 2 is not violated in its literal form and I am not
claiming a true-but-unkeyed choice. The charge is criterion 7: a referenced figure
that does not render what the item asserts. That is precisely the ground r2 used
to charge rows C and D, and r2 charged them while stating in terms that "scoring is
unaffected — the key is choice A, C and D are negated". Row F fails the same test
on the same criterion with the same scoring impact and 0.96 units of misplaced ink
where C and D had 1.73. A slice cannot charge the one and excuse the other.

Pre-existence is not a defence either, and r2 already established that: it recorded
the C/D construction as present in the original, said "no blame attaches to the
fix", and charged it anyway. Row F's 45px-marker-on-25px-ray condition is likewise
pre-existing — the +220 px shift preserved ray lengths — and is likewise chargeable.

**fix:** Make the marker shorter than the shortest ray. One element, one line, no
coordinate changes. In both `h6-` and `h7-number-line-options.svg` replace

```
<marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#075985"/></marker>
```

with

```
<marker id="arrow" markerWidth="18" markerHeight="14" refX="17" refY="7" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L0,14 L17,7 z" fill="#075985"/></marker>
```

`markerUnits="userSpaceOnUse"` decouples the arrow from `stroke-width`, giving a
fixed 17 x 14 px head that fits inside row F's 25 px ray with 8 px of shaft to
spare.

I applied this to scratchpad copies (**not** to the package — I edited no package
file) and re-measured both figures. Result:

```
H6 after:  A[+5.577,+7.923] B[+5.577,+7.923] C[-8.000,+6.385] D[-8.000,+6.385]
           E[+4.577,+7.923] F[+6.577,+7.923] G[+5.577,+6.385]
H7 after:  A[+1.577,+7.923] B[+1.577,+7.923] C[-8.000,+2.385] D[-8.000,+2.385]
           E[-2.423,+7.923] F[+2.577,+7.923] G[+1.577,+2.385]
```

Row F's ink boundary moves from +6.038 to **+6.577**, which is exactly its own
circle's outer edge — the same relationship every other row already has. **No other
row's ink boundary moves by a single pixel** in either file. H7 needs the change
only for construction parity (all its rays already exceed 17 px), but applying it
to both keeps the two figures identical, which is the property r2's fix was chasing.

An alternative that also works: keep the marker and lengthen row F's ray by
extending the axis and ticks to +9 (x = 752) and ending all rightward rays there.
I do not recommend it — it moves 20+ coordinates in two files to fix one row.

---

## THE FOUR REPAIRS, VERIFIED INDEPENDENTLY

**1. Answer-leak neutralisation — CLOSED, and I checked for residue, not just for
the strings named.**

I took an element census of both files rather than grepping for expected words.
Both are identical in structure: 1 svg, 1 rect, 1 title, 1 style, 1 defs, 1 marker,
1 path, 132 `<line>`, 126 `<text>`, 7 `<circle>`. The 132 lines = 7 axes + 7x17
ticks (119) + 6 rays. The 126 texts = 7 row labels + 119 tick labels. **Fully
accounted for; there is no unexplained element in either file.**

- `<title>`: "H6 / H7 number-line answer choices A through G." — neutral.
- `aria-label`: same string, still present on the root, `role="img"` retained.
  Accessibility attributes kept as required.
- Rendered `<text>`: no answer-bearing element survives. The 7 row labels are
  neutral descriptions ("A. open circle at 6, ray right") that mirror the seven
  `<response_label>` texts one-for-one; they are the only way to map a picture to a
  choice and leak nothing the choice list does not already state.
- No hidden residue: zero `opacity`, `visibility`, `display`, `fill="white"` on
  text, zero `<desc>`, zero `<metadata>`, and every `<text>` carries only `x` and
  `y`. Zero hits for `correct`, `Answer:`, `key`, `solution` in either SVG.
- The QTI `alt` text is neutral too: "Accessible number-line option graphic for H6:
  answer choices described in text and image."

Note, not a defect: because the SVG is embedded via `<img src=…>`, its internal
`aria-label`/`<title>` are not exposed to assistive technology — the `alt`
attribute governs. Keeping them is harmless, and the real accessibility path here
is the seven choice texts, which do carry the full descriptions.

**2. Label/axis collision and the +220 px shift — CLOSED.**
Labels start at x=20; the longest ("B. closed circle at 6, ray right", 31 chars at
16 px Arial) ends near x=274. Axes start at x=310. 36 px of clearance, confirmed on
both renders: every label is fully legible, including H7 row E's minus sign in
"at -2". No strike-through anywhere.

Observation, not a defect: content bbox ends at x≈742 but `width="1180"`, so 37% of
each image is blank right margin. In a ~750 px Canvas question body the figure
scales to ≈0.64 and the 16 px labels render near 10 px — small but legible. The
widening overshot what the shift required. Cosmetic; I am not charging it.

**3. `$IMS-CC-FILEBASE$` token and the webcontent resource — CLOSED.**
- H6 stem: `src="$IMS-CC-FILEBASE$/media/h6-number-line-options.svg"`; H7 the same.
  Both `<img>` tags are correctly entity-escaped inside `texttype="text/html"` and
  self-closed. Exactly one `<img>` per stem; no bare `src="media/…"` survives
  anywhere in the slice.
- Manifest: `<resource identifier="…_media" type="webcontent">` lists all three
  SVGs as `<file>` entries, and the QTI resource carries
  `<dependency identifierref="…_media"/>`. All three files exist on disk.
- This is exactly the form criterion 7 names as what Canvas expects.

**4. The leftward-ray arrowheads on rows C and D — CLOSED, on both files, verified
from the bitmaps rather than from the attributes.**
- Source: zero `style=` attributes remain in either file; zero `marker-start`; zero
  `marker-end:none`. `.ray` supplies `marker-end:url(#arrow)` and it is the only
  marker reference in either file.
- H6 rows C/D: `<line class="ray" x1="674" x2="310"/>`. Measured ink -8.000 …
  +6.385. The arrowhead is at x=310 (value -8, the axis terminus) pointing left;
  the ink stops at the circle's outer right edge (+6.385). **Zero ink to the right
  of the circle at 6.** The 1.73 units the r2 defect painted across (6, 7.73] are
  gone.
- H7 rows C/D: same construction with x1=570. Measured ink -8.000 … +2.385.
  **Zero ink to the right of the circle at 2.** Confirmed independently of H6.
- The unbounded end now carries the arrowhead on all six rays in both files, so one
  convention runs throughout — which is what made row F's outlier status visible.

**All seven rows, judged against what their labels claim:** H7 rows A-G all depict
what they say. H6 rows A, B, C, D, E, G all depict what they say. **H6 row F does
not.** That is the finding.

---

## RULING ON THE OPEN QUESTION

**Row F's arrowhead overshoot — previous ruling "cosmetic" is OVERTURNED.**

The ruling turned on the test "the row still depicts what it claims". Measured
rather than eyeballed, it does not: the boundary of row F's inked region is 6.038,
its claimed boundary is 7.000, and the 0.962 units between them are covered by the
widest part of a filled triangle. The full reasoning, the three-path measurement,
the harm channel on this specific item, and a tested one-line fix are in the DEFECT
section above.

Two corrections to r3's account of it, both minor and both pointing the same way:
r3 put the wedge base at value 6.23 (the source geometry); rendered, it is 6.038.
And r3's "reads as a fat arrowhead, not as the set starting at 6.2" does not
survive magnification — the base lands on the 6 tick and the circle sits inside the
wedge, not at its edge.

---

## CANDIDATES AND PRIOR RULINGS, RE-RULED COLD

- **F4 stale companion** -> **CONFIRMED CORRECT AS SHIPPED, no defect.** The
  updated worksheet F4 reads "Undo x5, use inverse op:" (read rendered at 300 dpi).
  The QTI stem reads "To undo x5, use the inverse operation ____." with key
  "divide by 5". They match. The companion still poses "To undo /5" with checked
  answer "multiply by 5 (or x5)" and is stale, exactly as briefed. Had the fixer
  followed the companion it would have keyed choice_2 "multiply by 5" and inverted
  the item; it did not. This is an upstream companion ticket, not a package defect.
- **F4 choice_6 "multiply by 1/5 then add 5"** -> **REFUTED as a true-but-unkeyed
  choice.** Multiplying by 1/5 *is* dividing by 5, so the first half alone would
  have been true and would have been a criterion-2 defect. The trailing "then add
  5" makes the composite v/5 + 5, which equals v/5 only when 5 = 0. False, and
  correctly negated. The near-miss is deliberate and correctly built.
- **H5 `y > -6` and `-6 < y`** -> **REFUTED as true-but-unkeyed.** Both mean
  y > -6, which `6 < y` implies but is not equivalent to: y = 0 satisfies y > -6
  and fails 6 < y. Correctly negated. Noted and dismissed: these two choices are
  equivalent to *each other*, which is unusual design, but their visible text
  differs (so criterion 6's duplicate-text rule is not engaged) and both are false
  and both are negated. No defect.
- **H4 choice_6 "6 < x"** -> **REFUTED.** 6 < x is x > 6, the negation of the key
  x < 6. The genuinely equivalent form "6 > x" is *not* offered. Correctly built.
  Same structure in H3: "5 > x" is offered (false); the equivalent "5 < x" is not.
- **E3's `$`** -> **REFUTED.** A single unpaired currency `$` in "cost $20",
  matching the worksheet. Canvas does not treat `$…$` as a math delimiter by
  default and there is no second `$` to pair with. No item in the slice contains
  `\(`, `\)`, or any other math delimiter; the stems are plain text with Unicode
  `x`, `>=`, `<=` and correctly escaped `&gt;`/`&lt;`.
- **"Point only at 6" vs figure label "open point only at 6"** -> **REFUTED as a
  defect, noted as drift.** Both describe the same drawn object (a lone open circle
  at 6, no ray) and it is false under either reading, so no scoring path is
  affected. Same in H7.
- **SVG axis window -8..8 vs the worksheet's 4..8 (H6) and 0..5 (H7)** -> **not a
  defect.** The SVG presents answer *options* to compare, not a reproduction of the
  worksheet's blank line; ticks are labelled throughout and every referenced value
  (including H7's -2 distractor) is on-scale. Answerability is unaffected: a student
  solves x > 2 and picks row A.
- **Axis line ends at x=725 while the "8" tick is at x=726** -> 1 px; not a defect.

---

## VERIFICATION OF EVERYTHING NOT PART OF THE REPAIR

Worked from the source before opening any prior report, so this is a genuine second
pass on the mathematics rather than a re-read of r1's.

**Scoring trees parsed properly, not regexed.** I walked each `<respcondition>` as
a tree with `<not>` inverting the sense, per the recorded trap. Result for all 18
items: exactly one `<respcondition>`, `continue="No"`,
`<setvar action="Set" varname="SCORE">100</setvar>`, `respident="response"`
throughout. On all 11 multiple-answers items the split is `choice_1` required and
`choice_2..choice_7` negated, every choice ident covered, none left unconstrained.
No duplicate visible choice text on any item. The seven fill-ins carry a single
`answer1` label and the `<or>`/`<vargte>`/`<varlte>` equivalent-value wrapper, which
is a numeric tolerance idiom, not a second key.

**Stems, checked against the rendered updated worksheet** (`pdftotext -layout`
transposes the built-up fractions in E2, E4 and H2 — I did not use it for any
value). All 18 match their same-labelled worksheet item, wording and numbers.

**Keys, worked independently and then cross-checked against the companion's
"Checked answer" lines:**

| item | worked | key in XML | companion |
|---|---|---|---|
| E1 | 5/8 = 0.625 > 0.610 | `5/8` | 5/8 |
| E2 | 21/7 = 3, 4x3 | `12` | 12 |
| E3 | 20/4 = 5/snack, 7x5 | `35` | 35 dollars |
| E4 | 18/6 = 3, 5x3 | `15` | x = 15 |
| F1 | 7 multiplies m | `coefficient` | coefficient |
| F2 | n is the unknown | `variable` | variable |
| F3 | inverse of +8 | `subtract 8` | subtract 8 (or -8) |
| F4 | inverse of x5 | `divide by 5` | *(stale — see above)* |
| F5 | (6-2)y | `4y` | 4y |
| F6 | 5(4) - 3 = 20 - 3 | `17` | 17 |
| G1 | 3y + 3(6) | `3y + 18` | 3y + 18 |
| H1 | 18 - 7 | `11` | x = 11 |
| H2 | 6 x 4 | `24` | x = 24 |
| H3 | x > 8 - 3 | `x > 5` | x > 5 |
| H4 | x < 2 + 4 | `x < 6` | x < 6 |
| H5 | 6 < y is y > 6 | `y > 6` | y > 6 |
| H6 | y > 6 | open circle 6, ray right | open circle at 6, shade right |
| H7 | x > 2 | open circle 2, ray right | open circle at 2, shade right |

No key is written with an "or" that the item requires both halves of. The three
items where the companion writes `x = 11` / `x = 24` / `x = 15` are numerical
fill-ins whose stems say "Enter the value only, without x =." — the bare-value /
`n = value` mismatch trap is explicitly headed off in the stem text. Same for E3,
whose companion answer is "35 dollars" against a stem that says "Enter the number
only, no units or symbols."

**Every non-keyed choice worked for truth (criterion 2, the primary hunt).** All 66
distractors across the 11 multiple-answers items are false. The ones worth naming
because they are near-misses and all resolve correctly: F1 choice_3 "constant term"
(7m's only term carries a variable, so 7 is not a constant *term*); F1 choice_6
"product only" (7 is a factor of the product, not the product); F2 choice_3
"constant" (n is the unknown); F4 choice_6 (worked above); F5 choice_3 "4"
(4y != 4 as an expression); G1 choice_5 "3(y) + 6" = 3y + 6 != 3y + 18; H3 choice_6
"5 > x"; H4 choice_6 "6 < x"; H5 choices 6 and 7 (worked above); H6/H7 choice_2
(closed circle = the non-strict inequality) and choice_7 (point only = equality).
**No true-but-unkeyed choice anywhere in the slice.** No keyed choice is false.

**Nothing outside the repair moved.** r1 recorded all six of its defects on the
H6/H7 figures, the two image `src` attributes and the manifest; it recorded E1-H5
as clean on the mathematics. I did not rely on that record — I reworked all 18
items from the worksheet and the companion, and the stems, choice sets and
required/negated splits I read today are consistent with what r1 and r3 describe.
The QTI XML (00:03) predates both SVG writes (00:11) and has not been touched
since. `a1-number-line-options.svg` (00:02) is untouched and contains no `class="ray"`
element, so the marker fix I propose cannot affect it; I did not score A1, which is
outside this slice.

---

## CLEAN — 17 of 18

E1, E2, E3, E4, F1, F2, F3, F4, F5, F6, G1, H1, H2, H3, H4, H5, H7 — stem, key,
every distractor, scoring tree, structure and markup all verified with no defect.
H7's figure is clean on all seven rows and needs no change on its own account.

**H6 — the item's mathematics, stem, key, all seven choice texts and its scoring
tree are clean. The defect is confined to row F of its figure.**

---

Score **9/10**. One defect stands, on criterion 7. It does not change any key, and
a student who reads the choice labels rather than the pictures is scored correctly
today — but the stem tells them to use the pictures, and one picture does not show
what it says. The slice goes back around for a one-element change to the marker
definition; re-render both figures and re-measure row F's left ink boundary against
+6.577 to confirm.
