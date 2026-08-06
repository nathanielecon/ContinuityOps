SLICE: T1-9          SCORE: 10/10
ITEMS WORKED: 4 of 4     (none skipped)

Second cold read. I formed a complete independent view of all four items —
stems, keys, every distractor, the scoring tree, markup and the package
wrapper — before opening `T1-9-r1.md`, `T1-9-r2.md` or `T1-9-cold.md`. Nothing
below is taken on the earlier judges' word; where I reach the same conclusion I
reached it on my own evidence, and I say what that evidence was.

Shape A confirmed from the raw XML: 4 `multiple_answers_question` items,
`respident="response1"`, `correct_*` / `wrong_*` idents, 8 choices per item,
exactly one `<respcondition>` per item carrying `<setvar action="Set"
varname="SCORE">100</setvar>`, and `maxvalue="100"` on `<decvar>` inside
`<resprocessing><outcomes>` (not on the `<respcondition>` — as the rubric
states).

Authority used: `/tmp/qtiwork/pkg/topic-1-9-independent-practice-accuracy-check-qti/`.
No slice cache was read at any point.

---

## WHICH COPY OF EACH SOURCE IS AUTHORITATIVE

I settled this before citing anything, because it is what broke the first cold
read of this slice.

| Source | Repo copy | Scratchpad copy | Governing |
|---|---|---|---|
| Topic1ExplanationsPart1.pdf | 356,001 B, 15:28, md5 `d3b1373f…` | 308,307 B, 10:02, md5 `f32b48f3…` | **repo** |
| Topic1Part1Solutions.pdf | 188,024 B, md5 `ef9e633a…` | 138,095 B, md5 `ead4ec42…` | **repo** |
| Topic1Part2Solutions.pdf | 200,111 B | 136,359 B | **repo** |
| Topic1IndependentPractice.pdf | md5 `c6e63e05…` | md5 `c6e63e05…` — **byte-identical** | either |

Direction of the correction, established from the documents themselves rather
than assumed:

- Scratchpad companion, line 1662: `A business owner loses $450.75 as a result
  of a shipping delay.` — the **uncorrected** text.
- Repo companion, line 1580: `A business loses $450.75 as a result of a shipping
  delay.` — the **corrected** text.

Two further 1-9 corrections logged in `CorrectionsReport.pdf` are present in the
repo companion and absent from the scratchpad one, which independently fixes the
direction (the repo file is the post-corrections rebuild, not a different
edition):

- p.36 `To cancel (cancel matching factors) means…` → `To cancel matching factors
  means…`. Repo line 1684 has the corrected form; scratchpad line 1769 has the
  defective form.
- p.37 `Four spacings of 3 7/8 fit exactly into 15 1/2… each spacing gives 4
  stations.` → `Four intervals of 3 7/8 …  each interval gives 4 stations.`
  Repo line 1721 corrected; scratchpad line 1810 uncorrected.

So the repo copy is the one the corrections pass produced, and it is the only
one a stem may be validated against. The assignment is unaffected either way,
the two copies being the same bytes.

---

## DEFECTS

  (none)

---

## 1. DO THE STEMS NOW MATCH THE ASSIGNMENT AND THE CORRECTED COMPANION?

**Yes — verified against both, independently.**

Current QTI stems, read from the raw `<mattext>` (tags stripped first, entities
unescaped second):

- `1_9_part_1_question_1`: "A business loses $450.75 as a result of a shipping
  delay. The 3 owners of the business have to share the loss equally. Write the
  quotient that represents each person's share of the loss."
- `1_9_part_2_question_1`: "A business loses $625.50 as a result of damaged
  inventory. The 5 owners of the business have to share the loss equally. Write
  the quotient that represents each person's share of the loss."

Against the **assignment** (repo `source/Topic1IndependentPractice.pdf`, page 3
rendered at 200 dpi, Lesson 1-9 table read from the image):

- Part 1 Q1: "A business loses $450.75 due to shipping delay. The 3 owners share
  the loss equally. Write the quotient representing each person's share."
- Part 2 Q1: "A business loses $625.50 due to damaged inventory. The 5 owners
  share the loss equally. Write the quotient representing each person's share."

Subject of the first sentence is the business in both. Numbers, divisor and
operation identical. The QTI prose is fuller, which is the corpus house style;
what matters is that the "one owner loses it / three owners share it"
contradiction is gone.

Against the **corrected companion** (repo `Topic1ExplanationsPart1.pdf`, PDF
page 32 rendered, Question block read from the image, not from extraction):

> A business loses $450.75 as a result of a shipping delay. The 3 owners of the
> business have to share the loss equally. Write the quotient that represents
> each person's share of the loss.
> **Checked answer:** −150.25 (or −$150.25 per owner)

Character-for-character identical to the QTI Part 1 Q1 stem. The repair is
exactly the published replacement, not a paraphrase of it.

`CorrectionsReport.pdf` p.35 confirms the logged entry and its replacement text
verbatim (Where: Topic 1-9 Question 1 > Question block).

Part 2 Q1 has no companion entry — there is no Part 2 explanations document in
the repository, only `Topic1ExplanationsPart1.pdf`. I checked that this is a
gap in coverage rather than a judgement that Part 2 was fine: grepping the whole
corrections report for `A business` returns only the two Part 1 lines (411/413).
The Part 2 fix is nonetheless correct, and required by criterion 1 on its own
footing, because the assignment's Part 2 Q1 reads "A business loses $625.50",
and because the identical internal contradiction was present.

---

## 2. DID ANYTHING ELSE MOVE?

**No. The total change is 12 bytes — the two occurrences of "owner ".**

I did not rely on any report's record of untouched items. I diffed the current
package against the originally shipped zip:

```
diff  /home/user/ContinuityOps/inbox/Inbox/topic-1-9-…-qti.zip  (28,153 B, Aug 5 21:12)
 vs   /tmp/qtiwork/pkg/topic-1-9-…-qti/                          (Aug 6 01:50)
```

Result: two changed lines, 34 and 244, each the deletion of the word `owner`
from a Q1 stem. `imsmanifest.xml` and `assessment_meta.xml` are byte-identical
(both still stamped 2026-01-01 inside the archive). Nothing in any choice, any
ident, any `<respcondition>`, or either Q2 item moved.

The shipping artifacts agree with what I read:

- `/tmp/qtiwork/staged/topic-1-9-…-qti.zip` unpacks byte-identical to the
  package directory (`diff -r` clean).
- `/home/user/ContinuityOps/docs/math-corrections/qti/zips/topic-1-9-…-qti.zip`
  (rebuilt 01:53) is also identical to the package.

### The four values, verified from the stems

Worked in exact rational arithmetic from the stem text alone, then checked
against the repo answer keys read from **rendered** page 5 of each Solutions PDF.

| Item | From the stem | Key PDF (rendered) | QTI keyed choice |
|---|---|---|---|
| P1 Q1 | (−450.75) ÷ 3 = −1803/12 = −601/4 = **−150.25**  (check 3 × 150.25 = 450.75) | "Answer: −150.25 (or −$150.25 per owner)" | `-150.25 per owner` |
| P1 Q2 | 31/2 ÷ 31/8 = 31/2 × 8/31 = **4** | "= 4 intervals … ⇒ 4. Answer: 4 water stations" | `4 water stations` |
| P2 Q1 | (−625.50) ÷ 5 = −1251/10 = **−125.10**  (check 5 × 125.10 = 625.50) | "Answer: −125.10 (or −$125.10 per owner)" | `-125.10 per owner` |
| P2 Q2 | 33/2 ÷ 11/4 = 33/2 × 4/11 = 132/22 = **6** | "= 6 intervals … ⇒ 6. Answer: 6 rest stops" | `6 rest stops` |

All four agree. Part 1 items carry Part 1 numbers and Part 2 items carry Part 2
numbers — no cross-part contamination.

On criterion 4's "or" trap: both money keys write a parenthetical alternate
(`−150.25 (or −$150.25 per owner)`). These are two spellings of one value, not
two required components, and only one form is offered as a choice — so there is
no all-or-nothing both-forms failure. The repo keys also already carry the
notation correction logged at CorrectionsReport p.5/p.4 (`$ − 150.25` →
`−$150.25`); the QTI writes neither form's dollar sign and is unaffected.

---

## 3. THE MIXED NUMBERS, READ FROM RENDERED PAGES

`pdftotext -layout` flattens these — the assignment extracts as `15 12` and
`3 78`, and the key extracts as `15 12 = 31 2`. I did not use any of that. All
four built-up fractions were read from images:

- **Assignment**, page 3 rendered at 200 dpi and cropped: `15½` miles / every
  `3⅞` miles (Part 1); `16½` miles / every `2¾` miles (Part 2).
- **Part 1 key**, page 5 rendered: `15½ = 31/2`, `3⅞ = 31/8`,
  `31/2 ÷ 31/8 = 31/2 × 8/31 = 4`.
- **Part 2 key**, page 5 rendered: `16½ = 33/2`, `2¾ = 11/4`,
  `33/2 ÷ 11/4 = 33/2 × 4/11 = 6`.
- **Companion**, PDF page 33 rendered: "A race is 15½ miles long … every 3⅞
  miles … Checked answer: 4 water stations."

QTI markup: `\(15\dfrac{1}{2}\)`, `\(3\dfrac{7}{8}\)`, `\(16\dfrac{1}{2}\)`,
`\(2\dfrac{3}{4}\)`. Every numerator and denominator matches the rendered
source. No transposition survived into the package.

**Equivalent-form distractors: none exist here, and I checked why rather than
just looking.** Both division items resolve to *integers* (4 and 6), so the
improper/mixed/unsimplified pair that normally hides in mixed-number division
cannot be constructed — there is no second way to write 4 or 6 as a count. Both
money items resolve to terminating two-place decimals; the forms that would be
defects (`-150 1/4`, `-$150.25`, `-150.250`; `-125.1`, `-125.100`, `-$125.10`)
appear in no distractor. I checked each of the 28 choices against its item's key
for equality of value, not just of string.

---

## 4. THE FINISH-LINE COUNT — WORKED MYSELF

**Part 1.** Route 15½ mi; stations every 3⅞ mi *along the route*, plus one at the
finish line. Station positions from the recurrence: 3⅞, 7¾, 11⅝, **15½**.
15½ ÷ 3⅞ = 4 exactly, so the fourth recurring station *lands on* the finish
line. The clause "and one at the finish line" is satisfied by that same station;
it does not add a fifth, because a fifth would have to be placed at a point
already occupied. **Total 4.** The first station is at 3⅞, not at mile 0, so no
start-line station is implied either.

**Part 2.** Route 16½ mi; stops every 2¾ mi: 2¾, 5½, 8¼, 11, 13¾, **16½**.
16½ ÷ 2¾ = 6 exactly, sixth stop on the finish line. **Total 6.**

So the count does *not* depend on a disputable reading — the double-count and
the no-count readings coincide, because the division is exact. This is what
makes `5 water stations` and `7 rest stops` legitimately false rather than
defensible alternatives, and it is the reason I can rule on them at all.

Both answer keys state the same resolution explicitly and independently of me:
"Stations at the end of each interval (**including the finish line**) ⇒ 4" and
"Rest stops at the end of each interval (**including the finish line**) ⇒ 6".

Had either division left a remainder, the two readings would diverge and the
item would be defective. Neither does.

---

## 5. TRUE-BUT-UNKEYED HUNT — ALL 28 CHOICES WORKED

I worked every non-keyed choice from the stem. Nothing selectable is true.

**P1 Q1** (key −150.25 per owner)
`150.25` sign error, and the stem's loss must carry a negative quotient ·
`-149.25`, `-151.25`, `-148.25`, `-152.25` each off by ±1.00 and fail the check
3 × value = 450.75 · `0.00` false · `-15025` decimal point misplaced by 10^2.
All false.

**P1 Q2** (key 4 water stations)
`3` (undercount) · `5` (the finish-line double count — false, see §4) · `8`
(= 2 × 4) · `-4` (a count cannot be negative) · `6` (Part 2's answer, wrong
route and wrong divisor here) · `2`. All false.

**P2 Q1** (key −125.10 per owner)
`125.10` sign error · `-124.10`, `-126.10`, `-123.10`, `-127.10` each fail
5 × value = 625.50 · `0.00` · `-12510` decimal misplaced. All false.

**P2 Q2** (key 6 rest stops)
`5` · `7` (double count) · `12` (= 2 × 6) · `-6` · `8` · `4` (Part 1's answer).
All false.

### The two weaker cases, recorded explicitly per the rubric and ruled on

**(a) Label swap — `1_9_part_1_question_2_wrong_3` = "4 rest stops" and
`1_9_part_2_question_2_wrong_3` = "6 water stations".** These carry the correct
numeral with the other part's noun.

RULING: **not defects.** The rubric's "right value in different units" case
means one quantity expressed in two measures (2 ft / 24 in), where both
statements are true. That is not what these are. "Rest stops" are not a unit of
"water stations"; they are a different object that exists only in the other
part's scenario. I tested each against **both** parts rather than only its own
stem: the Part 1 race has no rest stops at all, and the Part 2 trail has 6 rest
stops, not 4 — so "4 rest stops" is false under either reading. Symmetrically,
water stations exist only in Part 1 where the count is 4, so "6 water stations"
is false under either reading. Neither is a true statement anywhere in this
lesson. They are the intended read-the-question distractors.

**(b) Unsigned magnitude — `1_9_part_1_question_1_wrong_1` = "150.25 per owner"
and `1_9_part_2_question_1_wrong_1` = "125.10 per owner".** These are true
*arithmetic* statements (450.75 ÷ 3 really is 150.25) that answer a different
question — the size of each share rather than the signed quotient.

RULING: **not defects**, and I am flagging this as the weaker case the rubric
asks to be named rather than merged. The stem asks for "the quotient that
represents each person's share of the **loss**", in a lesson titled Divide
Rational Numbers whose whole point is sign handling. Both answer keys model the
loss as negative and print −150.25 / −125.10 as the answer. The repo companion
makes the modelling step explicit and unmissable — "Write the loss as −450.75",
"Opposite signs: the quotient is negative", "Three equal shares of a loss stay
negative. Check: (−150.25) × 3 = −450.75". A student who selects the unsigned
value has made the canonical sign error the item exists to detect. The choice is
false *as an answer to the question asked*.

### No false-but-keyed choice

All four keyed choices recomputed above and matched to the rendered keys. No
double-signed phrasing anywhere in this slice (no "below sea level" constructions
here).

### Answerability from the assignment

A student holding only the assignment can produce each keyed set: the numbers,
the divisor and the operation are all present in the assignment's own Lesson 1-9
table, and nothing in any QTI stem introduces information the assignment lacks
or keys an answer the assignment excludes.

---

## 6. STRUCTURE — PARSED, NOT REGEXED

Parsed with ElementTree and read out of the `<respcondition>` tree with `<not>`
subtrees separated from bare `<varequal>`s, so a negated ident can never be
counted as required. Per item:

| Item | choices | respconditions | required | negated | key == `correct_*` set | negated == `wrong_*` set | decvar |
|---|---|---|---|---|---|---|---|
| Part 1 Question 1 | 8 | 1 | `…_correct_1` | 7 × `…_wrong_1..7` | yes | yes | maxvalue=100 |
| Part 1 Question 2 | 8 | 1 | `…_correct_1` | 7 × `…_wrong_1..7` | yes | yes | maxvalue=100 |
| Part 2 Question 1 | 8 | 1 | `…_correct_1` | 7 × `…_wrong_1..7` | yes | yes | maxvalue=100 |
| Part 2 Question 2 | 8 | 1 | `…_correct_1` | 7 × `…_wrong_1..7` | yes | yes | maxvalue=100 |

No two choices share visible text within any item (checked by exact string map
of all 8 per item; 0 collisions). `original_answer_ids` metadata equals the
`response_label` ident sequence in document order, in all four items.

## 7. MARKUP AND IMPORT VALIDITY

- Delimiters: Q2 items have 2 `\(` and 2 `\)` each, balanced and paired; Q1
  items have none.
- Dollar signs: exactly one per Q1 stem, the currency symbol in `$450.75` /
  `$625.50`. A single unpaired `$` cannot open a math region, and neither Q1
  stem contains any `\(`, so the interleaved `$…\(…\)…$` failure cannot form. I
  checked this convention corpus-wide rather than assuming it: 39 `<mattext>`
  blocks across the 14 packages contain a `$`, and **zero** of them also contain
  a `\(`. Currency-`$` alongside `\(…\)` math is never mixed anywhere in this
  corpus. Not a defect.
- Exactly one "Canvas accuracy check" instruction block per stem — no
  duplication.
- No `img`, no `src=`, no media directory, so the `$IMS-CC-FILEBASE$` image trap
  does not arise.
- No double-escaped entities (`&amp;amp;` count 0). File parses cleanly.
- `imsmanifest.xml`: both resource `href`s resolve to files present.
  `assessment_meta.xml`: `points_possible` 4.0 = 4 items × 1 point.

---

## INDEPENDENT SWEEP FOR OTHER UNAPPLIED CORRECTIONS

Rather than trust that only one correction touched this package, I parsed all
**110** `Found:` / `Corrected to:` pairs out of `CorrectionsReport.pdf` and
longest-substring-matched every `Found:` text (≥5 words, whitespace- and
punctuation-normalised) against the package's tag-stripped text.

Raw result: 1 hit — `loses $450.75 as a result of a shipping delay. The 3 owners
of the business have to share the loss equally.` That fragment is also contained
in the *Corrected to:* text of the same entry (the correction deleted only the
leading word), so it is a shared-tail false positive, not a survivor. After
excluding fragments present in the paired replacement text: **0 real survivors.**

Instrument self-test: run against the pre-fix stem text, the same probe returns
the full 24-word hit "A business owner loses $450.75 as a result of a shipping
delay. The 3 owners of the business have to share the loss equally." So the
probe fires on the class of defect it is meant to catch, and its zero on the
current package is a real zero.

---

## CANDIDATES RULED ON

- **First cold judge's criterion-1 overturn of r1's 10/10** → **CONFIRMED, on my
  own evidence.** The defect was real: the pre-repair stems, which I read from
  the inbox zip directly, said "A business owner loses…". The corrections report
  logs the sentence and publishes the replacement.
- **r1's candidate D** ("stem matches Topic1ExplanationsPart1 verbatim, therefore
  canonical") → **REFUTED.** It matched the 308,307-byte scratchpad companion,
  which is the pre-corrections input, not the post-corrections output. The repo
  rebuild says the opposite. I re-derived the direction from three separate
  corrections (the stem, the "cancel" bullet, "spacings"→"intervals") all
  appearing corrected in the repo file and uncorrected in the scratchpad file.
  A house-style argument cannot clear a string that has a published correction
  against it.
- **r2's claim that the fix is correct and correctly scoped** → **CONFIRMED
  independently**, by byte-diffing the shipped original zip against the current
  package (two lines, 12 bytes) rather than by re-reading r2's record.
- **r2's claim of 0 surviving unapplied corrections** → **CONFIRMED** by my own
  110-pair sweep, self-tested, with shared-tail false positives excluded.
- **Mixed-number equivalent-form trap** → **REFUTED**, with the reason: both
  divisions resolve to integers, so no improper/mixed twin can be written.
- **"Right value, wrong unit" (label swaps)** → **REFUTED**; see §5(a).
- **Unsigned-magnitude distractors** → **REFUTED**; see §5(b), recorded as the
  weaker "true statement, different question" case per the rubric.
- **Finish-line double count** → **REFUTED as a source of ambiguity**; see §4.
  Both readings coincide because both divisions are exact.

---

## CLEAN

- **Part 1 Question 1** — corrected stem matches the assignment and the repo
  companion character-for-character; $450.75 and 3 owners confirmed from the
  rendered assignment page. Key `-150.25 per owner` reproduces the repo Part 1
  key. All 7 distractors recomputed false. 8 choices, no duplicate text, 1
  respcondition, correct/negated split exact, 1 instruction block, 1 currency
  `$`, no `\(`, no `src=`.
- **Part 1 Question 2** — untouched by the repair and verified from scratch.
  `\(15\dfrac{1}{2}\)` and `\(3\dfrac{7}{8}\)` confirmed against rendered pages
  of both the assignment and the companion. 15½ ÷ 3⅞ = 4 exactly; fourth station
  is the finish line. Key `4 water stations` matches the rendered Part 1 key.
  All 7 distractors false. Delimiters balanced 2/2, no `$`.
- **Part 2 Question 1** — corrected stem matches the assignment; $625.50 and
  5 owners confirmed from the render. Key `-125.10 per owner` reproduces the
  repo Part 2 key. All 7 distractors recomputed false. Structure and markup as
  above.
- **Part 2 Question 2** — untouched by the repair and verified from scratch.
  `\(16\dfrac{1}{2}\)` and `\(2\dfrac{3}{4}\)` confirmed by render.
  16½ ÷ 2¾ = 6 exactly; sixth stop is the finish line. Key `6 rest stops`
  matches the rendered Part 2 key. All 7 distractors false.
- **Package level** — manifest hrefs resolve; `assessment_meta.xml`
  points_possible 4.0 matches 4 × 1; staged zip and repo `qti/zips` copy both
  byte-identical to the package directory, so what I scored is what students
  receive.

---

## NON-SCORING OBSERVATIONS

Recorded so the next reader does not have to rediscover them. Neither bears on
the score, and I am not converting either into a note-shaped defect.

1. **Key is always the first choice, corpus-wide.** All 88 Shape A items list
   their `correct_*` ident first, and all 14 packages set
   `<shuffle_answers>false</shuffle_answers>`. In every Shape A item the answer
   is therefore choice A as rendered in Canvas. This is uniform corpus design,
   is outside the seven criteria, and is not specific to T1-9 — but a student who
   notices it can pass these checks without doing the arithmetic. Worth raising
   with the author at the corpus level, not against this slice.
2. **`/tmp/qtiwork/slices/T1-9.json` is a working file, not the artifact.** I did
   not read it. If any downstream consumer does, note that r2 reported it still
   carries the pre-fix stems; the package itself is correct.
