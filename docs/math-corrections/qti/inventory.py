#!/usr/bin/env python3
"""Inventory every remaining multiple_answers_question: its keyed choices, its
stem, and a proposed disposition under the author's rule --

  numeric entry by default; one part per question; no units; the stem states the
  answer format; select-all only where the answer is genuinely not a number.
"""
import glob, os, re, html, sys, json
import xml.etree.ElementTree as ET

ns = lambda e: e.tag.split('}')[-1]

NUM = re.compile(
    r'^\s*\$?\(?\s*([+-]?\d+(?:,\d{3})*(?:\.\d+)?)\s*\)?\s*'
    r'(feet|ft|foot|meters?|m|kilometers?|km|degrees?|units?|floors?|dollars?|'
    r'per owner|students?|cupcakes? per friend|muffins? per friend|%|)'
    r'\s*(\(?(?:below|above) sea level\)?)?\s*\.?\s*$', re.I)


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


def numeric(key):
    """Strip a Part label, then test whether what remains is a bare number."""
    k = re.sub(r'^\s*Part\s+[AB]\s*:\s*', '', key, flags=re.I)
    k = k.replace(',', '').replace('$', '').strip()
    m = NUM.match(k)
    return m.group(1) if m else None


rows = []
for d in sorted(glob.glob(sys.argv[1] + '/*/')):
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
    pkg = os.path.basename(d.rstrip('/')).replace(
        '-independent-practice-accuracy-check-qti', '').replace(
        '-accuracy-check-qti', '')
    root = ET.fromstring(open(xs[0], encoding='utf-8').read().encode('utf-8'))
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
        stem = ''
        for mt in it.iter():
            if ns(mt) == 'mattext':
                stem = plain(mt)
                break
        vals = [numeric(k) for k in keys]
        if len(keys) == 1:
            disp = 'NUMERIC' if vals[0] is not None else 'THEORETICAL'
        elif len(keys) == 2:
            disp = 'SPLIT' if all(v is not None for v in vals) else \
                   ('SPLIT-PARTIAL' if any(v is not None for v in vals) else 'THEORETICAL')
        else:
            disp = 'THEORETICAL'
        rows.append(dict(pkg=pkg, ident=it.get('ident'), title=it.get('title'),
                         n=len(labels), keys=keys, vals=vals, disp=disp,
                         stem=stem[:240]))

print(json.dumps(rows, indent=1, ensure_ascii=False))
print('\n=== DISPOSITION ===', file=sys.stderr)
from collections import Counter
for k, v in Counter(r['disp'] for r in rows).most_common():
    print(f'{v:4d}  {k}', file=sys.stderr)
print(f'{len(rows):4d}  TOTAL', file=sys.stderr)
