#!/usr/bin/env python3
"""Structural gate for the answer-format round.

Every rule the round asserts is checked here mechanically, against the built
tree, so that "it passed" is a measurement rather than a claim. Run before
repackaging and before any commit.

Usage:  validate.py <work-tree> [<pristine-baseline-tree>]

The baseline is optional; when given, the line-ending regression check (BF-029)
runs too.
"""
import glob, html, os, re, sys
import xml.etree.ElementTree as ET

AUTOSCORED = {'numerical_question', 'multiple_answers_question',
              'short_answer_question', 'multiple_choice_question'}
MIN_CHOICES = 7

ITEM = re.compile(r'<item ident="([^"]*)" title="([^"]*)">(.*?)</item>', re.S)
LABEL = re.compile(r'<response_label ident="([^"]*)"')

fails, warns, stats = [], [], {}


def bump(k):
    stats[k] = stats.get(k, 0) + 1


def plain(s):
    s = html.unescape(s)
    s = re.sub(r'</?[a-zA-Z][^>]*>', '', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


def keys_of(body):
    cv = re.search(r'<conditionvar>(.*?)</conditionvar>', body, re.S)
    if not cv:
        return set()
    pos = re.sub(r'<not>.*?</not>', '', cv.group(1), flags=re.S)
    return set(re.findall(r'<varequal[^>]*>([^<]*)</varequal>', pos))


def check(work, base=None):
    for f in sorted(glob.glob(os.path.join(work, '*/*/*.xml'))):
        if 'manifest' in f or 'meta' in f:
            continue
        rel = os.path.relpath(f, work)
        raw = open(f, encoding='utf-8', newline='').read()

        try:
            ET.fromstring(raw.encode('utf-8'))
        except Exception as e:
            fails.append(f'{rel}: does not parse: {e}')
            continue

        # BF-029 -- line endings must match the pristine file exactly.
        if base:
            b = os.path.join(base, rel)
            if os.path.exists(b):
                bb = open(b, 'rb').read()
                wb = open(f, 'rb').read()
                if (b'\r\n' in bb) != (b'\r\n' in wb):
                    fails.append(f'{rel}: line-ending convention changed')
                if b'\r\n' in wb and wb.count(b'\r\n') != wb.count(b'\n'):
                    fails.append(f'{rel}: mixed line endings')

        for ident, title, body in ITEM.findall(raw):
            where = f'{rel} :: {title}'
            qt = re.search(r'<fieldlabel>question_type</fieldlabel>\s*'
                           r'<fieldentry>([^<]*)</fieldentry>', body)
            qt = qt.group(1) if qt else '?'
            bump(qt)

            if qt not in AUTOSCORED:
                fails.append(f'{where}: type {qt} is not auto-scored')

            stem = re.search(r'<mattext texttype="text/html">(.*?)</mattext>',
                             body, re.S)
            stem = plain(stem.group(1)) if stem else ''

            # One part per question.
            if re.search(r'Part\s+[AB]\s*:', stem):
                fails.append(f'{where}: stem still contains a Part A/B prompt')

            # The retired boilerplate must be gone everywhere.
            if 'Part 1 and Part 2 both must be correct' in stem:
                fails.append(f'{where}: retired Part 1/Part 2 sentence present')

            keys = keys_of(body)
            idents = LABEL.findall(body)
            choice_idents = [i for i in idents if i != 'answer1']

            if qt == 'numerical_question':
                if any(v.strip().startswith('-') for v in keys) and \
                        not re.search(r'negative sign|minus sign', stem, re.I):
                    fails.append(f'{where}: negative key, no sign guidance')
                if not keys:
                    fails.append(f'{where}: numeric item has no accepted value')

            if qt == 'short_answer_question':
                if not keys:
                    fails.append(f'{where}: short answer has no accepted value')

            if qt in ('multiple_answers_question', 'multiple_choice_question'):
                n = len(choice_idents)
                if n < MIN_CHOICES:
                    fails.append(f'{where}: {n} choices, minimum is {MIN_CHOICES}')
                if len(set(choice_idents)) != n:
                    fails.append(f'{where}: duplicate choice ident')
                # BF-031 -- no key may sit at position 0.
                if choice_idents and choice_idents[0] in keys:
                    fails.append(f'{where}: keyed choice is first (BF-031)')
                # Duplicate visible text is a defect in every shape.
                texts = [plain(t) for t in re.findall(
                    r'<response_label[^>]*>\s*<material>\s*'
                    r'<mattext[^>]*>(.*?)</mattext>', body, re.S)]
                if len(set(texts)) != len(texts):
                    fails.append(f'{where}: two choices share visible text')
                # Scoring must only reference choices that exist.
                for k in keys:
                    if k not in choice_idents:
                        fails.append(f'{where}: key {k} is not a choice')

            # original_answer_ids must be a permutation of the real choices.
            oai = re.search(r'<fieldlabel>original_answer_ids</fieldlabel>\s*'
                            r'<fieldentry>([^<]*)</fieldentry>', body)
            if oai and choice_idents:
                listed = [x for x in oai.group(1).split(',') if x]
                if sorted(listed) != sorted(choice_idents):
                    fails.append(f'{where}: original_answer_ids does not match '
                                 f'the choice list')

    # points_possible must equal the item count on every package.
    for d in sorted(glob.glob(os.path.join(work, '*/'))):
        xs = [x for x in glob.glob(d + '*/*.xml')
              if 'manifest' not in x and 'meta' not in x]
        meta = glob.glob(d + '*/assessment_meta.xml')
        if not xs or not meta:
            continue
        n = open(xs[0], encoding='utf-8', newline='').read().count('<item ident=')
        m = open(meta[0], encoding='utf-8', newline='').read()
        for v in set(re.findall(r'<points_possible>([\d.]+)</points_possible>', m)):
            if abs(float(v) - n) > 1e-9:
                fails.append(f'{os.path.basename(d.rstrip("/"))}: '
                             f'points_possible {v} but {n} items')


if __name__ == '__main__':
    check(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    print('type census:')
    for k, v in sorted(stats.items(), key=lambda t: -t[1]):
        print(f'  {v:4d}  {k}')
    print(f'  {sum(stats.values()):4d}  TOTAL')
    if warns:
        print(f'\n{len(warns)} warnings:')
        for w in warns:
            print('  ' + w)
    if fails:
        print(f'\nFAILED -- {len(fails)} violations:')
        for x in fails:
            print('  ' + x)
        sys.exit(1)
    print('\nall checks pass')
