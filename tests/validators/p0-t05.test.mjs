import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, writeFileSync, mkdirSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import {
  ValidationError,
  getValidator,
  createWorkerReplacement,
  assertStreamIsolationFixture,
  validateFullRepository,
  assertSavedFreshCouncil,
  assertFreshJudgeExit,
  P0_T05_VALIDATOR_IDS,
  runValidator
} from '../../scripts/validators/core.mjs';

test('P0-T05 validator IDs are registered and unknown IDs still fail closed', () => {
  for (const id of P0_T05_VALIDATOR_IDS) {
    assert.equal(typeof getValidator(id), 'function');
  }
  assert.throws(() => getValidator('not_a_real_validator'), (error) => error instanceof ValidationError && error.code === 'validator_unknown');
});

test('worker_replacement dispatches fresh Grok or same-session bottleneck', () => {
  const sessionId = 'sess-1';
  const grok = createWorkerReplacement({ sessionId, failedCheck: 'fail-a', mode: 'fresh_grok' });
  assert.equal(grok.kind, 'fresh_grok_worker');
  assert.equal(grok.session_id, sessionId);
  assert.equal(grok.model_record.model, 'cursor-grok-4.5-high');
  assert.equal(grok.model_record.provider, 'xAI');

  const bottleneck = createWorkerReplacement({ sessionId, failedCheck: 'fail-a', mode: 'bottleneck' });
  assert.equal(bottleneck.kind, 'bottleneck');
  assert.equal(bottleneck.session_id, sessionId);
  assert.equal(bottleneck.can_write, false);
  assert.equal(bottleneck.supervisor_session_id, sessionId);
  assert.throws(
    () => createWorkerReplacement({ sessionId, failedCheck: '', mode: 'fresh_grok' }),
    (error) => error instanceof ValidationError && error.code === 'worker_replacement_invalid'
  );
});

test('stream_isolation rejects overlapping scopes and broken sequences', () => {
  assert.equal(assertStreamIsolationFixture({
    streams: [
      { id: 'a', owner: 'oa', writeScope: ['scripts/a'], sequence: [{ order: 1 }, { order: 2 }] },
      { id: 'b', owner: 'ob', writeScope: ['tests/b'], sequence: [] },
      { id: 'c', owner: 'oc', writeScope: ['evidence/c'], sequence: [] }
    ]
  }), true);
  assert.throws(() => assertStreamIsolationFixture({
    streams: [
      { id: 'a', owner: 'oa', writeScope: ['scripts'], sequence: [] },
      { id: 'b', owner: 'ob', writeScope: ['scripts/x'], sequence: [] },
      { id: 'c', owner: 'oc', writeScope: ['evidence'], sequence: [] }
    ]
  }), /写范围重叠/);
  assert.throws(() => assertStreamIsolationFixture({
    streams: [
      { id: 'a', owner: 'oa', writeScope: ['scripts/a'], sequence: [{ order: 1 }, { order: 3 }] },
      { id: 'b', owner: 'ob', writeScope: ['tests/b'], sequence: [] },
      { id: 'c', owner: 'oc', writeScope: ['evidence/c'], sequence: [] }
    ]
  }), /内部顺序/);
});

test('full_repository parses standalone JSON and fenced json blocks', () => {
  const dir = mkdtempSync(join(tmpdir(), 'co-fullrepo-'));
  try {
    writeFileSync(join(dir, 'ok.json'), '{"a":1}\n');
    writeFileSync(join(dir, 'note.md'), '# t\n\n```json\n{"b":2}\n```\n');
    const result = validateFullRepository(dir);
    assert.equal(result.standalone_json, 1);
    assert.equal(result.fenced_json, 1);
    writeFileSync(join(dir, 'bad.json'), '{not-json');
    assert.throws(() => validateFullRepository(dir), /full_repository/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('saved_fresh_council rejects saved final certification and saved-score leakage', () => {
  const must = [{ id: 'M1', status: 'pass', evidence: ['e'] }];
  const dims = [{ id: 'd', score: 9.6, rationale: '理由', evidence: ['e'] }];
  const model = { provider: 'xAI', model: 'cursor-grok-4.5-high', mode: 'default', role: 'judge' };
  const base = {
    schema_version: '1.0',
    slice_id: 'S0',
    candidate_sha: 'a'.repeat(40),
    rubric_sha256: 'b'.repeat(64),
    evidence_manifest_sha256: 'c'.repeat(64),
    judge_model_id: 'cursor-grok-4.5-high',
    must_haves: must,
    blocking_findings: [],
    scored_dimensions: dims,
    unsupported_claims: [],
    security_findings: [],
    improvements: [],
    model_record: model
  };
  const saved = { ...base, round: 'saved_provisional', provisional_pass: true, overall_score: 9.6, merge_ready: 'provisional' };
  const fresh = [1, 2, 3].map((n) => ({
    ...base,
    round: 'fresh',
    judge_id: `j${n}`,
    overall_score: 9.6,
    merge_ready: 'yes',
    notes_zh: '独立评审'
  }));
  assert.equal(assertSavedFreshCouncil(saved, fresh).pass, true);
  assert.throws(() => assertSavedFreshCouncil({ ...saved, merge_ready: 'yes' }, fresh), /provisional/);
  assert.throws(() => assertFreshJudgeExit(fresh.map((j, i) => i === 0 ? { ...j, saved_scores: [1] } : j)), /saved/);
  assert.throws(() => assertFreshJudgeExit(fresh.map((j, i) => i === 0 ? { ...j, overall_score: 8.9 } : j)), /9\.0/);
});

test('worker_replacement and stream_isolation validators run via registry', () => {
  const streamState = {
    streams: [
      { id: 'a', owner: 'oa', writeScope: ['scripts/a'], sequence: [{ order: 1 }, { order: 2 }] },
      { id: 'b', owner: 'ob', writeScope: ['tests/b'], sequence: [] },
      { id: 'c', owner: 'oc', writeScope: ['evidence/c'], sequence: [] }
    ]
  };
  assert.equal(runValidator('stream_isolation', { streamState }).pass, true);
  assert.equal(runValidator('worker_replacement', { sessionId: 's', failedCheck: 'x' }).pass, true);
});
