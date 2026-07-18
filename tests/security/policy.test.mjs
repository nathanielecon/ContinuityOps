import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

test('least-privilege and admission negatives parse', () => {
  const lp = JSON.parse(readFileSync(resolve(ROOT, 'security/least-privilege.json'), 'utf8'));
  assert.ok(lp.negative_cases.some((c) => c.expect === 'deny'));
  const adm = JSON.parse(readFileSync(resolve(ROOT, 'security/admission-negative.json'), 'utf8'));
  assert.ok(adm.blocked_deployments.length >= 2);
});

test('SBOM stub does not claim L4+', () => {
  const sbom = JSON.parse(readFileSync(resolve(ROOT, 'security/sbom-stub.json'), 'utf8'));
  assert.equal(sbom.claim_ceiling, 'L1');
});
