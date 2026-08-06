SLICE: G1a          SCORE: 10/10
ITEMS WORKED: 18 of 18     (A1, B1-B6, C1-C7, D1-D4 — none skipped)

Round 2, after the fixer applied all three round-1 defects. All three are gone, and
nothing else in the slice moved. Shape B throughout; choice counts under 8 and the
second respconditions on D3/D4 remain correctly unscored as defects.

ROUND-1 DEFECTS — RE-VERIFIED

  1. Answer leak in media/a1-number-line-options.svg -> FIXED
     The `<text x="20" y="30">…Correct: choice A…</text>` element is gone. `<title>`
     and `aria-label` both now read "A1 number-line answer choices A through G.", and
     the stem's `alt` now reads "…answer choices described in text and image", no
     longer "correct choice described in…". The string "Correct" does not occur in
     the QTI XML or in any of the three SVGs.
     Measured, not assumed: I rendered the SVG and counted ink pixels above y=55,
     the band that used to carry the leak line. Zero. The image now opens on row A.

  2. Label/axis collision -> FIXED
     Geometry moved +60px; labels held at x=20; width 960 -> 1020; axis x2 505 -> 565.
     Measured per row off the bitmap, taking the rightmost label ink and the leftmost
     axis ink in each row's band:
       A 103|149 gap 46   B 108|149 gap 41   C 104|149 gap 45   D 104|149 gap 45
       E 103|149 gap 46   F 115|149 gap 34   G  97|149 gap 52
     Worst clearance 34px, on F ("F. point at 4.5", the longest label and the one
     that was worst overstruck in round 1). No row collides.

  3. Import validity -> FIXED
     `src="$IMS-CC-FILEBASE$/media/a1-number-line-options.svg"`; all three srcs in
     the corpus now carry the token. The manifest declares
     `sixth_grade_review_section_1_accuracy_check_media` as `type="webcontent"`
     listing all three SVGs, the QTI resource declares a dependency on it, and the
     media `<file>` entries are out of the `imsqti_xmlv1p2` resource.
     Checked further than the token: every manifest `<file href>` exists on disk
     (0 missing), both dependency identifierrefs resolve to declared resources, the
     manifest, the QTI XML and all three SVGs parse as well-formed XML, and the
     token's target path resolves to a file that is actually present.

GEOMETRY RE-DERIVED FROM THE BITMAP — the coordinator's specific request

Rendered at 1020x560 and read the pixels; I did not take the +60 shift on trust and
did not read the values off the SVG source.

  Value-to-pixel map, re-derived post-shift: 26.0000 px/unit, x(value 0) = 357.50.
  Round 1 pre-shift was 26.000 px/unit at x(0) = 298.00. So scale change +0.0000 and
  origin +59.50px against the fixer's claimed +60. The 0.5px is the antialias
  centroid of a 1px stroke and is present identically pre- and post-fix; it is not
  drift.

  Every dot, measured from its colour centroid, against the value its label claims:
    A "point at 4"    -> +4.0014    OK
    B "point at -4"   -> -3.9986    OK
    C "point at 0"    -> +0.0014    OK
    D "point at 3"    -> +3.0014    OK
    E "point at 5"    -> +5.0014    OK
    F "point at 4.5"  -> +4.5014    OK
    G "no point"      -> no teal blob on that row    OK
  Six teal blobs, all area 362px, none on row G. The error is +0.0014 on all six —
  identical, not scattered — which is the signature of a genuinely uniform
  translation. A per-dot slip would show as unequal residuals. The uniform shift did
  preserve the mapping.

  Instrument log, since "should" is what this project keeps getting caught by. My
  first two sweeps both returned MISMATCH on all six dots, contradicting what the
  rendered image plainly shows. Both times the instrument was at fault, not the SVG:
    - Sweep 1 scanned the full width for tick marks and swallowed the choice-label
      glyphs as ticks — 29 "ticks" instead of 17, giving a nonsense 19.45 px/unit.
      Also: a `dark < 90` threshold finds ZERO ticks, because a 1px `stroke="#111"`
      line lands on an integer x and antialiases to ~50% grey across two columns.
    - Sweep 2 masked the teal out of the tick search, which erased the tick sitting
      underneath each dot — 16 ticks on rows A-E, 17 on F (whose dot sits between
      ticks) and G (which has none).
    - Sweep 3 derived the map from row G, the one row carrying no dot, so neither
      fault can reach it, then cross-checked against row A read with the teal left
      in. Both give 17 ticks, 26.0000 px/unit, x(0)=357.50 — agreement along two
      independent paths, and only then did I accept the numbers.

NOTHING ELSE MOVED

  I re-derived required/negated for all 18 items from the current XML by `<not>`
  nesting depth parity and compared against my round-1 record: all 18 key sets and
  all 18 stems are byte-identical to round 1, every `<setvar>` is still 100, every
  `respident` is still `response`, and the respcondition counts are unchanged (1 for
  each item except D3 and D4, which keep their 2 equivalent-form blocks). The fixer
  touched A1's image reference, A1's `alt`, the manifest, and the SVG. It changed no
  stem, no key and no other item.

  One thing the fix newly introduces and I checked rather than assumed: the stem now
  contains two `$` characters, from the `$IMS-CC-FILEBASE$` token. Criterion 7 treats
  stray `$…$` as a defect because it renders literally as math. It does not apply
  here — both `$` sit inside the `src` attribute of the img tag, not in text content.
  Stripping tags leaves 0 `$` in A1's rendered text, so MathJax has nothing to latch
  onto, and Canvas substitutes the token at import before any rendering happens.

MATHEMATICS — unchanged from round 1, all 18 re-confirmed against the current XML

  B1 20 | B2 51 | B3 17 | B4 36 | B5 12 | B6 36
  C1 7 | C2 344.28 | C3 73.56 | C4 32 | C5 0.65 | C6 4/5 | C7 12
  D1 54 | D2 7 | D3 3.6 and 3.60 | D4 7 and 7.00
  A1 keys choice_1 "Point at 4" and negates choice_2..choice_7, each of which I
  confirmed false by measuring the SVG dot positions above.
  B5 3(2^2)=12 and B6 (3x2)^2=36 remain correctly distinguished. D3/D4's second
  respconditions remain load-bearing: both stems ask for two decimal places, so the
  compliant answers 3.60 and 7.00 are what those blocks accept.
  Stems still match the 6th Grade Review worksheet (updated revision) as rendered.
  The C7 "$80" vs "80" wording difference stands as ruled in round 1: not a defect —
  same number, same key, stem says no symbols, and the explanations companion states
  it the same way.

CANDIDATES RULED ON

  Round-1 candidate: A1 plain `src="media/…"` is import-blocking -> CONFIRMED in
  round 1, now REMEDIATED and re-verified along the four paths above.
  Round-1 candidate: audit called A1 clean -> REFUTED in round 1 (three defects), and
  the fixer's action on all three settles it.
  No new candidates were attached for round 2, and I found no new defect.

CLEAN

  All 18 items: A1, B1, B2, B3, B4, B5, B6, C1, C2, C3, C4, C5, C6, C7, D1, D2, D3, D4.

  Nothing stands. 10/10.
