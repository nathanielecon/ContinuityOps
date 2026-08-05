# Deep Typographical Scan — 7th Grade Math Document Set

Corrected LaTeX sources and rebuilt PDFs for a five-document math set, plus the
full findings record from the scan that produced them.

## Deliverables

| PDF | Pages | Matches original |
|---|---|---|
| `pdf/6thGradeReview.pdf` | 4 | yes |
| `pdf/6thGradeReviewExplanations.pdf` | 52 | yes |
| `pdf/Topic1ExplanationsPart1.pdf` | 53 | yes |
| `pdf/Topic1Part1Solutions.pdf` | 6 | yes |
| `pdf/Topic1Part2Solutions.pdf` | 6 | yes |
| `pdf/CorrectionsReport.pdf` | 30 | — (new) |

Every rebuilt document has the same page count as the original it replaces.

## Findings

**120 verified findings** — 6 high, 39 medium, 75 low — across
inconsistency (46), formatting (22), grammar (19), notation (15), math (8),
punctuation (5) and spacing (5).

The six high-severity ones:

1. **Topic 1 companion, p.2** — Topic 1-1 Q1's question stem and Checked answer
   describe a submarine rising and descending 18 m, but the restatement, all
   five worked steps and the Final answer solve the additive inverse of a
   **4.5 m climb**. Both answer keys agree with the 4.5 m version, and the
   parallel Part 2 item is likewise a single-move inverse question, so the stem
   was the defect and has been replaced.
2. **6th Grade Review companion, p.46** — the `168.8 ÷ 8` long-division figure
   set the quotient one column too far left, contradicting its own caption and
   steps 1 and 3. Rebuilt with fixed-width alignment.
3–6. **Part 1 Solutions** omitted four questions the companion documents and
   students are told to check against: Topic 1-2 Q3 (Jordan / `3/11`),
   Topic 1-4 Q4 (elevator / 20 floors), and Topic 1-5 Q2 (`−8 °C`) and Q3
   (4.25 miles). All four have been added.

Full detail, with the exact text found and the exact replacement, is in
`pdf/CorrectionsReport.pdf`. Machine-readable records are in `findings/`.

## One finding withdrawn

Extracting these PDFs with `pypdf` produces run-together words
(`onexplanations`, `donotuse`, `Nonzeromeans`) and flattened exponents. Three
scanners raised this as a corpus-wide text-layer fault. It is not a document
defect: the pages render correctly and poppler's `pdftotext` extracts the same
originals cleanly (0 fused words vs `pypdf`'s 29 in the Topic 1 companion). It
is an artefact of one extractor's word-break heuristic. The finding was
withdrawn and nothing in the rebuild was changed on its account. It is retained
in `findings/findings_dismissed.json` for the record.

## Not applied

Four findings propose restructuring an assignment rather than fixing an error,
and acting on them would desynchronise these documents from Independent Practice
worksheets that are not part of this set. They are logged in the report and left
alone — see "Not applied" on page 1 of `CorrectionsReport.pdf`.

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
