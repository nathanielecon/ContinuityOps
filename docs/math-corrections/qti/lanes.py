#!/usr/bin/env python3
"""Generate LANES.md — the live board for the QTI judge/nixer/fixer lanes.

Reads GitHub, writes a snapshot. Run it; do not hand-edit LANES.md.

Why a generator rather than a page someone maintains: ACCEPTANCE.md was exactly
that page, and it sat stale from before the written-response pass while nine
break-fix entries landed around it. A ledger nobody regenerates is how an
unaccepted slice gets mistaken for an accepted one. This reads the actual
issues, so it cannot drift from them.

Usage:
    python3 lanes.py               # write LANES.md
    python3 lanes.py --print       # stdout only
"""
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone

REPO = 'nathanielecon/ContinuityOps'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'LANES.md')

# lane issue -> slice name. Seeded lanes only; add a row when a lane is seeded.
LANES = {
    181: 'SHORTANS',
    184: 'NUMERIC',
    185: 'SOURCE',
    186: 'STRUCT',
}

# The author's thresholds. The supervisor holds these; judges are never told
# them (RALPHY_ORCHESTRATION.md section 12 — a judge told its target scores
# toward it). They live here so the board can show distance-to-bar without any
# of it reaching a dispatch.
BAR_STRUCTURE = 9.5
BAR_MATHEMATICS = 10.0
MATH_SLICES = {'SHORTANS', 'NUMERIC', 'SOURCE'}


def api(path):
    req = urllib.request.Request(
        f'https://api.github.com/repos/{REPO}/{path}',
        headers={'Accept': 'application/vnd.github+json',
                 'User-Agent': 'continuityops-lanes'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def build_hash():
    p = os.path.join(HERE, 'zips', 'sha256sums.txt')
    if not os.path.exists(p):
        return 'unknown'
    out = subprocess.run(['sha256sum', p], capture_output=True, text=True)
    return out.stdout[:16] if out.returncode == 0 else 'unknown'


def scan(comments):
    """Latest worker self-report, verdict and score on a lane."""
    st = {'worker': '-', 'model': '-', 'reasoning': '-', 'ctx': '-',
          'verdict': '-', 'score': None, 'last': '-', 'rounds': 0}
    for c in comments:
        body = c.get('body', '')
        login = c.get('user', {}).get('login', '')
        if login != 'chatgpt-codex-connector[bot]':
            continue
        st['rounds'] += 1
        st['last'] = c.get('created_at', '-')[11:16]
        for key, rx in (('worker', r'worker_id:\s*(\S+)'),
                        ('model', r'model:\s*([^\n]+)'),
                        ('reasoning', r'reasoning:\s*(\S+)'),
                        ('ctx', r'context_remaining:\s*(\S+)')):
            m = re.search(rx, body)
            if m:
                st[key] = m.group(1).strip().strip('`*')
        m = re.search(r'(?im)^\s*verdict:\s*(pass|fail)', body)
        if m:
            st['verdict'] = m.group(1).lower()
        m = re.search(r'Score[:*\s]*([0-9.]+)\s*/\s*10', body)
        if m:
            st['score'] = float(m.group(1))
    return st


def bar_for(slice_name):
    return BAR_MATHEMATICS if slice_name in MATH_SLICES else BAR_STRUCTURE


def main():
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    bh = build_hash()

    rows = []
    for num, name in sorted(LANES.items(), key=lambda kv: kv[1]):
        try:
            issue = api(f'issues/{num}')
            comments = api(f'issues/{num}/comments?per_page=100')
        except Exception as exc:                      # network, rate limit
            rows.append((name, num, {'worker': f'({exc})', 'model': '-',
                                     'reasoning': '-', 'ctx': '-',
                                     'verdict': '-', 'score': None,
                                     'last': '-', 'rounds': 0},
                         'unknown'))
            continue
        rows.append((name, num, scan(comments), issue.get('state', '?')))

    # Auto-opened downstream work: anything the routers created.
    try:
        recent = api('issues?state=all&per_page=25&sort=created&direction=desc')
    except Exception:
        recent = []
    auto = [i for i in recent
            if i.get('user', {}).get('login') == 'github-actions[bot]']

    L = []
    L.append('# QTI lanes — live board')
    L.append('')
    L.append(f'Generated {now} by `lanes.py`. **Do not hand-edit.** Re-run the')
    L.append('script; a board someone maintains by hand is how `ACCEPTANCE.md`')
    L.append('went stale for a whole corpus revision.')
    L.append('')
    L.append(f'**Build under test:** `{bh}`')
    L.append('')
    L.append('## Lanes')
    L.append('')
    L.append('| slice | issue | worker | model | ctx | rounds | verdict | score | bar | last |')
    L.append('|---|---|---|---|---|---|---|---|---|---|')
    for name, num, st, state in rows:
        score = f'{st["score"]:.1f}' if st['score'] is not None else '—'
        bar = f'{bar_for(name):.1f}'
        L.append(f'| **{name}** | [#{num}](https://github.com/{REPO}/issues/{num}) '
                 f'| `{st["worker"]}` | {st["model"]} | {st["ctx"]} '
                 f'| {st["rounds"]} | {st["verdict"]} | {score} | {bar} | {st["last"]} |')
    L.append('')
    L.append('`verdict` and `score` are the latest a worker reported. **No slice is')
    L.append('accepted until it clears its bar twice — once from the judge that found')
    L.append('its defects, re-scoring after repair, and once from a cold judge reading')
    L.append('fresh.** A single pass is not acceptance.')
    L.append('')
    L.append('## Opened by the routers, not by hand')
    L.append('')
    if auto:
        for i in auto[:10]:
            kind = 'PR ' if 'pull_request' in i else 'ISS'
            L.append(f'- `{kind}` [#{i["number"]}](https://github.com/{REPO}/issues/{i["number"]}) '
                     f'{i["created_at"][11:16]} — {i["title"]}')
    else:
        L.append('- none yet')
    L.append('')
    L.append('Each of these is a hop the supervisor did not perform. That is the')
    L.append('measure of zero-hop: not that the wiring looks right, but that')
    L.append('downstream work appears without a human trigger.')
    L.append('')

    text = '\n'.join(L) + '\n'
    if '--print' in sys.argv:
        print(text)
    else:
        with open(OUT, 'w') as fh:
            fh.write(text)
        print(f'wrote {OUT}')


if __name__ == '__main__':
    main()
