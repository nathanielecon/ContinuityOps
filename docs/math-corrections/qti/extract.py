import zipfile, glob, os, re, json, html, hashlib
import xml.etree.ElementTree as ET

SRC="/tmp/qtiwork/staged"
def strip(t):
    # Two traps, both hit this run:
    #  1. A bare '<' survives XML decoding in the STEMS (the source escapes the
    #     comparison operator one layer, so ElementTree hands back "\\(q < 0\\)").
    #     A greedy <[^>]+> tag-stripper eats from that '<' to the next '>',
    #     silently truncating the stem. Browsers do not: HTML5 only starts a tag
    #     when '<' is followed by an ASCII letter or '/'. Match that rule.
    #  2. The CHOICES escape it two layers, so unescaping must come AFTER tag
    #     removal or the recovered '<' is eaten by the same stripper.
    if t is None: return ""
    t = re.sub(r'</?[a-zA-Z][^>]*>', ' ', t)     # real tags only
    return re.sub(r'\s+', ' ', html.unescape(t)).strip()

def lt(e):  # localname-insensitive find-all
    return e.tag.split('}')[-1] if isinstance(e.tag,str) else ''

rows=[]
for z in sorted(glob.glob(f"{SRC}/*.zip")):
    pkg=os.path.basename(z)
    zf=zipfile.ZipFile(z)
    sha=hashlib.sha256(open(z,'rb').read()).hexdigest()[:12]
    axml=[n for n in zf.namelist() if n.endswith('.xml') and 'manifest' not in n and 'meta' not in n]
    if not axml: continue
    root=ET.fromstring(zf.read(axml[0]))
    for item in root.iter():
        if lt(item)!='item': continue
        title=item.get('title','')
        # stem: first mattext under presentation/material
        stem=""
        for m in item.iter():
            if lt(m)=='mattext': stem=strip(m.text); break
        # choices
        choices=[]
        for rl in item.iter():
            if lt(rl)!='response_label': continue
            txt=""
            for m in rl.iter():
                if lt(m)=='mattext': txt=strip(m.text); break
            choices.append({"ident":rl.get('ident',''),"text":txt})
        # scoring: walk respcondition tree properly (NOT flat regex - varequal
        # also appears inside <not>, which made every choice look correct)
        required, negated, nconds = [], [], 0
        for rc in item.iter():
            if lt(rc)!='respcondition': continue
            nconds+=1
            for child in rc.iter():
                if lt(child)=='not':
                    for ve in child.iter():
                        if lt(ve)=='varequal' and ve.text: negated.append(ve.text.strip())
            negset=set(negated)
            for ve in rc.iter():
                if lt(ve)=='varequal' and ve.text and ve.text.strip() not in negset:
                    required.append(ve.text.strip())
        qtype=""
        for f in item.iter():
            if lt(f)=='fieldlabel' and (f.text or '').strip()=='question_type':
                p=list(item.iter()); i=p.index(f)
                for e in p[i:i+3]:
                    if lt(e)=='fieldentry': qtype=(e.text or '').strip(); break
        imgs=[m.get('src') for m in item.iter() if lt(m)=='matimage' or (lt(m)=='mattext' and False)]
        imgs+=re.findall(r'src="([^"]+)"', ET.tostring(item, encoding='unicode'))
        rows.append({"package":pkg,"zip_sha12":sha,"title":title,"question_type":qtype,
                     "stem":stem,"choices":choices,"n_choices":len(choices),
                     "required":sorted(set(required)),"negated":sorted(set(negated)),
                     "n_respcondition":nconds,"images":sorted(set(imgs))})
json.dump(rows, open("corpus_v2.json","w"), indent=1, ensure_ascii=False)
print("items cached:", len(rows))
import collections
print("by type:", dict(collections.Counter(r['question_type'] for r in rows)))
print("packages:", len({r['package'] for r in rows}))
print("items with images:", sum(1 for r in rows if r['images']))
print("items with >1 respcondition:", sum(1 for r in rows if r['n_respcondition']>1))
