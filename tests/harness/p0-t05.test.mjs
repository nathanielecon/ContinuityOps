import test from 'node:test';
import assert from 'node:assert/strict';
import { readPlan, runP0T05ValidationSuite, assertPhaseAuthorized, ContractError } from '../../scripts/project.mjs';
import { P0_T05_VALIDATOR_IDS } from '../../scripts/validators/core.mjs';

test('runP0T05ValidationSuite passes all integrated-gate validators', () => {
  const plan = readPlan();
  assert.equal(plan.authorized_through_phase, 8);
  assert.equal(assertPhaseAuthorized(plan, 'P0-T05').id, 'P0-T05');
  const beyond = {
    ...plan,
    tasks: [...plan.tasks, { id: 'P99-T01', phase: 9, state: 'planned', write_scope: [], evidence: [] }]
  };
  assert.throws(() => assertPhaseAuthorized(beyond, 'P99-T01'), (error) => error instanceof ContractError && error.code === 'phase_unauthorized');

  const result = runP0T05ValidationSuite();
  assert.equal(result.task_id, 'P0-T05');
  assert.deepEqual(result.failed, []);
  for (const id of P0_T05_VALIDATOR_IDS) {
    assert.equal(result.validators[id], true, id);
  }
  assert.equal(result.model_record.provider, 'xAI');
  assert.equal(result.model_record.model, 'cursor-grok-4.5-high');
});
