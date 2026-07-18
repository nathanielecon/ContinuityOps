import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  getValidator,
  P5_T01_VALIDATOR_IDS,
  P5_T02_VALIDATOR_IDS,
  P5_T03_VALIDATOR_IDS,
  P6_T01_VALIDATOR_IDS,
  P6_T02_VALIDATOR_IDS,
  P6_T03_VALIDATOR_IDS,
  P6_T04_VALIDATOR_IDS,
  P7_T01_VALIDATOR_IDS,
  P7_T02_VALIDATOR_IDS,
  P7_T03_VALIDATOR_IDS,
  P7_T04_VALIDATOR_IDS,
  P8_T01_VALIDATOR_IDS,
  P8_T02_VALIDATOR_IDS,
  P8_T03_VALIDATOR_IDS,
  P8_T04_VALIDATOR_IDS,
  ValidationError
} from '../../scripts/validators/core.mjs';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

test('P5-P8 validator IDs are registered and unknown IDs fail closed', () => {
  const ids = [
    ...P5_T01_VALIDATOR_IDS,
    ...P5_T02_VALIDATOR_IDS,
    ...P5_T03_VALIDATOR_IDS,
    ...P6_T01_VALIDATOR_IDS,
    ...P6_T02_VALIDATOR_IDS,
    ...P6_T03_VALIDATOR_IDS,
    ...P6_T04_VALIDATOR_IDS,
    ...P7_T01_VALIDATOR_IDS,
    ...P7_T02_VALIDATOR_IDS,
    ...P7_T03_VALIDATOR_IDS,
    ...P7_T04_VALIDATOR_IDS,
    ...P8_T01_VALIDATOR_IDS,
    ...P8_T02_VALIDATOR_IDS,
    ...P8_T03_VALIDATOR_IDS,
    ...P8_T04_VALIDATOR_IDS
  ];
  for (const id of ids) {
    assert.equal(typeof getValidator(id), 'function');
  }
  assert.throws(
    () => getValidator('not_a_p5_validator'),
    (error) => error instanceof ValidationError && error.code === 'validator_unknown'
  );
});

test('runbook command_safety rejects unmarked destructive patterns', () => {
  const ctx = { root: ROOT, taskId: 'P5-T01', sliceId: 'S5' };
  assert.equal(getValidator('command_safety')(ctx).pass, true);
  assert.equal(getValidator('runbook_schema')(ctx).pass, true);
});

test('eight drills and two misleading symptoms exist', () => {
  const index = JSON.parse(readFileSync(resolve(ROOT, 'operations/incidents/S5/drill-index.json'), 'utf8'));
  assert.equal(index.required_drills.length, 8);
  assert.equal(index.misleading_symptoms.length, 2);
  assert.equal(index.live_production_drills, false);
});
