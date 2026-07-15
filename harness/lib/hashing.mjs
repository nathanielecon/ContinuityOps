// Deterministic hashing helpers for bundle pinning and evidence binding.
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';

/** SHA-256 of a UTF-8 string, hex-encoded. */
export function sha256(text) {
  return createHash('sha256').update(text, 'utf8').digest('hex');
}

/** SHA-256 of a file's raw bytes. */
export function sha256File(path) {
  return createHash('sha256').update(readFileSync(path)).digest('hex');
}

/**
 * Canonical JSON stringify: object keys sorted recursively so the same
 * logical value always hashes to the same digest regardless of key order.
 */
export function canonicalize(value) {
  if (value === null || typeof value !== 'object') return JSON.stringify(value);
  if (Array.isArray(value)) return '[' + value.map(canonicalize).join(',') + ']';
  const keys = Object.keys(value).sort();
  return '{' + keys.map((k) => JSON.stringify(k) + ':' + canonicalize(value[k])).join(',') + '}';
}

/** SHA-256 over the canonical form of a JSON-serializable value. */
export function hashJson(value) {
  return sha256(canonicalize(value));
}
