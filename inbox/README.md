# Inbox — drop files here

Put source material here for the next session to pick up. Zips are fine.

## Where

```
inbox/                     <- this folder, at the repo root
```

**Path:** `nathanielecon/ContinuityOps` -> `inbox/`
**Branch:** `claude/deep-scan-typo-check-xuxtgw` (or tell me which branch you used)

Via the GitHub web UI: open the repo, switch to that branch, navigate to
`inbox/`, then **Add file -> Upload files**. Drag the zip in and commit.

## Naming

One folder or one zip per drop, named for what it is and when:

```
inbox/2026-08-06-canvas-quizzes.zip
inbox/2026-08-06-topic2-source/
```

Date first so drops sort chronologically. No spaces.

## Include a MANIFEST.txt

Inside the zip or folder, list what you put in and what it is:

```
MANIFEST.txt
------------
Topic1-Quiz-Part1.pdf      Canvas quiz, Topic 1 Part 1 - students check HW answers
Topic1-Quiz-Part2.pdf      Canvas quiz, Topic 1 Part 2
Topic2-IndependentPractice.pdf   assignment, Parts 1 and 2
NOTE: Topic 2 explanations not written yet
```

This matters more than it looks. The rule in `MASTER_PROMPT.md` is *do not plan
until every authoritative source is in hand* - the two worst errors of the last
run came from working with a partial set. A manifest lets me tell "you sent
everything" apart from "that is all that exists yet", which are very different
situations and are indistinguishable from the files alone.

## What happens to a drop

1. I `git pull`, unzip into place, and commit the **extracted** files - zips are
   opaque to diffs, so the extracted copy becomes the tracked source of truth.
2. I check the drop against its MANIFEST and report anything missing or extra
   **before** starting work.
3. Originals stay in `inbox/` untouched as the provenance record. I do not edit
   anything in here.

## Alternative: just upload in chat

Dropping files straight into the conversation works too and is faster for a
one-off - that is how every PDF in this project arrived. Use `inbox/` when you
want the material version-controlled next to the documents it verifies, which is
the better default for the Canvas quizzes since they need to be diffable against
the assignments they check.

## Not for

Secrets, credentials, student PII, or anything with a real student's name in it.
This is a public repository.
