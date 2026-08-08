# AGENTS-2.0 — the QTI math-corrections workstream

**Scope.** This file governs work on `docs/math-corrections/qti/` — the 14 Canvas
QTI accuracy-check packages. It does **not** govern the ContinuityOps DR and
Terraform workstream; that is `AGENTS.md`, and its chief/junior supervisor seats,
Ralphy rounds, `PLAN.md` authority order and D-0xx decisions do not apply here.
If you were dispatched on a QTI task and find yourself reading about
`chief-pager` labels, you are in the wrong contract.

**Read this before anything else on a QTI task.** Where this file and `AGENTS.md`
conflict on a QTI task, this file wins.

---

## 1. What the work is, and why the standard is high

177 → 199 items across 14 packages let students self-check their maths homework.
Canvas scores short answer by **exact string match** — whitespace trimmed, case
folded, every internal byte literal. There is no equivalence grader anywhere in
Canvas.

That single fact sets the bar. A missing accepted spelling does not produce a
slightly worse quiz; it tells a student who did the mathematics correctly that
they got it wrong. Measured this round: a realistically hand-written accepted
list rejects **38%** of plausible correct answers on the riskiest items.

**The worst defect available here is an item that fails precisely the student who
followed the instruction.** Everything below exists to prevent that.

---

## 2. The frozen gate

Read in this order. Where the first two conflict, **FORMAT_ROUND wins** — it says
so itself.

1. `docs/math-corrections/qti/judge/COLD_BRIEF.md`
2. `docs/math-corrections/qti/judge/JUDGE_RUBRIC_QTI.md` — criteria 1–7
3. `docs/math-corrections/qti/judge/FORMAT_ROUND.md` — F1–F7
4. `docs/math-corrections/MASTER_PROMPT.md`

The gate is **frozen**: it is amended only between rounds, never mid-round, and
every amendment is recorded as a break-fix entry. F1 has been amended twice
(BF-2026-042, BF-2026-068); both are logged in the file itself.

---

## 3. Roles, and which ones compress

| role | job | caveman |
|---|---|---|
| **judge** | produce a frozen checklist, or score a slice against one | **NO — never** |
| **fixer** | work a checklist, emit a patch | yes |
| **investigator** | locate code, list call sites, census a corpus | yes |

**Judges do not compress, and this is not negotiable.** The gate demands a defect
format of *found / why / fix* with the mathematics worked in full, and
`COLD_BRIEF.md` demands an independently formed view. A compressed verdict is not
a verdict — **the reasoning is the artifact**, and it enters the permanent record
in `BREAK_FIX_LOG.md`. Every finding that has mattered in this project was worth
more than the tokens it cost.

**caveman**, for the roles that may use it, is a compression skill that works on
Codex as well as Claude Code — `juliusbrussee/caveman` upstream, and the Codex
port `yibie/caveman-codex`, which `.codex/cloud-setup.sh` vendors into
`.codex-plugins/caveman`. Enable with `$caveman`, at `lite`, `full` or `ultra`;
leave with `stop caveman`. Both paths are gitignored, so a fixer's unified diff
never carries plugin files.

Compression that is always safe, for every role:

- **Reason in Simplified Chinese; deliver in English.** Mandarin is denser per
  token and the saving is free. The deliverable enters an English record.
  Upstream caveman also offers a `wenyan` mode, denser still — but classical
  Chinese is a *compression of the output*, so it belongs to the roles that may
  compress, not to judges.
- **RTK** — see §4. It drops lines from tool output and is lossless on what
  remains.

---

## 4. RTK — the golden rule

Prefix commands with `rtk`. If RTK has a filter it uses it; if not it passes
through unchanged, so it is always safe.

```bash
rtk git status && rtk git diff          # not: git status && git diff
rtk grep 'pattern' path/
rtk ls docs/math-corrections            # measured here: 3181 -> 273 bytes
```

Even inside `&&` chains.

RTK filters *tool output only*. Every command it wraps runs identically without
it, so a worker missing RTK is slower, never wrong — which is why
`.codex/cloud-setup.sh` treats a failed install as non-fatal.

`.codex/cloud-setup.sh` pins `RTK_VERSION` and installs from `RTK_INSTALL_URL`,
which the author sets in the Codex environment. **Pin the version.** The
unpinned installer resolves "latest" through an unauthenticated GitHub API call,
which rate-limits in a cloud container and then fails the whole setup under
`set -e`.

---

## 5. pxpipe is prohibited on this workstream

pxpipe compresses by **rendering text as PNG images**. This project's entire
subject matter is exact-byte string matching — whether `8(x+2)` and `8 (x+2)` are
both accepted, whether an ASCII hyphen and U+2212 are both present. A judge
reading the corpus as pixels cannot reliably distinguish a space from no space,
or one minus glyph from another.

RTK is safe because it drops whole lines and is lossless on what survives.
pxpipe is not, because every character passes through a rasteriser. **Do not
route QTI work through it.**

---

## 6. Building and checking

```bash
cd docs/math-corrections/qti && ./build.sh
```

Extracts pristine packages from git ref `f63d392`, then runs `finalize.py` →
`permute.py` → `validate.py` → `battery.py` → `repackage.py`. Never build from the
working tree or from `zips/`; feeding the pipeline its own output is what made an
earlier artifact non-reproducible.

- `validate.py` — the structural gate. ~40 rules, each proved by injection.
- `battery.py` — derives answer probes **independently of the generator**, so it
  cannot rubber-stamp it. It found a real defect on its first run.
- Pin every verdict to `sha256sum zips/sha256sums.txt | cut -c1-16`.

**A green build is not a green slice.** Neither gate can see whether a stem asks
the right question or whether a key is mathematically correct.

---

## 7. Falsifiability is mandatory

> A gate that cannot fail proves nothing.

Every rule you add must be proved by **injecting the bug and watching the gate
fail**. Every claim that a rule is holed must be proved by constructing the input,
running the gate, and showing it passes.

Sweep the candidate space rather than reasoning from one exhibit. Twice this
round a hole looked unreachable after a few attempts and a full sweep then found
it open at every site; in both cases the exhibit was over-constrained, not the
defect narrow.

**Run positive controls first, and assert your mutation landed — in the parsed
tree, not the text.** Five consecutive rounds, a control caught an error in the
judge's own instrument: `root.iter('item')` returning 0 because QTI 1.2 declares a
default namespace; a parallel sweep sharing trial directories reporting false
passers; a trial directory named with `[...]`, which `glob` reads as a character
class, making every package invisible while 197 mutations reported "caught".

Suspect the instrument first. Instrument errors have outnumbered document defects
in every round of this project.

---

## 8. The recurring defect class

Twenty-plus instalments are recorded. **A rule narrower than its own comment or
message claims.** Its shapes:

- the same lesson applied at some sites and not the rest (worst ratio: 1 of 14);
- a **guard never itself asserted**, so the rule it protects silently does not run;
- a rule correct at one **granularity** and absent at the next one out;
- a **proxy** for the real invariant — a tag census where the property is
  arithmetic, containment, or identity;
- a **magic string** standing in for a structural property, or a substring for an
  attribute;
- **coverage** asserted where the criterion states a **partition**;
- the contents asserted and never the container, then the container and never
  *its* container;
- two censuses of one thing, reconciled by nothing, going blind together;
- a parse performed, used only for well-formedness, and thrown away.

When you fix a rule, ask where else that property is required. Then check there.

---

## 9. Output contracts

**Judges** emit prose. No patch, no PR, no `git push`. A checklist item must be
decidable true/false, tied to a named item or rule, and state the harm if false.

**Fixers** emit a `continuityops-patch-v1` block — `base_branch`, `base_sha`,
`context_remaining`, then a fenced unified diff. The `codex-patch-publish` Action
applies it and opens the PR. Your container has no git remote and no `gh`; do not
attempt to push.

**Never write** `.github/**`, any path holding a secret, `.env*`, or a binary
patch.

---

## 10. Acceptance

Two consecutive **10/10** verdicts per slice, pinned to one build hash, on content
that did not change between the reads. One from the judge that found the defects
re-scoring after repair; one from a cold judge reading fresh.

The author's threshold: **10/10 on mathematical accuracy and answer format —
non-negotiable.** 9.5 is sufficient for structure.

A rebuild that changes an accepted slice's text reopens it. A checklist frozen
against one corpus must be **re-derived, not amended**, when the corpus changes.

**A majority of judges is not evidence.** Two independent judges once reached the
same wrong answer because they reasoned from the same place; a third overturned
both by reading what the item said about itself.

---

## 11. What is blocked outside this environment

- **The live Canvas import.** `verify_canvas_import.py` is written and self-tests
  green, but needs a URL, token and scratch course that must not live in this
  repo. See `docs/math-corrections/qti/TEACHER_ACTIONS.md`.
- **Three paper defects** in the worksheet and the stale explanations companion.
  Verified not to leak into the corpus; they need a human with the source
  documents.
