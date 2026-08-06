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
    # Part A is an expression, so it stays select-all; 2^4/2^2 = 4
    ('topic-sc-2', 'Part 1 Question 2'): (
        ('sel', ['correct_1', 'wrong_1', 'wrong_2', 'wrong_5', 'wrong_6'], None),
        ('num', '4', 'Enter your answer as a whole number of cupcakes. ' + ONLY)),
    # 3^4/3^2 = 9
    ('topic-sc-2', 'Part 2 Question 2'): (
        ('sel', ['correct_1', 'wrong_1', 'wrong_2', 'wrong_5', 'wrong_6'], None),
        ('num', '9', 'Enter your answer as a whole number of muffins. ' + ONLY)),
    # Part A is an explanation, so it stays select-all; 10 - 4 - 8 = -2
    ('topic-1-3', 'Part 1 Question 1'): (
        ('sel', ['correct_1', 'correct_2', 'correct_3',
                 'wrong_1', 'wrong_2', 'wrong_3'], None),
        ('num', '-2', NUM_INT)),
    # 12 - 5 - 9 = -2
    ('topic-1-3', 'Part 2 Question 1'): (
        ('sel', ['correct_1', 'correct_2', 'correct_3',
                 'wrong_1', 'wrong_2', 'wrong_3'], None),
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
    m = re.search(r'      <item ident="[^"]*" title="%s">.*?</item>'
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
            _, keep, _ = half
            ids = [f'{base}_{s}' for s in keep]
            missing = [i for i in ids if i not in labels]
            if missing:
                log.append(f'  !! {pkg} {title}{suffix}: missing choices {missing}')
                return raw
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
    total = {'convert': 0, 'split': 0}
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
        for (p, t), halves in SPLIT.items():
            if p == pkg:
                raw = do_split(raw, pkg, t, halves, log)
                total['split'] += 1
        raw = do_boiler(raw, log)
        raw = do_sign_sweep(raw, log)
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
    print(f"\n{total['convert']} converted, {total['split']} split")


if __name__ == '__main__':
    main(sys.argv[1])
