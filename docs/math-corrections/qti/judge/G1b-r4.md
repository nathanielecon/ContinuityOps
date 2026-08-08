# G1b — round 4 judge report (re-score after marker-units fix)

SLICE: G1b (6th Grade Review Section 1, items E1-H7)          SCORE: 10/10
ITEMS WORKED: 18 of 18
HISTORY: r1 6/10 -> r2 9/10 -> r3 10/10 (row F ruled cosmetic) -> **cold judge
overturned row F, 9/10** -> r4 10/10 (row F fixed and verified by measurement).

## 1. THE OVERTURN: I ACCEPT IT. MY r3 RULING ON ROW F WAS WRONG.

The consistency argument is decisive and I should have applied it to myself. In r2
I charged rows C and D under criterion 7 for putting filled ink on the side the
graph must leave blank, and I charged them *while stating* that scoring was
unaffected and the construction was pre-existing — so neither of those facts can
be a reason to excuse row F, which fails the same test on the same criterion. I
drew the line at "does the row still read as its label" and then applied it by
inspection rather than by measurement, which is exactly the move the standing rule
warns against. A slice cannot charge 1.73 units of misplaced ink in one row and
excuse 0.75 units in another. The cold judge was right to overturn it.

What I got right in r3 was the *mechanism* — I identified the 45px marker on a
25px ray and computed the wedge base from the source geometry. What I got wrong
was the ruling I built on top of it.

## 2. TWO NUMBERS IN THE OVERTURN THAT MY MEASUREMENT DOES NOT SUPPORT

Recording these because the record should be accurate, not because they change the
verdict. They do not: the defect is real, correctly charged, and now fixed.

**(a) The pre-fix boundary was +6.250, not +6.038.** Measured on my own r3-era
render, exact-RGB match on `#075985`, tick-calibrated: row F ink ran x 680..724 =
**+6.250 .. +7.942**. So the misplaced ink was **0.750 units**, not 0.962. My r3
source-geometry figure of 6.23 was right to within half a pixel (predicted 6.231,
measured 6.250) — the overturn's claim that source geometry misplaced it and only
rendering revealed 6.038 is the opposite of what I measure.

**Probable cause of 6.038, and I reproduced the failure mode.** The tick mark for
6 sits at x=674 (value exactly 6.000); antialiased, it spreads over columns
673-675, and x=675 maps to **+6.038**. A colour test with tolerance picks that
grey tick up as ink. The overturn's own phrasing — "the base lands on the tick for
6" — is the tell: the base does not land on that tick, the tick is simply the
leftmost non-white pixel a loose colour test finds. I ran the experiment: my
tolerance-40 variant reported row ink beginning at x=21, i.e. it swallowed the
option label text. On this figure a tolerance-based colour test is not a usable
instrument; exact match is, because every fill here is flat.

**(b) The harm-channel comparison is backwards as stated.** The claim was that row
F's ink began "further left than the correct answer's". Measured pre-fix:

| row | leftmost ink | ray/arrow ink only |
|---|---|---|
| A (the key, circle at 6) | x=664 = **+5.635** | x=674 = +6.000 |
| F (circle at 7) | x=680 = **+6.250** | x=680 = +6.250 |

Row A's ink began *further left* than row F's, by either measure — 0.615 units
further including the open-circle ring, 0.250 units excluding it. Row A's ring
necessarily extends about 0.42 units either side of 6, which is ordinary
number-line drafting, not a fault. The underlying concern is still sound: row F
showed filled ink starting 0.75 units left of the 7 it claims, and that is why the
defect stands. The specific "shaded from 6 like the correct answer" comparison
is not supported by the pixels.

## 3. VERIFICATION OF THE APPLIED FIX — MEASURED, NOT INSPECTED

**Calibration.** Derived from the tick marks of row G (the only row with no ray in
either figure), with indices recovered from uniform spacing so the fit never
assumes the SVG's own coordinates: step **26.000 px/unit**, fit residual
**0.0000 units**, mapping value = 0.038462x - 19.9038. The render is 1:1 with SVG
user units, so no device-pixel-ratio correction is needed.

**Row F boundary, H6.** +6.250 -> **+6.635**, a shift of +0.385 units. The new
left edge is the open circle's own outer ring (cx=700, r=9, stroke 4 -> outer edge
x=689; measured 690), i.e. the ink now begins at the circle and nothing filled
sits left of it. You measured +6.615; I measure +6.635. That is half a pixel, and
it is the uniform sampling difference you flagged, not a disagreement.

**No other row moved.** Per-row left and right boundary deltas, both figures, all
seven rows each: **exactly +0.000** everywhere except H6 row F's left edge.
H7 never had the fault to begin with — its shortest ray is row F at 129px, far
longer than the old 45px marker — and all seven H7 boundaries are unchanged.

**No coordinate changed, proven at the byte level.** I still held my r3-state copy
of h6. Diffing it against the current package file, the *entire* difference is two
lines:

```
< <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
< <path d="M0,0 L0,6 L9,3 z" fill="#075985"/>
> <marker id="arrow" markerWidth="18" markerHeight="14" refX="17" refY="7" orient="auto" markerUnits="userSpaceOnUse">
> <path d="M0,0 L0,14 L17,7 z" fill="#075985"/>
```

Every `<line>` and `<circle>` element is identical as an ordered list, and the
element census is unchanged in both files (line 132, text 126, circle 7, marker 1,
path 1).

**Every arrowhead is still present and correctly oriented.** You were right that a
vanished marker would also "fix" the measurement, so I built the negative control:
a scratchpad copy with `marker-end` suppressed on every ray. Result — all 12 ray
rows across both figures report **ARROWHEAD PRESENT** (taper slope +4.0 to +9.2 px
walking inward from the tip), and all 12 control rows report **NO HEAD** (slope
+0.0 to +0.8). Orientation confirmed by where the taper sits: rows C and D at the
left terminus (x approx 310), rows A, B, E, F at the right (x approx 725), row G
correctly has no ray in either figure.

**Two instrument failures, disclosed.** My first arrowhead test used max thickness
per row; the control proved it blind, because the dot ring alone reaches the same
peak — it reported "present" for every control row. My second gave a false
positive on H6 control row F, again from the ring. Only the third — taper slope
over the marker's own 17px, with the ring's columns excluded — discriminated all
24 row-checks correctly. I am reporting the two failures rather than only the
working instrument, because an unvalidated detector reporting a clean result is
the exact failure this loop exists to catch. No conclusion above rests on the
first two.

**Six earlier defects still closed.** `Correct:` returns zero hits in both SVGs
and in the QTI XML; `<title>` and `aria-label` are the neutral "H6 / H7
number-line answer choices A through G."; labels sit at x=20 with axes from x=310,
so nothing overprints; all three `src` attributes carry `$IMS-CC-FILEBASE$/media/`;
the manifest's `type="webcontent"` resource and its dependency are intact; all
five XML/SVG files parse well-formed.

**All 18 items unchanged.** One `<respcondition>` each, 7 choices (1 for
fill-ins), keys byte-identical across all four rounds: E1 `5/8`, E2 `12`, E3 `35`,
E4 `15`, F6 `17`, H1 `11`, H2 `24`, and `choice_1` required with `choice_2..7`
negated on the eleven multiple-answers items.

## 4. OBSERVATION FOR THE G1a FIXER — NOT A DEFECT IN THIS SLICE

`a1-number-line-options.svg` still carries the **old** marker definition
(`markerUnits="strokeWidth"`, `markerWidth="10" markerHeight="10" refX="9"`, 9x6
path). It is inert today: a1 has no `class="ray"` element at all (126 `<line>`
elements against 132 in h6/h7 — exactly the six rays' difference), so the marker
is never instantiated and no a1 row can show misplaced ink. Not a defect, and A1
is not my item. But it is a live trap: any future edit that gives a1 a ray would
inherit the same stroke-width inflation that produced this defect. One line to the
G1a fixer if the file is ever reopened.

## 5. CLEAN — ALL 18

Mathematics re-confirmed against the current XML; no stem, key or choice has been
touched in any round. E1 (5/8 = 0.625 > 0.61), E2 (12), E3 (35), E4 (15),
F1 (coefficient), F2 (variable), F3 (subtract 8), F4 (divide by 5, matching the
updated worksheet's "Undo x5"), F5 (4y), F6 (17), G1 (3y + 18), H1 (11), H2 (24),
H3 (x > 5), H4 (x < 6), H5 (y > 6, with `y > -6` and `-6 < y` correctly unkeyed as
one-way implications), H6 (open circle at 6, ray right), H7 (open circle at 2, ray
right). No true-but-unkeyed choice; no false-but-keyed choice; every key agrees
with the explanations companion and the updated worksheet.

Score 10/10: every item worked, every figure row measured against a calibrated
scale, and no defect stands.
