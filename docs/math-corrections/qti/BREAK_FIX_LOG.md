
## 2026-08-08 — BF-2026-075 — The gate refused the orchestrator's ruling, and the gate was right

`FIXER-B` was told to narrow `g6_s2_k6` to the single instructed form `1 3/4`,
because the SHORTANS checklist found the item accepting `7/4` and `1.75` in
defiance of its own stem sentence *"Type it the same way it is written in the
question."*

The build stopped:

```text
K6: ACCEPTED VALUE DROPPED ['7/4'] -- a student who gave the pristine answer
is now marked wrong
```

### The instrument was correct and the ruling was not

`validate.py:369` computes `lost = keys_of(bbody) - keys_of(wbody)` — pristine
against work. It protects answers present in the **original** package, not
answers added by a later widening. That precision is why the same narrowing
passed for `f3` and `f4`: `subtract`, `subtraction`, `-8`, `−8`, `division` and
`divide` were widening additions and are legitimately droppable. `7/4` is
source-blessed.

`1 3/4`, `7/4` and `1.75` are one number. A student who writes `7/4` has solved
the problem. Failing them over a formatting sentence is a worse defect than the
superset that was reported, and it violates the standing bar that no student who
did the mathematics correctly is ever failed.

**Two ways existed to make the stem and the acceptance agree, and I chose the
harmful one.** Corrected: keep the accepted set, delete the notation sentence,
replace it with one naming the permitted forms. The item tests which of `1 3/4`
and `(1)(3/4)` is greater; it does not test mixed-number notation, so the
instruction was never load-bearing.

Recorded because a gate firing against its own author is the whole point of the
falsifiability doctrine, and this is the first time in the project it has
happened in that direction.

### Second defect in the same return: `f3` demanded the number as a word

`FIXER-B` closed `g6_s1_f3` to the single string `subtract eight`, having
rewritten the stem example from the source's `add 3` to `subtract three`.

That rejects `subtract 8` — the most natural form, and the one the item's own
original example implied. It is also inconsistent with `f4` one question later,
whose example stayed a numeral (`divide by 3`). Two adjacent items in one
section would have demanded opposite conventions for the same kind of answer.

**Closure does not mean one accepted string. It means a set that can be written
down completely.** Where the stem admits a numeral or a number word, both are
in. Corrected ruling: example stays a numeral, accept `subtract 8` and
`subtract eight`, keep rejecting the half-answers `subtract`, `subtraction`,
`-8`, `−8` — that half-acceptance was the actual `R4` defect.

### Standing

Corpus unchanged at **199 items**, build `81e700c3f40bb7b5`. Neither fixer's
build was applied. The generator's new accepted-set replacement capability is
retained but must stay opt-in per `TOSHORT` entry: a global switch to
replacement would let a future edit silently drop a pristine answer at any of
199 sites, and the rule that caught this one only fires while the pristine set
remains the comparison basis.
