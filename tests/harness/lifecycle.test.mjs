import { test } from 'node:test';
import assert from 'node:assert/strict';
import { isLegalTransition, assertTransition } from '../../harness/lib/lifecycle.mjs';

test('legal happy-path transitions', () => {
  assert.ok(isLegalTransition('planned', 'ready'));
  assert.ok(isLegalTransition('ready', 'running'));
  assert.ok(isLegalTransition('running', 'review'));
  assert.ok(isLegalTransition('review', 'verified'));
  assert.ok(isLegalTransition('verified', 'done'));
});

test('no task jumps straight to done', () => {
  assert.equal(isLegalTransition('review', 'done'), false);
  assert.equal(isLegalTransition('running', 'done'), false);
  assert.equal(isLegalTransition('planned', 'done'), false);
});

test('worker may not set verified or done', () => {
  assert.throws(() => assertTransition('review', 'verified', 'worker'), /adapter-only/);
  assert.throws(() => assertTransition('verified', 'done', 'worker'), /adapter-only/);
});

test('worker may recommend review or blocked', () => {
  assert.ok(assertTransition('running', 'review', 'worker'));
  assert.ok(assertTransition('running', 'blocked', 'worker'));
});

test('illegal transitions rejected regardless of actor', () => {
  assert.throws(() => assertTransition('planned', 'verified', 'adapter'), /illegal transition/);
});
