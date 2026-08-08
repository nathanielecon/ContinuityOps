# Cold validation — T1-7 + T1-10

SLICE: T1-7+10          SCORE: 10/10
ITEMS WORKED: 4 of 4     (none skipped)

Read cold from the raw XML at
`/tmp/qtiwork/pkg/topic-1-7-independent-practice-accuracy-check-qti/` and
`/tmp/qtiwork/pkg/topic-1-10-independent-practice-accuracy-check-qti/`.
`/tmp/qtiwork/slices/*.json` and `/tmp/qtiwork/corpus.json` were not consulted.
My own extractor strips real tags first (`</?[a-zA-Z][^>]*>`) and unescapes
after; every value that could depend on layout was settled by rendering the PDF
page at 150 dpi, not by `pdftotext` order.

Shape identified before scoring: **Shape A** on all four items —
`multiple_answers_question`, `respident="response1"`, `rcardinality="Multiple"`,
idents `..._correct_N` / `..._wrong_N`, one `<respcondition>` with
`maxvalue="100"` and `<setvar action="Set" varname="SCORE">100</setvar>`,
8 choices each. Shape A criteria applied.

Nothing in this slice was repaired. `FIXES_APPLIED.txt` records edits to T1-6
and T1-8 only; all six files in my two packages still carry the pristine
`2026-01-01T00:00:00` mtime, so there is no repair to test for displacement.
The slice therefore stands on this reading and the first judge's, and on nothing
else.

---

## DEFECTS

  (none)

---

## CANDIDATES RULED ON

  **1-10 P1Q1 `1_10_part_1_question_1_wrong_4` = "450 + (-120) = 330"**
  -> **REFUTED** (not a defect). Recorded explicitly as criterion 2's weaker
  case and not merged with the true-equivalent-form list.

    The sentence is arithmetically true: 450 + (-120) = 330. It answers a
    different question. The stem asks for the total vertical distance between a
    hiker at +450 ft and a hiker at -120 ft, which is |450 - (-120)| = 570 ft;
    Part 1 key PDF p.5 reads "We Solve: 450 - (-120) = 450 + 120 = 570 /
    Answer: 570 feet" (read rendered).

    Three reasons the criterion-2 harm mechanism cannot fire here:

    1. The instruction is "Select every choice that belongs in complete correct
       answer", not "select every true sentence". The same instruction block
       appears once and identically on all 88 Shape A items, so the reading is
       settled corpus-wide, not by this item alone.
    2. The choice asserts the value 330, which contradicts the answer the
       student computed. A student who reasons correctly to 570 has an explicit
       reason to reject it. The same misconception already sits in the list in
       plain value form as `wrong_1` = "330 feet", and both are negated in the
       scoring tree — the two are consistent with each other, so there is no
       contradiction a correct reasoner could be caught by.
    3. Stronger than (2): this stem asks for a **value**, not an expression.
       Contrast Lesson 1-4, whose stems say "Write at least two expressions" and
       whose items legitimately key expressions. No expression belongs in this
       item's answer at all, so the correct alternative expression
       `450 - (-120) = 570` is rightly absent from the list and its
       wrong-operation twin cannot belong either. The choice is unselectable by
       correct reasoning on two independent grounds.

    Contrast recorded for the next reader: had `450 - (-120) = 570` been present
    and unkeyed, that *would* be a criterion-2 defect ("a correct alternative
    expression"). It is not present. Verified by working all 8 choices.

  **1-10 P2Q1 `1_10_part_2_question_1_wrong_4` = "320 + (-85) = 235"**
  -> **REFUTED** (not a defect). Same analysis, same three grounds.
  320 + (-85) = 235 is true arithmetic; the distance is |320 - (-85)| = 405 ft.
  Part 2 key PDF p.5, rendered: "320 - (-85) = 320 + 85 = 405 / Answer: 405
  feet". `wrong_1` = "235 feet" carries the same misconception in value form and
  is likewise negated. `320 - (-85) = 405` is absent from the choice list.

  **The first judge's 10/10 on this slice** -> **CONFIRMED**, independently and
  not by ratification. Every one of the 4 keyed and 28 non-keyed choices was
  recomputed below from the stem, and criteria 1, 4, 5, 6 and 7 were re-tested
  against sources the first report only asserted (rendered assignment pages,
  both rendered key pages, the Explanations PDF, the staged zips). Two of its
  arguments I replaced with stronger ones — see criterion 1 and the third ground
  above.

---

## MATHEMATICS, WORKED FROM THE STEM

### 1-7 Part 1 Question 1

Stem: `Evaluate: \(-0.5(10 + 6) =\)`
Assignment, rendered p.3, Lesson 1-7 Part 1: "Q1. Evaluate: -0.5(10 + 6) =" —
verbatim.

PEMDAS: 10 + 6 = 16, then -0.5 x 16 = -8. Key: Part 1 Solutions rendered p.4,
"We Solve: -0.5(10 + 6) = -0.5 x 16 = -8 / Answer: -8". Third path:
Topic1ExplanationsPart1.pdf, "Checked answer: -8", "Final answer: -8".

Keyed `correct_1` = "-8". True, and agrees with the key.

Every non-keyed choice worked:

| ident | text | value / why false |
|---|---|---|
| wrong_1 | 8 | sign dropped; 8 != -8 |
| wrong_2 | -7 | off by one |
| wrong_3 | -9 | off by one |
| wrong_4 | -6 | off by two |
| wrong_5 | -10 | -0.5 x 20, wrong parenthesis sum |
| wrong_6 | 0 | zero-product error |
| wrong_7 | -80 | -0.5 x 160, decimal misplaced |

None equals -8; none is an equivalent form, restated value, alternative
expression, or unit variant of -8. Also checked for a *defensible alternative
reading* of the expression that would make a distractor true:
`-0.5 x 10 + 6 = 1` and `-0.5 + 10 + 6 = 15.5` are the two misreadings
available, and neither 1 nor 15.5 appears in the list. No distractor is
reachable by any correct chain of reasoning.

### 1-7 Part 2 Question 1

Stem: `Evaluate: \(-0.2(15 + 5) =\)` — verbatim against rendered assignment p.3
Part 2. 15 + 5 = 20, -0.2 x 20 = -4. Part 2 Solutions rendered p.4:
"-0.2(15 + 5) = -0.2 x 20 = -4 / Answer: -4". Keyed `correct_1` = "-4". Agrees.

Non-keyed: "4" (sign dropped), "-3", "-5", "-2", "-6" (off by one/two),
"0", "-40" (-0.2 x 200, decimal misplaced). All false, none equivalent to -4.
Misreadings `-0.2 x 15 + 5 = 2` and `-0.2 + 15 + 5 = 19.8` produce values absent
from the list.

### 1-10 Part 1 Question 1

Stem: "Two people are hiking. The first person climbs to the top of a peak that
is 450 feet above sea level. The second person descends into a valley that is
120 feet below sea level. What is the total vertical distance between the two
hikers?"

Positions +450 and -120. Distance = |450 - (-120)| = 450 + 120 = 570 ft.
Key, rendered p.5: "Answer: 570 feet". Explanations PDF: "Checked answer: 570
feet", and explicitly "Distance is never negative", "Absolute value of 570 is
still 570".

Keyed `correct_1` = "570 feet". True, agrees with the key including the unit
word.

Every non-keyed choice worked:

| ident | text | why false |
|---|---|---|
| wrong_1 | 330 feet | 450 + (-120); the signed sum, not the distance |
| wrong_2 | 570 miles | 570 mi = 3,009,600 ft. Same numeral, different quantity — this is **not** criterion 2's "right value in different units". The true unit-variant, 190 yards, is absent from the list; I checked for it specifically. |
| wrong_3 | -570 feet | a distance is non-negative; the key and the explanation both say so |
| wrong_4 | 450 + (-120) = 330 | ruled on above |
| wrong_5 | 570 meters | 570 m ~ 1,870 ft; same reasoning as wrong_2 |
| wrong_6 | 571 feet | off by one |
| wrong_7 | 569 feet | off by one |

Criterion 3 double-sign check on the keyed choice: "570 feet" carries no
direction word, so the `-96 feet below sea level` construction that broke T1-8
and T1-6 cannot occur here. The signed form appears only as `wrong_3`, negated.

### 1-10 Part 2 Question 1

Stem: ridge 320 ft above sea level, canyon 85 ft below. Distance =
|320 - (-85)| = 405 ft. Key, rendered p.5: "Answer: 405 feet".
Keyed `correct_1` = "405 feet". Agrees.

Non-keyed: "235 feet" (signed sum), "405 miles" and "405 meters" (different
quantities, not unit-equivalents; 135 yards is absent), "-405 feet" (signed),
"320 + (-85) = 235" (ruled on above), "406 feet", "404 feet" (off by one). All
false.

---

## CRITERION BY CRITERION

**1 — Stem fidelity.** 1-7 both parts verbatim against the rendered assignment
p.3, checked against the part named in each item title; Part 1 numbers
(10, 6, -0.5) and Part 2 numbers (15, 5, -0.2) do not cross-contaminate.

1-10 expands the assignment's compressed table wording ("Hiker 1 climbs to a
peak 450 ft above sea level…") into prose. **This is not a paraphrase the QTI
invented.** Topic1ExplanationsPart1.pdf, the student-facing companion, quotes
the stem in the QTI's exact words — "Two people are hiking. The first person
climbs to the top of a peak that is 450 feet above sea level. The second person
descends into a valley that is 120 feet below sea level. What is the total
vertical distance between the two hikers?" — so the QTI reproduces the canonical
student-facing wording, and the assignment table is the abbreviation. Separately,
expansion is the corpus norm: I extracted all 88 Shape A stems and every word
problem is expanded the same way (1-4 P1Q2 "Two birds are flying in the sky.
Bird A is 150 feet above sea level…" for the assignment's "Bird A is 150 ft
above sea level."). Every number (450, 120 / 320, 85), every direction, every
landform noun (peak, valley / ridge, canyon) and the question asked are
preserved. Not a defect.

**2 — No true-but-unkeyed choice.** All 28 non-keyed choices worked
individually, above. None is true of its stem. The two equation choices are
criterion 2's stated weaker case, recorded as such and ruled on explicitly. I
also searched for the specific true-forms the rubric enumerates and confirmed
each is absent rather than merely unnoticed: no unsimplified/equivalent
fraction (no fractions in this slice), no bare-value-vs-`n =` pair, no restated
value, no correct alternative expression, no true unit conversion (190 yards /
135 yards absent), no `+-` form, and nothing asserted as true in a stem.

**3 — No false-but-keyed choice.** All 4 keyed choices recomputed: -8, -4,
570 feet, 405 feet. All true. No double-signed direction phrasing anywhere in
either package.

**4 — Key agreement.** Each keyed set is a single choice and reproduces its
answer key PDF exactly, read rendered: Part 1 p.4 (-8) and p.5 (570 feet);
Part 2 p.4 (-4) and p.5 (405 feet). No key in this slice writes two forms joined
by "or", so the all-or-nothing over-requirement failure (SC-2's class 3) cannot
arise here. Checked, not assumed.

**5 — Answerability from the assignment.** A student with only the assignment
computes -8 / -4 / 570 ft / 405 ft and finds exactly one matching choice per
item. No item offers an option the assignment excludes (the SC-1 failure mode),
and no item keys something the assignment's own framing rules out. Coverage:
Lesson 1-7 and Lesson 1-10 each carry exactly one question per part on the
rendered assignment (p.3 and p.4 — single "Q1." row in each column, no Q2), and
each package has exactly two items. Complete, no missing item and no missing
answer blank.

**6 — Structure.** Verified by walking the `<conditionvar>` tree with `<not>`
depth tracked, not by regex, so `<varequal>` inside `<not>` is counted as
negated. Per item, all four: exactly one `<respcondition>`; a single `<and>`
with no other logic node; the `correct_*` ident set equals the bare-`<varequal>`
required set; the `wrong_*` ident set equals the `<not><varequal>` negated set;
no ident in the tree that is not a declared choice; 8 choices; no two choices
share visible text (compared after tag-stripping); `original_answer_ids` lists
all 8 idents in choice order. Single `respident="response1"` throughout.

**7 — Markup and import validity.** Zero `$` characters in either XML — checked
by raw byte count, so no currency false-positive and no stray TeX. 1-7: two
`\(` and two `\)`, one balanced non-interleaved pair per stem; no `\[`/`\]`.
1-10: plain prose, zero math delimiters, internally consistent. The "Canvas
accuracy check:" instruction block appears exactly once in each of the four
stems (the duplicated-block defect is absent). No `<img>`, no `src=`, so the
`$IMS-CC-FILEBASE$` image-path failure cannot apply. All six XML files parse.
Both manifests declare the QTI resource plus its `assessment_meta.xml`
dependency with hrefs that resolve on disk; both `assessment_meta.xml` set
`points_possible` 2.0, consistent with 2 items at 1 point each, and
`allowed_attempts` 1 matching `cc_maxattempts` 1.

**Shipping artifacts (outside the rubric, checked anyway).** Both staged zips
unpack byte-identical to the `pkg/` trees (`diff -r` clean), match their
recorded SHA-256 in `staged/sha256sums.txt`, and place `imsmanifest.xml` at the
archive root as Canvas requires. Nothing was displaced between the source of
truth and the deliverable.

---

## CONSIDERED AND NOT SCORED AS A DEFECT

Recorded so a later reader sees these were examined and ruled on, not missed.

1. **1-10 equation distractors, pedagogical read.** Marking an arithmetically
   true sentence "incorrect" could in principle leave a student thinking
   450 + (-120) != 330. This is a style observation about distractor
   construction. It maps to none of criteria 1-7: the choice is not true *of
   this stem*, so criterion 2 does not reach it, and criterion 2 explicitly
   creates the weaker category and asks for a ruling rather than an automatic
   defect. Not scored. Not a "10/10 with minor notes" — it is not a defect.

2. **1-10 keys a value while its distractor is written as an equation.** A
   stylistic inconsistency within the choice list. Both equation choices are
   negated and both agree in value with their plain-value twin (`330 feet`,
   `235 feet`), so the list is internally consistent and no scoring
   contradiction exists.

3. **`<assignment_group_identifierref>` in both `assessment_meta.xml` files**
   points at a group identifier not declared in the package. Present identically
   in all 14 packages, so it is a corpus-wide Canvas convention, not a defect in
   this slice; Canvas creates the group on import. Out of scope either way.

---

## CLEAN

  topic-1-7-independent-practice-accuracy-check-qti  | Part 1 Question 1
  topic-1-7-independent-practice-accuracy-check-qti  | Part 2 Question 1
  topic-1-10-independent-practice-accuracy-check-qti | Part 1 Question 1
  topic-1-10-independent-practice-accuracy-check-qti | Part 2 Question 1

All four items worked in full — every stem against the rendered assignment,
every keyed choice against the rendered answer key, every one of the 28 non-keyed
choices recomputed. No defect stands.

**SCORE: 10/10.** Second independent 10/10. Slice accepted.
