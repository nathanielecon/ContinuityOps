import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { StateStore } from '../../harness/lib/state.mjs';

function seed(overrides = {}) {
  return {
    schema_version: '1.0',
    plan_id: 'test',
    revision: 0,
    authorized_through_phase: 0,
    baseline_sha: 'abcdef0',
    tasks: [
      { id: 'P0-T01', phase: 0, slice: 'S0', title: 'a', state: 'planned', depends_on: [], write_scope: ['x/'] },
      { id: 'P0-T02', phase: 0, slice: 'S0', title: 'b', state: 'planned', depends_on: ['P0-T01'], write_scope: ['y/'] },
      { id: 'P1-T01', phase: 1, slice: 'S1', title: 'c', state: 'planned', depends_on: [], write_scope: ['z/'] },
    ],
    ...overrides,
  };
}

function freshStore() {
  const dir = mkdtempSync(join(tmpdir(), 'cops-'));
  const path = join(dir, 'tasks.json');
  writeFileSync(path, JSON.stringify(seed()));
  return new StateStore(path);
}

test('revision bumps on every mutation', () => {
  const s = freshStore();
  assert.equal(s.data.revision, 0);
  s.transition('P0-T01', 'ready');
  assert.equal(s.data.revision, 1);
});

test('stale expected revision is rejected (optimistic concurrency)', () => {
  const s = freshStore();
  s.transition('P0-T01', 'ready');
  assert.throws(() => s.transition('P0-T01', 'running', { expectedRevision: 0, stream: 'A' }), /stale revision/);
});

test('phase 1 task cannot become ready while authorized_through_phase=0', () => {
  const s = freshStore();
  assert.throws(() => s.transition('P1-T01', 'ready'), /not authorized/);
});

test('authorizing phase 1 lets the phase-1 task become ready; monotonic', () => {
  const s = freshStore();
  s.authorizePhase(1);
  assert.ok(s.transition('P1-T01', 'ready'));
  assert.throws(() => s.authorizePhase(0), /monotonic/);
});

test('authorizePhase rejects non-integer / NaN (no state bricking)', () => {
  // regression: authorize-phase abc -> Number('abc')=NaN slipped past the guard.
  const s = freshStore();
  assert.throws(() => s.authorizePhase(NaN), /non-negative integer/);
  assert.throws(() => s.authorizePhase(1.5), /non-negative integer/);
  assert.throws(() => s.authorizePhase(-1), /non-negative integer/);
  assert.equal(s.data.authorized_through_phase, 0, 'state untouched after rejected authorize');
});

test('dependency must be verified before dependent becomes ready', () => {
  const s = freshStore();
  assert.throws(() => s.transition('P0-T02', 'ready'), /dependencies not satisfied/);
});

test('running transition re-checks phase authorization (defense in depth)', () => {
  // Seed a phase-1 task straight into 'blocked' with auth=0, then try running.
  const s = freshStore();
  s.data.tasks.find((t) => t.id === 'P1-T01').state = 'blocked';
  s.data.tasks.find((t) => t.id === 'P1-T01').stream = 'A';
  assert.throws(() => s.transition('P1-T01', 'running', { stream: 'A' }), /not authorized/);
});
