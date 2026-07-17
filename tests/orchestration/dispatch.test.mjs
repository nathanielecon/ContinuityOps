import test from 'node:test';
import assert from 'node:assert/strict';
import { createBottleneckDispatch } from '../../scripts/orchestration/bottleneck-dispatch.mjs';
import { recordModelRoute } from '../../scripts/orchestration/model-routing.mjs';

test('bottleneck dispatch stays in-session and diagnostic-only', () => {
  const dispatch = createBottleneckDispatch({ sessionId: 'supervisor-1', issueId: 'ISSUE-1', specialist: 'toolchain', failedCheck: 'node --test tests/' });
  assert.equal(dispatch.session_id, dispatch.supervisor_session_id);
  assert.equal(dispatch.can_write, false);
});

test('actual model route records provider, model, mode, and role', () => {
  const route = recordModelRoute({ provider: 'OpenAI', model: 'gpt-5.5', mode: 'default', role: 'validator-worker' });
  assert.equal(route.role, 'validator-worker');
  assert.ok(route.recorded_at);
  assert.throws(() => recordModelRoute({ provider: 'OpenAI', model: '', mode: 'default', role: 'worker' }), /requires/);
});
