# Review of the reported error list

A list of ~25 claimed errors was raised against the corrected document set,
grouped as calculation errors, exponent-expansion errors, missing symbols, and
question/answer inconsistencies.

**Every claim checked is false against both the LaTeX source and the built PDF.**
All of them are produced by a single fault in whatever extracted the text: it
drops U+2212 MINUS SIGN (`−`), U+007C VERTICAL LINE (`|`), and U+00B7 MIDDLE DOT
(`·`). The documents are correct; the reading of them was not.

## How the claims were checked

Three independent sources, agreeing:

1. **LaTeX source** — `tex/parts/*.tex`, the authored form.
2. **Built PDF** — `pdf/Topic1ExplanationsPart1.pdf`, extracted with `pdftotext`,
   which preserves `−`, `|` and `·` correctly.
3. **Git history** — `git log -S` for each claimed error string. None has ever
   existed in this repository.

## The mechanism, demonstrated

Applying `drop −, drop |, · → -` to the true PDF text reproduces the reported
claims verbatim:

| PDF actually says | List claims | Reproduced by the fault |
|---|---|---|
| `So \|a\| equals \|b\|.` | "States *So a equals b*" | `So a equals b.` |
| `Start at −5. Move right 3. Land on −2.` | "Writes 6+(−8)=2"; "Start at 5" | `Start at 5. Move right 3. Land on 2.` |
| `Both sides simplify to −3` | "States *Both sides simplify to 3*" | `Both sides simplify to 3` |
| `20. Start 64 · 30 by finding 64 · 3.` | "Uses subtraction signs for multiplication" | `Start 64 - 30 by finding 64 - 3.` |
| `+18 + (−18) = 0` | "Refers to *+18 and 18*" | `+18 + (18) = 0` |
| `floor −3 … floor −1` | "References floor numbers 3 and 1" | `floor 3 … floor 1` |
| `Checked answer: Part A: −15` | "Checked answer lists 15" | `Checked answer: Part A: 15` |
| `Checked answer: −1 kilometer` | "Drops the negative sign" | `Checked answer: 1 kilometer` |

The whole "Missing Symbols, Variables, & Text Corruption" group is the same
fault seen directly rather than through its arithmetic consequences: absolute
value bars reported as "blank spaces", `Test :` missing its `≠`, `-8-5|` and
`120-150` in the Lesson 1-4 expression lists. Those are `|` and `≠` and `−`
failing to survive extraction.

## Two claims that are not extraction artifacts, and are still wrong

- **"Expanding 3⁶ lists only five factors of 3."** The source and the PDF both
  read `3^{6} = 3 × 3 × 3 × 3 × 3 × 3` — six factors — at all three cited sites
  (`t1e_F.tex` lines 43, 562, 744). A miscount. Note that `3^{6}` extracts as
  the digit pair `36`, which may have started it.
- **"(−5)² expands as three factors."** Source and PDF both read
  `(−5)^{2} = (−5) × (−5)` — two factors (`t1e_D.tex` line 130). No three-factor
  expansion of `(−5)²` exists anywhere in the set.

## Why it "passed inspection"

It did not need to. These errors are not present and, per `git log -S`, never
were. The 114 verified findings this project did log and fix are recorded in
`findings/findings_verified.json` and `tex/CorrectionsReport.tex`; none of them
corresponds to a claim on this list.

## What to do about it

Nothing in the documents. If the list came from a tool in the review pipeline,
that tool needs a Unicode-aware text layer — these documents use real typographic
minus, vertical bars and middle dots, and any check that reads them through an
ASCII-lossy extractor will keep generating this same list of phantom sign errors.
