# Fix brief — frozen repair decisions

You are a **fixer**. Apply exactly the changes assigned to you. Do not judge, do
not add improvements, do not "tidy" anything not listed. The same judge that
found each defect will re-score your work.

## Where to work

Edit the extracted XML under `/tmp/qtiwork/pkg/<package>/`. Do **not** touch
`/home/user/ContinuityOps/inbox/` — the originals stay as the provenance record.
Repackaging is handled centrally after all fixes land.

## Rules

1. **Match the file's escaping exactly.** Stem and choice bodies live inside
   `<mattext texttype="text/html">` and are HTML-escaped one layer
   (`&lt;p&gt;`). Choice text carrying a comparison operator is escaped a
   second layer (`&amp;lt;`). Copy the surrounding convention; do not normalise it.
2. **Never change an ident** unless the assignment says to. Idents are the
   scoring key; a renamed ident silently unscores a choice.
3. If you change the set of choices, you must also update the
   `<respcondition>` block **and** the `original_answer_ids` metadata field.
4. Keep **8 choices** on every Shape A item. Never fix by deletion alone.
5. After editing, confirm the file still parses:
   `python3 -c "import xml.etree.ElementTree as ET; ET.parse('<file>')"`
6. Report what you changed, per item, old text -> new text. If an instruction
   does not match what you find in the file, **stop and report** — do not
   improvise. A mismatch means the brief is wrong, and guessing is how a fixer
   files a false self-report.

## Adjudicated decisions — these override individual judge suggestions

**SC-2 mixed/improper pairs (SC-2a P1Q7, P1Q11; SC-2b P2Q7).** Two judges
proposed different repairs. The decision is the **stem amendment**, applied
identically to all three items. In each stem replace

  `Select every choice that belongs in complete correct answer.`

with

  `Select every choice that belongs in complete correct answer, including every equivalent form of that answer.`

Leave the keys alone. Rationale: de-keying one form converts a criterion-4
defect into a criterion-2 one, because the mixed number and the improper
fraction are the same number — both judges reached that conclusion
independently. The answer key writes the two forms with "or", and the stem
amendment is what makes the two-form requirement derivable by a student.

**The "select all equivalent" cluster in 6th-grade Section 2.** The first-pass
audit flagged six items (K9, K10, K11, L1, N5, N6). Two judges on opposite sides
of the slice boundary independently derived the same test and reached the same
answer: for the property items the modifier constrains the **derivation**, so a
value-equal form arrived at by a different property is not what the stem asks
for. `13` is an evaluation, `(8+5)+0` is the additive identity, `(b+9)+3` needs
commutation, and the given expression restated is not a rewrite at all.

**K9, K10, K11, N5 and N6 are therefore NOT defects. Do not change them.**

**L1 is a defect** and is the only survivor of the cluster. There the modifier
"factored" describes the **form of the result**, not the derivation, and
`4(2x + 4)` = 8x + 16 is both equivalent and factored — squarely inside the class
the stem says to select all of. Repair by **narrowing the stem**, not by keying
the extra form:

  `Factor: 8x + 16 = Enter select all equivalent factored expressions.`
  ->
  `Factor: 8x + 16 completely, using the greatest common factor. Enter select all equivalent factored expressions.`

**Currency is not a math delimiter.** `$500`, `$450.75`, `$20`, `$8.75` and
every other bare `$` in front of a numeral is currency in plain HTML. Three
judges independently confirmed this. **Converting them to `\(...\)` would be a
regression. Leave every one alone.** Only the `$...$` *pairs* wrapping TeX
markup are defects, and they are listed individually below.

**T1-6 P1Q1 keeps its signed form with a parenthetical.** Unlike T1-8, this item
offers no competing Part B choice, so the repair is to match the answer key's own
notation rather than to swap two choices.
