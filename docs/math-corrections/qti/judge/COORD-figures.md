# Coordinator finding — the three number-line figures print their own answers

Derived independently of any judge, confirmed along four paths.

Files (all in `6th-grade-review-section-1`):
`media/a1-number-line-options.svg`, `media/h6-number-line-options.svg`,
`media/h7-number-line-options.svg` — the figures for items **A1, H6, H7**, where
the image *is* the question.

## Defect 1 — the answer is stated on the student-facing figure (HIGH)

Each SVG carries its answer three times over:

| Encoding | A1 | Effect |
|---|---|---|
| `<text x="20" y="30">` | `A1 number-line choices. Correct: choice A, closed point at 4.` | **rendered as the first visible line of the image** |
| `<title>` | same string | browser tooltip on hover |
| `aria-label` on `<svg role="img">` | same string | read aloud by a screen reader |

H6: `Correct: choice A, open circle at 6 with ray right.`
H7: `Correct: choice A, open circle at 2 with ray right.`

Confirmed by rendering each SVG at 960x560 with headless Chromium and reading the
bitmap: the sentence appears in black 16px Arial above choice A in all three.
This is not a hidden authoring comment — it is printed on the figure. Any student
opening A1, H6 or H7 is told the answer before choosing. For a screen-reader user
it is the *first* thing announced.

In all three the answer is choice A, so the leak also makes the position
predictable across the set.

**Fix:** delete the `<text>` element, and reduce `<title>` and `aria-label` to a
neutral description (`"Number-line answer choices A through G."`). The
accessibility attributes must stay — they must simply stop naming the answer.

## Defect 2 — choice labels collide with the axis (MEDIUM)

Each label is drawn at `x=20, y=<row>` while that row's axis starts at `x=90`, so
every label longer than ~70px is struck through by the axis line. Worst in H6/H7,
where labels are long: `C. open circle at 6, ray left` is rendered with the axis
running through the middle of the text and is close to illegible. Visible in the
render for all three files, every row.

**Fix:** move the axis origin right (`x1=90` -> `x1=300`) or put each label on its
own line above its axis. This is a coordinate change across ~7 rows x 3 files —
Sonnet-tier work, not a text substitution.

## Defect 3 — image `src` is not Canvas-rewritable (HIGH, import-blocking)

```
src="media/a1-number-line-options.svg"
```

Canvas rewrites in-item image paths only when they are written against the
`$IMS-CC-FILEBASE$/` token. Corpus-wide check: **the token appears zero times in
any of the 14 packages.** The three SVGs are declared as `<file>` entries inside
the `imsqti_xmlv1p2` resource rather than as a separate `webcontent` resource, so
they are unlikely to be imported into course files at all. On import the relative
path resolves against the quiz page URL, not the file location, and the image
404s.

Where the image *is* the question — all three of these — a broken image makes the
item unanswerable, not merely ugly.

**Fix:** `src="$IMS-CC-FILEBASE$/media/<file>.svg"`, and declare the media as a
`webcontent` resource that the QTI resource depends on.

## Instrument note

The `<text>` element was found first by string search, which on its own proves
only that the string exists in the file — it could have been clipped, white on
white, or outside the viewport. The render settles it. Standing rule applied in
the opposite direction from usual: the instrument agreed with the visible fact,
and the render is what made it a finding rather than a suspicion.
