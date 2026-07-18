/**
 * Parse continuityops-chief-page-v1 marker.
 */

/**
 * @param {string} body
 * @returns {null | {
 *   reason: string,
 *   issue_ids: number[],
 *   recommended_action: string,
 *   context_remaining: string
 * }}
 */
export function parseChiefPage(body) {
  const text = String(body || '');
  if (!/<!--\s*continuityops-chief-page-v1\s*-->/i.test(text)) return null;
  const reason = (text.match(/^reason:\s*(.+)$/m) || [])[1]?.trim() || '';
  const action =
    (text.match(/^recommended_action:\s*(\S+)/m) || [])[1]?.trim() || '';
  const ctx =
    (text.match(/^context_remaining:\s*(.+)$/m) || [])[1]?.trim() || '';
  const idsRaw = (text.match(/^issue_ids:\s*(\[[^\]]*\])/m) || [])[1];
  let issue_ids = [];
  if (idsRaw) {
    try {
      issue_ids = JSON.parse(idsRaw).map(Number).filter((n) => Number.isFinite(n));
    } catch {
      issue_ids = [];
    }
  }
  return {
    reason,
    issue_ids,
    recommended_action: action,
    context_remaining: ctx,
  };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const fs = await import('node:fs');
  const body = fs.readFileSync(process.argv[2] || '/dev/stdin', 'utf8');
  process.stdout.write(JSON.stringify(parseChiefPage(body)) + '\n');
}
