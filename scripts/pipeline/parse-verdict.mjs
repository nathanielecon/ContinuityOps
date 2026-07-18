/**
 * Parse latest D-037 bot verdict from issue comments JSON or raw body.
 */

/**
 * @param {unknown} comments
 * @returns {'pass' | 'fail' | null}
 */
export function parseLatestVerdict(comments) {
  const list = typeof comments === 'string' ? JSON.parse(comments) : comments;
  if (!Array.isArray(list)) return null;
  let found = null;
  for (const c of list) {
    const login = c?.user?.login || '';
    if (login !== 'chatgpt-codex-connector[bot]') continue;
    const body = c?.body || '';
    const m = body.match(/"verdict"\s*:\s*"(pass|fail)"/i);
    if (m) {
      found = m[1].toLowerCase();
      continue;
    }
    if (/^\s*verdict\s*:\s*pass\b/im.test(body) || /\bverdict\b[^\n]*\bpass\b/i.test(body)) {
      found = 'pass';
    } else if (
      /^\s*verdict\s*:\s*fail\b/im.test(body) ||
      /\bverdict\b[^\n]*\bfail\b/i.test(body)
    ) {
      found = 'fail';
    }
  }
  return found;
}

/**
 * @param {string} body
 * @returns {'pass' | 'fail' | null}
 */
export function parseVerdictFromBody(body) {
  return parseLatestVerdict([
    { user: { login: 'chatgpt-codex-connector[bot]' }, body: String(body || '') },
  ]);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const fs = await import('node:fs');
  const raw = fs.readFileSync(process.argv[2] || '/dev/stdin', 'utf8');
  let result;
  try {
    result = parseLatestVerdict(JSON.parse(raw));
  } catch {
    result = parseVerdictFromBody(raw);
  }
  process.stdout.write(JSON.stringify({ verdict: result }) + '\n');
}
