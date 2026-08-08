#!/usr/bin/env python3
"""Convert select-all items whose answer is a single number into Canvas
numerical_question items, matching the shape already proven to work in the
6th-grade packages.

Operates by string surgery on the raw assessment XML so that file formatting,
namespaces and every untouched item survive byte-identical.
"""
import glob, os, re, html, sys, json
from decimal import Decimal, ROUND_HALF_UP
import xml.etree.ElementTree as ET

ns = lambda e: e.tag.split('}')[-1]

UNIT = re.compile(
    r'^\s*\$?\(?\s*([+-]?\d+(?:\.\d+)?)\s*\)?\s*'
    r'(feet|ft|meters?|m|kilometers?|km|degrees?|units?|floors?|dollars?|per owner|students?|%|)\s*\.?\s*$',
    re.I)


def plain(e):
    s = ''.join(e.itertext())
    s = re.sub(r'</?[a-zA-Z][^>]*>', '', html.unescape(s))
    return re.sub(r'\s+', ' ', s).strip()


def walk(e, neg, pos, negs):
    if ns(e) == 'varequal':
        (negs if neg else pos).add(e.text)
        return
    nn = neg ^ (ns(e) == 'not')
    for c in e:
        walk(c, nn, pos, negs)


def numeric_value(key):
    k = key.replace(',', '').replace('$', '').strip()
    m = UNIT.match(k)
    return m.group(1) if m else None


def accepted_values(v):
    """Values Canvas should accept. Exact always; plus the 2dp rounding when the
    exact value carries more than two decimals, so 3/8 = 0.375 is not marked
    wrong by a contract that asks for two places."""
    vals = [v]
    if '.' in v and len(v.split('.')[1]) > 2:
        # Round half UP, the convention taught in class. Python's round() is
        # banker's rounding and turns 0.625 into 0.62, which is not what a
        # student following "round to two decimal places" will type.
        r = str(Decimal(v).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        if r not in vals:
            vals.append(r)
    return vals


def build_resprocessing(vals, indent='        '):
    ors = []
    for v in vals:
        ors.append(f'<varequal respident="response" case="No">{v}</varequal>')
        ors.append(f'<and><vargte respident="response">{v}</vargte>'
                   f'<varlte respident="response">{v}</varlte></and>')
    body = ''.join(ors)
    return (f'{indent}<resprocessing>\n'
            f'{indent}  <outcomes>\n'
            f'{indent}    <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>\n'
            f'{indent}  </outcomes>\n'
            f'{indent}  <respcondition continue="No">\n'
            f'{indent}    <conditionvar><or>{body}</or></conditionvar>\n'
            f'{indent}    <setvar action="Set" varname="SCORE">100</setvar>\n'
            f'{indent}  </respcondition>\n'
            f'{indent}</resprocessing>')


PRESENTATION_RESP = (
    '<response_str ident="response" rcardinality="Single">'
    '<render_fib fibtype="Decimal" prompt="Box" rows="1" columns="20">'
    '<response_label ident="answer1"/>'
    '</render_fib></response_str>')

BOILER = re.compile(
    r'&lt;p&gt;&lt;strong&gt;Canvas accuracy check:&lt;/strong&gt;.*?&lt;/p&gt;', re.S)


def convert_file(path, dry=False):
    raw = open(path, encoding='utf-8').read()
    root = ET.fromstring(raw.encode('utf-8'))
    targets = {}
    for it in [e for e in root.iter() if ns(e) == 'item']:
        fields = [e for e in it.iter() if ns(e) in ('fieldlabel', 'fieldentry')]
        qt = None
        for i, e in enumerate(fields):
            if ns(e) == 'fieldlabel' and e.text == 'question_type' and i + 1 < len(fields):
                qt = fields[i + 1].text
        if qt != 'multiple_answers_question':
            continue
        pos, negs = set(), set()
        for rc in it.iter():
            if ns(rc) == 'respcondition' and any(
                    '100' in (s.text or '') for s in rc.iter() if ns(s) == 'setvar'):
                for c in rc:
                    if ns(c) == 'conditionvar':
                        walk(c, False, pos, negs)
        labels = [e for e in it.iter() if ns(e) == 'response_label']
        keys = [plain(L) for L in labels if L.get('ident') in pos]
        if len(keys) != 1:
            continue
        v = numeric_value(keys[0])
        if v is None:
            continue
        targets[it.get('ident')] = (v, keys[0])

    changed = []
    for ident, (v, origkey) in targets.items():
        m = re.search(r'<item ident="%s"[^>]*>.*?</item>' % re.escape(ident), raw, re.S)
        if not m:
            print(f"  !! could not locate item {ident}", file=sys.stderr)
            continue
        block = m.group(0)
        new = block

        # 1. question type
        new = new.replace('<fieldentry>multiple_answers_question</fieldentry>',
                          '<fieldentry>numerical_question</fieldentry>')
        # 2. answer id list collapses to the single fib answer
        new = re.sub(r'(<fieldlabel>original_answer_ids</fieldlabel>\s*<fieldentry>)[^<]*(</fieldentry>)',
                     r'\1choice_1\2', new)
        # 3. stem: drop the select-all boilerplate, state the answer format
        vals = accepted_values(v)
        instr = 'Enter the number only, no units or symbols.'
        if '.' in v:
            instr += ' Round to two decimal places.'
        newpara = ('&lt;p&gt;&lt;strong&gt;Canvas accuracy check:&lt;/strong&gt; '
                   + instr + '&lt;/p&gt;')
        if BOILER.search(new):
            new = BOILER.sub(newpara, new)
        else:
            print(f"  !! boilerplate not found in {ident}", file=sys.stderr)
        # 4. swap the choice list for a fill-in box
        new = re.sub(r'<response_lid.*?</response_lid>', PRESENTATION_RESP, new, flags=re.S)
        # 5. numeric scoring
        new = re.sub(r'[ \t]*<resprocessing>.*?</resprocessing>',
                     build_resprocessing(vals), new, flags=re.S)

        raw = raw.replace(block, new)
        changed.append((ident, origkey, vals))

    if not dry:
        open(path, 'w', encoding='utf-8').write(raw)
    return changed


if __name__ == '__main__':
    base = sys.argv[1]
    total = []
    for d in sorted(glob.glob(os.path.join(base, '*/'))):
        xs = [f for f in glob.glob(d + '*/*.xml')
              if 'manifest' not in f and 'meta' not in f]
        if not xs:
            continue
        ch = convert_file(xs[0])
        if ch:
            print(f"{os.path.basename(d.rstrip('/'))}: {len(ch)} converted")
            for ident, k, vals in ch:
                print(f"    {ident:38s} '{k}' -> accept {vals}")
        total += ch
    print(f"\nTOTAL CONVERTED: {len(total)}")
