# Fixer addendum (token-lean mode)

> **Read `WORKER_DIRECTIVES.md` first** — it governs language (Mandarin reasoning
> and reporting, English-only deliverables) and rtk output compression.

## Reasoning language
Think in Mandarin. Internal reasoning only.

## HARD GUARD — output stays English
NO CJK character may enter any .tex file. Files are student-facing US school
worksheets. Reasoning = Mandarin. File content + your report = English only.
Before finishing run:
    grep -P '[\x{4e00}-\x{9fff}\x{3000}-\x{303f}\x{ff00}-\x{ffef}]' <yourfile>
Must print nothing. If it prints, remove the characters and re-check.

## Style
Terse. No preamble, no restating the task, no summary of what you are about to
do. Do the edit. Report in <=4 short lines.

## RESUME MODE (slices A B C D H)
A previous fixer was killed mid-work. Your file may be partly fixed already.
For EACH defect: check current state first. If already correct, skip it and say
"already done". Do not re-apply, do not revert. Only close what is still open.

## Budget
Do not re-verify things the judge already passed. Do not re-read whole files
when grep suffices. One compile at the end, not per edit.
