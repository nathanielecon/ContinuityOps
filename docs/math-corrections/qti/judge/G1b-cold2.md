# G1b — second cold validation judge report

SLICE: G1b (6th Grade Review Section 1, items E1-E4, F1-F6, G1, H1-H7)   SCORE: 10/10
ITEMS WORKED: 18 of 18   (E1 E2 E3 E4 F1 F2 F3 F4 F5 F6 G1 H1 H2 H3 H4 H5 H6 H7)

SHAPE: B. Idents are `choice_1..choice_7` / `answer1`, `respident="response"`,
fewer than 8 choices on every item (this corpus's design, not scored as a defect).
No item in this slice carries a second `<respcondition>`, so that allowance never
arises here.

**No defect stands. The slice is clean on all seven criteria.**

## ORDER OF WORK — stated explicitly, because the brief requires it

I worked in this order and did not deviate:

1. Read `JUDGE_RUBRIC_QTI.md` and `COLD_BRIEF.md`.
2. Confirmed the extracted package at `/tmp/qtiwork/pkg/6th-grade-review-section-1-accuracy-check-qti/`
   is byte-identical to `docs/math-corrections/qti/zips/6th-grade-review-section-1-accuracy-check-qti.zip`
   (all six files, sha256 each), that the zip matches its entry in `sha256sums.txt`,
   and that the zip is unmodified against git HEAD.
3. Extracted the 18 items from the raw QTI XML myself. I never read
   `/tmp/qtiwork/slices/*.json` or any other cache at any point.
4. Worked all 18 items' mathematics from the XML and from `6thGradeReviewUpdated.pdf`
   **rendered at 200 dpi**, corroborated against `6thGradeReviewExplanations.pdf`.
5. Measured both SVG figures — geometry parsed from source, then rendered to raster
   and measured with exact-RGB matching plus a negative control.
6. Wrote my findings.
7. **Only then** opened `G1b-r1.md`, `G1b-r2.md`, `G1b-r3.md`, `G1b-r4.md` and
   `G1b-cold.md` to compare. Nothing in section "FINDINGS" below was formed after
   opening them; the comparison is quarantined in its own section at the end.

---

## METHOD

**Package integrity.** `find | sha256sum` over the extracted tree and over a fresh
unzip of the shipped zip: six files, six identical digests. `sha256sum -c
sha256sums.txt` -> OK for this package. `git diff HEAD` on the zip -> empty. So the
artifact I measured is the artifact that ships.

**Scoring tree.** Parsed with `xml.etree`, walking `<conditionvar>` recursively and
carrying a `negated` flag that flips at every `<not>`, so a `<varequal>` inside a
`<not>` can never be counted as required. `<vargte>`/`<varlte>` collected
separately. No regex was used to decide requiredness.

**Stems.** `pdftotext -layout` on `6thGradeReviewUpdated.pdf` transposes the
built-up fractions exactly as the rubric warns (E2 extracts as `47 = 21 / ?`), so
every fraction-bearing stem was settled on a 200 dpi **render** of page 1, read as
an image: E1, E2, E4, H2 all confirmed visually.

**Figure measurement — instrument and its validation.** Rendered both SVGs with
cairosvg at scale 4 (4720x2240) and matched **exactly** on the flat fill
`#075985` = RGB(7,89,133). No tolerance was used anywhere; the rubric's standing
warning about antialiased grey ticks producing false boundaries is why.

Calibration is taken from the figures' own tick coordinates, not from a fit to the
raster: the 17 tick `<line>` elements per row run x=310..726 at a spacing of
exactly 26.000 with zero variance, and the `0` tick is at x=518, so
**value = (x - 518) / 26**. Both files use the identical axis.

For the arrowhead test I did not use peak thickness (the dot ring reaches the same
peak and would report "present" everywhere). I used the **taper slope over the
marker's own 17 user units walking inward from each terminus**, and I built the
**negative control**: a scratchpad copy of each file with `marker-end:url(#arrow)`
replaced by `marker-end:none`, rendered and measured identically. The control
flips exactly the 12 ray termini and nothing else — see the table below. A detector
that cannot be shown to fail is not a measurement.

---

## FINDINGS

### DEFECTS

None. All seven criteria hold on all 18 items.

### Criterion 1 — stem fidelity (worksheet render, 200 dpi)

| item | `6thGradeReviewUpdated.pdf` | QTI stem | verdict |
|---|---|---|---|
| E1 | Greater: 5/8 or 0.61? | Greater: 5/8 or 0.61? | match (fraction read from render) |
| E2 | 4/7 = ?/21, ? = | 4/7 = ?/21 | match (extraction transposes; render does not) |
| E3 | 4 snacks cost $20. 7 snacks cost __ dollars. | same | match |
| E4 | 5/6 = x/18, x = | 5/6 = x/18 | match (render) |
| F1 | In 7m, 7 is the __ | In 7m, the number 7 is the __ | match (companion wording) |
| F2 | In n + 8 = 12, n is the __ | same | match |
| F3 | Undo +8, use inverse op: | To undo +8, use the inverse operation __ | match |
| F4 | **Undo x5**, use inverse op: | **To undo x5**, use the inverse operation __ | match — see ruling below |
| F5 | Combine like terms: 6y - 2y = | same | match |
| F6 | If n = 4, then 5n - 3 = | same | match |
| G1 | Expand: 3(y + 6) = | 3(y + 6) = ... select all equivalent simplified expressions | match |
| H1 | x + 7 = 18, x = | x + 7 = 18 | match |
| H2 | x/4 = 6, x = | x/4 = 6 | match (render) |
| H3 | Solve: x + 3 > 8 | x + 3 > 8 ... equivalent inequalities | match |
| H4 | Solve: x - 4 < 2 | same shape | match |
| H5 | Write an equivalent way to express 6 < y: | same | match |
| H6 | Graph 6 < y on a number line: | same + graphic | match |
| H7 | Graph x > 2 on a number line: | same + graphic | match |

### Criteria 3 and 4 — keys worked, and key agreement

Every key recomputed from the stem, then checked against the companion's
"Checked answer" line (E1's checked answer is a built-up fraction and was read from
a 150 dpi render of companion page 15: it is 5/8).

E1 `5/8` (5/8 = 0.625 > 0.61, and 5/8 is already simplified) · E2 `12`
(21/7 = 3, 4x3) · E3 `35` (20/4 = 5 per snack, 7x5) · E4 `15` (18/6 = 3, 5x3) ·
F1 coefficient · F2 variable · F3 subtract 8 · F4 divide by 5 · F5 `4y`
((6-2)y) · F6 `17` (5x4 - 3) · G1 `3y + 18` · H1 `11` · H2 `24` · H3 `x > 5` ·
H4 `x < 6` · H5 `y > 6` · H6 choice_1 · H7 choice_1. All agree with the companion.

No key requires two "or" forms simultaneously. F3's companion key writes
"subtract 8 (or -8)", but the item offers only "subtract 8" as a choice and no
"-8" choice exists, so no student can be forced to supply both. Not a
criterion-4 problem.

### Criterion 2 — every non-keyed choice worked (the primary hunt)

All 77 distractors across the 11 multiple-answers items were worked individually.
The ones worth naming:

- **F1 `choice_3` "constant term"** — 7m is a single term *containing* a variable,
  so it has no constant term; 7 is a constant *factor*, which the option does not
  say. False. (Had the option read bare "constant" this would be arguable; it does
  not.)
- **F1 `choice_6` "product only"** — 7m is a product, but 7 is a factor of it, not
  the product. False. Weaker-case wording, ruled false.
- **F2 `choice_4` "answer only"** — the *value* of n is the answer; n itself is the
  variable. This is the rubric's weaker case (a true-ish statement about a
  different question). Recorded as such and ruled **false**: as a name for n's
  role in `n + 8 = 12` it is wrong.
- **F3 `choice_6` "add 0"** — identity, does not undo +8. False.
- **F4 `choice_6` "multiply by 1/5 then add 5"** — the near miss. `x -> 5x -> x ->
  x + 5`. The multiply-by-1/5 alone would be equivalent; the trailing "add 5"
  breaks the round trip. False.
- **F5 `choice_3` "4"** — `4 != 4y`. False.
- **G1 `choice_5` "3(y) + 6"** — reads 3y + 6, not 3y + 18. False. (The stem's own
  form `3(y + 6)` is not among the choices, so there is no trivially-true unkeyed
  option.)
- **H3 `choice_6` "5 > x"** = x < 5. **H4 `choice_6` "6 < x"** = x > 6. Both authors'
  reversals keep the option **false**; neither is the equivalent-but-flipped form
  (`5 < x`, `6 > x`) that would have been a criterion-2 defect. I checked this
  character by character in the raw entities (`&gt;` / `&lt;`).
- **H3 `choice_3` "x >= 5"** admits x = 5, and 5 + 3 > 8 is 8 > 8, false. Correctly
  unkeyed. **H4 `choice_3` "x <= 6"** admits x = 6, and 6 - 4 < 2 is 2 < 2, false.
- **H5 `choice_6` "y > -6"** and **`choice_7` "-6 < y"** — the same statement written
  two ways, and both are *implied by* 6 < y without being *equivalent* to it
  (y = 0 satisfies y > -6 and fails 6 < y). The stem asks for equivalent
  inequalities, so both are correctly negated. Their visible text differs, so this
  is not criterion 6's duplicate-text fault; both sit on the same side of the
  required/negated split, so the split stays coherent.
- **H6/H7** distractors are y >= 6, y < 6, y <= 6, y > 5, y > 7 and a lone point
  (H6); x >= 2, x < 2, x <= 2, x > -2, x > 3 and a lone point (H7). None equals the
  keyed set.

No true-but-unkeyed choice exists anywhere in the slice.

### Criterion 5 — answerability from the assignment

Each fill-in stem states its required form: "Enter a simplified a/b, no spaces or
mixed numbers" (E1), "the number only, no units or symbols" (E2, E3, F6), "the
value only, without x =" (E4, H1, H2). The worksheet's own blanks accept exactly
those. H6/H7 convert a draw-it task into a choose-from-seven task; the keyed row
is the one the worksheet's answer describes, and the seven options are each
restated in words in the choice text, so a student holding only the assignment can
map their drawing onto a choice.

### Criterion 6 — structure

Measured across all 18: exactly **one** `<respcondition>` each, `continue="No"`,
`<setvar action="Set" varname="SCORE">100</setvar>`, and `maxvalue="100"` on
`<decvar>` in `<resprocessing><outcomes>` (which is where the rubric says it
belongs). On all 11 multiple-answers items the tree is `choice_1` required and
`choice_2..choice_7` each negated — union equals the declared choice set exactly,
no choice missing from the tree and no ident in the tree without a choice. Zero
duplicate visible choice texts in any item. `respident` is `response` everywhere
and matches the `<response_lid>` / `<response_str>` ident. Package-wide the 36
items have 36 distinct idents and 36 distinct titles; `points_possible` is 36 for
36 one-point items.

### Criterion 7 — markup, import validity, and the figures

**Text markup.** No `\(`, no `\[`, no LaTeX delimiters at all in this slice — the
math is plain text throughout, so there is no interleaving to get wrong. The only
`$` characters are the currency `$20` in E3 (unpaired, matching the worksheet, in
an item with no math delimiters) and the two paired `$IMS-CC-FILEBASE$` tokens in
H6/H7. No stem carries a duplicated instruction block. Non-ASCII is confined to
`x` (U+00D7) in F4 and the relation glyphs U+2264/U+2265 in H3/H4/H5 `choice_3` —
all intentional. CJK scan: detector self-tested against a known CJK string
(returns True), then run over the QTI XML and both SVGs — clean.

**Image resolution.** Both stems use `src="$IMS-CC-FILEBASE$/media/h6-..."` /
`h7-...`. The manifest declares a separate `type="webcontent"` resource carrying
all three media `<file>` entries, and the QTI resource `<dependency>`s on it. All
referenced files exist. Import-clean.

**Figures — measured.** Geometry parsed from source and then confirmed on the
raster. Circle centres land on exact ticks in every row: h6 rows A-D and G at
x=674 (value 6.000), E at 648 (5.000), F at 700 (7.000); h7 rows A-D and G at 570
(2.000), E at 466 (-2.000), F at 596 (3.000). Row G in both files has no `class="ray"`
element at all.

Exact-RGB ink extents, in **values** (my calibration, value = (x-518)/26):

| row | H6 ink | H7 ink | reading |
|---|---|---|---|
| A | +5.587 .. +7.952 | +1.587 .. +7.952 | open circle, ray right |
| B | +5.587 .. +7.952 | +1.587 .. +7.952 | closed circle, ray right |
| C | -8.000 .. +6.404 | -8.000 .. +2.404 | open circle, ray left |
| D | -8.000 .. +6.404 | -8.000 .. +2.404 | closed circle, ray left |
| E | +4.587 .. +7.952 | -2.413 .. +7.952 | open circle at 5 / -2, ray right |
| F | **+6.587** .. +7.952 | +2.587 .. +7.952 | open circle at 7 / 3, ray right |
| G | +5.587 .. +6.404 | +1.587 .. +2.404 | circle only, no ray |

Every row's ink on its excluded side extends **exactly 0.423 units** past the
circle centre and no further — that is the open/closed circle's own outer ring
(r=9 plus half of stroke-width 4 = 11 px = 0.423 u), which is ordinary
number-line drafting and is identical in the keyed row A. **No row has filled ink
on the excluded side beyond its own circle.** In particular H6 row F's left ink
edge measures +6.587 against a nominal ring edge of +6.577 (a quarter of a device
pixel at scale 4), i.e. the ink begins at the circle and nothing sits left of it.

**Arrowheads — present, single, and correctly oriented, with a negative control.**
Taper slope over 17 user units inward from each terminus, actual vs. the
`marker-end:none` control:

| terminus | actual slope / peak | control slope / peak | verdict |
|---|---|---|---|
| A,B,E,F right end (both files, 8 termini) | +0.52 / 11.5 | -0.00 / 5.0 | head present, points right |
| C,D left end (both files, 4 termini) | +0.52 / 11.5 | -0.00 / 5.0 | head present, points left |
| every circle end (14 termini) | -0.44 / 15.5 (open) or +0.73 / 21.5 (closed) | **identical** | no marker ink at the circle |
| G, both ends (4 termini) | unchanged by control | unchanged | no ray, correctly |

The control flips exactly the 12 ray far-ends and nothing else. Because the circle
termini are byte-for-byte identical between actual and control, there is **no
marker-start residue anywhere in either file** — this is a measurement, not a
source reading. The source agrees independently: `grep` for `marker-start` returns
zero in both files, and both files contain **zero** `style="..."` attributes (the
only styling is the one `<style>` element).

I also rendered both figures whole and read them as images: every row reads as its
own label.

---

## RULINGS ON THINGS I LOOKED HARD AT AND DID NOT CHARGE

**H6 row F is geometrically the tightest row in the slice, and I ruled it clean.**
The open circle at 7 has outer ring edge x=711; the arrowhead occupies x=708..725
(17 user units, `markerUnits="userSpaceOnUse"`, refX=17 pinned to the line end).
So the bare shaft between ring and arrow base is **-3 px** — there is none, and the
arrowhead's base sits 3 px inside the ring. The visible triangle beyond the ring is
x=711..725 = 14 px = **0.538 units**. For comparison the bare shaft is 23 px in H6
row A, 49 px in H6 row E and 101 px in H7 row F. This is inherent to placing an
option at 7 on an axis that stops at 8. I charge nothing, for three reasons that
are all measurements or facts, not taste: (a) the ink still begins at the circle
and never crosses to the excluded side, which is the test that mattered for rows
C, D and F historically; (b) the head is 14 units tall against a 5-unit shaft and
renders as an unmistakable right-pointing triangle — I confirmed this on the
raster, and my arrowhead detector reports it with the same +0.52 slope as every
other row; (c) the row is a distractor that is labelled in the figure and restated
in `choice_6`. A student cannot be mis-scored by it. If a future pass wants more
air, the honest fix is widening the axis to 9 or 10, not touching the marker.

**F4 — companion contradicts the worksheet; the QTI follows the worksheet and is
right.** `6thGradeReviewExplanations.pdf` F4 poses "To undo /5" with checked answer
"multiply by 5". `6thGradeReview.pdf` (the pre-update revision) poses the same. The
**updated** worksheet, which the brief names as the source of record, poses "Undo
x5", for which "divide by 5" is correct — and the QTI keys "divide by 5". I
verified the direction of the change by diffing the two worksheet revisions
myself, and `docs/math-corrections/pdf/CorrectionsReport.pdf` records it
explicitly: "F4 - superseded by the updated worksheet ... Corrected to: Undo x5,
use inverse op: -> divide by 5". Not a package defect. Stale companion, upstream,
already ticketed.

**H6/H7 `choice_7` "Point only at 6" / "Point only at 2" vs the figure's row G
label "open point only at 6" / "at 2".** Wording drift. Both descriptions name the
same drawn object, both are false for a strict inequality, and both are negated.
No scoring channel. Not charged.

**E3's single `$`.** Currency, unpaired, in an item with no math delimiters, and it
matches the worksheet. Not the stray-delimiter fault.

**`original_answer_ids` says `choice_1` on the fill-in items whose response label
is `answer1`.** Uniform across all 36 items of the package regardless of type
(22 numerical, 12 multiple-answers, 2 short-answer). Canvas metadata, not scoring.
Not charged.

**Neither figure carries a `viewBox`** (nor does `a1-...svg`), and content occupies
x=20..730 of a 1180-wide canvas — 38% of the width is blank, so the figure will
display at roughly 62% of the scale it could. Both are uniform across all three
figures in the package, are unrelated to any repair, and neither changes which row
a student picks. Cosmetic; recorded, not charged.

**Axis `<line>` ends at x=725 while the "8" tick is at x=726.** One pixel. Not a
defect.

---

## COMPARISON WITH THE PRIOR REPORTS — read only after the above was written

I opened `G1b-r1.md` through `G1b-r4.md` and `G1b-cold.md` only after forming every
finding above.

- **All six r1 defects are closed in the shipped artifact, verified by my own
  measurements before I knew what they were**: `$IMS-CC-FILEBASE$` tokens present
  and the manifest carries a `webcontent` resource with a dependency; zero "Correct:"
  strings in either SVG, `<title>` and `aria-label` both neutral ("H6/H7 number-line
  answer choices A through G."); labels at x=20 with axes starting at x=310, so
  nothing overprints — I read both figures as images and every label is clear of
  every axis and ray.
- **r2's rows C and D marker-start defect is closed.** My negative control proves
  it from the raster, not from the source: the circle termini of rows C and D are
  identical between the real file and a marker-suppressed control, so no marker ink
  exists there.
- **The cold judge's row F overturn and r4's fix.** I reached the current state
  independently and measure H6 row F's left ink edge at +6.587 against a ring edge
  of +6.577 — no wedge, nothing to charge. On the historical numbers I note only
  that r4's caution is the right one: my own exact-RGB pass reproduces r4's
  boundaries to within a quarter of a device pixel, and a tolerance-based test
  would not have. I did not re-litigate the history and I do not need to; the
  question in front of me was the current state.
- **The one place I could have disagreed and did not**: r3 ruled row F cosmetic,
  the cold judge overturned it, r4 fixed it. Post-fix, row F still has zero bare
  shaft (my measurement, -3 px). I considered charging that and ruled against it
  above, on the ground that the defect actually charged — filled ink on the
  excluded side — is now measurably absent, and shaft length was never the test.
  That is a ruling I would defend, not a smoothing-over.
- **The `a1-...svg` old marker note in r4 section 4** I confirm independently: a1
  retains `markerUnits="strokeWidth"` and has zero `class="ray"` elements, so the
  marker is never instantiated. Inert. Not my item.

Nothing in the prior reports changed a single finding of mine, in either direction.

---

## CLEAN — ALL 18

E1, E2, E3, E4, F1, F2, F3, F4, F5, F6, G1, H1, H2, H3, H4, H5, H6, H7.

Every stem matched against the updated worksheet read as a render; every key
recomputed and cross-checked against the companion; every one of the 77 distractors
worked and confirmed false; every scoring tree parsed with `<not>` handled
correctly; both figures measured with exact-RGB matching and a validated
arrowhead detector with a negative control.

**SCORE: 10/10.** I found nothing wrong, and I am saying so plainly rather than
manufacturing a note to look thorough.
