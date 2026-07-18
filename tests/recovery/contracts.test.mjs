import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

test('backup/rollback contracts and synthetic restore fixture', async () => {
  const backup = JSON.parse(readFileSync(resolve(ROOT, 'operations/recovery/backup-contract.json'), 'utf8'));
  assert.ok(backup.rto_minutes_target > 0);
  assert.equal(backup.isolated_restore_required, true);
  const rollbackMod = await import(pathToFileURL(resolve(ROOT, 'scripts/recovery/rollback-check.mjs')).href);
  assert.equal(rollbackMod.assertRollbackTarget({ knownGoodDigest: null, firstReleaseDecision: null }).allow, false);
  assert.equal(rollbackMod.assertRollbackTarget({ knownGoodDigest: 'sha256:abc', requestedDigest: 'sha256:abc' }).allow, true);
  const fixture = JSON.parse(readFileSync(resolve(ROOT, 'evidence/slices/S7/recovery/restore-fixture.json'), 'utf8'));
  assert.equal(fixture.live_cloud, false);
  assert.equal(fixture.checks.digest.pass, true);
});

test('performance before/after improves p95 and errors', () => {
  const before = JSON.parse(readFileSync(resolve(ROOT, 'performance/baseline-before.json'), 'utf8'));
  const after = JSON.parse(readFileSync(resolve(ROOT, 'performance/baseline-after.json'), 'utf8'));
  assert.ok(after.p95_ms < before.p95_ms);
  assert.ok(after.error_rate < before.error_rate);
});

test('teardown inventory is dry-run only', async () => {
  const { reconcileTeardown } = await import(pathToFileURL(resolve(ROOT, 'scripts/teardown/reconcile.mjs')).href);
  const inventory = { live_teardown_executed: false, resources: [{ id: 'x' }] };
  const result = reconcileTeardown({ inventory, retainedEvidencePaths: ['evidence/slices/S7/cost/finops-evidence.json'] });
  assert.equal(result.live_teardown_executed, false);
  assert.throws(() => reconcileTeardown({ inventory: { live_teardown_executed: true }, retainedEvidencePaths: [] }));
});
