# Canvas QTI accuracy checks — audit and repair

14 QTI 1.2 packages, 157 items. Students import these into Canvas to check their
homework against Independent Practice. A wrong key here is worse than a
worksheet typo: it tells a student who got the question right that they got it
wrong.

Corrected packages are in `zips/`. The originals are untouched in `inbox/Inbox/`
as the provenance record.

## What was wrong

30 defects across 12 of the 14 packages. Two packages — `topic-1-7`,
`topic-1-9` — and one slice of the 6th-grade Section 2 corpus were clean on the
first pass and stayed clean.

### A keyed choice that is false, beside a distractor that is true

The worst class, and it inverts the intended outcome: the student who applies
the sign convention correctly scores zero, and the student who reads loosely
passes.

**topic-1-8, Part 1 Question 1.** The submarine descends at −24 ft/min, so after
4 minutes it is at −96 ft.

| ident | was | asserts | |
|---|---|---|---|
| `correct_2` | `Part B: -96 feet below sea level` | +96 ft | **false, and keyed** |
| `wrong_4` | `Part B: -96 feet above sea level` | −96 ft | **true, and marked wrong** |

"d feet below sea level" denotes elevation −d, so a *negative* d flips the
direction word. The two texts have been swapped: the keyed choice now reads
`96 feet below sea level` and the distractor `-96 feet below sea level`.

Three independent confirmations that this was the right direction: the answer
key writes the direction phrase with an unsigned magnitude, `-96 feet (96 feet
below sea level)`; the parallel Part 2 item already keys the clean
`84 feet above sea level` and uses the signed form as its distractor; and a
parity argument explains why only Part 1 inverts — the true elevation is
negative there, so sign × direction flips the other way.

**topic-1-6, Part 1 Question 1.** `Part B: -180 feet below sea level`, keyed,
same double-signing. Corrected to the answer key's own parenthesised form,
`-180 feet (below sea level)`. This item offers no competing Part B choice, so a
swap was neither possible nor needed.

### A true choice marked wrong

Under all-or-nothing scoring these punish precisely the strongest students, and
they are invisible to anyone who only checks that the keyed choices are right.

| Package | Item | Was | Now | Why it was true |
|---|---|---|---|---|
| topic-1-1 | P1Q1 | `+-18 and -18` | `+18 and +18` | un-typeset ±, ranging over the keyed +18 |
| topic-1-1 | P1Q2 | `a + b = 0` | `\|a\| = 2\|b\|` | asserted in the stem, and equivalent to the keyed `\|a\|=\|b\|` |
| topic-1-1 | P2Q2 | `p + q = 0` | `\|p\| = 2\|q\|` | same, mirrored |
| topic-1-8 | P1Q4 | `12` | `n = 72` | equals the keyed `n = 12` |
| topic-1-8 | P2Q4 | `9` | `n = 72` | equals the keyed `n = 9` |
| topic-sc-2 | P1Q4 | `1 exactly` | `1/7` | 7⁰ = 1, the keyed value restated |
| topic-sc-2 | P2Q4 | `1 exactly` | `25` | 5⁰ = 1, same |
| 6th-grade s2 | L1 | — | stem narrowed | `4(2x + 4)` = 8x + 16 is a valid factorisation |

The `a + b = 0` case is the sharpest: with a < 0 < b it is not merely true but
*logically equivalent* to the keyed answer, and the answer key itself reads
"|a| = |b| (or equivalent)". The scoring negated exactly what the key allowed.

### The QTI offering what the assignment does not

**topic-sc-1 Q2, both parts.** `≤` and `≥` were keyed alongside `=`. Both are
true of 3/4 vs 0.75 and 2/5 vs 0.4 — and both are unreachable: the assignment
offers only `<, >, =, ≠`, and both solution PDFs read "Answer: = (only)". A
student following the assignment selected `=` alone and scored **zero**. The QTI
stem manufactured the extra options itself, listing six symbols where the
assignment lists four.

The repair had to be deletion, not re-labelling. Moving `≤` and `≥` into the
negated set would have created two more true-but-marked-wrong choices, since
3/4 ≤ 0.75 is true. Both choices were removed, `≪` and `≫` added to hold the
count at 8, and the stem's symbol list cut to the assignment's four.

### Keys demanding more than the answer key allows

**topic-sc-2 P1Q7, P1Q11, P2Q7** each required *both* an improper fraction and
its mixed-number twin (`46/9` **and** `5 1/9`) where the solutions PDF joins them
with "**or**". A student who wrote one acceptable form scored zero.

De-keying one form would have converted this into a true-but-unkeyed defect —
the two forms are the same number. Instead each stem now reads "…including every
equivalent form of that answer", which makes the requirement derivable by a
student and leaves the key matching what the solutions allow.

### Markup that renders as garbage in Canvas

- **topic-1-5** P1Q2/P2Q2: delimiters *interleaved*, not merely mixed. The `\(`
  and `\)` counts balanced 2/2, so a naive check passed — while the prose was
  typeset as mathematics and the two numbers the student must add fell outside
  the span as literal `$2.4^\circ`.
- **topic-1-5** P1Q3/P2Q3, **topic-1-2** P1Q3, **topic-1-1** P2Q4: `$…$` where
  the corpus uses `\(…\)`. `$1.75$` inside a miles problem reads as currency.
- **topic-1-2** P2Q3: `$0.\overline{6}\( … \)\dfrac{2}{3}$`, mismatched pairs.
- **Duplicated instruction block**, 10 items across topic-1-2, topic-1-3 and
  topic-1-4: two differently worded rules under one bold heading, the first
  implying partial credit and the second stating the all-or-nothing rule the
  scoring actually implements. The other 78 items carry exactly one block, so
  the canonical wording was not in doubt.

### The figures printed their own answers

`media/a1-`, `h6-` and `h7-number-line-options.svg` — the figures for A1, H6 and
H7, where the image **is** the question — each stated their answer three times:

| Encoding | Effect |
|---|---|
| `<text x="20" y="30">` | **rendered as the first visible line of the image** |
| `<title>` | browser tooltip on hover |
| `aria-label` on `<svg role="img">` | the first thing a screen reader announces |

All three read `…Correct: choice A…`, so the leak also made the position
predictable across the set. Confirmed by rendering each SVG and reading the
bitmap — two different renderers, independently.

Two further faults in the same files:

- **Labels struck through by the axis.** Labels drawn at `x=20`, axes starting
  at `x=90`. In A1 the struck-through character in "B. point at -4" was the
  minus sign — the one character distinguishing B from A. Geometry shifted
  +60px (A1) and +220px (H6/H7), uniformly across axes, ticks, tick labels, dots
  and rays so the value-to-pixel mapping is preserved.
- **Import-blocking paths.** `$IMS-CC-FILEBASE$` appeared **zero times** in any
  of the 14 packages, and the SVGs were declared inside the `imsqti_xmlv1p2`
  resource rather than as `webcontent`, so Canvas would never publish them to a
  resolvable path. Every `src` now carries the token, and the media moved to a
  `webcontent` resource the QTI resource depends on.

## What was checked and found correct

Recorded because a first-pass audit reported several of these as defects.

**The "select all equivalent" cluster.** Six 6th-grade items — K9, K10, K11, L1,
N5, N6 — were flagged for having unkeyed true choices. Two judges, on opposite
sides of a slice boundary, independently derived the same test:

> A modifier naming the **operation used to derive** the rewrite constrains the
> derivation. A modifier naming a **property of the resulting form** constrains
> only the form.

Under it, `13` is an evaluation, `(8+5)+0` is the additive identity, `(b+9)+3`
requires commutation, and the given expression restated is not a rewrite at all
— so none of them is what "commutative rewrite" or "associative rewrite" asks
for. **K9, K10, K11, N5 and N6 are correctly keyed and were not changed.** Only
L1 survives, because "factored" describes the form of the result and
`4(2x + 4)` genuinely has it.

**Currency is not a math delimiter.** `$500`, `$450.75`, `$8.75` and every other
bare `$` before a numeral is currency in plain HTML. Three judges independently
confirmed this after an automated sweep flagged them; converting them would have
been a regression. None was touched.

**Trailing-zero alternates.** Six items (D3, D4, M3–M6) carry two
`<respcondition>` blocks keying `3.6`/`3.60`, `220.8`/`220.80` and so on. Their
stems say "Enter a decimal rounded to two places", so the alternate is what
accepts the obedient student. Good design, not a defect.

**A stale companion, not a key error.** 6th-grade M2 keys `700.32 − 84.67 =
615.65`. The explanations companion still poses the *previous* revision's
`700.3 − 284.67 = 415.63`. The QTI matches the updated worksheet and is correct;
the companion is out of date. Changing the key here would have been a serious
regression.

### What the cold round caught that the same-judge round had passed

The cold validation round overturned two slices that had already been re-scored
10/10 by the judge that repaired them. Both defects were invisible to the kind of
reading that had cleared them.

**topic-1-9, both Q1 stems.** They read "A business **owner** loses $450.75…"
and then said the 3 owners share the loss equally — the first sentence gives the
whole loss to one owner, the next says several share it. This project had
**already found and corrected that exact sentence**: `CorrectionsReport.pdf`
logs it and publishes the replacement, and it was applied to the explanations
companion. Only the QTI still carried it, so the accuracy check and the
companion beside it disagreed on the first line of the same question.

The earlier judge cleared it by matching the stem verbatim against the
companion — but against the **superseded** copy in the session scratchpad
(timestamped 10:02) rather than the corrected rebuild in the repo (15:28). It
matched the wording that had been corrected *away from*. Fixed by deleting one
word in each of two stems. No key or choice was affected.

**topic-sc-1 Q2, both parts.** `≡` (U+2261, "is identically equal to") and `~`
were left as distractors. Both are **true**: 3/4 and 0.75 are two spellings of
one rational, and the congruence reading does not rescue `≡` either, since the
difference is 0 and therefore divisible by every modulus.

They survived the repair round on the argument that the narrowed stem now
enumerates a four-symbol answer space in which they do not sit. But that is
exactly the protection the same judge had **rejected one round earlier** when it
insisted `≤` and `≥` be deleted rather than re-labelled, on the ground that being
outside the stem's symbol list does not license leaving a true choice in place.
The package was left applying the strict standard to one pair and the lenient
standard to the other. Replaced with `≉` (U+2249) and `≢` (U+2262), which are
false precisely because the numbers *are* identical and *are* approximately
equal.

## Method

One dedicated judge per slice, 16 slices, no judge holding more than 18 items.
Judges never edit; separate fixers apply. Each slice scored /10, repaired,
re-scored **by the same judge**, then put through a cold adversarial validation
round at higher effort. Two consecutive 10/10 accepts a package.

The cold round was not a formality. Beyond the two overturns above, it corrected
the *reasoning* in four reports that had reached the right verdict on unsound
grounds — including a consistency argument that rested on treating the original
worksheet's own wording as though the package had invented it, and a claim that
a slice cache built *after* a repair could serve as that repair's before-image.

Candidate findings from the first-pass audit were given to judges as *candidates
to verify*, never as findings. Five of the six "select all equivalent"
candidates were refuted on that basis, and two audit claims of "package clean"
were overturned.

## Instrument failures

Three, all mine, all caught. Recorded because on this project instrument errors
have consistently outnumbered document defects.

1. **The corpus cache truncated 89 of 157 stems.** The extractor unescaped HTML
   entities *before* stripping tags, so a single-escaped `<` inside a stem became
   a real `<` and the tag-stripper ate to the next `>`. `Graph 6 < y` cached as
   `Graph 6`. The packages were fine — HTML5 only opens a tag when `<` is
   followed by an ASCII letter, so browsers render them correctly. Two judges
   caught it from the raw XML before I did. Fixed by matching real tags only and
   unescaping afterwards.
2. **A `$`-counter flagged currency as broken TeX**, reporting defects in
   topic-1-3 and topic-1-9 that did not exist.
3. **A glob for `topic-1-1*` matched `topic-1-10`**, briefly reporting three
   applied fixes as missing.
4. **A prescribed verification method that could not detect the defect it was
   for.** Judges were told to check math-delimiter nesting by an ordered scan of
   `\(` and `\)` rather than by counting. A cold judge tested that against the
   known-broken original: the ordered scan **passes** there too — token order
   `\( \) \( \)`, depth never exceeding 1 — while the second span was actually
   the prose `C, then drops $1.85^\circ`. The check that does discriminate is to
   reject any `mattext` block containing both `$` and `\(`; corpus-wide, 39
   blocks contain a bare `$` and none also contains `\(`, so it flags all four
   original defects with no false positive on the currency stems.
5. **A misdescription in the rubric.** It said each item's `<respcondition>`
   carries `maxvalue="100"`. It does not — the respcondition carries
   `<setvar action="Set" varname="SCORE">100</setvar>`, and `maxvalue` lives on
   `<decvar>`. Two judges repeated the phrasing. Nothing is wrong with the
   packages, but a later reader grepping for `maxvalue` inside a `<respcondition>`
   would find nothing and could misread that as a structural defect.

And one bookkeeping failure worth recording because it nearly corrupted the
record rather than the artifact. I lost track of having dispatched the
leftward-ray fix and announced it to the judge that found the defect, then
reported the resulting file write as unattributable and accused that judge of
fabricating a quotation from my own message. The judge was right, refused the
amendment I demanded on the ground that it would put a false statement into the
record to remove a true one, and was vindicated by its own timestamps. The
artifact was never in doubt; my account of it was.

A fourth, narrowly avoided: the slice caches were still pre-fix when the
re-scoring round began, and would have resurrected every closed defect. A judge
flagged it; the caches were rebuilt from the repaired packages.

**Standing rule, reaffirmed in both directions:** when a measurement contradicts
a visible fact, suspect the instrument first — and note that the same suspicion
applied to the *artifacts* would have been wrong here. The packages were sound
every time an instrument disagreed with them.

## Verification

- All 14 packages re-parse as well-formed XML after repair.
- Every `href` declared in every manifest resolves to a file present in the zip.
- `sha256sums.txt` regenerated covering **all 14** packages. The originals'
  checksum file listed only 12 — the two 6th-grade packages had no checksum and
  no validation record, and had never been checked by anyone.
- Item-count reconciliation: **157 items in, 157 out**, none dropped or
  duplicated by the repair and repackage cycle.
- The repaired figures were re-rendered and read as bitmaps, confirming no
  leaked answer, every label legible and clear of its axis, and every dot still
  on the value its label claims.

### The leftward rays painted the wrong side of the line

Rows C and D of H6 and H7 — "ray left" from 6 and from 2 — drew their arrowhead
at the circle rather than at the open end, because the SVG put `marker-start` on
a right-to-left path.

I first recorded this as cosmetic and left it: pre-existing, and affecting only
distractors in items whose key is choice A. The judge that owns those items
overruled me, and quantified why. `markerUnits="strokeWidth"` scales the 9×6
marker path by the ray's `stroke-width:5` to 45×30px, and `refX="9"` pins the
tip at the circle, so the body extends 45px the wrong way — **a filled wedge
across 1.73 units of the set the graph must leave blank.** On a number line, ink
means membership. Both rows depicted something other than what their label
claimed.

Fixed by deleting `style="marker-end:none;marker-start:url(#arrow)"` from the
four affected lines, letting the `.ray` class supply `marker-end` and place the
arrowhead at the unbounded end — the convention the other five rows already use.
Verified by render, twice independently.

## Needs a Canvas import test before the figures can be trusted

**The `$IMS-CC-FILEBASE$` path depth is unverified.** The three image `src`
attributes now read `$IMS-CC-FILEBASE$/media/<file>.svg`, while the manifest
declares those files at
`sixth_grade_review_section_1_accuracy_check/media/<file>.svg`.

The token stands for the root of the package's imported web content, and
Canvas's own exports place that content under `web_resources/`. On that reading
the token resolves to `media/<file>.svg` — one path segment short of where the
files actually sit — and the images would import as broken links. The repair
verified that stripping the token and rejoining under the quiz folder finds a
file on disk, which assumes the mapping rather than testing it.

This is recorded as an open question rather than closed in either direction,
because **it cannot be settled from this environment**: there is no Canvas to
import into and no reference Canvas export in the repository to compare against.
The judge that found it ruled it not a defect — the form present is the one this
project's own rubric prescribes corpus-wide, and severity is low because all
seven options in A1, H6 and H7 are also given verbatim as text choices, so each
item is answerable and correctly scored with the image absent. A missing file
yields a migration warning, not a failed import or a wrong key.

**To settle it:** import one package into Canvas and look at A1. If the figure is
broken, the remedy is to move the three SVGs to `web_resources/media/` and point
the manifest `<file href>` entries there, leaving the `src` strings unchanged.
The same question applies identically to H6 and H7.

What is certain is that the original packages were broken here: they carried no
`$IMS-CC-FILEBASE$` token at all — the token appears zero times in all 14 —
and declared the SVGs inside the `imsqti_xmlv1p2` resource rather than as
`webcontent`, so Canvas would never have published them to any resolvable path.

## Known open items

Neither is in this package set; both are recorded so they are not lost.

- **The worksheet's L1 prompt is now looser than the QTI's.** Narrowing the QTI
  stem to "factor completely using the GCF" makes it stricter than the
  worksheet's bare `Factor: 8x + 16 =`. A student who wrote `4(2x + 4)` on paper
  is now told it is not the answer. The QTI is right and the answer key agrees
  with it; the worksheet wording is what is loose.
- **The 6th-grade explanations companion is stale in two places.** It poses M2 as
  `700.3 − 284.67` where the updated worksheet asks `700.32 − 84.67`, and it
  answers F4 for "undo ÷5" where the updated worksheet asks "undo ×5". The QTI
  matches the updated worksheet in both cases and was left alone.
