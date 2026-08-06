# Corrections-sweep: CorrectionsReport.pdf vs. the 14 QTI packages

## Self-test (run first, per instructions)

Matcher tested against `/tmp/qtiwork/corpus_BROKEN.json` (the pre-fix corpus, which
still carries the known topic-1-9 defect) with the probe string:

> "A business owner loses $450.75 as a result of a shipping delay."

Result: **fired once**, on `topic-1-9-independent-practice-accuracy-check-qti.zip`
/ "Part 1 Question 1" (exact full-string match). The same probe against the
current, already-fixed `/tmp/qtiwork/corpus.json` returns **zero** hits, as
expected post-fix. The matcher is confirmed working before being trusted on the
rest of the corpus.

## Extraction

- **CorrectionsReport.pdf → Found/Corrected pairs:** `pdftotext -layout`, page
  breaks tracked via form-feed characters (27 physical PDF pages), entries
  segmented on the report's own `p. N <High|Medium|Low> <category>` headers.
  **111 of 111** entries parsed cleanly with non-empty Found and Corrected
  text — matches the report's own summary total (10 High + 35 Medium + 66 Low
  = 111) exactly. None were unreadable.
- **Fraction/superscript self-check:** 21 entries flagged as fraction- or
  exponent-adjacent were checked by rendering their source page with
  `pdftoppm -r 200` and reading the image. One entry's automated text *was*
  wrong exactly as warned: entry #55 (p.5, Topic SC-2 Q2 Part A) reads
  "Part A: 2⁴/2² (or equivalent)" in the rendered image; `-layout` had
  linearized the built-up exponents to "24 /22". Corrected by hand from the
  image before matching. Long division (#75), mixed numbers (#34, #47, #56,
  #59), and all other checked entries matched the rendered page exactly and
  needed no correction.
- **QTI corpus:** used the project's existing `/tmp/qtiwork/corpus.json`
  (157 items, 14 packages), built by `extract_v2.py`, which already follows
  the required order — real HTML tags stripped first via
  `</?[a-zA-Z][^>]*>`, entities unescaped second. Verified this is the
  *current* (post topic-1-9-fix) state: its topic-1-9 Part 1 Question 1 stem
  reads "A business loses $450.75…", not "A business owner loses…".

## Method

For each of the 111 Found strings: normalized (Unicode NFKC, unicode
minus/dashes folded to hyphen, whitespace collapsed, lowercased) and searched
against every item's title+stem+choices, both as a full-string substring and
as a 5+-word literal prefix. Every raw hit was then manually inspected against
the source PDF page and the actual QTI stem text, because a short or generic
Found string (e.g. "-120", a bare page heading) produces coincidental prefix
hits that are not real survivors.

## Hits, and which are real

The automated pass surfaced 8 candidate entries. Manual review split them:

**Not real survivors (5) — correction never touches this text:**

| idx | Found (truncated) | Why it's not a miss |
|---|---|---|
| 2 | "In a class debate, Jordan says 0.27…" | Correction adds a missing answer-key entry to `Topic1Part1Solutions` (or drops the companion's Q3) — it does not reword this question. The text is untouched by design; QTI carrying it is correct, not stale. |
| 4 | "An elevator starts on floor −3…" | Same pattern — correction adds missing solutions-key entries, doesn't reword the stem. |
| 12 | "A person is designing a rectangular poster…" | Correction is a body-type/font-size fix for the whole SC-2 section in the companion PDF — no textual change to this sentence at all. |
| 35 | "-120" | Cited defect is a number-line **figure's** tick label in the companion (Topic 1-10 Q1). The QTI's four "-120" occurrences are unrelated coincidental values in four different problems (a hiking-distance choice, a bird-distance choice, a bank-balance choice, a division choice) — none has a number-line figure, and topic-1-10's QTI item has no image at all. Confirmed false positive from a too-short, too-generic search string. |
| 91 | "In 82.731, the tenths digit is __________." | Prefix match only caught the shared preamble. The QTI item (6th-grade-review-section-1, C1) uses a `____` fill-in-blank format entirely different from the companion's `__________.` — the actual defect (trailing period after the blank) doesn't exist in the QTI text to begin with. |

**Real survivors (3 corrections-report entries, 4 QTI items) — confirmed:**

All three concern `topic-sc-2-independent-practice-accuracy-check-qti.zip`,
"Topic SC-2 Question 2" and "Question 3." The report cites them against the
Explanations companion's "Question block" — the companion's verbatim quote of
the assignment question — and the same wording was carried, unfixed, into the
QTI stems built from that same assignment.

### 1. Report entry (p.41, Low, grammar) — "total number" contradicts "each friend"

- **Found:** "Part A: What expression gives the total number of cupcakes each friend will get?"
- **Corrected to:** "Part A: What expression gives the number of cupcakes each friend will get?"
- **Survives in:**
  - `topic-sc-2-independent-practice-accuracy-check-qti.zip` → **Part 1 Question 2** — stem contains verbatim: *"Part A: What expression gives the total number of cupcakes each friend will get?"*
  - `topic-sc-2-independent-practice-accuracy-check-qti.zip` → **Part 2 Question 2** — same defect, parallel item: *"Part A: What expression gives the total number of muffins each friend will get?"* (not literally identical text — "cupcakes"→"muffins" — but the same "total number...each friend" contradiction the correction was written to fix; the report's Found/Corrected pair doesn't cite this parallel occurrence explicitly, but it's the same bug.)

### 2. Report entry (p.41, Low, inconsistency) — "person" vs "friend"

- **Found:** "Part B: How many cupcakes will each person get?"
- **Corrected to:** "Part B: How many cupcakes will each friend get?"
- **Survives in:**
  - `topic-sc-2-independent-practice-accuracy-check-qti.zip` → **Part 1 Question 2** — stem contains verbatim: *"Part B: How many cupcakes will each person get?"*
  - `topic-sc-2-independent-practice-accuracy-check-qti.zip` → **Part 2 Question 2** — same defect, parallel item: *"Part B: How many muffins will each person get?"*

### 3. Report entry (p.42, Low, inconsistency) — "property" vs the doc's own "law", and a missing answer blank

- **Found:** "Evaluate using the power-of-a-power property: (4³)² =."
- **Corrected to:** "Evaluate using the power-of-a-power law: (4³)² = ____."
- **Survives in:**
  - `topic-sc-2-independent-practice-accuracy-check-qti.zip` → **Part 1 Question 3** — stem contains: *"Evaluate using the power-of-a-power property: \((4^{3})^{2} =\)"* — both defects present (says "property," and no trailing blank after "=").
  - `topic-sc-2-independent-practice-accuracy-check-qti.zip` → **Part 2 Question 3** — same defect, parallel item: *"Evaluate using the power-of-a-power property: \((2^{4})^{2} =\)"*

All four affected items are in the same package: `topic-sc-2-independent-practice-accuracy-check-qti.zip`
(zip sha256 prefix `2c5847861017` in the cached corpus). Items "Part 1 Question 2"
and "Part 2 Question 2" each carry both the Part A and Part B defect together.

## Everything else: confirmed clean

The remaining 108 report entries were checked and found not to survive
anywhere in the 157-item QTI corpus, and every negative rests on the
self-tested matcher above (not a silently-broken probe). Breakdown by source
document (matches the report's own summary table, 111 total):

- Topic 1 — Explanations companion (Part 1): 43 entries, 4 of the 8 raw
  candidate hits were from here (3 real, 1 false-positive: idx 35), rest clean.
- Topic 1 — Part 1 Solutions: 13 entries, all clean, all answer-key prose the
  QTI packages don't contain (no "We Need/We Know/We Solve" scaffolding in
  QTI stems or choices).
- Topic 1 — Part 2 Solutions: 13 entries, same as above, all clean.
- 6th Grade Review (worksheet): 3 entries (structural instruction-prefix and
  section-merge fixes to Sections G/H/L), none present in the QTI corpus.
- 6th Grade Review — Explanations companion: 39 entries, 1 raw candidate
  (idx 91) which turned out to be a false positive on a shared preamble; rest
  clean.

A large fraction of the 111 entries are inherently inapplicable to QTI by
construction, independent of any search: answer-key "We Need/We Know/We
Solve" scaffolding text (Topic 1 Part 1/Part 2 Solutions, 26 entries total),
missing-answer-key additions that don't reword any existing sentence (several
in the Explanations companion), pure typesetting/spacing/font-size fixes with
no textual change, and companion-only structural headings ("Before leaving
this question" / "Why this makes sense"). These were still run through the
matcher — none produced a hit — but they were never going to, since the
corrected content in those cases either never existed in the QTI packages'
vocabulary or the "correction" doesn't touch the cited text at all.

## Bottom line

Three CorrectionsReport.pdf entries (the "total number," "person/friend," and
"power-of-a-power property/missing blank" fixes for Topic SC-2 Questions 2–3)
never made it into the QTI packages, and the same unfixed wording is
duplicated across both the Part 1 (cupcakes) and Part 2 (muffins) parallel
items — four items total, all in
`topic-sc-2-independent-practice-accuracy-check-qti.zip`. No other survivors
were found anywhere in the 14-package, 157-item corpus, and that zero rests on
a matcher that was shown, on the known topic-1-9 case, to actually detect
survivors when they exist.
