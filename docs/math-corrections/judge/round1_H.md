JUDGE-H  slice g6e_H  (D1-D4, E1-E4, F1-F6)
SCORE 9/10  ROUND 1  VERDICT FAIL

1. [E1] Arithmetic / step logic: step 1 says "divide 5 / 8", then step 2 jumps to
   "8 into 50 is 6 ... remainder 2". The 50 is never derived (nothing says 8 does
   not go into 5, so append a 0), and the decimal point is never placed - step 4
   asserts 0.625 from the digits 6,2,5 without saying where the point goes.
   Internally inconsistent: steps 3 and 4 both narrate "Bring down 0", and the
   Important words block defines "bring down a digit" for exactly this move.
   -> insert "8 does not go into 5, so write 0. and bring down a 0 to make 50"
   before the current step 2, and state in the final step that the digits 6,2,5
   fall after the decimal point.

CONFIRMED CORRECT: F4 fully converted to the revision (Question "Undo x5",
Checked answer "divide by 5 (or /5)", steps 1-4 with the round trip 4->20->4,
Final answer, closing) with NO residual "multiply by 5" anywhere in the document;
F3 retains "subtract 8" in all four blocks; D3/D4 keep the "(decimal)" tag with
the answer rule; E1 stays telegraphic; E2/E3/E4 proportion displays correctly
spaced with the butterfly figures and the /N /N annotations; the "two diagonal
products (a x d and b x c)" fix applied; arithmetic checks (84/7=12, 4x=140->35,
90=6x->15); all restatements match the revised worksheet in wording, numbers and
answer-slot form; no orphaned headings; no glyph collisions; true superscripts;
money renders correctly.
