import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const script = fileURLToPath(new URL('../../scripts/parse-junior-actuate.py', import.meta.url));

function run(mode, text) {
  const dir = mkdtempSync(join(tmpdir(), 'co-actuate-'));
  const path = join(dir, 'in.txt');
  writeFileSync(path, text);
  const result = spawnSync('python3', [script, mode, path], { encoding: 'utf8' });
  return result;
}

test('parse merge intent', () => {
  const result = run(
    'intent',
    '<!-- continuityops-merge-v1 -->\npr: 44\nd037_issue: 45\n'
  );
  assert.equal(result.status, 0, result.stderr);
  assert.deepEqual(JSON.parse(result.stdout), { kind: 'merge', pr: 44, d037_issue: 45 });
});

test('parse dispatch intent with fenced @codex body', () => {
  const result = run(
    'intent',
    '<!-- continuityops-dispatch-v1 -->\ntarget_issue: 46\n\n```text\n@codex do the thing\n```\n'
  );
  assert.equal(result.status, 0, result.stderr);
  const parsed = JSON.parse(result.stdout);
  assert.equal(parsed.kind, 'dispatch');
  assert.equal(parsed.target_issue, 46);
  assert.match(parsed.body, /@codex/);
});

test('latest verdict prefers last bot structured verdict', () => {
  const comments = JSON.stringify([
    { user: { login: 'chatgpt-codex-connector[bot]' }, body: '{"verdict":"fail"}' },
    { user: { login: 'chatgpt-codex-connector[bot]' }, body: '### x\n```json\n{"verdict":"pass"}\n```' }
  ]);
  const result = run('verdict', comments);
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stdout.trim(), 'pass');
});

test('refuse secret-like dispatch body', () => {
  const result = run(
    'intent',
    '<!-- continuityops-dispatch-v1 -->\ntarget_issue: 46\n\n```text\n@codex ghp_exampletoken\n```\n'
  );
  assert.notEqual(result.status, 0);
});
