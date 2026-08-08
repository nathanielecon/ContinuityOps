# QTI defect ledger — round 1 verdicts

Scores are round-1 only. Every slice still owes a fix pass, a re-score by the
same judge, and a cold validation round at high effort.

| Slice | Score | Defects standing |
|---|---|---|
| T1-1 | 6/10 | 4 |
| T1-2 | 7/10 | 4 (markup only) |
| T1-3 | 8/10 | 2 (markup only) |
| T1-4 | 9/10 | 1 defect x 6 items |
| T1-5 | 7/10 | 4 (markup only) |
| T1-6 | 8/10 | 1 |
| T1-7+10 | **10/10** | 0 |
| T1-8 | 5/10 | 4 |
| T1-9 | **10/10** | 0 |
| SC-1 | 5/10 | 2 |
| SC-2a | 7/10 | 3 |
| SC-2b | 7/10 | 2 |
| G1a | 6/10 | 3 (all in the A1 figure) |
| G1b, G2a, G2b | pending | |

## Class 1 — a keyed choice is false, and the distractor beside it is true

The most damaging class: the student who applies the sign convention correctly
fails, and the student who reads loosely passes.

**T1-8 P1Q1** — `correct_2` = "Part B: -96 feet below sea level" asserts +96 ft
and is **false**; `wrong_4` = "Part B: -96 feet above sea level" asserts -96 ft,
the submarine's true position, and is **true**. The item is currently unpassable
for a student who reads the sign convention literally. Fix: the two texts trade
places.

Confirmed three ways by that judge: the Part 1 key writes the direction phrase
with an unsigned magnitude, "-96 feet (96 feet below sea level)"; the parallel
Part 2 item keys the clean "84 feet above sea level" and uses the signed form as
its distractor; and the parity argument explains why only Part 1 inverts — the
true elevation is negative there, so sign x direction flips the other way.

**T1-6 P1Q1** — `correct_2` = "Part B: -180 feet below sea level", same
construction, keyed and false. Fix to the key's own form, "-180 feet (below sea
level)".

## Class 2 — a true choice is marked wrong

| Slice | Item | Choice | Why true |
|---|---|---|---|
| T1-1 | P1Q1 | `+-18 and -18` | un-typeset ±; ranges over the keyed +18 |
| T1-1 | P1Q2 | `a + b = 0` | asserted in the stem; **equivalent** to the keyed `\|a\|=\|b\|` under a<0<b, and the key says "(or equivalent)" |
| T1-1 | P2Q2 | `p + q = 0` | same, mirrored |
| T1-8 | P1Q4 | `12` | equals the keyed `n = 12` |
| T1-8 | P2Q4 | `9` | equals the keyed `n = 9` |
| SC-2a | P1Q4 | `1 exactly` | 7^0 = 1, the keyed value restated |
| SC-2b | P2Q4 | `1 exactly` | 5^0 = 1, same |

## Class 3 — the key demands more than the answer key allows

**SC-2a P1Q7, P1Q11 and SC-2b P2Q7** key both an improper fraction and its mixed
twin where the solutions PDF joins them with **"or"**. Under all-or-nothing a
student who wrote one acceptable form scores zero.

Both judges independently found the same trap in the obvious repair: de-keying
one form turns it into a true-but-unkeyed choice, trading a criterion-4 defect
for a criterion-2 one. The SC-2a judge's preferred fix — amend the stem to ask
for every equivalent form — is the one to apply, and it must be applied
identically to all three items.

The SC-2a judge also **refuted** part of the candidate it was given: the claim
that the improper fraction is "the form the assignment asks for" is wrong. The
assignment says only "Simplify". Neither form is privileged, which is precisely
why de-keying one is the weaker repair.

## Class 4 — the QTI offers what the assignment does not

**SC-1 P1Q2 and P2Q2.** `≤` and `≥` are keyed. Both are true of 3/4 vs 0.75 and
2/5 vs 0.4 — and both are unreachable: the assignment offers only `<, >, =, ≠`
and both solution PDFs read "Answer: = (only)". The QTI stem manufactures the two
extra options itself by listing six symbols where the assignment lists four. **A
student who follows the assignment scores zero.**

The judge's fix is right and non-obvious: delete the two choices rather than
re-label them as wrong, because `3/4 ≤ 0.75` is true and a re-labelled choice
becomes a class-2 defect. Backfill two false symbols to hold the count at 8.

## Class 5 — markup that renders as garbage in Canvas

- **T1-5** P1Q2/P2Q2: delimiters *interleaved*, not merely mixed. `\(` and `\)`
  counts balance 2/2, so a naive check passes — and the corrupted text is exactly
  the two numbers the student must add.
- **T1-5** P1Q3/P2Q3, **T1-2** P1Q3, **T1-1** P2Q4: `$...$` where the corpus uses
  `\(...\)`; renders literally. In T1-5 Q3 `$1.75$` reads as currency inside a
  miles problem.
- **T1-2** P2Q3: `$0.\overline{6}\( ... \)\dfrac{2}{3}$` — the prose gets
  typeset as mathematics and both numerals dump as literal characters.
- **Duplicated instruction block**, 10 items: T1-2 P1Q3/P2Q3, T1-3 P1Q1/P2Q1,
  T1-4 P1Q1-Q3/P2Q1-Q3. Two differently worded rules under one bold heading; the
  first suggests partial credit, the second states the all-or-nothing rule the
  scoring actually implements. The other 78 items carry exactly one block, so the
  canonical wording is settled.

## Class 6 — the figures (G1a, and G1b pending)

Three defects, all in `media/*.svg`, covering A1, H6, H7:

1. **Each figure prints its own answer** — as a rendered `<text>` element, as the
   `<title>` tooltip, and as the `aria-label` a screen reader announces first.
   An accuracy check that states its answer cannot do its job.
2. **Labels collide with the axis.** Labels start at x=20, axes at x=90.
   In A1 the struck-through character in "B. point at -4" is the minus sign —
   the one character distinguishing B from A.
3. **Import-blocking image paths.** `$IMS-CC-FILEBASE$` appears **zero times**
   corpus-wide, and the SVGs are declared inside the `imsqti_xmlv1p2` resource
   rather than as `webcontent`, so they are never published to a resolvable path.
   The image *is* the question in all three items.

Verified along four independent paths — string search, `<title>`, `aria-label`,
and two different renderers (my headless Chromium, the judge's cairosvg).

## Confirmed clean, stated explicitly

T1-7, T1-10, T1-9 fully clean. Mathematically clean with markup-only defects:
T1-2, T1-3, T1-5, and T1-4 (whose 8 items the judge worked expression by
expression against the key's "Valid:" lists). G1a's 17 non-A1 items — every
fill-in key independently recomputed and correct.

## Instrument failures this run

1. **My corpus cache truncated 89 of 157 stems.** The extractor unescaped HTML
   entities before stripping tags, so a single-escaped `<` inside a stem became a
   real `<` and the tag-stripper ate to the next `>`. The packages are fine —
   HTML5 only opens a tag when `<` is followed by an ASCII letter, so a browser
   renders them correctly. Two judges caught it from the raw XML before I did.
   Fixed by matching real tags only (`</?[a-zA-Z][^>]*>`) and unescaping after.
2. **My `$`-counter flagged currency as TeX**, marking `$500`, `$450.75`, `$20`
   as broken markup. Three judges independently rejected the false positives.
   The T1-5 judge went further and noted that converting them *would be* a
   regression.
3. The audit's "topic-1-3 all clean" and "topic-1-9 all clean" claims: 1-9 held,
   1-3 did not — it carried the duplicated instruction block, which survives a
   math-only reading.
