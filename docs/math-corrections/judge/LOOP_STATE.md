# Judge loop — state at session limit (resets 2:50pm UTC)

Rule: a slice is ACCEPTED only on TWO CONSECUTIVE 10/10 from its judge
(round-N pass, then a cold adversarial validation pass).

| Slice | Content | R1 | R2 | R3 | Validation | Status |
|---|---|---|---|---|---|---|
| A | 1-1 Q1-4, 1-2 Q1-3 | 7 | 8 | 9→10 | **10 PASS** | **ACCEPTED*** (replacement judge) |
| B | SC-1, 1-3 | 8 | 10 | — | **10 PASS** | **ACCEPTED** |
| C | 1-4, 1-5 | 7 | 10 | — | **10 PASS** | **ACCEPTED** |
| D | 1-6, 1-7, 1-8 | 8 | 10 | — | **10 PASS** | **ACCEPTED** |
| E | 1-9, 1-10 | 9 | 10 | 9→10 (r4→r5) | **10 PASS** | **ACCEPTED** |
| F | SC-2 Q1-12 | 9 | 10 | — | **10 PASS** | **ACCEPTED** |
| G | A1, B, C | 8 | 10 | — | **10 PASS** | **ACCEPTED** |
| H | D, E, F | 9 | 9 | 9→10 | **10 PASS** | **ACCEPTED*** (validation instance had no round-4 memory) |
| I | G, H, I, J | 8 | 10 | 10 | **10 PASS** | **ACCEPTED*** (re-judged after revocation; no shared memory) |
| J | K, L | 8 | 9 | 10 | **10 PASS** | **ACCEPTED*** (validation instance had no round-4 memory) |
| K | M, N | 8 | 10 | — | **10 PASS** | **ACCEPTED** |

## TOOLING BUG FOUND BY THE JUDGES — the CJK guard failed open

The guard I wrote into WORKER_DIRECTIVES was
`grep -nP '[\x{4e00}-\x{9fff}...]'`. On this machine that errors with
"character code point value in \x{} or \o{} is too large", prints nothing,
and exits 0. It reads as "clean" while checking nothing.

Verified by planting a real CJK character in a file: the command missed it.
`LC_ALL=C.UTF-8 grep -P` catches it; a Python regex catches it. The directive
now mandates the Python check and documents the trap, because a guard that
fails open is worse than no guard — it manufactures false confidence.

Judges D and F both reported this independently. Judge D also caught that its
first run had produced a FALSE POSITIVE (17 .tex files flagged) before it
switched to Python and got the true answer of zero.

## Slice E — validation overturned its own round-2 pass

Rounds 1-2 cleared the p.35 number-line figure by LOOKING at it (150/400 dpi).
The validation round pulled glyph coordinates and scanned at 600 dpi and found
the teal dotted leader lines start at a hard-coded x=296.46pt, which sits INSIDE
the label glyph boxes, so they cross "-120" and "450" at mid-glyph height and
read as a strikethrough. Root cause: one shared start x sized for the
3-character "450", never widened for the 4-character "-120" (whose math minus is
wider still).

Note what this is: the EARLIER fix for this same figure did clear the
strikethrough on "sea level: 0" - the judge confirmed that label is now at zero
teal pixels. The defect did not return; it MIGRATED to two neighbouring labels
the fix never measured. Third time in this run a repair has moved a defect
instead of closing it.

The fix in flight anchors each leader to its own label node's east edge rather
than raising the magic number, so the geometry survives the next label that gets
wider, and must prove it by measuring teal pixels in all five label boxes -
including the three already clean.

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


## Acceptance is bound to a build hash

Judge A2 raised this and it is right. A slice is accepted against the PDF it was
measured on. Every later rebuild of that document invalidates the measurement
evidence, even when the slice's own text is untouched — page numbers and glyph
coordinates move.

Current builds at the time of writing:
- Topic1ExplanationsPart1.pdf — slices A, B, C, D, E, F
- 6thGradeReviewExplanations.pdf — slices G, H, I, J, K

Consequence: while slice E is still in its loop, any further E fix rebuilds
Topic1ExplanationsPart1.pdf and technically stales the acceptances of A, B, C,
D and F. The same holds for 6thGradeReviewExplanations.pdf while H is open.

This does NOT mean re-running every judge on every rebuild — the accepted
slices' source text is unchanged and a text diff can prove it. But an acceptance
should be recorded against a hash, and a rebuild that alters an accepted slice's
TEXT (not merely its pagination) reopens that slice.

* A is marked ACCEPTED* because both of its passing rounds came from a
  replacement judge. Slice A cannot satisfy the same-judge rule: the original
  judge's transcript is unrecoverable. The replacement disclosed this at the top
  of every report rather than presenting itself as a continuation.


## Systemic finding: 22 restatements were missing the worksheet's answer blanks

The 6th Grade companion restates each worksheet item before explaining it. The
revised worksheet prints a fill-in rule on EVERY item. 22 restatements across
three slices dropped it.

- Judge H found 7 (D1, D2, E1, E2, E4, F5, F6) in round 2, reversing its own
  round-1 clearance and explaining why: it had hypothesised a house convention
  of omitting the rule after a terminal "=" or a complete "?" and tested that
  hypothesis only against K1. B1, C7 and M1-M6 falsify it.
- Judge J found 10 more (K1-K6, K9-K11, L1) in its VALIDATION round, having
  passed the slice at 10/10 one round earlier - and flagged a further 12 in
  slice I, which it does not own.

Judge J's method is why it saw what others did not: it measured every rule wider
than 35pt with PyMuPDF get_drawings() across all 69 restatements - 47 present,
22 absent - rather than reading for it. Its clinching evidence is internal:
K10 and N5 are character-identical items; N5 renders a blank, K10 does not.

**Slice I's acceptance is REVOKED.** It passed two rounds carrying this defect.
Its judge was not careless - it recomputed all arithmetic, measured glyph
clearances to 1.3pt and inspected arrowheads at 600 dpi. It simply never asked
whether every restatement carried a blank. A question nobody asks does not get
answered by care.

## Open fidelity gap, unowned by any slice

The revised worksheet sets its section headings as navy banner boxes with white
text on light-blue rounded panels. The rebuilt worksheet uses plain bold
headings. The rebuild agent disclosed this at the time ("Not reproduced: the
source's colored banner boxes") and it was relayed in a summary rather than
logged as a defect. It is a fidelity defect and is recorded here as one.


## Broken same-judge guarantees: slices A, H and J

Slice H's validation instance reported that it had NO record of its own round 4 -
its prompt arrived labelled "Round 1". Same agent ID, but the transcript did not
carry. It disclosed this at the top of its report rather than writing as though
it remembered, and noted that for a VALIDATION round a cold read is a benefit
rather than a harm, which is fair.

Slice J's validation instance reported the same thing, in the same words:
no round-4 transcript, therefore a true cold read rather than a recollection.

So A, H and J are all ACCEPTED* : two 10/10 rounds each, but not from a judge
with continuous memory across them. FOUR of eleven slices could not satisfy the
same-judge rule. All four are marked, none is dressed up.

Slice I is the sharpest case. A round-3 report WAS produced under its agent ID
and delivered - a full 69-item audit. Its validation instance then stated
plainly: "I have no round 3 ... Whatever round-3 work is being credited to me,
it is not mine, and I did not lean on it." Both statements are true: the report
exists and came from that agent ID; the later instance has no memory of it. The
work was not disowned, the memory was simply gone.

That the two independent derivations AGREE - both concluded A1, H6 and H7
correctly carry no answer blank because their number lines are the answer space,
and both audited all 69 items - is worth more than a single judge confirming
itself would have been.

The honest reading is that transcript persistence across long runs is not
reliable enough to guarantee "same judge" as specified. What the loop actually
delivered on those three slices is two independent 10/10 reads, which is a
different - and for a validation pass arguably stronger - property than the one
requested. It is not the property that was requested.

## Methodological finding from slice H: -layout extraction inverts fractions

`pdftotext -layout` renders a built-up fraction with numerator and denominator
transposed. On the authoritative worksheet, E2 extracts as "47 = 21 / ?" and E4
as "56 = 18 / x". Read literally, both look like the companion has corrupted the
problem. By span coordinates the truth is the opposite: E2 numerator "?" sits at
y=403.7 above denominator "21" at y=411.1, i.e. 4/7 = ?/21, and the companion is
correct.

A judge trusting -layout here would have failed a correct item as a fatal
fidelity defect. Every fraction claim in this corpus must be settled by glyph
y-coordinates, never by extracted text order.


## Detector paradoxes, and the rule that resolved them

Instrument errors outnumbered document defects in the late rounds. Four were
found, every one capable of producing a confident wrong answer:

1. CJK guard failed OPEN — `grep -P` errored, printed nothing, exited 0.
2. The same guard fails CLOSED on PDFs — compressed-stream bytes decode to
   stray CJK, false-positiving 6 of 6 files.
3. `\rule` emits an `l` line primitive, not an `re` rectangle. Counting `re`
   reports every answer blank as missing.
4. `pdftotext -layout` TRANSPOSES built-up fractions, so a correct 4/7 = ?/21
   extracts as "47 = 21 / ?" and reads as corruption.

The working rule, arrived at independently by judge J: when a measurement
contradicts a visible fact, suspect the instrument first, then confirm along a
second and third independent path (bitmap render, source, coordinates). Judge J
hit two such paradoxes in one round and resolved both correctly.
