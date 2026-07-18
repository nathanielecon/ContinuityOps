import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

test('worker and event contracts parse with claim ceiling L1', () => {
  const worker = JSON.parse(readFileSync(resolve(ROOT, 'serverless/worker-contract.json'), 'utf8'));
  const events = JSON.parse(readFileSync(resolve(ROOT, 'serverless/event-contract.json'), 'utf8'));
  assert.equal(worker.claim_ceiling, 'L1');
  assert.ok(worker.remaining_boundaries.some((b) => /Lambda/i.test(b)));
  assert.ok(events.required_fields.includes('event_id'));
  assert.ok(existsSync(resolve(ROOT, 'terraform/modules/serverless/main.tf')));
  const tf = readFileSync(resolve(ROOT, 'terraform/modules/serverless/main.tf'), 'utf8');
  assert.match(tf, /long_lived_keys\s*=\s*false/);
});
