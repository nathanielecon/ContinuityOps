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
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

# resp_numeric emits <and><vargte>V</vargte><varlte>V</varlte></and> -- "x >= V
# and x <= V", i.e. exactly x = V, written as a degenerate closed interval so
# that 7.00 matches a key of 7. Three rounds asserted PREDICATES over that
# structure -- the connective joining the pair (BF-2026-058), the top node
# (BF-2026-059), the pair's existence (BF-2026-061) -- and not one of them ever
# read a bound's VALUE. This gate had no notion of a number at all: it never
# imported Decimal and every numeric rule in it was a census of tags or strings.
# The invariant is arithmetic, so it needs arithmetic (BF-2026-062).
RANGE_AND = re.compile(
    r'<and>\s*<vargte\b[^>]*>([^<]*)</vargte>\s*'
    r'<varlte\b[^>]*>([^<]*)</varlte>\s*</and>')
CMP_OP = re.compile(r'<var(?:gte|lte|gt|lt)\b')


def dec(s):
    """The value as a NUMBER, or None if it is not one."""
    try:
        return Decimal(s.strip())
    except (InvalidOperation, ValueError):
        return None

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
    # Attribute ORDER is not part of the contract and neither is the response
    # element's flavour. The old form demanded `ident` be the first attribute of
    # a response_lid/response_str, so swapping two attributes returned None and
    # switched off every rule built on this. The caller now asserts a non-None
    # result, which is the load-bearing half; widening here removes the most
    # likely cause rather than only reporting it (BF-2026-061).
    m = re.search(r'<response_(?:lid|str|num|xy|grp)\b[^>]*?\bident="([^"]*)"',
                  body)
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


def check_line_endings(work, base):
    """BF-029, over EVERY file rather than the item XMLs alone.

    This lived inside the item loop, which skips `imsmanifest.xml` and
    `assessment_meta.xml` -- so it compared 14 of the 42 XML files and 2 of the
    6 CRLF files. BF-029's own damage was `finalize.py` rewriting whole files in
    the 6th-grade packages, which is precisely these, and the guarantee it
    protects -- an untouched file stays byte-identical, so a reviewer can trust
    the diff -- was unenforced for two thirds of them (BF-2026-057).
    """
    for f in sorted(glob.glob(os.path.join(work, '**', '*'), recursive=True)):
        if not os.path.isfile(f):
            continue
        rel = os.path.relpath(f, work)
        b = os.path.join(base, rel)
        if not os.path.exists(b):
            continue
        bb, wb = open(b, 'rb').read(), open(f, 'rb').read()
        if (b'\r\n' in bb) != (b'\r\n' in wb):
            fails.append(f'{rel}: line-ending convention changed')
        if b'\r\n' in wb and wb.count(b'\r\n') != wb.count(b'\n'):
            fails.append(f'{rel}: mixed line endings')


def check(work, base=None):
    for f in sorted(glob.glob(os.path.join(work, '*/*/*.xml'))):
        # basename, not the whole path: a work tree under a directory
        # named `metadata` or `manifests` matched every file and
        # checked zero items while still printing 'all checks pass'.
        if 'manifest' in os.path.basename(f) or 'meta' in os.path.basename(f):
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
            # A NINE-TAG ENUMERATION, where the failure message states the
            # general property. <sup> was the live gap: this is a mathematics
            # corpus, and an unescaped 5<sup>2</sup> becomes a child element,
            # so Canvas takes the node's text and the stem ships as "52" --
            # the exact mechanism that ate the word NOT in BF-2026-047. Match
            # any tag; every < that is genuinely text here is escaped, and
            # this pattern finds zero hits across all 458 bodies
            # (BF-2026-055).
            stray = re.findall(r'</?[a-zA-Z][a-zA-Z0-9]*\b[^>]*>', mt)
            if stray:
                fails.append(f'{rel}: raw HTML {stray[0]!r} inside <mattext> -- '
                             f'must be escaped; Canvas drops it silently')

        try:
            ET.fromstring(raw.encode('utf-8'))
        except Exception as e:
            fails.append(f'{rel}: does not parse: {e}')
            continue

        # Since BF-2026-050 the pristine tree is used for what it was always
        # there for: proving no key silently moved. The line-ending comparison
        # moved OUT of this loop -- see check_line_endings -- because this loop
        # skips every manifest and assessment_meta, which are exactly the files
        # BF-029 damaged (BF-2026-057).
        if base:
            b = os.path.join(base, rel)
            if os.path.exists(b):
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
            # Widened twice. `Part\s+[AB]\s*:` missed prose references; then
            # `\bPart\s+[AB1-9]\b` still missed lowercase `part 1`, `Part C`,
            # `Part 10` and `Part II`. Lowercase is the live risk, because the
            # retired boilerplate this replaced was prose and prose lowercases.
            # The letter class stays uppercase-only so ordinary English -- "part
            # a whole" -- does not false-positive (BF-2026-054).
            # Widened four times. Still missed PART A, `Parts 1 and 2`,
            # `In parts A and B`, `part b`, `Part iii` -- and the plural form
            # also slipped past the retired-boilerplate rule below, so the
            # exact sentence could return as `Parts 1 and 2 both must be
            # correct`. The only false positive the earlier narrowing was
            # actually protecting against is prose like "part a whole", so
            # that one string is carved out and nothing else (BF-2026-055).
            # Three bugs at once. re.search took only the FIRST match, so
            # benign prose ('part a whole') shadowed a real label later in
            # the same stem. The plural `s?` was a literal lowercase s, so
            # `PARTS 1` never matched. And it scanned the stem only -- while
            # the historical defect lived in CHOICE text ('Part A: -15'),
            # which is what the split was performed to remove, so the rule
            # could not detect a regression to the state it exists to
            # prevent (BF-2026-056).
            for mt in re.findall(r'<mattext[^>]*>(.*?)</mattext>', body, re.S):
                for m_pl in re.finditer(
                        r'\b[Pp][Aa][Rr][Tt][Ss]?\s+(?:[A-Za-z]|[0-9]+|[IVXivx]+)\b',
                        plain(mt)):
                    if m_pl.group(0) != 'part a':
                        fails.append(f'{where}: references a part label '
                                     f'({m_pl.group(0)!r})')

            # The retired boilerplate must be gone everywhere.
            if 'Part 1 and Part 2 both must be correct' in stem:
                fails.append(f'{where}: retired Part 1/Part 2 sentence present')

            keys = keys_of(body)
            # The <not> rule in the fill-in branch names "an empty box scores
            # 100" as the harm it prevents, and guards only the node that
            # produces that harm by NEGATION. An empty <varequal></varequal>
            # produces it directly: Canvas trims the submission before
            # comparing, so a blank entry equals the empty accepted string, the
            # arm fires and SCORE is Set to 100. keys_of()'s ([^<]*) matches
            # the empty string happily and every rule downstream then treats it
            # as a legitimate accepted value -- `if not keys` sees a non-empty
            # set, `numericish` is undisturbed because "" holds no letter, and
            # check_keys_vs_base is a SUBSET test so an ADDED value is
            # invisible to it by design. On a select-all the key `''` would be
            # caught by `k not in choice_idents`; the hole is therefore exactly
            # on the 143 fill-ins (BF-2026-061).
            if any(not k.strip() for k in keys):
                fails.append(f'{where}: an empty <varequal> is accepted -- a '
                             f'blank submission scores 100')
            idents = LABEL.findall(body)
            choice_idents = [i for i in idents if i != 'answer1']

            # Sign guidance applies to EVERY fill-in, not just numeric entry --
            # F4 asks for "the sign convention if the answer can be negative" of
            # any item where the student types the answer. Three short-answer
            # items ship negative keys and none was examined (BF-2026-054).
            #
            # Two guards, both load-bearing. `numericish` excludes word answers
            # where a minus is only an alias spelling (F3 accepts `-8` beside
            # "subtract 8"), which would otherwise false-positive. And a worked
            # example counts as guidance: the ordering items say "Type it like
            # -5,0,2" and the topic-1-4 items say "write |4-(-9)|", which tell a
            # student what to type more concretely than the sentence does.
            if qt in ('numerical_question', 'short_answer_question'):
                numericish = keys and not any(re.search(r'[A-Za-z]', v) for v in keys)
                if (numericish
                        and any(re.search(r'(^|[\s(,])[-−]\d', v) for v in keys)
                        and not re.search(r'negative sign|minus sign'
                                          r'|(?:type it like|write)[^.]*[-−]\d',
                                          stem, re.I)):
                    fails.append(f'{where}: negative key, no sign guidance')

            if qt == 'numerical_question':
                if not keys:
                    fails.append(f'{where}: numeric item has no accepted value')
                # The respcondition-count rule is scoped to choice-bearing
                # items on purpose: the rubric permits a fill-in a second arm
                # as a trailing-zero or equivalent-form alternate. Nothing then
                # checked that a second arm IS an equivalent form. Copy an
                # item's arm and change 0 to 77 and the gate passes: keys_of()
                # unions across conditionvars so 77 just becomes a key, the
                # setvar/decvar/connective rules all pass on a faithful copy,
                # and check_keys_vs_base is a SUBSET test by explicit design so
                # an ADDED value is invisible to it in principle. An
                # execution-based auditor cannot see this either -- it derives
                # the accepted set FROM the artifact, so 77 is accepted and 77
                # does score 100. Only knowing the semantic invariant catches
                # it, and a NUMBER is comparable where a spelling is not: the
                # corpus's six two-arm items are 3.6/3.60, 7/7.00, 220.8/220.80,
                # 21.1/21.10, 6.3/6.30, 9/9.00, and two more are a value with
                # its 2-dp half-up rounding (0.375/0.38, 0.625/0.63). All
                # collapse to one number under that quantisation. {0, 77} does
                # not (BF-2026-062).
                q, bad_v = set(), []
                for v in keys:
                    d = dec(v)
                    if d is None:
                        bad_v.append(v)
                    else:
                        q.add(d.quantize(Decimal('0.01'),
                                         rounding=ROUND_HALF_UP))
                for v in bad_v:
                    fails.append(f'{where}: accepted value {v!r} is not a '
                                 f'number on a numerical_question')
                if len(q) > 1:
                    fails.append(f'{where}: accepts {sorted(keys)} -- these '
                                 f'are different numbers; an extra arm is '
                                 f'legitimate only as an equivalent spelling '
                                 f'(3.6 / 3.60) or the 2-dp rounding of the '
                                 f'same value (0.375 / 0.38)')

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
            # An ABSENT setvar is worse than one holding 0, and the loop
            # could not see it: with no <setvar> the body never ran.
            # Deleting every setvar corpus-wide passed. <decvar> still
            # declares SCORE, so it sits at minvalue 0 and every correct
            # student is marked wrong on every item. Same class as
            # BF-2026-050's `if dv and ...`, one element over (BF-2026-056).
            # <other/> is QTI's "everything else" condition. One awarding 100
            # makes EVERY submission score full marks, and nothing looked for
            # it. No generator emits it, so a judge correctly declined to score
            # this -- but it is the same "scores 100 for anything" shape as the
            # empty-key and tautological-range defects, and the guard is free
            # (BF-2026-059).
            for rc_ in re.findall(r'<respcondition\b.*?</respcondition>', body, re.S):
                if '<other' in rc_ and '<setvar' in rc_:
                    fails.append(f'{where}: an <other/> respcondition awards a '
                                 f'score -- every submission would match it')
            svs = re.findall(r'<setvar([^>]*)>([^<]*)</setvar>', body)
            if not svs:
                fails.append(f'{where}: no <setvar> -- SCORE is never '
                             f'written, so it stays at minvalue 0')
            # ...and PER RESPCONDITION, not once per item. The value, action
            # and varname clauses below already iterate every setvar; only the
            # EXISTENCE clause was written against the item as a whole. Six
            # items ship two respconditions -- D3, D4 and M3-M6, each pairing
            # an exact-string condition with a numeric range -- so deleting the
            # setvar from one of the two leaves `svs` non-empty and the item
            # passes, while a student who satisfies that arm (typing `7.00`
            # against a key of `7`) scores 0. The same "asserted once, needed
            # at every site" shape as BF-2026-050 and -053 (BF-2026-060).
            for rc_ in re.findall(r'<respcondition\b.*?</respcondition>',
                                  body, re.S):
                if '<setvar' not in rc_:
                    fails.append(f'{where}: a <respcondition> writes no '
                                 f'<setvar> -- a student who satisfies it '
                                 f'scores 0')
            for attrs, value in svs:
                # The THIRD instalment of this rule. BF-2026-047 checked the
                # value, BF-2026-051 added the variable and called it "closed
                # halfway", and the action -- the operator applied to the value
                # -- stayed unread. decvar sets minvalue="0", so SCORE starts at
                # 0: action="Multiply" gives 0x100 = 0, "Divide" gives 0, and
                # "Subtract" gives -100. Each passed corpus-wide while the
                # message claimed a correct answer scores 100 (BF-2026-057).
                if 'action="Set"' not in attrs:
                    fails.append(f'{where}: setvar {attrs.strip()!r} is not '
                                 f'action="Set" -- SCORE starts at minvalue 0, '
                                 f'so any other action leaves it below 100')
                if 'varname="SCORE"' not in attrs:
                    fails.append(f'{where}: setvar writes {attrs.strip()!r}, '
                                 f'not SCORE -- SCORE is never set, so it stays 0')
                if value.strip() != '100':
                    fails.append(f'{where}: a correct answer scores '
                                 f'{value.strip()}, not 100')
            # `if dv and ...` skipped the whole check when <decvar> was ABSENT,
            # which is the worse case: <setvar varname="SCORE"> then writes an
            # outcome nothing declares. And minvalue was never read at all, so
            # minvalue="100" -- every wrong answer scoring full marks -- passed
            # silently (BF-2026-050).
            # re.search returns the FIRST match. This rule's message is a
            # claim about *the* decvar, asserted against one of however many
            # exist, so an item whose scoring declaration contradicts itself
            # ships certified unambiguous. QTI 1.2 does not define a duplicate
            # <decvar> for one variable, so which one Canvas honours cannot be
            # settled from here -- and that ambiguity IS the defect: if it takes
            # the last, a second declaration at maxvalue="0" caps the outcome
            # and every correct student scores 0. Assert the cardinality first,
            # then check every occurrence. Same treatment for the two other
            # metadata rules that read the first match (BF-2026-062).
            dvs = re.findall(r'<decvar([^>]*)>', body)
            if len(dvs) != 1:
                fails.append(f'{where}: {len(dvs)} <decvar> declarations -- '
                             f'SCORE is declared '
                             f'{"more than once" if dvs else "never"}, so '
                             f'which bounds apply is undefined')
            for a in dvs:
                if ('maxvalue="100"' not in a or 'minvalue="0"' not in a
                        or 'varname="SCORE"' not in a):
                    fails.append(f'{where}: decvar is not '
                                 f'maxvalue=100 minvalue=0 varname=SCORE')

            # Package totals compared the meta value to the item COUNT, which
            # assumes every item is worth 1 without ever checking it. An item at
            # 0 points is unscorable, and two compensating errors (0 and 2)
            # leave the package total correct.
            pps = re.findall(r'<fieldlabel>points_possible</fieldlabel>\s*'
                             r'<fieldentry>([\d.]+)</fieldentry>', body)
            if len(pps) != 1:
                fails.append(f'{where}: {len(pps)} points_possible fields -- '
                             f'which one Canvas reads is undefined')
            for v in pps:
                if float(v) != 1.0:
                    fails.append(f'{where}: points_possible is {v}, not 1')
            if not pps:
                fails.append(f'{where}: points_possible is absent, not 1')

            # Criterion 7 requires referenced images to RESOLVE and to use
            # Canvas's $IMS-CC-FILEBASE$ form, calling a plain src="media/..."
            # import-blocking wherever the image IS the question. Neither tool
            # checked either half: pointing an <img> at a filename present in no
            # mirror passed, and so did dropping the token. repackage.py walks
            # manifest->file and file->manifest, but never item-XML->file
            # (BF-2026-055).
            for src in re.findall(r'<img[^>]*src="([^"]*)"', html.unescape(body)):
                m_fb = re.fullmatch(r'\$IMS-CC-FILEBASE\$/media/(.+)', src)
                if not m_fb:
                    fails.append(f'{where}: <img src={src!r}> is not '
                                 f'$IMS-CC-FILEBASE$/media/... -- import-blocking')
                    continue
                pkgdir = os.path.join(work, rel.split(os.sep)[0])
                hits = glob.glob(os.path.join(pkgdir, '**', 'media', m_fb.group(1)),
                                 recursive=True)
                if not hits:
                    fails.append(f'{where}: <img> target {m_fb.group(1)!r} exists '
                                 f'in no media directory of this package')

            # --- ITEM SCOPE, and that is the whole point -------------------
            # These three were written for every item and then indented inside
            # the select-all branch, so they ran on 34 of 177 and the other 143
            # -- the larger population -- went unchecked. Twice now a rule of
            # mine has been logged as closed while covering only select-all
            # (BF-2026-051 rule 3 was the same mistake). Scope is the bug that
            # keeps recurring, so these sit here deliberately (BF-2026-053).
            want = respident_of(body)
            # A GUARD, NEVER ASSERTED -- the BF-2026-050 shape one element out.
            # That entry's lesson was "`if dv and ...` skipped the whole check
            # when <decvar> was ABSENT, which is the worse case"; it was applied
            # to decvar and not here, and then BF-2026-060 layered its
            # respident-presence fix INSIDE this unfixed guard. respident_of is
            # one regex requiring ident to be the first attribute of a
            # response_lid/response_str, so reordering two attributes returns
            # None and BOTH respident rules evaporate together. On a select-all
            # the choice-negation loop below fails closed by accident (it uses
            # `respident_of(body) or ''`, matches nothing and reports every
            # distractor un-negated); on a FILL-IN nothing else reads a
            # respident at all, so scoring goes wholly unchecked on 143 of the
            # 177 items -- and an operator naming no live response never fires,
            # so a correct student scores 0 (BF-2026-061).
            if not want:
                fails.append(f'{where}: no <response_lid>/<response_str> '
                             f'declaring a respident this gate can read -- '
                             f'every respident rule below is skipped, so the '
                             f'item\'s scoring goes unchecked')
            if want:
                # Comparison operators too: a numeric item scores through
                # vargte/varlte, so checking only varequal leaves the range
                # conditions unexamined.
                bad = set(re.findall(
                    r'<var(?:equal|gte|lte|lt|gt)\b[^>]*?\brespident="([^"]*)"', body)) - {want}
                if bad:
                    fails.append(f'{where}: scoring uses respident {sorted(bad)} '
                                 f'but the item declares "{want}" -- those '
                                 f'conditions match nothing, so SCORE stays 0')
                # IDENTITY was checked; PRESENCE was not. The rule above reads
                # respident out of the operator and compares it, so an operator
                # carrying no respident at all contributes nothing to `bad` and
                # is invisible to it -- the mismatch it exists to catch is the
                # louder half of the same defect. Only the negated side was
                # covered, by the choice-negation rule further down, which
                # requires each <not><varequal> to name the declared respident;
                # the positive operators that actually award the score had no
                # such check. An operator that names no response matches
                # nothing, so the arm never fires and SCORE stays 0
                # (BF-2026-060).
                for op_ in re.findall(
                        r'<var(?:equal|gte|lte|lt|gt)\b[^>]*>', body):
                    if not re.search(r'\brespident="', op_):
                        fails.append(f'{where}: scoring operator {op_!r} '
                                     f'declares no respident -- it names no '
                                     f'response, so the condition matches '
                                     f'nothing')

            # multiple_choice_question is NOT select-all. Criterion 6's
            # amendment specifies exactly one keyed choice,
            # rcardinality="Single", no <not> blocks -- the opposite of
            # what routing it through the select-all branch demanded. The
            # type is unexercised (0 of 177), so nothing ships wrong, but
            # the gate encoded the inverse of the rubric for a shape the
            # rubric keeps ready on purpose (BF-2026-055).
            if qt == 'multiple_answers_question':
                if 'rcardinality="Multiple"' not in body:
                    fails.append(f'{where}: select-all is not '
                                 f'rcardinality="Multiple" -- unscoreable')
            elif qt == 'multiple_choice_question':
                if 'rcardinality="Single"' not in body:
                    fails.append(f'{where}: multiple choice is not '
                                 f'rcardinality="Single"')
                if '<not>' in body:
                    fails.append(f'{where}: multiple choice carries a '
                                 f'<not> block')
                if len(keys) != 1:
                    fails.append(f'{where}: multiple choice has '
                                 f'{len(keys)} keys, expected exactly 1')
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
                    # The MIRROR of the select-all <and>-to-<or> flip, which
                    # the comment above names and then did not check. Turning
                    # a fill-in's <or> into <and> means no single typed string
                    # can satisfy it, the respcondition never fires, and every
                    # student scores 0. 24 items hold more than one accepted
                    # value; the corpus-wide flip passed (BF-2026-056).
                    if (len(re.findall(r'<varequal', cv)) > 1
                            and not re.match(r'\s*<or\b', cv)):
                        fails.append(f'{where}: fill-in conditionvar has '
                                     f'multiple accepted values but is not a '
                                     f'top-level <or> -- no single entry can '
                                     f'satisfy it, so everyone scores 0')
                    # The select-all rule this mirrors asserts the whole tree
                    # shape; this one asserted only the identity of the TOP node,
                    # and only under a guard that excluded 125 of 149 fill-in
                    # conditionvars. Every numeric item nests
                    # <and><vargte>V</vargte><varlte>V</varlte></and> inside the
                    # top-level <or>; flip that inner <and> to <or> and
                    # "x >= V or x <= V" is a tautology over the reals, so EVERY
                    # entry scores 100 and the item tests nothing. Emitted as an
                    # f-string from two generators, guarded at neither
                    # (BF-2026-058).
                    for conn, inner in re.findall(
                            r'<(and|or)>((?:(?!</?(?:and|or)\b).)*?)</\1>', cv, re.S):
                        if (conn != 'and' and re.search(r'<vargte\b', inner)
                                and re.search(r'<varlte\b', inner)):
                            fails.append(f'{where}: a vargte/varlte range pair '
                                         f'is joined by <{conn}> -- "x >= V or '
                                         f'x <= V" is true for every number, so '
                                         f'any entry scores 100')
                    # ...and the TOP node too, not only the inner pair. Flipping
                    # the outer <or> to <and> requires the entry to satisfy both
                    # the exact string and the range, so "7.00" against a key of
                    # "7" is rejected -- a correct student marked wrong. The
                    # lesson from the inner case was "assert the tree, not the
                    # top"; the converse needed saying too (BF-2026-059).
                    if (re.search(r'<vargte\b', cv) and re.search(r'<varequal\b', cv)
                            and not re.match(r'\s*<or\b', cv)):
                        fails.append(f'{where}: conditionvar joins the exact '
                                     f'value and the range with <and> -- an '
                                     f'equivalent spelling would be rejected')
                    # ...and that the PAIR EXISTS. The rule above asserts the
                    # connective joining two bounds and is vacuous when only one
                    # is present. resp_numeric emits <and><vargte>V</vargte>
                    # <varlte>V</varlte></and>, which is "x >= V and x <= V" --
                    # exactly x = V, written as a degenerate closed interval so
                    # that 7.00 matches a key of 7. Drop either bound and what
                    # is left is a half-line: against a key of 3.6, "x >= 3.6"
                    # scores 100 for 4, for 100, for 999999. The item stops
                    # testing the answer and starts testing whether the student
                    # typed a big enough number. Same family as BF-2026-058's
                    # tautology -- there the condition was true over all of the
                    # reals, here over half of them. Half a tautology is still
                    # not a test (BF-2026-061).
                    # The FOURTH instalment, and the first to read a value.
                    # Four malformations survive a balanced tag census, all
                    # injected and all passing the previous gate:
                    #   [0, 1000000]   -- a live interval; a million wrong
                    #                     answers score 100.
                    #   <and><vargte>V</vargte></and><and><varlte>V</varlte></and>
                    #                  -- counts balanced, bounds in SEPARATE
                    #                     disjuncts of the top <or>, so the
                    #                     semantics is "x >= V or x <= V",
                    #                     true for every real. Verbatim the
                    #                     BF-2026-058 tautology, reached with
                    #                     that rule's predicate satisfied.
                    #   [9.9, 9.9] on a key of 3.6 -- degenerate, well-formed,
                    #                     and awards 100 for a wrong number.
                    #   <vargt>/<varlt> -- strict, so the census reads 0 == 0
                    #                     while "x > V and x < V" is EMPTY. The
                    #                     exact arm is a STRING compare under
                    #                     case="No", so "3.60" != "3.6": kill
                    #                     the range and the trailing-zero
                    #                     spelling the two-arm design exists to
                    #                     accept is marked wrong. F5's worst
                    #                     shape -- the failure lands on the
                    #                     student who followed the instruction.
                    exact = {dec(v) for v in re.findall(
                        r'<varequal[^>]*>([^<]*)</varequal>', cv)} - {None}
                    pairs = RANGE_AND.findall(cv)
                    if len(CMP_OP.findall(cv)) != 2 * len(pairs):
                        fails.append(f'{where}: a comparison operator sits '
                                     f'outside an <and><vargte>V</vargte>'
                                     f'<varlte>V</varlte></and> pair -- a lone '
                                     f'bound is a half-line, and two bounds in '
                                     f'separate disjuncts are "x >= V or '
                                     f'x <= V", true for every number')
                    for lo, hi in pairs:
                        dlo, dhi = dec(lo), dec(hi)
                        if dlo is None or dhi is None or dlo != dhi:
                            fails.append(f'{where}: range bounds [{lo}, {hi}] '
                                         f'are not one point -- every value in '
                                         f'the interval scores 100')
                        elif exact and dlo not in exact:
                            fails.append(f'{where}: the range arm awards 100 '
                                         f'for {lo}, which no <varequal> in '
                                         f'this conditionvar accepts')
                    if '<not>' in cv:
                        fails.append(f'{where}: <not> inside a fill-in '
                                     f'conditionvar -- any non-matching entry, '
                                     f'including an empty box, scores 100')

            # ITEM SCOPE, which nothing held. The connective rule below asserts
            # "an empty or partial selection cannot score 100" and enforces it
            # per <conditionvar>; append a SECOND <respcondition> and every
            # conditionvar is still a single <and>, so the rule is satisfied at
            # every site it inspects while the property its own message names is
            # false at the item. Criterion 6 states it outright for Shape A --
            # "exactly one <respcondition>" -- and no rule counted them. The two
            # loops that do iterate respconditions (the <other/> guard and
            # BF-2026-060's setvar clause) each ask a question ABOUT a block and
            # neither asks how many blocks there are.
            #   Worked: append to a one-key select-all an arm whose conditionvar
            # is <and><not><varequal>KEY</varequal></not></and>. A student who
            # ticks nothing satisfies the negation, the arm fires, SCORE is Set
            # to 100. keys_of() strips <not> subtrees, so the key set is
            # unchanged and MIN_DISTRACTORS, the contiguous-run test and
            # check_keys_vs_base are all invariant. Every rule passes.
            # Restricted to choice-bearing items deliberately: the rubric's
            # second-arm carve-out is justified by equivalent-form alternates
            # (3.6 / 3.60), which exist only for a TYPED value. A select-all
            # answer is a set of idents, so a second arm necessarily awards 100
            # for a different set (BF-2026-061).
            if qt in ('multiple_answers_question', 'multiple_choice_question'):
                rcs = re.findall(r'<respcondition\b.*?</respcondition>',
                                 body, re.S)
                if len(rcs) != 1:
                    fails.append(f'{where}: {len(rcs)} <respcondition> blocks '
                                 f'-- an all-or-nothing item scores through '
                                 f'exactly one arm; a second arm awards 100 '
                                 f'for a selection the first one rejects')

            if qt == 'multiple_answers_question':
                # Every other autoscored type has a minimum-key rule -- numeric
                # and short answer fail on `not keys`, multiple choice on
                # `!= 1` -- and the one type scored by CONJUNCTION had none.
                # With zero positives the conditionvar is a pure conjunction of
                # negations, which a student who selects NOTHING satisfies in
                # every conjunct: setvar fires 100 on an empty submission and
                # the student who picks the right choice scores 0. Every other
                # select-all rule is invariant under it (BF-2026-058).
                if not keys:
                    fails.append(f'{where}: select-all has no keyed choice -- '
                                 f'the conditionvar is a conjunction of '
                                 f'negations, so an empty submission satisfies '
                                 f'every one and scores 100')
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


                # Every non-keyed choice must actually be NEGATED, using the
                # item's own respident. A <not> naming the wrong respident
                # negates nothing: the choice becomes optional and a student
                # who selects it still scores 100. Nothing else here catches
                # that -- keys_of() strips <not> blocks and only reads
                # positives -- and a real bug shipped through the gap
                # (BF-2026-043).
                negated = set(re.findall(
                    # respident anywhere in the tag -- BF-2026-056 fixed this at
                    # the mismatch rule and not here, so the two adjacent rules
                    # disagreed about what a respident attribute is. With
                    # case="No" written first (the majority spelling on positive
                    # varequals) this reported every correct distractor as
                    # un-negated: a false accusation, failing closed but untrue
                    # (BF-2026-057).
                    r'<not>\s*<varequal\b[^>]*?\brespident="%s"[^>]*>([^<]*)</varequal>\s*</not>'
                    % re.escape(respident_of(body) or ''), body))
                # "Negated" was implemented as "appears inside at least one
                # <not>", with no regard for how many <not> ancestors the node
                # has. Wrap an existing <not><varequal>WRONG</varequal></not>
                # in a second <not> and the choice becomes REQUIRED, because
                # not(not X) = X -- yet keys_of() strips <not>...</not>
                # non-greedily so the outer swallows the inner and the key set
                # is UNCHANGED, which leaves MIN_DISTRACTORS, the
                # contiguous-run test, original_answer_ids and
                # check_keys_vs_base all invariant; and this rule matches the
                # INNER node and files the choice as negated. A student who
                # reasons correctly, ticks the key and leaves the distractor
                # alone, scores 0. Assert the tree rather than the connective:
                # the scoring <and> may hold nothing but bare <varequal> and
                # single-depth <not><varequal></not> nodes. The inner
                # substitution must run FIRST, or stripping bare <varequal>
                # leaves a bare <not></not> and false-positives on the clean
                # corpus (BF-2026-062).
                shape = re.search(
                    r'<conditionvar>\s*<and>(.*?)</and>\s*</conditionvar>',
                    body, re.S)
                if shape:
                    residue = re.sub(
                        r'<varequal\b[^>]*>[^<]*</varequal>', '',
                        re.sub(r'<not>\s*<varequal\b[^>]*>[^<]*</varequal>'
                               r'\s*</not>', '', shape.group(1)))
                    if residue.strip():
                        fails.append(f'{where}: the scoring <and> holds more '
                                     f'than bare <varequal> and single '
                                     f'<not><varequal></not> nodes -- nesting '
                                     f'silently changes which choices are '
                                     f'required ({residue.strip()[:60]!r})')
                for c in choice_idents:
                    if c not in keys and c not in negated:
                        fails.append(f'{where}: choice {c} is neither keyed '
                                     f'nor negated under the declared respident'
                                     f' -- selecting it would still score 100')

            # These three apply to ANY choice-bearing item, and all three sat
            # inside the multiple_answers branch -- so multiple_choice_question,
            # which the rubric keeps ready, could name a non-existent key, put
            # its key at position 0, and repeat a choice's visible text, all
            # unchecked. The duplicate-text comment even said "a defect in every
            # shape" from inside a branch that reached one (BF-2026-056).
            # `if choice_idents:` is "has choices", not "is choice-bearing" --
            # so a select-all with its <render_choice> emptied passed: an
            # unanswerable item whose original_answer_ids still names eight
            # idents that no longer exist. Ten split halves passed
            # unconditionally, since MIN_DISTRACTORS is the only rule that
            # notices n == 0 and SPLIT_HALF exempts exactly them (BF-2026-057).
            if qt in ('multiple_answers_question', 'multiple_choice_question'):
                if not choice_idents:
                    fails.append(f'{where}: choice-bearing item has no '
                                 f'<response_label> -- unanswerable')
                for k in keys:
                    if k not in choice_idents:
                        fails.append(f'{where}: key {k} is not a choice')
                # BF-031 -- no key may sit at position 0.
                if choice_idents and choice_idents[0] in keys:
                    fails.append(f'{where}: keyed choice is first (BF-031)')
                texts = [plain(t) for t in re.findall(
                    r'<response_label[^>]*>\s*<material>\s*'
                    r'<mattext[^>]*>(.*?)</mattext>', body, re.S)]
                if len(set(texts)) != len(texts):
                    fails.append(f'{where}: two choices share visible text')
                # The FOURTH sibling, left behind when BF-2026-056 hoisted the
                # other three out of the multiple_answers branch. Same rule,
                # same reason, same hole: a multiple_choice_question could
                # repeat a choice ident, and a repeated ident means the two
                # <response_label>s are indistinguishable to scoring -- a
                # <varequal> on it matches whichever Canvas resolves first, so
                # selecting the other one is unscoreable. Hoisting three of
                # four is how this class of defect keeps surviving its own fix
                # (BF-2026-060).
                if len(set(choice_idents)) != len(choice_idents):
                    fails.append(f'{where}: duplicate choice ident')

            # original_answer_ids must be a permutation of the real choices.
            oais = re.findall(r'<fieldlabel>original_answer_ids</fieldlabel>'
                              r'\s*<fieldentry>([^<]*)</fieldentry>', body)
            if len(oais) > 1:
                fails.append(f'{where}: {len(oais)} original_answer_ids fields '
                             f'-- which one Canvas reads is undefined')
            oai = re.search(r'<fieldlabel>original_answer_ids</fieldlabel>\s*'
                            r'<fieldentry>([^<]*)</fieldentry>', body)
            # `if oai and choice_idents` made this inert on all 143 fill-in
            # items: choice_idents excludes the `answer1` label, so it is empty
            # for them and the branch never ran. Rewriting a fill-in's
            # original_answer_ids to anything at all passed (BF-2026-054).
            listed = [x for x in oai.group(1).split(',') if x] if oai else None
            if not oai:
                fails.append(f'{where}: original_answer_ids absent')
            elif qt in ('multiple_answers_question', 'multiple_choice_question'):
                if sorted(listed) != sorted(choice_idents):
                    fails.append(f'{where}: original_answer_ids does not match '
                                 f'the choice list')
            elif qt in ('numerical_question', 'short_answer_question'):
                # Canvas's own export convention, uniform on all 94 fill-ins in
                # the pristine tree: a single `choice_1` against the `answer1`
                # render label. Not a permutation candidate, but it still has a
                # right value and nothing was checking it.
                if listed != ['choice_1']:
                    fails.append(f'{where}: fill-in original_answer_ids is '
                                 f"{listed!r}, not the convention ['choice_1']")

    # points_possible must equal the item count on every package.
    for d in sorted(glob.glob(os.path.join(work, '*/'))):
        # basename, not the whole path -- the SAME predicate as line ~201 and
        # the same bug, left behind when that one was fixed. With any ancestor
        # directory containing "meta" or "manifest", xs was empty for every
        # package, the loop `continue`d on all 14, and BOTH rules under it went
        # silent while the census still printed 177 TOTAL. build.sh builds in
        # `mktemp -d`, so which rules ran was not deterministic across builds
        # (BF-2026-059).
        xs = [x for x in glob.glob(d + '*/*.xml')
              if 'manifest' not in os.path.basename(x)
              and 'meta' not in os.path.basename(x)]
        meta = glob.glob(d + '*/assessment_meta.xml')
        if not xs or not meta:
            continue
        _raw = open(xs[0], encoding='utf-8', newline='').read()
        # `<item ident=` was the prefix BOTH counts shared, so rewriting a tag
        # as `<item title="..." ident="...">` hid the item from the raw count
        # AND from ITEM.findall(), leaving the difference at 0 and the
        # reconciliation unable to fire. `\b` does not match <itemmetadata> or
        # <itemfeedback> (BF-2026-062).
        n = len(re.findall(r'<item\b', _raw))
        # TWO NOTIONS OF "AN ITEM" live in this file, forty lines apart, and
        # nothing reconciles them. This raw count accepts any `<item ident=`;
        # ITEM.findall() up in the per-item loop demands ident-then-title,
        # single-spaced, with `>` immediately after. Their DIFFERENCE is exactly
        # the set of items that no per-item rule examines -- not one rule, all
        # of them: type, decvar, setvar, respident, connectives, negation,
        # points_possible, original_answer_ids, images, part labels -- while the
        # package total stays self-consistent and the census still prints a
        # plausible number. Add one attribute to an item tag and it becomes
        # invisible to the whole gate; set its SCORE to 0 in the same edit and a
        # student who answers correctly is told they are wrong, with `all checks
        # pass` printed over it. BF-2026-059 wrote the warning itself -- "the
        # item census still prints 177 TOTAL, so the tool looks healthy while a
        # whole rule is switched off" -- and the census stayed decoration
        # (BF-2026-061).
        if n != len(ITEM.findall(_raw)):
            fails.append(f'{os.path.basename(d.rstrip("/"))}: {n} `<item '
                         f'ident=` in the file but {len(ITEM.findall(_raw))} '
                         f'match the item pattern -- the difference is checked '
                         f'by no rule in this gate')
        m = open(meta[0], encoding='utf-8', newline='').read()
        # The loop could only compare values it FOUND, so a meta declaring no
        # points_possible at all passed. The item-level twin forty lines up
        # handles absence explicitly. Same rule, two sites, absence at one
        # (BF-2026-058).
        vs = set(re.findall(r'<points_possible>([\d.]+)</points_possible>', m))
        if not vs:
            fails.append(f'{os.path.basename(d.rstrip("/"))}: assessment_meta '
                         f'declares no points_possible at all')
        for v in vs:
            if abs(float(v) - n) > 1e-9:
                fails.append(f'{os.path.basename(d.rstrip("/"))}: '
                             f'points_possible {v} but {n} items')


def check_items_vs_base(work, base, expect_total=None):
    """No item may silently vanish, and the census must mean something.

    check_keys_vs_base does `if wbody is None: continue` -- a baseline item that
    is simply GONE from the build is skipped in silence. The only backstop was
    the package rule points_possible == item count, which stays self-consistent
    if the meta is edited in the same breath, so deleting an item and
    decrementing its meta passed. Meanwhile build.sh's own comment says the
    baseline is kept "so any item can be diffed against how it shipped", and it
    was consulted for line endings and key text and never for whether the item
    is still there.

    The test cannot be count equality -- splits are legitimate, and the baseline
    holds 157 items where the build holds 177. The real invariant is F7 ("every
    part of the original stem must survive into exactly one of the halves") and
    it is mechanical: every baseline item either survives by ident or becomes at
    least two lettered halves in the same package. The 18 that disappear are the
    split parents, each with its 1a/1b siblings present.

    And the census: BF-2026-059 wrote the warning itself -- "the item census
    still prints 177 TOTAL, so the tool looks healthy while a whole rule is
    switched off" -- and BF-2026-061 quoted that line back while closing a
    different hole. It is still printed and was still never asserted
    (BF-2026-062).
    """
    IDENT = re.compile(r'<item\b[^>]*\bident="([^"]*)"')
    total = 0
    for d in sorted(glob.glob(os.path.join(base, '*/'))):
        pkg = os.path.basename(d.rstrip('/'))
        pick = lambda g: [x for x in g
                          if 'manifest' not in os.path.basename(x)
                          and 'meta' not in os.path.basename(x)]
        bxs = pick(glob.glob(d + '*/*.xml'))
        wxs = pick(glob.glob(os.path.join(work, pkg, '*', '*.xml')))
        if not bxs:
            continue
        if not wxs:
            fails.append(f'{pkg}: shipped in the baseline and is absent from '
                         f'the build')
            continue
        wids = set(IDENT.findall(
            open(wxs[0], encoding='utf-8', newline='').read()))
        total += len(wids)
        for i in IDENT.findall(
                open(bxs[0], encoding='utf-8', newline='').read()):
            if i in wids:
                continue
            if len([x for x in wids
                    if re.fullmatch(re.escape(i) + r'[a-z]', x)]) < 2:
                fails.append(f'{pkg}: item {i!r} shipped in the baseline and '
                             f'is gone -- it neither survives by ident nor '
                             f'splits into halves (F7), so students lose the '
                             f'question and nothing else here notices')
    if expect_total is not None and total != expect_total:
        fails.append(f'corpus holds {total} items, expected {expect_total} -- '
                     f'the census has never been asserted against anything')


if __name__ == '__main__':
    _base = sys.argv[2] if len(sys.argv) > 2 else None
    if _base:
        check_line_endings(sys.argv[1], _base)
        check_items_vs_base(sys.argv[1], _base,
                            int(os.environ.get('QTI_EXPECT_ITEMS', 177)))
    check(sys.argv[1], _base)
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
