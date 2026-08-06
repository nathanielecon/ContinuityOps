#!/usr/bin/env python3
"""Rebuild the 14 corrected QTI zips from /tmp/qtiwork/pkg and emit checksums.

Deliberately mirrors the originals' internal layout: the zip root holds
imsmanifest.xml plus one directory named for the assessment. Canvas rejects a
package whose manifest is not at the root, so the archive is written from the
package directory itself rather than from its parent.
"""
import hashlib, os, sys, zipfile
import xml.etree.ElementTree as ET

SRC = "/tmp/qtiwork/pkg"
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
    for el in man.iter():
        href = el.get("href")
        if href and href not in rel:
            failures.append(f"{pkg}: manifest href does not resolve: {href}")

    zpath = os.path.join(OUT, f"{pkg}.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for full, r in members:
            z.write(full, r)

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
