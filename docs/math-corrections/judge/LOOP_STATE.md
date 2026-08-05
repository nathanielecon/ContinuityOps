# Judge loop — state at session limit (resets 2:50pm UTC)

Rule: a slice is ACCEPTED only on TWO CONSECUTIVE 10/10 from its judge
(round-N pass, then a cold adversarial validation pass).

| Slice | Content | R1 | R2 | R3 | Validation | Status |
|---|---|---|---|---|---|---|
| A | 1-1 Q1-4, 1-2 Q1-3 | 7 | 8 | not run | — | **OPEN** — fix applied, needs re-judge |
| B | SC-1, 1-3 | 8 | 10 | — | died mid-read | **OPEN** — needs validation |
| C | 1-4, 1-5 | 7 | 10 | — | died mid-read | **OPEN** — needs validation |
| D | 1-6, 1-7, 1-8 | 8 | 10 | — | died mid-read | **OPEN** — needs validation |
| E | 1-9, 1-10 | 9 | 10 | — | died mid-read | **OPEN** — needs validation |
| F | SC-2 Q1-12 | 9 | 10 | — | died mid-read | **OPEN** — needs validation |
| G | A1, B, C | 8 | 10 | — | **10 PASS** | **ACCEPTED** |
| H | D, E, F | 9 | 9 | — | — | **OPEN** — fix APPLIED, needs re-judge |
| I | G, H, I, J | 8 | 10 | — | died mid-read | **OPEN** — needs validation |
| J | K, L | 8 | 9 | — | — | **OPEN** — fix APPLIED, needs re-judge |
| K | M, N | 8 | 10 | — | died mid-read | **OPEN** — needs validation |

## Outstanding work, in order

1. ~~Fix J~~ **DONE** (applied by hand, not by a subagent). 17 prose lines
   converted to \tfrac; the 11 remaining \dfrac are exactly the 3 restated
   Question lines (which mirror the worksheet's own built-up fractions) plus the
   4 \checked and 4 \finalans lines. Original spec was: Fraction-size sweep was incomplete: prose inside
   numbered work-steps and Important-words bullets still uses \dfrac while
   paragraph prose now uses \tfrac, so the same expression appears at two sizes
   within a few lines. Rule: \tfrac for ALL running prose incl. list items and
   bullets; \dfrac only for standalone displays and the \checked / \finalans
   lines. Known loci: K4 "Why this makes sense" + step 4; K5 bullet 2 + step 4;
   K6 bullets 1-2 + steps 1-3; K7 steps 1-3; K8 steps 1-5.

2. ~~Fix H~~ **DONE** (applied by hand). All 7 answer slots added; compiles
   clean at 52 pages. Original spec was: Seven restated Questions drop the worksheet's answer
   blank: D1 "9 x 6 =", D2 "63 / 9 =", E1 "Greater: 5/8 or 0.61?", E2 "? =",
   E4 "x =", F5 "6y - 2y =", F6 "5n - 3 =". Append \ansblank to each (E1 takes
   \blank[2.4cm]). Source lines cited by the judge: g6e_H.tex 11, 45, 156, 536,
   572 plus the E2/E4 question lines. NOTE: this judge REVERSED its round-1
   clearance here and explained why — it had hypothesised a house convention of
   omitting the rule after a terminal "=" and tested it only against K1; B1, C7
   and M1-M6 falsify it.

3. **Re-judge A.** Its regression fix (restored stem sentence + two \tfrac
   lines) is applied and committed but never scored. NOTE: the original slice-A
   judge's transcript is UNRECOVERABLE ("No transcript found"), so the
   same-judge guarantee is broken for A. A replacement judge was spawned and
   also died. Any new slice-A judge is a fresh judge, not a continuation —
   this must be disclosed, not papered over.

4. **Validation passes** for B, C, D, E, F, I, K (all at 10/10 round 2), then
   for A, H, J once they reach 10/10.

## Judge IDs (resume with SendMessage to keep the same judge)
B aa7e3af94be7b1a89 · C abfbf5c6637f7da92 · D ad779e8d5b10441bf
E a847f037d121c80df · F ae3a1736191bc44c9 · G a7cd61021cda9a927 (done)
H ad58d8324d5a982a2 · I a9b3a1f3921639dfa · J ac5f2552e85c47122
K a4fbd1ccbe98afc27 · A — transcript lost, must be a new judge

## What the loop caught that the earlier passes did not
- A fabricated 4.5 m number, invented "board game"/"turns" context, invented
  "Two birds are flying in the sky" openers.
- A logged correction reported as applied that was not ("written |x|").
- A regression introduced BY a fix (deleted stem sentence).
- Two fixes that moved a defect rather than closing it (blank block, crowding).
- Root causes behind symptom clusters (\degF eating spaces; heading reserve).
- A misaligned decimal grid and a doubled arrowhead, both found by measurement.
