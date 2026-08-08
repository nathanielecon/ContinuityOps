#!/usr/bin/env bash
# Rebuild the 14 QTI packages from a pristine git ref, in one pass.
#
# WHY THIS EXISTS: repackage.py writes into zips/, and zips/ was also being used
# as the extraction source. Re-running the pipeline then applied the transforms
# on top of their own output. The result happened to stay valid -- the gate still
# passed -- but the artifact was no longer reproducible, and permute.py had run
# twice, so the shipped choice order was not the one the spec describes.
#
# The build source is therefore a git ref, never the working tree and never
# zips/. Feeding the pipeline its own output is now impossible by construction.
#
#   usage:  ./build.sh [ref]      (default: the round's baseline, f63d392)
set -euo pipefail

REF="${1:-f63d392}"
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

echo "== extracting pristine packages from $REF"
mkdir -p "$WORK/src" "$WORK/pkg"
cd "$ROOT"
for path in $(git ls-tree --name-only "$REF" docs/math-corrections/qti/zips/ | grep '\.zip$'); do
    name="$(basename "$path" .zip)"
    git show "$REF:$path" > "$WORK/src/$name.zip"
    mkdir -p "$WORK/pkg/$name"
    unzip -q -o "$WORK/src/$name.zip" -d "$WORK/pkg/$name"
done
echo "   $(ls "$WORK/pkg" | wc -l) packages"

# Keep an untouched copy so validate can prove no file's line endings moved
# (BF-2026-029) and so any item can be diffed against how it shipped.
cp -r "$WORK/pkg" "$WORK/base"

echo "== finalize"
python3 "$HERE/finalize.py" "$WORK/pkg"

echo "== permute (BF-2026-031)"
python3 "$HERE/permute.py" "$WORK/pkg" | tail -1

echo "== validate"
python3 "$HERE/validate.py" "$WORK/pkg" "$WORK/base"

echo "== answer battery"
# Derives its probes from each item's own answer by rules the generator does
# not share, so it cannot rubber-stamp expr_variants(). Found the Unicode-minus
# gap on its first run, on items no transform touches (BF-2026-068).
python3 "$HERE/battery.py" "$WORK/pkg" 2>/dev/null || \
    QTI_BATTERY_SRC="$WORK/pkg" python3 "$HERE/battery.py" "$WORK/pkg"

echo "== repackage"
QTI_SRC="$WORK/pkg" python3 "$HERE/repackage.py" "$HERE/zips"

echo "== done"
