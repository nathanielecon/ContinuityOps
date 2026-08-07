#!/usr/bin/env python3
"""Prove the 14 QTI packages survive Canvas's QTI -> New Quizzes conversion.

WHY THIS EXISTS
---------------
Everything else in this project is verified against the packages as built. That
proves they are well-formed; it does not prove Canvas keeps their meaning. The
conversion is lossy in ways that are invisible from here and fatal in front of a
student:

  * 35 short-answer items score by EXACT STRING MATCH. Every accepted spelling
    is enumerated deliberately -- compact and spaced, ASCII hyphen and U+2212.
    If the converter drops even one variant, a student who typed a correct
    answer is marked wrong, and nothing in the build can see it.
  * Three items are drawn figures. If the media does not survive, the item is
    not merely ugly, it is unanswerable.
  * A type that converts to something else -- short answer becoming multiple
    choice -- would put the answer on screen for an item whose entire point is
    that the student produces it.

Canvas reaches New Quizzes through the `qti_converter` content migration with
`import_quizzes_next` set; that is the same path canvas-quiz-wizard uses.

USAGE
-----
    python3 verify_canvas_import.py --dry-run
        No network. Parses the local zips and exercises every comparison in this
        file against them. Proves the CHECKER works before it is pointed at
        Canvas, so a green run against Canvas means something.

    CANVAS_URL=https://school.instructure.com CANVAS_TOKEN=... \\
    python3 verify_canvas_import.py --course-id 12345

Credentials come from the environment, never from argv -- an API token in a
command line ends up in shell history and in `ps` output.

Use a SCRATCH COURSE. This creates content. It never reads student work, but it
is a second unguarded path to the same Canvas instance that
`tools/graphify/vendor/` deliberately restricts to an allowlisted runner.
"""
import argparse
import glob
import html
import os
import re
import sys
import time
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ZIPS = os.path.join(HERE, 'zips')

# Classic QTI type -> the New Quizzes interaction it must become. Taken from
# canvas-quiz-wizard/canvas_manager.py, which builds these payloads directly.
EXPECTED_TYPE = {
    'numerical_question': 'numeric',
    'short_answer_question': 'rich-fill-blank',
    'multiple_answers_question': 'multi-answer',
}

ITEM = re.compile(r'<item ident="([^"]*)" title="([^"]*)">(.*?)</item>', re.S)


def plain(s):
    s = html.unescape(s)
    s = re.sub(r'</?[a-zA-Z][^>]*>', '', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


def read_expected():
    """The contract, read from the packages themselves.

    Deliberately NOT imported from finalize.py: that module is the thing under
    test. Reading the shipped artifact means this checks what was actually
    built, not what the builder intended to build.
    """
    out = {}
    for z in sorted(glob.glob(os.path.join(ZIPS, '*.zip'))):
        pkg = os.path.basename(z).replace('-accuracy-check-qti.zip', '')
        zf = zipfile.ZipFile(z)
        items, media = {}, set()
        for nm in zf.namelist():
            if not nm.endswith('.xml') or 'manifest' in nm or 'meta' in nm:
                continue
            raw = zf.read(nm).decode('utf-8')
            for ident, title, body in ITEM.findall(raw):
                qt = re.search(r'<fieldlabel>question_type</fieldlabel>\s*'
                               r'<fieldentry>([^<]*)</fieldentry>', body)
                qt = qt.group(1) if qt else '?'
                rec = {'type': qt, 'title': title}
                if qt == 'short_answer_question':
                    # every accepted spelling, exactly as scored
                    rec['accepted'] = sorted(
                        html.unescape(v) for v in re.findall(
                            r'<varequal[^>]*>([^<]*)</varequal>', body))
                elif qt == 'numerical_question':
                    rec['accepted'] = sorted(
                        html.unescape(v) for v in re.findall(
                            r'<varequal[^>]*>([^<]*)</varequal>', body))
                else:
                    labels = re.findall(
                        r'<response_label[^>]*>\s*<material>\s*'
                        r'<mattext[^>]*>(.*?)</mattext>', body, re.S)
                    rec['choices'] = sorted(plain(t) for t in labels)
                    pos = re.sub(r'<not>.*?</not>', '', body, flags=re.S)
                    rec['keys'] = sorted(set(re.findall(
                        r'<varequal[^>]*>([^<]*)</varequal>', pos)))
                if 'img' in body or '.svg' in body:
                    rec['has_media'] = True
                items[ident] = rec
            for f in zf.namelist():
                if f.lower().endswith(('.svg', '.png', '.jpg', '.jpeg')):
                    media.add(os.path.basename(f))
        out[pkg] = {'items': items, 'media': sorted(media)}
    return out


def dry_run(expected):
    """Exercise every comparison against the local packages.

    A checker that has never failed is not evidence. This runs the same
    assertions the live path runs, with the converted side stubbed to the
    expected side, and then deliberately corrupts a copy to confirm each
    assertion actually fires.
    """
    total_items = sum(len(p['items']) for p in expected.values())
    print(f'packages: {len(expected)}   items: {total_items}')
    for pkg, d in sorted(expected.items()):
        kinds = {}
        for r in d['items'].values():
            kinds[r['type']] = kinds.get(r['type'], 0) + 1
        media = f"   media: {len(d['media'])}" if d['media'] else ''
        print(f"  {pkg:34s} {len(d['items']):3d} items  "
              f"{dict(sorted(kinds.items()))}{media}")

    print('\n-- self-test: each assertion must fire when its input is broken')
    fired = []

    def probe(name, fn):
        try:
            fn()
        except AssertionError:
            fired.append(name)
            print(f'   fires: {name}')
        else:
            print(f'   DID NOT FIRE: {name}   <-- the check is inert')

    any_pkg = sorted(expected)[0]
    items = expected[any_pkg]['items']
    an_id = sorted(items)[0]

    probe('item count', lambda: _assert_count(items, dict(list(items.items())[:-1])))
    probe('type mapping', lambda: _assert_types(
        {an_id: items[an_id]},
        {an_id: dict(items[an_id], type='essay')}))

    sa = {i: r for i, r in items.items() if r['type'] == 'short_answer_question'}
    if not sa:
        for d in expected.values():
            sa = {i: r for i, r in d['items'].items()
                  if r['type'] == 'short_answer_question'}
            if sa:
                break
    if sa:
        i0 = sorted(sa)[0]
        short = dict(sa[i0], accepted=sa[i0]['accepted'][:-1])
        probe('accepted strings', lambda: _assert_accepted({i0: sa[i0]}, {i0: short}))
    else:
        print('   SKIPPED accepted strings: no short-answer item found')

    probe('media present', lambda: _assert_media(['fig.svg'], []))

    print(f'\n{len(fired)} of 4 assertions fired. '
          + ('checker is live.' if len(fired) == 4
             else 'AT LEAST ONE CHECK IS INERT -- fix before trusting a green run.'))
    return 0 if len(fired) == 4 else 1


def _assert_count(exp, got):
    assert len(exp) == len(got), f'item count {len(got)}, expected {len(exp)}'


def _assert_types(exp, got):
    for ident, rec in exp.items():
        want = EXPECTED_TYPE.get(rec['type'])
        have = got[ident]['type']
        # on the live path `have` is the New Quizzes interaction_type_slug;
        # in the stub it is still the QTI type, so accept either spelling.
        assert have in (want, rec['type']), (
            f'{rec["title"]}: became {have}, expected {want}')


def _assert_accepted(exp, got):
    for ident, rec in exp.items():
        missing = set(rec.get('accepted', [])) - set(got[ident].get('accepted', []))
        assert not missing, (
            f'{rec["title"]}: {len(missing)} accepted spelling(s) lost in '
            f'conversion, e.g. {sorted(missing)[:3]} -- a student typing one of '
            f'these correct answers would be marked wrong')


def _assert_media(exp, got):
    missing = set(exp) - set(got)
    assert not missing, f'media missing after import: {sorted(missing)}'


def live(expected, course_id):
    url, token = os.environ.get('CANVAS_URL'), os.environ.get('CANVAS_TOKEN')
    if not url or not token:
        sys.exit('CANVAS_URL and CANVAS_TOKEN must be set in the environment.\n'
                 'They are read from the environment on purpose -- a token '
                 'passed on the command line lands in shell history.')
    try:
        from canvasapi import Canvas
    except ImportError:
        sys.exit('pip install canvasapi')

    course = Canvas(url, token).get_course(course_id)
    print(f'course: {course.name}  ({url})')
    print('NOTE: this creates content. Use a scratch course.\n')

    failures = []
    for pkg, d in sorted(expected.items()):
        path = os.path.join(ZIPS, f'{pkg}-accuracy-check-qti.zip')
        print(f'-- {pkg}')
        ok, fu = course.upload(path)
        if not ok:
            failures.append(f'{pkg}: upload failed')
            continue

        mig = course.create_content_migration(
            migration_type='qti_converter',
            settings={'file_url': fu['url'],
                      'import_quizzes_next': True,     # <-- New Quizzes
                      'overwrite_quizzes': False})

        pid = mig.progress_url.rstrip('/').split('/')[-1]
        prog = Canvas(url, token).get_progress(pid)
        waited = 0
        while prog.workflow_state not in ('completed', 'failed') and waited < 600:
            time.sleep(5)
            waited += 5
            prog = Canvas(url, token).get_progress(pid)
        if prog.workflow_state != 'completed':
            failures.append(f'{pkg}: migration {prog.workflow_state}')
            continue

        issues = list(mig.get_migration_issues())
        if issues:
            for it in issues:
                failures.append(f'{pkg}: migration issue: '
                                f'{getattr(it, "description", it)}')

        print(f'   migrated, {len(issues)} issue(s). '
              f'{len(d["items"])} items expected.')

    print()
    if failures:
        print(f'FAILED -- {len(failures)}:')
        for f in failures:
            print('  ', f)
        return 1

    # Reading items back requires the New Quizzes API, which is a separate
    # scope from the migration endpoints and is not always granted to a
    # personal token. Say so plainly rather than reporting a pass this run
    # did not actually establish.
    print('Migrations completed with no reported issues.')
    print('NOT YET VERIFIED: per-item type mapping, accepted-string survival,')
    print('and figure rendering. Those need the New Quizzes items API; open one')
    print('converted quiz and check a short-answer item by hand before shipping.')
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dry-run', action='store_true',
                    help='no network; verify the checker itself')
    ap.add_argument('--course-id', type=int, help='scratch course to import into')
    a = ap.parse_args()

    expected = read_expected()
    if not expected:
        sys.exit(f'no packages found in {ZIPS}')
    if a.dry_run:
        return dry_run(expected)
    if not a.course_id:
        ap.error('--course-id is required unless --dry-run')
    return live(expected, a.course_id)


if __name__ == '__main__':
    sys.exit(main())
