/**
 * Extract merge_ready from judge evidence JSON text or PR file content.
 */

/**
 * @param {string} text
 * @returns {'yes' | 'no' | 'provisional' | null}
 */
export function extractMergeReady(text) {
  const body = String(text || '');
  try {
    const obj = JSON.parse(body);
    const v = obj?.merge_ready;
    if (v === 'yes' || v === 'no' || v === 'provisional') return v;
  } catch {
    /* fall through to regex */
  }
  const m = body.match(/"merge_ready"\s*:\s*"(yes|no|provisional)"/i);
  if (m) return m[1].toLowerCase();
  const y = body.match(/^merge_ready:\s*(yes|no|provisional)\s*$/im);
  if (y) return y[1].toLowerCase();
  return null;
}

/**
 * @param {Array<{ path?: string, filename?: string, content?: string }>} files
 * @returns {{ path: string, merge_ready: 'yes' | 'no' | 'provisional' }[]}
 */
export function extractMergeReadyFromJudgeFiles(files) {
  const out = [];
  for (const f of files || []) {
    const path = f.path || f.filename || '';
    if (!path.includes('evidence/judges/')) continue;
    const mr = extractMergeReady(f.content || '');
    if (mr) out.push({ path, merge_ready: mr });
  }
  return out;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const fs = await import('node:fs');
  const raw = fs.readFileSync(process.argv[2] || '/dev/stdin', 'utf8');
  process.stdout.write(JSON.stringify({ merge_ready: extractMergeReady(raw) }) + '\n');
}
