import { test } from 'node:test';
import assert from 'node:assert/strict';
import { canActivateInStream, scopesOverlap, IntegrationQueue } from '../../harness/lib/streams.mjs';

const mk = (id, state, stream, scope) => ({ id, state, stream, write_scope: scope });

test('scope overlap detection', () => {
  assert.ok(scopesOverlap(['terraform/'], ['terraform/modules/']));
  assert.equal(scopesOverlap(['terraform/'], ['kubernetes/']), false);
});

test('a stream is sequential internally', () => {
  const all = [mk('T1', 'running', 'A', ['a/']), mk('T2', 'ready', 'A', ['b/'])];
  const res = canActivateInStream(all[1], 'A', all);
  assert.equal(res.ok, false);
  assert.match(res.reason, /sequential/);
});

test('max three concurrent streams', () => {
  const all = [
    mk('T1', 'running', 'A', ['a/']),
    mk('T2', 'running', 'B', ['b/']),
    mk('T3', 'running', 'C', ['c/']),
  ];
  const incoming = mk('T4', 'ready', 'D', ['d/']);
  const res = canActivateInStream(incoming, 'D', [...all, incoming]);
  assert.equal(res.ok, false);
  assert.match(res.reason, /max 3/);
});

test('overlapping write scopes across streams are rejected', () => {
  const all = [mk('T1', 'running', 'A', ['terraform/'])];
  const incoming = mk('T2', 'ready', 'B', ['terraform/modules/']);
  const res = canActivateInStream(incoming, 'B', [...all, incoming]);
  assert.equal(res.ok, false);
  assert.match(res.reason, /overlaps/);
});

test('disjoint streams activate fine', () => {
  const all = [mk('T1', 'running', 'A', ['terraform/'])];
  const incoming = mk('T2', 'ready', 'B', ['kubernetes/']);
  assert.ok(canActivateInStream(incoming, 'B', [...all, incoming]).ok);
});

test('integration queue is FIFO and serialized', () => {
  const q = new IntegrationQueue();
  q.enqueue({ task_id: 'T1', stream: 'A', candidate_sha: 'aaa' });
  q.enqueue({ task_id: 'T2', stream: 'B', candidate_sha: 'bbb' });
  assert.equal(q.length, 2);
  assert.equal(q.dequeue().task_id, 'T1');
  assert.equal(q.dequeue().task_id, 'T2');
  assert.equal(q.dequeue(), null);
});
