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

/**
 * Reduce a write-scope entry to its literal directory prefix: drop a leading
 * `./`, keep everything up to the first glob character, and collapse repeated
 * slashes. Reducing at the first glob is conservative — it errs toward
 * detecting overlap (blocking), which is the safe direction for isolation.
 */
export function normalizeScope(p) {
  let s = String(p).replace(/^\.\//, '');
  const star = s.indexOf('*');
  if (star !== -1) s = s.slice(0, star);
  return s.replace(/\/{2,}/g, '/');
}

/** Normalize a task's whole write-scope list. */
function scopePrefixes(task) {
  return (task.write_scope || []).map(normalizeScope);
}

/**
 * True when `prefix` contains `path` at a path-segment boundary — i.e. they are
 * equal, or `prefix` is an ancestor directory of `path`. Prevents `src/app`
 * from being treated as a prefix of `src/application`.
 */
export function isPrefixAtBoundary(prefix, path) {
  // An empty prefix means the scope reduced to a bare/leading glob (e.g. '*',
  // '**/*.md'), which is effectively repo-wide: it contains every path. Return
  // true so such a scope is detected as overlapping (the safe direction).
  if (prefix === '') return true;
  if (prefix === path) return true;
  if (!path.startsWith(prefix)) return false;
  return prefix.endsWith('/') || path[prefix.length] === '/';
}

/** True if any normalized scope in one list contains/equals one in the other. */
export function scopesOverlap(aPrefixes, bPrefixes) {
  const a = aPrefixes.map(normalizeScope);
  const b = bPrefixes.map(normalizeScope);
  for (const x of a) {
    for (const y of b) {
      if (isPrefixAtBoundary(x, y) || isPrefixAtBoundary(y, x)) return true;
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
