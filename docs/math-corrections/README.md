# Deep Typographical Scan — 7th Grade Math Document Set

Corrected LaTeX sources and rebuilt PDFs for a five-document math set, plus the
full findings record from the scan that produced them.

## Deliverables

| PDF | Pages | Matches original |
|---|---|---|
| `pdf/6thGradeReview.pdf` | 2 | yes (rebuilt from the revised worksheet) |
| `pdf/6thGradeReviewExplanations.pdf` | 52 | yes |
| `pdf/Topic1ExplanationsPart1.pdf` | 53 | yes |
| `pdf/Topic1Part1Solutions.pdf` | 7 | no — 6 in the original, +1 by design (see below) |
| `pdf/Topic1Part2Solutions.pdf` | 6 | yes |
| `pdf/CorrectionsReport.pdf` | 27 | — (new) |

Every rebuilt document matches its source's page count except
`Topic1Part1Solutions.pdf`, which grew 6 -> 7. That is intended, not drift: the
key was missing four questions the assignment contains (Lesson 1-2 Q3, 1-4 Q4,
1-5 Q2 and Q3) and they were added. A key that fits the old page count would
still be missing them.

## Findings

**114 verified findings** — 12 high — across two rounds. Round 1 scanned the
five documents against each other; round 2 re-checked everything against the
**Topic 1 Independent Practice** assignment and a **revised 6th Grade Review**
worksheet supplied afterwards. Those sources overturned 12 round-1 findings and
produced 10 new ones.

### Round 2 corrected round 1's headline finding

The assignment's Lesson 1-1 Q1 is *"A submarine rises 18 m from a point below sea
level, then descends 18 m"* (Part A: sum; Part B: why they are additive
inverses). The companion's **question stem was right**; its **worked steps and
both answer keys** solved a single-move inverse of a 4.5 m climb — a number
absent from the assignment. Round 1 treated the two agreeing keys as evidence
and rewrote the correct stem to match the wrong steps. Both keys were wrong the
same way, so they corroborated each other. Now fixed the right way round.

Other round-2 findings: **Lesson SC-1 Q2** — both keys answered `=, ≤, ≥` but the
assignment offers only `<, >, =, ≠`, so the answer is `=` alone; the **Part 2 key
was missing the same four questions** the Part 1 key was; Part 2's SC-2 Q2 said
cupcakes where the assignment says muffins; and individual lessons are
**"Lesson 1-N:"**, not "Topic 1-N" — "Topic 1" names the unit. The revised 6th
Grade Review also changed real math: **M2 is now 700.32 − 84.67 = 615.65**, **F4
now asks to undo ×5 (answer: divide by 5)**, and **C7 is now 15% of $80 = $12**.

Round 1's other high-severity findings, all still standing:

1. **6th Grade Review companion, p.46** — the `168.8 ÷ 8` long-division figure
   set the quotient one column too far left, contradicting its own caption and
   steps 1 and 3. Rebuilt with fixed-width alignment.
2–5. **Part 1 Solutions** omitted four questions the companion documents and
   students are told to check against: Topic 1-2 Q3 (Jordan / `3/11`),
   Topic 1-4 Q4 (elevator / 20 floors), and Topic 1-5 Q2 (`−8 °C`) and Q3
   (4.25 miles). All four have been added — and round 2 confirmed all four
   against the assignment, then found the Part 2 key missing its own four.

Full detail, with the exact text found and the exact replacement, is in
`pdf/CorrectionsReport.pdf`. Machine-readable records are in `findings/`.

## Judge loop

After the corrections were applied, every slice of both explanation companions
was put through an adversarial judge loop: a dedicated judge per slice, scoring
out of 10 against a fixed rubric, looping with a separate fixer until 10/10, then
a second cold 10/10 to validate. **All 11 slices were accepted.**
`judge/LOOP_STATE.md` holds the per-slice ledger.

It was worth running. It caught a regression introduced by a fix, a fixer's
false self-report, residue from a withdrawn edit, three fixes that displaced a
defect rather than closing it, and 22 restatements missing the worksheet's answer
blanks. One slice was accepted, then **revoked** when another slice's judge found
that defect in it, then re-judged clean.

Two caveats are recorded rather than smoothed over:
- **Four of eleven slices** (A, H, I, J) completed their two passes with judges
  that had lost memory of the earlier round. They got two independent 10/10
  reads, not one judge confirming itself - a different property from the one
  specified.
- **Four instrument failures** were found, each capable of a confident wrong
  verdict: a CJK guard that failed open, the same guard false-positiving on
  PDFs, `\rule` emitting an `l` primitive so rectangle-counting reports every
  blank missing, and `pdftotext -layout` transposing built-up fractions.

## Known open item

The revised worksheet sets its section headings as navy banner boxes with white
text on light panels. The rebuild uses plain bold headings. No slice owns the
worksheet, so no judge covers it. Unfixed.

## Withdrawn findings

Extracting these PDFs with `pypdf` produces run-together words
(`onexplanations`, `donotuse`, `Nonzeromeans`) and flattened exponents. Three
scanners raised this as a corpus-wide text-layer fault. It is not a document
defect: the pages render correctly and poppler's `pdftotext` extracts the same
originals cleanly (0 fused words vs `pypdf`'s 29 in the Topic 1 companion). It
is an artefact of one extractor's word-break heuristic. The finding was
withdrawn and nothing in the rebuild was changed on its account.

**SC-lesson naming (3 findings).** `Lesson SC-1: Compare Rational Numbers` was
flagged as a one-off against the `Topic 1-N` pattern and normalised to
`Topic SC-1`. The teacher's weekly lesson plan names it
**Lesson SC-1: Compare Rational Numbers (SC1-1)**, so the source was correct.
Reverted in all three documents, along with `Topic SC-2: Use the Laws of
Exponents`. The remaining Lesson SC-1 / Topic SC-2 asymmetry is left as written
and flagged as a question for the teacher.

**Round-1 over-corrections to the 6th Grade Review (9 findings).** Section
title case, the Directions sentence, E1's telegraphic "Greater:", J3/J5 slash
notation, C1's missing period, the D4/M6 "(decimal)" tags and the deliberate
K10/N5 duplicate were all flagged as defects. The author kept every one of them
in the revised worksheet, so they are house style. All reverted.

**"on your notebook" (1 finding).** Changed to "in your notebook", then
reverted: the lesson plan's own wording is "Independent Practice *on* notebook",
so this is the author's register, not an error.

All withdrawn findings are retained in `findings/findings_dismissed.json`.

## Not applied

Four findings propose restructuring an assignment rather than fixing an error,
and acting on them would desynchronise these documents from Independent Practice
worksheets that are not part of this set. They are logged in the report and left
alone — see "Not applied" on page 1 of `CorrectionsReport.pdf`.

## Token strategy

`TOKEN_STRATEGY.md` records what the tooling actually cost and saved on this
run, measured rather than quoted, and how to apply pxpipe next time. Short
version: the cost was input, not output; the two output-compression tools
produced no net saving; the cheap-fixer/frontier-judge split was the one clear
win; and pxpipe is the correctly-aimed tool but is a launch-time wrapper, not
something that can be enabled mid-session in a managed remote environment.

## Building

Requires TeX Live with `lmodern`, `tcolorbox`-free `tikz`, `enumitem`,
`needspace`, `xspace`, `microtype`.

```sh
cd tex
for f in 6thGradeReview 6thGradeReviewExplanations Topic1ExplanationsPart1 \
         Topic1Part1Solutions Topic1Part2Solutions CorrectionsReport; do
  pdflatex -interaction=nonstopmode "$f.tex" && pdflatex -interaction=nonstopmode "$f.tex"
done
```

`tex/mathdocs.sty` carries the shared house style. The two large companions are
assembled from fragments in `tex/parts/`; the other documents are single files.

`SCAN_BRIEF.md` and `REBUILD_BRIEF.md` are the briefs the scanning and rebuild
passes worked from.
