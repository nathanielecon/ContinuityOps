# Worker directives (applies to ALL agents: fixers and judges)

## 1. Language + compression — caveman wenyan mode
The `caveman` skill is installed (~/.claude/skills/caveman). Invoke it and set
wenyan mode, which is Mandarin AND compressed in one setting:

    /caveman wenyan-full

Reason in Mandarin. Write your report back to the coordinator in Mandarin.
Caveman rules still bind: drop filler, no tool-call narration, no preamble.
Never drop a negation (not / never / no / only / except) to save a token —
flipping a defect's meaning is worse than any saving. Numbers and units exact.

### HARD GUARD — deliverables stay English
NO CJK character may enter any file under docs/math-corrections/.
These are US school worksheets for 7th graders. Mandarin is for your reasoning
and your report ONLY. File content stays English.

Before you finish, run on every file you touched:

    grep -nP '[\x{4e00}-\x{9fff}\x{3000}-\x{303f}\x{ff00}-\x{ffef}]' <file>

It must print nothing. If it prints, remove the characters and re-check.
A judge that finds CJK in a .tex file must score the slice 0 and say so.

This guard is why wenyan mode is safe here: the compression and the language
apply to YOUR REASONING AND REPORT, never to the artefact. Quoted LaTeX, defect
strings, worksheet wording and error text stay verbatim English inside your
Mandarin report — caveman's own rule is that technical terms, code and exact
error strings are never translated.

## 2. rtk — compress bash output
`rtk` (Rust Token Killer, v0.42.4) is installed at /usr/local/bin/rtk.
Prefix a shell command with `rtk` to filter/compress its output before it
reaches your context:

    rtk ls -la <dir>        # measured 1995B -> 719B (64% saving)
    rtk grep -n ... <file>
    rtk cargo build

USE IT for: ls, grep/rg, find, cat of long files, build output, git log/diff.
DO NOT use it for: commands whose output is already a few lines (on tiny
outputs rtk ADDS bytes — measured 160B -> 187B on `git status`), or when you
need byte-exact output for a measurement (e.g. extracting glyph coordinates).

Never let rtk stand between you and evidence you are about to score. If you are
verifying a rendered page, read the PDF directly.

## 3. Budget discipline
- One compile at the end, not per edit.
- Do not re-verify what the judge already passed.
- Do not re-read whole files when grep suffices.
