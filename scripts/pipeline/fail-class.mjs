/**
 * Fail-class hashing and two-strike counter helpers (D-047).
 */

import { createHash } from 'node:crypto';

/**
 * Stable short hash for a failure class fingerprint.
 * @param {string | string[]} fingerprint
 * @returns {string} 8-char hex
 */
export function failClassHash(fingerprint) {
  const material = Array.isArray(fingerprint)
    ? fingerprint.map(String).sort().join('\n')
    : String(fingerprint || '');
  return createHash('sha256').update(material).digest('hex').slice(0, 8);
}

/**
 * Label name for GitHub: fail-class:<hash>
 * @param {string} hash
 */
export function failClassLabel(hash) {
  return `fail-class:${hash}`;
}

/**
 * Count how many labels match fail-class:<hash> on an issue/PR label list,
 * or sum strike annotations. Prefer explicit strike_count when provided.
 *
 * @param {{ labels?: Array<string | { name: string }>, strike_count?: number, hash?: string }} opts
 * @returns {{ hash: string | null, strike_count: number, halt: boolean }}
 */
export function countFailClassStrikes(opts = {}) {
  const labels = (opts.labels || []).map((l) => (typeof l === 'string' ? l : l.name));
  let hash = opts.hash || null;
  if (!hash) {
    const hit = labels.find((n) => n.startsWith('fail-class:'));
    if (hit) hash = hit.slice('fail-class:'.length);
  }
  let strike_count =
    typeof opts.strike_count === 'number' ? opts.strike_count : 0;
  if (!strike_count && hash) {
    strike_count = labels.filter((n) => n === failClassLabel(hash)).length;
    // Also accept fail-class:<hash>-n annotations
    for (const n of labels) {
      const m = n.match(new RegExp(`^fail-class:${hash}-(\\d+)$`));
      if (m) strike_count = Math.max(strike_count, Number(m[1]));
    }
    if (strike_count === 0 && labels.includes(failClassLabel(hash))) {
      strike_count = 1;
    }
  }
  return { hash, strike_count, halt: strike_count >= 2 };
}

/**
 * Next strike annotation label after seeing a repeat of the same class.
 * @param {string} hash
 * @param {number} current
 */
export function nextStrikeLabel(hash, current) {
  const next = Math.max(1, Number(current) || 0) + 1;
  return `fail-class:${hash}-${next}`;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const mode = process.argv[2] || 'hash';
  if (mode === 'hash') {
    const fp = process.argv.slice(3).join(' ') || '';
    const hash = failClassHash(fp);
    process.stdout.write(JSON.stringify({ hash, label: failClassLabel(hash) }) + '\n');
  } else if (mode === 'count') {
    const fs = await import('node:fs');
    const raw = fs.readFileSync(process.argv[3] || '/dev/stdin', 'utf8');
    process.stdout.write(JSON.stringify(countFailClassStrikes(JSON.parse(raw))) + '\n');
  } else {
    console.error('usage: fail-class.mjs hash <fp> | count <json>');
    process.exit(2);
  }
}
