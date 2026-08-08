# T1-2 cold validation report (independent second read)

SLICE: T1-2 (topic-1-2-independent-practice-accuracy-check-qti)   SCORE: 10/10
ITEMS WORKED: 6 of 6     (none skipped)

Shape A confirmed. Mathematics re-derived from scratch on all six items, keyed
and non-keyed choices alike, before reading `T1-2-r1.md` / `T1-2-r2.md`.

Sources used directly:
- `.../scratchpad/Topic1IndependentPractice.pdf`, page 1, **rendered** at 200 dpi
  (`pdftoppm`) — the vinculum on `0.27` and `0.6` and the built-up fractions
  `x/y`, `a/b`, `2/3` were read off the image, not off `pdftotext`, which drops
  the overline entirely and prints a bare `0.27`.
- `docs/math-corrections/pdf/Topic1Part1Solutions.pdf`, Lesson 1-2, pp. 1-2.
- `docs/math-corrections/pdf/Topic1Part2Solutions.pdf`, Lesson 1-2, pp. 1-2.
- Raw XML only:
  `pkg/topic-1-2-independent-practice-accuracy-check-qti/topic_1_2_independent_practice_accuracy_check/topic_1_2_independent_practice_accuracy_check.xml`
  (sha256 `9c99078b7f94279269549be6154c5698c3879b6f522dd737b9f7a7fc8aece787`).
  `slices/T1-2.json` was **not** used as evidence — see the methodology note.

Overline settled on the render: on Part 1 Q3 the bar spans **both** digits of
`27`, so the value is `0.272727...`, not `0.2777...`. This matters — under the
`0.27` reading with the bar on the 7 alone the value would be `25/90 = 5/18`
and the entire keyed set of that item would be wrong. It is not; the QTI's
`\(0.\overline{27}\)` is faithful. Part 2 Q3's bar sits on the single `6`, and
the assignment's own stem corroborates it by writing `it equals 2/3`.

## DEFECTS

None. No defect stands under any of the seven criteria.

## MATHEMATICS WORKED FROM SCRATCH

**Part 1 Question 1** — 3 out of 8. `3 / 8 = 0.375` exactly (`3.000 / 8`:
30/8 = 3 r 6, 60/8 = 7 r 4, 40/8 = 5 r 0). Part 1 key: `Answer: 0.375`.
Keyed `correct_1 = 0.375`. Agrees.
Non-keyed worked: `-0.375` false (3/8 > 0); `1.375 = 11/8`; `-0.625 = -5/8`;
`2.375 = 19/8`; `-1.625 = -13/8`; `0.000` false (3/8 != 0); `0375` is the
integer 375, no decimal point, not equal to 0.375. Seven false. No equivalent
form of the answer (`3/8`, `.375`, `0.3750`, `37.5%`) appears unkeyed.

**Part 1 Question 2** — `x/y`, `y != 0`, which outcome is NOT possible.
Long division of an integer by `y` produces remainders drawn from
`{0, 1, ..., |y|-1}`, a finite set, so within at most `|y|` steps a remainder
either reaches 0 (terminating) or repeats a previous remainder (repeating).
"Neither terminates nor repeats" is therefore impossible. That is the
assignment's option C, and Part 1 key: `Answer: C`. Keyed `correct_1` is
verbatim the assignment's option C. Agrees.
Non-keyed worked: `The decimal terminates (stops).` possible, e.g. 1/8 = 0.125;
`The decimal repeats a pattern.` possible, e.g. 1/3 = 0.333...;
`All listed choices are correct.` false; `No listed choice can be correct.`
false, `correct_1` is; `More than one listed choice is correct.` false, exactly
one impossible outcome is listed; `The denominator alone determines answer.`
false, see the two-reading kill below; `The sign does not matter here.` see the
weaker-case ruling below. All seven false.

**Part 1 Question 3** — `0.272727...`. Let `x = 0.272727...`. Then
`100x = 27.272727...`, so `100x - x = 27`, i.e. `99x = 27` and
`x = 27/99 = 3/11` (divide by gcd 9). Check back: `3/11 = 0.2727...`. Part 1
key: `Answer: Jordan; 0.27bar = 3/11`, with the worked line `99x = 27`.
Keyed set `{Jordan is correct: a repeating decimal is rational; 0.272727...
equals 3/11; If x = 0.272727..., then 99x = 27}` reproduces the key's verdict,
its fraction and its equation. The key writes no "or"-alternate, so there is no
all-or-nothing splitting hazard under criterion 4.
Non-keyed worked: `A decimal must end to be rational.` false, 1/3 = 0.333... is
rational and never ends; `Every nonterminating decimal is irrational.` false,
same counterexample; `0.272727... equals 27/100.` false, 27/100 = 0.27
terminating, and the difference is `3/11 - 27/100 = (300 - 297)/1100 = 3/1100`;
`If x = 0.272727..., then 100x = 27.` false, `100x = 27.272727...`, off by
exactly `0.272727... = 3/11` — the off-by-one-step error, correctly a
distractor; `Casey is correct because the decimal has no last digit.` false.
All five false.

**Part 2 Question 1** — 5 out of 8. `5 / 8 = 0.625` exactly (50/8 = 6 r 2,
20/8 = 2 r 4, 40/8 = 5 r 0). Part 2 key: `Answer: 0.625`. Keyed
`correct_1 = 0.625`. Agrees.
Non-keyed worked: `-0.625` false; `1.625 = 13/8`; `-0.375 = -3/8` (the Part 1
value negated); `2.625 = 21/8`; `-1.375 = -11/8`; `0.000` false; `0625` is the
integer 625. Seven false. No equivalent form (`5/8`, `.625`, `0.6250`) unkeyed.

**Part 2 Question 2** — `a/b`, which statement about the result is always right.
Same finite-remainder argument: the decimal always terminates or repeats.
That is the assignment's option B, and Part 2 key: `Answer: B` (the key names
the counterexamples itself: A fails for 1/3, C fails for 1/2). Keyed
`correct_1` is verbatim the assignment's option B. Agrees.
Non-keyed worked: `The decimal will eventually terminate (stop).` false,
1/3 never terminates; `The quotient a/b never terminates or repeats.` false,
1/2 = 0.5 terminates; `All listed choices are correct.` false;
`No listed choice can be correct.` false; `More than one listed choice is
correct.` false, exactly one is always-right; `The denominator alone determines
answer.` false under both readings — (i) the value of a/b plainly depends on a
(1/6 vs 5/6), and (ii) even the narrower reading "the denominator decides
whether it terminates" fails on an unreduced fraction: `3/6 = 0.5` terminates
while `1/6 = 0.1666...` repeats, same denominator 6, so it is the *reduced*
denominator, not b, that decides; `The sign does not matter here.` see below.
All seven false.

**Part 2 Question 3** — `0.666...`. Let `x = 0.666...`. Then `10x = 6.666...`,
so `9x = 6` and `x = 6/9 = 2/3`. Part 2 key: `Answer: Mia; 0.6bar = 2/3`, with
the worked line `9x = 6`. Keyed set `{Mia is correct: a repeating decimal is
rational; 0.666... equals 2/3; If x = 0.666..., then 3x = 2}`.
`3x = 2` is true: `3 * (2/3) = 2`. It is `9x = 6` divided through by 3, i.e. the
same equation in lowest terms, and it supports the claim exactly as the stem
asks. Agrees with the key's verdict and fraction.
Non-keyed worked: `A decimal must end to be rational.` false;
`Every nonterminating decimal is irrational.` false;
`0.666... equals 6/10.` false, 6/10 = 0.6 terminating, and
`2/3 - 3/5 = (10 - 9)/15 = 1/15`; `If x = 0.666..., then 100x = 6.` false,
`100x = 66.666...`; `Lee is correct because the decimal has no last digit.`
false. All five false.

Note recorded, not a defect: `0.666... equals 2/3` is asserted in the stem
itself ("Mia says 0.6bar is rational because it equals 2/3"). Criterion 2's
"statement given as true in the stem" clause bites only on *unkeyed* choices;
this one is keyed, so a student who reads the stem and selects it is scored
correct. The parallel Part 1 stem withholds the fraction, which makes P1Q3 the
harder of the two, but that asymmetry is inherited verbatim from the assignment
and is not the package's to fix.

## WEAKER CASES — recorded separately and ruled, per criterion 2

1. `The sign does not matter here.` (`1_2_part_1_question_2_wrong_7` and
   `1_2_part_2_question_2_wrong_7`). This is the one genuinely arguable choice
   in the slice, and it is a "true statement answering a different question"
   candidate rather than an equivalent-form candidate. Under the reading
   "the sign has no bearing on *whether* the decimal terminates or repeats" the
   statement is true. **Ruled not a defect**, on two independent grounds.
   (a) Referent. Part 1 Q2 asks which *outcome of the long division* is not
   possible; "the sign does not matter" is not an outcome at all, so it cannot
   be the impossible one. Part 2 Q2 asks which statement *about the result* is
   always right; about the result the sign manifestly does matter, since
   `-1/2 = -0.5` and `1/2 = 0.5` are different results. Read literally against
   the stem's own referent — the reading criterion 3 mandates for
   `-96 feet below sea level` — the choice is false in both items.
   (b) The word `always`. For the statement to be always right, `here` needs a
   fixed referent, and the only referent the stem supplies is the result.
   This ruling is load-bearing: it is what keeps `More than one listed choice is
   correct.` (`wrong_5`) false in both Q2 items. Had I ruled `wrong_7` true,
   `wrong_5` would have become true as well and both Q2 items would carry two
   true-but-unkeyed choices. Ruling it false is self-consistent; ruling it true
   is not, since `wrong_5` would then be true and unkeyed by the same act.

2. P2Q3 keys `3x = 2` where the key PDF derives `9x = 6`. **Ruled not a
   defect.** `3x = 2` is true and is the key's equation in lowest terms;
   `9x = 6` is not among the eight choices, so no student who derived the key's
   form is left with nothing to select — they select the equivalent one, which
   is presented to them and is checkable in one step. Criterion 5 asks whether
   the keyed set is *producible from the assignment*: the stem hands the student
   `x = 2/3`, from which `3x = 2` follows immediately. A future fixer should not
   "correct" this to `9x = 6`; it is right as written, and changing it would
   break nothing but would gain nothing either.

3. Both Q2 items carry eight choices where the assignment prints only options
   A/B/C. **Ruled not a defect** under criterion 5: the keyed choice is verbatim
   the assignment's own lettered option (C in Part 1, B in Part 2), matching
   `Answer: C` and `Answer: B`; every one of the five added choices is false;
   and the >=8-choice count is Shape A's mandated design.

4. The assignment's global direction says "Round to two decimal places," which
   would give 0.38 and 0.63 on the two Q1 items. **Ruled not a defect.** Both
   answer keys write the exact three-place values 0.375 and 0.625, criterion 4
   binds the QTI to the key, and neither item offers a rounded distractor
   (`0.38`, `0.63`) that a rounding student could be trapped by. The direction
   governs answers that require rounding; these terminate exactly.

5. Choice glosses. P1Q2 `wrong_1` reads `The decimal terminates (stops).` where
   the assignment's option A reads `The decimal terminates.`; P2Q2 `wrong_1`
   reads `...terminate (stop).` for `...terminate.` **Ruled not a defect** —
   the parenthetical is a synonym gloss, changes no truth value, and leaves each
   option recognisable as its lettered original, so criterion 5's mapping from
   the assignment's A/B/C to the QTI choices survives intact.

## STEM FIDELITY, ITEM BY ITEM (criterion 1)

Checked against the rendered assignment, Lesson 1-2, the part named in each
item title. Part 1 numbers were checked only against the Part 1 column and Part
2 numbers only against the Part 2 column.

| item | assignment | verdict |
|---|---|---|
| P1 Q1 | 3 out of 8, basketball | word-for-word |
| P1 Q2 | `x/y (where y != 0)`, "Which outcome is NOT possible?" | equivalent (parenthetical rendered as a comma clause) |
| P1 Q3 | Jordan / Casey, `0.27bar` | word-for-word |
| P2 Q1 | 5 out of 8, soccer | word-for-word |
| P2 Q2 | `a/b`, "Which statement is ALWAYS right?" | equivalent; QTI adds "of the following statements about the result", which narrows the referent and helps rather than harms |
| P2 Q3 | Mia / Lee, `0.6bar`, `2/3` | word-for-word |

No Part 1 number appears in a Part 2 stem or the reverse. The 3/8-vs-5/8 and
27-vs-6 pairs are the obvious cross-contamination risk in this slice and both
are clean.

## STRUCTURE (criterion 6) — parsed, not regexed

Parsed with ElementTree; `<not>` subtrees were collected first and their
`<varequal>` idents excluded before reading the bare requirements, so the
flat-regex trap the rubric names does not apply. All six items:

- exactly one `<respcondition>`; `maxvalue="100"`, `minvalue="0"`,
  `setvar action="Set" varname="SCORE">100`; `respident="response1"` throughout
- required ident set == the `correct_*` ident set, exactly
- negated ident set == the `wrong_*` ident set, exactly
- 8 choices each (1+7, 1+7, 3+5, 1+7, 1+7, 3+5)
- no two choices in an item share visible text
- `original_answer_ids` matches the `response_label` render order exactly

File re-parses as well-formed XML. `imsmanifest.xml` resource plus dependency
pair resolves to the two files that exist; `points_possible` is 6.0 in both
`assessment_meta.xml` locations, matching 6 items at 1 point. No `src=`
attribute anywhere in the package, so the `$IMS-CC-FILEBASE$` import trap does
not arise here.

## MARKUP (criterion 7) — the repaired criterion, re-tested

- `$` characters in the whole file: **0**.
- `\(` count 6, `\)` count 6, and per stem the tokens alternate open-close with
  depth never exceeding 1 and returning to 0: P1Q2 `\(\dfrac{x}{y}\)` and
  `\(y\neq 0\)`; P1Q3 `\(0.\overline{27}\)`; P2Q2 `\(\dfrac{a}{b}\)`;
  P2Q3 `\(0.\overline{6}\)` and `\(\dfrac{2}{3}\)`. P1Q1 and P2Q1 carry no math.
- LaTeX brace balance per stem: (0,0), (2,2), (1,1), (0,0), (2,2), (3,3) — every
  `\overline{...}` and `\dfrac{...}{...}` closed.
- `Canvas accuracy check` occurs exactly once per stem, six times in the file.
  The canonical block appears **byte-exact 6 times** and every stem *ends* with
  it. The non-canonical wording `part of a correct solution` occurs **0** times,
  which confirms the fixer deleted the stray block and kept the canonical one
  rather than the reverse.
- Escaping is single, not double: `amp;lt;` occurs 0 times.

## POINT 4 OF THE COLD BRIEF — "nothing outside the repair moved"

Established on a **genuine pre-fix before-image**, which r2 did not have.

Methodology note, and it is a real hole in r2's evidence rather than a defect in
the slice. `T1-2-r2.md` lines 76-77 assert that `/tmp/qtiwork/slices/T1-2.json`
"was built from the pre-fix package and therefore serves as the before-image."
That is false. The package XML was written at `2026-08-06 00:02:03`; every file
in `slices/` carries mtime `2026-08-06 00:07`, five minutes later, and the cold
brief states outright that `slices/*.json` "has been rebuilt from the repaired
packages." r2's "NO MATHEMATICS MOVED" table therefore compares the repaired
package against a cache derived from that same repaired package. It would have
returned "identical" on all six rows whether or not the fixer moved
mathematics, so it carried no information. r2's conclusion happens to be right,
but it was not evidenced.

Re-established properly. `/tmp/qtiwork/corpus_BROKEN.json` has mtime
`2026-08-05 23:57`, five minutes *before* the fix, and is a true before-image.
Its stem field is untrustworthy (it is the file that carries the
unescape-before-strip truncation bug the brief warns about), but that bug
affects only stem text; the `choices`, `required` and `negated` fields are
unaffected. Diffing its six T1-2 records against the current package:

| item | choice idents + visible text | required list | negated list |
|---|---|---|---|
| Part 1 Question 1 | identical | identical | identical |
| Part 1 Question 2 | identical | identical | identical |
| Part 1 Question 3 | identical | identical | identical |
| Part 2 Question 1 | identical | identical | identical |
| Part 2 Question 2 | identical | identical | identical |
| Part 2 Question 3 | identical | identical | identical |

Ordered exact string equality on all three lists in all six items. The repair
was stem-only, as claimed.

This also disposes of cold-brief points 1 and 2 by making them vacuous:
**no choice was replaced in this slice at all**, so there is no replacement to
test for being genuinely false and none to test for colliding with another
choice's text or value. The displaced-defect failure mode the round exists to
catch cannot have occurred here, because nothing in the answer space was
touched.

Deliverable check: `staged/topic-1-2-independent-practice-accuracy-check-qti.zip`
unzips byte-identical to the audited `pkg/` tree (`diff -r` clean), so the thing
that ships is the thing I scored.

## CANDIDATES RULED ON

- r1's four markup defects (P1Q3 bare `$...$`; P1Q3 duplicated instruction
  block; P2Q3 interleaved `$0.\overline{6}\( ... \)\dfrac{2}{3}$`; P2Q3
  duplicated instruction block) -> **all four CONFIRMED as having been real,
  and CONFIRMED CLOSED.** Zero `$` remain, both Q3 stems carry two properly
  nested `\(...\)` pairs, and each stem holds exactly one canonical
  instruction block.
- r1's ruling that `The sign does not matter here.` is not a defect ->
  **CONFIRMED**, reached independently before reading r1, and on the added
  self-consistency ground that ruling it true would make `wrong_5` true too.
- r1's ruling that P2Q3's `3x = 2` is correct and must not be "fixed" to
  `9x = 6` -> **CONFIRMED**, independently.
- r1's claim that the audit found no mathematical defect -> **CONFIRMED**,
  independently, by re-deriving all 48 choices across the 6 items from the
  rendered assignment and both answer keys rather than by re-reading r1.
- r2's claim that `slices/T1-2.json` is a pre-fix before-image ->
  **REFUTED** on file mtimes and on the cold brief's own statement. The
  underlying conclusion is nonetheless correct, re-established above against
  `corpus_BROKEN.json`. No score impact: it is a flaw in r2's reasoning, not a
  defect in the package.

## CLEAN

- Part 1 Question 1 — no defect
- Part 1 Question 2 — no defect
- Part 1 Question 3 — no defect
- Part 2 Question 1 — no defect
- Part 2 Question 2 — no defect
- Part 2 Question 3 — no defect

All six items worked. All 48 choices (10 keyed, 38 non-keyed) evaluated
individually. No defect stands under criteria 1 through 7.

SCORE: 10/10
