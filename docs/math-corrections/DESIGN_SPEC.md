# Design spec — the three-variant rule

**This supersedes the fidelity criterion every earlier brief and rubric used.**
Read it before touching the explanation companions.

## The intended structure

Each lesson question exists in **three** variants:

| Artifact | Numbers | Purpose |
|---|---|---|
| **Explanations companion** | variant **C** — distinct from both | teaches the method fully worked |
| **Independent Practice Part 1** | variant **A** | student does it alone |
| **Independent Practice Part 2** | variant **B** | student does it again, fresh numbers |

Same question *structure*, *type* and *wording pattern* throughout. Only the
numbers — or the variables — change between variants.

**The point is pedagogical:** a student reading the fully worked explanation
must not be able to copy its answer into Part 1. They have to carry the *method*
across. An explanation that restates Part 1 verbatim defeats the assignment.

## What this means concretely

- Explanations Lesson 1-1 Q1 is a rise-then-descend sum question with numbers
  that are **neither** Part 1's 18 m **nor** Part 2's 24 m.
- Every block of that question — stem, Checked answer, worked steps, Final
  answer, closing paragraph — uses variant C consistently.
- **The answer keys are NOT variant C.** `Topic1Part1Solutions` answers variant
  A; `Topic1Part2Solutions` answers variant B. A key exists to check a student's
  own practice, so it must carry that part's numbers.

## Status: NOT implemented, and I made it worse

Measured against the original documents, not asserted:

- The original companion carried **Part 1's** distinctive numbers throughout —
  `$500` (6 hits), `$12.50` (7), `168` (7), `$450.75` (8), `250.50` (5),
  `10 points` (3). So variant C was never implemented across the document.
- The **single** vestige of variant C was Lesson 1-1 Q1's worked steps, which
  solved a 4.5 m climb while the stem showed Part 1's 18 m submarine — a
  half-applied variant, not a clean one, and it also changed the question *type*
  (single-move inverse vs two-move sum).
- **My correction removed that vestige.** I made the stem, steps and answer all
  agree on Part 1's 18 m. Under the real design that is the wrong direction: the
  right repair was to bring the *stem* to variant C, not to drag the working back
  to variant A.

So implementing this is **new work across ~30 questions**, not a repair of
something that regressed.

## The judge certification is void on this criterion

All 11 slices were accepted partly on: *"each restated Question matches the
source worksheet's wording, numbers and answer-slot form."* For the explanation
companion that criterion is now known to be **backwards on numbers**. Judges
enforced it diligently — several verified restatements character by character
against Part 1 — which under this spec means they certified the defect.

Still valid from that loop, because they do not depend on which variant is used:
arithmetic correctness, internal consistency within a question, typography,
figure geometry, answer-slot presence, no-fabrication.

Invalid for `Topic1ExplanationsPart1`: the numbers-match-the-assignment clause.

## Revised fidelity criterion

For an **explanation companion** question:

1. Question *type*, structure and wording pattern match the corresponding
   Part 1 / Part 2 item.
2. Numbers (or variables) are variant C — **distinct from both** Part 1 and
   Part 2.
3. Variant C is used **consistently in every block** of that question. A stem in
   one variant and working in another is the defect that started all this.
4. Variant C numbers must be *pedagogically equivalent*: same difficulty, same
   number of steps, same kind of arithmetic. Do not turn a two-digit subtraction
   into a one-digit one, or make a division come out even that was meant to have
   a remainder.
5. The **answer key** for a part keeps that part's numbers. Keys are never
   variant C.

For the **6th Grade Review companion**: unresolved — that worksheet has no
Part 1 / Part 2 (0 occurrences). Ask before applying variant C there.

## Answered

1. **Different numbers** — the companion uses its own set, distinct from both parts.
2. **Author fresh.** Variant C exists nowhere: the documents were not built to
   this spec.
3. **Numbers and variables both vary.** Where an item has no number to change,
   change the variable letter.

Read as: variant C changes numbers AND variable letters — not as "replace every
number with a symbol". A fully symbolic explanation cannot show a slow worked
long division (3 / 8 = 0.375), which is what these companions exist to do. If
fully symbolic is genuinely wanted, that is a different document and needs
confirming before anyone builds it.
