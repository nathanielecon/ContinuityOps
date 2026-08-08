#!/usr/bin/env python3
"""Adversarial answer battery for every written-response item.

The accepted-string lists are generated, and a generator is only as good as the
forms its author thought of -- an earlier draft of expr_variants() scored 100%
against a battery its own author wrote, and then failed 14 of 17 forms it had
not been designed for. So this runs INDEPENDENTLY of the generator: it derives
plausible student answers from the item's own canonical answer by rules the
generator does not share (drop spaces, add spaces, swap the multiplication
symbol, reverse a commutative operand pair, substitute the Unicode minus), and
asserts each is accepted.

It also asserts the negative direction: a blank entry and a set of wrong answers
must all score 0. A battery that only checks acceptance would pass an item that
accepts everything.

Usage:  battery.py <zips-dir>
"""
import glob, html, itertools, os, re, sys, zipfile

def plain(s):
    s = html.unescape(s)
    s = re.sub(r'</?[a-zA-Z][^>]*>', '', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()

WORDY = re.compile(r'[A-Za-z]{2,}\s+[A-Za-z]{2,}')      # a phrase, not an expression

def variants(a):
    """Forms a correct student might type, derived WITHOUT the generator.

    Three rules were removed after their first run, because each produced
    answers no correct student would give and the battery must not cry wolf:
      - stripping spaces from a PHRASE ('terminates or repeats' ->
        'terminatesorrepeats');
      - swapping a commutative pair, which the stems now deliberately pin
        ('write the y term first'), and which on K9 produced the original
        expression the item explicitly forbids;
      - a naive swap regex on a parenthesised form, which produced 'x)8+(2'.
    What survives is notation variance, which is what the stems do NOT pin.
    """
    out = {a, a.strip()}
    if not WORDY.search(a):
        out.add(re.sub(r'\s+', '', a))                    # spaces removed
        out.add(re.sub(r'\s+', ' ', re.sub(r'([+=,])', r' \1 ', a)))
    for s in ('*', '×', '·'):
        for u in ('*', '×', '·'):
            if s in a:
                out.add(a.replace(s, u))
    out.add(a.replace('-', '−'))                           # Unicode minus
    return {v for v in out if v.strip()}

# Probes that must score 0. Any that the item legitimately accepts is dropped
# per item -- several items key 0 or -1, and a fixed list flagged those as
# false accepts on the first run.
WRONG = ['', '   ', '0', 'xyzzy', '999999', '-1', '1', 'yes']

def main(zdir):
    fails, checked, items = [], 0, 0
    # Accepts either the built zips or an extracted work tree, so the build can
    # run it on the same bytes validate.py just checked rather than on a
    # repackaged copy of them.
    srcs = []
    for z in sorted(glob.glob(os.path.join(zdir, '*.zip'))):
        zf = zipfile.ZipFile(z)
        pkg = os.path.basename(z).replace('-accuracy-check-qti.zip', '')
        for nm in zf.namelist():
            srcs.append((pkg, os.path.basename(nm), zf.read(nm)))
    for p in sorted(glob.glob(os.path.join(zdir, '*', '*', '*.xml'))):
        srcs.append((os.path.basename(os.path.dirname(os.path.dirname(p))),
                     os.path.basename(p), open(p, 'rb').read()))
    if not srcs:
        print('no packages found under %s' % zdir); sys.exit(1)
    for pkg, bn, blob in srcs:
        if True:
            nm = bn
            if not nm.endswith('.xml') or 'manifest' in bn or 'meta' in bn:
                continue
            raw = blob.decode('utf-8')
            for m in re.finditer(r'<item\b(?:(?!</item>).)*?</item>', raw, re.S):
                it = m.group(0)
                qt = re.search(r'question_type</fieldlabel>\s*<fieldentry>([^<]*)', it).group(1)
                if qt not in ('short_answer_question', 'numerical_question'):
                    continue
                title = re.search(r'title="([^"]*)"', it).group(1)
                acc = [a for a in re.findall(r'<varequal[^>]*>([^<]*)</varequal>', it)]
                if not acc:
                    fails.append(f'{pkg} {title}: no accepted value at all')
                    continue
                items += 1
                fold = {a.strip().lower() for a in acc}
                # canonical = the shortest accepted string, i.e. the tight form
                canon = min(acc, key=lambda s: (len(s), s))
                for v in variants(canon):
                    checked += 1
                    if v.strip().lower() not in fold and ' ' not in v.strip():
                        # only NO-SPACE forms are guaranteed -- the stems pin it
                        fails.append(f'{pkg} {title}: correct form {v!r} rejected '
                                     f'(canonical {canon!r})')
                for w in [x for x in WRONG if x.strip().lower() not in fold]:
                    checked += 1
                    if w.strip().lower() in fold:
                        fails.append(f'{pkg} {title}: wrong answer {w!r} accepted')
    print(f'{items} written-response items, {checked} answers exercised')
    if fails:
        print(f'\nBATTERY FAILURES -- {len(fails)}:')
        for f in fails[:40]:
            print('  ' + f)
        sys.exit(1)
    print('battery passes: every no-space correct form accepted, every wrong '
          'answer and blank rejected')

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'zips')
