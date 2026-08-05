# Worker directives (applies to ALL agents: fixers and judges)

## 1. Language + compression — caveman wenyan mode
The `caveman` skill is installed at /root/.claude/skills/caveman. NOTE: an
agent's available-skill list is fixed when it spawns, so an agent RESUMED from
an earlier transcript will not see it and cannot invoke `/caveman wenyan-full`.
That is expected — do not report it as a fault, and do not claim to have invoked
a skill you could not. Follow the rules below directly instead; they are the
substance of what the skill does.

Reason in Mandarin. Write your report back to the coordinator in Mandarin.
Caveman rules still bind: drop filler, no tool-call narration, no preamble.
Never drop a negation (not / never / no / only / except) to save a token —
flipping a defect's meaning is worse than any saving. Numbers and units exact.

### HARD GUARD — deliverables stay English
NO CJK character may enter any file under docs/math-corrections/.
These are US school worksheets for 7th graders. Mandarin is for your reasoning
and your report ONLY. File content stays English.

Before you finish, check every file you touched. **Use this Python check, not
grep.** The obvious grep incantation FAILS OPEN on this machine:

    grep -P '[\x{4e00}-\x{9fff}]' file    # -> "character code point value
                                           #     too large", prints nothing,
                                           #     exits 0. Looks clean. Is not.

Verified: a planted CJK character passes that command undetected. Use:

    python3 -c "
    import re,sys,glob
    pat=re.compile('[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')
    bad=[f for f in sys.argv[1:] if pat.search(open(f,encoding='utf-8',errors='replace').read())]
    print('CJK FOUND:',bad) if bad else print('clean')" <files...>

(`LC_ALL=C.UTF-8 grep -P` also works, but the Python check is the one to use —
it cannot fail silently.)

A judge that finds CJK in a .tex file must score the slice 0 and say so.
A judge that reports "clean" on the strength of the broken grep has not
checked at all.

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
