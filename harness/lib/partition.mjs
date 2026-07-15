// Partition manifest: assign every retained path to exactly one primary slice,
// hash each slice's file list, and detect duplicate ownership.
// (MASTER_PLAN.md section 6; RALPHY_ORCHESTRATION.md section 4.)

import { hashJson, sha256File } from './hashing.mjs';
import { existsSync } from 'node:fs';

/**
 * Verify unique ownership across a partition manifest.
 * @param manifest { slices: [{ id, paths: [] }, ...] }
 * Returns { ok, duplicates: [{path, slices:[]}], sliceHashes }
 */
export function verifyUniqueOwnership(manifest) {
  const owners = new Map(); // path -> [sliceId]
  for (const slice of manifest.slices) {
    for (const p of slice.paths) {
      if (!owners.has(p)) owners.set(p, []);
      owners.get(p).push(slice.id);
    }
  }
  const duplicates = [];
  for (const [p, slices] of owners) {
    if (slices.length > 1) duplicates.push({ path: p, slices });
  }
  return { ok: duplicates.length === 0, duplicates };
}

/** Compute a content hash for each slice's existing files. */
export function hashSlices(manifest, repoRoot) {
  const out = {};
  for (const slice of manifest.slices) {
    const entries = slice.paths.map((p) => {
      const abs = `${repoRoot}/${p}`;
      return { path: p, sha256: existsSync(abs) ? sha256File(abs) : null };
    });
    out[slice.id] = { files: entries, slice_sha256: hashJson(entries) };
  }
  return out;
}
