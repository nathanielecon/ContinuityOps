import { mkdtempSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';

const repoRoot = new URL('../..', import.meta.url).pathname;

test('security SBOM generator emits deterministic repository inventory when timestamp is pinned', () => {
  const dir = mkdtempSync(join(tmpdir(), 'continuityops-sbom-'));
  const first = join(dir, 'first.json');
  const second = join(dir, 'second.json');
  const env = { ...process.env, SOURCE_DATE_EPOCH: '1784332800' };

  execFileSync('node', ['scripts/security/generate-sbom.mjs', `--output=${first}`], { cwd: repoRoot, env });
  execFileSync('node', ['scripts/security/generate-sbom.mjs', `--output=${second}`], { cwd: repoRoot, env });

  const firstDoc = JSON.parse(readFileSync(first, 'utf8'));
  const secondDoc = JSON.parse(readFileSync(second, 'utf8'));

  assert.deepEqual(firstDoc, secondDoc);
  assert.equal(firstDoc.metadata.generator, 'scripts/security/generate-sbom.mjs');
  assert.ok(firstDoc.components.some((component) => component.path === 'tests/package.json'));
  assert.ok(firstDoc.components.every((component) => /^[a-f0-9]{64}$/.test(component.sha256)));
});
