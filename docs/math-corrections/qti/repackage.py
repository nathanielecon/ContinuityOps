#!/usr/bin/env python3
"""Rebuild the 14 corrected QTI zips from $QTI_SRC and emit checksums.

Deliberately mirrors the originals' internal layout: the zip root holds
imsmanifest.xml plus one directory named for the assessment. Canvas rejects a
package whose manifest is not at the root, so the archive is written from the
package directory itself rather than from its parent.
"""
import hashlib, os, re, sys, zipfile
import xml.etree.ElementTree as ET

SRC = os.environ.get("QTI_SRC", "/tmp/qtiwork/pkg")
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/qtiwork/out"
os.makedirs(OUT, exist_ok=True)

def files_of(root):
    out = []
    for dirpath, _, names in os.walk(root):
        for n in sorted(names):
            full = os.path.join(dirpath, n)
            out.append((full, os.path.relpath(full, root)))
    return sorted(out, key=lambda t: t[1])

rows, failures = [], []
for pkg in sorted(os.listdir(SRC)):
    d = os.path.join(SRC, pkg)
    if not os.path.isdir(d):
        continue
    members = files_of(d)

    # Gate on structure before writing anything: a zip that fails to import is
    # worse than no zip, because the failure surfaces in front of students.
    rel = [r for _, r in members]
    if "imsmanifest.xml" not in rel:
        failures.append(f"{pkg}: no imsmanifest.xml at archive root")
        continue
    for full, r in members:
        if r.endswith(".xml"):
            try:
                ET.parse(full)
            except Exception as e:
                failures.append(f"{pkg}: {r} does not parse: {e}")

    # Every href the manifest declares must resolve to a file actually present.
    man = ET.parse(os.path.join(d, "imsmanifest.xml")).getroot()
    declared = set()
    for el in man.iter():
        href = el.get("href")
        if href:
            declared.add(href)
            if href not in rel:
                failures.append(f"{pkg}: manifest href does not resolve: {href}")

    # ...and the reverse, which was missing. files_of() is a bare os.walk, so a
    # media file that nothing declares gets packaged happily and is then never
    # published by Canvas. The symptom -- a broken image -- is identical to the
    # $IMS-CC-FILEBASE$ path-depth question, so it would have been diagnosed as
    # that and "fixed" somewhere it was not broken (BF-2026-048).
    # Every packaged file must be declared -- not just media. BF-2026-048 named
    # the one-directional gate as the bug and then closed it only for media,
    # which left the general property unenforced; and the media predicate itself
    # was wrong twice (a substring form that missed the archive root, then a
    # path predicate at all). "Everything in the archive is declared" is what
    # makes the archive trustworthy, and it needs no predicate (BF-2026-050).
    for r in rel:
        if r != "imsmanifest.xml" and r not in declared:
            failures.append(f"{pkg}: {r} is packaged but not declared in the "
                            f"manifest -- Canvas will not publish it")

    # Duplicate resource identifiers, and dangling dependencies. This is the
    # round that added a SECOND resource to a manifest, so it is exactly the
    # round where a collision becomes possible. A duplicate identifier makes
    # <dependency identifierref> ambiguous and Canvas resolves one resource and
    # drops the other -- which would present as one of the $IMS-CC-FILEBASE$
    # mirrors silently not publishing, the very failure the mirrors exist to
    # rule out.
    # The mirrors are compared by NAME everywhere above -- every href resolves,
    # every packaged file is declared -- and by BYTES nowhere. If two copies of
    # a figure drift apart, all three still resolve and all three are still
    # declared, so the package looks perfect while Canvas serves a DIFFERENT
    # figure depending on which $IMS-CC-FILEBASE$ reading wins. Undiagnosable
    # from the package. Drift in this path is demonstrated, not hypothetical:
    # BF-2026-049 records do_media copying a file onto itself (BF-2026-051).
    groups = {}
    for full, r in members:
        if re.search(r"(^|/)media/", r):
            groups.setdefault(os.path.basename(r), []).append(full)
    for name, paths in sorted(groups.items()):
        digests = {hashlib.sha256(open(p, "rb").read()).hexdigest() for p in paths}
        if len(digests) > 1:
            failures.append(f"{pkg}: the {len(paths)} copies of {name} are not "
                            f"byte-identical -- Canvas would serve different "
                            f"figures depending on how the token resolves")

    ids = [el.get("identifier") for el in man.iter()
           if el.tag.endswith("resource") and el.get("identifier")]
    for dup in {i for i in ids if ids.count(i) > 1}:
        failures.append(f"{pkg}: duplicate resource identifier {dup!r} -- "
                        f"dependency references to it are ambiguous")
    for el in man.iter():
        ref = el.get("identifierref")
        if ref and ref not in ids:
            failures.append(f"{pkg}: dependency identifierref {ref!r} "
                            f"resolves to no resource")

    # Deterministic archives: zip stores each entry's mtime, and extracting to a
    # fresh temp dir stamps "now" on every file, so two builds of byte-identical
    # content produced different sha256s. Checksums are how this project proves
    # an artifact is the one that was judged, so that had to be pinned. Fixed
    # date and permissions; entries already sorted by path above.
    zpath = os.path.join(OUT, f"{pkg}.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for full, r in members:
            info = zipfile.ZipInfo(r, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(full, "rb") as fh:
                z.writestr(info, fh.read())

    sha = hashlib.sha256(open(zpath, "rb").read()).hexdigest()
    rows.append((sha, f"{pkg}.zip", len(members)))

if failures:
    print("STRUCTURAL FAILURES — not writing checksums:")
    for f in failures:
        print("  " + f)
    sys.exit(1)

with open(os.path.join(OUT, "sha256sums.txt"), "w") as fh:
    for sha, name, _ in rows:
        fh.write(f"{sha}  {name}\n")

print(f"{len(rows)} packages written to {OUT}")
for sha, name, n in rows:
    print(f"  {sha[:12]}  {n:2d} files  {name}")
