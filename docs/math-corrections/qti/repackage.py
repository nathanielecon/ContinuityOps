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
    # `(^|/)media/`, not `"/media/" in r`: the substring form requires a slash
    # BEFORE media, so a media directory at the ARCHIVE ROOT was invisible to
    # this check -- and the archive root is one of the three places the
    # $IMS-CC-FILEBASE$ mirrors now go, so the check would have gone silent on
    # exactly the layout it exists to police (BF-2026-049).
    for r in rel:
        if re.search(r"(^|/)media/", r) and r not in declared:
            failures.append(f"{pkg}: {r} is packaged but not declared in the "
                            f"manifest -- Canvas will not publish it")

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
