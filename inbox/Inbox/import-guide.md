# Canvas Import Guide

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
