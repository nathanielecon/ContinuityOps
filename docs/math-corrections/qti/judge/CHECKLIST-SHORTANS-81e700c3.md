# Frozen Checklist — SHORTANS Slice — Build `81e700c3f40bb7b5`

## Status and scope

This checklist is frozen against build `81e700c3f40bb7b5`.

The judged corpus contains 199 items across 14 packages:

- 125 `numerical_question` items;
- 74 `short_answer_question` items;
- zero `multiple_answers_question` items.

This checklist governs only the 74 `short_answer_question` items. It is a derivation of the requirements for a later 10/10 judgment, not a score and not an authorization to repair the corpus.

The following facts were carried forward from the established build evidence and were not rerun for this re-dispatch:

- `./build.sh` completed successfully and reproduced build hash `81e700c3f40bb7b5`;
- the census was 125 numeric items and 74 short-answer items;
- `battery.py` exercised 1,500 answers across all 199 written-response items.

Canvas short-answer comparison trims leading and trailing whitespace and folds case, but every remaining internal byte is literal. It has no mathematical-equivalence grader. Therefore, a correct but unaccepted string is a full-severity defect: a student who did the mathematics correctly receives zero.

## Decision rule

The SHORTANS slice may receive 10/10 only if every rule below is true, every listed exception has been resolved, and a fresh judge confirms the resolution against the unchanged build.

Each rule is atomic at the item level: for every named item, a later judge records `pass`, `fail`, or `undecidable`. A rule passes for the slice only when all 74 item-level decisions are `pass`.

## R1 — Build binding and complete census

**Rule.** The artifact under judgment must hash to `81e700c3f40bb7b5`, and an independent parse of the authoritative package XML must find exactly 74 distinct `short_answer_question` items. Every item must have a unique QTI ident and exactly one entry in the judge's working census.

**Harm if false.** A result could be attributed to a different corpus, or an omitted item could ship without review and reject any correct answer it fails to enumerate.

**Coverage.** R1: 74 checked, 74 pass, 0 exceptions.

## R2 — Source fidelity and split conservation

**Rule.** Each item must ask the question asked by its source assignment, preserving every load-bearing number, operation, qualifier, and direction. A split is permitted only when required for automatic grading; all split items together must ask exactly what the source asked, no more and no less, and each split item must remain independently answerable.

**Harm if false.** A student can answer the assignment correctly but be asked or scored on a different problem. For example, a student solving the source's "prime factorization" task with `2,3,3,5` would be marked wrong if the QTI silently changed the requested operation or retained the wrong source numbers.

**Coverage.** R2: 74 checked, 74 pass, 0 exceptions.

## R3 — Independent answerability, no answer disclosure, and no duplicates

**Rule.** The stem must contain all information necessary to produce the answer without consulting a sibling item, while neither the stem nor another part may disclose the answer being graded. No two short-answer items may ask the same full question merely under different idents.

**Harm if false.** An independently correct student may be unable to answer from the assignment alone, while another student may receive the answer from scaffolding rather than demonstrate the required mathematics. A duplicate can also count the same skill twice and amplify one answer-format defect.

**Coverage.** R3: 74 checked, 74 pass, 0 exceptions.

## R4 — Mathematical correctness and reverse acceptance

**Rule.** Every accepted string must be a mathematically correct answer to the exact task and must comply with every explicit format instruction in the stem. Equivalent value alone is insufficient when the stem requires a particular representation. The accepted set must not include a wrong answer, an incomplete answer, or a representation the stem expressly excludes.

**Harm if false.** A student who types a wrong or instruction-violating response can receive credit, defeating the accuracy check and making the result unreliable for students and teachers.

**Coverage.** R4: 74 checked, 71 pass, 3 exceptions.

### R4 exception — `g6_s1_f3` (`F3`)

**found:** The stem says, `Name the operation and the number, like: add 3.` The accepted set is:

`{"subtract 8", "subtract8", "subtraction", "subtract", "minus 8", "take away 8", "subtract eight", "subtracting 8", "subtracting eight", "minus eight", "take away eight", "-8", "−8"}`

The strings `subtraction` and `subtract` do not name the number. The strings `-8` and `−8` name a signed number but do not name the operation.

**why:** Undoing `+8` requires subtraction of 8 because `x + 8 - 8 = x`. A complete answer under the stem's own format must communicate both subtraction and 8. `subtract`, `subtraction`, `-8`, and `−8` omit one of those required components. A student can therefore supply an incomplete answer and receive credit.

**fix:** Either narrow the accepted set to responses that name both the operation and 8, or change the stem to enumerate the shorter forms that are intentionally accepted. Do not retain a mismatch between the promised response shape and the accepted set.

### R4 exception — `g6_s1_f4` (`F4`)

**found:** The stem says, `Name the operation and the number, like: add 3.` The accepted set is:

`{"divide by 5", "divide by5", "division", "divide", "dividing by 5", "divide by five", "dividing by five", "divide 5", "/5", "÷5", "÷ 5"}`

The strings `division` and `divide` do not name the number.

**why:** Undoing multiplication by 5 requires division by 5 because `5x ÷ 5 = x`. `division` and `divide` identify an operation but not the divisor. A student can omit the required number and still receive credit.

**fix:** Either remove responses that do not identify 5 or revise the stem to state exactly which shorter responses are accepted.

### R4 exception — `g6_s2_k6` (`K6`)

**found:** The stem asks which is greater, `1 3/4` or `(1)(3/4)`, and then instructs, `Type it the same way it is written in the question.` The accepted set is:

`{"7/4", "1 3/4", "1.75"}`

Only `1 3/4` is written in the question in the required form. `7/4` and `1.75` are accepted despite violating the explicit representation instruction.

**why:** `1 3/4 = 7/4 = 1.75`, while `(1)(3/4) = 3/4 = 0.75`; therefore the greater value is `1 3/4`. The strings `7/4` and `1.75` are mathematically equivalent values, but they are not typed the same way as the value appears in the question. The current scoring accepts students who do not follow the stated format.

**fix:** Make the instruction and acceptance policy agree. If exact source representation is required, accept only `1 3/4` subject to Canvas's documented trimming and case behavior. If equivalent forms are intended, remove the instruction to type the value exactly as written and state the permitted formats explicitly.

## R5 — Closed response language prescribed by the stem

**Rule.** The stem and accepted set together must define a finite, closed response language. For symbolic answers, the stem must give a worked example and state the exact separators, order, grouping, spacing, and symbol notation. For word answers, the stem must enumerate the permitted words or otherwise make one term uniquely required. If a mathematically correct student can follow the stem and produce a correct string outside the accepted set, the rule fails.

**Harm if false.** Canvas marks a mathematically correct answer wrong solely because the student chose an unenumerated synonym or notation. The concrete harmed students for the current exceptions are listed below.

**Coverage.** R5: 74 checked, 70 pass, 4 exceptions.

### R5 exception — `g6_s1_f1` (`F1`)

**found:** A student can type the mathematically correct response `factor`, but the exact accepted set is:

`{"coefficient", "numerical coefficient"}`

`factor` is rejected.

**why:** In `7m = 7 × m`, the number 7 is both the numerical coefficient of `m` and a factor of the product. The stem asks, `the number 7 is the ____`, and constrains only the length to one or two words. It does not say that the expected vocabulary word must be `coefficient`, nor does it enumerate the permitted terminology. The answer family therefore remains open.

**fix:** Make the requested vocabulary unique in the stem, for example by asking for the term meaning "the numerical factor multiplying a variable," or enumerate the accepted terms. Do not attempt to close an open vocabulary task merely by adding synonyms one at a time.

### R5 exception — `g6_s1_f2` (`F2`)

**found:** A student can type the mathematically correct response `unknown quantity`, but the exact accepted set is:

`{"variable", "unknown", "unknown number", "unknown value"}`

`unknown quantity` is rejected.

**why:** In `n + 8 = 12`, `n` is a variable representing an unknown quantity. The stem permits any one- or two-word response and does not enumerate the four accepted phrases. `unknown quantity` satisfies both the mathematics and the stated length constraint, yet Canvas's literal comparison rejects it.

**fix:** Enumerate the permitted words in the stem, require one unique vocabulary term, or change the question type if the vocabulary family cannot be closed. Merely adding `unknown quantity` would not prove closure because other correct synonyms could remain.

### R5 exception — `g6_s1_f3` (`F3`)

**found:** A student can type the plausible complete response `subtraction by 8`, but the exact accepted set is:

`{"subtract 8", "subtract8", "subtraction", "subtract", "minus 8", "take away 8", "subtract eight", "subtracting 8", "subtracting eight", "minus eight", "take away eight", "-8", "−8"}`

`subtraction by 8` is rejected.

**why:** Undoing `+8` means applying subtraction by 8. The rejected string names both the correct operation and the correct number and follows the stem's example-level instruction to name the operation and number. The stem does not enumerate its permitted grammar, so the accepted list is an open-ended selection of English phrasings rather than a closed response language.

**fix:** Constrain the response to an enumerated form, such as `Write exactly subtract 8`, or retain a choice-based format. Do not treat further synonym widening as proof of closure.

### R5 exception — `g6_s1_f4` (`F4`)

**found:** A student can type the mathematically correct response `division by 5`, but the exact accepted set is:

`{"divide by 5", "divide by5", "division", "divide", "dividing by 5", "divide by five", "dividing by five", "divide 5", "/5", "÷5", "÷ 5"}`

`division by 5` is rejected.

**why:** Undoing `×5` requires division by 5. `division by 5` states exactly that operation and number and complies with the instruction, yet it is absent. As with `F3`, the stem does not enumerate the allowed grammar, so the English response family is not finite.

**fix:** Constrain the student to one explicitly shown string, enumerate a genuinely finite set in the stem, or use a question type that does not depend on exhaustive English-synonym enumeration.

## R6 — Whitespace closure

**Rule.** For every item, either internal whitespace must be forbidden with an explicit no-space instruction and a worked example, or every internal-whitespace placement plausibly produced under the stem must be accepted. Leading and trailing whitespace may rely only on Canvas's documented trimming behavior, not on additional accepted strings.

**Harm if false.** A student who types `x > 5` instead of `x>5`, or `|5 - (-8)|` instead of `|5-(-8)|`, can be marked wrong despite identical mathematics.

**Concrete result.** All symbolic items that depend on a finite exact form either prescribe no spaces or include explicit spaced insurance forms. The tested no-space canonical forms were present. No additional whitespace rejection remained for a student who followed the current instructions.

**Coverage.** R6: 74 checked, 74 pass, 0 exceptions.

## R7 — ASCII hyphen-minus and U+2212 minus-sign closure

**Rule.** Whenever a correct response contains a negative sign or subtraction sign that a student could copy from rendered mathematics, every otherwise permitted form must be accepted with both ASCII `-` and U+2212 `−`, unless the stem explicitly supplies and requires one copyable character.

**Harm if false.** A student who copies the rendered `−8` instead of typing ASCII `-8` can be marked wrong even though the two strings display the same mathematics.

**Concrete result.** Every applicable negative or subtraction-bearing accepted family contained the corresponding ASCII and U+2212 forms. Examples include the orderings `-3,-1,8` / `−3,−1,8`, signed expressions `10+(-4)+(-8)` / `10+(−4)+(−8)`, and the Topic 1-4 distance expressions. No concrete missing minus-glyph twin was found.

**Coverage.** R7: 74 checked, 74 pass, 0 exceptions.

## R8 — Multiplication-notation closure

**Rule.** Where the stem does not prescribe one multiplication notation, every mathematically permitted expression must be closed across the applicable forms: asterisk `*`, multiplication sign `×`, middle dot `·`, and conventional juxtaposition. If the stem prescribes one form, the prescribed form must be accepted and a worked example must demonstrate it.

**Harm if false.** A student typing `a*7`, `a×7`, `a·7`, or `a7` can be marked wrong solely because Canvas compares the notation byte-for-byte.

**Concrete result.**

- `g6_s1_f5` accepts `4y`, `4*y`, `4×y`, and `4·y`.
- `g6_s2_k10` and `g6_s2_n5` explicitly prescribe `*` and accept the required `a*7`; they also accept the alternate multiplication glyphs and juxtaposition as insurance.
- `g6_s2_l1` includes the applicable `*`, `×`, `·`, and juxtaposition variants around the factor and parentheses.

No correct multiplication notation permitted by the corresponding stem was found rejected.

**Coverage.** R8: 74 checked, 74 pass, 0 exceptions.

## R9 — Comparison-symbol and inequality closure

**Rule.** Every item requiring a comparison must provide a copyable symbol palette when a non-ASCII character may be needed, prescribe the operand order or accept every equivalent order left open, and accept every comparison symbol that makes the exact displayed statement true.

**Harm if false.** A student typing `5<x` instead of `x>5`, or using the true inclusive comparison `3/4≤0.75` when the blank permits it, can be marked wrong despite writing a true statement.

**Concrete result.**

- `g6_s1_h3` accepts both `x>5` and `5<x`, with the enumerated internal-spacing variants.
- `g6_s1_h4` accepts both `x<6` and `6>x`, with the enumerated internal-spacing variants.
- `g6_s1_h5` asks for the equivalent reversed statement and accepts `y>6`.
- The greater-than and less-than statement items in `topic-sc-1` accept the prescribed no-space statements.
- The equality-symbol items accept `=`, `≥`, and `≤`; all three make the displayed equal quantities form a true statement.

No permitted comparison string was found rejected.

**Coverage.** R9: 74 checked, 74 pass, 0 exceptions.

## R10 — Case closure for alphabetic answers

**Rule.** Every alphabetic response must be correct under Canvas's actual case-folding behavior. The checklist must not infer case sensitivity from duplicate capitalized accepted strings; it must verify the scoring behavior used by Canvas.

**Harm if false.** A student typing `jordan`, `Jordan`, `NO`, or `Open,Right` can be marked wrong solely because of capitalization.

**Concrete result.** The word and name answers are compatible with Canvas case folding. Capitalized duplicates in some accepted sets are redundant but not harmful. No case-only correct response was found rejected under the stated Canvas comparison behavior.

**Coverage.** R10: 74 checked, 74 pass, 0 exceptions.

## R11 — Fraction and division-form closure

**Rule.** A fraction item must state whether the answer must be simplified, must use `a/b`, must contain no spaces, and must exclude mixed numbers when those restrictions apply. The accepted string must be the independently recomputed fraction in the exact required form. An expression containing division must not be mistaken for a request to evaluate unless the stem says to evaluate.

**Harm if false.** A student can correctly type `3/4` and be rejected because the key expects a decimal, or correctly preserve `2^4/2^2` as requested and be rejected because the scorer expects its value.

**Concrete result.** The 15 short-answer items requesting a fraction value accept their independently appropriate simplified `a/b` forms. The two power-division expression items accept `2^4/2^2` and `3^4/3^2` as expressions rather than incorrectly requiring evaluation. No compliant fraction string was found rejected.

**Coverage.** R11: 74 checked, 74 pass, 0 exceptions.

## R12 — Grouping and parenthesis closure

**Rule.** When grouping is mathematically load-bearing, the stem must prescribe the required grouping and order, and the accepted set must include the exact no-space form demonstrated by the instruction. Parentheses may not be silently removed where removal changes the expression.

**Harm if false.** A student typing `b+(3+9)` for the associative property or `10+(-4)+(-8)` for signed changes can be marked wrong even though the grouping is exactly what the task requests.

**Concrete result.**

- `g6_s2_k11` accepts `b+(3+9)`.
- `g6_s2_n6` accepts `x+(5+8)`.
- `1_3_part_1_question_1a` accepts `10+(-4)+(-8)` and its U+2212 twin.
- `1_3_part_2_question_1a` accepts `12+(-5)+(-9)` and its U+2212 twin.
- The Topic 1-4 expression families include the parenthesized forms permitted by their stems.

No instructed grouping form was found rejected.

**Coverage.** R12: 74 checked, 74 pass, 0 exceptions.

## R13 — Finite-language enumeration

**Rule.** For every short-answer item, the judge must be able to write down the complete language of correct responses permitted by the stem. The accepted set, after applying only Canvas's documented outer-whitespace trimming and case folding, must equal that language. Neither a strict subset nor a strict superset passes.

**Harm if false.** A strict subset marks a correct student wrong; a strict superset awards credit for an incomplete, incorrect, or instruction-violating answer.

**Coverage.** R13: 74 checked, 69 pass, 5 exceptions.

The open-language exceptions are `g6_s1_f1`, `g6_s1_f2`, `g6_s1_f3`, and `g6_s1_f4`, for the concrete rejected correct strings listed under R5.

`g6_s2_k6` is a strict-superset exception: `7/4` and `1.75` are accepted even though the stem requires the answer to be typed as it appears in the question.

## R14 — QTI scoring-tree validity

**Rule.** Every short-answer item must have exactly one response blank bound to the response ident, at least one nonempty accepted `<varequal>`, disjunctive scoring across alternate accepted strings, a score-setting branch only for accepted responses, and no malformed response-processing structure that Canvas could interpret as a conjunction or an unbound blank.

**Harm if false.** A student can type a listed correct answer into the visible blank and receive zero because the blank is unbound, because alternate spellings were combined as an impossible conjunction, or because the score-setting branch does not match the displayed field.

**Coverage.** R14: 74 checked, 74 pass, 0 exceptions.

## R15 — Gate limitations and mandatory human semantic review

**Rule.** A green `validate.py`, `battery.py`, or `build.sh` result must never be treated as proof of mathematical accuracy, source fidelity, or complete natural-language closure. A later 10/10 judgment must independently recompute each answer and compare plausible student strings against the artifact's actual accepted set.

**Harm if false.** A stem can be changed to ask different mathematics while retaining its old key, and all automated gates can still report success. Students who answer the changed stem correctly are then marked wrong.

**Established falsification.**

The item `g6_s1_b1` originally asks for the value of:

`8 + 3 × 4`

The correct value is:

`3 × 4 = 12`, then `8 + 12 = 20`.

The semantic injection changed only the stem to:

`8 + 3 × 5`

while retaining the accepted key `20`.

The injected stem's correct value is:

`3 × 5 = 15`, then `8 + 15 = 23`.

Both `validate.py` and `battery.py` nevertheless passed the injected artifact. This proves that neither gate detects a stem/key semantic mismatch. The gates remain useful structural instruments, but their green result cannot establish mathematical correctness.

**Coverage.** R15: the limitation applies to all 74 short-answer items; 74 require independent semantic review. The limitation itself is confirmed, with 0 undecided cases.

## Exception ledger

Only items that fail at least one rule are listed.

| Ident | Title | Failed rules | Exact rejected or wrongly accepted string |
| --- | --- | --- | --- |
| `g6_s1_f1` | F1 | R5, R13 | Correct `factor` rejected against `{"coefficient", "numerical coefficient"}` |
| `g6_s1_f2` | F2 | R5, R13 | Correct `unknown quantity` rejected against `{"variable", "unknown", "unknown number", "unknown value"}` |
| `g6_s1_f3` | F3 | R4, R5, R13 | Correct `subtraction by 8` rejected; incomplete `subtraction`, `subtract`, `-8`, and `−8` accepted |
| `g6_s1_f4` | F4 | R4, R5, R13 | Correct `division by 5` rejected; incomplete `division` and `divide` accepted |
| `g6_s2_k6` | K6 | R4, R13 | `7/4` and `1.75` accepted despite the instruction to type the answer as written in the question |

All other short-answer idents passed every rule checked above and therefore require no per-item row.

## Required defect-report format for the later judge

Every standing defect must be recorded as:

- **found:** the exact stem text, exact student string, and exact accepted set;
- **why:** the mathematics worked from the stem and the exact Canvas comparison that produces the wrong result;
- **fix:** the required behavioral outcome, without silently widening an open language or weakening an instruction.

A finding is not actionable if it merely says that closure, formatting, or wording is "incomplete" without naming the student string that is mishandled.

## Acceptance and invalidation

This slice cannot receive 10/10 while any exception in this checklist remains.

After repair:

1. rebuild the complete corpus;
2. bind all evidence to the new `sha256sums.txt` hash;
3. rerun the structural validator and answer battery;
4. independently recheck all 74 short-answer items against every rule above;
5. repeat the closure probes against the artifact's actual accepted strings;
6. run a fresh negative control to prove wrong answers remain rejected; and
7. obtain two independent 10/10 judgments against unchanged content.

Any change to a short-answer stem, accepted set, question type, response-processing tree, package membership, or corpus census invalidates the corresponding item-level result. A corpus change requires this checklist to be re-derived rather than amended.
