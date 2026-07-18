import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

test('Helm chart files and digest pin present', () => {
  const out = execFileSync('node', ['scripts/kubernetes/render-chart.mjs'], { cwd: ROOT, encoding: 'utf8' });
  const parsed = JSON.parse(out);
  assert.equal(parsed.ok, true);
  assert.equal(parsed.digest_pin, true);
});

test('values require probes, resources, HPA, PDB, RBAC annotations', () => {
  const values = readFileSync(resolve(ROOT, 'kubernetes/chart/values.yaml'), 'utf8');
  assert.match(values, /liveness:/);
  assert.match(values, /readiness:/);
  assert.match(values, /requests:/);
  assert.match(values, /autoscaling:/);
  assert.match(values, /podDisruptionBudget:/);
  assert.match(values, /eks\.amazonaws\.com\/role-arn/);
  assert.match(values, /runAsNonRoot:\s*true/);
});

test('policies JSON parse', () => {
  for (const name of ['digest-pin.json', 'security-context.json', 'network-negative.json']) {
    const path = resolve(ROOT, 'kubernetes/policies', name);
    assert.ok(existsSync(path));
    JSON.parse(readFileSync(path, 'utf8'));
  }
});
