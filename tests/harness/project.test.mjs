import test from 'node:test';
import assert from 'node:assert/strict';
import {
  ContractError,
  appendStreamMutation,
  assertPhaseAuthorized,
  createStreamState,
  enqueueIntegration,
  transitionTask
} from '../../scripts/project.mjs';

const plan = {
  revision: 8,
  authorized_through_phase: 0,
  tasks: [
    { id: 'P0-T02', phase: 0, state: 'ready', write_scope: ['scripts/project*'], evidence: ['evidence/slices/S0/harness.json'] },
    { id: 'P1-T01', phase: 1, state: 'planned', write_scope: [], evidence: [] }
  ]
};

test('state transitions require a matching revision and legal lifecycle edge', () => {
  const next = transitionTask(plan, { taskId: 'P0-T02', fromRevision: 8, toState: 'running', actorRole: 'worker' });
  assert.equal(next.revision, 9);
  assert.equal(next.tasks.find((task) => task.id === 'P0-T02').state, 'running');
  assert.throws(() => transitionTask(next, { taskId: 'P0-T02', fromRevision: 8, toState: 'blocked', actorRole: 'worker' }), /revision 不匹配/);
  assert.throws(() => transitionTask(plan, { taskId: 'P0-T02', fromRevision: 8, toState: 'done', actorRole: 'orchestrator' }), /非法生命周期迁移/);
});

test('authorization boundary accepts current phase and rejects next phase', () => {
  assert.equal(assertPhaseAuthorized(plan, 'P0-T02').phase, 0);
  assert.throws(() => assertPhaseAuthorized(plan, 'P1-T01'), (error) => error instanceof ContractError && error.code === 'phase_unauthorized');
  const open = { ...plan, authorized_through_phase: 8 };
  assert.equal(assertPhaseAuthorized(open, 'P1-T01').phase, 1);
  const beyond = {
    ...open,
    tasks: [...open.tasks, { id: 'P99-T01', phase: 9, state: 'planned', write_scope: [], evidence: [] }]
  };
  assert.throws(() => assertPhaseAuthorized(beyond, 'P99-T01'), (error) => error instanceof ContractError && error.code === 'phase_unauthorized');
});

test('workers cannot mark verified or done', () => {
  const reviewPlan = { ...plan, tasks: plan.tasks.map((task) => task.id === 'P0-T02' ? { ...task, state: 'review' } : task) };
  assert.throws(() => transitionTask(reviewPlan, { taskId: 'P0-T02', fromRevision: 8, toState: 'verified', actorRole: 'worker' }), /worker 不能写入/);
});

test('up to three disjoint streams are isolated and sequential internally', () => {
  const state = createStreamState([
    { id: 'a', owner: 'owner-a', writeScope: ['scripts/project.mjs'] },
    { id: 'b', owner: 'owner-b', writeScope: ['tests/harness'] },
    { id: 'c', owner: 'owner-c', writeScope: ['evidence/slices/S0'] }
  ]);
  const updated = appendStreamMutation(appendStreamMutation(state, 'a', { candidateSha: 'a'.repeat(40) }), 'a', { candidateSha: 'b'.repeat(40) });
  assert.deepEqual(updated.streams.find((stream) => stream.id === 'a').sequence.map((entry) => entry.order), [1, 2]);
  assert.throws(() => createStreamState([...state.streams, { id: 'd', owner: 'owner-d', writeScope: ['docs'] }]), /不能超过三条/);
  assert.throws(() => createStreamState([{ id: 'a', owner: 'a', writeScope: ['scripts'] }, { id: 'b', owner: 'b', writeScope: ['scripts/project.mjs'] }]), /写范围重叠/);
});

test('integration queue serializes candidate merges', () => {
  const queue = enqueueIntegration(enqueueIntegration([], { streamId: 'a', candidateSha: 'a'.repeat(40), evidence: 'evidence/a.json' }), { streamId: 'b', candidateSha: 'b'.repeat(40), evidence: 'evidence/b.json' });
  assert.deepEqual(queue.map((entry) => entry.order), [1, 2]);
  assert.equal(queue[1].streamId, 'b');
});
