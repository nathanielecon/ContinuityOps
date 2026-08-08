# Standing author rulings — QTI math corrections

**Every judge, nixer, fixer and reviewer on this workstream must read this before
reporting a defect.** These are decisions the author has made, with the trade-off
stated at the time. They are **settled**. Reporting one as a defect wastes a
round and, worse, produces a fixer patch that undoes a deliberate choice.

Each entry records what was decided, what it costs, and what a worker should do
if it finds the cost recurring. **Surfacing the cost is welcome. Re-litigating
the decision is not.**

---

## AR-1 — F1 and F2 stay open production

`g6_s1_f1` ("In 7m, the number 7 is the ____") and `g6_s1_f2` ("In n + 8 = 12,
n is the ____") present a blank and ask the student to **produce** a vocabulary
term. They must **not** enumerate candidate words in the stem.

A cold SOURCE judge correctly found that an enumerated candidate list converts
production into recognition — a student who cannot recall `coefficient` can
still reach it by eliminating visibly false options. Put to the author with the
trade stated plainly: nothing here is at once source-faithful, auto-gradable,
and incapable of failing a correct student. **The author chose source fidelity.**

**The accepted cost:** the accepted set is wide but **not provably closed**.
Canvas compares bytes, so an unlisted correct synonym is marked wrong. Terms
surfaced and added so far: `factor`, `numerical factor`, `multiplier`,
`numerical multiplier` on F1; `unknown quantity`, `unknown variable` on F2.

**If you find another defensible rejected term: report it.** The author wants
the recurrence rate visible. Do not propose closing the stem.

## AR-2 — Near-identical Part 1 / Part 2 items are correct

`1_2_part_1_question_2` and `1_2_part_2_question_2` differ only in variable
letters (`x/y` versus `a/b`). **The author ruled they are two separate
questions.** Part 1 and Part 2 are parallel practice sets throughout this
corpus — the same exercise posed twice with variables or numbers changed, so a
student can check one and then the other. `1_6_part_1_question_3` keys
`(-5)² = 25` while its Part 2 twin keys `(-6)² = 36`; the pattern is everywhere.

**Do not report parallel Part 1/Part 2 phrasing as duplication or as forbidden
harmonisation.** This has now been raised twice and overturned twice.

The forbidden-harmonisation rule protects something narrower and real: P1Q2's
*"which outcome is NOT possible"* framing must not be flattened into P2Q2's
framing **or vice versa**, because that negation is what makes its distractors
false. Substituted variables are not that.

## AR-3 — Comparison items carry the full symbol palette

Items requiring a comparison offer `<`, `>`, `=`, `≠`, `≥`, `≤` as copyable
characters. **The author asked for every symbol a student might need**, including
`≥` and `≤`, even where the source question offered a narrower set.

Rationale: a student cannot type `≥` without a source to copy from, and an item
that requires a character the student cannot produce fails them for their
keyboard rather than their mathematics.

**Do not propose narrowing a symbol palette to the source's offered set.** If a
non-strict symbol makes a *different* statement true and is wrongly accepted as
a key, that is a real finding — report the wrong acceptance, not the palette.

## AR-4 — A1 asks for 4 or −4

`g6_s1_a1b` plots the point four units left of zero. The source's section A
question 1 asks only about positive 4. **The author ruled the item should say
"plot at 4 or −4"**, so the second point is deliberate, not invented.

**Do not report `g6_s1_a1b` as a source-identity failure or propose removing
it.**

## AR-5 — Splitting for gradability is sanctioned; broadening is not

Stick with what the source asked, **unless** a question was split purely to make
automatic grading possible. Splitting for gradability is fine. Changing what is
being asked is not.

A split family must, taken together, demand exactly what the source demanded —
no additional result, no dropped result. An item that scores a value the source
never requested **is** a real finding under this rule; an item that splits one
source demand into two deterministically gradable halves is not.

## AR-6 — Never fail a student who did the mathematics correctly

The governing bar, and the tie-breaker whenever two repairs are both defensible.

Where a stem and its accepted set disagree, there are always two ways to make
them agree: narrow the acceptance, or fix the instruction. **Choose the one that
fails nobody.** `validate.py` enforces one half of this mechanically — it
refuses to drop an answer the pristine package accepted — and it has overruled
the orchestrator twice and been right both times.

Corollary: closure does **not** mean one accepted string. It means a set that
can be written down completely. Where a stem permits a numeral or a number word,
both are in.

---

## How to raise something covered here

If you believe a ruling produces a concrete harm, **report the harm with the
exact student string and the mathematics worked** — do not silently patch
against the ruling, and do not restate the design objection. The author decides;
the supervisor relays. A finding that names a rejected correct answer under AR-1
is exactly what is wanted. A finding that says F1 should enumerate candidates is
not.
