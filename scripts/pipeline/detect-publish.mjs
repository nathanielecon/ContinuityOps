/**
 * Detect D-034 publish-ok / publish-failed markers in a comment body.
 */

/**
 * @param {string} body
 * @returns {{ kind: 'publish-ok' | 'publish-failed' | null, prUrl: string | null, prNumber: number | null }}
 */
export function detectPublish(body) {
  const text = String(body || '');
  const failed = /publish-failed\s*\(D-034\)/i.test(text);
  const ok = /publish-ok\s*\(D-034\)/i.test(text);
  if (failed && !ok) {
    return { kind: 'publish-failed', prUrl: null, prNumber: null };
  }
  if (ok) {
    const urlMatch = text.match(
      /https:\/\/github\.com\/[^/\s]+\/[^/\s]+\/pull\/(\d+)/
    );
    const prNumber = urlMatch ? Number(urlMatch[1]) : null;
    return {
      kind: 'publish-ok',
      prUrl: urlMatch ? urlMatch[0] : null,
      prNumber,
    };
  }
  return { kind: null, prUrl: null, prNumber: null };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const fs = await import('node:fs');
  const body = fs.readFileSync(process.argv[2] || '/dev/stdin', 'utf8');
  process.stdout.write(JSON.stringify(detectPublish(body)) + '\n');
}
