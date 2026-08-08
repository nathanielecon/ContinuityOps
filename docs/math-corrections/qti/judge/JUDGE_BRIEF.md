# Judge brief — shared, identical for every slice

## Your role

You are a **judge**, not a fixer. You score a slice against
`/tmp/qtiwork/JUDGE_RUBRIC_QTI.md`. **Read that rubric first — it is the
scoring standard and it defines the two structural shapes.**

**Do not modify, create, or delete any file** except your own report under
`/tmp/qtiwork/reports/`. A separate fixer applies changes. If you edit a
package your verdict is void.

## Working mode

Reason and take notes in **Mandarin**, compressed (`/caveman wenyan-full`
style): drop function words, keep the mathematics exact. Numbers, identifiers,
XML and quoted source text stay verbatim — never translate or compress those.

**The report you write is English only.** No CJK character may appear in any
`.md`, `.json` or `.xml` you produce. Before you hand back, run a Python regex
CJK check on your report file — and **self-test the detector on a known CJK
string first**, because the shell `grep -P` form of this check errors, prints
nothing, and exits 0.

Use `rtk` to compress long shell output (`ls`, `find`, `grep` sweeps) if it is
on PATH. **Never** put `rtk` between yourself and evidence you are scoring:
read item text, XML and PDF pages raw.

## Your inputs

| What | Where |
|---|---|
| Rubric | `/tmp/qtiwork/JUDGE_RUBRIC_QTI.md` |
| Your slice, parsed | `/tmp/qtiwork/slices/<SLICE>.json` |
| Candidate findings | `/tmp/qtiwork/cand/<SLICE>.md` |
| Raw extracted XML | `/tmp/qtiwork/pkg/<package-name>/` |
| Assignment (Topic 1) | `/tmp/claude-0/-home-user-ContinuityOps/ebe1222c-2fe9-5342-8afc-bd62d3c3390b/scratchpad/Topic1IndependentPractice.pdf` |
| Part 1 answer key | `/home/user/ContinuityOps/docs/math-corrections/pdf/Topic1Part1Solutions.pdf` |
| Part 2 answer key | `/home/user/ContinuityOps/docs/math-corrections/pdf/Topic1Part2Solutions.pdf` |
| 6th Grade worksheet | `/tmp/claude-0/-home-user-ContinuityOps/ebe1222c-2fe9-5342-8afc-bd62d3c3390b/scratchpad/6thGradeReviewUpdated.pdf` |
| 6th Grade companion | `/tmp/claude-0/-home-user-ContinuityOps/ebe1222c-2fe9-5342-8afc-bd62d3c3390b/scratchpad/6thGradeReviewExplanations.pdf` |

The slice JSON is a cache built by parsing the `<respcondition>` tree with
`<not>` blocks stripped first. Its `required` / `negated` lists are the scoring
truth. Read the raw XML for anything the cache does not carry — markup,
delimiters, image `src` attributes, manifest structure.

`pdftoppm` and `pdftotext` are installed. Read PDF pages **rendered**
(`Read` with `pages=`) when a value depends on layout: `pdftotext -layout`
transposes built-up fractions, so `4/7 = ?/21` extracts as `47 = 21 / ?`.

## How to work

1. Read the rubric. Identify which shape your slice is.
2. Work **every item** in your slice. Recompute the mathematics yourself from
   the stem. Do not trust the ident labels, the cache, the candidate list, or
   any earlier report.
3. For each item, check every keyed choice and **every non-keyed choice**
   against rubric criterion 2 and 3. Criterion 2 is the primary hunt.
4. Rule explicitly on each attached candidate: CONFIRMED or REFUTED.
5. Write your report to `/tmp/qtiwork/reports/<SLICE>-r1.md` in the rubric's
   report format, and return the same content as your final message.

## The bar

Score 10/10 only when every item is worked and no defect stands. No rounding
up. No "10/10 with minor notes" — a note is a defect or it is not.

Reporting a slice clean without working every item is the failure mode this
loop exists to catch. On the previous run a fixer reported "0 teal pixels on
all five labels" against an unchanged PDF, and a whole judge loop certified a
property that was backwards. **When a measurement contradicts a visible fact,
suspect the instrument first, then confirm along a second and third independent
path.**
