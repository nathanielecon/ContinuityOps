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

### The same marker bug in row F, and two numbers I got wrong reporting it

Row F of H6 draws a short ray, 25px. The 45px arrowhead is longer than the ray
it terminates, so the wedge overhung the circle and put filled ink to the left of
the 7 the row claims. I passed this as cosmetic in one round; the cold judge
overturned it on a consistency argument that is decisive — the same slice had
already charged rows C and D for putting ink on the side the graph must leave
blank, and charged them while noting scoring was unaffected and the construction
pre-existing, so neither fact can excuse row F.

The fix is the same deletion, and the re-score measured it: row F's left ink
boundary moved **+6.250 → +6.635**, the new edge being the open circle's own
outer ring, with every other boundary in both figures moving exactly +0.000.

Two figures I reported when recording the overturn do not survive measurement:

- I said the misplaced ink spanned **0.962 units from +6.038**. Measured by
  exact-RGB match against tick calibration, it is **0.750 units from +6.250**.
  The 6.038 came from a tolerance-based colour test picking up the antialiased
  grey tick at 6, not the wedge. On flat fills like these, exact match is the
  right instrument and tolerance is not — at tolerance 40 the same test swallows
  the option label text.
- I said row F's ink began further left than the correct answer's. **It did not.**
  Row A, the key, begins at +5.635 including its open-circle ring and +6.000
  excluding it; row F began at +6.250. Row A's ring extending either side of 6
  is ordinary number-line drafting, not a fault.

The defect stands and the fix is right — 0.750 units of filled ink sat left of
the 7 — but it stands on its own measurement, not on the comparison I drew.

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

## Item format: 43 free-response questions restored to numeric entry

The worksheet states the answer contract in its own directions: *"Write decimal
answers as decimals and fraction answers in simplest terms. Round to two decimal
places."* The Topic packages did not honour it. All 88 Topic items were
`multiple_answers_question` — select-all — including questions whose source is a
bare calculation. `Evaluate: |−9| =` shipped as eight choices with the key at
position 0.

**How it got past the judge loop.** This run's task, per `MASTER_PROMPT.md` §2.2,
was to *verify* the Canvas quizzes against the assignment and keys. The quizzes
arrived already built in select-all form, and the seven-criterion rubric covered
key correctness, scoring, and rendering — not item-format fidelity. Judges who
raised the format repeatedly and correctly ruled it outside the rubric. The loop
was scoped so that it could not catch this.

**Converted: 43 items** whose key is a single numeric value, now
`numerical_question`, matching the shape the 6th-grade packages already use
successfully (`response_str` / `render_fib fibtype="Decimal"`, scored by an `<or>`
of an exact `varequal` and a `vargte`/`varlte` range).

Corpus item types, before → after:

| type | before | after |
|---|---|---|
| `multiple_answers_question` | 109 | 66 |
| `numerical_question` | 37 | 80 |
| `short_answer_question` | 11 | 11 |
| **total** | **157** | **157** |

Details worth recording:

- Stems lost the select-all boilerplate and gained **"Enter the number only, no
  units or symbols."** Keys carrying units or currency (`570 feet`, `$425`,
  `20 floors`, `-150.25 per owner`) became bare numbers.
- Decimal answers gained **"Round to two decimal places."**
- **Two answers are exact at three decimals** — 3/8 = 0.375 and 5/8 = 0.625.
  Rounding them blindly would mark the exact answer wrong, so both the exact
  value and the two-place form are accepted.
- The two-place form uses **round-half-up**, the convention taught in class.
  Python's built-in `round()` is banker's rounding and turns 0.625 into 0.62,
  which is not what a student following the instruction types. 0.625 → 0.63.

**Three fraction answers** — `5^0+3^{-2}+\frac{2^6\cdot 2^3}{2^7}` = 46/9,
`6^{-2}+(8/4)^3` = 289/36, and `2^0+2^{-3}` = 9/8 — became `short_answer_question`
taking a simplified `a/b`, the pattern 6th-grade Section 2 item K4 already uses.
They are the only fraction-valued answers in the corpus. Final tallies:
select-all 109 → 63, numeric 37 → 80, short answer 11 → 14, total still 157.

**63 items remain select-all**, and none of them can be a numeric entry: 39 have a
single non-numeric answer (vocabulary such as "coefficient", algebraic forms such
as `3y + 18`, inequalities such as `x > 5`, and the number-line graph choices),
22 are multi-part questions combining a value with an explanation, and 2 ask for
an ordered list rather than a single value.

### The eight that a split would convert, with their answers already verified

Eight of those 22 hold a numeric answer inside a multi-part item. Splitting each
into a numeric item plus a conceptual one would carry the contract the rest of
the way. It is **not done here**, because it changes the item count and every
quiz's points total and requires authoring new stems — the author's call, not a
repair. The values are recorded so that call is a mechanical step rather than
another investigation. Each is quoted from the solutions PDFs, not inferred:

| Item | Part A | Part B | Source line |
|---|---|---|---|
| topic-1-6 P1Q1 | **−15** | **−180** | `Answer: Part A: −15; Part B: −180 feet (below sea level)` |
| topic-1-6 P2Q1 | **+20** | **+180** | `Answer: Part A: 20 (or +20); Part B: 180 feet above sea level` |
| topic-1-8 P1Q1 | **−24** | **−96** | `Answer: Part A: −24; Part B: −96 feet (below sea level)` |
| topic-1-8 P2Q1 | **+28** | **+84** | `Answer: Part A: 28 (or +28); Part B: 84 feet above sea level` |
| topic-sc-2 P1Q2 | expression | **4** | `Answer: Part A: 2 (or equivalent); Part B: 4 cupcakes per friend` |
| topic-sc-2 P2Q2 | expression | **9** | `Answer: Part A: 2 (or equivalent); Part B: 9 muffins per friend` |
| topic-1-3 P1Q1 | number-line | **−2** | `Answer: Part A: number-line moves as above; Part B: −2` |
| topic-1-3 P2Q1 | number-line | **−2** | `Answer: Part A: number-line moves as above; Part B: −2` |

The two `topic-sc-2` Part A answers extract as a bare "2", which is the
superscripts collapsing — the expression is `2^4 ÷ 2^2`, not the number 2. Those
Part As are expressions and stay select-all. Same for the `topic-1-3` Part As.

Worth noting in favour of the split: a numeric Part B **removes** the
double-signing trap entirely. `-96 feet below sea level` is the phrasing that
produced two of this project's worst defects, because a signed magnitude plus a
direction word can assert the opposite of what it appears to. A box that takes
−96 cannot be read two ways.

## The answer is always the first choice

Raised independently by four judges, each correctly noting it falls outside the
seven rubric criteria. Verified corpus-wide rather than sampled:

- **88 of 88** Shape A items list their keyed choices as the leading contiguous
  block — 63 key position 0 alone, 11 key positions 0–1, 11 key 0–2, 3 key 0–3.
  Zero exceptions.
- **21 of 21** Shape B select-all items key position 0.
- All **14** packages set `<shuffle_answers>false</shuffle_answers>`.

So "select the first option, or the first N" scores 100% on every select-all item
in the corpus without doing any mathematics. On an instrument whose entire
purpose is letting a student check whether they got a question right, that is
worth the author's attention.

**Nothing was changed.** Every key is correct and every item scores accurately
for a student who actually answers, so this is not a defect in any item — it is a
test-design property of the whole corpus, and the fix is a decision rather than a
repair. Three routes, with the trade-off that makes it non-obvious:

1. `shuffle_answers=true` on the 12 Topic packages and 6th-grade Section 2, which
   reference no images. **Not** on Section 1: A1, H6 and H7 present seven lettered
   rows in a single graphic and their choice texts mirror that order, so shuffling
   would desynchronise the picture from the option list.
2. `shuffle_answers=true` everywhere, and rewrite A1/H6/H7's choices to be
   self-describing so they no longer depend on position.
3. Permute the choice order inside each item and leave shuffling off. Preserves
   the figure correspondence and makes the packages correct on their own rather
   than depending on a Canvas setting, but touches all 109 select-all items and
   every reorder needs its `original_answer_ids` updated to match.

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

---

# The answer-format round

The corpus was built almost entirely as select-all with all-or-nothing scoring.
That is the wrong instrument for most of these questions twice over: the choices
leak the answer, and a distractor that happens to be true makes a student who
reasons correctly score **zero**.

The author's hierarchy for this round, in priority order:

1. **Numeric entry** — almost all.
2. **Short answer** — one or two words, or a symbolic answer where the stem
   prescribes the exact format with a worked example.
3. **Select-all** — last resort, **at least 7 close distractors**. Distinguishing
   *expressions* is the good case and stays select-all.

Every stem prescribes the exact format of its answer. Every item is auto-scored
by Canvas; nothing requires manual grading.

| | before | after |
|---|---|---|
| items | 157 | 175 |
| numeric entry | 80 | 106 |
| short answer | 14 | 37 |
| select-all | 63 | 32 |

Select-all falls from 40% of the corpus to 18%, and every survivor is a figure,
an expression-discrimination item, or multi-statement reasoning.

## Defects found this round that were mis-scoring students

Found by parallel workers reading the pristine corpus against the source PDFs,
not by any prior judge round.

### Six items shipped TRUE statements as wrong answers

Under all-or-nothing scoring, selecting one costs the whole item.

| Item | True, and scored wrong |
|---|---|
| `K9` | `8 + 5` (its own stem), `13`, `(8 + 5) + 0`, `8 + (5 + 0)` — all equal 13 |
| `K10`, `N5` | `7a + 0`, `7 × a` (the stem verbatim) — identically `7a` for every `a` |
| `K11` | `(b + 9) + 3`, `b + 12`, `(b + 3) + 9` — all equal `b + 12` |
| `N6` | `(x + 8) + 5`, `x + 13`, `(x + 5) + 8` |
| `topic-1-2` P2Q2 | `The sign does not matter here.` — true; `The denominator alone determines answer.` — the textbook rule, so it punishes the taught student |

**The systemic cause was that every rewrite item included its own stem
expression as a distractor.** Under "select all *equivalent* rewrites" that is a
correct answer, not a trap. The value-collapsed choices (`13`, `b + 12`,
`x + 13`) compound it.

The stems had to be tightened as well as the choices, because under the old
wording no choice set could be made correct — `13` genuinely is equivalent to
`8 + 5`. The narrowing is the author's own definition, from the explanations
PDF: *"Regroup means move the parentheses without changing the left-to-right
order of the terms."*

### Other live defects

- **`topic-1-4` scored "at least two" as all-or-nothing.** The worksheet asks for
  at least two expressions; all six items keyed 3–4 under `<and>`. A student who
  wrote two — exactly what was asked — scored zero.
- **Eight numeric items keyed a negative value with no sign guidance.** "Enter
  the number only, no units or symbols" reads as "omit the minus sign".
- **`topic-1-2` P2Q3 keyed `3x = 2`** where its own solution PDF derives
  `9x = 6`. Part 1 keys `99x = 27`, which does match its PDF.
- **`topic-1-2` P2Q2's stem omitted the `b ≠ 0` guard** that Part 1 carries and
  the solution states. Without it the key is not "always right".
- **`topic-sc-1` Q2 offered `≉ ≢ ≪ ≫`**, symbols neither the assignment nor
  either key ever names.

## Load-bearing wording — do not "tidy" these

Three items are correct **only** because of a single word. Normalising any of
them creates a second true answer.

- `K2` — "**prime** factorization". `9 × 10`, `3^2 × 10`, `2 × 45` all equal 90.
- `L1` — "factor **completely**". `4(2x + 4)` expands to exactly `8x + 16`.
- `topic-1-2` **P1Q2** — "which outcome is **NOT** possible". It carries the same
  statement distractors that broke its Part 2 twin, and they are false only under
  this framing. **The two stems must not be harmonised in either direction.**

## Self-referential choices are banned

`topic-1-2` P2Q2 offered `More than one listed choice is correct.`, `All listed
choices are correct.`, `No listed choice can be correct.`

Their truth is a function of the *other* choices. `More than one…` became true
only because a different distractor was true — so an edit elsewhere re-keys them
with no signal at the site of the edit, which is exactly how the defect arose.
They also carry no mathematical content and are not authored: the source
worksheet has only options A, B, C. Removed, and recorded as a structural rule.

`topic-1-2` P1Q2 still carries the trio and was deliberately left alone; it is
flagged for a separate structural pass with its stem untouched.

## topic-1-4 → twelve short-answer items

Split by **form**, not by "write a different one". Canvas cannot compare one
item's answer with another's, so "a different expression" would accept the same
string twice. Form-a strings contain no `|` and form-b strings all do, so the two
accepted sets are provably disjoint.

- **a** — "uses subtraction and no absolute-value bars"
- **b** — "uses absolute-value bars"

Each stem then **names the methods it permits** (BF-2026-042). Form-general
wording left an open family that exact string matching cannot close — the key's
own phrase is "any correct distance expressions" — and two widening rounds each
revealed more correct forms still rejected. Pinning the operand order would close
it, but would rule the key's own `|-8| + 5` split-at-zero method off-form. Naming
the methods closes the set by enumeration and drops nothing.

**The second method is per-item, and this is the part that is easy to get wrong.**
It depends on whether the two values straddle zero: on Part 1 Q1 (`5`, `-8`) the
distances from zero **add** (`|-8|+5` = 13); on the other five, both values sit on
one side and the distances **subtract** (`|150|-|120|` = 30). A single global
"sum" clause would name a method yielding 270 on Part 1 Q2. Form a needs the same
per-item treatment on the two signed-elevation items, which admit both
`-25-(-40)` and the key's own `40-25`.

172 accepted strings, each evaluated against the item's true distance, each
listed compact, spaced, and with a U+2212 twin — a student who copies the stem's
rendered MathJax gets a Unicode minus, and Canvas compares bytes. Two automated
checks hold: 0 value mismatches, and 0 closure violations (every accepted string
reachable from a named method, every named method reachable).

## Forbidden near-misses

These are TRUE and must never be authored as distractors. The failure mode now
is an editor "correcting" `8 + (5 × 0)` into `× 1` and silently restoring a true
choice.

- `2^(4/2)` and `3^(4/2)` — dividing the exponents is the classic error, but with
  exponents 4 and 2 it evaluates to the key in **both** variants.
- `27/99` (= 3/11), `6/9` (= 2/3), `a7` (reads as `7a`), `7a + 0`, `7a × 1`
- `8 + (x + 5)`, `9 + (b + 3)`, `b + 12`, `x + 13` — any reordering of the
  addends is value-true even though it is not an associative rewrite
- `10 - 4 - 8`, `12 - 5 - 9`, `(-4) + (-8) + 10`
- `Their sum is zero.`, `They have the same absolute value.`, `Each is the
  opposite of the other.`, `They are the same distance from zero.`

## Build reproducibility

Two defects in the build itself, both caught late.

`repackage.py` writes into `zips/`, and `zips/` was also the extraction source
for the next build, so the pipeline was applying its transforms on top of its own
output. `validate.py` still passed — every rule it enforces is a property of the
final state, not of how that state was reached — but the permutation had run
twice, so the shipped choice order was not the one this document describes.
`build.sh` now takes a **git ref** as its source and extracts to a temp
directory; feeding the pipeline its own output is impossible by construction.

Separately, two builds of provably identical content produced different sha256s,
because zip stores each entry's mtime and extraction stamps "now". Checksums are
how this project proves an artifact is the one a judge scored, so entries are now
written with a fixed date in sorted path order. Two independent builds are
byte-identical.
