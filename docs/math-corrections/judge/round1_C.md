JUDGE-C  slice t1e_C  (Lesson 1-4 Q1-4, Lesson 1-5 Q1-3)
SCORE 7/10  ROUND 1  VERDICT FAIL

1. [1-4 Q1] ROOT CAUSE typography: \degF in mathdocs.sty has no \xspace, so TeX
   eats the following space. Renders "5degFand -8degFare." and "8degFbelow zero".
   3 occurrences on one page. -> CENTRAL FIX: add \xspace to \degF and \degC.
2. [1-5 Q1] Orphaned headings: page ends with "Lesson 1-5: Add and Subtract
   Rational Numbers" + "Question 1" and no body. Same class as the logged 1-4 Q3
   fix. -> CENTRAL FIX: raise \needspace on \lesson/\question.
3. [1-5 Q1] Fidelity: "a fee of $15 each month"; assignment says "$15.00".
4. [1-5 Q1] Fidelity: "Another bank account starts with $200."; assignment says
   "An account starts with $200." ("Another" has no antecedent.)
5. [1-4 Q2,Q3] FABRICATION: invented opening sentences "Two birds are flying in
   the sky." / "Two fish are swimming beneath the water."; Q3 also recasts
   "Fish A is 25 ft below sea level (-25 ft)" as "Fish A's elevation is -25 feet
   relative to sea level." -> restate exactly as the worksheet does.
6. [1-4 Q1 / 1-5 Q3] Fidelity: Q1 drops "dropped to"; 1-5 Q3 drops "between
   them". -> match the assignment wording.
7. [KEY DEFECT, mine] Topic1Part1Solutions 1-5 Q2 says "Temperature after the
   three drops." The assignment has TWO drops (2.4 then 1.85). The companion is
   right. -> "after the two drops". Also key 1-5 Q3 says "the two marks"; the
   source objects are a lookout and a mountain base.

CONFIRMED CORRECT: all seven questions' arithmetic (13degF, 30 ft, 15 ft,
11+9=20 floors; 140 with the month chain; -8.00; 4.25). The three newly added
key entries agree with companion and assignment on VALUES. Tight abs bars
verified at glyph level (zero gap). The 1-4 Q1 number line is to scale
(35.15pt per 2 units), dots land exactly on -8 and +5, math minus labels, the
stray crowding "5" is gone. All logged corrections for the slice applied; no
dismissed finding crept back.
