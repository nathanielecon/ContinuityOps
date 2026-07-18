import test from 'node:test';
import assert from 'node:assert/strict';
import { IdempotencyStore, processWithIdempotency } from '../../serverless/idempotency.mjs';

test('idempotency skips duplicate event_id', () => {
  const store = new IdempotencyStore();
  const event = {
    event_id: 'evt-1',
    tenant_id: 't1',
    type: 'order.created',
    payload: {},
    occurred_at: '2026-07-18T00:00:00Z'
  };
  let calls = 0;
  const handler = () => {
    calls += 1;
    return { ok: true };
  };
  const first = processWithIdempotency(store, event, handler);
  const second = processWithIdempotency(store, event, handler);
  assert.equal(first.status, 'processed');
  assert.equal(second.status, 'duplicate_skipped');
  assert.equal(calls, 1);
});

test('missing event_id fails closed', () => {
  const store = new IdempotencyStore();
  assert.throws(() => processWithIdempotency(store, {}, () => ({})), /event_id required/);
});
