# Acceptance ledger — QTI slices

A slice is **accepted** only on two consecutive 10/10 verdicts: one from the
judge that found its defects, re-scoring after repair, and one from a cold judge
reading the slice fresh at high effort.

Slices clean at r1 with no repair have no r2 round — their two reads are r1 and
cold.

| Slice | r1 | r2 | cold | Accepted |
|---|---|---|---|---|
| T1-1 | 6 | 10 | **10** | **yes** |
| T1-2 | 7 | 10 | **10** | **yes** |
| T1-3 | 8 | 10 | **10** | **yes** |
| T1-4 | 9 | 10 | **10** | **yes** |
| T1-5 | 7 | 10 | **10** | **yes** |
| T1-6 | 8 | 10 | **10** | **yes** |
| T1-7+10 | 10 | n/a | **10** | **yes** |
| T1-8 | 5 | 10 | | |
| T1-9 | 10 | n/a | | |
| SC-1 | 5 | 10 | | |
| SC-2a | 7 | 10 | | |
| SC-2b | 7 | 10 | | |
| G1a | 6 | 10 | | |
| G1b | 6 | 9 -> 10 (r3) | **10** | **yes** (content, at pre-format-round state) |
| G2a | 10 | n/a | | |
| G2b | 8 | 10 | | |

## G1b cold read closed the outstanding bottleneck — 10/10

18 of 18 items worked, no defects. It did not ratify: it ruled explicitly on nine
near-misses, and the two that mattered were the ones where a true-but-unkeyed
choice would actually hide — `H3/choice_6` and `H4/choice_6`, where an equivalent
flip (`5 < x` for `x > 5`) would have been a criterion-2 defect. It read the raw
entities to confirm both were the *reversed* form, and therefore false.

**It re-verified the H6/H7 arrowhead fix along three independent paths** rather
than taking r3's word for it: marker source (`markerUnits="userSpaceOnUse"`,
`refX="17"`, so the marker no longer scales with `stroke-width:5`), coordinate
geometry (leftward rays terminate at x=310, value −8, the open end), and a raster
render. Ink means membership and the ink is correct.

**Scope of this acceptance.** The cold read was taken against the corpus *before*
the answer-format round. Its finding is that the mathematics, keys, stems and
figures are sound. The answer-format round then converts several of these items
from select-all to single-answer multiple choice, which does not move a key but
does change the structure — so the type change is verified separately, and this
row is not a certification of the post-round file.

## G1b took three rounds

r2 closed the six original defects but opened a seventh: the leftward rays on
rows C and D of H6/H7 put their arrowhead at the circle rather than the open end.
`markerUnits="strokeWidth"` scales the marker by the ray's `stroke-width:5` to
45px, and `refX="9"` pins the tip at the circle, so the body painted a filled
wedge across ~1.73 units of the region the graph must leave blank. On a number
line ink means membership, so both rows depicted something other than what their
label claimed. r3 closed it.

I had recorded that defect as cosmetic and left it. The judge that owns those
items overruled me, quantified the geometry, prototyped the fix in its own
scratchpad and rendered it before recommending. It was right.

## A coordinator error, recorded because it nearly damaged the record

I accused that judge of fabricating a quotation. **The accusation was false and
the judge was right.**

I sent it four messages, not the two I remembered. The second read "Coordinator.
Your ruling stood and I applied your fix. Re-score G1b." and contained the
passage the judge quoted, verbatim. I lost track of having sent it, told the
judge in my third message that the provenance of the SVG write could not be
reconstructed, and in my fourth asserted it had invented the quotation.

The judge refused the amendment I demanded. I had asked it to write that I never
said the fix was applied; it declined on the ground that this would put a false
statement into the record to remove a true one, and restored the verbatim text
instead. That was the correct call, made under pressure from the party
commissioning its report.

The one error that was genuinely its own it had already found and owned before I
raised anything: it put quotation marks around a compressed paraphrase, having
applied a stricter standard to the md5 evidence in the same report than to its
own citation.

**This also resolves the 00:11:34 write, against me.** It was not unattributed.
I dispatched that fix, announced it to the judge, then lost the thread and
reported it as a mystery. The timestamps the judge produced were accurate
throughout.

## An instrument recommendation of mine that was wrong

I told the cold judges to verify delimiter nesting by an ordered scan of `\(`
and `\)` rather than by counting. The T1-5 cold judge tested that against the
known-broken original and found **the ordered scan passes on the broken text
too** — token order `\( \) \( \)` with depth never exceeding 1, while the second
span was actually the prose `C, then drops $1.85^\circ`.

Two checks do discriminate, and both are cleaner:
- **span-content inspection** — extract each `\(...\)` span and reject any
  containing prose or a `$`;
- **`$`/`\(` co-occurrence** — reject any `mattext` block containing both. This
  is the better test: corpus-wide, 39 blocks contain a bare `$` and exactly none
  of them also contains `\(`, so it flags all four original defects with no
  false positive on the legitimate currency stems.

An ordered scan that also tokenises `$` reports a false alarm on the currency
stems, because their `$` counts are odd, and would have sent a correct file back
around.
