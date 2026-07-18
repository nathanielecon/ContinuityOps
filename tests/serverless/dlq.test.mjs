import test from 'node:test';
import assert from 'node:assert/strict';
import { Dlq, isPoison } from '../../serverless/dlq.mjs';
import { createWorker } from '../../serverless/worker.mjs';
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const contract = JSON.parse(readFileSync(resolve(ROOT, 'serverless/event-contract.json'), 'utf8'));

test('poison / malformed events route toward DLQ', () => {
  assert.equal(isPoison({}, contract), true);
  assert.equal(isPoison({ event_id: 'e1' }, contract), true);
  const good = {
    event_id: 'e2',
    tenant_id: 't1',
    type: 'order.created',
    payload: {},
    occurred_at: '2026-07-18T00:00:00Z'
  };
  assert.equal(isPoison(good, contract), false);
});

test('max receive count enqueues DLQ and alarm', () => {
  const dlq = new Dlq({ maxReceiveCount: 3 });
  let msg = { id: 'm1', body: {} };
  for (let i = 0; i < 3; i += 1) {
    const r = dlq.receiveAttempt(msg);
    msg = r.message;
    assert.equal(r.action, 'retry');
  }
  const last = dlq.receiveAttempt(msg);
  assert.equal(last.action, 'dlq');
  assert.equal(dlq.alarms.length, 1);
});

test('DLQ replay requires approval', () => {
  const dlq = new Dlq({ maxReceiveCount: 1 });
  const { message } = dlq.receiveAttempt({ id: 'm2', receiveCount: 1 });
  assert.equal(dlq.messages.length, 1);
  assert.throws(() => dlq.replay('m2', { approved: false }), /approval/);
  const replayed = dlq.replay('m2', { approved: true });
  assert.equal(replayed.action, 'requeued');
  assert.equal(dlq.messages.length, 0);
  assert.ok(message);
});

test('worker handles duplicate and poison', () => {
  const worker = createWorker();
  const event = {
    event_id: 'evt-w1',
    tenant_id: 't1',
    type: 'order.created',
    payload: { n: 1 },
    occurred_at: '2026-07-18T00:00:00Z'
  };
  assert.equal(worker.handle(event).status, 'processed');
  assert.equal(worker.handle(event).status, 'duplicate_skipped');
  assert.equal(worker.handle({}).action, 'dlq');
});
