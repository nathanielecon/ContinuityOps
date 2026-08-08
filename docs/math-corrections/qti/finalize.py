#!/usr/bin/env python3
"""Bring the corpus onto the author's answer-format rule.

  Numeric entry is the default. One part per question. No units in the answer.
  The stem states the format of the number expected. Select-all survives only
  where the answer genuinely is not a number.

Three passes, all by string surgery on the raw assessment XML so that untouched
items stay byte-identical:

  1. CONVERT  -- single-key select-alls whose key is a number wearing a unit
                 ("-8*C", "4 water stations", "n = 12") become numeric entry.
  2. SPLIT    -- the eight Part A / Part B items become sixteen questions. A
                 part whose answer is a number becomes numeric entry; a part
                 whose answer is an expression or an explanation stays
                 select-all, carrying only its own choices.
  3. BOILER   -- after the splits no select-all item has parts any more, so the
                 "Part 1 and Part 2 both must be correct" sentence is removed
                 rather than reworded. It referred to labels that never existed:
                 the items label their parts A and B, and "Part 1" is the name
                 of the quiz's first half.

Every keyed value below was recomputed from its own stem before being written
here; none is copied from the choice text it replaces.
"""
import glob, os, re, html, shutil, sys
from decimal import Decimal, ROUND_HALF_UP

# --------------------------------------------------------------------------
# Pass 1 -- single-key numeric conversions. (value, format sentence)
# The format sentence always ends with the same "number only" clause the 43
# already-converted items use, so a student meets one instruction, not two.
# --------------------------------------------------------------------------
ONLY = 'Enter the number only, no units or symbols.'

# BF-2026-034: a format clause is added ONLY where the format is genuinely in
# question -- the answer can be negative, rounding is required, or a decimal is
# expected. Where the answer is an unambiguous non-negative whole number the bare
# clause is used verbatim, matching the 39 numeric items already shipped. Adding
# an integer/sign sentence everywhere would have created a third instruction
# variant and handed the student two instructions where the brief asks for one.
# BF-2026-035: "Enter the number only, no units or symbols" is readable as
# "omit the minus sign". Any item whose answer can be negative must say so.
SIGNED = 'Include the negative sign if the answer is negative. ' + ONLY
KM = ('Round to the nearest kilometer and enter that whole number, and include '
      'the negative sign if the answer is negative. ' + ONLY)

CONVERT = {
    # -3.75 - 2.4 - 1.85 = -8      /      -4.6 - 1.35 - 2.05 = -8
    ('topic-1-5', 'Part 1 Question 2'): ('-8', SIGNED),
    ('topic-1-5', 'Part 2 Question 2'): ('-8', SIGNED),
    # 2.5 - (-1.75) = 4.25         /      3.25 - (-2.5) = 5.75
    ('topic-1-5', 'Part 1 Question 3'): ('4.25',
        'Enter your answer as a decimal. ' + ONLY),
    ('topic-1-5', 'Part 2 Question 3'): ('5.75',
        'Enter your answer as a decimal. ' + ONLY),
    # 250.50 * 4.5 = 1127.25 m down = -1.12725 km -> -1
    ('topic-1-6', 'Part 1 Question 2'): ('-1', KM),
    # 180.25 * 3.5 = 630.875 m up = 0.630875 km -> 1
    ('topic-1-6', 'Part 2 Question 2'): ('1', KM),
    # -18/6 = -3 = n/-4 -> n = 12  /      -24/8 = -3 = n/-3 -> n = 9
    ('topic-1-8', 'Part 1 Question 4'): ('12', ONLY),
    ('topic-1-8', 'Part 2 Question 4'): ('9', ONLY),
    # 15.5 / 3.875 = 4             /      16.5 / 2.75 = 6
    ('topic-1-9', 'Part 1 Question 2'): ('4', ONLY),
    ('topic-1-9', 'Part 2 Question 2'): ('6', ONLY),
    # 3^2 * 3^4 = 3^6 = 729        /      2^3 * 2^5 = 2^8 = 256
    ('topic-sc-2', 'Part 1 Question 1'): ('729', ONLY),
    ('topic-sc-2', 'Part 2 Question 1'): ('256', ONLY),
}

# --------------------------------------------------------------------------
# topic-1-4 -- six select-all items become twelve short-answer items, one
# expression each. The worksheet asks the student to WRITE expressions, and the
# author's hierarchy puts short answer above select-all for that.
#
# Splitting by FORM (subtraction vs absolute value) rather than by "write a
# different one" is what makes this safe: Canvas cannot compare one item's
# answer with another's, so "a different expression" would accept the same
# string twice. Form-a strings contain no "|" and form-b strings all do, so the
# two accepted sets are provably disjoint.
#
# Every accepted string below was evaluated against the item's true distance.
# The spaced twin of each is accepted as insurance against a correct student who
# ignores the no-spaces instruction -- being marked wrong for a spacing choice
# is exactly the harm this project exists to prevent.
# --------------------------------------------------------------------------
FORM_A = ('Type only the expression, with no words, no units, no equals sign, '
          'and do not work out the answer. Use a minus sign and no '
          'absolute-value bars. Type it with no spaces: write 4-(-9), not '
          '4 - (-9). That example shows spacing only, not the correct order '
          'for this problem. Remember that a distance is never negative.')
FORM_B = ('Type only the expression, with no words, no units, no equals sign, '
          'and do not work out the answer. Use the vertical bar key | for the '
          'absolute-value bars, not the letters abs. Type it with no spaces: '
          'write |4-(-9)|, not | 4 - (-9) |. That example shows spacing only, '
          'not the correct order for this problem.')

# --------------------------------------------------------------------------
# Method clauses. A stem that says only "uses absolute-value bars" leaves an
# OPEN family -- the answer key's own wording is "any correct distance
# expressions", and two rounds of widening each turned up more correct forms
# still rejected. What closes a set is naming the methods, which is the same
# device every other short-answer item in this corpus uses.
#
# The second method is NOT the same for every item, and this is easy to get
# wrong: it depends on whether the two values straddle zero.
#
#   Part 1 Question 1 alone straddles (5 and -8), so the two distances from
#   zero ADD:            |-8|+5 = 13.
#   The other five sit on one side, so they SUBTRACT:
#                        |150|-|120| = 30.
#
# Naming "the sum" globally would be wrong for five of six items -- on
# Part 1 Question 2 it would name a method yielding 270, not 30. Verified by
# evaluating every accepted string: Part 1 Question 1 has 8 sum-shaped forms
# and 0 difference-shaped; the other five have 0 sum-shaped.
# --------------------------------------------------------------------------
A_ONE = ''
A_TWO = (' You may either subtract the two given elevations, or subtract the '
         'smaller distance from zero from the larger.')
B_SUM = (' You may either write one absolute value of a difference, or add '
         'the two distances from zero.')
B_DIFF = (' You may either write one absolute value of a difference, or '
          'subtract the smaller distance from zero from the larger.')

# (context, distance phrase, accepted form a, accepted form b,
#  (form-a method clause, form-b method clause))
SHORTANS = {
    ('topic-1-4', 'Part 1 Question 1'): (
        'At 6:00 PM, the temperature was 5\\(^\\circ\\)F. By midnight, the '
        'temperature was \\(-8^\\circ\\)F.', 'distance between the two temperatures',
        ['5-(-8)', '5 - (-8)', '5--8', '5 - -8'],
        # the |-8|+5 family is the "split the trip at zero" method, which the
        # answer key itself lists. The stem must stay form-general ("uses
        # absolute-value bars") -- saying "bars around a subtraction" would make
        # the key's own method off-form and mark a correct student wrong.
        ['|5-(-8)|', '|-8-5|', '|(-8)-5|', '|-8|+5', '5+|-8|', '|5|+|-8|',
         '|-8|+|5|', '|5--8|', '|5 - (-8)|', '|-8 - 5|', '|(-8) - 5|',
         '|-8| + 5', '5 + |-8|', '|5| + |-8|', '|-8| + |5|', '|5 - -8|'],
        # the only item whose values straddle zero, so the two distances ADD
        (A_ONE, B_SUM)),
    ('topic-1-4', 'Part 1 Question 2'): (
        'Two birds are flying in the sky. Bird A is 150 feet above sea level. '
        'Bird B is 120 feet above sea level.', 'vertical distance between the birds',
        ['150-120', '150 - 120'],
        ['|150-120|', '|120-150|', '|150 - 120|', '|120 - 150|',
         '|150|-|120|', '|150| - |120|'],
        (A_ONE, B_DIFF)),
    ('topic-1-4', 'Part 1 Question 3'): (
        "Two fish are swimming beneath the water. Fish A's elevation is "
        '\\(-25\\) feet relative to sea level. Fish B\'s elevation is \\(-40\\) '
        'feet relative to sea level.', 'vertical distance between the fish',
        # the key lists only 40-25, but -25-(-40) is equally valid and is what a
        # student working from the signed elevations writes. Omitting it would
        # be a wrong-answer generator.
        ['-25-(-40)', '(-25)-(-40)', '40-25', '-25--40', '-25 - (-40)',
         '(-25) - (-40)', '40 - 25', '-25 - -40'],
        ['|-25-(-40)|', '|-40-(-25)|', '|(-25)-(-40)|', '|(-40)-(-25)|',
         '|40-25|', '|25-40|', '|-25--40|', '|-40--25|', '|-25 - (-40)|',
         '|-40 - (-25)|', '|(-25) - (-40)|', '|(-40) - (-25)|', '|40 - 25|',
         '|25 - 40|', '|-25 - -40|', '|-40 - -25|',
         '|-40|-|-25|', '|-40| - |-25|', '|40|-|25|', '|40| - |25|'],
        # |-25+40| and its spaced twin were REMOVED here (BF-2026-047). They
        # were added in an earlier widening round when the stem was still
        # form-general ("uses absolute-value bars"), where they were genuinely
        # on-form. Under the method-naming stem they are not: -25+40 is a SUM,
        # and neither named method produces it. Keeping them accepted one
        # ordering while rejecting the mirror |-40+25|, which is equally correct
        # and equally reachable -- arbitrary, and the asymmetry is the defect.
        # Adding the mirror instead would readmit sums generally and reopen the
        # family, which is what F1 forbids. Ten sibling items carry no sum form.
        # form a admits two methods here too: the key lists 40-25, and a student
        # working from the signed elevations writes -25-(-40). Both stay on-form.
        (A_TWO, B_DIFF)),
    ('topic-1-4', 'Part 2 Question 1'): (
        'At 7:00 AM, the temperature was 3\\(^\\circ\\)F. By noon, the '
        'temperature was 12\\(^\\circ\\)F.', 'distance between the two temperatures',
        ['12-3', '12 - 3'],
        ['|12-3|', '|3-12|', '|12 - 3|', '|3 - 12|',
         '|12|-|3|', '|12| - |3|'],
        (A_ONE, B_DIFF)),
    ('topic-1-4', 'Part 2 Question 2'): (
        'Two planes are flying in the sky. Plane A is 280 feet above sea level. '
        'Plane B is 210 feet above sea level.', 'vertical distance between the planes',
        ['280-210', '280 - 210'],
        ['|280-210|', '|210-280|', '|280 - 210|', '|210 - 280|',
         '|280|-|210|', '|280| - |210|'],
        (A_ONE, B_DIFF)),
    ('topic-1-4', 'Part 2 Question 3'): (
        "Two submarines are traveling beneath the water. Submarine A's "
        'elevation is \\(-18\\) feet relative to sea level. Submarine B\'s '
        'elevation is \\(-45\\) feet relative to sea level.',
        'vertical distance between the submarines',
        ['-18-(-45)', '(-18)-(-45)', '45-18', '-18--45', '-18 - (-45)',
         '(-18) - (-45)', '45 - 18', '-18 - -45'],
        ['|-18-(-45)|', '|-45-(-18)|', '|(-18)-(-45)|', '|(-45)-(-18)|',
         '|45-18|', '|18-45|', '|-18--45|', '|-45--18|', '|-18 - (-45)|',
         '|-45 - (-18)|', '|(-18) - (-45)|', '|(-45) - (-18)|', '|45 - 18|',
         '|18 - 45|', '|-18 - -45|', '|-45 - -18|',
         '|-45|-|-18|', '|-45| - |-18|', '|45|-|18|', '|45| - |18|'],
        # |-18+45| removed for the same reason as its Part 1 twin -- see above.
        (A_TWO, B_DIFF)),
}


# --------------------------------------------------------------------------
# F-1 -- additional distractors so every text select-all carries >=7.
#
# The bar was documented twice (rubric criterion 6: ">=8 choices"; the plan:
# ">=7 close distractors") but validate.py enforced MIN_CHOICES = 7, i.e. six
# distractors on a single-key item. 26 of 34 select-all items were below the
# documented bar and nothing could see it.
#
# Every string below is FALSE as an answer to its own stem, with the reason
# worked in the comment. Checked against the forbidden-near-miss list in
# CHANGES.md -- several obvious-looking additions are TRUE and are recorded
# there precisely so they are never authored in:
#   (3 + b) + 9   value-true reordering, not an associative rewrite
#   7a x 1        identically 7a
#   27/99         = 3/11, the very value the item asks for
#   -2 after all three turns of 10, -4, -8
# --------------------------------------------------------------------------
ADDWRONG = {
    # 6y - 2y = 4y. -4y reverses the subtraction; it is not 4y.
    ('6th-grade-review-section-1', 'F5'): ['-4y'],
    # 3(y + 6) = 3y + 18. 3y + 9 adds 3 + 6 instead of multiplying.
    ('6th-grade-review-section-1', 'G1'): ['3y + 9'],
    # 8x and 1 are NOT like terms, and likeness is not why it is linear.
    ('6th-grade-review-section-2', 'K1'): ['Yes; because 8x and 1 are like terms'],
    # 2 x 3 x 15 = 90, but 15 is composite, so it is not a PRIME factorization.
    # Same trap as the existing 9 x 10 and 2 x 45: the load-bearing word is "prime".
    ('6th-grade-review-section-2', 'K2'): ['2 × 3 × 15'],
    # the original expression with +0 appended -- not the two addends reversed.
    ('6th-grade-review-section-2', 'K9'): ['8 + 5 + 0'],
    # a^7 is a multiplied by itself 7 times, not 7 x a.
    ('6th-grade-review-section-2', 'K10'): ['a^7'],
    # b + (3 - 9) = b - 6. Grouping moved but the operation changed too.
    ('6th-grade-review-section-2', 'K11'): ['b + (3 - 9)'],
    # 2(4x + 8) = 8x + 16, but 4x + 8 still has a common factor of 4, so the
    # factorization is not COMPLETE. Same category as the existing 4(2x + 4).
    ('6th-grade-review-section-2', 'L1'): ['2(4x + 8)'],
    # 7 - a is subtraction, not the same operation reversed.
    ('6th-grade-review-section-2', 'N5'): ['7 - a'],
    # x + (5 - 8) = x - 3. Grouping moved but the operation changed too.
    ('6th-grade-review-section-2', 'N6'): ['x + (5 - 8)'],
    # (12-4)-3 = 5 and 12-(4-3) = 11. "8 and 11" stops at the intermediate 12-4.
    ('6th-grade-review-section-2', 'N7'): ['No; 8 and 11'],
    # rises 18 then descends 18 -> +18 and -18. The second value is wrong.
    ('topic-1-1', 'Part 1 Question 1a'): ['+18 and -17'],
    # (+18)/(-18) = -1, not 1.
    ('topic-1-1', 'Part 1 Question 1c'): ['Their quotient is 1.'],
    # descends 24 then climbs 24 -> -24 and +24. Both negative is wrong.
    ('topic-1-1', 'Part 2 Question 1a'): ['-24 and -24'],
    ('topic-1-1', 'Part 2 Question 1c'): ['Their quotient is 1.'],
    # 10x = 2.7272..., not 27. And 0.2727... = 3/11, so it IS a fraction.
    ('topic-1-2', 'Part 1 Question 3'): [
        'If x = 0.272727..., then 10x = 27.',
        'Casey is correct because 0.272727... cannot be written as a fraction.'],
    # 10x = 6.666..., not 6. And 0.666... = 2/3, so it IS a fraction.
    ('topic-1-2', 'Part 2 Question 3'): [
        'If x = 0.666..., then 10x = 6.',
        'Lee is correct because 0.666... cannot be written as a fraction.'],
    # the first move is +10, i.e. RIGHT. Three lefts describes -10, -4, -8.
    ('topic-1-3', 'Part 1 Question 1a'): [
        'Start at 0; move left 10, left 4, then left 8.'],
    ('topic-1-3', 'Part 2 Question 1a'): [
        'Start at 0; move left 12, left 5, then left 9.'],
    # (-5)^2 = 25 and -5^2 = -25. -10 is 2 x -5, the multiply-by-the-exponent
    # error; and they are not both -25, which is only the second one.
    ('topic-1-6', 'Part 1 Question 4b'): ['(-5)^2 = -10', 'Both expressions equal -25.'],
    ('topic-1-6', 'Part 2 Question 4b'): ['(-6)^2 = -12', 'Both expressions equal -36.'],
    # 10.4 >= 10.6 is false, so the conjunction is false. Mirrors the existing
    # <= distractor, which fails on its other half.
    ('topic-sc-1', 'Part 1 Question 1'): ['10.6 ≥ 10.4 and 10.4 ≥ 10.6'],
    ('topic-sc-1', 'Part 2 Question 1'): ['9.8 ≤ 9.3 and 9.3 ≤ 9.8'],
}

# The three figure stems said "Use the graphic choices." -- which makes the
# diagram load-bearing. It should not be. Whether the $IMS-CC-FILEBASE$ token
# resolves to the figure is genuinely unknown (see do_media), and a stem that
# points at a possibly-absent image tells a student to use something that may not
# be on screen. The options are already written out verbatim as text, so say so:
# the words are the answer choices, the diagram draws the same seven. Answerable
# from the assignment alone either way -- criterion 5 (BF-2026-048).
FIGURE_STEM = {
    ('6th-grade-review-section-1', 'A1'):
        ('Plot the point 4 on a number line. Each choice is written out below, '
         'and the diagram shows the same seven options. Select all correct '
         'choices; no units.'),
    ('6th-grade-review-section-1', 'H6'):
        ('Graph 6 &lt; y on a number line. Each choice is written out below, and '
         'the diagram shows the same seven options. Select all correct graph '
         'choices.'),
    ('6th-grade-review-section-1', 'H7'):
        ('Graph x &gt; 2 on a number line. Each choice is written out below, and '
         'the diagram shows the same seven options. Select all correct graph '
         'choices.'),
}


# Symbol palettes. A student cannot type a character that is not on their
# keyboard, so any item whose answer needs one states it copyably in the stem.
# This is the corpus-wide convention (BF-2026-068).
PALETTE_CMP = 'You may need one of these symbols -- copy it from here: < > = \u2260 \u2265 \u2264'
PALETTE_NEG = 'Include the negative sign if the answer is negative.'

# Multiplication as a student may type it: implied, asterisk, times sign,
# middle dot. Canvas compares bytes, so each is a different string.
MULT_SYMS = ('', '*', '\u00d7', '\u00b7')


def expr_variants(canonical_forms):
    """Every string a student following the stem can produce, for a typed
    expression.

    Measured, not assumed. Enumerating SPACING is unwinnable -- 448 generated
    strings still left gaps, and each round of widening only revealed more. What
    closes it is the STEM: "use no spaces" collapses the space to the operand
    orders and the multiplication symbol, and there the enumeration is complete.
    Of the eleven no-space forms a correct student can produce for 8(x+2) --
    both operand orders, both inner-term orders, all four multiplication symbols
    -- the generated list accepts eleven. Spaced twins are added on top as
    INSURANCE for the student who ignores the instruction, the same device
    topic-1-4 and topic-1-1 already use; those are covered but not guaranteed,
    and the parts-and-whole scaffold caps the loss at one mark of three when a
    spacing slips through (BF-2026-068).
    """
    out = set()
    for form in canonical_forms:
        for m in MULT_SYMS:
            base = form.replace('@', m)
            out.add(base)
            out.add(base.replace('+', ' + '))          # spaces round the plus
            out.add(base.replace('(', ' (').lstrip())  # space before the paren
            out.add(re.sub(r'\(\s*', '( ', base).replace(')', ' )'))
            out.add(base.replace('+', ' + ').replace('(', '( ').replace(')', ' )'))
            if m:                                      # spaces round the symbol
                sp = form.replace('@', f' {m} ')
                out.add(sp)
                out.add(sp.replace('+', ' + '))
    return with_unicode_minus(sorted(x.strip() for x in out if x.strip()))


def with_unicode_minus(vals):
    """A student who copies the stem's rendered MathJax gets U+2212, not ASCII
    hyphen-minus, and Canvas compares bytes. Accepting both costs nothing and
    closes the one residual risk the design worker could not close in wording.
    """
    out = list(vals)
    for v in vals:
        u = v.replace('-', '−')
        if u != v and u not in out:
            out.append(u)
    return out


# Whole-stem numeric replacement. Kept as machinery; currently unused.
#
# topic-1-4 was briefly routed here (numeric distance: 13, 30, 15, 9, 70, 27, all
# agreeing with both solution PDFs) before the author set the type hierarchy:
# numeric first, then short answer, then select-all as a last resort -- and named
# expression discrimination as the good select-all case. topic-1-4 asks the
# student to WRITE expressions, so it becomes twelve short-answer items instead,
# one expression each. The numeric values stay recorded above because they are
# what BF-2026-033's fix depends on either way.
CONVERT_FULL = {}

# --------------------------------------------------------------------------
# Pass 2 -- the eight splits. For each half: ('num', value, format sentence)
# or ('sel', keep-suffixes, format sentence) where keep-suffixes lists the
# choices that belong to that part.
# --------------------------------------------------------------------------
NUM_INT = 'Enter your answer as an integer. ' + ONLY
SEA = ('Enter your answer as an integer number of feet, using a negative sign '
       'for a position below sea level. ' + ONLY)

SPLIT = {
    # 15 ft/min down -> -15 ; 12 min -> -180
    ('topic-1-6', 'Part 1 Question 1'): (
        ('num', '-15', 'Enter your answer as an integer number of feet per '
                       'minute, using a negative sign for a descent. ' + ONLY),
        ('num', '-180', SEA)),
    # 20 ft/min up -> 20 ; 9 min -> 180
    ('topic-1-6', 'Part 2 Question 1'): (
        ('num', '20', 'Enter your answer as an integer number of feet per '
                      'minute, using a negative sign for a descent. ' + ONLY),
        ('num', '180', SEA)),
    # -168 ft / 7 min = -24 ; 4 min -> -96
    ('topic-1-8', 'Part 1 Question 1'): (
        ('num', '-24', 'Enter your answer as an integer number of feet per '
                       'minute, using a negative sign for a descent. ' + ONLY),
        ('num', '-96', SEA)),
    # 140 ft / 5 min = 28 ; 3 min -> 84
    ('topic-1-8', 'Part 2 Question 1'): (
        ('num', '28', 'Enter your answer as an integer number of feet per '
                      'minute, using a negative sign for a descent. ' + ONLY),
        ('num', '84', SEA)),
    # Part A is an expression -- the author's own example of a good select-all,
    # since distinguishing expressions is the skill. 2^4/2^2 = 4.
    # NEVER author 2^(4/2): dividing the exponents is the classic error, but with
    # 4 and 2 it evaluates to the key in BOTH variants. Same for 3^(4/2).
    ('topic-sc-2', 'Part 1 Question 2'): (
        ('sel', ['correct_1', 'wrong_1', 'wrong_2', 'wrong_5', 'wrong_6'],
         [('wrong_7', '2^4 / 2'),        # divisor is 2^2 = 4, not 2; 16/2 = 8
          ('wrong_8', '2^4 - 2^2'),      # 16 - 4 = 12; the rule subtracts exponents
          ('wrong_9', '2^(2-4)')]),      # 2^-2 = 1/4; difference is 4 - 2
        ('num', '4', 'Enter your answer as a whole number of cupcakes. ' + ONLY)),
    # 3^4/3^2 = 9
    ('topic-sc-2', 'Part 2 Question 2'): (
        ('sel', ['correct_1', 'wrong_1', 'wrong_2', 'wrong_5', 'wrong_6'],
         [('wrong_7', '3^4 / 3'),        # divisor is 3^2 = 9, not 3; 81/3 = 27
          ('wrong_8', '3^4 - 3^2'),      # 81 - 9 = 72
          ('wrong_9', '3^(2-4)')]),      # 3^-2 = 1/9
        ('num', '9', 'Enter your answer as a whole number of muffins. ' + ONLY)),
    # Part A is an explanation, so it stays select-all; 10 - 4 - 8 = -2
    ('topic-1-3', 'Part 1 Question 1'): (
        ('sel', ['correct_1', 'correct_2', 'correct_3',
                 'wrong_1', 'wrong_2', 'wrong_3'],
         [('wrong_4', 'Start at 0; move right 10, left 4, then right 8.'),
          ('wrong_5', '10 + (-4) - (-8)'),
          ('wrong_6', 'After the first two turns, the point is at -6.')]),
        ('num', '-2', NUM_INT)),
    # 12 - 5 - 9 = -2.  P2 says "moves" where P1 says "turns" -- track it.
    ('topic-1-3', 'Part 2 Question 1'): (
        ('sel', ['correct_1', 'correct_2', 'correct_3',
                 'wrong_1', 'wrong_2', 'wrong_3'],
         [('wrong_4', 'Start at 0; move right 12, left 5, then right 9.'),
          ('wrong_5', '12 + (-5) - (-9)'),
          ('wrong_6', 'After the first two moves, the point is at -7.')]),
        ('num', '-2', NUM_INT)),
}

SELECT_BOILER = ('Select every choice that belongs in the complete correct '
                 'answer. Select no incorrect choices.')

FIB = ('<response_str ident="response" rcardinality="Single">'
       '<render_fib fibtype="Decimal" prompt="Box" rows="1" columns="20">'
       '<response_label ident="answer1"/></render_fib></response_str>')

# Short answer differs from numeric only in fibtype. Shape copied from the 14
# short_answer items already shipped (e.g. g6_s1_c6, g6_s1_e1).
SHORT_FIB = ('<response_str ident="response" rcardinality="Single">'
             '<render_fib fibtype="String" prompt="Box" rows="1" columns="20">'
             '<response_label ident="answer1"/></render_fib></response_str>')


def resp_short(values, indent='        '):
    """Canvas short answer is exact string matching -- it trims surrounding
    whitespace and ignores case (case="No"), but internal spacing and notation
    are literal. Every spelling a correct student might type has to be listed
    here, or the item tells a right student they are wrong. That is why the
    accepted list is generated from an explicit spec and judged for coverage
    rather than inferred.
    """
    ors = ''.join(f'<varequal respident="response" case="No">{esc(v)}</varequal>'
                  for v in values)
    body = ors if len(values) == 1 else f'<or>{ors}</or>'
    return (f'{indent}<resprocessing>\n'
            f'{indent}  <outcomes>\n'
            f'{indent}    <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>\n'
            f'{indent}  </outcomes>\n'
            f'{indent}  <respcondition continue="No">\n'
            f'{indent}    <conditionvar>{body}</conditionvar>\n'
            f'{indent}    <setvar action="Set" varname="SCORE">100</setvar>\n'
            f'{indent}  </respcondition>\n'
            f'{indent}</resprocessing>')

BOILER_RE = re.compile(
    r'&lt;p&gt;&lt;strong&gt;Canvas accuracy check:&lt;/strong&gt;.*?&lt;/p&gt;', re.S)


def esc(s):
    """Author text -> the escaped-HTML form these stems are stored in."""
    return html.escape(s, quote=False)


def check_para(text):
    return ('&lt;p&gt;&lt;strong&gt;Canvas accuracy check:&lt;/strong&gt; '
            + esc(text) + '&lt;/p&gt;')


def accepted(v):
    vals = [v]
    if '.' in v and len(v.split('.')[1]) > 2:
        r = str(Decimal(v).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        if r not in vals:
            vals.append(r)
    return vals


def resp_numeric(v, indent='        '):
    """The Unicode-minus twin belongs here too, not only on short answer.

    with_unicode_minus() was applied to every short-answer list and to no
    numeric one, so a student who copies a negative value out of rendered
    MathJax types U+2212 and is marked wrong on every negative-keyed numeric
    item in the corpus -- including items this round never touched. Found by
    the answer battery on its first run, which is the whole reason the battery
    derives its probes independently of the generator (BF-2026-068).
    """
    ors = []
    for x in with_unicode_minus(accepted(v)):
        ors.append(f'<varequal respident="response" case="No">{x}</varequal>')
        ors.append(f'<and><vargte respident="response">{x}</vargte>'
                   f'<varlte respident="response">{x}</varlte></and>')
    return (f'{indent}<resprocessing>\n'
            f'{indent}  <outcomes>\n'
            f'{indent}    <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>\n'
            f'{indent}  </outcomes>\n'
            f'{indent}  <respcondition continue="No">\n'
            f'{indent}    <conditionvar><or>{"".join(ors)}</or></conditionvar>\n'
            f'{indent}    <setvar action="Set" varname="SCORE">100</setvar>\n'
            f'{indent}  </respcondition>\n'
            f'{indent}</resprocessing>')


def resp_select(keys, wrongs, indent='        '):
    parts = [f'\n{indent}        <varequal respident="response1">{k}</varequal>'
             for k in keys]
    for w in wrongs:
        parts.append(f'\n{indent}        <not>'
                     f'\n{indent}          <varequal respident="response1">{w}</varequal>'
                     f'\n{indent}        </not>')
    return (f'{indent}<resprocessing>\n'
            f'{indent}  <outcomes>\n'
            f'{indent}    <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>\n'
            f'{indent}  </outcomes>\n'
            f'{indent}  <respcondition continue="No">\n'
            f'{indent}    <conditionvar>\n'
            f'{indent}      <and>{"".join(parts)}\n'
            f'{indent}      </and>\n'
            f'{indent}    </conditionvar>\n'
            f'{indent}    <setvar action="Set" varname="SCORE">100</setvar>\n'
            f'{indent}  </respcondition>\n'
            f'{indent}</resprocessing>')


ITEM = '''      <item ident="{ident}" title="{title}">
        <itemmetadata>
          <qtimetadata>
            <qtimetadatafield>
              <fieldlabel>question_type</fieldlabel>
              <fieldentry>{qtype}</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>points_possible</fieldlabel>
              <fieldentry>1</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>original_answer_ids</fieldlabel>
              <fieldentry>{answer_ids}</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>assessment_question_identifierref</fieldlabel>
              <fieldentry>{ref}</fieldentry>
            </qtimetadatafield>
          </qtimetadata>
        </itemmetadata>
        <presentation>
          <material>
            <mattext texttype="text/html">{stem}</mattext>
          </material>
          {body}
        </presentation>
{resp}
      </item>'''


def item_block(raw, title):
    # Topic packages indent items six spaces; the two 6th-grade packages write
    # them at line start in a compact single-line layout. Match either.
    m = re.search(r'[ \t]*<item ident="[^"]*" title="%s">.*?</item>'
                  % re.escape(title), raw, re.S)
    return m.group(0) if m else None


def stem_paras(block):
    stem = re.search(r'<mattext texttype="text/html">(.*?)</mattext>',
                     block, re.S).group(1)
    return re.findall(r'&lt;p&gt;(.*?)&lt;/p&gt;', stem, re.S)


def wrap(paras):
    return ''.join('&lt;p&gt;%s&lt;/p&gt;' % p for p in paras)


def strip_part_label(p):
    return re.sub(r'^&lt;strong&gt;Part [AB]:&lt;/strong&gt;\s*', '', p)


def do_convert(raw, pkg, title, value, fmt, log, newstem=None):
    block = item_block(raw, title)
    if block is None:
        log.append(f'  !! {pkg} {title}: item not found')
        return raw
    new = block.replace('<fieldentry>multiple_answers_question</fieldentry>',
                        '<fieldentry>numerical_question</fieldentry>')
    new = re.sub(r'(<fieldlabel>original_answer_ids</fieldlabel>\s*<fieldentry>)[^<]*(</fieldentry>)',
                 r'\1choice_1\2', new)
    if newstem is not None:
        # The whole stem is replaced, not just the instruction line: these items
        # asked for "at least two expressions" and now ask for one value.
        old = re.search(r'(<mattext texttype="text/html">)(.*?)(</mattext>)',
                        new, re.S)
        new = new.replace(old.group(0),
                          old.group(1) + wrap([newstem]) + check_para(fmt)
                          + old.group(3))
        log.append(f'  restem   {title:18s} -> numeric {value}')
    elif not BOILER_RE.search(new):
        log.append(f'  !! {pkg} {title}: boilerplate not found')
        return raw
    else:
        new = BOILER_RE.sub(check_para(fmt), new)
    # count=1. Without it an item carrying two <response_lid> blocks is
    # rewritten into TWO <response_str ident="response"> blocks, so Canvas
    # renders two indistinguishable blanks for one question and the student
    # who answers in the box it does not bind scores 0 (BF-2026-064).
    new = re.sub(r'<response_lid.*?</response_lid>', FIB, new, count=1,
                 flags=re.S)
    new = re.sub(r'[ \t]*<resprocessing>.*?</resprocessing>',
                 resp_numeric(value), new, flags=re.S)
    if newstem is None:
        log.append(f'  convert  {title:18s} -> numeric {value}')
    return raw.replace(block, new)


def do_split(raw, pkg, title, halves, log):
    block = item_block(raw, title)
    if block is None:
        log.append(f'  !! {pkg} {title}: item not found')
        return raw
    paras = stem_paras(block)
    if len(paras) != 4:
        log.append(f'  !! {pkg} {title}: expected 4 paragraphs, saw {len(paras)}')
        return raw
    intro, pa, pb, _ = paras
    base = re.search(r'<item ident="([^"]*)"', block).group(1)
    ref = re.search(r'<fieldlabel>assessment_question_identifierref</fieldlabel>\s*'
                    r'<fieldentry>([^<]*)</fieldentry>', block).group(1)
    labels = dict(re.findall(
        r'<response_label ident="([^"]*)">\s*<material>\s*'
        r'<mattext texttype="text/html">(.*?)</mattext>', block, re.S))

    out = []
    for suffix, prompt, half in (('a', pa, halves[0]), ('b', pb, halves[1])):
        kind = half[0]
        ident = f'{base}{suffix}'
        newtitle = f'{title}{suffix}'
        if kind == 'num':
            _, value, fmt = half
            stem = wrap([intro, strip_part_label(prompt)]) + check_para(fmt)
            out.append(ITEM.format(
                ident=ident, title=newtitle, qtype='numerical_question',
                answer_ids='choice_1', ref=f'{ref}{suffix}', stem=stem,
                body=FIB, resp=resp_numeric(value)))
            log.append(f'  split    {newtitle:19s} -> numeric {value}')
        else:
            _, keep, authored = half
            ids = [f'{base}_{s}' for s in keep]
            missing = [i for i in ids if i not in labels]
            if missing:
                log.append(f'  !! {pkg} {title}{suffix}: missing choices {missing}')
                return raw
            # The half's stem no longer mentions parts, so a choice reading
            # "Part A: 2^4 / 2^2" would point at a label that is gone.
            for i in ids:
                labels[i] = re.sub(r'(&lt;p&gt;)\s*Part [AB]:\s*', r'\1', labels[i])
            # Authored distractors bring the half up to the >=7 floor. Each
            # carries a falsity proof in CHANGES.md and is judged adversarially:
            # an authored choice that is accidentally TRUE zeroes a student who
            # reasoned correctly, which is the worst defect available here.
            for suf, text in (authored or []):
                aid = f'{base}_{suf}'
                labels[aid] = '&lt;p&gt;' + esc(text) + '&lt;/p&gt;'
                ids.append(aid)
            keys = [i for i in ids if '_correct_' in i]
            wrongs = [i for i in ids if '_correct_' not in i]
            stem = wrap([intro, strip_part_label(prompt)]) + check_para(SELECT_BOILER)
            choices = ''.join(
                '\n              <response_label ident="%s">'
                '\n                <material>'
                '\n                  <mattext texttype="text/html">%s</mattext>'
                '\n                </material>'
                '\n              </response_label>' % (i, labels[i]) for i in ids)
            body = ('<response_lid ident="response1" rcardinality="Multiple">'
                    '\n            <render_choice>%s'
                    '\n            </render_choice>'
                    '\n          </response_lid>' % choices)
            out.append(ITEM.format(
                ident=ident, title=newtitle, qtype='multiple_answers_question',
                answer_ids=','.join(ids), ref=f'{ref}{suffix}', stem=stem,
                body=body, resp=resp_select(keys, wrongs)))
            log.append(f'  split    {newtitle:19s} -> select-all, '
                       f'{len(keys)} of {len(ids)}')
    return raw.replace(block, '\n'.join(out))


SIGN_SENTENCE = 'Include the negative sign if the answer is negative.'
WHOLE = 'Enter your answer as a whole number.'
# A whole number is {0, 1, 2, ...}; -15 is not one. Emitting WHOLE for a
# negative key made the stem contradict ITSELF -- the next sentence is "Include
# the negative sign if the answer is negative" -- and contradict the item's own
# question, e.g. topic-1-6 P1Q1a asks "What INTEGER represents the unit rate of
# their descent?" and then demanded a whole number for a key of -15. That is
# exactly F5's shape: a stem property contradicted by the key, failing the
# student who read the instruction. The right word already existed at NUM_INT
# and this sweep, which runs last, was overwriting it (BF-2026-051).
INTEGER = 'Enter your answer as an integer.'
# The old wording was 'Enter your answer as a decimal to two places, like 0.00.'
# The cold NUMERIC judge found eight items where that instruction contradicts the
# item's own accepted set: `g6_s1_d3` accepts `3.6` and `3.60`, `g6_s2_m6`
# accepts `9` and `9.00`, and so on. Its proposed fix was to narrow each set to
# the padded form only.
#
# That is the harmful direction, and the same one `validate.py` refused on K6
# (BF-2026-075). `3.6` and `3.60` are the same number; a student who types `3.6`
# has solved the problem, and narrowing marks them wrong. The instruction is what
# is wrong, not the acceptance.
#
# A census settles which: of the 17 items carrying this sentence, 15 have an
# exact answer of two decimals or fewer, so demanding a padded second place asks
# for a trailing zero that carries no information. The remaining two are worse
# than reported -- `1_2_part_1_question_1` asks for the decimal equivalent of
# 3/8, which is exactly `0.375`, so a two-place instruction forces an
# APPROXIMATION to a question about exact equivalence.
#
# So the demand is dropped and the optional trailing zero is stated outright.
# No numeric example is given: this constant is shared by 17 items, and any
# concrete example risks colliding with some item's own answer, which is the
# disclosure defect recorded as BF-2026-076.
DECIMAL = ('Enter your answer as a decimal. A zero on the end is optional.')
FRACTION = 'Enter a simplified a/b, no spaces or mixed numbers.'


def do_format_sweep(raw, log):
    """Every numeric stem prescribes the EXACT format its key has.

    Derived from the item's own accepted values, never assumed. Any "Round to
    the nearest X" clause already in the stem is preserved -- that is a
    mathematical instruction, not a formatting one, and dropping it would change
    the question. The 39 items shipped with only "Enter the number only, no
    units or symbols" are swept too: that says the answer is a bare number but
    not whether it is whole or decimal.
    """
    n = 0
    for item in re.findall(r'[ \t]*<item ident="[^"]*" title="[^"]*">.*?</item>',
                           raw, re.S):
        if 'numerical_question' not in item:
            continue
        vals = [v.strip() for v in
                re.findall(r'<varequal[^>]*>([^<]*)</varequal>', item)]
        if not vals:
            continue
        m = BOILER_RE.search(item)
        if m:
            old = re.sub(r'<[^>]+>', '', html.unescape(html.unescape(m.group(0))))
            old = re.sub(r'^.*?Canvas accuracy check:\s*', '', old).strip()
        else:
            # The two 6th-grade packages carry the instruction inline, with no
            # "Canvas accuracy check:" prefix. Same rule applies to them.
            m = re.search(r'(Enter [^<]*?\.)(?=\s*(?:&lt;img|</mattext>))', item)
            if not m:
                continue
            old = m.group(1)

        neg = any(v.strip().startswith('-') for v in vals)
        fmt = (DECIMAL if any('.' in v for v in vals)
               else INTEGER if neg else WHOLE)
        parts = []
        # These are mathematical instructions, not formatting ones -- dropping
        # them would change the question, so they survive the sweep.
        # Carried verbatim, two of these read as fragments glued to the
        # expression -- "5/6 = x/18 without x =." and "0.32 = ____ % omit the %
        # symbol." -- because the clause that governed them was dropped
        # upstream and this sweep faithfully re-emitted the remains. They are
        # rewritten as whole sentences, keeping the instruction exactly
        # (BF-2026-050).
        # The rounding clause is DELIBERATELY restated in the accuracy-check
        # paragraph even though the question sentence already carries it.
        #
        # An earlier judge called that a duplicated instruction block under
        # criterion 7 and I wrote a guard to suppress the second copy. F4
        # settles it the other way, in terms: "The accuracy-check paragraph
        # names what kind of number to type -- integer / whole number / decimal,
        # THE ROUNDING IF ANY, and the sign convention". Criterion 1 separately
        # requires the question sentence to match the assignment, which prints
        # "(Round to nearest kilometer)". Both sentences are mandated by
        # different rules, they say the identical thing, and removing either
        # breaks its own rule -- so the guard was trying to delete something the
        # gate requires. It never fired anyway, because the question sentence
        # reads "Round YOUR ANSWER to the nearest kilometer" and the pattern
        # below does not match that; inert code encoding a wrong intent is worse
        # than either outcome, so it is gone (BF-2026-052).
        for pat, rewrite in ((r'Round to the nearest [a-z]+', None),
                             (r'omit the % symbol', 'Omit the % symbol.'),
                             (r'without x =', 'Enter the value of x, not "x =".')):
            k = re.search('(' + pat + ')', old, re.I)
            if k:
                parts.append(rewrite or (k.group(1).rstrip('.') + '.'))
        parts.append(fmt)
        if neg:
            parts.append(SIGN_SENTENCE)
        parts.append(ONLY)
        new_text = ' '.join(parts)
        if new_text == old:
            continue
        body = (check_para(new_text) if m.group(0).startswith('&lt;p&gt;')
                else esc(new_text))
        raw = raw.replace(item, item.replace(m.group(0), body))
        n += 1
    if n:
        log.append(f'  format   {n} numeric stems given an exact format')
    return raw


def do_minus_sweep(raw, log):
    """Every negative numeric key gets its U+2212 twin, wherever it came from.

    resp_numeric() was fixed to emit the twin, and that reached only the items
    this pipeline GENERATES. The corpus also contains negative-keyed numeric
    items that no transform rewrites -- they ship exactly as the pristine export
    made them -- and on those a student who copies the value out of rendered
    MathJax still typed U+2212 and was still marked wrong. Eight items, found by
    the answer battery after the generator fix had already been declared done.
    The same shape this log keeps recording: a fix applied where the code
    happens to run rather than everywhere the property is required
    (BF-2026-068).
    """
    n = 0
    def fix(m):
        nonlocal n
        cv = m.group(0)
        add = []
        for val in re.findall(r'<varequal respident="response"[^>]*>'
                              r'(-[\d.]+)</varequal>', cv):
            twin = val.replace('-', '\u2212')
            if twin not in cv:
                add.append(f'<varequal respident="response" case="No">'
                           f'{twin}</varequal>')
        if not add:
            return cv
        n += 1
        return cv.replace('</or>', ''.join(add) + '</or>')
    raw = re.sub(r'<conditionvar><or>.*?</or></conditionvar>', fix, raw, flags=re.S)
    if n:
        log.append(f'  minus    {n} negative numeric keys gained a U+2212 twin')
    return raw


def do_sign_sweep(raw, log):
    """BF-2026-035 -- every numeric item whose key can be negative must say so.

    "Enter the number only, no units or symbols" is readable as "omit the minus
    sign", which silently marks a correct student wrong. 8 shipped items had a
    negative key and no sign guidance. Applies to converted items too, so the
    rule holds for anything this pipeline produces rather than only for what it
    was told about.
    """
    n = 0
    for item in re.findall(r'<item ident="[^"]*" title="[^"]*">.*?</item>',
                           raw, re.S):
        if 'numerical_question' not in item:
            continue
        vals = re.findall(r'<varequal[^>]*>([^<]*)</varequal>', item)
        if not any(v.strip().startswith('-') for v in vals):
            continue
        m = BOILER_RE.search(item)
        if not m:
            continue
        body = html.unescape(html.unescape(m.group(0)))
        if re.search(r'negative sign|minus sign', body, re.I):
            continue
        text = re.sub(r'^.*?Canvas accuracy check:\s*', '',
                      re.sub(r'<[^>]+>', '', body)).strip()
        new = item.replace(m.group(0), check_para(SIGN_SENTENCE + ' ' + text))
        raw = raw.replace(item, new)
        title = re.search(r'title="([^"]*)"', item).group(1)
        log.append(f'  sign     {title:18s} key {vals[0]} -- added sign guidance')
        n += 1
    return raw


def do_repair(raw, pkg, title, spec, log):
    """D1 -- replace choices that are TRUE while being scored as wrong.

    In-place text replacement on existing choice idents: no ident is added or
    removed, so <resprocessing> and original_answer_ids need no edit and the
    key cannot drift. Each replacement is one edit away from the true choice it
    replaces, so the item still discriminates exactly where it broke.

    Several items also need the STEM tightened, because under "select all
    equivalent rewrites" a choice like `13` genuinely is equivalent to `8 + 5`
    and no choice set can be made correct without narrowing what is asked. The
    narrowing is the author's own definition, quoted from the explanations PDF.
    """
    block = item_block(raw, title)
    if block is None:
        log.append(f'  !! {pkg} {title}: item not found')
        return raw
    newstem, swaps = spec
    new = block

    for ident, text in swaps.items():
        m = re.search(r'(<response_label ident="[^"]*%s">\s*<material>\s*'
                      r'<mattext[^>]*>)(.*?)(</mattext>)' % re.escape(ident),
                      new, re.S)
        if not m:
            log.append(f'  !! {pkg} {title}: choice {ident} not found')
            return raw
        # Section-2 choices are text/plain; topic-1-2's are text/html wrapped in
        # an escaped <p>. Match whichever the item already uses.
        body = (('&lt;p&gt;' + esc(text) + '&lt;/p&gt;')
                if m.group(2).lstrip().startswith('&lt;p&gt;') else esc(text))
        new = new.replace(m.group(0), m.group(1) + body + m.group(3))

    if newstem is not None:
        old = re.search(r'(<mattext texttype="text/html">)(.*?)(</mattext>)',
                        new, re.S)
        new = new.replace(old.group(0), old.group(1) + newstem + old.group(3))

    log.append(f'  repair   {title:18s} {len(swaps)} true choices replaced'
               + ('  + stem tightened' if newstem else ''))
    return raw.replace(block, new)


def do_addwrong(raw, pkg, title, texts, log, total):
    """F-1 -- author additional distractors so every select-all carries >=7.

    Unlike do_repair, this DOES add idents, so all three places that name a
    choice have to move together or the item silently breaks:

      1. <render_choice>        -- the visible choice
      2. original_answer_ids    -- validate.py asserts this matches the real list
      3. the <and> in <respcondition> -- a new choice that is not negated is
         effectively OPTIONAL, and under all-or-nothing a student who selects it
         still scores 100. An un-negated distractor is not a distractor.

    Keyed idents are never touched, so the key set cannot drift. permute.py runs
    after this and reorders both the labels and original_answer_ids together.
    """
    block = item_block(raw, title)
    if block is None:
        log.append(f'  !! {pkg} {title}: item not found')
        return raw

    idents = re.findall(r'<response_label ident="([^"]*)"', block)
    if not idents:
        log.append(f'  !! {pkg} {title}: no choices to pattern from')
        return raw

    # Two ident schemes coexist in this corpus and both must be handled:
    # topic-* items use "<base>_wrong_N" / "<base>_correct_N"; the 6th-grade
    # packages use a bare "choice_N". Derive from whichever the item uses
    # rather than assuming, and never collide with an existing number.
    wrongs = [i for i in idents if re.search(r'_wrong_(\d+)$', i)]
    if wrongs:
        stem_id = re.sub(r'_wrong_\d+$', '', wrongs[0]) + '_wrong_'
        # Allocate against every ident sharing this base ANYWHERE in the file,
        # not just this item's. A split leaves sibling halves (1a, 1c) drawing
        # from one base, so numbering per-item hands the same string to two
        # different choices. Harmless to Canvas -- idents scope to their own
        # <response_lid> -- but a file-wide ident replace is the documented fix
        # method in BF-2026-036, and it would silently edit the wrong choice.
        used = [int(m.group(1))
                for m in re.finditer(r'%s(\d+)"' % re.escape(stem_id), raw)]
    elif all(re.fullmatch(r'choice_\d+', i) for i in idents):
        stem_id = 'choice_'
        used = [int(i.split('_')[1]) for i in idents]
    else:
        log.append(f'  !! {pkg} {title}: unrecognised ident scheme {idents[:2]}')
        return raw
    nxt = max(used) + 1

    # Match the item's existing markup exactly -- some choices are text/plain
    # and bare, others text/html wrapped in an escaped <p>.
    sample = re.search(r'<response_label ident="[^"]*">\s*<material>\s*'
                       r'<mattext texttype="([^"]*)">(.*?)</mattext>', block, re.S)
    ttype = sample.group(1)
    wrap = sample.group(2).lstrip().startswith('&lt;p&gt;')

    # Indentation differs between packages, so anchor on the tag and reuse
    # whatever leading whitespace that tag already has.
    rc = re.search(r'([ \t]*)</render_choice>', block)
    an = re.search(r'([ \t]*)</and>', block)
    if not rc or not an:
        log.append(f'  !! {pkg} {title}: no </render_choice> or </and>')
        return raw
    ind, aind = rc.group(1), an.group(1)

    # Read respident off the item instead of assuming it. The 6th-grade
    # packages use respident="response"; topic-* use "response1". A <not> that
    # names the wrong one negates nothing, so the choice would be scored as
    # optional and a student selecting it would still get 100.
    ri = re.search(r'<varequal respident="([^"]*)"', block)
    if not ri:
        log.append(f'  !! {pkg} {title}: no varequal to read respident from')
        return raw
    respident = ri.group(1)

    new, added = block, []
    for off, text in enumerate(texts):
        ident = f'{stem_id}{nxt + off}'
        added.append(ident)
        body = ('&lt;p&gt;' + esc(text) + '&lt;/p&gt;') if wrap else esc(text)
        label = (f'{ind}  <response_label ident="{ident}">\n'
                 f'{ind}    <material>\n'
                 f'{ind}      <mattext texttype="{ttype}">{body}</mattext>\n'
                 f'{ind}    </material>\n'
                 f'{ind}  </response_label>\n')
        new = new.replace(f'{ind}</render_choice>', label + f'{ind}</render_choice>', 1)

    ids = re.search(r'(<fieldlabel>original_answer_ids</fieldlabel>\s*<fieldentry>)([^<]*)(</fieldentry>)', new)
    new = new.replace(ids.group(0), ids.group(1) + ids.group(2) + ',' + ','.join(added) + ids.group(3))

    nots = ''.join(f'{aind}  <not>\n'
                   f'{aind}    <varequal respident="{respident}">{i}</varequal>\n'
                   f'{aind}  </not>\n' for i in added)
    new = new.replace(f'{aind}</and>', nots + f'{aind}</and>', 1)

    total['addwrong'] += len(added)
    log.append(f'  addwrong {title:18s} +{len(added)} distractors')
    return raw.replace(block, new)


# topic-1-1 Q1 -- Part A and Part B sit INLINE in one paragraph, which is why
# both the recorded census and the first splitter missed these (BF-2026-032).
# Part A itself asks two things: represent the pair, and find its sum. So each
# item becomes three: the pair (select-all -- two signed numbers, not one), the
# sum (numeric), and the explanation (select-all -- a statement).
#
# The explanation half has NO distractors in the source: all five wrongs belong
# to Part A. Six are authored, each false for BOTH 18 and 24.
# FORBIDDEN, all TRUE, never author here: "Their sum is zero." / "They have the
# same absolute value." / "Each is the opposite of the other." / "They are the
# same distance from zero." / "The second change undoes the first."
_INV = [
    ('wrong_7', 'equal magnitude and the same sign'),
    ('wrong_8', 'different magnitudes and opposite signs'),
    ('wrong_9', 'Their product is zero.'),
    ('wrong_10', 'They are reciprocals of each other.'),
    ('wrong_12', 'Subtracting the second change from the first gives 0.'),
]
_SUM = ('0', 'Enter your answer as a whole number. '
             'Include the negative sign if the answer is negative. ' + ONLY)

REBUILD = {
    ('topic-1-6', 'Part 1 Question 4'): ('', [
        ('a', 'num', 'Evaluate: \\(-5^{2} =\\)',
         ('-25', 'Enter your answer as a whole number. ' + SIGN_SENTENCE
          + ' ' + ONLY)),
        # the old stem said "how Question 3 and Question 4 differ" -- a
        # cross-reference that stops resolving once the items are renumbered.
        ('b', 'sel', 'Compare \\((-5)^{2}\\) and \\(-5^{2}\\). Explain '
                     'briefly how the two expressions differ.',
         (['correct_2', 'correct_3', 'wrong_2', 'wrong_3', 'wrong_4'],
          # to the >=7 floor. Both false for BOTH variants:
          # (-5)^2 = +25 and -5^2 = -25, so the values differ and the
          # parentheses make the result positive, not negative.
          [('wrong_6', 'Both expressions have the same value.'),
           ('wrong_7', 'The parentheses make the answer negative.')])),
    ]),
    ('topic-1-6', 'Part 2 Question 4'): ('', [
        ('a', 'num', 'Evaluate: \\(-6^{2} =\\)',
         ('-36', 'Enter your answer as a whole number. ' + SIGN_SENTENCE
          + ' ' + ONLY)),
        ('b', 'sel', 'Compare \\((-6)^{2}\\) and \\(-6^{2}\\). Explain '
                     'briefly how the two expressions differ.',
         (['correct_2', 'correct_3', 'wrong_2', 'wrong_3', 'wrong_4'],
          # to the >=7 floor. Both false for BOTH variants:
          # (-6)^2 = +36 and -6^2 = -36, so the values differ and the
          # parentheses make the result positive, not negative.
          [('wrong_6', 'Both expressions have the same value.'),
           ('wrong_7', 'The parentheses make the answer negative.')])),
    ]),
    ('topic-1-1', 'Part 1 Question 1'): (
        'A submarine rises 18 meters from a point below sea level, then '
        'descends 18 meters.', [
            # "in the order they happened" is load-bearing: without it the
            # reversed pair is TRUE as an unordered pair, not a distractor.
            ('a', 'sel', 'Which pair of signed numbers represents the two '
                         'changes, in the order they happened?',
             (['correct_1', 'wrong_1', 'wrong_2', 'wrong_3', 'wrong_4',
               'wrong_5'], [('wrong_6', '-18 and +18')])),
            ('b', 'num', 'Each change can be written as a signed number. What '
                         'is the sum of the two signed changes?', _SUM),
            ('c', 'sel', 'The two changes are additive inverses of each other. '
                         'Which statement explains why?',
             (['correct_3'], _INV + [
                 ('wrong_11', 'The two changes are equal because both are '
                              '18 meters.')])),
        ]),
    ('topic-1-1', 'Part 2 Question 1'): (
        'A hiker descends 24 meters from a trail marker, then climbs 24 '
        'meters.', [
            ('a', 'sel', 'Which pair of signed numbers represents the two '
                         'changes, in the order they happened?',
             (['correct_1', 'wrong_1', 'wrong_2', 'wrong_3', 'wrong_4',
               'wrong_5'], [('wrong_6', '+24 and -24')])),
            ('b', 'num', 'Each change can be written as a signed number. What '
                         'is the sum of the two signed changes?', _SUM),
            ('c', 'sel', 'The two changes are additive inverses of each other. '
                         'Which statement explains why?',
             (['correct_3'], _INV + [
                 ('wrong_11', 'The two changes are equal because both are '
                              '24 meters.')])),
        ]),
}


# Select-all items whose answer is one or two words, or a short symbolic form.
# The author's hierarchy puts short answer above select-all for these; each stem
# names the exact characters to type and shows one worked example, because
# Canvas short answer is byte-exact string matching.
WORDS = 'Your answer is one or two words.'
INEQ = ('You may need to use >, <, or =. Type it with no spaces: if your answer '
        'were x greater than 4, write it as x>4.')
SYMBOL = 'Enter one symbol only: <, >, =, or ≠.'
ORDER = ('Separate the numbers with commas, least first. Type it like '
         '-5,0,2 with no spaces.')
# F3/F4 failed in BOTH directions (SHORTANS R4 and R5). They rejected correct
# `subtraction by 8` / `division by 5`, and they accepted `subtract`,
# `subtraction`, `-8`, `−8`, `division`, `divide` -- each naming only ONE of the
# two things the stem demands, so a half-answer scored full credit.
#
# Widening the English phrasings cannot close this: `take 8 away`, `minus eight`
# and the next construction are unbounded. Closure comes from the stem naming
# the permitted forms. But closure does NOT mean one accepted string -- it means
# a set that can be written down completely. A first attempt narrowed F3 to the
# single `subtract eight` and rewrote the example from the source's numeral
# (`add 3`) to a number word, which rejected `subtract 8`, the most natural form,
# and contradicted F4 one item later whose example stayed a numeral
# (BF-2026-075).
#
# So: the example stays a numeral, the stem says both forms are allowed, and
# both are accepted. F4 needs its own example because its answer carries `by`
# and the `add 3` pattern would mislead a student into `divide 5`; the example
# uses a different operation and number, so it prescribes the shape without
# hinting the answer.
OPNAME = ('Use exactly one of these two patterns: a base action verb followed by '
          'the number, like multiply 4; or an operation noun followed by the '
          'word by and the number, like multiplication by 4. Write the number '
          'as a numeral or a word. At each gap independently, use either one '
          'space or no space.')
OPNAME_BY = ('Use exactly one of these two patterns: a base action verb followed '
             'by the word by and the number, like multiply by 4; or an operation '
             'noun followed by the word by and the number, like multiplication '
             'by 4. Write the number as a numeral or a word. At each gap '
             'independently, use either one space or no space.')

# F1/F2 -- AUTHOR'S RULING, and it overrides the engineering preference.
#
# History, so this is not re-litigated. SHORTANS found both items rejecting a
# mathematically correct answer: `factor` for the 7 in `7m`, `unknown quantity`
# for the `n` in `n + 8 = 12`. A vocabulary family cannot be closed by adding
# synonyms, so closure was attempted by enumerating candidates in the stem. The
# first attempt offered a list containing two true answers and was rejected
# (BF-2026-074); the second used mutually exclusive candidates and shipped.
#
# The cold SOURCE judge then failed both items: the source presents a blank and
# asks the student to PRODUCE the term, while an enumerated list asks them to
# RECOGNISE it. A student who cannot recall `coefficient` can still reach it by
# eliminating three visibly false options. That is a different cognitive task,
# and the judge correctly declined to grant a source-fidelity exception on its
# own authority.
#
# Put to the author with the trade stated plainly -- no option is at once
# source-faithful, auto-gradable and incapable of failing a correct student.
# **The author chose to restore open production.** So the candidate lists are
# gone and the blanks are back.
#
# The accepted sets are therefore widened as far as the mathematics allows,
# which is the only lever left for protecting correct students under this
# ruling. Every term below is genuinely true of its own expression:
#   F1, the 7 in `7m = 7 x m` -- it is the numerical coefficient of `m`, and it
#     is equally a factor of the product. Both families accepted.
#   F2, the `n` in `n + 8 = 12` -- it is the variable, and it is the unknown
#     quantity/number/value the equation determines. All accepted.
#
# KNOWN AND ACCEPTED RESIDUAL RISK: this set is wide but not provably closed.
# Some further correct synonym may exist that is not listed, and Canvas compares
# bytes, so such a student is marked wrong. That possibility is the stated cost
# of the ruling, not an oversight, and it must not be "fixed" by silently
# reintroducing an enumerated stem. Only the author may revisit it.

TOSHORT = {
    ('6th-grade-review-section-1', 'F1'): (
        ['coefficient', 'numerical coefficient', 'factor', 'numerical factor',
         'multiplier', 'numerical multiplier'],
        WORDS, None),
    ('6th-grade-review-section-1', 'F2'): (
        ['variable', 'unknown', 'unknown number', 'unknown value',
         'unknown quantity', 'unknown variable'], WORDS, None),
    # Both spellings of the number, each with its space-stripped twin. Canvas
    # trims only OUTER whitespace, so `subtract8` is a distinct byte string from
    # `subtract 8` and a student who omits the space has still answered
    # correctly. `battery.py` derives exactly these and rejected the first
    # attempt that omitted them -- the instrument earning its keep.
    ('6th-grade-review-section-1', 'F3'): (
        [f'subtract{gap}{number}'
         for number in ('8', 'eight') for gap in (' ', '')] +
        [f'subtraction{left}by{right}{number}'
         for number in ('8', 'eight') for left in (' ', '')
         for right in (' ', '')],
        OPNAME, None),
    ('6th-grade-review-section-1', 'F4'): (
        [f'{operation}{left}by{right}{number}'
         for operation in ('divide', 'division')
         for number in ('5', 'five') for left in (' ', '')
         for right in (' ', '')], OPNAME_BY, None),
    # H3/H4: the worksheet says "Solve:"; the conversion dropped it, leaving a
    # stem with no instruction verb at all. The flipped form is the SAME
    # statement -- and H5 teaches that flip one item later.
    ('6th-grade-review-section-1', 'H3'): (
        ['x>5', 'x > 5', 'x> 5', 'x >5', '5<x', '5 < x', '5< x', '5 <x'],
        INEQ, 'Solve: '),
    ('6th-grade-review-section-1', 'H4'): (
        ['x<6', 'x < 6', 'x< 6', 'x <6', '6>x', '6 > x', '6> x', '6 >x'],
        INEQ, 'Solve: '),
    ('6th-grade-review-section-1', 'H5'): (
        ['y>6', 'y > 6', 'y> 6', 'y >6'], INEQ, None),
    ('topic-1-1', 'Part 1 Question 4'): (
        ['-3,-1,8', '-3, -1, 8', '-3,-1, 8', '-3, -1,8'], ORDER, None),
    ('topic-1-1', 'Part 2 Question 4'): (
        ['-2,4,6', '-2, 4, 6', '-2,4, 6', '-2, 4,6'], ORDER, None),
}


def do_toshort(raw, pkg, title, spec, log):
    """Select-all -> short answer, dropping the choice list entirely."""
    block = item_block(raw, title)
    if block is None:
        log.append(f'  !! {pkg} {title}: item not found')
        return raw
    accepted, fmt, prefix = spec
    vals = with_unicode_minus(accepted)
    new = re.sub(r'<fieldentry>multiple_answers_question</fieldentry>',
                 '<fieldentry>short_answer_question</fieldentry>', block)
    new = re.sub(r'(<fieldlabel>original_answer_ids</fieldlabel>\s*<fieldentry>)[^<]*(</fieldentry>)',
                 r'\1choice_1\2', new)
    m = BOILER_RE.search(new)
    if m:
        new = new.replace(m.group(0), check_para(fmt))
    else:
        # 6th-grade packages carry the instruction inline, before any <img>.
        m2 = re.search(r'(Enter [^<]*?\.)(?=\s*(?:&lt;img|</mattext>))', new)
        if not m2:
            log.append(f'  !! {pkg} {title}: instruction sentence not found')
            return raw
        new = new.replace(m2.group(1), esc(fmt))
    if prefix:
        # The conversion had deleted the worksheet's own task verb, leaving a
        # stem that never says what to do with the inequality.
        m3 = re.search(r'(<mattext texttype="text/html">)', new)
        new = new.replace(m3.group(1), m3.group(1) + esc(prefix), 1)
    # count=1. Without it an item carrying two <response_lid> blocks is
    # rewritten into TWO <response_str ident="response"> blocks, so Canvas
    # renders two indistinguishable blanks for one question and the student
    # who answers in the box it does not bind scores 0 (BF-2026-064).
    new = re.sub(r'<response_lid.*?</response_lid>', SHORT_FIB, new, count=1,
                 flags=re.S)
    new = re.sub(r'[ \t]*<resprocessing>.*?</resprocessing>',
                 resp_short(vals), new, flags=re.S)
    log.append(f'  toshort  {title:18s} -> {len(vals)} accepted')
    return raw.replace(block, new)


LETTERED = {('6th-grade-review-section-1', t) for t in ('A1', 'H6', 'H7')}

# The row letters these items' figures are drawn with. Long enough that adding a
# choice is a content decision rather than a crash, and checked at use anyway.
CHOICE_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def do_letter_prefix(raw, pkg, title, log):
    block = item_block(raw, title)
    if block is None:
        log.append(f'  !! {pkg} {title}: item not found')
        return raw
    new, n = block, 0
    # `choice_(\d+)`, not `choice_(\d)`. The single-digit form stopped matching
    # at choice_9, so a choice_10 would silently ship with NO letter prefix while
    # its stem promises the diagram shows the same lettered options -- and it
    # also capped idx at 8, which made the bounds check below unreachable dead
    # code. Widening the alphabet only helps once the regex can produce an index
    # that overflows it (BF-2026-049).
    for m in re.finditer(r'(<response_label ident="[^"]*choice_(\d+)">\s*<material>'
                         r'\s*<mattext[^>]*>)(.*?)(</mattext>)', block, re.S):
        # Was 'ABCDEFG', exactly seven long: a choice_8 on A1/H6/H7 raised
        # IndexError and crashed the build, with nothing in the traceback
        # pointing at the choice that caused it (BF-2026-048).
        idx = int(m.group(2)) - 1
        if not 0 <= idx < len(CHOICE_LETTERS):
            # Keep the letters already applied to earlier choices in this item.
            # Returning bare `raw` discarded them, so an item that tripped this
            # shipped with ZERO letters -- worse than the overflow, and silent,
            # because build.sh does not gate on finalize.py's log.
            log.append(f'  !! {pkg} {title}: choice_{idx + 1} outside the '
                       f'{len(CHOICE_LETTERS)}-letter alphabet')
            return raw.replace(block, new)
        letter = CHOICE_LETTERS[idx]
        if m.group(3).lstrip().startswith(letter + '.'):
            continue
        new = new.replace(m.group(0),
                          m.group(1) + f'{letter}. ' + m.group(3) + m.group(4))
        n += 1
    if n:
        log.append(f'  letters  {title:18s} {n} choices tied to their figure row')
    return raw.replace(block, new)


# Existing short-answer items whose accepted list is missing a form the answer
# key itself prints.
STEM_INSTR = {
    # SHORTANS found K6 accepting `7/4` and `1.75` against its own sentence
    # "Type it the same way it is written in the question", which permits only
    # `1 3/4`. Two ways existed to make stem and acceptance agree. Narrowing the
    # accepted set was tried first and `validate.py` refused it -- `7/4` is a
    # PRISTINE answer, so dropping it would fail a student the original quiz
    # accepted. The gate was right (BF-2026-075): the three strings are one
    # number, and the item tests which of `1 3/4` and `(1)(3/4)` is greater, not
    # mixed-number notation. So the instruction was never load-bearing and it is
    # the instruction that changes.
    # The format examples must NOT use this item's own answer. Naming the three
    # forms as `1 3/4`, `7/4`, `1.75` -- which my own ruling, the fixer and the
    # PR reviewer all independently proposed -- prints the correct answer three
    # times in the instruction, so a student who cannot compare the two values
    # simply copies it. That is self-answer disclosure (SOURCE R5) and would be a
    # worse defect than the superset being repaired. The example below uses an
    # unrelated number, so it prescribes the three forms without hinting.
    ('6th-grade-review-section-2', 'K6'):
        'Enter the greater value. You may write it as a mixed number, an '
        'improper fraction in simplest form, or a decimal with no trailing '
        'zeros -- for example 2 1/2, 5/2, or 2.5.',
    ('6th-grade-review-section-1', 'E1'):
        'Type the greater of the two values exactly as it appears above.',
}


def do_stem_instr(raw, pkg, title, text, log):
    block = item_block(raw, title)
    if block is None:
        log.append(f'  !! {pkg} {title}: item not found')
        return raw
    m = re.search(r'(Enter [^<]*?\.)(?=\s*(?:&lt;img|</mattext>))', block)
    if not m:
        log.append(f'  !! {pkg} {title}: instruction not found')
        return raw
    log.append(f'  instr    {title:18s} format line rewritten')
    return raw.replace(block, block.replace(m.group(1), esc(text)))


WIDEN = {
    # K6 asks which is greater, 1 3/4 or (1)(3/4). The key is 7/4 -- but the
    # explanations PDF answers "1 3/4", and the item's boilerplate format line
    # ("no mixed numbers") forbids typing it. The key's own answer scored zero.
    # All three pristine forms kept -- they are one number, and dropping `7/4`
    # is what `validate.py` refused (BF-2026-075). The mixed-number spacings are
    # insurance: Canvas trims only OUTER whitespace, so every internal spacing a
    # student might type is a distinct byte string. `battery.py` does not derive
    # these, so they are added deliberately rather than on its prompting.
    ('6th-grade-review-section-2', 'K6'): [
        '1 3/4', '1  3/4', '1 3 /4', '1 3/ 4', '1 3 / 4', '1.75', '7/4'],
}


def do_widen(raw, pkg, title, vals, log):
    block = item_block(raw, title)
    if block is None:
        log.append(f'  !! {pkg} {title}: item not found')
        return raw
    # REFUSE rather than silently corrupt. The regex below is flat over the
    # item -- the rubric's own trap table records that shape as the one that
    # makes every choice look required -- and it does not strip <not> subtrees;
    # resp_short then REPLACES the whole <resprocessing>. Pointed at a
    # select-all this promotes the negated distractors to accepted answers.
    # Pointed at a numeric item it discards the <vargte>/<varlte> arms and
    # narrows the item to exact-string matching while question_type still reads
    # numerical_question, so `7.00` against a key of `7` is rejected. Every
    # current WIDEN target is a short answer with neither node, so no harm is
    # live; the guard exists because the next one added need not be, and the
    # damage would surface as a correct student marked wrong (BF-2026-061).
    if '<not>' in block or '<vargte' in block or '<varlte' in block:
        log.append(f'  !! {pkg} {title}: do_widen refuses -- the item carries '
                   f'<not> or range bounds, which resp_short would discard')
        return raw
    have = re.findall(r'<varequal[^>]*>([^<]*)</varequal>', block)
    allv = with_unicode_minus(list(dict.fromkeys(list(have) + vals)))
    new = re.sub(r'[ \t]*<resprocessing>.*?</resprocessing>',
                 resp_short(allv), block, flags=re.S)
    log.append(f'  widen    {title:18s} {len(have)} -> {len(allv)} accepted')
    return raw.replace(block, new)


# Stems whose wording no longer matches what their key requires.
STEM_FIX = {
    # The split left this asking only "explain ... using a number line", while
    # the key still requires the expression 10 + (-4) + (-8) -- which both
    # solution PDFs file under Part B. A student answering the question as
    # asked selected two of three keyed choices and scored zero.
    ('topic-1-3', 'Part 1 Question 1a'):
        'In the first round of a board game, a player scores 10 points. On '
        'their next turn, they lose 4 points. On their last turn of the round, '
        'they lose 8 points. Which choices correctly describe the change in '
        'score, including the moves on a number line and the expression for '
        'the round?',
    ('topic-1-3', 'Part 2 Question 1a'):
        'In the first round of a card game, a player scores 12 points. On '
        'their next turn, they lose 5 points. On their last turn of the round, '
        'they lose 9 points. Which choices correctly describe the change in '
        'score, including the moves on a number line and the expression for '
        'the round?',
}


def do_stemfix(raw, pkg, title, text, log):
    block = item_block(raw, title)
    if block is None:
        log.append(f'  !! {pkg} {title}: item not found')
        return raw
    # Consume EVERY leading paragraph up to the Canvas boilerplate, not just the
    # first. The old non-greedy single-<p> pattern left the superseded Part A
    # prompt standing as paragraph 2 -- the last thing a student read before the
    # choices -- so an item whose key includes an expression still ended with
    # "Explain how to show the change ... using a number line." A student who
    # obeyed that final sentence selected one of three keys and scored zero,
    # which is the exact defect the stem fix was written to cure (BF-2026-047).
    m = re.search(r'(<mattext texttype="text/html">)'
                  r'(?:&lt;p&gt;(?!&lt;strong&gt;Canvas).*?&lt;/p&gt;)+',
                  block, re.S)
    if not m:
        log.append(f'  !! {pkg} {title}: no leading paragraph to replace')
        return raw
    new = block.replace(m.group(0), m.group(1) + wrap([text]))
    log.append(f'  stemfix  {title:18s} widened to match its key')
    return raw.replace(block, new)


def _repairs():
    """D1 repair table. Built as a function so the stems can call check_para.

    Every replacement below is provably FALSE for the item's own values; the
    proof is recorded in CHANGES.md. The forbidden near-misses are recorded too,
    because the failure mode here is a later editor "correcting" `x 0` back to
    `x 1` and silently reintroducing a true choice.
    """
    commutative = ('Enter select all choices that show the same two %s joined '
                   'by the same operation in the opposite order; do not select '
                   'the original expression or its computed value.')
    associative = ('Enter select all choices that keep the addends %s in this '
                   'same left-to-right order and move only the grouping; do not '
                   'select the original expression, a reordered expression, or '
                   'a partly added-up expression.')
    return {
        # F-3. The QTI stem is STRICTER than the worksheet, which asks a bare
        # "Factor: 8x + 16 =". The QTI is right and the answer key agrees -- the
        # worksheet is what is loose -- so the key must not be relaxed. But a
        # student who wrote 4(2x + 4) on paper was being told they were wrong
        # without being told why.
        #
        # Fix: make the stem carry its own standard. Stating the completeness
        # criterion is not a giveaway, because applying it IS the skill being
        # tested, and it satisfies rubric criterion 5 -- answerable from the
        # assignment alone. No choice changes truth value: 4(2x + 4) and the
        # added 2(4x + 8) both still equal 8x + 16 and are both still incomplete.
        # (The worksheet's own wording is recorded in TEACHER_ACTIONS.md.)
        ('6th-grade-review-section-2', 'L1'): (
            esc('Factor completely by pulling out the greatest common factor: '
                '8x + 16 = A factorization is complete only when the expression '
                'left inside the parentheses has no common factor of its own. '
                'Enter select all expressions that are the complete GCF '
                'factorization.'),
            {}),
        # 8 + 5 = 13. Removed: `8 + 5` (stem verbatim), `13`, `(8 + 5) + 0`,
        # `8 + (5 + 0)` -- all equal 13, all were scored wrong.
        ('6th-grade-review-section-2', 'K9'): (
            esc('Rewrite using the commutative property: 8 + 5 = ')
            + esc(commutative % 'addends'),
            {'choice_2': '5 × 8',          # 40, order switched but operation too
             'choice_3': '8 - 5',          # 3, operation changed, order kept
             'choice_6': '-5 + 8',         # 3, "moving a term flips its sign"
             'choice_7': '8 + (5 × 0)'}),  # 8, identity grabbed with the wrong op
        # 7 x a = 7a. Removed: `7a + 0`, `7 x a` (stem verbatim).
        ('6th-grade-review-section-2', 'K10'): (
            esc('Rewrite using the commutative property: 7 × a = ')
            + esc(commutative % 'factors'),
            {'choice_3': 'a + 7',          # not an identity; 10 vs 21 at a=3
             'choice_4': '7a + 1'}),       # differs by 1 for every a
        ('6th-grade-review-section-2', 'N5'): (
            esc('Rewrite using the commutative property: 7 × a = ')
            + esc(commutative % 'factors'),
            {'choice_3': 'a + 7', 'choice_4': '7a + 1'}),
        # (b + 3) + 9 = b + 12. Removed: `(b + 9) + 3`, `b + 12`, `(b + 3) + 9`.
        ('6th-grade-review-section-2', 'K11'): (
            esc('Rewrite using the associative property: (b + 3) + 9 = ')
            + esc(associative % 'b, 3, 9'),
            {'choice_2': '(b + 3) + (3 + 9)',   # b + 15, old grouping left in
             'choice_3': 'b - (3 + 9)',         # b - 12, outer operation flipped
             'choice_4': '(b + 3) × 9'}),       # 9b + 27
        ('6th-grade-review-section-2', 'N6'): (
            esc('Rewrite using the associative property: (x + 5) + 8 = ')
            + esc(associative % 'x, 5, 8'),
            {'choice_2': '(x + 5) + (5 + 8)',   # x + 18
             'choice_3': 'x - (5 + 8)',         # x - 13
             'choice_4': '(x + 5) × 8'}),       # 8x + 40
        # D6: the b != 0 guard the solution states and Part 1 carries. Without
        # it the key is not "always right". The self-referential trio goes for
        # good: their truth is a function of the OTHER choices, so a later edit
        # re-keys them with no signal at the edit site -- which is how this
        # defect arose. Part 1 Question 2 is NOT touched; its "which outcome is
        # NOT possible" framing is what keeps its copies of these false.
        # F-2. Two separate defects.
        #
        # (1) The GUARD WAS MISSING, not merely asymmetric. This item keys "the
        #     decimal neither terminates nor repeats" as the IMPOSSIBLE outcome,
        #     which is impossible only for a ratio of INTEGERS -- pi/1 neither
        #     terminates nor repeats. Part 2's twin spells the guard out, so the
        #     author already knew it was needed. Adding it changes no
        #     distractor's truth value: every other choice is a possible outcome
        #     under integers (1/4 terminates in two places, 1/3 repeats one
        #     digit, 1/7 repeats six) and stays correctly non-keyed.
        #
        #     This is NOT the forbidden harmonisation. That rule protects the
        #     "which outcome is NOT possible" framing, which is untouched here.
        #
        # (2) Two choices were CATEGORY ERRORS -- "The sign does not matter
        #     here." and "The denominator alone determines answer." are not
        #     outcomes at all, so neither can answer "which outcome is not
        #     possible". Replaced with real outcomes that ARE possible and are
        #     therefore correctly non-keyed: 1/27 = 0.037037... repeats a block
        #     of three, and 1/2 = 0.5 terminates after one place.
        ('topic-1-2', 'Part 1 Question 2'): (
            wrap(['A student uses long division to convert a fraction '
                  '\\(\\dfrac{x}{y}\\), where x and y are integers and '
                  '\\(y\\neq 0\\), into a decimal. Which outcome is '
                  # wrap() interpolates its paragraph bodies VERBATIM and escapes
                  # only the <p> it adds, so markup passed in here must already
                  # be escaped. A raw <strong> becomes a child ELEMENT of
                  # <mattext> rather than text: still well-formed XML, so the
                  # gate passed it, but Canvas takes the node's text content and
                  # the emphasis on NOT silently disappears -- and NOT is the
                  # word that inverts this whole item.
                  '&lt;strong&gt;NOT possible&lt;/strong&gt;?'])
            + check_para(SELECT_BOILER),
            {'wrong_3': 'The decimal terminates after two places.',
             'wrong_4': 'The decimal repeats a single digit forever.',
             'wrong_5': 'The decimal repeats a block of six digits.',
             'wrong_6': 'The decimal repeats a block of three digits.',
             'wrong_7': 'The decimal terminates after one place.'}),
        ('topic-1-2', 'Part 2 Question 2'): (
            wrap(['A student uses long division to convert a fraction '
                  '\\(\\dfrac{a}{b}\\), where a and b are integers and '
                  '\\(b\\neq 0\\), into a decimal. Which of the following '
                  'statements about the long division and its result is always '
                  'right?']) + check_para(SELECT_BOILER),
            {'wrong_3': 'A remainder of 0 always appears eventually, so the '
                        'division always stops.',
             'wrong_4': 'During the long division, any whole number can turn up '
                        'as a remainder.',
             'wrong_5': 'If the division never stops, the digits never settle '
                        'into a repeating block.',
             'wrong_6': 'With the denominator fixed, changing the numerator can '
                        'never change whether the decimal terminates.',
             'wrong_7': 'A negative fraction gives a decimal that neither '
                        'terminates nor repeats.'}),
    }


def do_rebuild(raw, pkg, title, context, parts, log):
    """Replace one item with N single-task items, authored from scratch.

    Used where the source packs several tasks into one stem with no structure a
    splitter can key on -- topic-1-1 Q1 carries Part A and Part B inline in a
    single paragraph, which is why the earlier census missed it entirely, and
    Part A itself asks two things ("represent both changes AND find their sum").

    parts: list of (suffix, kind, prompt, payload)
      ('num',  (value, format sentence))
      ('sel',  (keep-suffixes, [(ident-suffix, text), ...] authored))
    """
    block = item_block(raw, title)
    if block is None:
        log.append(f'  !! {pkg} {title}: item not found')
        return raw
    base = re.search(r'<item ident="([^"]*)"', block).group(1)
    ref = re.search(r'<fieldlabel>assessment_question_identifierref</fieldlabel>\s*'
                    r'<fieldentry>([^<]*)</fieldentry>', block).group(1)
    labels = dict(re.findall(
        r'<response_label ident="([^"]*)">\s*<material>\s*'
        r'<mattext texttype="text/html">(.*?)</mattext>', block, re.S))

    out = []
    for suffix, kind, prompt, payload in parts:
        ident, newtitle = f'{base}{suffix}', f'{title}{suffix}'
        stem = wrap([(context + ' ' + prompt).strip()])
        if kind == 'num':
            value, fmt = payload
            out.append(ITEM.format(
                ident=ident, title=newtitle, qtype='numerical_question',
                answer_ids='choice_1', ref=f'{ref}{suffix}',
                stem=stem + check_para(fmt), body=FIB, resp=resp_numeric(value)))
            log.append(f'  rebuild  {newtitle:19s} -> numeric {value}')
        else:
            keep, authored = payload
            ids = [f'{base}_{s}' for s in keep]
            missing = [i for i in ids if i not in labels]
            if missing:
                log.append(f'  !! {pkg} {newtitle}: missing {missing}')
                return raw
            for suf, text in authored:
                aid = f'{base}_{suf}'
                labels[aid] = '&lt;p&gt;' + esc(text) + '&lt;/p&gt;'
                ids.append(aid)
            keys = [i for i in ids if '_correct_' in i]
            wrongs = [i for i in ids if '_correct_' not in i]
            choices = ''.join(
                '\n              <response_label ident="%s">'
                '\n                <material>'
                '\n                  <mattext texttype="text/html">%s</mattext>'
                '\n                </material>'
                '\n              </response_label>' % (i, labels[i]) for i in ids)
            body = ('<response_lid ident="response1" rcardinality="Multiple">'
                    '\n            <render_choice>%s'
                    '\n            </render_choice>'
                    '\n          </response_lid>' % choices)
            out.append(ITEM.format(
                ident=ident, title=newtitle, qtype='multiple_answers_question',
                answer_ids=','.join(ids), ref=f'{ref}{suffix}',
                stem=stem + check_para(SELECT_BOILER), body=body,
                resp=resp_select(keys, wrongs)))
            log.append(f'  rebuild  {newtitle:19s} -> select-all, '
                       f'{len(keys)} of {len(ids)}')
    return raw.replace(block, '\n'.join(out))


# --------------------------------------------------------------------------
# The written-response pass. Every select-all item whose answer a student can
# TYPE becomes one or more written-response items -- whole first, parts after.
#
# Order is deliberate and is the author's ruling: the whole-form item comes
# first so a student meets it cold, and the parts follow as scaffolding. The
# leak runs the harmless way -- a student who can assemble the whole would have
# earned the parts anyway, while one who cannot still earns part marks -- and it
# is what caps the loss to one mark of three when a spacing variant slips past
# the accepted list on a typed expression.
#
# Each entry: (suffix, kind, task sentence, answer(s)).
#   'num'   -> numerical_question, answer is one number
#   'short' -> short_answer_question, answers enumerated verbatim
#   'expr'  -> short_answer_question, answers generated by expr_variants from
#              canonical forms with '@' marking the multiplication slot
# CONTEXT supplies the shared scenario sentence for split families.
# --------------------------------------------------------------------------
NOSPACE = 'Use no spaces.'
EXPAND = {
 ('6th-grade-review-section-1', 'F5'): ('Combine like terms: 6y - 2y', [
   ('', 'expr', 'Write the simplified expression. ' + NOSPACE
        + ' Example: for 3x + 5x write 8x.', ['4y', '4@y']),
 ]),
 ('6th-grade-review-section-1', 'G1'): ('3(y + 6)', [
   ('', 'expr', 'Write the expanded expression, the y term first. ' + NOSPACE
        + ' Example: for 2(x + 4) write 2x+8.', ['3y+18']),
 ]),
 ('6th-grade-review-section-2', 'K2'): ('Prime factorization of 90', [
   ('', 'short', 'Write the prime factors from smallest to largest, separated '
        'by commas. ' + NOSPACE + ' Example: for 12 write 2,2,3.',
    ['2,3,3,5', '2, 3, 3, 5']),
 ]),
 ('6th-grade-review-section-2', 'K9'): ('Rewrite using the commutative property: 8 + 5', [
   ('', 'expr', 'Write the same two addends joined by the same operation in the '
        'opposite order. ' + NOSPACE + ' Example: for 2 + 7 write 7+2.', ['5+8']),
 ]),
 ('6th-grade-review-section-2', 'L1'): (
   'Factor completely by pulling out the greatest common factor: 8x + 16. '
   'A factorization is complete only when the expression left inside the '
   'parentheses has no common factor of its own.', [
   ('', 'expr', 'Write the complete factorization, the common factor first and '
        'the terms inside the parentheses in the order they appear. ' + NOSPACE
        + ' Example: for 6x + 9 write 3(2x+3).',
    ['8@(x+2)', '8@(2+x)', '(x+2)@8', '(2+x)@8']),
 ]),
 ('6th-grade-review-section-2', 'N7'): (
   'Is subtraction associative? Compare (12 - 4) - 3 and 12 - (4 - 3).', [
   ('', 'short', 'Is subtraction associative? Write yes or no.', ['no', 'No']),
   ('b', 'num', 'What is the value of (12 - 4) - 3?', '5'),
   ('c', 'num', 'What is the value of 12 - (4 - 3)?', '11'),
 ]),
}
# ---- 6th-grade review, section 1 -------------------------------------------
EXPAND[('6th-grade-review-section-1', 'A1')] = (
  'A point is plotted on a number line.', [
   ('', 'num', 'The point is 4 units to the RIGHT of 0. Write its coordinate.', '4'),
   ('b', 'num', 'A second point is 4 units to the LEFT of 0. Write its coordinate.', '-4'),
])
EXPAND[('6th-grade-review-section-1', 'H6')] = ('Graph 6 < y on a number line.', [
   ('', 'short', 'Describe the graph you would draw: write the circle type and '
        'the ray direction, separated by a comma. ' + NOSPACE
        + ' Example: closed,left', ['open,right', 'open, right']),
])
EXPAND[('6th-grade-review-section-1', 'H7')] = ('Graph x > 2 on a number line.', [
   ('', 'short', 'Describe the graph you would draw: write the circle type and '
        'the ray direction, separated by a comma. ' + NOSPACE
        + ' Example: closed,left', ['open,right', 'open, right']),
])
# ---- 6th-grade review, section 2 -------------------------------------------
EXPAND[('6th-grade-review-section-2', 'K1')] = ('Is 8x + 1 a linear expression?', [
   ('', 'short', 'Write yes or no.', ['yes', 'Yes']),
   ('b', 'num', 'What is the exponent on x in 8x + 1?', '1'),
])
for _p, _t, _var, _num in (('K10', 'K10', 'a', '7'), ('N5', 'N5', 'a', '7')):
    EXPAND[('6th-grade-review-section-2', _t)] = (
      'Rewrite using the commutative property: 7 × a', [
       ('', 'expr', 'Write the same two factors joined by the same operation in '
            'the opposite order. ' + NOSPACE
            + ' Use * for multiply. Example: for 3 × b write b*3.',
        ['%s@%s' % (_var, _num)]),
    ])
for _t, _v, _x, _y in (('K11', 'b', '3', '9'), ('N6', 'x', '5', '8')):
    EXPAND[('6th-grade-review-section-2', _t)] = (
      'Rewrite using the associative property: (%s + %s) + %s. Keep the addends '
      'in this same left-to-right order and move only the grouping.'
      % (_v, _x, _y), [
       ('', 'expr', 'Write the regrouped expression. ' + NOSPACE
            + ' Example: for (n + 2) + 6 write n+(2+6).',
        ['%s+(%s+%s)' % (_v, _x, _y)]),
    ])



# ---- topic-1-1 --------------------------------------------------------------
for _pt, _s1, _s2, _v1, _v2 in (
        ('Part 1', 'rises 18 meters from a point below sea level, then descends '
                   '18 meters', 'submarine', '+18', '-18'),
        ('Part 2', 'descends 24 meters from a trail marker, then climbs 24 '
                   'meters', 'hiker', '-24', '+24')):
    _ctx = 'A %s %s.' % (_s2, _s1)
    EXPAND[('topic-1-1', '%s Question 1a' % _pt)] = (_ctx, [
       ('', 'num', 'Write the signed number for the FIRST change. ' + PALETTE_NEG, _v1),
       ('b', 'num', 'Write the signed number for the SECOND change. ' + PALETTE_NEG, _v2),
    ])
    EXPAND[('topic-1-1', '%s Question 1c' % _pt)] = (
       _ctx + ' The two changes are additive inverses of each other.', [
       ('b', 'short', 'Are their magnitudes the same or different? Write same or '
            'different.', ['same', 'Same']),
       ('c', 'short', 'Are their signs the same or opposite? Write same or '
            'opposite.', ['opposite', 'Opposite']),
    ])
for _pt, _a, _b in (('Part 1', 'a', 'b'), ('Part 2', 'p', 'q')):
    _lt, _gt = (_a, _b) if _pt == 'Part 1' else (_b, _a)
    EXPAND[('topic-1-1', '%s Question 2' % _pt)] = (
      'On a number line, zero is in the middle. Two mystery numbers %s and %s '
      'satisfy %s + %s = 0, with one negative and one positive.' % (_a, _b, _a, _b), [
       ('', 'short', 'Write an equation relating the ABSOLUTE VALUES of %s and %s. '
            % (_a, _b) + NOSPACE + ' Use | | for absolute value. '
            'Example: for m and n write |m|=|n|.',
        ['|%s|=|%s|' % (_a, _b), '|%s|=|%s|' % (_b, _a),
         '|%s| = |%s|' % (_a, _b), '|%s| = |%s|' % (_b, _a)]),
    ])
# ---- topic-1-2 --------------------------------------------------------------
for _pt, _x, _y in (('Part 1', 'x', 'y'), ('Part 2', 'a', 'b')):
    EXPAND[('topic-1-2', '%s Question 2' % _pt)] = (
      'A student uses long division to convert a fraction %s/%s, where %s and %s '
      'are integers and %s is not zero, into a decimal.' % (_x, _y, _x, _y, _y), [
       ('', 'short', 'Can the decimal go on forever WITHOUT ever repeating? '
            'Write yes or no.', ['no', 'No']),
    ])
# The twins keyed DIFFERENT derivations -- P1 the raw 99x = 27 and P2 the
# simplified 3x = 2, which is 9x = 6 divided by 3. Invisible while both were
# offered as select-all strings; fatal once the student types the numbers, since
# the same method applied to both yields 99,27 and 9,6 and P2 would mark a
# correct student wrong. Both now key the raw derivation (BF-2026-068).
for _pt, _who, _dec, _mul, _lhs, _rhs, _frac in (
        ('Part 1', 'Jordan', '0.272727...', '100', '99', '27', '3/11'),
        ('Part 2', 'Mia',    '0.666...',    '10',  '9',  '6',  '2/3')):
    EXPAND[('topic-1-2', '%s Question 3' % _pt)] = (
      'In a class debate, %s says %s is rational; the other student says it is '
      'not, because it never ends.' % (_who, _dec), [
       ('', 'short', 'Which student is correct? Write their name.', [_who, _who.lower()]),
       ('b', 'num', 'Let x = %s. Multiply by %s and subtract x. What number '
            'multiplies x on the left?' % (_dec, _mul), _lhs),
       ('c', 'num', 'And what number is on the right?', _rhs),
       ('d', 'short', 'Write %s as a fraction in lowest terms. ' % _dec + NOSPACE
            + ' Example: write 1/2.', [_frac]),
    ])
# ---- topic-1-3 --------------------------------------------------------------
for _pt, _a, _b, _c, _mid, _fin in (('Part 1', '10', '4', '8', '6', '-2'),
                                    ('Part 2', '12', '5', '9', '7', '-2')):
    EXPAND[('topic-1-3', '%s Question 1a' % _pt)] = (
      'In the first round of a game a player scores %s points, then loses %s '
      'points, then loses %s points.' % (_a, _b, _c), [
       ('', 'expr', 'Write the expression for the round, in the order the turns '
            'happened, using signed numbers. ' + NOSPACE
            + ' Example: for +5 then -2 write 5+(-2).',
        ['%s+(-%s)+(-%s)' % (_a, _b, _c)]),
       ('d', 'num', 'What is the score after the first two turns?', _mid),
    ])
# ---- topic-1-6 --------------------------------------------------------------
for _pt, _n, _pos, _neg in (('Part 1', '5', '25', '-25'), ('Part 2', '6', '36', '-36')):
    EXPAND[('topic-1-6', '%s Question 4b' % _pt)] = (
      'Compare (-%s)^2 and -%s^2.' % (_n, _n), [
       ('', 'short', 'Explain how the two expressions differ: in which one is the '
            'negative sign squared? Write with parentheses or without '
            'parentheses.', ['with parentheses', 'with']),
    ])
# ---- topic-sc-1 -------------------------------------------------------------
for _pt, _n1, _n2, _a1, _a2 in (('Part 1', '10.4', '10.6', 'cat', 'rabbit'),
                                ('Part 2', '9.3', '9.8', 'dog', 'cat')):
    EXPAND[('topic-sc-1', '%s Question 1' % _pt)] = (
      'Your %s weighs %s pounds. The %s weighs %s pounds.' % (_a1, _n1, _a2, _n2), [
       ('', 'short', 'Write a TRUE statement using the greater-than symbol. '
            + NOSPACE + ' ' + PALETTE_CMP + ' Example: 7>3',
        ['%s>%s' % (_n2, _n1), '%s > %s' % (_n2, _n1)]),
       ('b', 'short', 'Now write a TRUE statement using the less-than symbol. '
            + NOSPACE + ' ' + PALETTE_CMP + ' Example: 3<7',
        ['%s<%s' % (_n1, _n2), '%s < %s' % (_n1, _n2)]),
    ])
for _pt, _f, _d in (('Part 1', '3/4', '0.75'), ('Part 2', '2/5', '0.4')):
    EXPAND[('topic-sc-1', '%s Question 2' % _pt)] = (
      'Compare the fraction %s with the decimal %s.' % (_f, _d), [
       ('', 'short', 'Is %s less than, greater than, or equal to %s? Write less, '
            'greater, or equal.' % (_f, _d), ['equal', 'Equal']),
       ('c', 'short', 'Write a symbol that makes %s __ %s a true statement. '
            % (_f, _d) + PALETTE_CMP, ['=', '≥', '≤']),
    ])
# ---- topic-sc-2 -------------------------------------------------------------
for _pt, _b, _each, _food in (('Part 1', '2', '4', 'cupcakes'),
                              ('Part 2', '3', '9', 'muffins')):
    EXPAND[('topic-sc-2', '%s Question 2a' % _pt)] = (
      'A person makes %s^4 %s and divides them equally among %s^2 friends.'
      % (_b, _food, _b), [
       ('', 'expr', 'Write the expression for how many each friend gets, as one '
            'power divided by another. ' + NOSPACE
            + ' Example: for 5^3 shared among 5^1 write 5^3/5^1.',
        ['%s^4/%s^2' % (_b, _b)]),
       ('c', 'num', 'Written as a single power of %s, what is the exponent?' % _b, '2'),
    ])


def do_expand(raw, pkg, title, spec, log):
    """One select-all item becomes N written-response items, whole first.

    Modelled on do_shortsplit, which already proved the shape: derive the new
    idents and the assessment_question_identifierref from the parent so nothing
    collides corpus-wide, and emit through the same ITEM template so every new
    item carries the metadata the gate asserts. The first entry keeps the
    parent's bare ident and title -- it IS the item, re-typed -- and the parts
    take lettered suffixes (BF-2026-068).
    """
    block = item_block(raw, title)
    if block is None:
        log.append(f'  !! {pkg} {title}: item not found')
        return raw
    context, parts = spec
    base = re.search(r'<item ident="([^"]*)"', block).group(1)
    ref = re.search(r'<fieldlabel>assessment_question_identifierref</fieldlabel>\s*'
                    r'<fieldentry>([^<]*)</fieldentry>', block).group(1)
    out = []
    for suffix, kind, task, ans in parts:
        if kind == 'num':
            vals = [ans]
            fmt = (INTEGER if not '.' in ans else DECIMAL)
            # ...unless the task sentence already says it. Appending
            # unconditionally put "Include the negative sign if the answer is
            # negative." twice in one stem on every part whose author had
            # already written it, which criterion 7 names as a duplicated
            # instruction block (BF-2026-070).
            if (ans.strip().startswith(('-', '\u2212'))
                    and PALETTE_NEG not in task):
                fmt += ' ' + PALETTE_NEG
            body, qtype, resp = FIB, 'numerical_question', resp_numeric(ans)
        else:
            vals = (expr_variants(ans) if kind == 'expr'
                    else with_unicode_minus(list(ans)))
            fmt = ''
            body, qtype = SHORT_FIB, 'short_answer_question'
            resp = resp_short(vals)
        # esc() first: wrap() takes ALREADY-ESCAPED text, and these stems
        # carry raw < > = ≠ ≥ ≤ in their symbol palettes. Passing them
        # through unescaped produced a <mattext> containing a literal '<'
        # and the whole package stopped parsing (BF-2026-068).
        stem = wrap([esc(context + ' ' + task)]
                    + ([esc(fmt)] if fmt else []))
        out.append(ITEM.format(
            ident=f'{base}{suffix}', title=f'{title}{suffix}',
            qtype=qtype, answer_ids='choice_1',
            ref=f'{ref}{suffix}', stem=stem, body=body, resp=resp))
        log.append(f'  expand   {title+suffix:20s} {qtype.split("_")[0]:9s} '
                   f'{len(vals):3d} accepted')
    return raw.replace(block, '\n'.join(out))


def do_shortsplit(raw, pkg, title, spec, log):
    """One expression-writing item becomes two short-answer items, split by the
    FORM of expression asked for. Splitting by form rather than by "write a
    different one" is what makes this safe: Canvas cannot compare one item's
    answer with another's, so "a different expression" would accept the same
    string twice. Form-a strings contain no '|' and form-b strings all do, so the
    two accepted sets are provably disjoint.
    """
    block = item_block(raw, title)
    if block is None:
        log.append(f'  !! {pkg} {title}: item not found')
        return raw
    context, phrase, acc_a, acc_b, (clause_a, clause_b) = spec
    base = re.search(r'<item ident="([^"]*)"', block).group(1)
    ref = re.search(r'<fieldlabel>assessment_question_identifierref</fieldlabel>\s*'
                    r'<fieldentry>([^<]*)</fieldentry>', block).group(1)

    out = []
    for suffix, task, acc, check in (
            ('a', 'Write one expression that uses subtraction and no '
                  'absolute-value bars to represent the ' + phrase + '.'
                  + clause_a,
             acc_a, FORM_A),
            # Method-enumerating, not form-general and not order-pinned. Pinning
            # the order would close the set but rule the answer key's own
            # |-8|+5 method off-form; staying form-general leaves the family
            # open. Naming the methods does both: the set closes by enumeration
            # and every method the key endorses stays on-form.
            ('b', 'Write one expression that uses absolute-value bars to '
                  'represent the ' + phrase + '.' + clause_b, acc_b, FORM_B)):
        vals = with_unicode_minus(acc)
        stem = wrap([context + ' ' + task]) + check_para(check)
        out.append(ITEM.format(
            ident=f'{base}{suffix}', title=f'{title}{suffix}',
            qtype='short_answer_question', answer_ids='choice_1',
            ref=f'{ref}{suffix}', stem=stem, body=SHORT_FIB,
            resp=resp_short(vals)))
        log.append(f'  short    {title}{suffix:1s} -> {len(vals)} accepted strings')
    return raw.replace(block, '\n'.join(out))


# The corrected arrowhead, and the broken one it replaces. `markerUnits`
# defaulting to "strokeWidth" scales the marker by the ray's stroke-width:5, so
# a 9x6 path paints at 45x30, and refX="9" pins the tip at the circle -- putting
# the body 45px the WRONG side of it. On a number line ink means membership, so
# that wedge asserted 1.73 units the graph must leave blank (BF-2026-039).
MARKER_BROKEN = ('<marker id="arrow" markerWidth="10" markerHeight="10" '
                 'refX="9" refY="3" orient="auto" markerUnits="strokeWidth">'
                 '<path d="M0,0 L0,6 L9,3 z" fill="#075985"/>')
MARKER_FIXED = ('<marker id="arrow" markerWidth="18" markerHeight="14" '
                'refX="17" refY="7" orient="auto" markerUnits="userSpaceOnUse">'
                '<path d="M0,0 L0,14 L17,7 z" fill="#075985"/>')

# Where the $IMS-CC-FILEBASE$ mirrors go, relative to the package root. The
# empty string is the archive root itself. See do_media for why all of these
# and not just one.
MIRROR_DIRS = ('web_resources', '')


def do_figstem(raw, pkg, title, text, log):
    """Reword a figure item's prose while leaving its <img> exactly as it is.

    The stem is `<prose> &lt;img src=... /&gt;` in one mattext, so only the part
    before the image is replaced. The img is preserved byte-for-byte: criterion 7
    prescribes the $IMS-CC-FILEBASE$ form corpus-wide, and this change is about
    the sentence, not the path.
    """
    block = item_block(raw, title)
    if block is None:
        log.append(f'  !! {pkg} {title}: item not found')
        return raw
    # Operate on the FIRST text/html mattext only -- that is the stem -- and
    # only if the image is inside it.
    #
    # Two bugs lived here. A bare `.*?` ran from the stem's opening tag to the
    # first &lt;img ANYWHERE in the item, so an item whose stem had no image but
    # whose choice did would lose its stem, the intervening choices, and their
    # response_label openers in one replace. Bounding the span to a single
    # mattext fixed that but not the second problem: re.search scans forward, so
    # it simply re-anchored on the CHOICE's mattext and rewrote the choice text
    # instead. Neither is reachable in this corpus -- all three &lt;img
    # occurrences sit in the stem mattext of A1/H6/H7 -- but Shape A items carry
    # 9-11 text/html mattexts each, so both are one authored image away from
    # being live (BF-2026-049).
    m = re.search(r'<mattext texttype="text/html">((?:(?!</mattext>).)*?)</mattext>',
                  block, re.S)
    if not m or '&lt;img' not in m.group(1):
        log.append(f'  !! {pkg} {title}: no prose-then-image stem')
        return raw
    inner = m.group(1)
    new = block.replace(m.group(0),
                        f'<mattext texttype="text/html">{text} '
                        f'{inner[inner.index("&lt;img"):]}</mattext>')
    log.append(f'  figstem  {title:18s} diagram made supplementary')
    return raw.replace(block, new)


def do_media(pkgdir, pkg, log):
    """Media stage -- the pipeline had none, so media could not be fixed at all.

    Nothing in this pipeline ever read or wrote an SVG, and build.sh rebuilds
    from a git ref rather than the working tree, so editing a figure inside the
    shipped zip was silently discarded by the next build. That is why A1 still
    carried the broken arrowhead long after H6/H7 were repaired.

    Two jobs:

    1. Normalise any figure still carrying the pre-BF-2026-039 marker. A1 is the
       only one, and it is inert there ONLY because A1 happens to have no rays --
       the record calls it a live trap, since any future edit that adds one
       inherits the defect. Fixing it now costs nothing and disarms it.

    2. Hedge the $IMS-CC-FILEBASE$ path depth. The src attributes say
       `$IMS-CC-FILEBASE$/media/<f>.svg`; the files sit at `<quizfolder>/media/`.
       The token stands for the root of the package's imported web content, and
       nothing here can establish which directory Canvas maps that to.

       THREE readings are plausible, not two -- an earlier draft of this
       docstring said two and then mirrored to a location that was neither of
       them, leaving the reading it was most worried about still unhedged
       (BF-2026-049):

         a) `<quizfolder>/`   -- the files already sit here
         b) `web_resources/`  -- where Canvas's own CC exports put web content
         c) the archive root  -- the literal reading of "package root"

       So emit at all three and declare all three. Whichever way the token
       resolves, a file is there. Six extra copies of three ~12 KB SVGs is a
       trivial price for removing a question that cannot otherwise be answered
       without a live Canvas. The src strings are untouched; criterion 7
       prescribes that form corpus-wide.
    """
    # Exclude the mirrors from the source glob, or a rerun copies a file onto
    # itself. Reproduced as shutil.SameFileError killing the whole build when
    # the manifest guard and the filesystem disagreed -- which they can, because
    # they are separate state.
    svgs = sorted(f for f in glob.glob(os.path.join(pkgdir, '*/media/*.svg'))
                  if os.path.basename(os.path.dirname(os.path.dirname(f)))
                  not in MIRROR_DIRS)
    if not svgs:
        return

    for f in svgs:
        s = open(f, encoding='utf-8', newline='').read()
        if MARKER_BROKEN in s:
            open(f, 'w', encoding='utf-8', newline='').write(
                s.replace(MARKER_BROKEN, MARKER_FIXED))
            log.append(f'  media    {os.path.basename(f):32s} arrowhead normalised')

    man = os.path.join(pkgdir, 'imsmanifest.xml')
    if not os.path.exists(man):
        return
    m = open(man, encoding='utf-8', newline='').read()

    # Look the resource up BEFORE writing anything. Bailing out after the copies
    # left undeclared files on disk, which repackage.py's reverse check then
    # hard-failed on with a message naming the symptom and not this cause.
    rid = re.search(r'<resource identifier="([^"]*_media)"', m)
    if not rid:
        log.append(f'  !! {pkg}: no _media resource to mirror')
        return
    new_id = rid.group(1) + '_mirror'

    # Idempotency keys on the resource id, not on a path substring. Testing
    # `f'{d}/media/' in m` was wrong for the archive-root mirror, where d is ''
    # and the test degenerates to `'/media/' in m` -- which the ORIGINAL
    # declaration already satisfies, so the mirror would never have been
    # written at all.
    if new_id in m:
        return

    hrefs = []
    for d in MIRROR_DIRS:
        mirror = os.path.join(pkgdir, *d.split('/')) if d else pkgdir
        os.makedirs(os.path.join(mirror, 'media'), exist_ok=True)
        for f in svgs:
            shutil.copy2(f, os.path.join(mirror, 'media', os.path.basename(f)))
            hrefs.append(f'{d}/media/' + os.path.basename(f) if d
                         else 'media/' + os.path.basename(f))

    files = ''.join(f'<file href="{h}" />' for h in hrefs)
    block = (f'<resource identifier="{new_id}" type="webcontent" '
             f'href="{hrefs[0]}">{files}</resource>')
    m = m.replace('</resources>', block + '</resources>')
    m = m.replace(f'<dependency identifierref="{rid.group(1)}" />',
                  f'<dependency identifierref="{rid.group(1)}" />'
                  f'<dependency identifierref="{new_id}" />')
    open(man, 'w', encoding='utf-8', newline='').write(m)
    log.append(f'  media    manifest         +{len(hrefs)} mirrored at '
               + ', '.join(d or '<archive root>' for d in MIRROR_DIRS))


# Four stems were left as grammatical fragments when an earlier round stripped
# the clause that governed them -- "5/6 = x/18 without x =." reads as a
# sentence that stops halfway. The NUMERIC judge ruled these breach no gate
# criterion, and that is right: the format is stated, true and complete. They
# are still bad text in front of a student, and the instruction each fragment
# was carrying ("don't type the % sign", "don't type x =") is already covered by
# the format sentence that follows it (BF-2026-050).
FRAGMENTS = {
    '0.32 = ____ % omit the % symbol.': '0.32 = ____ % Find the missing number.',
    '5/6 = x/18 without x =.': '5/6 = x/18 Find the value of x.',
    'x + 7 = 18 without x =.': 'x + 7 = 18 Find the value of x.',
    'x/4 = 6 without x =.': 'x/4 = 6 Find the value of x.',
}


def do_fragments(raw, log):
    n = 0
    for old, new in FRAGMENTS.items():
        if esc(old) in raw:
            raw = raw.replace(esc(old), esc(new))
            n += 1
    if n:
        log.append(f'  fragment {n} stem fragments made whole sentences')
    return raw


def do_grammar(raw, log):
    n = len(re.findall(r'Enter select all', raw))
    if n:
        raw = raw.replace('Enter select all', 'Select all')
        log.append(f'  grammar  {n} stems: "Enter select all" -> "Select all"')
    return raw


def do_boiler(raw, log):
    """Every surviving select-all is single-part now; drop the parts sentence."""
    n = 0
    for m in list(BOILER_RE.finditer(raw)):
        if 'Select every choice' not in m.group(0):
            continue
        raw = raw.replace(m.group(0), check_para(SELECT_BOILER))
        n += 1
    if n:
        log.append(f'  boiler   {n} select-all stems reworded')
    return raw


def main(base):
    total = {'convert': 0, 'split': 0, 'short': 0, 'repair': 0,
             'addwrong': 0, 'expand': 0}
    for d in sorted(glob.glob(os.path.join(base, '*/'))):
        xs = [f for f in glob.glob(d + '*/*.xml')
              # basename, not the whole path -- build.sh builds in
              # `mktemp -d`, so an ancestor directory named `metadata` or
              # `manifests` made this filter match every file and the stage
              # silently processed nothing. Hardened at validate.py's two
              # sites by BF-2026-059 and left at these four, so WHICH code
              # paths ran still varied build to build (BF-2026-061).
              if 'manifest' not in os.path.basename(f)
                and 'meta' not in os.path.basename(f)]
        if not xs:
            continue
        path = xs[0]
        pkg = os.path.basename(d.rstrip('/')).replace(
            '-independent-practice-accuracy-check-qti', '').replace(
            '-accuracy-check-qti', '')
        # newline='' so the file's own line endings survive the round trip.
        # 12 of the 14 packages are CRLF; reading without this collapses them to
        # LF and rewrites every line, which destroys the property the whole
        # method rests on -- that an untouched item stays byte-identical.
        raw = open(path, encoding='utf-8', newline='').read()
        crlf = '\r\n' in raw
        raw = raw.replace('\r\n', '\n')
        before = raw.count('<item ident=')
        log = []
        for (p, t), (v, fmt) in CONVERT.items():
            if p == pkg:
                raw = do_convert(raw, pkg, t, v, fmt, log)
                total['convert'] += 1
        for (p, t), (v, stem, fmt) in CONVERT_FULL.items():
            if p == pkg:
                raw = do_convert(raw, pkg, t, v, fmt, log, newstem=stem)
                total['convert'] += 1
        for (p, t), spec in SHORTANS.items():
            if p == pkg:
                raw = do_shortsplit(raw, pkg, t, spec, log)
                total['short'] += 1
        for (p, t), spec in TOSHORT.items():
            if p == pkg:
                raw = do_toshort(raw, pkg, t, spec, log)
                total['short'] += 1
        for p, t in sorted(LETTERED):
            if p == pkg:
                raw = do_letter_prefix(raw, pkg, t, log)
        for (p, t), text in STEM_INSTR.items():
            if p == pkg and (p, t) not in EXPAND:
                raw = do_stem_instr(raw, pkg, t, text, log)
        for (p, t), vals in WIDEN.items():
            if p == pkg and (p, t) not in EXPAND:
                raw = do_widen(raw, pkg, t, vals, log)
        for (p, t), spec in _repairs().items():
            if p == pkg and (p, t) not in EXPAND:
                raw = do_repair(raw, pkg, t, spec, log)
                total['repair'] += 1
        for (p, t), (ctx, parts) in REBUILD.items():
            if p == pkg and (p, t) not in EXPAND:
                raw = do_rebuild(raw, pkg, t, ctx, parts, log)
                total['split'] += 1
        for (p, t), halves in SPLIT.items():
            if p == pkg and (p, t) not in EXPAND:
                raw = do_split(raw, pkg, t, halves, log)
                total['split'] += 1
        # AFTER rebuild and split on purpose: both reconstruct the choice list
        # from scratch, so distractors added earlier would be silently dropped.
        # Several ADDWRONG targets (topic-1-1 Q1a/Q1c, topic-1-6 Q4b) do not
        # even exist as items until those two have run.
        # The written-response pass. Placed AFTER do_split and do_rebuild because
        # several of its targets -- 'Part 1 Question 1a' and its siblings -- are
        # PRODUCTS of the split and do not exist before it runs; and BEFORE the
        # choice-oriented passes below, which have nothing to operate on once an
        # item has been expanded into fill-ins (BF-2026-068).
        for (p, t), spec in EXPAND.items():
            if p == pkg:
                raw = do_expand(raw, pkg, t, spec, log)
                total['expand'] = total.get('expand', 0) + 1
        for (p, t), texts in ADDWRONG.items():
            if p == pkg and (p, t) not in EXPAND:
                # do_addwrong counts only what it actually applied -- counting
                # len(texts) here would report successes it never verified.
                raw = do_addwrong(raw, pkg, t, texts, log, total)
        for (p, t), text in STEM_FIX.items():
            if p == pkg and (p, t) not in EXPAND:
                raw = do_stemfix(raw, pkg, t, text, log)
        # Before do_boiler, which appends the select-all instruction paragraph.
        for (p, t), text in FIGURE_STEM.items():
            if p == pkg and (p, t) not in EXPAND:
                raw = do_figstem(raw, pkg, t, text, log)
        raw = do_fragments(raw, log)
        raw = do_grammar(raw, log)
        raw = do_boiler(raw, log)
        raw = do_sign_sweep(raw, log)
        raw = do_minus_sweep(raw, log)
        raw = do_format_sweep(raw, log)
        after = raw.count('<item ident=')
        out = raw.replace('\n', '\r\n') if crlf else raw
        open(path, 'w', encoding='utf-8', newline='').write(out)

        # Media is a package-level concern, not an item-level one, so it runs
        # against the extracted directory rather than the item XML.
        do_media(d.rstrip('/'), pkg, log)

        if after != before:
            meta = os.path.join(os.path.dirname(path), 'assessment_meta.xml')
            m = open(meta, encoding='utf-8', newline='').read()
            mcrlf = '\r\n' in m
            m = m.replace('\r\n', '\n')
            m = re.sub(r'<points_possible>[\d.]+</points_possible>',
                       f'<points_possible>{float(after)}</points_possible>', m)
            if mcrlf:
                m = m.replace('\n', '\r\n')
            open(meta, 'w', encoding='utf-8', newline='').write(m)
            log.append(f'  points   {before} -> {after}')
        if log:
            print(f'{pkg}:')
            print('\n'.join(log))
    print(f"\n{total['convert']} converted, {total['split']} split, "
          f"{total['short']} expression items to short answer, "
          f"{total['addwrong']} distractors added")


if __name__ == '__main__':
    main(sys.argv[1])
