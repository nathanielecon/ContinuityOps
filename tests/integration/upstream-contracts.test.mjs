import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

function loadJson(rel) {
  return JSON.parse(readFileSync(resolve(ROOT, rel), 'utf8'));
}

test('upstreams.lock pins concrete SHAs and legal image_digest', () => {
  const lock = loadJson('integration/upstreams.lock.json');
  assert.equal(lock.schema_version, '1.0');
  assert.match(lock.project_a.commit_sha, /^[0-9a-f]{40}$/);
  assert.match(lock.project_c.commit_sha, /^[0-9a-f]{40}$/);
  assert.equal(lock.project_a.repository, 'nathanielecon/aws-landing-zone-lab');
  assert.equal(lock.project_c.repository, 'nathanielecon/local-first-governed-cicd');
  const digest = lock.project_c.image_digest;
  assert.ok(
    digest === 'UNAVAILABLE' || /^sha256:[0-9a-f]{64}$/.test(digest),
    'image_digest must be UNAVAILABLE or sha256:…'
  );
  assert.notEqual(digest, 'REQUIRED_OR_EXPLICITLY_UNAVAILABLE');
  assert.ok(Array.isArray(lock.project_a.consumed_contracts) && lock.project_a.consumed_contracts.length > 0);
  assert.ok(Array.isArray(lock.project_c.consumed_contracts) && lock.project_c.consumed_contracts.length > 0);
  assert.ok(Array.isArray(lock.missing_capabilities) && lock.missing_capabilities.length >= 1);
});

test('consumed contract files exist and declare pinned_sha alignment', () => {
  const lock = loadJson('integration/upstreams.lock.json');
  for (const rel of lock.project_a.consumed_contracts) {
    assert.ok(existsSync(resolve(ROOT, rel)), `missing ${rel}`);
    const contract = loadJson(rel);
    assert.equal(contract.pinned_sha, lock.project_a.commit_sha);
    assert.equal(contract.upstream, 'project_a');
  }
  for (const rel of lock.project_c.consumed_contracts) {
    assert.ok(existsSync(resolve(ROOT, rel)), `missing ${rel}`);
    if (rel.startsWith('integration/contracts/')) {
      const contract = loadJson(rel);
      assert.equal(contract.pinned_sha, lock.project_c.commit_sha);
      assert.equal(contract.upstream, 'project_c');
    }
  }
});

test('app-contract release contract marks digest UNAVAILABLE and lab boundary', () => {
  const app = loadJson('app-contract/release-contract.json');
  assert.equal(app.artifact.image_digest, 'UNAVAILABLE');
  assert.match(app.artifact.label, /lab/i);
  assert.ok(app.remaining_boundaries.some((b) => /digest/i.test(b)));
});

test('missing capabilities are explicit and named', () => {
  const lock = loadJson('integration/upstreams.lock.json');
  const ids = new Set(lock.missing_capabilities.map((m) => m.id));
  assert.ok(ids.has('MC-C-DIGEST'));
  assert.ok(ids.has('MC-A-TREE') || ids.has('MC-C-TREE'));
});
