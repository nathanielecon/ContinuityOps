import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

test('Azure governance is designed/static with ExpressRoute non-claim', () => {
  const gov = JSON.parse(readFileSync(resolve(ROOT, 'azure/governance.json'), 'utf8'));
  assert.equal(gov.implemented_versus_designed, 'designed_static');
  assert.ok(gov.non_claims.some((n) => /ExpressRoute/i.test(n)));
  assert.equal(gov.claim_ceiling, 'L1');
});
