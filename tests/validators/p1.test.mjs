import test from 'node:test';
import assert from 'node:assert/strict';
import {
  getValidator,
  P1_T01_VALIDATOR_IDS,
  P1_T02_VALIDATOR_IDS,
  P1_T03_VALIDATOR_IDS,
  P1_T04_VALIDATOR_IDS,
  ValidationError
} from '../../scripts/validators/core.mjs';

test('P1 validator IDs are registered and unknown IDs fail closed', () => {
  for (const id of [...P1_T01_VALIDATOR_IDS, ...P1_T02_VALIDATOR_IDS, ...P1_T03_VALIDATOR_IDS, ...P1_T04_VALIDATOR_IDS]) {
    assert.equal(typeof getValidator(id), 'function');
  }
  assert.throws(
    () => getValidator('not_a_p1_validator'),
    (error) => error instanceof ValidationError && error.code === 'validator_unknown'
  );
});
