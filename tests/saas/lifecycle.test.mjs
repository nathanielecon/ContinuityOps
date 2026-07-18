import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

test('SaaS lifecycle stages and severity ownership defined', () => {
  const lifecycle = JSON.parse(readFileSync(resolve(ROOT, 'operations/saas/lifecycle.json'), 'utf8'));
  const stages = lifecycle.stages.map((s) => s.id);
  for (const required of ['onboarding', 'config', 'migration', 'support', 'suspension', 'export', 'deprovision']) {
    assert.ok(stages.includes(required), `missing stage ${required}`);
  }
  assert.equal(lifecycle.tenant_isolation.cross_tenant_reads, 'prohibited');
  const sev = JSON.parse(readFileSync(resolve(ROOT, 'operations/saas/severity-escalation.json'), 'utf8'));
  assert.ok(sev.severities.length >= 3);
  assert.ok(existsSync(resolve(ROOT, 'docs/architecture/tenant-boundary.md')));
});
