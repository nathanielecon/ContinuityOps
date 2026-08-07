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
import glob, os, re, html, sys
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
         '|-40|-|-25|', '|-40| - |-25|', '|40|-|25|', '|40| - |25|',
         '|-25+40|', '|-25 + 40|'],
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
         '|-45|-|-18|', '|-45| - |-18|', '|45|-|18|', '|45| - |18|',
         '|-18+45|', '|-18 + 45|'],
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
    ors = []
    for x in accepted(v):
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
    new = re.sub(r'<response_lid.*?</response_lid>', FIB, new, flags=re.S)
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
DECIMAL = 'Enter your answer as a decimal to two places, like 0.00.'
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

        fmt = DECIMAL if any('.' in v for v in vals) else WHOLE
        parts = []
        # These are mathematical instructions, not formatting ones -- dropping
        # them would change the question, so they survive the sweep.
        for pat in (r'Round to the nearest [a-z]+',
                    r'omit the % symbol', r'without x ='):
            k = re.search('(' + pat + ')', old, re.I)
            if k:
                parts.append(k.group(1).rstrip('.') + '.')
        parts.append(fmt)
        if any(v.startswith('-') for v in vals):
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
        used = [int(re.search(r'_wrong_(\d+)$', i).group(1)) for i in wrongs]
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
OPNAME = 'Name the operation and the number, like: add 3.'

TOSHORT = {
    # F3/F4: the old sentence promised "one or two words" while the key was three
    # ("divide by 5"), so a student who obeyed the stem was scored wrong. The key
    # PDF also blesses a second form for each ("subtract 8 (or -8)").
    ('6th-grade-review-section-1', 'F1'): (['coefficient', 'numerical coefficient'],
                                           WORDS, None),
    ('6th-grade-review-section-1', 'F2'): (['variable', 'unknown'], WORDS, None),
    ('6th-grade-review-section-1', 'F3'): (
        ['subtract 8', 'subtract8', 'subtraction', 'subtract', 'minus 8',
         'take away 8', 'subtract eight', 'subtracting 8', 'subtracting eight',
         'minus eight', 'take away eight', '-8'], OPNAME, None),
    ('6th-grade-review-section-1', 'F4'): (
        ['divide by 5', 'divide by5', 'division', 'divide', 'dividing by 5',
         'divide by five', 'dividing by five', 'divide 5', '/5', '÷5',
         '÷ 5'], OPNAME, None),
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
    new = re.sub(r'<response_lid.*?</response_lid>', SHORT_FIB, new, flags=re.S)
    new = re.sub(r'[ \t]*<resprocessing>.*?</resprocessing>',
                 resp_short(vals), new, flags=re.S)
    log.append(f'  toshort  {title:18s} -> {len(vals)} accepted')
    return raw.replace(block, new)


LETTERED = {('6th-grade-review-section-1', t) for t in ('A1', 'H6', 'H7')}


def do_letter_prefix(raw, pkg, title, log):
    block = item_block(raw, title)
    if block is None:
        log.append(f'  !! {pkg} {title}: item not found')
        return raw
    new, n = block, 0
    for m in re.finditer(r'(<response_label ident="[^"]*choice_(\d)">\s*<material>'
                         r'\s*<mattext[^>]*>)(.*?)(</mattext>)', block, re.S):
        letter = 'ABCDEFG'[int(m.group(2)) - 1]
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
    ('6th-grade-review-section-2', 'K6'):
        'Answer with whichever of the two values is greater. Type it the same '
        'way it is written in the question.',
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
    ('6th-grade-review-section-2', 'K6'): ['1 3/4', '1.75', '7/4'],
}


def do_widen(raw, pkg, title, vals, log):
    block = item_block(raw, title)
    if block is None:
        log.append(f'  !! {pkg} {title}: item not found')
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
    m = re.search(r'(<mattext texttype="text/html">)&lt;p&gt;.*?&lt;/p&gt;',
                  block, re.S)
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
                  '<strong>NOT possible</strong>?']) + check_para(SELECT_BOILER),
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
    total = {'convert': 0, 'split': 0, 'short': 0, 'repair': 0, 'addwrong': 0}
    for d in sorted(glob.glob(os.path.join(base, '*/'))):
        xs = [f for f in glob.glob(d + '*/*.xml')
              if 'manifest' not in f and 'meta' not in f]
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
            if p == pkg:
                raw = do_stem_instr(raw, pkg, t, text, log)
        for (p, t), vals in WIDEN.items():
            if p == pkg:
                raw = do_widen(raw, pkg, t, vals, log)
        for (p, t), spec in _repairs().items():
            if p == pkg:
                raw = do_repair(raw, pkg, t, spec, log)
                total['repair'] += 1
        for (p, t), (ctx, parts) in REBUILD.items():
            if p == pkg:
                raw = do_rebuild(raw, pkg, t, ctx, parts, log)
                total['split'] += 1
        for (p, t), halves in SPLIT.items():
            if p == pkg:
                raw = do_split(raw, pkg, t, halves, log)
                total['split'] += 1
        # AFTER rebuild and split on purpose: both reconstruct the choice list
        # from scratch, so distractors added earlier would be silently dropped.
        # Several ADDWRONG targets (topic-1-1 Q1a/Q1c, topic-1-6 Q4b) do not
        # even exist as items until those two have run.
        for (p, t), texts in ADDWRONG.items():
            if p == pkg:
                # do_addwrong counts only what it actually applied -- counting
                # len(texts) here would report successes it never verified.
                raw = do_addwrong(raw, pkg, t, texts, log, total)
        for (p, t), text in STEM_FIX.items():
            if p == pkg:
                raw = do_stemfix(raw, pkg, t, text, log)
        raw = do_grammar(raw, log)
        raw = do_boiler(raw, log)
        raw = do_sign_sweep(raw, log)
        raw = do_format_sweep(raw, log)
        after = raw.count('<item ident=')
        out = raw.replace('\n', '\r\n') if crlf else raw
        open(path, 'w', encoding='utf-8', newline='').write(out)

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
