# Rebuild Brief — corrected LaTeX reconstruction

You are transcribing a slice of an existing PDF into LaTeX **and applying the
agreed corrections as you go**. The output is a corrected replacement for the
original document.

## Absolute rules

1. **Transcribe, do not rewrite.** Reproduce the assigned pages faithfully:
   every question, every Important-words bullet, every numbered step, every
   "Why this makes sense" paragraph, in the original order and wording.
   The ONLY wording you may change is a correction listed for your range
   (or a defect of the same class as one listed — see "Pattern fixes").
   Do not summarise, condense, drop bullets, or invent new content.
2. **Read the rendered PDF.** `Read(file_path=..., pages="N-M")`. The plain-text
   extraction in `scratchpad/extract/` fuses words across bold/italic runs
   (`Nonzeromeans`) and flattens exponents (`32 ×3 4` is really `3^2 \times 3^4`).
   Use the extraction only as a typing aid; the render is the source of truth.
3. **Output a LaTeX FRAGMENT**, not a full document. No `\documentclass`,
   no `\begin{document}`. Your file is `\input`-ed into a wrapper that already
   loads `mathdocs.sty`.
4. **Use only the shared macros** (below). Do not define new commands, do not
   `\usepackage` anything, do not change font sizes.
5. **Compile-safe.** Escape `$ % & # _ { }` in prose. Every `$…$` balanced.
   No unicode math glyphs — write `\times`, `\div`, `-`, `\le`, `\ge`, `\neq`,
   `\Rightarrow`, `\to`, `\ldots` in math mode. Degrees: `\degF` / `\degC`.

## Shared macros (from mathdocs.sty)

```latex
\lesson{Topic 1-3 Add Integers}      % lesson banner
\question{Question 2}                 % question banner
\blockhead{Question}                  % bold heading on its own line
  % also: \blockhead{What the question is asking}
  %       \blockhead{Important words}
  %       \blockhead{Work the problem one tiny step at a time}
  %       \blockhead{Why this makes sense}
\checked{+4.5 + (-4.5) = 0}           % renders "Checked answer: ..."
\finalans{4.5 meters downward}        % renders "Final answer: ..."
\runin{Part A:}Represent both changes  % bold label + guaranteed space
\begin{words} \item ... \end{words}   % Important-words bullet list
\begin{steps} \item ... \end{steps}   % numbered "Work the problem" steps
\term{Nonzero}means not equal to zero % italic term + guaranteed space
\abs{-9}          % |-9| with tight interior minus
\barsym           % the bare bar-pair symbol, e.g. "written \barsym"
\mixed{15}{1}{2}  % 15 1/2 mixed number
\money{425}       % $425
\degF \degC
\numline{-9}{0}{3}{-9}        % number line min/max/step/marked points
\blanknumline{0}{8}{1}        % unmarked number line
```

Notes:
- `\term{X}` already emits the trailing space — write `\term{Nonzero}means …`.
- `\runin{Part A:}` likewise — write `\runin{Part A:}Represent …`.
- For a negative inside absolute-value bars ALWAYS use `\abs{-9}`, never
  `$|-9|$` (which renders as `| − 9|` with binary-minus spacing).
- For negative money write `$-\$150.25$`, never `\money{}` after a minus.

## Pattern fixes to apply everywhere in your range

These were found across the corpus; apply them wherever they occur in your
pages even if not individually listed for your range:

| Defect | Fix |
|---|---|
| `| − 9|` binary-minus inside bars | `\abs{-9}` |
| `written ||` (empty bars) | `written \barsym` |
| `$ − 150.25` | `$-\$150.25$` |
| ~~`Lesson SC-1:` -> `Topic SC-1`~~ | **SUPERSEDED — see RECONCILE.md section F.** The assignment and the weekly plan both use `Lesson N-M: Title`. Lesson headings are `Lesson 1-1:`, `Lesson SC-1:`, `Lesson SC-2:`. `Topic 1` names the unit only. |
| Hyphen `-12` as a negative in prose or figures | math minus `$-12$` |
| Tight operators `6+6+1` | spaced `$6 + 6 + 1$` |
| `Important words box` in prose | `Important words list` |
| Bare money in prose where the question uses `$` | add `\$` consistently |
| Term defined but not italicised | wrap in `\term{...}` |
| Heading orphaned from its list | the `\blockhead` macro already calls `\needspace`; just use it |
| Body text smaller in one section | do not reproduce — use normal size throughout |

## Corrections specific to your range

Read `scratchpad/findings_all.json` and filter to your document and page range.
Apply every finding whose `correction` is a concrete text replacement.
Skip findings whose `correction` only proposes restructuring the assignment
(e.g. "merge these two sections", "drop this question") — those are logged as
recommendations, not applied.

## Deliverable

Write your fragment to the exact path given in your assignment.
Then reply with AT MOST 5 lines: the file path, the page range covered, the
number of questions transcribed, and any correction you chose not to apply
(with a one-line reason). **Do not paste the LaTeX into your reply.**
