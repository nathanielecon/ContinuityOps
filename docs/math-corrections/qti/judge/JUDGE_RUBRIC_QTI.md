# Judge rubric — Canvas QTI accuracy checks

You are a **judge**. You score. You do **not** edit any file. A separate fixer
applies changes. Editing disqualifies your verdict.

## What these artifacts are

14 Canvas QTI 1.2 packages. Students import them and use them to check their
own homework against the Independent Practice assignment. **A wrong key here is
worse than a worksheet typo:** it tells a student who got the question right
that they got it wrong.

## The two structural shapes — identify yours before scoring

Your slice is one shape or the other. Applying the wrong shape's criteria is
itself a scoring failure.

**Shape A — Topic 1 packages** (`topic-*`, 88 items total)
- `multiple_answers_question`, select-all-that-apply, all-or-nothing.
- Choice idents encode intent: `..._correct_N` and `..._wrong_N`.
- Scoring: one `<respcondition>` carrying
  `<setvar action="Set" varname="SCORE">100</setvar>`, every `correct_*`
  required by a bare `<varequal>`, every `wrong_*` negated by `<not><varequal>`.
  **`maxvalue="100"` is on `<decvar>` in `<resprocessing><outcomes>`, not on the
  `<respcondition>`** — an earlier draft of this rubric said otherwise and two
  judges repeated it. Grepping for `maxvalue` inside a `<respcondition>` finds
  nothing; that is correct, not a defect. The corpus is uniform at 163/163.
- ≥8 choices per item.
- **Verified corpus-wide: the scoring key equals the `correct_*` ident set on
  all 88 items, zero exceptions.** So the ident labels are the scoring truth —
  but that says nothing about whether those labels are *mathematically* right,
  which is what you are here to determine.

**Shape B — the two 6th-grade packages** (69 items total)
- Mixed: `multiple_answers_question` (21), `numerical_question` (37),
  `short_answer_question` (11).
- Idents are `choice_1…choice_7` or `answer1`. There is **no `correct_*` /
  `wrong_*` naming.** Intent lives only in the `required` / `negated` lists.
- `respident="response"`, not `response1`.
- **All 69 items have fewer than 8 choices.** Do not score this as a defect —
  it is this corpus's design, not a violation.
- Six items carry **two `<respcondition>` blocks**. Inspect before judging: on
  every one seen so far these are deliberate trailing-zero or equivalent-form
  alternates (`3.6` / `3.60`). That is good design. Only flag a second
  respcondition if it is *not* an equivalent-form alternate.
- These two packages have **no checksum and no validation record.** Nobody has
  ever checked them. Treat every claim about them as unverified.

## Rubric — all criteria must hold. Score /10.

No rounding up. No "10/10 with minor notes". A note is a defect or it is not.

1. **Stem fidelity.** The stem matches the assignment's wording and numbers
   **for the part named in the item title**. Part 1 and Part 2 carry different
   numbers — check against the right one. For Shape B, check against the
   6th Grade Review worksheet item of the same label (A1, K9, N6, …).

2. **No true-but-unkeyed choice.** THIS IS THE PRIMARY HUNT. Work every
   non-keyed choice yourself and confirm it is false. Under all-or-nothing
   scoring, a distractor that is actually true means a student who reasons
   correctly selects it and scores **zero** — the defect punishes precisely the
   strongest students, and it is invisible to anyone who only checks that the
   keyed choices are right.

   Count as true, i.e. as a defect:
   - an equivalent or unsimplified fraction, or a mixed/improper pair
   - a bare value where the key writes `n = value` (or vice versa)
   - the same value restated (`1 exactly` vs `1`)
   - a correct alternative expression or an alternative valid factorisation
   - the right value in different units
   - `±18` written `+-18` where the key is `+18 and -18`
   - a statement given as true in the stem itself
   - for a stem that says "select all **equivalent** …": every algebraically
     equivalent form, whether or not it is the form the author had in mind

   A distractor that is a *true arithmetic statement but answers a different
   question* is a weaker case — record it, say so explicitly, and rule on it;
   do not silently merge it with the above.

3. **No false-but-keyed choice.** Work every keyed choice yourself. Watch for
   double-signed phrasing (`-96 feet below sea level` asserts 96 ft *above*).

4. **Key agreement.** The keyed set together reproduces the answer key PDF's
   answer for that lesson / part / question. If the key writes two forms with
   **"or"**, requiring both under all-or-nothing scoring is a defect: a student
   who gives one acceptable form scores zero.

5. **Answerability from the assignment.** A student who has only the assignment
   in front of them must be able to produce the keyed set. If the QTI stem
   offers options the assignment does not, or keys an answer the assignment's
   own choices exclude, that is a defect even when the keyed choice is
   mathematically true in the abstract.

6. **Structure.**
   - Shape A: exactly one `<respcondition>`; every `correct_*` required; every
     `wrong_*` negated; ≥8 choices; no two choices with identical visible text.
   - Shape B: the required/negated split is coherent; duplicate visible text is
     still a defect; choice count and second respconditions are **not**.

7. **Markup and import validity.** Math delimiters balanced and consistent
   (`\(...\)` throughout — a stray `$…$` or an interleaved `$…\(…\)…$` renders
   literally in Canvas). No duplicated instruction block in a stem. Referenced
   images resolve: Canvas expects `$IMS-CC-FILEBASE$/media/…`, and a plain
   `src="media/…"` is import-blocking wherever the image **is** the question.

## Candidate findings

A first-pass audit produced candidate defects for some slices; yours are
attached if any. **They are candidates, not findings.** Confirm or refute each
one independently and say which. That audit is a single unreviewed pass and has
no more standing than your own reading. Finding nothing beyond the candidates is
an acceptable outcome only if you actually worked every item.

## Instrument traps — verified, do not rediscover

| Trap | Correct method |
|---|---|
| A regex over an `<item>` catches `<varequal>` inside `<not>` — every choice then looks correct | parse the `<respcondition>` tree; strip `<not>` blocks first. **This trap was hit this session.** |
| `pdftotext -layout` **transposes** built-up fractions: a correct `4/7 = ?/21` extracts as `47 = 21 / ?` | settle any fraction by rendering the page, never by extraction order |
| `grep -P '[\x{4e00}-…]'` errors, prints nothing, and **exits 0** | Python regex, self-tested on a known CJK string first |
| The same CJK check on a PDF or zip false-positives (stream bytes decode as CJK) | text files only |

**Standing rule: when a measurement contradicts a visible fact, suspect the
instrument first, then confirm along a second and third independent path.**

## Report format — English only, no CJK in the deliverable

```
SLICE: <id>          SCORE: n/10
ITEMS WORKED: <count> of <count>     (list any you could not work, and why)

DEFECTS
  <item title> | <criterion #> | <ident or location>
    found:  <exact text>
    why:    <the mathematics, worked>
    fix:    <the exact replacement text, or the exact structural change>

CANDIDATES RULED ON
  <candidate> -> CONFIRMED | REFUTED  (+ one line of reasoning)

CLEAN
  <item titles verified with no defect>
```

Score 10/10 only when every item in the slice is worked and no defect stands.
