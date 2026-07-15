// Concurrent-but-disjoint Ralphy stream isolation and the serialized
// integration queue (MASTER_PLAN.md section 6, RALPHY_ORCHESTRATION.md section 3).
//
//  - up to `maxStreams` streams may run at once (default 3);
//  - each stream is sequential internally: at most one non-terminal task
//    per stream is active;
//  - two live streams may never own overlapping write paths;
//  - merges are serialized through a single integration queue.

export const MAX_STREAMS = 3;
const ACTIVE = new Set(['ready', 'running', 'blocked', 'review']);

/** Normalize a write-scope glob list to comparable prefixes. */
function scopePrefixes(task) {
  return (task.write_scope || []).map((p) => p.replace(/\*+$/, ''));
}

/** True if two prefix lists share any overlapping path root. */
export function scopesOverlap(aPrefixes, bPrefixes) {
  for (const a of aPrefixes) {
    for (const b of bPrefixes) {
      if (a.startsWith(b) || b.startsWith(a)) return true;
    }
  }
  return false;
}

/**
 * Validate that assigning `task` to `stream` keeps all invariants.
 * Returns { ok: true } or { ok: false, reason }.
 */
export function canActivateInStream(task, stream, allTasks, maxStreams = MAX_STREAMS) {
  const live = allTasks.filter((t) => ACTIVE.has(t.state) && t.id !== task.id);

  // sequential within a stream
  const sameStreamActive = live.filter((t) => t.stream === stream);
  if (sameStreamActive.length > 0) {
    return { ok: false, reason: `stream ${stream} already has an active task (${sameStreamActive[0].id}); streams are sequential` };
  }

  // stream-count ceiling
  const liveStreams = new Set(live.map((t) => t.stream).filter(Boolean));
  if (!liveStreams.has(stream) && liveStreams.size >= maxStreams) {
    return { ok: false, reason: `max ${maxStreams} concurrent streams already active` };
  }

  // disjoint write scopes across live streams
  const mine = scopePrefixes(task);
  for (const other of live) {
    if (other.stream === stream) continue;
    if (scopesOverlap(mine, scopePrefixes(other))) {
      return { ok: false, reason: `write scope overlaps live task ${other.id} in stream ${other.stream}` };
    }
  }
  return { ok: true };
}

/**
 * Integration queue: a completed stream cannot merge itself; the lead
 * orchestrator dequeues one candidate at a time in FIFO order.
 */
export class IntegrationQueue {
  constructor() {
    this._q = [];
  }
  enqueue(candidate) {
    // candidate: { task_id, stream, candidate_sha }
    this._q.push({ ...candidate });
  }
  /** Merge is serialized: only the head may be dequeued. */
  dequeue() {
    return this._q.shift() || null;
  }
  get length() {
    return this._q.length;
  }
  peek() {
    return this._q[0] || null;
  }
}
