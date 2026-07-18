import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

test('kind scenario labeled local-only', () => {
  const kind = JSON.parse(readFileSync(resolve(ROOT, 'kubernetes/scenarios/kind-local.json'), 'utf8'));
  assert.equal(kind.label, 'local-only');
  assert.equal(kind.environment, 'local');
  assert.ok(kind.remaining_boundaries.includes('managed_cluster_apply'));
});

test('failure matrix covers required classes', () => {
  const matrix = JSON.parse(readFileSync(resolve(ROOT, 'kubernetes/scenarios/failure-matrix.json'), 'utf8'));
  const ids = matrix.scenarios.map((s) => s.id).sort();
  assert.deepEqual(ids, ['crashloop', 'dns', 'network-policy', 'readiness', 'resource', 'scheduling']);
  for (const s of matrix.scenarios) {
    assert.ok(existsSync(resolve(ROOT, s.path)));
    const scenario = JSON.parse(readFileSync(resolve(ROOT, s.path), 'utf8'));
    assert.equal(scenario.synthetic, true);
    assert.ok(scenario.reset?.script);
  }
});

test('reset script records synthetic evidence', () => {
  const evidencePath = resolve(ROOT, 'evidence/slices/S2/scenarios/crashloop-reset.json');
  const before = readFileSync(evidencePath, 'utf8');
  try {
    const out = execFileSync('node', ['scripts/kubernetes/reset-scenario.mjs', 'crashloop'], {
      cwd: ROOT,
      encoding: 'utf8'
    });
    const parsed = JSON.parse(out);
    assert.equal(parsed.ok, true);
    const evidence = JSON.parse(readFileSync(resolve(ROOT, parsed.path), 'utf8'));
    assert.equal(evidence.synthetic, true);
    assert.equal(evidence.action, 'reset');
  } finally {
    writeFileSync(evidencePath, before);
  }
});

test('kind preflight emits claim level without managed apply', () => {
  const out = execFileSync('node', ['scripts/kubernetes/kind-preflight.mjs'], { cwd: ROOT, encoding: 'utf8' });
  const parsed = JSON.parse(out);
  assert.ok(['L1', 'L2'].includes(parsed.claim_level));
  assert.ok(parsed.remaining_boundaries.includes('managed_cluster_apply'));
  assert.equal(parsed.label, 'local-only');
});
