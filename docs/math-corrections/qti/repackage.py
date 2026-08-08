#!/usr/bin/env python3
"""Rebuild the 14 corrected QTI zips from $QTI_SRC and emit checksums.

Deliberately mirrors the originals' internal layout: the zip root holds
imsmanifest.xml plus one directory named for the assessment. Canvas rejects a
package whose manifest is not at the root, so the archive is written from the
package directory itself rather than from its parent.
"""
import hashlib, os, re, shutil, sys, tempfile, zipfile
import xml.etree.ElementTree as ET

# The three directories a $IMS-CC-FILEBASE$/media/ reference could resolve to.
MIRROR_PREFIXES = ("media/", "web_resources/media/", "<quizfolder>/media/")

SRC = os.environ.get("QTI_SRC", "/tmp/qtiwork/pkg")
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/qtiwork/out"
os.makedirs(OUT, exist_ok=True)
# Staging dir: nothing lands in OUT until every package has passed.
STAGE = tempfile.mkdtemp(
    prefix="qti-stage-",
    # abspath+rstrip, because os.path.dirname("/x/out/") returns "/x/out" --
    # a trailing slash put the staging directory INSIDE the artifact
    # directory, so a leak landed in OUT itself (BF-2026-056).
    dir=os.path.dirname(os.path.abspath(OUT.rstrip(os.sep))) or ".")

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
    manifest_members = [r for r in rel
                        if os.path.basename(r).lower() == "imsmanifest.xml"]
    if manifest_members != ["imsmanifest.xml"]:
        failures.append(f"{pkg}: imsmanifest.xml members are "
                        f"{manifest_members!r}, expected exactly "
                        f"['imsmanifest.xml'] at the archive root")
        continue
    for full, r in members:
        if r.endswith(".xml"):
            try:
                ET.parse(full)
            except Exception as e:
                failures.append(f"{pkg}: {r} does not parse: {e}")

    # A package that already failed to parse must not reach the unguarded
    # re-parse below: a malformed imsmanifest.xml raised ParseError, aborted the
    # process by traceback, and skipped the cleanup -- leaking a staging
    # directory full of zips no checksum vouches for. That failure mode did not
    # exist before staging; I introduced it (BF-2026-056).
    if any(f.startswith(pkg + ":") for f in failures):
        continue

    # Every href the manifest declares must resolve to a file actually present.
    manifest_path = os.path.join(d, "imsmanifest.xml")
    manifest_bytes = open(manifest_path, "rb").read()
    man = ET.parse(manifest_path).getroot()
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
    # ...and that there are THREE of them. The digest rule asserts the copies
    # AGREE and never that they all exist: deleting one mirror plus its <file>
    # declaration left every href resolving, every file declared, and the two
    # survivors identical -- so the gate passed while one of the three
    # $IMS-CC-FILEBASE$ readings the mirrors exist to cover silently lost its
    # file (BF-2026-055).
    # Counting three is not covering three. MIRROR_PREFIXES was consulted only
    # for its LENGTH, so three copies in the wrong three places passed: moving
    # web_resources/media/ to bogus/media/ kept the count, the digests and every
    # declaration intact while the web_resources reading of the token silently
    # lost its file -- verbatim the harm the rule was written to prevent
    # (BF-2026-056).
    for name, paths in sorted(groups.items()):
        locs = {r.rsplit("/", 1)[0] + "/" if "/" in r else "" for r in
                [os.path.relpath(p, d) for p in paths]}
        # Assert all THREE locations, including the quiz folder's. The previous
        # fix hardcoded two prefixes and left the third as a bare count -- so
        # the identical hole survived on the very mirror MIRROR_PREFIXES is
        # named for: moving <quizfolder>/media/ to bogus3/media/ kept the count
        # at three and passed. The quiz folder is derived from the manifest
        # rather than guessed (BF-2026-057).
        qres = man.find('.//*[@type="imsqti_xmlv1p2"]')
        qf = os.path.dirname(qres.get("href")) if qres is not None else ""
        want = {p.replace("<quizfolder>", qf) for p in MIRROR_PREFIXES}
        if locs != want:
            failures.append(f"{pkg}: {name} mirrors sit at {sorted(locs)}, "
                            f"expected {sorted(want)} -- a $IMS-CC-FILEBASE$ "
                            f"reading would 404")
        digests = {hashlib.sha256(open(p, "rb").read()).hexdigest() for p in paths}
        if len(digests) > 1:
            failures.append(f"{pkg}: the {len(paths)} copies of {name} are not "
                            f"byte-identical -- Canvas would serve different "
                            f"figures depending on how the token resolves")

    # THE QUIZ ITSELF WAS NEVER IDENTIFIED. Every rule above is about names
    # resolving -- each href resolves, each packaged file is declared, no
    # identifier collides -- and none asks which resource Canvas will read as
    # the quiz. `type="imsqti_xmlv1p2"` was consulted exactly once in this file,
    # inside the media-mirror loop, which iterates `groups` and so runs only on
    # the ONE package that has media; the other 13 never evaluated it. That is
    # this project's recurring sub-shape -- a lesson reaching some sites and not
    # the rest -- at its most extreme ratio yet, 1 of 14. Break the type and the
    # package passes both tools while Canvas finds no quiz resource and imports
    # nothing. validate.py never opens the manifest and this file never opens an
    # item XML, so nothing anywhere tied the file that was validated to the file
    # that will be imported (BF-2026-066).
    qress = [el for el in man.iter()
             if el.tag.endswith("resource")
             and el.get("type") == "imsqti_xmlv1p2"]
    if len(qress) != 1:
        failures.append(f"{pkg}: {len(qress)} resources of type "
                        f"imsqti_xmlv1p2 -- Canvas reads the quiz from this "
                        f"resource, so the package imports nothing or imports "
                        f"an ambiguous quiz")
    else:
        qhrefs = ([qress[0].get("href")] if qress[0].get("href") else []) + \
                 [fe.get("href") for fe in qress[0]
                  if fe.tag.endswith("file") and fe.get("href")]
        qhrefs = list(dict.fromkeys(qhrefs))
        if len(qhrefs) != 1:
            failures.append(f"{pkg}: the imsqti_xmlv1p2 resource names "
                            f"{len(qhrefs)} files {qhrefs}")
        else:
            qbody = open(os.path.join(d, qhrefs[0]), encoding="utf-8").read()
            if ("questestinterop" not in qbody
                    or not re.findall(r"<item\b", qbody)):
                failures.append(f"{pkg}: the imsqti_xmlv1p2 resource points at "
                                f"{qhrefs[0]!r}, which holds no "
                                f"<questestinterop> items -- the validated file "
                                f"and the imported file are not the same file")

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
    # Build into a STAGING directory, never straight into OUT. The docstring
    # above has always said "gate on structure before writing anything", and
    # the code did not do it: the zip was written here inside the per-package
    # loop while `failures` was not consulted until every package had been
    # written. Proved by drifting one byte of an SVG and rebuilding -- the good
    # zip was overwritten by the defective one, and sha256sums.txt survived
    # from the previous run still vouching for a hash no longer present. That
    # inverts this project's own doctrine that a checksum proves an artifact is
    # the one a judge scored (BF-2026-055).
    zpath = os.path.join(STAGE, f"{pkg}.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for full, r in members:
            info = zipfile.ZipInfo(r, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(full, "rb") as fh:
                z.writestr(info, fh.read())

    # Bind the member written to the bytes parsed above. Reading it back from
    # the staged archive makes this assertion independent of the member loop.
    with zipfile.ZipFile(zpath) as z:
        written_manifest = z.read("imsmanifest.xml")
    if written_manifest != manifest_bytes:
        failures.append(f"{pkg}: archived imsmanifest.xml differs from the "
                        f"manifest parsed during packaging")
        continue

    sha = hashlib.sha256(open(zpath, "rb").read()).hexdigest()
    rows.append((sha, f"{pkg}.zip", len(members)))

if failures:
    print("STRUCTURAL FAILURES — nothing written:")
    for f in failures:
        print("  " + f)
    shutil.rmtree(STAGE, ignore_errors=True)
    sys.exit(1)

# Only now does anything in OUT change, so a failing run leaves the last good
# artifacts and their checksums exactly as they were.
for name in os.listdir(STAGE):
    shutil.move(os.path.join(STAGE, name), os.path.join(OUT, name))
shutil.rmtree(STAGE, ignore_errors=True)

# Drop any zip no row vouches for. Removing a package from SRC used to leave a
# stale artifact in OUT with no checksum covering it at all -- the converse of
# the BF-2026-055 failure, and the same broken guarantee: the publish directory
# served a build from a corpus nobody judged (BF-2026-056).
expected = {n for _, n, _ in rows}
for f in sorted(os.listdir(OUT)):
    if f.endswith(".zip") and f not in expected:
        os.remove(os.path.join(OUT, f))
        print(f"  removed stale artifact no checksum covers: {f}")

with open(os.path.join(OUT, "sha256sums.txt"), "w") as fh:
    for sha, name, _ in rows:
        fh.write(f"{sha}  {name}\n")

print(f"{len(rows)} packages written to {OUT}")
for sha, name, n in rows:
    print(f"  {sha[:12]}  {n:2d} files  {name}")
