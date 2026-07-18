import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import {
  ValidationError, getValidator, createEvidence, verifyEvidence, assertWorkerHandoffLanguage,
  detectForbiddenPaths, assertBottleneckProfile, assertClaudeProxyProfile, assertTypescriptPolicy
} from '../../scripts/validators/core.mjs';

test('unknown validator IDs fail closed', () => {
  assert.throws(() => getValidator('missing'), (error) => error instanceof ValidationError && error.code === 'validator_unknown');
});

test('adapter evidence is SHA-bound and rejects stale candidate SHA', () => {
  const evidence = createEvidence({ taskId: 'P0-T03', baselineSha: 'a'.repeat(40), candidateSha: 'b'.repeat(40), command: 'cmd', exitCode: 0, environment: { id: 'env' }, validators: ['validator_contract'], modelRecord: { provider: 'OpenAI', model: 'gpt-5.5', mode: 'default', role: 'validator-worker' } });
  assert.equal(verifyEvidence(evidence, 'b'.repeat(40)), true);
  assert.throws(() => verifyEvidence(evidence, 'c'.repeat(40)), /freshness/);
});

test('worker free-text handoff values must be Simplified Chinese', () => {
  assert.equal(assertWorkerHandoffLanguage({ completed: ['已完成检查'], validation_results: ['命令通过'] }), true);
  assert.throws(() => assertWorkerHandoffLanguage({ completed: ['completed in English'] }), /不是简体中文/);
});

test('late-created forbidden paths are detectable', () => {
  const dir = mkdtempSync(join(tmpdir(), 'co-forbidden-'));
  try {
    writeFileSync(join(dir, '.env'), 'SECRET=1\n');
    assert.deepEqual(detectForbiddenPaths(dir, ['.env']), ['.env']);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('bottleneck and Claude proxy profiles are policy-gated', () => {
  assert.equal(assertBottleneckProfile({ session_id: 's', supervisor_session_id: 's', purpose: 'diagnostic_handoff', can_write: false, can_expand_authority: false }), true);
  assert.throws(() => assertBottleneckProfile({ session_id: 's', supervisor_session_id: 'other', purpose: 'diagnostic_handoff', can_write: false, can_expand_authority: false }), /同一监督会话/);
  assert.equal(assertClaudeProxyProfile({ package: 'pxpipe-proxy@0.9.0', policy_approved: true, credential_safe: true, measured: true, direct_fallback: true }), true);
  assert.throws(() => assertClaudeProxyProfile({ package: 'pxpipe-proxy@latest', policy_approved: true, credential_safe: true, measured: true, direct_fallback: true }), /未 pin/);
});

test('TypeScript policy allows absence and rejects unpinned version when present', () => {
  const dir = mkdtempSync(join(tmpdir(), 'co-ts-'));
  try {
    assert.equal(assertTypescriptPolicy(dir), true);
    writeFileSync(join(dir, 'package.json'), JSON.stringify({ devDependencies: { typescript: '^7.0.2' } }));
    assert.throws(() => assertTypescriptPolicy(dir), /pin/);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});
