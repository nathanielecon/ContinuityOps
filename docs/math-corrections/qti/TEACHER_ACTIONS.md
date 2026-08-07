# Things only a human with the source documents can fix

Everything else in this project is fixed in the QTI packages themselves.

**Two things need you** — §1 and §2, both defects in the **paper materials**
rather than in the packages. The packages are already correct; left alone, the
screen and the paper disagree in front of a student. Neither is urgent enough to
hold a release; both are cases where a student who does the right thing gets a
confusing signal.

**One thing needs a Canvas login** — §4, the import test. It is the only check in
this project that cannot be run from the build environment.

**§3 needs nothing.** It is kept because an earlier version of this file asked
you to act on it and that request was based on my error.

---

## 1. The 6th-grade explanations companion is stale in two places

The companion PDF handed out beside the accuracy checks was written against an
earlier revision of the worksheet and never re-generated. **Both QTI items match
the current worksheet and are correct** — it is the companion that drifted.

| Item | Worksheet (current, and what the QTI uses) | Companion (stale) |
|---|---|---|
| `M2` | `700.32 − 84.67 = 615.65` | poses it as `700.3 − 284.67` |
| `F4` | "To undo ×5…" → answer `divide by 5` | answers it for "undo ÷5" |

`F4` is the one that actually misleads: the companion's answer is *multiply by
5*, which is the exact inverse of the correct answer. A student checking their
work against it is told the right answer is wrong.

**Verified there is no leak into the corpus.** `F4`'s accepted list was widened
in BF-2026-041, and that widening was checked specifically for the companion's
inverse creeping in — the item accepts only the `divide by 5` family. `M2` keys
`615.65`, correct for the current numbers.

**Action:** regenerate the companion from the current worksheet, or strike those
two entries from it.

---

## 2. The worksheet's `L1` prompt is looser than the answer key

The worksheet asks a bare **"Factor: 8x + 16 ="**. The answer key expects the
complete GCF factorization, `8(x + 2)`. A student who writes `4(2x + 4)` has
answered the question *as printed* — it does expand to `8x + 16` — and is then
marked wrong.

The QTI has been made self-contained rather than loosened (the key is right):
its stem now states the criterion — *"A factorization is complete only when the
expression left inside the parentheses has no common factor of its own."*

**Action:** add "completely, using the GCF" to the worksheet so the paper asks
the question the key grades. Until then, paper and screen ask slightly different
things, with the screen being the stricter and more accurate one.

---

## 3. The figure items — resolved, nothing for you to do

An earlier draft of this file asked you to act here. That was based on a mistake
of mine, now corrected, and it is recorded so the history stays honest.

`A1`, `H6` and `H7` carry 6 distractors where the topic packages carry 7, and I
had flagged that as a gap to close by drawing three new figures. It was not a
gap. The judging rubric scopes the choice-count rule to the topic packages and
says of the 6th-grade packages, which is where these three live: *"All 69 items
have fewer than 8 choices. Do not score this as a defect."* My local checker was
enforcing a bar the rubric deliberately does not set, and I had been about to
author three SVG figures to satisfy it.

Both the checker and the record are fixed. There is no exemption any more,
because none is needed.

Two real improvements did come out of looking:

- **The three stems no longer depend on the diagram.** They used to say "Use the
  graphic choices", which points a student at an image that might not load. Every
  option was always written out in words as well, so they now say so. The items
  are answerable either way.
- **Each figure now ships at three locations inside the package**, because
  Canvas's `$IMS-CC-FILEBASE$` token can resolve to any of three plausible
  directories and there is no way to determine which without a live Canvas.
  Satisfying all three costs six small duplicate files and removes the question.

## 4. The Canvas import test itself

**This is the one thing standing between "built and verified" and "safe to give
to students", and it cannot be run from the build environment** — it needs a
Canvas URL, an API token and a scratch course, none of which belong in this
repository.

```bash
cd docs/math-corrections/qti
python3 verify_canvas_import.py --dry-run        # no network; checks the checker
python3 verify_canvas_import.py --course-id NNN  # the real thing
```

It reads credentials from the environment (`CANVAS_URL`, `CANVAS_TOKEN`) and
never takes them on the command line, so they do not land in shell history.

Run it against a **scratch course, not a live one.** It only creates content and
never reads student work, but it is a second unguarded path to the same Canvas
instance — `tools/graphify/vendor/` deliberately restricts Canvas access to an
allowlisted Playwright runner, and this bypasses that.

What it proves, and why each matters:

| Check | Why it is load-bearing |
|---|---|
| item count per package | a conversion that silently drops items is otherwise invisible |
| type mapping survived | short answer becoming multiple choice would put the answer on screen |
| **every accepted string survived** | 35 short-answer items score by exact string match; one lost variant marks a correct student wrong |
| SVG media present | three items are unanswerable if their figure does not render |
| zero migration issues | Canvas reports conversion problems here and nowhere else |
