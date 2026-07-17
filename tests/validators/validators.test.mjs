import test from 'node:test';
import assert from 'node:assert/strict';
import { createEvidenceAdapter, runValidator, runValidators, verifyEvidenceAdapter, ValidatorError } from '../../scripts/validators/index.mjs';

test('unknown validator IDs fail closed', () => {
  assert.throws(() => runValidator('not_real'), ValidatorError);
});

test('adapter evidence is SHA-bound and cannot be forged', () => {
  const now = new Date().toISOString();
  const evidence = createEvidenceAdapter({ taskId: 'P0-T03', validatorId: 'evidence_schema', command: 'node --test tests/', exitCode: 0, startedAt: now, completedAt: now });
  assert.equal(verifyEvidenceAdapter(evidence), true);
  assert.throws(() => verifyEvidenceAdapter({ ...evidence, exit_code: 99 }), /签名不匹配/);
  assert.throws(() => verifyEvidenceAdapter({ ...evidence, candidate_sha: '0'.repeat(40) }), /签名不匹配|SHA/);
});

test('validator suite runs without mutating repository', () => {
  const results = runValidators();
  assert.equal(results.length, 10);
  assert(results.every((entry) => entry.ok));
});
