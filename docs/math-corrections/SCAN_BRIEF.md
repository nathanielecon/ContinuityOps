# Deep Typo Scan — Shared Brief

## Corpus
Five student-facing 7th-grade math documents (LaTeX-produced PDFs) in
`/tmp/claude-0/-home-user-ContinuityOps/ebe1222c-2fe9-5342-8afc-bd62d3c3390b/scratchpad/`:

| File | Pages | Role |
|---|---|---|
| `6thGradeReview.pdf` | 4 | Diagnostic worksheet, sections A–N |
| `6thGradeReviewExplanations.pdf` | 52 | Worked explanation companion for the above |
| `Topic1ExplanationsPart1.pdf` | 53 | Worked explanation companion for Topic 1 Independent Practice Part 1 |
| `Topic1Part1Solutions.pdf` | 6 | Brief answer key, Part 1 |
| `Topic1Part2Solutions.pdf` | 6 | Brief answer key, Part 2 (parallel version of Part 1, different numbers) |

Plain-text extractions live in `scratchpad/extract/*.txt` (page markers included).

## Method — READ THE PDF, NOT JUST THE TEXT
Use the `Read` tool with the `pages` parameter on the PDF itself so you SEE the
rendered typography (max 20 pages per call). The text extraction mangles kerning
("W e Need"), so you MUST confirm every spacing complaint against the render.

- Real defect: words genuinely fused in the render, e.g. `isnotright`, `yon`,
  `donotuse`, `Go4.5 meters down` — caused by `\textbf{...}` runs with no space.
- Extraction artifact only: `W e`, `82 .731`, `1 3\n4` fraction splits. Do NOT report these.

## What counts as a finding
1. **Spelling / grammar / punctuation** errors.
2. **Word-fusion & spacing** defects visible in the render (missing space around
   bold/italic runs, missing space after a colon or before a unit).
3. **Math errors**: wrong arithmetic, wrong sign, wrong simplification.
4. **Internal inconsistency**: the stated question does not match the worked
   solution or the "Checked answer" (this corpus has at least one such case —
   see below), answer key disagrees with the explanation companion, a term is
   defined two different ways, section/question numbering skips or repeats.
5. **Notation inconsistency**: e.g. `−52` where `−5^2` is meant, exponents that
   lost their superscript, `⇒`/`→` used inconsistently, inconsistent use of
   `$` on money, degree symbol spacing (`13 ◦F` vs `13°F`).
6. **Mixed-number / fraction formatting** that reads ambiguously, e.g. `151/2`
   intended as `15 1/2`.

### Known seed example (confirm and describe precisely)
`Topic1ExplanationsPart1.pdf` p.2, Topic 1-1 Question 1: the *Question* block
reads "A submarine rises 18 meters ... then descends 18 meters" with
"Checked answer: +18 + (−18) = 0", but every following block ("What the question
is asking", the numbered steps, "Final answer") is about the additive inverse of
a **4.5 meter climb**, matching `Topic1Part1Solutions.pdf`. One of the two is wrong.

## Output format — STRICT
Write your findings as a JSON array to the file path you are given, and also
return the same JSON as your final text. Schema per finding:

```json
{
  "doc": "Topic1ExplanationsPart1",
  "page": 2,
  "locator": "Topic 1-1 Question 1 > Question block",
  "category": "inconsistency",     // spelling|grammar|punctuation|spacing|math|inconsistency|notation|formatting
  "severity": "high",              // high (changes meaning/answer) | medium (confusing) | low (cosmetic)
  "quote": "exact text as rendered",
  "correction": "exact replacement text",
  "why": "one sentence"
}
```

Rules:
- `quote` must be verbatim from the rendered page, long enough to locate uniquely.
- Report every real instance. If a defect repeats (e.g. the same fused bold label
  on 40 pages), report it ONCE with `"locator"` noting the pattern and add a field
  `"occurrences": "all pages / list"`, rather than 40 duplicate entries.
- Do NOT invent findings. If a page is clean, say so by omitting it.
- Be exhaustive on your assigned pages; do not sample.
