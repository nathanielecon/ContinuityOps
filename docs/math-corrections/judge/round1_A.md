JUDGE-A  slice t1e_A  (front matter, Lesson 1-1 Q1-4, Lesson 1-2 Q1-3)
SCORE 7/10  ROUND 1  VERDICT FAIL

1. [1-1 Q1] Residual vocabulary from the WITHDRAWN 4.5 m version: the bullets
   "Downward means the opposite direction of up." and "To flip the direction
   means change up<->down (or + <-> -) while keeping the same size." are used
   nowhere in Q1's asking line, its 11 steps, its Final answer or its closing.
   -> delete both.
2. [1-1 Q1] Ten Important-words bullets the submarine item never uses and does
   not support (Nonzero, a/b fraction, Tenths/Hundredths, decimal, whole number,
   terminating decimal, repeating decimal, rational number incl. "18 = 18/1").
   These are Lesson 1-2 vocabulary preloaded into a Lesson 1-1 signed-number
   question. -> trim to the terms the steps use: signed number, positive,
   negative, sum, additive inverse, cancel, vertical, sea level, rise, descent,
   integer.
3. [1-1 Q2] UNAPPLIED logged correction (findings_verified.json, notation,
   medium): "Absolute value of a number, written | |" must read "written |x|".
   Currently still renders as an empty bar pair.
4. [1-1 Q3] Same unapplied correction, 2nd occurrence: "Absolute value | | means
   distance from zero" -> "Absolute value |x| means ...".
   NOTE: judge reports the empty bar pair also occurs in Lesson 1-4 and 1-5
   (slice C) -> sweep all occurrences.
5. [1-2 Q2] Fidelity: option A restated as "A) The decimal terminates (stops)."
   The worksheet reads "A) The decimal terminates." -> drop the gloss. Answer
   choices are text the student must match.
6. [1-1 Q2] Fidelity: stem split into two sentences. Worksheet reads
   "We have two mystery numbers, a and b, where a < 0, b > 0, and a + b = 0."
   -> restore the single sentence with "where".
7. [1-2 Q3] Breaks the slice's own pattern: (a) its two Important-words bullets
   are the only ones with the defined term NOT italicised; (b) "What the question
   is asking" is a bare imperative instead of the house "This question asks ..."
   form; (c) the repeating-bar overline notation is introduced here and never
   defined. -> fix all three.
8. [1-2 Q3] Step 3 reads only "Subtract: 99x = 27" - does not say what is
   subtracted from what, in a document whose steps are otherwise atomic.
   -> "Subtract the first equation from the second: 100x - x = 27.27... - 0.27...,
   so 99x = 27."
9. [1-2 Q1 and Q2] Full-size \frac set inline in running text stretches leading
   and breaks lines badly (asking line for 3/8; the Q2 stem, where the tall
   fraction pushes "NOT possible?" onto its own line). The same fraction is set
   inline-small three lines below on the same page. -> use \tfrac or x/y in all
   running text.

CONFIRMED CORRECT: Q1 stem/checked answer/11 steps/final answer all match the
submarine item and the key; Part A and Part B both answered; Q2 |a|=|b|;
Q3 |-9|=9 with tight bars; Q4 order; 1-2 Q1 0.375 (long division recomputed);
1-2 Q2 answer C; 1-2 Q3 Jordan / 3-11ths. Lesson headings correct. The
withdrawn climber stem has not crept back.
