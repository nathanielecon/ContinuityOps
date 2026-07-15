// Authoritative task-state store with atomic, revision-checked writes.
//
// The store is the single source of truth for task lifecycle. Every mutation
// bumps `revision`; a caller supplying a stale expected-revision is rejected
// (optimistic concurrency), so two orchestrator turns cannot silently clobber
// each other. Writes are atomic: serialize to a temp file, then rename.

import { readFileSync, writeFileSync, renameSync, existsSync } from 'node:fs';
import { assertTransition } from './lifecycle.mjs';
import { assertPhaseAuthorized, dependenciesSatisfied } from './authorization.mjs';
import { canActivateInStream } from './streams.mjs';

export class StateStore {
  constructor(path) {
    this.path = path;
    this.data = existsSync(path)
      ? JSON.parse(readFileSync(path, 'utf8'))
      : null;
  }

  static init(path, seed) {
    const store = new StateStore(path);
    store.data = seed;
    store._persist();
    return store;
  }

  _tasksById() {
    return new Map(this.data.tasks.map((t) => [t.id, t]));
  }

  task(id) {
    const t = this._tasksById().get(id);
    if (!t) throw new Error(`unknown task ${id}`);
    return t;
  }

  _persist() {
    // Unique temp name per write so concurrent writers cannot clobber a shared
    // temp file; rename is atomic on POSIX, so readers always see a whole file.
    const tmp = `${this.path}.${process.pid}.${(StateStore._seq = (StateStore._seq || 0) + 1)}.tmp`;
    writeFileSync(tmp, JSON.stringify(this.data, null, 2) + '\n');
    renameSync(tmp, this.path);
  }

  /**
   * Apply a state transition with full guard checks.
   * @param opts.expectedRevision  optimistic-concurrency guard
   * @param opts.actor  'worker' | 'adapter'
   */
  transition(id, toState, opts = {}) {
    const { expectedRevision, actor = 'adapter', stream } = opts;
    if (expectedRevision !== undefined && expectedRevision !== this.data.revision) {
      throw new Error(
        `stale revision: expected ${expectedRevision} but store is at ${this.data.revision}`,
      );
    }
    const task = this.task(id);
    const tasksById = this._tasksById();

    // Lifecycle legality + actor authority.
    assertTransition(task.state, toState, actor);

    // Activation guards apply when moving into `ready`/`running`.
    if (toState === 'ready') {
      assertPhaseAuthorized(task, this.data.authorized_through_phase);
      if (!dependenciesSatisfied(task, tasksById)) {
        throw new Error(`dependencies not satisfied for ${id}`);
      }
    }
    if (toState === 'running') {
      // Defense in depth: re-verify phase authorization on activation, so an
      // inconsistently-seeded blocked/running path cannot escape the gate.
      assertPhaseAuthorized(task, this.data.authorized_through_phase);
      const chosenStream = stream ?? task.stream;
      if (!chosenStream) throw new Error(`task ${id} needs a stream assignment to run`);
      const check = canActivateInStream({ ...task, stream: chosenStream }, chosenStream, this.data.tasks);
      if (!check.ok) throw new Error(`stream guard: ${check.reason}`);
      task.stream = chosenStream;
    }

    task.state = toState;
    this.data.revision += 1;
    this._persist();
    return { id, state: toState, revision: this.data.revision };
  }

  /** Raise authorized_through_phase — the human-gated, monotonic advance. */
  authorizePhase(newPhase, opts = {}) {
    const { expectedRevision } = opts;
    if (expectedRevision !== undefined && expectedRevision !== this.data.revision) {
      throw new Error(`stale revision: expected ${expectedRevision} but store is at ${this.data.revision}`);
    }
    if (newPhase < this.data.authorized_through_phase) {
      throw new Error('authorization is monotonic; cannot lower authorized_through_phase');
    }
    this.data.authorized_through_phase = newPhase;
    this.data.revision += 1;
    this._persist();
    return { authorized_through_phase: newPhase, revision: this.data.revision };
  }
}
