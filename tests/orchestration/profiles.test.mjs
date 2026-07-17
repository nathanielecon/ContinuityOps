import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

test('bottleneck profiles stay diagnostic and in-session', () => {
  const profiles = JSON.parse(readFileSync('scripts/orchestration/bottleneck-profiles.json', 'utf8'));
  assert.equal(profiles.session_scope, 'same_supervisory_session');
  assert.equal(profiles.permission_expansion, false);
  assert(profiles.profiles.every((profile) => profile.may_mutate === false));
});

test('Claude proxy profile is pinned and gated', () => {
  const profile = JSON.parse(readFileSync('scripts/orchestration/claude-proxy-profile.json', 'utf8'));
  assert.equal(profile.package, 'pxpipe-proxy@0.9.0');
  assert.equal(profile.policy_gate, true);
  assert.equal(profile.credential_safe, true);
  assert.equal(profile.metrics_required, true);
  assert.equal(profile.direct_fallback, true);
});
