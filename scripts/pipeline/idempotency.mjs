/**
 * Zero-hop idempotency keys and label state machine (D-047).
 */

export const ZH_DISPATCHING = 'zh-dispatching';
export const ZH_DISPATCHED = 'zh-dispatched';

/**
 * Build a stable hop key so the same event does not double-fire.
 * @param {{ hop: string, subject: string | number, tip_sha?: string }} opts
 */
export function hopKey(opts) {
  const tip = (opts.tip_sha || '').slice(0, 7);
  return `zh:${opts.hop}:${opts.subject}${tip ? `@${tip}` : ''}`;
}

/**
 * Decide whether a hop may proceed given current labels and prior marker comments.
 * @param {{
 *   labels?: Array<string | { name: string }>,
 *   markerBodies?: string[],
 *   key: string
 * }} opts
 * @returns {{ proceed: boolean, reason: string, nextLabel: string | null }}
 */
export function evaluateIdempotency(opts) {
  const labels = (opts.labels || []).map((l) => (typeof l === 'string' ? l : l.name));
  const key = opts.key;
  const markers = opts.markerBodies || [];

  if (labels.includes(ZH_DISPATCHED) && markers.some((b) => b.includes(key) && b.includes('zh-done'))) {
    return { proceed: false, reason: 'already_dispatched', nextLabel: null };
  }
  if (markers.some((b) => String(b).includes(`zh-done:${key}`))) {
    return { proceed: false, reason: 'marker_done', nextLabel: null };
  }
  if (labels.includes(ZH_DISPATCHING) && markers.some((b) => b.includes(`zh-claim:${key}`))) {
    return { proceed: false, reason: 'in_flight', nextLabel: null };
  }
  return { proceed: true, reason: 'ok', nextLabel: ZH_DISPATCHING };
}

/**
 * Marker comment bodies for claim / done.
 */
export function claimMarker(key) {
  return `<!-- continuityops-zero-hop-v1 -->\nzh-claim:${key}`;
}

export function doneMarker(key) {
  return `<!-- continuityops-zero-hop-v1 -->\nzh-done:${key}`;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const fs = await import('node:fs');
  const raw = fs.readFileSync(process.argv[2] || '/dev/stdin', 'utf8');
  process.stdout.write(JSON.stringify(evaluateIdempotency(JSON.parse(raw))) + '\n');
}
