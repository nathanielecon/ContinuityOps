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
# The bar is DISTRACTORS, not choices -- it was written as MIN_CHOICES = 7,
# which on a single-key item permits six (BF-2026-043).
#
# It applies to SHAPE A ONLY, and getting that wrong is what produced three
# standing warnings and eleven unnecessary distractors. The frozen rubric scopes
# the rule explicitly:
#
#   Shape A (topic-*, respident="response1", _correct_N/_wrong_N idents):
#       ">=8 choices" -- the bar lives here.
#   Shape B (the two 6th-grade packages, respident="response", choice_N):
#       "All 69 items have fewer than 8 choices. Do not score this as a defect."
#   Split halves (Shape A): exempt by the criterion-6 amendment, because a half
#       inherits only its own part's choices -- and the rubric refuses the
#       alternative in terms: "padding every split half back to 8 means
#       authoring distractors wholesale, and every authored distractor is fresh
#       criterion-2 exposure, which is the trade this amendment refuses."
#
# A1/H6/H7 are Shape B, so they were never below any bar the gate sets, and the
# FIGURE_ITEMS exemption that used to sit here was covering for this mistake
# rather than for anything in the corpus (BF-2026-048).
MIN_DISTRACTORS = 7

# A split half's title ends in a letter glued to its question number --
# "Part 1 Question 1a", "Part 2 Question 4b" -- where an unsplit item ends in
# the bare number.
SPLIT_HALF = re.compile(r'Question\s+\d+[a-z]$')


def respident_of(body):
    """The respident the item DECLARES, which is the only authority.

    Reading it from the scoring block instead only catches a block that
    disagrees with itself; a block that is internally consistent but uniformly
    names the wrong respident matches nothing, never fires <setvar>, and leaves
    SCORE at minvalue 0 for every correct student.
    """
    m = re.search(r'<response_(?:lid|str) ident="([^"]*)"', body)
    return m.group(1) if m else None


def shape_a(body):
    """Shape A is identified by its scoring declaration, not by package name.

    Reading it off the item means a package that is renamed, or an item moved
    between packages, still gets scored under the right shape.
    """
    return 'respident="response1"' in body

ITEM = re.compile(r'<item ident="([^"]*)" title="([^"]*)">(.*?)</item>', re.S)
LABEL = re.compile(r'<response_label ident="([^"]*)"')

fails, warns, stats = [], [], {}
# ident -> [files]. Module scope because the duplicate report runs after every
# package has been walked; Canvas keys questions by ident across the whole
# import, so a collision between two packages matters as much as one inside a
# package (BF-2026-053).
seen_idents = {}


def bump(k):
    stats[k] = stats.get(k, 0) + 1


def plain(s):
    s = html.unescape(s)
    s = re.sub(r'</?[a-zA-Z][^>]*>', '', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


def keys_of(body):
    """Union over ALL <conditionvar> blocks, not just the first.

    Six items ship two <respcondition> blocks (trailing-zero alternates like
    7 and 7.00). re.search saw only the first, so every key-derived rule --
    sign guidance, "no accepted value", "key is not a choice", the distractor
    count -- was blind to the second block. The corpus is clean today, so this
    was a live hole rather than a live bug (BF-2026-047).
    """
    keys = set()
    for cv in re.findall(r'<conditionvar>(.*?)</conditionvar>', body, re.S):
        pos = re.sub(r'<not>.*?</not>', '', cv, flags=re.S)
        keys |= set(re.findall(r'<varequal[^>]*>([^<]*)</varequal>', pos))
    return keys


# A keyed choice may legitimately gain the drawn figure's row letter -- that is
# the ONLY sanctioned change to keyed text on an item that stays select-all
# (BF-2026-041). Everything else is a key move.
LETTER_PREFIX = re.compile(r'^[A-Z]\.\s+')


def keyed_texts(body):
    """The keyed choices' visible TEXT, normalised. Text, not idents, because a
    permutation renames nothing but a rebuild can reassign idents freely."""
    keys = keys_of(body)
    out = set()
    for m in re.finditer(r'<response_label ident="([^"]*)">\s*<material>\s*'
                         r'<mattext[^>]*>(.*?)</mattext>', body, re.S):
        if m.group(1) in keys:
            out.add(LETTER_PREFIX.sub('', plain(m.group(2))))
    return out


def check_keys_vs_base(rel, work_raw, base_raw):
    """No key may silently move.

    The pristine tree was passed in from the start and consulted only for line
    endings, while the brief calls a silently-moved key "the worst defect
    available here" -- the gate was handed exactly the evidence needed and never
    looked at it (BF-2026-050).

    Scope, stated because it is NOT total and should not be read as total:
    items that keep their ident and are select-all in BOTH trees -- 24 of the 34
    select-all items today. The other ten are products of a split or rebuild and
    carry new idents, so there is nothing to compare them against by ident; a
    base item's keys legitimately redistribute across its halves, and some
    became numeric answers whose text will never match. Those are covered by the
    type-specific rules here and by a judge working them by hand. An item whose
    type changed is likewise skipped: comparing choice text across a conversion
    compares two different things.
    """
    wi = {i: b for i, _, b in ITEM.findall(work_raw)}
    for ident, title, bbody in ITEM.findall(base_raw):
        wbody = wi.get(ident)
        if wbody is None:
            continue
        # Fill-in items FIRST, and they are the larger population -- 143 of 177,
        # where the accepted value IS the key and one character moves it. The
        # original check skipped them entirely and the docstring named only the
        # select-all limit, so the omission it did not mention was the bigger
        # one. Changing g6_s1_b1's key from 20 to 21 marks every correct student
        # wrong, and the right answer was sitting in the pristine tree the whole
        # time (BF-2026-051).
        #
        # Widening is legitimate (BF-2026-041/042 added accepted spellings), so
        # the test is SUBSET, not equality: every pristine accepted value must
        # still be accepted. A value that disappears is the defect.
        if 'render_fib' in bbody and 'render_fib' in wbody:
            lost = keys_of(bbody) - keys_of(wbody)
            if lost:
                fails.append(f'{rel} :: {title}: ACCEPTED VALUE DROPPED '
                             f'{sorted(lost)!r} -- a student who gave the '
                             f'pristine answer is now marked wrong')
            continue
        if ('multiple_answers_question' not in bbody
                or 'multiple_answers_question' not in wbody):
            continue
        was, now = keyed_texts(bbody), keyed_texts(wbody)
        if was != now:
            fails.append(
                f'{rel} :: {title}: KEY MOVED. no longer keyed: '
                f'{sorted(was - now)!r}; newly keyed: {sorted(now - was)!r}')


def check(work, base=None):
    for f in sorted(glob.glob(os.path.join(work, '*/*/*.xml'))):
        if 'manifest' in f or 'meta' in f:
            continue
        rel = os.path.relpath(f, work)
        raw = open(f, encoding='utf-8', newline='').read()

        # Every <mattext> body in this corpus carries its HTML ESCAPED
        # (&lt;p&gt;, &lt;strong&gt;). A raw <strong> written into one is
        # still well-formed XML -- it just becomes a child ELEMENT -- so the
        # parse below cannot see it, and it shipped once (BF-2026-047). Canvas
        # takes the node's text content, so the markup silently vanishes; on the
        # item it hit, the word that disappeared was the "NOT" that inverts the
        # question. Mixed conventions inside one body are the tell.
        for mt in re.findall(r'<mattext[^>]*>(.*?)</mattext>', raw, re.S):
            stray = re.findall(r'</?(?:p|strong|em|b|i|br|img|span|div)\b[^>]*>', mt)
            if stray:
                fails.append(f'{rel}: raw HTML {stray[0]!r} inside <mattext> -- '
                             f'must be escaped; Canvas drops it silently')

        try:
            ET.fromstring(raw.encode('utf-8'))
        except Exception as e:
            fails.append(f'{rel}: does not parse: {e}')
            continue

        # BF-029 -- line endings must match the pristine file exactly.
        # And, since BF-2026-050, the pristine tree is used for what it was
        # always there for: proving no key silently moved.
        if base:
            b = os.path.join(base, rel)
            if os.path.exists(b):
                bb = open(b, 'rb').read()
                wb = open(f, 'rb').read()
                if (b'\r\n' in bb) != (b'\r\n' in wb):
                    fails.append(f'{rel}: line-ending convention changed')
                if b'\r\n' in wb and wb.count(b'\r\n') != wb.count(b'\n'):
                    fails.append(f'{rel}: mixed line endings')
                check_keys_vs_base(rel, raw,
                                   open(b, encoding='utf-8', newline='').read())

        # Choice idents were checked for uniqueness; ITEM idents were not.
        # Canvas keys imported questions by item ident, so a collision means one
        # item silently replaces the other -- a 4-item quiz imports as 3 while
        # assessment_meta still claims 4 points (BF-2026-051).
        # Tracked CORPUS-WIDE, not per file. Canvas keys imported questions by
        # ident across the whole import, so a collision between two packages is
        # just as fatal as one inside a package -- and the per-file version
        # missed it entirely (BF-2026-053).
        for i in [x for x, _, _ in ITEM.findall(raw)]:
            seen_idents.setdefault(i, []).append(rel)

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

            # One part per question. F2 is "No item stem may reference a part
            # label AT ALL", not "no Part A: prompt" -- the colon form missed
            # prose like "In Part B you found that..." (BF-2026-053).
            if re.search(r'\bPart\s+[AB1-9]\b', stem):
                fails.append(f'{where}: stem references a part label')

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

            # A correct answer must actually be awarded 100. Nothing checked
            # this: an item whose setvar holds 0 marks every correct student
            # wrong -- the exact harm the rubric's preamble names -- and is
            # invisible to every other rule here (BF-2026-047).
            # The VALUE was checked and the VARIABLE was not, so this was closed
            # halfway. <setvar varname="TOTAL">100</setvar> passed: SCORE is
            # declared by <decvar> and then never written, so it stays at
            # minvalue 0 and every correct student is marked wrong on that item
            # (BF-2026-051).
            for m in re.finditer(r'<setvar([^>]*)>([^<]*)</setvar>', body):
                if 'varname="SCORE"' not in m.group(1):
                    fails.append(f'{where}: setvar writes {m.group(1).strip()!r},'
                                 f' not SCORE -- SCORE is never set, so it stays 0')
                if m.group(2).strip() != '100':
                    fails.append(f'{where}: a correct answer scores '
                                 f'{m.group(2).strip()}, not 100')
            # `if dv and ...` skipped the whole check when <decvar> was ABSENT,
            # which is the worse case: <setvar varname="SCORE"> then writes an
            # outcome nothing declares. And minvalue was never read at all, so
            # minvalue="100" -- every wrong answer scoring full marks -- passed
            # silently (BF-2026-050).
            dv = re.search(r'<decvar([^>]*)>', body)
            if not dv:
                fails.append(f'{where}: no <decvar> -- SCORE is undeclared')
            elif ('maxvalue="100"' not in dv.group(1)
                  or 'minvalue="0"' not in dv.group(1)
                  or 'varname="SCORE"' not in dv.group(1)):
                fails.append(f'{where}: decvar is not '
                             f'maxvalue=100 minvalue=0 varname=SCORE')

            # Package totals compared the meta value to the item COUNT, which
            # assumes every item is worth 1 without ever checking it. An item at
            # 0 points is unscorable, and two compensating errors (0 and 2)
            # leave the package total correct.
            pp = re.search(r'<fieldlabel>points_possible</fieldlabel>\s*'
                           r'<fieldentry>([\d.]+)</fieldentry>', body)
            if not pp or float(pp.group(1)) != 1.0:
                fails.append(f'{where}: points_possible is '
                             f'{pp.group(1) if pp else "absent"}, not 1')

            # --- ITEM SCOPE, and that is the whole point -------------------
            # These three were written for every item and then indented inside
            # the select-all branch, so they ran on 34 of 177 and the other 143
            # -- the larger population -- went unchecked. Twice now a rule of
            # mine has been logged as closed while covering only select-all
            # (BF-2026-051 rule 3 was the same mistake). Scope is the bug that
            # keeps recurring, so these sit here deliberately (BF-2026-053).
            want = respident_of(body)
            if want:
                # Comparison operators too: a numeric item scores through
                # vargte/varlte, so checking only varequal leaves the range
                # conditions unexamined.
                bad = set(re.findall(
                    r'<var(?:equal|gte|lte|lt|gt) respident="([^"]*)"', body)) - {want}
                if bad:
                    fails.append(f'{where}: scoring uses respident {sorted(bad)} '
                                 f'but the item declares "{want}" -- those '
                                 f'conditions match nothing, so SCORE stays 0')

            if qt in ('multiple_answers_question', 'multiple_choice_question'):
                if 'rcardinality="Multiple"' not in body:
                    fails.append(f'{where}: select-all is not '
                                 f'rcardinality="Multiple" -- unscoreable')
            elif qt in ('numerical_question', 'short_answer_question'):
                if 'rcardinality="Single"' not in body:
                    fails.append(f'{where}: fill-in is not rcardinality="Single"')
                # A <not> inside a fill-in's top-level <or> is the same hazard
                # as <and>-to-<or> on a select-all: every entry that is not the
                # negated string satisfies the disjunct, including an EMPTY
                # box, so the item scores 100 for almost any submission. 136 of
                # the corpus's conditionvars are fill-in <or> and none of them
                # was being examined.
                for cv in re.findall(r'<conditionvar>(.*?)</conditionvar>', body, re.S):
                    if '<not>' in cv:
                        fails.append(f'{where}: <not> inside a fill-in '
                                     f'conditionvar -- any non-matching entry, '
                                     f'including an empty box, scores 100')

            if qt in ('multiple_answers_question', 'multiple_choice_question'):
                n = len(choice_idents)
                # keys_of() already strips <not> blocks, which is the only
                # trap-safe way to count keys here (the rubric records that a
                # naive regex makes every choice look keyed).
                ndist = n - len(keys & set(choice_idents))
                if (ndist < MIN_DISTRACTORS and shape_a(body)
                        and not SPLIT_HALF.search(title)):
                    fails.append(f'{where}: {ndist} distractors '
                                 f'({n} choices, {n - ndist} keyed), '
                                 f'minimum is {MIN_DISTRACTORS}')
                if len(set(choice_idents)) != n:
                    fails.append(f'{where}: duplicate choice ident')
                # BF-031 -- no key may sit at position 0.
                if choice_idents and choice_idents[0] in keys:
                    fails.append(f'{where}: keyed choice is first (BF-031)')
                # ...and no CONTIGUOUS RUN of keys. BF-031's own statement of
                # the defect is "pick the first option, OR THE FIRST N, scored
                # 100% without doing any mathematics", and only the first clause
                # was enforced. Keys at positions 1,2,3 pass the position-0 test
                # while "tick boxes 2, 3 and 4" still scores 100 with no
                # reasoning. 8 items have more than one key (BF-2026-051).
                kp = sorted(i for i, c in enumerate(choice_idents) if c in keys)
                if len(kp) > 1 and kp == list(range(kp[0], kp[0] + len(kp))):
                    fails.append(f'{where}: keys occupy a contiguous run {kp} '
                                 f'-- "the first N" scores without reasoning')
                # rcardinality: a select-all rendered Single is radio buttons,
                # so a multi-key item becomes literally unscoreable -- 100 is
                # unreachable no matter what the student does.
                if 'rcardinality="Multiple"' not in body:
                    fails.append(f'{where}: select-all is not '
                                 f'rcardinality="Multiple" -- unscoreable')
                # Duplicate visible text is a defect in every shape.
                texts = [plain(t) for t in re.findall(
                    r'<response_label[^>]*>\s*<material>\s*'
                    r'<mattext[^>]*>(.*?)</mattext>', body, re.S)]
                if len(set(texts)) != len(texts):
                    fails.append(f'{where}: two choices share visible text')
                # The CONNECTIVE, which nothing checked. Flip the single <and>
                # to <or> and the conditionvar becomes a disjunction of one
                # positive varequal and N negations -- so a student who selects
                # NOTHING satisfies every negation, the disjunction is true, and
                # setvar fires 100. The item scores full marks for essentially
                # any submission. Every other rule here is invariant under that
                # flip: keys_of() strips <not> and reads positives, the negation
                # check still finds each choice inside a <not>, the distractor
                # count and original_answer_ids are untouched. Same class as the
                # wrong-respident <not> in BF-2026-043 -- a scoring block that
                # looks right and enforces nothing (BF-2026-050).
                for cv in re.findall(r'<conditionvar>(.*?)</conditionvar>', body, re.S):
                    if re.search(r'<or\b', cv) or len(re.findall(r'<and\b', cv)) != 1:
                        fails.append(f'{where}: conditionvar is not a single '
                                     f'<and> -- an empty or partial selection '
                                     f'can score 100')

                # Scoring must only reference choices that exist.
                for k in keys:
                    if k not in choice_idents:
                        fails.append(f'{where}: key {k} is not a choice')

                # Every non-keyed choice must actually be NEGATED, using the
                # item's own respident. A <not> naming the wrong respident
                # negates nothing: the choice becomes optional and a student
                # who selects it still scores 100. Nothing else here catches
                # that -- keys_of() strips <not> blocks and only reads
                # positives -- and a real bug shipped through the gap
                # (BF-2026-043).
                negated = set(re.findall(
                    r'<not>\s*<varequal respident="%s"[^>]*>([^<]*)</varequal>\s*</not>'
                    % re.escape(respident_of(body) or ''), body))
                for c in choice_idents:
                    if c not in keys and c not in negated:
                        fails.append(f'{where}: choice {c} is neither keyed '
                                     f'nor negated under the declared respident'
                                     f' -- selecting it would still score 100')

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
    for i, files in sorted(seen_idents.items()):
        if len(files) > 1:
            fails.append(f'duplicate <item ident="{i}"> in {files} -- Canvas '
                         f'keys questions by ident, so one silently replaces '
                         f'the other')

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
