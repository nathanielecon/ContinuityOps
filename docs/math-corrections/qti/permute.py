#!/usr/bin/env python3
"""BF-3 -- break the "answer is always the first choice" property.

Corpus-wide, every choice-based item listed its keyed choices as the leading
contiguous block, and all 14 packages ship shuffle_answers=false. "Select the
first option, or the first N" therefore scored 100% on every such item without
doing any mathematics. No key was wrong, so nothing mis-scored -- the instrument
simply did not measure anything.

This reorders the choices inside each item and rewrites original_answer_ids to
match. It does NOT touch <resprocessing>: scoring references choice idents, not
positions, so the key survives a reorder untouched. That is asserted here rather
than assumed.

The permutation is deterministic, seeded from the item ident via sha256, so the
build is reproducible on any machine and across runs. Python's hash() is
randomised per process and must not be used.

Acceptance for a permutation, in order of priority:
  P1  position 0 is NOT a keyed choice   -- defeats "pick the first"
  P2  the keyed set is not contiguous    -- defeats "pick the first/last N block"
Both are satisfiable unless the item is small and mostly keys (e.g. 2 keys in 3
choices, where P1 and P2 cannot both hold). Such items take P1 and are reported,
never silently downgraded.
"""
import glob, hashlib, os, re, sys
from itertools import permutations

LABEL = re.compile(r'<response_label\b.*?</response_label>', re.S)
ITEM = re.compile(r'<item ident="[^"]*" title="[^"]*">.*?</item>', re.S)
# `<render_choice\b[^>]*>`, not the bare tag: validate.py reads this same
# element and the two regexes disagreeing about what it is has already
# produced one defect (BF-2026-065).
RENDER = re.compile(r'<render_choice\b[^>]*>(.*?)</render_choice>', re.S)


def keyed_idents(item):
    """Idents required by the scoring condition, with <not> subtrees removed."""
    cv = re.search(r'<conditionvar>(.*?)</conditionvar>', item, re.S)
    if not cv:
        return set()
    body = re.sub(r'<not>.*?</not>', '', cv.group(1), flags=re.S)
    return set(re.findall(r'<varequal[^>]*>([^<]*)</varequal>', body))


def rank(order, keys):
    """(P1, P2) satisfaction for a candidate ordering.

    P2 is vacuous for a single-key item -- one element is always a contiguous
    block -- so it counts as satisfied there. The meaningful guarantee for a
    single-key item is P1 plus the fact that its position varies per item,
    which the per-ident seed already gives.
    """
    p1 = order[0] not in keys
    pos = [i for i, x in enumerate(order) if x in keys]
    p2 = True if len(pos) < 2 else pos[-1] - pos[0] != len(pos) - 1
    return (p1, p2)


def choose(idents, keys, seed):
    """Deterministic best ordering. Exhaustive for <=7 choices, sampled above."""
    rng = _Rng(seed)
    n = len(idents)
    if n <= 7:
        cands = list(permutations(idents))
        rng.shuffle(cands)
    else:
        cands = []
        cur = list(idents)
        for _ in range(400):
            rng.shuffle(cur)
            cands.append(tuple(cur))
    best, best_r = None, (-1, -1)
    for c in cands:
        r = rank(c, keys)
        if r == (True, True):
            return c, r
        if (r[0], r[1]) > best_r:
            best, best_r = c, r
    return best, best_r


class _Rng:
    """Reproducible shuffle from a sha256 stream -- no dependence on Python's
    per-process hash seed or on random module version differences."""

    def __init__(self, seed):
        self.s = hashlib.sha256(seed.encode()).digest()
        self.i = 0

    def _byte(self):
        if self.i >= len(self.s):
            self.s = hashlib.sha256(self.s).digest()
            self.i = 0
        b = self.s[self.i]
        self.i += 1
        return b

    def _below(self, n):
        while True:
            v = (self._byte() << 8) | self._byte()
            if v < (65536 // n) * n:
                return v % n

    def shuffle(self, seq):
        for i in range(len(seq) - 1, 0, -1):
            j = self._below(i + 1)
            seq[i], seq[j] = seq[j], seq[i]


def process(path, log):
    raw = open(path, encoding='utf-8', newline='').read()
    crlf = '\r\n' in raw
    raw = raw.replace('\r\n', '\n')
    out = raw

    for item in ITEM.findall(raw):
        ident = re.search(r'<item ident="([^"]*)"', item).group(1)
        title = re.search(r'title="([^"]*)"', item).group(1)
        rc = RENDER.search(item)
        if not rc:
            continue                      # numeric / short answer: no choices
        blocks = list(LABEL.finditer(rc.group(1)))
        if len(blocks) < 2:
            continue
        idents = [re.search(r'ident="([^"]*)"', b.group(0)).group(1) for b in blocks]
        keys = keyed_idents(item) & set(idents)
        if not keys or len(keys) == len(idents):
            continue

        order, r = choose(idents, keys, ident)
        by_id = {i: b.group(0) for i, b in zip(idents, blocks)}

        # Rebuild the render_choice span positionally: the i-th block's text is
        # replaced by the permuted block's text and every separator between them
        # is left exactly as it was, so whitespace and formatting are preserved.
        span = rc.group(1)
        pieces, last = [], 0
        for b, newid in zip(blocks, order):
            pieces.append(span[last:b.start()])
            pieces.append(by_id[newid])
            last = b.end()
        pieces.append(span[last:])
        newspan = ''.join(pieces)

        newitem = item.replace(rc.group(1), newspan)
        newitem = re.sub(
            r'(<fieldlabel>original_answer_ids</fieldlabel>\s*<fieldentry>)[^<]*(</fieldentry>)',
            lambda m: m.group(1) + ','.join(order) + m.group(2), newitem)

        # Scoring must be byte-identical -- a reorder may not touch the key.
        a = re.search(r'<resprocessing>.*?</resprocessing>', item, re.S).group(0)
        b2 = re.search(r'<resprocessing>.*?</resprocessing>', newitem, re.S).group(0)
        assert a == b2, f'{ident}: resprocessing changed'
        assert keyed_idents(newitem) == keyed_idents(item), f'{ident}: key changed'
        assert sorted(order) == sorted(idents), f'{ident}: choice set changed'

        out = out.replace(item, newitem)
        flag = '' if r == (True, True) else f'   <-- only P1 (keys {len(keys)}/{len(idents)})'
        log.append((title, len(idents), len(keys), r, flag))

    if crlf:
        out = out.replace('\n', '\r\n')
    open(path, 'w', encoding='utf-8', newline='').write(out)


def main(base):
    total, partial = 0, 0
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
        log = []
        process(xs[0], log)
        if log:
            pkg = os.path.basename(d.rstrip('/')).replace(
                '-independent-practice-accuracy-check-qti', '').replace(
                '-accuracy-check-qti', '')
            print(f'{pkg}: {len(log)} items permuted')
            for title, n, k, r, flag in log:
                if flag:
                    print(f'    {title:22s} {k}/{n} keys{flag}')
                    partial += 1
            total += len(log)
    print(f'\n{total} items permuted; {partial} could satisfy P1 only')


if __name__ == '__main__':
    main(sys.argv[1])
