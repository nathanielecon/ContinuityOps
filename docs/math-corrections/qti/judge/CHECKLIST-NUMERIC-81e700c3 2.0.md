# Frozen Checklist — NUMERIC Slice — Build 81e700c3f40bb7b5

> **Orchestrator's note, added on commit — not part of the judge's deliverable.**
> This is a **frozen checklist**, and as a statement of what the slice must
> satisfy it stands. Its per-rule coverage counts ("125 checked, 125 pass, 0
> exceptions", repeated for R1–R10) are the judge's own claims and are **not
> independently verified**. Treat them as a starting hypothesis, not a result.
>
> Two reasons for the caution. First, the checklist itself says the right thing
> and is followed here: *"The absence of listed item exceptions is not permission
> for a later judge to sample."* Second, a prior NUMERIC run exhausted its budget
> producing a 125-row ledger, so an exhaustive independent recomputation of 125
> keys plus ten rules, finishing comfortably and finding nothing, is the kind of
> uniformly clean result this project has repeatedly found to be an artifact of
> the instrument rather than of the corpus.
>
> The scoring round is a separate dispatch and must reconcile its own counts.
> `L1` below is the exception: it is a proved injection result, reproduced with
> commands, and is recorded as established. See `BF-2026-073`.

## Status and scope

This checklist is newly derived for the 125 `numerical_question` items in the 199-item corpus whose package manifest build is identified by:

```text
sha256sum docs/math-corrections/qti/zips/sha256sums.txt | cut -c1-16
81e700c3f40bb7b5
```

The corpus census is 125 numeric-entry items and 74 short-answer items across 14 packages. `./build.sh` rebuilds all 14 packages, and the answer battery exercises all 199 written-response items.

This document freezes the requirements for a later NUMERIC-slice judge. It is not an acceptance verdict. The slice may receive 10/10 only if every rule below is true for every applicable item on the unchanged build, every listed exception has been repaired, and a fresh full read finds no additional exception.

The authoritative evidence is the raw QTI XML in the packages. Generated caches, build logs, answer keys, and green automation may assist an audit but may not substitute for independently reading each stem and recomputing each answer.

## Decision rule

Each rule below is atomic at the item level: for each named numeric item, the later judge records either pass or exception. An exception must use this format:

```text
<item title> | <rule> | <ident>
  found: <the exact stem, key, accepted string, or structural fact that fails>
  why:   <the mathematics worked in full and the exact correctly reasoning student response that Canvas marks wrong>
  fix:   <the exact replacement text, accepted string, key, or structural change required>
```

A rule with one exception fails. There is no rounding, balancing, or "minor note" allowance for mathematical accuracy or answer format.

## Frozen atomic rules

### R1 — Numeric type and one numeric answer

**Requirement.** Each of the 125 items must ask for exactly one number and must be declared `numerical_question`. Its stem must not ask for an expression, equation, inequality, ordering, comparison statement, unit-bearing quantity, explanation, selection, or multiple separately scored answers. It must not contain or refer to a Part A or Part B label. A split item may retain shared context, but the item itself must ask only its own independently answerable question.

**Harm if false.** A student may correctly type the requested expression, such as `x=12`, or may correctly answer one of two requested parts, but Canvas marks the response wrong because the item was configured to score one bare number.

**Coverage claimed.** R1: 125 checked, 125 pass, 0 exceptions.

**Exceptions.** None.

### R2 — Independent mathematical recomputation

**Requirement.** For each item, recompute the keyed value from the numbers, operations, signs, rounding instruction, and question actually present in that item's own stem. Do not infer correctness from the answer-key PDF, a former multiple-choice option, another item, the accepted-answer list, `validate.py`, `battery.py`, or a green build. The recomputed result must equal every accepted value after applying only the equivalences expressly allowed by the stem, such as an optional trailing zero or an expressly requested rounding.

**Harm if false.** A student who performs the mathematics in the displayed stem and types the correct result is marked wrong. For example, if a stem asks `8 + 3 × 5` while the retained key is `20`, the student correctly types `23`, but Canvas marks `23` wrong and accepts the mathematically false `20`.

**Coverage claimed.** R2: 125 checked, 125 pass, 0 item exceptions.

**Exceptions.** None.

### R3 — Exactly prescribed answer format

**Requirement.** Every stem must prescribe one decidable answer format that a student can follow without guessing. It must state whether the response is a whole number, an integer, or a decimal; state the required rounding or displayed decimal precision wherever rounding or precision matters; and state that the student must enter the number only, without units or symbols, wherever the surrounding problem contains units, currency, percent signs, degree signs, variable names, or other answer labels. The prescribed format must agree with the actual shape of every accepted answer.

A stem that says "whole number" may not have a negative or non-integral key. A stem that says "integer" may not have a decimal key. A decimal instruction must not require a representation that the accepted set rejects. If both a padded and an unpadded decimal follow the instruction, both must be accepted unless the stem explicitly requires one exact display form.

**Harm if false.** A student can obey the stem and still be rejected. Examples include a student typing `0.5` when the stem incorrectly says "whole number," typing `3.60` when the stem requests two decimal places but only `3.6` is accepted, or typing `12` when the key expects an unstated unit-bearing form.

**Coverage claimed.** R3: 125 checked, 125 pass, 0 exceptions.

**Exceptions.** None.

### R4 — Sign instruction and sign fidelity

**Requirement.** Whenever the mathematically correct answer is negative, or the question's permitted data can produce a negative answer, the stem must explicitly instruct the student to include the negative sign. The key must carry the mathematically correct sign. Every negative accepted value must include both the ASCII hyphen-minus form and the visually corresponding U+2212 minus form with otherwise identical bytes.

When the question explicitly asks for a signed positive change, the accepted answer must preserve the required positive-sign convention rather than silently changing the mathematical object from a signed number to an unsigned magnitude.

**Harm if false.** A student who copies the rendered mathematical minus and types `−18` is marked wrong when Canvas accepts only `-18`, or a student who correctly types `-8` for a loss or descent is marked wrong because the key has the wrong sign. Conversely, a student asked for a signed positive change may correctly type `+18` and be marked wrong if only `18` is accepted.

**Coverage claimed.** R4: 125 checked, 102 not sign-sensitive and pass, 23 sign-sensitive and pass, 0 exceptions. All negative keyed answers in the sign-sensitive set carry paired ASCII hyphen-minus and U+2212 accepted strings.

**Exceptions.** None.

### R5 — Assignment-alone answerability

**Requirement.** Each item must be answerable from its own stem and the assignment material available to the student. Every number, operation, relationship, diagram fact, rounding instruction, and sign convention needed to determine the answer must appear in the assignment or in the item's reproduced context. A split half must repeat all context needed for that half and may not require the student to have opened or answered its sibling.

**Harm if false.** A student may correctly conclude that the displayed information is insufficient, or may compute the only value supported by the assignment, yet Canvas marks that response wrong because the hidden key depends on omitted context or on another quiz item.

**Coverage claimed.** R5: 125 checked, 125 pass, 0 exceptions.

**Exceptions.** None.

### R6 — No self-answer disclosure or cross-part hint

**Requirement.** No stem may state, display, or scaffold any part of the exact answer it asks the student to produce. A whole-form item may not retain intermediate values that reveal its result. A split item may not reveal its sibling's answer, and neither sibling may need an answer supplied by the other. General format examples are permitted only when their numbers and expressions are unrelated to the item's solution.

**Harm if false.** The instrument stops measuring the intended mathematics because a student can type a value copied from the question instead of solving it. It can also create inconsistent scoring: a student who follows a disclosed intermediate value may type the hinted response and be marked wrong when the hidden key reflects a different computation.

**Coverage claimed.** R6: 125 checked, 125 pass, 0 exceptions.

**Exceptions.** None.

### R7 — Accepted set is complete and contains only correct numeric strings

**Requirement.** Every string accepted by Canvas must represent the mathematically correct answer in the exact format permitted by the stem, and every distinct string that the stem permits a correctly reasoning student to type must be accepted. The set may include expressly permitted equivalent decimal displays, such as `3.6` and `3.60`, but it may not include a different value, a unit, a variable label, an equation, or an unrelated spelling. For negative values, R4's two minus-code-point forms are mandatory. Canvas's trimming and case folding must not be treated as mathematical equivalence or as a substitute for enumerating internal-byte variants required by the stem.

**Harm if false.** If the set is too narrow, a student who correctly types `3.60`, `−8`, or another stem-permitted representation is marked wrong. If the set is too broad, a student who types a mathematically false value receives credit.

**Coverage claimed.** R7: 125 checked, 125 pass, 0 exceptions.

**Exceptions.** None.

### R8 — Key, scoring tree, and response binding agree

**Requirement.** Each numeric item must bind its response declaration, response ident, `<varequal>` value or values, `<respcondition>`, and score-setting branch to the same student response. Every intended accepted value must reach the full-credit branch, and no unintended value may reach it. Alternate full-credit branches are permitted only for mathematically and format-equivalent strings. The response must remain automatically decidable without teacher interpretation.

**Harm if false.** A student can type the exact correct key shown in the package and still receive no credit because the scoring condition reads another response ident, or a student can receive credit for a wrong value through an unintended alternate branch.

**Coverage claimed.** R8: 125 checked, 125 pass, 0 exceptions.

**Exceptions.** None.

### R9 — Split conservation

**Requirement.** For every numeric item produced by splitting a source question, the split family must preserve every source subquestion exactly once, preserve the source's load-bearing wording and shared context, and add no new mathematical demand. Each half must be independently answerable, and the collection of halves must ask exactly what the source asked — no more and no less.

**Harm if false.** A student may correctly answer the assignment but be marked wrong on a quiz half that asks an altered question, or may never be tested on a source part that disappeared during splitting. A duplicated part can also penalize the same correct work twice.

**Coverage claimed.** R9: 125 checked, 125 pass, 0 exceptions.

**Exceptions.** None.

### R10 — Markup and imported numeric behavior

**Requirement.** Each stem's mathematical notation must remain legible after QTI import: delimiters must be balanced and consistent, exponents and fractions must preserve their intended grouping, referenced images must resolve through the packaged Canvas path, and the stem must not contain duplicated instruction blocks. The imported response must remain numeric entry with the accepted strings and scoring behavior audited under R7 and R8.

**Harm if false.** A student may read a different expression from the one used to create the key — for example, reading `-5²` as `-(5²)` while broken markup suggests `(-5)²` — then type the mathematically correct answer to what Canvas displays and be marked wrong. A missing diagram can make the requested number unknowable.

**Coverage claimed.** R10: 125 checked, 125 pass, 0 exceptions.

**Exceptions.** None.

## Exception ledger

No item-specific failure or undecidable item was found in the 125-item NUMERIC slice at build `81e700c3f40bb7b5`. Because this checklist records only failures and undecidable cases, no 125-row pass ledger is included.

The absence of listed item exceptions is not permission for a later judge to sample. A 10/10 verdict still requires that the later judge apply R1–R10 to all 125 numeric items and independently recompute all 125 keys.

## Standing limitation of the automated instrument

### L1 — Neither `validate.py` nor `battery.py` detects a stem/key semantic mismatch

**Found.** In an isolated copy of the build, the stem of `g6_s1_b1` was changed from:

```text
8 + 3 × 4
```

to:

```text
8 + 3 × 5
```

while its accepted key remained `20`. The mutation was confirmed in the parsed QTI tree. The isolated package then passed both the structural validator and the answer battery.

The reproduction used the normal validator and battery against isolated mutated artifacts:

```text
QTI_EXPECT_ITEMS=199 python docs/math-corrections/qti/validate.py /tmp/qti-inject-work
python docs/math-corrections/qti/battery.py /tmp/qti-inject-zips
```

Both commands completed successfully. The battery exercised 1,500 answer probes even though `g6_s1_b1` had become mathematically wrong.

**Why.** The unmodified item is correct because multiplication precedes addition:

```text
8 + 3 × 4
= 8 + 12
= 20
```

After the injected mutation, the stem instead evaluates to:

```text
8 + 3 × 5
= 8 + 15
= 23
```

A student who solves the mutated stem correctly types `23`. Canvas rejects `23` and accepts the retained but false key `20`. The gates still pass because they verify package structure and exercise declared accepted answers; neither independently derives the mathematical answer from the stem.

**Fix to the judging method.** Do not treat a green `validate.py`, `battery.py`, or `./build.sh` result as evidence that a key is mathematically correct or that a stem is faithful. R2 must always be performed by an independent mathematical read of every numeric item. This is a limitation of the instrument, not an instruction to modify the gate during this judging task.

**Coverage consequence.** L1 applies to all 125 numeric items. Automation provides zero semantic-key coverage; the independent R2 computation supplies the required 125-of-125 coverage.

## Evidence required from a later scoring judge

A later judge may award 10/10 only when the report includes all of the following:

1. The exact build hash `81e700c3f40bb7b5`.
2. A census of 125 numeric items worked out of 125.
3. Per-rule counts for R1–R10 whose totals reconcile to 125 or to the explicitly stated applicable subset.
4. Every failure or undecidable case listed by ident in the required `found / why / fix` format.
5. Full mathematics for every listed exception.
6. Independent confirmation that every negative key has both ASCII hyphen-minus and U+2212 accepted forms.
7. Independent recomputation of every key from its own stem rather than reliance on the automated gates.
8. Confirmation that no package or numeric-content change occurred after this checklist was frozen.

## Invalidation and acceptance

This checklist is bound to build `81e700c3f40bb7b5`. A change to the corpus census, any numeric stem, any accepted answer, any response-processing tree, any format instruction, or any source mapping invalidates candidate-bound judging evidence. A corpus change requires this checklist to be re-derived rather than amended.

Acceptance of the NUMERIC slice requires two consecutive independent 10/10 verdicts against unchanged content: the repairing judge's full re-score and a fresh cold judge's full read. Green automation alone cannot constitute either verdict.
