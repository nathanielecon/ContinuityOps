# Canvas Import Guide

> ## ⛔ SUPERSEDED — DO NOT IMPORT THE ZIPS IN THIS FOLDER
>
> These 14 packages are the **original 157-item select-all corpus** (109
> `multiple_answers_question`, 37 numeric, 11 short answer). All 14 differ from
> the current build; none is the corpus under correction. Every zip here has a
> different sha256 from `docs/math-corrections/qti/zips/`.
>
> **They are known to mis-score students.** The "Accuracy-Check Mapping" section
> below claims "Correct selections collectively reproduce full answer-key
> result." That claim has since been disproved. Recorded defects in *these*
> files:
>
> - **BF-031** — every key sat in the leading block with shuffle off, so a
>   student who simply picked the first N choices scored 100%: 47 of 47 items
>   keyed at position 0.
> - **D1** — six items ship statements that are **true** as choices you must not
>   select. Under all-or-nothing scoring, a student who correctly recognises a
>   true statement scores **zero**.
> - **D2** — `topic-1-4` asks for "at least two" expressions and scores 3–4
>   under `<and>`, so a compliant answer fails.
> - **D3** — 8 numeric items key a negative value while instructing "no units or
>   symbols", which reads as "omit the minus sign".
> - **D4** — `topic-1-2` P2Q3 keys `3x = 2`; its own solution PDF derives
>   `9x = 6`.
> - **D5** — `topic-sc-1` Q2 offers symbols neither the assignment nor the key
>   ever names.
> - **D6** — `topic-1-2` P2Q2 omits the `b ≠ 0` guard its own twin item carries.
>
> `validation-report.json` in this folder describes that same superseded corpus
> — its `signature_match: true` entries confirm the packages match the
> **then-current** answer key, not that the key or the item type was right.
>
> **The corrected corpus is 199 items — 125 numeric entry, 74 short answer, zero
> select-all — at `docs/math-corrections/qti/zips/`, build `81e700c3f40bb7b5`.**
>
> **It is not certified for students yet.** Every content acceptance was voided
> when the corpus changed, and the mathematics slices must return to 10/10 —
> the bar is 10/10 on mathematical accuracy and answer format — before anything
> ships. So do not substitute those zips for these and import them instead; wait
> for the acceptance, which will be recorded in
> `docs/math-corrections/qti/ACCEPTANCE.md`.
>
> Nothing in this folder has been deleted. Everything below this box describes
> the superseded packages and is kept for the record.

## Files

Each ZIP in this folder is one lesson-level Canvas-flavored QTI 1.2 package.
Import each ZIP separately.

## Canvas Title

Each package imports with this title pattern:

`Topic <ID> Independent Practice: Accuracy Check`

SC-1 uses `Lesson SC-1 Independent Practice: Accuracy Check`.

## Recommended Import Workflow

1. In Canvas, open target course.
2. Go to **Settings**.
3. Select **Import Course Content**.
4. Choose **QTI .zip file**.
5. Upload one lesson ZIP.
6. Leave package unpublished until import finishes and confirm select-all mapping.

## Accuracy-Check Mapping

Every Canvas item in these packages imports as `multiple_answers_question`
(select-all-that-apply).

- Every item has at least 8 choices.
- Correct selections collectively reproduce full answer-key result.
- Multi-part prompts require all correct parts.
- Units / equivalent representations are included when answer key requires them.

## Recommended Quiz Settings After Import

- Attempts allowed: course policy value.
- Score to keep: `Highest`.
- Shuffle answers: teacher preference.
- One question at a time: teacher preference.

## Build on Previous Attempt

1. Open imported quiz settings.
2. Enable **Multiple Attempts**.
3. Turn on **Build on Last Attempt** if theme exposes it.
4. Keep **Score to Keep** at `Highest`.

## Validation Notes

- Packages use stable identifiers and deterministic ZIP timestamps.
- Every lesson ZIP contains both Part 1 and Part 2 questions together.
- Validation report records exact correct-choice signatures for every item.
