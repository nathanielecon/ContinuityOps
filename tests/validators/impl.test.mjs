import { test } from 'node:test';
import assert from 'node:assert/strict';
import { scopeCheck, looksSimplifiedChinese } from '../../harness/lib/validators/impl.mjs';
import { runValidator } from '../../harness/lib/validators/registry.mjs';
import { EvidenceLog } from '../../harness/lib/evidence.mjs';
import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

test('scope check flags path escapes', () => {
  const ok = scopeCheck(['harness/lib/a.mjs'], ['harness/']);
  assert.equal(ok.ok, true);
  const bad = scopeCheck(['terraform/main.tf'], ['harness/']);
  assert.equal(bad.ok, false);
  assert.deepEqual(bad.escapes, ['terraform/main.tf']);
});

test('simplified-chinese heuristic', () => {
  assert.ok(looksSimplifiedChinese('已完成任务并通过校验'));
  assert.equal(looksSimplifiedChinese('all done and validated'), false);
});

test('model_routing rejects an uninvokable claimed engine', async () => {
  const bad = await runValidator('model_routing', { producedBy: { role: 'worker', model_id: 'codex-5.4-cli' } });
  assert.equal(bad.ok, false);
  const good = await runValidator('model_routing', { producedBy: { role: 'worker', model_id: 'claude-opus-4-8' } });
  assert.equal(good.ok, true);
  const simMarked = await runValidator('model_routing', { producedBy: { role: 'worker', model_id: 'codex-5.4-sim' } });
  assert.equal(simMarked.ok, true);
});

test('worker_language validator wants zh-CN handoff', async () => {
  const bad = await runValidator('worker_language', { handoff: { summary_zh: 'done' } });
  assert.equal(bad.ok, false);
  const good = await runValidator('worker_language', { handoff: { summary_zh: '实现完成，全部校验通过' } });
  assert.equal(good.ok, true);
});

test('evidence append requires an actual model id and is append-only', () => {
  const dir = mkdtempSync(join(tmpdir(), 'cops-ev-'));
  const log = new EvidenceLog(join(dir, 'ev.json'));
  assert.throws(() => log.append({ task_id: 'P0-T01', candidate_sha: 'x', result: 'pass' }), /actual producing model_id/i);
  const e = log.append({ task_id: 'P0-T01', candidate_sha: 'x', result: 'pass', produced_by: { role: 'adapter', model_id: 'claude-opus-4-8' } });
  assert.equal(e.recorded_at_index, 0);
  assert.ok(e.artifact_sha256);
  const e2 = log.append({ task_id: 'P0-T01', candidate_sha: 'y', result: 'pass', supersedes: e.event_id, produced_by: { role: 'adapter', model_id: 'claude-opus-4-8' } });
  assert.equal(e2.recorded_at_index, 1);
  assert.equal(log.events.length, 2, 'prior event preserved, not overwritten');
});

test('worker cannot forge adapter evidence', () => {
  assert.throws(
    () => EvidenceLog.assertNotForged({ produced_by: { role: 'adapter', model_id: 'x' } }, 'worker'),
    /forge/,
  );
});
