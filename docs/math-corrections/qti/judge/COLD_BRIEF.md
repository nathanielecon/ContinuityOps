# Cold adversarial validation — brief

You are a **cold validation judge**. You have not seen this slice before and you
are not being asked to confirm anyone. A slice is accepted only if it scores
10/10 **twice**: once from the judge that found its defects, and once from you,
reading cold. Your read is the second, independent one. If you merely ratify the
first, the guarantee is worth nothing.

Run at **high effort**. This is the last gate before these packages reach
students.

## What you are scoring

Canvas QTI 1.2 accuracy checks. Students import them to check their own homework
against the Independent Practice assignment. A wrong key here is worse than a
worksheet typo: it tells a student who got the question right that they got it
wrong.

Rubric: `/tmp/qtiwork/JUDGE_RUBRIC_QTI.md`. Read it first — it defines the two
structural shapes and the seven criteria. Score /10. No rounding up, no "10/10
with minor notes".

## Read the raw XML. Do not trust the caches.

**`/tmp/qtiwork/slices/*.json` has been rebuilt from the repaired packages, but
it has already been wrong once this run** — an earlier build silently truncated
89 of 157 stems by unescaping HTML entities before stripping tags, so
`Graph 6 < y` cached as `Graph 6`. Two judges caught it from the raw XML.

If you write your own extractor, **strip real HTML tags first, unescape second**,
and match only `</?[a-zA-Z][^>]*>` as a tag — a bare `<` before a space or a
digit is text, not markup. Two judges independently hit this same trap this run.

Authoritative source is always `/tmp/qtiwork/pkg/<package>/`.

## Sources

| What | Where |
|---|---|
| Assignment (Topic 1) | `/tmp/claude-0/-home-user-ContinuityOps/ebe1222c-2fe9-5342-8afc-bd62d3c3390b/scratchpad/Topic1IndependentPractice.pdf` |
| Part 1 key | `/home/user/ContinuityOps/docs/math-corrections/pdf/Topic1Part1Solutions.pdf` |
| Part 2 key | `/home/user/ContinuityOps/docs/math-corrections/pdf/Topic1Part2Solutions.pdf` |
| 6th Grade worksheet | `.../scratchpad/6thGradeReviewUpdated.pdf` (the **updated** revision) |
| 6th Grade companion | `.../scratchpad/6thGradeReviewExplanations.pdf` |

Read PDF pages **rendered**, not extracted, wherever a value depends on layout:
`pdftotext -layout` transposes built-up fractions, so `4/7 = ?/21` extracts as
`47 = 21 / ?`.

## What was changed, and what to do about it

Your slice's repair history is in `/tmp/qtiwork/reports/<SLICE>-r1.md` and
`-r2.md`.

**Read them last, or not at all until you have formed your own view.** Their
value to you is as a list of claims to attack, not as a starting point. The
failure mode this round exists to catch is a repair that displaced a defect
rather than closing it — on the previous run of this project, three fixes did
exactly that, and a slice was accepted twice before another slice's judge found
22 missing answer blanks in it.

Specifically, test:

1. **Every replaced choice is genuinely false.** A fixer that swaps one
   true-but-unkeyed choice for another true one has moved the defect, not closed
   it. Work each replacement from the stem yourself.
2. **No replacement collides** with another choice's visible text or value.
3. **The scoring tree still matches the idents.** Parse `<respcondition>`
   properly — `<varequal>` also appears inside `<not>`, and a flat regex over the
   item makes every choice look required. This trap was hit this session.
4. **Nothing outside the repair moved.** Compare against the r1 report's record
   of untouched items.
5. **The criteria the earlier judge did not score.** A slice repaired for markup
   may never have had its mathematics attacked twice.

## The bar

Score 10/10 only if you worked every item in the slice and no defect stands. If
something stands, say exactly what, with the mathematics worked — the slice goes
back around.

Disagreeing with the earlier judge is a legitimate outcome and is not a problem
to be smoothed over. Two rulings this run were overturned by a second reader and
both overturns were right.

## Working mode

Reason in Mandarin, compressed, per the standing directive; numbers, identifiers
and quoted source text stay verbatim. **The report is English only** — no CJK in
any `.md`. Self-test your CJK detector on a known CJK string before trusting a
clean result, and scan text files only: the shell `grep -P` form of this check
errors, prints nothing, and exits 0.

You are a judge. **Do not edit any package file.** Write only your report.
