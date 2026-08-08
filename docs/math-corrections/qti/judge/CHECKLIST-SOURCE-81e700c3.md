# Frozen Source-Fidelity Checklist — Build `81e700c3f40bb7b5`

## 1. Status and scope

This checklist is frozen against the build identified by:

```text
sha256sum docs/math-corrections/qti/zips/sha256sums.txt | cut -c1-16
81e700c3f40bb7b5
```

The governed corpus contains 199 QTI items across 14 packages: 125 `numerical_question` items and 74 `short_answer_question` items. Every item was checked against the assignment that generated it, not merely against another QTI artifact. The source set comprised:

- `6thGradeReview.pdf`
- `6thGradeReviewExplanations.pdf`
- `Topic1Part1Solutions.pdf`
- `Topic1Part2Solutions.pdf`
- `Topic1ExplanationsPart1.pdf`
- `CorrectionsReport.pdf`

This is a frozen checklist, not a score and not permission to repair an item. A later judge may award 10/10 for source fidelity only if every rule below is true on the exact build under review. Any content change, corpus change, source-document replacement, or changed build hash invalidates the counts and requires re-derivation rather than amendment.

An "exception" below means either a failed rule or a case requiring an explicit mathematical reconciliation. A reconciled case is not a defect when the stated ruling shows that the QTI is correct.

## 2. Controlling source rule

The assignment controls what the student is asked to do. A solution or explanation document is evidence of intended mathematics, but it does not silently replace the assignment when the two disagree.

A QTI item may divide one source question into separately graded parts only when the division is necessary for deterministic automatic grading. The resulting parts, considered together, must ask exactly what the source asked — no more and no less. A split may not introduce new mathematical demands, remove a demanded result, reveal one part's answer through another part, or turn an open response into a materially different task.

Where the assignment, a solution or explanation, and the QTI disagree, a judge must work the mathematics independently. The judge must identify which artifact is correct and why; agreement between two artifacts is not proof.

## 3. Atomic rules and coverage counts

### R1 — Every QTI item must have a specific source identity

**Decision rule:** For each QTI ident, a later reader must be able to name the source document, rendered page, source section or part, and source question number from which the item came. A thematic resemblance or a match to another QTI item is not sufficient.

**Harm if false:** A student may be asked an invented or misassigned question that was not part of the homework being checked, so a mathematically correct response to the actual assignment has no valid place to be entered.

**Coverage:** R1: 199 checked, 199 traced, 0 untraced, 0 undecidable.

### R2 — Each item must preserve the source question's mathematical demand

**Decision rule:** After allowing only a gradability-required split, each item must preserve the source's quantities, operations, relations, conditions, requested object, and direction of reasoning. Changing numbers, reversing an inequality, changing "not possible" to "possible," changing "prime factorization" to unrestricted factorization, or changing complete GCF factorization to any algebraically equivalent product is false under this rule.

**Harm if false:** A student can solve the assigned problem correctly and still be marked wrong because the QTI asks or keys a different problem. For example, a student who correctly identifies a product equal to 90 would be mis-scored if a QTI silently discarded the source word "prime," or a student who identifies an impossible outcome would be mis-scored if the item were harmonized to ask for a true statement instead.

**Coverage:** R2: 199 checked, 199 pass after the three explicit reconciliations below, 0 failed, 0 undecidable.

### R3 — Every load-bearing source word must survive

**Decision rule:** A word is load-bearing when removing, weakening, or replacing it changes which answers are mathematically correct. Every such word must remain operative in the QTI stem. In this build the protected cases include, but are not limited to:

- K2: **prime** factorization;
- L1: factor **completely** using the greatest common factor;
- Topic 1-2 Part 1 Question 2: which outcome is **NOT** possible.

A later editor must not normalize two superficially parallel stems when their different framing changes the truth of their choices.

**Harm if false:** A student can type or select an answer that is mathematically correct under the weakened wording and be marked wrong by a key that still assumes the missing restriction. For K2, `9×10` equals 90 but is not a prime factorization. For L1, `4(2x+4)` expands to `8x+16` but is not completely factored by the GCF. For Topic 1-2 Part 1 Question 2, a statement may be false as an "outcome of the long division" while not being false as a general statement about a decimal result.

**Coverage:** R3: 199 checked, 199 pass, 0 failed, 0 undecidable. Three load-bearing rulings are preserved below.

### R4 — Every item must be answerable from the assignment alone

**Decision rule:** A student who has the assignment and ordinary course knowledge, but not the solution PDF, explanation PDF, QTI key, another QTI part, or teacher-only notes, must have all information needed to produce the requested answer. Format instructions may be added for deterministic grading, but missing mathematical data may not be imported from a solution document.

**Harm if false:** A student who correctly completes the paper assignment may be unable to answer the QTI because a number, condition, diagram meaning, or requested form exists only in teacher material.

**Coverage:** R4: 199 checked, 199 pass, 0 failed, 0 undecidable.

### R5 — No item may disclose any part of its own answer

**Decision rule:** The stem, examples, parenthetical guidance, units, scaffolding, and response-format instructions must not state, algebraically force, or visibly contain any nontrivial part of the answer being graded. A format example must use different mathematics from the item. A whole-form response may not retain scaffolding that supplies one of its required components.

**Harm if false:** A student can receive credit without performing all of the source mathematics, so the QTI no longer checks the assigned work and can conceal a misconception.

**Coverage:** R5: 199 checked, 199 pass, 0 failed, 0 undecidable.

### R6 — No split part may hint another part's answer

**Decision rule:** For every source question represented by more than one QTI ident, each part must be independently answerable without displaying the answer, intermediate result, required symbol, or decisive reasoning needed by another part. The parts may share the original source facts, but one scored response may not be embedded in another part's stem or example.

**Harm if false:** A student can copy a displayed result from one QTI part into another and receive credit without independently doing the corresponding part of the assignment.

**Coverage:** R6: all 199 items and every represented split family checked; 199 pass, 0 failed, 0 undecidable.

### R7 — Every gradability split must conserve the source task exactly

**Decision rule:** When one source question becomes several QTI items, the union of the parts must require every mathematical result required by the source and no result the source did not require. Repetition for deterministic grading is not permission to broaden the exercise. A split must also be necessary: if one deterministically gradable response can preserve the source task without an open-ended or cross-response comparison, gratuitous subdivision fails.

**Harm if false:** A student may be marked wrong for an extra demand absent from the assignment, may receive full credit without completing a demanded source part, or may be forced to repeat a response in a way that changes the exercise.

**Coverage:** R7: all 199 items and every represented split family checked; 199 pass, 0 failed, 0 undecidable.

### R8 — The corpus may contain no unauthorized duplicate item

**Decision rule:** Duplicate detection must compare normalized full stems, source identities, requested answers, and mathematical demands. A suffix-only comparison is insufficient. Two QTI items are an unauthorized duplicate when they represent the same single source occurrence without a gradability justification. Identical mathematics appearing at two independently numbered source locations is not an unauthorized packaging duplicate, but both source locations must be cited.

**Harm if false:** A student is assessed twice for one assigned question, package counts are inflated, and a repeated response can distort the accuracy check.

**Coverage:** R8: 199 checked, 0 unauthorized duplicate items, 0 undecidable. One source-authored repeated exercise, K10/N5, was separately reconciled and is not a packaging duplicate.

### R9 — Known paper defects must not enter any QTI stem, key, or accepted set

**Decision rule:** Each recorded paper defect must be checked directly against the current assignment, the relevant companion or solution page, the QTI stem, and every accepted answer. A statement in `TEACHER_ACTIONS.md` that a defect did not leak is not evidence by itself. The QTI must follow the mathematically correct current assignment, and no stale question, stale key, or looser paper wording may cause a wrong response to be accepted or a correct response to be rejected.

**Harm if false:** A known upstream error becomes executable grading behavior. In the F4 case, a student typing `divide by 5` after correctly inverting multiplication by 5 could be rejected in favor of the stale opposite operation. In the M2 case, a student computing `615.65` from the current assignment could be rejected in favor of the answer to an obsolete subtraction problem. In the L1 case, a student following a stricter complete-GCF instruction could be judged under an ambiguous unrestricted-factorization prompt, or vice versa.

**Coverage:** R9: 199 items checked against all three recorded paper defects; 199 pass, 0 leaks, 0 undecidable. The three independent reconciliations are listed below.

### R10 — Any disagreement among assignment, solution, and QTI must be mathematically adjudicated

**Decision rule:** A disagreement may be closed only by quoting or precisely paraphrasing each artifact, citing its document and rendered page, and working the mathematics. The ruling must state which artifact controls and must identify the exact QTI ident affected. "The key agrees with the QTI" is not a mathematical adjudication.

**Harm if false:** Two artifacts can repeat the same mistake, and a later fixer may "correct" the only artifact that is actually right.

**Coverage:** R10: 199 checked, 3 recorded disagreement families adjudicated, all 3 QTI outcomes confirmed correct, 0 unresolved disagreements.

## 4. Exceptions and independent adversarial rulings

No item failed source tracing, split conservation, assignment-alone answerability, self-answer leakage, cross-part leakage, or unauthorized-duplicate review. The entries below are listed because they are load-bearing or because the source record required independent reconciliation.

### E1 — `g6_s2_k2` / K2: "prime factorization" is a form constraint, not decorative wording

**Source citation:** `6thGradeReview.pdf`, page 2, section K, question 2; `6thGradeReviewExplanations.pdf`, pages 34–35, K2.

**Found:** The source asks for the **prime factorization** of 90. The QTI preserves that demand and requires the prime factors in a deterministic order and notation.

**Mathematics:**

```text
90 = 2 × 45
   = 2 × 3 × 15
   = 2 × 3 × 3 × 5
   = 2 × 3² × 5.
```

Every terminal factor — 2, 3, and 5 — is prime. By uniqueness of prime factorization, this is the prime factorization of 90 up to order and equivalent exponent notation.

The adversarial alternatives are:

```text
9 × 10 = 90,
```

but 9 and 10 are composite;

```text
3² × 10 = 9 × 10 = 90,
```

but 10 is composite; and

```text
2 × 45 = 90,
```

but 45 is composite.

These are factorizations equal in value to 90, but they do not answer the source question because they are not products of primes only. The word "prime" constrains the resulting form. It does not merely describe a preferred derivation.

**Why:** Keying any of those composite-factor products would erase the source's mathematical distinction and reward the exact misconception the question tests. A mathematically strong student who reads "prime" does not choose them.

**Fix:** No fix. Preserve "prime." Do not generalize the stem to "factorization," "equivalent product," or "product equal to 90."

**Ruling:** Passes R2 and R3. This item does not fail source fidelity.

### E2 — `g6_s2_l1` / L1: the QTI is intentionally stricter than the worksheet's loose wording, and its mathematics is correct

**Source citation:** `6thGradeReview.pdf`, page 2, section L, question 1; `6thGradeReviewExplanations.pdf`, page 41, L1; `CorrectionsReport.pdf`, pages 18 and 26.

**Found:** The worksheet prints the loose prompt `Factor: 8x + 16 =`. The expected answer and instructional context require complete factorization by the greatest common factor. The QTI makes that criterion explicit: factor completely by pulling out the GCF, leaving no common factor inside the parentheses.

**Mathematics:**

The greatest common factor of the terms `8x` and `16` is 8:

```text
gcf(8x,16) = 8.
```

Therefore:

```text
8x + 16 = 8(x + 2).
```

The expression inside the parentheses is complete because the coefficients of `x` and `2` have no common factor greater than 1.

The weaker response

```text
4(2x + 4)
```

does expand correctly:

```text
4(2x + 4) = 8x + 16,
```

but it is not complete because `2x` and `4` still share the common factor 2:

```text
4(2x + 4) = 4 × 2(x + 2) = 8(x + 2).
```

Thus `4(2x+4)` is a valid factorization under the worksheet's bare wording, but it is not the complete GCF factorization expected by the solution and explicitly requested by the QTI.

**Why:** This is the recorded case in which assuming that every QTI/source disagreement makes the QTI wrong would produce a regression. The worksheet is underspecified; the QTI states the load-bearing completion criterion that the mathematics and answer key already require. Accepting `4(2x+4)` in the QTI would contradict "factor completely," while deleting the completion language would expose students to an ambiguous grading rule.

**Fix:** No QTI fix. Preserve "completely," "greatest common factor," and the no-common-factor-inside criterion. The paper worksheet should be amended by a human to say "factor completely using the GCF."

**Ruling:** Reconciled pass under R2, R3, R9, and R10. The paper wording is the defect; the QTI is correct.

### E3 — `1_2_part_1_question_2` and `1_2_part_2_question_2`: the two stems are deliberately not interchangeable

**Source citation:** `Topic1Part1Solutions.pdf`, page 1, Part 1 Question 2; `Topic1ExplanationsPart1.pdf`, pages 6–7, Part 1 Question 2; `Topic1Part2Solutions.pdf`, Part 2 Question 2.

**Found:** Part 1 asks which outcome of the long division is **NOT possible**. Part 2 asks for a statement about the result. The two items may contain superficially similar candidate statements, but those statements are evaluated under different predicates.

**Mathematics and semantics:**

For integers `x` and nonzero `y`, the decimal expansion of `x/y` terminates or repeats. A decimal expansion that neither terminates nor repeats is not possible for a rational number. Therefore the Part 1 statement describing a decimal that neither terminates nor repeats is the correct answer to the negated question.

The candidate statement "The sign does not matter here" illustrates why the stems cannot be harmonized:

- Under Part 1's wording, it is not an **outcome of the long division** at all. It therefore does not answer "which outcome is not possible."
- Under Part 2's request for a statement **about the result**, the sign does matter: if `a/b < 0`, the decimal result is negative; if `a/b > 0`, it is positive.

Consequently, a statement can be an invalid selection in Part 1 because it is not an outcome, and invalid in Part 2 for a different mathematical reason. Copying the Part 2 framing onto Part 1 — or the Part 1 negation onto Part 2 — would change which choices are true.

**Why:** Superficial parallelism is not source fidelity. Harmonizing the stems would detach at least one key from the predicate that makes it correct and could cause a student who understands rational decimal behavior to be marked wrong.

**Fix:** No fix. Preserve `NOT possible` in Part 1 and preserve the distinct Part 2 request. Do not normalize either stem to match the other.

**Ruling:** Passes R2 and R3. The deliberate difference is source-faithful.

### E4 — `g6_s2_m2` / M2: the current subtraction and QTI key are correct; the obsolete numbers did not leak

**Source citation:** `6thGradeReview.pdf`, page 2, section M, question 2; `6thGradeReviewExplanations.pdf`, page 43, M2; `CorrectionsReport.pdf`, page 19.

**Found:** The current assignment asks:

```text
700.32 − 84.67.
```

The QTI uses those numbers and keys `615.65`. The recorded obsolete form was:

```text
700.3 − 284.67.
```

Its answer would be `415.63`, but neither that obsolete stem nor that obsolete answer appears in the M2 QTI item or its accepted response.

**Mathematics for the current assignment:**

```text
700.32 − 84.67
= 700.32 − 80 − 4 − 0.67
= 620.32 − 4 − 0.67
= 616.32 − 0.67
= 615.65.
```

Check:

```text
615.65 + 84.67 = 700.32.
```

**Mathematics for the obsolete problem:**

```text
700.30 − 284.67 = 415.63.
```

That arithmetic is internally valid but answers a different, superseded question.

**Why:** The distinction is not a rounding variation. The minuend and subtrahend changed, so accepting `415.63` would mark the answer to the wrong assignment as correct and could reject a student who correctly typed `615.65`.

**Fix:** No QTI fix. Preserve the current stem and `615.65`. Do not import `700.3`, `284.67`, or `415.63` from historical material.

**Ruling:** No paper-defect leak. Passes R2, R9, and R10.

### E5 — `g6_s1_f4` / F4: undoing multiplication by 5 requires division by 5; the inverse operation did not leak backward

**Source citation:** `6thGradeReview.pdf`, page 1, section F, question 4; `6thGradeReviewExplanations.pdf`, pages 20–21, F4; `CorrectionsReport.pdf`, page 19.

**Found:** The current assignment asks for the inverse operation that undoes multiplication by 5. The QTI asks the same question and accepts the `divide by 5` family. It does not accept `multiply by 5`, the answer associated with the superseded "undo division by 5" prompt.

**Mathematics:**

Let the starting value be `x`. After multiplication by 5, the value is:

```text
5x.
```

Dividing by 5 restores the original value:

```text
(5x) ÷ 5 = x.
```

Multiplying by 5 again does not restore it:

```text
(5x) × 5 = 25x,
```

which differs from `x` except in the special case `x = 0`. An inverse operation must work generally, not only for one exceptional input.

Multiplying by `1/5` is algebraically equivalent to dividing by 5:

```text
(5x) × (1/5) = x.
```

The QTI's accepted responses remain within the division-by-5 family and do not admit the stale opposite operation.

**Why:** If `multiply by 5` leaked into the accepted set, a student giving the mathematical inverse would compete with an explicitly wrong response, and the item would cease to distinguish the misconception it tests.

**Fix:** No QTI fix. Preserve the current "undo ×5" stem and the divide-by-5 accepted family. Do not accept bare `multiply by 5`.

**Ruling:** No paper-defect leak. Passes R2, R9, and R10.

### E6 — K10/N5: identical source-authored exercise, not an unauthorized QTI duplicate

**Source citation:** `6thGradeReview.pdf`, page 2, K10 and N5; `6thGradeReviewExplanations.pdf`, the corresponding K10 and N5 entries.

**Found:** K10 and N5 present the same commutative-property exercise, but the repetition exists at two separately numbered locations in the assignment and in the companion. Each QTI occurrence traces to its own source location.

**Mathematics:**

```text
7 × a = a × 7
```

by the commutative property of multiplication.

**Why:** Removing either QTI occurrence merely because its full stem matches the other would cause one independently numbered assignment question to lose its accuracy-check counterpart. Conversely, treating one source occurrence as permission to manufacture unlimited copies would fail R8. The two rendered source locations provide the deciding evidence.

**Fix:** No fix. Retain both only while both independently numbered source questions remain in the assignment.

**Ruling:** Not an unauthorized duplicate. Passes R1 and R8.

## 5. Independent paper-defect leakage conclusion

The three recorded paper defects were checked independently rather than accepted from `TEACHER_ACTIONS.md`:

1. **M2 obsolete subtraction:** no leak. The QTI uses `700.32 − 84.67` and keys `615.65`; it does not use or accept the obsolete problem's `415.63`.
2. **F4 reversed inverse operation:** no leak. The QTI asks how to undo `×5` and accepts division by 5; it does not accept bare multiplication by 5.
3. **L1 loose paper prompt:** no leak into grading behavior. The QTI makes the intended complete-GCF criterion explicit and keys `8(x+2)`. The mathematical disagreement was resolved in favor of the QTI because `4(2x+4)` is algebraically equal but demonstrably not completely factored.

Therefore:

```text
Paper defects checked: 3
Paper defects reaching any QTI stem: 0
Paper defects reaching any QTI key: 0
Paper defects reaching any accepted-answer set: 0
Unresolved paper/QTI disagreements: 0
```

The current repository copy of `6thGradeReviewExplanations.pdf` also contains the corrected M2 and F4 material. That does not erase the historical leakage test: the QTI was checked for the obsolete numbers and inverse operation directly, and neither was found.

## 6. Required evidence format for a later scoring judge

For every failed or undecidable rule, the later judge must record:

### Found

- exact QTI ident;
- package;
- exact stem or accepted string involved;
- source document, rendered page, section or part, and source question;
- whether the case is a source mismatch, split mismatch, answer leak, duplicate, or paper-defect leak.

### Why

- the source demand in full;
- the QTI demand in full;
- independently worked mathematics;
- the exact student response or reasoning that is correct under the assignment;
- how the QTI would reject that correct response, accept a wrong response, disclose an answer, or assess an unassigned demand.

### Fix

- the smallest conceptual correction required;
- the source wording that must be restored or preserved;
- any split parts that must be removed, reunited, or made independent;
- the response behavior that must remain unchanged;
- a warning when the QTI is correct and the paper, solution, or explanation is the artifact requiring human correction.

A later judge must not report only "source mismatch," "wording issue," "duplicate," or "paper defect." Without the source citation and worked mathematics, the finding is not decidable.

## 7. Acceptance and invalidation

This source-fidelity slice may receive 10/10 only when:

- the build hash is exactly `81e700c3f40bb7b5`;
- the census is exactly 199 items;
- all rules R1–R10 are true;
- every exception is either repaired and freshly rechecked or explicitly reconciled as a pass;
- no source question is missing;
- no unauthorized QTI question is present;
- no gradability split changes the source demand;
- no part reveals another part's answer;
- no full-stem or semantic duplicate lacks two distinct source locations or a necessary split justification;
- none of the three recorded paper defects appears in a QTI stem, key, or accepted set; and
- the protected K2, L1, and Topic 1-2 Part 1 Question 2 wording remains operative.

Any repair or content change invalidates this build-bound result. A changed corpus requires a fresh checklist, not an amended count.
