#!/usr/bin/env python3
"""Convert the three select-all items whose answer is a fraction into
short_answer items taking a simplified a/b, matching the pattern already used
by 6th-grade Section 2 item K4."""
import glob, os, re, sys

TARGETS = {
    'sc_2_part_1_question_7':  '46/9',
    'sc_2_part_1_question_11': '289/36',
    'sc_2_part_2_question_7':  '9/8',
}

PRESENTATION_RESP = (
    '<response_str ident="response" rcardinality="Single">'
    '<render_fib fibtype="String" prompt="Box" rows="1" columns="20">'
    '<response_label ident="answer1"/>'
    '</render_fib></response_str>')

BOILER = re.compile(
    r'&lt;p&gt;&lt;strong&gt;Canvas accuracy check:&lt;/strong&gt;.*?&lt;/p&gt;', re.S)

INSTR = ('&lt;p&gt;&lt;strong&gt;Canvas accuracy check:&lt;/strong&gt; '
         'Enter a simplified a/b, no spaces or mixed numbers.&lt;/p&gt;')


def resproc(ans, indent='        '):
    return (f'{indent}<resprocessing>\n'
            f'{indent}  <outcomes>\n'
            f'{indent}    <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>\n'
            f'{indent}  </outcomes>\n'
            f'{indent}  <respcondition continue="No">\n'
            f'{indent}    <conditionvar><varequal respident="response" case="No">{ans}</varequal></conditionvar>\n'
            f'{indent}    <setvar action="Set" varname="SCORE">100</setvar>\n'
            f'{indent}  </respcondition>\n'
            f'{indent}</resprocessing>')


def main(base):
    done = []
    for d in sorted(glob.glob(os.path.join(base, '*/'))):
        xs = [f for f in glob.glob(d + '*/*.xml')
              if 'manifest' not in f and 'meta' not in f]
        if not xs:
            continue
        path = xs[0]
        raw = open(path, encoding='utf-8').read()
        touched = False
        for ident, ans in TARGETS.items():
            m = re.search(r'<item ident="%s"[^>]*>.*?</item>' % re.escape(ident), raw, re.S)
            if not m:
                continue
            block = m.group(0)
            new = block.replace('<fieldentry>multiple_answers_question</fieldentry>',
                                '<fieldentry>short_answer_question</fieldentry>')
            new = re.sub(r'(<fieldlabel>original_answer_ids</fieldlabel>\s*<fieldentry>)[^<]*(</fieldentry>)',
                         r'\1choice_1\2', new)
            if not BOILER.search(new):
                print(f"  !! boilerplate missing in {ident}", file=sys.stderr)
            new = BOILER.sub(INSTR, new)
            new = re.sub(r'<response_lid.*?</response_lid>', PRESENTATION_RESP, new, flags=re.S)
            new = re.sub(r'[ \t]*<resprocessing>.*?</resprocessing>', resproc(ans), new, flags=re.S)
            raw = raw.replace(block, new)
            touched = True
            done.append((ident, ans))
        if touched:
            open(path, 'w', encoding='utf-8').write(raw)
    for i, a in done:
        print(f"  {i:28s} -> accepts {a}")
    print(f"TOTAL: {len(done)}")


if __name__ == '__main__':
    main(sys.argv[1])
