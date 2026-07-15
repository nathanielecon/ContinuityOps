// Append-only, SHA-bound evidence adapter. Only the adapter writes evidence.
// Events are never rewritten in place: a correction appends a new event that
// `supersedes` the prior one (RALPHY_ORCHESTRATION.md section 14). Every event
// records the ACTUAL producing model id, not an aspirational one.

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname } from 'node:path';
import { hashJson } from './hashing.mjs';

export class EvidenceLog {
  constructor(path) {
    this.path = path;
    this.events = existsSync(path) ? JSON.parse(readFileSync(path, 'utf8')) : [];
  }

  _persist() {
    if (!existsSync(dirname(this.path))) mkdirSync(dirname(this.path), { recursive: true });
    writeFileSync(this.path, JSON.stringify(this.events, null, 2) + '\n');
  }

  /**
   * Append one evidence event. Refuses to mutate existing events.
   * @param event partial event; event_id, artifact_sha256 and index are filled.
   * @param opts.actorRole  the real role of the caller ('adapter' | 'worker').
   *        A worker attempting to write an adapter-owned event is rejected here,
   *        so the anti-forgery guard is enforced on every append, not optionally.
   */
  append(event, opts = {}) {
    EvidenceLog.assertNotForged(event, opts.actorRole || 'adapter');
    if (!event.produced_by || !event.produced_by.model_id) {
      throw new Error('evidence event must record the ACTUAL producing model_id');
    }
    const index = this.events.length;
    const body = {
      task_id: event.task_id,
      candidate_sha: event.candidate_sha,
      produced_by: event.produced_by,
      validator_ids: event.validator_ids || [],
      result: event.result,
      supersedes: event.supersedes ?? null,
      notes_zh: event.notes_zh || '',
    };
    const full = {
      event_id: `${event.task_id}#${index}`,
      ...body,
      artifact_sha256: hashJson(body),
      recorded_at_index: index,
    };
    this.events.push(full);
    this._persist();
    return full;
  }

  /** A worker-produced payload can never forge an adapter event: reject if the
   *  claimed role is 'adapter' but the model role indicates a worker. */
  static assertNotForged(event, actualRole) {
    if (event.produced_by?.role === 'adapter' && actualRole === 'worker') {
      throw new Error('worker attempted to forge adapter-owned evidence');
    }
    return true;
  }
}
