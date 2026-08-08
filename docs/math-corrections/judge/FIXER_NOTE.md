# Fixer note — round 1

## Already fixed centrally. DO NOT fix these in your slice file.
1. `\degF` / `\degC` swallowed the following space ("5degFand"). Fixed with
   \xspace in mathdocs.sty.
2. Orphaned lesson/question headings at page feet. Fixed by raising the
   heading reserve (\lessonneed / \questionneed) in mathdocs.sty, which the
   companions set to 10 / 8. This covers 1-5, 1-9, B2, K7, K10, M3, H6, J2.
3. Answer-key defects (Lesson 1-6 Q2 "4.5 minutes"->"change in height after 4.5
   seconds"; 1-5 Q2 "three drops"->"two drops"; 1-5 Q3 "two marks"->"the lookout
   and the mountain base"). The keys are not yours to edit.

If your judge's report lists one of the above, skip it — but DO re-check that it
actually looks fixed in your compiled output, and say so.

## Rules
- Edit ONLY your assigned part file(s) under
  /home/user/ContinuityOps/docs/math-corrections/tex/parts/.
- Do NOT edit mathdocs.sty or any other slice's file — other fixers are working
  in parallel and you will clobber them.
- Fix exactly the defects your judge listed. Do not "improve" anything else:
  the judge verified a long list of things as already correct, and changing them
  restarts the loop for no reason.
- Fidelity fixes mean quoting the source worksheet VERBATIM. Where a judge says a
  restatement invented context, delete the invention — do not reword it.

## Compiling without clobbering other fixers
Everyone shares one .tex tree, so compile to your OWN output directory:

    cd /home/user/ContinuityOps/docs/math-corrections/tex
    mkdir -p /tmp/build-<YOURSLICE>
    pdflatex -interaction=nonstopmode -output-directory=/tmp/build-<YOURSLICE> <DOC>.tex
    pdflatex -interaction=nonstopmode -output-directory=/tmp/build-<YOURSLICE> <DOC>.tex

where <DOC> is Topic1ExplanationsPart1 or 6thGradeReviewExplanations.
Read your pages back from /tmp/build-<YOURSLICE>/<DOC>.pdf and confirm each fix
with your own eyes. Zero LaTeX errors required.
Do NOT copy your build output over the shared PDF — the coordinator rebuilds once
at the end.
