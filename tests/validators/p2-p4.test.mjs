import test from 'node:test';
import assert from 'node:assert/strict';
import {
  getValidator,
  P2_T01_VALIDATOR_IDS,
  P2_T02_VALIDATOR_IDS,
  P2_T03_VALIDATOR_IDS,
  P2_T04_VALIDATOR_IDS,
  P3_T01_VALIDATOR_IDS,
  P3_T02_VALIDATOR_IDS,
  P3_T03_VALIDATOR_IDS,
  P4_T01_VALIDATOR_IDS,
  P4_T02_VALIDATOR_IDS,
  P4_T03_VALIDATOR_IDS,
  ValidationError
} from '../../scripts/validators/core.mjs';

test('P2-P4 validator IDs are registered and unknown IDs fail closed', () => {
  const ids = [
    ...P2_T01_VALIDATOR_IDS,
    ...P2_T02_VALIDATOR_IDS,
    ...P2_T03_VALIDATOR_IDS,
    ...P2_T04_VALIDATOR_IDS,
    ...P3_T01_VALIDATOR_IDS,
    ...P3_T02_VALIDATOR_IDS,
    ...P3_T03_VALIDATOR_IDS,
    ...P4_T01_VALIDATOR_IDS,
    ...P4_T02_VALIDATOR_IDS,
    ...P4_T03_VALIDATOR_IDS
  ];
  for (const id of ids) {
    assert.equal(typeof getValidator(id), 'function');
  }
  assert.throws(
    () => getValidator('not_a_p2_validator'),
    (error) => error instanceof ValidationError && error.code === 'validator_unknown'
  );
});
