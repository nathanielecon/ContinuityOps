import { test } from 'node:test';
import assert from 'node:assert/strict';
import { register, runValidator, runAll, isRegistered } from '../../harness/lib/validators/registry.mjs';

test('unknown validator id fails closed', async () => {
  const r = await runValidator('does_not_exist', {});
  assert.equal(r.ok, false);
  assert.equal(r.fail_closed, true);
});

test('mutating validators are rejected at registration', () => {
  assert.throws(() => register('bad_mutator', async () => ({ ok: true }), { mutates: true }), /check-only/);
});

test('a registered validator runs and reports findings', async () => {
  register('always_fail_demo', async () => ({ ok: false, findings: ['nope'] }));
  assert.ok(isRegistered('always_fail_demo'));
  const r = await runValidator('always_fail_demo', {});
  assert.equal(r.ok, false);
  assert.deepEqual(r.findings, ['nope']);
});

test('runAll is all-or-nothing', async () => {
  register('ok_demo', async () => ({ ok: true }));
  const good = await runAll(['ok_demo'], {});
  assert.equal(good.ok, true);
  const bad = await runAll(['ok_demo', 'unknown_x'], {});
  assert.equal(bad.ok, false);
});

test('a throwing validator is caught and reported as fail', async () => {
  register('thrower_demo', async () => { throw new Error('boom'); });
  const r = await runValidator('thrower_demo', {});
  assert.equal(r.ok, false);
  assert.match(r.findings[0], /boom/);
});
