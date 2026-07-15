import { test } from 'node:test';
import assert from 'node:assert/strict';
import { scopeCheck, looksSimplifiedChinese, isBinaryPath, scanText } from '../../harness/lib/validators/impl.mjs';
import { verifyCoverage } from '../../harness/lib/partition.mjs';
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

test('svg/drawio are NOT treated as binary (still secret-scanned)', () => {
  // regression: .svg/.drawio were in the skiplist despite being text XML.
  assert.equal(isBinaryPath('docs/architecture/x.svg'), false);
  assert.equal(isBinaryPath('docs/architecture/x.drawio'), false);
  assert.equal(isBinaryPath('docs/architecture/x.png'), true);
  assert.equal(isBinaryPath('a/b/keys.p12'), true);
});

test('secret_scan catches DSA/PGP private-key blocks (not just RSA/EC)', () => {
  // regression: private-key regex only allowed RSA|EC|OPENSSH prefixes.
  // Build the PEM headers dynamically so the literal secret-shaped string does
  // NOT sit in this tracked file (which would make secret_scan flag the test).
  const dashes = '-'.repeat(5);
  const pem = (kind, block) => `${dashes}BEGIN ${kind ? kind + ' ' : ''}PRIVATE KEY${block ? ' BLOCK' : ''}${dashes}`;
  assert.deepEqual(scanText(pem('DSA')), ['private key block']);
  assert.deepEqual(scanText(pem('PGP', true)), ['private key block']);
  assert.deepEqual(scanText(pem()), ['private key block']); // PKCS8 bare
  assert.deepEqual(scanText('nothing secret here'), []);
});

test('verifyCoverage flags an unowned code file', () => {
  // regression: partition_unique_ownership only detected duplicates, not gaps.
  const manifest = { slices: [{ id: 'S', paths: ['a.mjs', 'b.mjs'] }] };
  assert.equal(verifyCoverage(manifest, ['a.mjs', 'b.mjs']).ok, true);
  const gap = verifyCoverage(manifest, ['a.mjs', 'b.mjs', 'orphan.mjs']);
  assert.equal(gap.ok, false);
  assert.deepEqual(gap.unowned, ['orphan.mjs']);
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
  // regression: incidental substring 'sim' inside 'assimilate' must NOT pass.
  const sneaky = await runValidator('model_routing', { producedBy: { role: 'worker', model_id: 'grok-assimilate' } });
  assert.equal(sneaky.ok, false);
});

test('upstream_pin_schema rejects unresolved image_digest placeholder', async () => {
  const dir = mkdtempSync(join(tmpdir(), 'cops-pin-'));
  // Build two temp repos with an integration/ lock each.
  const { writeFileSync, mkdirSync } = await import('node:fs');
  const bad = join(dir, 'bad');
  mkdirSync(join(bad, 'integration'), { recursive: true });
  writeFileSync(join(bad, 'integration/upstreams.lock.json'), JSON.stringify({
    project_a: { repository: 'r/a', commit_sha: 'a'.repeat(40) },
    project_c: { repository: 'r/c', commit_sha: 'c'.repeat(40), image_digest: 'REQUIRED_OR_EXPLICITLY_UNAVAILABLE' },
  }));
  const rBad = await runValidator('upstream_pin_schema', { repoRoot: bad });
  assert.equal(rBad.ok, false);

  const good = join(dir, 'good');
  mkdirSync(join(good, 'integration'), { recursive: true });
  writeFileSync(join(good, 'integration/upstreams.lock.json'), JSON.stringify({
    project_a: { repository: 'r/a', commit_sha: 'a'.repeat(40) },
    project_c: { repository: 'r/c', commit_sha: 'c'.repeat(40), image_digest: 'UNAVAILABLE' },
  }));
  const rGood = await runValidator('upstream_pin_schema', { repoRoot: good });
  assert.equal(rGood.ok, true);
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

test('append() itself blocks a worker forging an adapter event', () => {
  // regression: assertNotForged was never called inside append().
  const dir = mkdtempSync(join(tmpdir(), 'cops-forge-'));
  const log = new EvidenceLog(join(dir, 'ev.json'));
  assert.throws(
    () => log.append(
      { task_id: 'T', candidate_sha: 'x', result: 'pass', produced_by: { role: 'adapter', model_id: 'm' } },
      { actorRole: 'worker' },
    ),
    /forge/,
  );
  assert.equal(log.events.length, 0, 'forged event not persisted');
});

test('append() rejects an aspirational (uninvokable-engine) model id', () => {
  // regression: model_routing was not enforced at evidence write time.
  const dir = mkdtempSync(join(tmpdir(), 'cops-asp-'));
  const log = new EvidenceLog(join(dir, 'ev.json'));
  assert.throws(
    () => log.append({ task_id: 'T', candidate_sha: 'x', result: 'pass', produced_by: { role: 'adapter', model_id: 'codex-5.4-cli' } }),
    /uninvokable engine/,
  );
  // a real id, or one with a delimited sim marker, is accepted
  assert.ok(log.append({ task_id: 'T', candidate_sha: 'x', result: 'pass', produced_by: { role: 'adapter', model_id: 'claude-opus-4-8' } }));
  assert.ok(log.append({ task_id: 'T', candidate_sha: 'y', result: 'pass', produced_by: { role: 'adapter', model_id: 'codex-5.4-sim' } }));
});
