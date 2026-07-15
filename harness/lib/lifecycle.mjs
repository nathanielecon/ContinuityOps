// Legal task lifecycle for ContinuityOps.
//
//   planned -> ready -> running -> blocked | review -> verified -> done
//
// Rules encoded here (RALPHY_ORCHESTRATION.md section 5):
//  - a worker may only recommend `review` or `blocked`;
//  - only the adapter/orchestrator may set `verified` or `done`;
//  - no task jumps straight to `done`.

export const STATES = ['planned', 'ready', 'running', 'blocked', 'review', 'verified', 'done'];

const LEGAL = {
  planned: ['ready'],
  ready: ['running'],
  running: ['blocked', 'review'],
  blocked: ['ready', 'running'],
  review: ['verified', 'blocked'],
  verified: ['done', 'review'],
  done: [],
};

/** States a *worker* is ever allowed to recommend. */
export const WORKER_RECOMMENDABLE = new Set(['review', 'blocked']);

/** States only the adapter/orchestrator may apply. */
export const ADAPTER_ONLY = new Set(['verified', 'done']);

export function isLegalTransition(from, to) {
  if (!STATES.includes(from) || !STATES.includes(to)) return false;
  return (LEGAL[from] || []).includes(to);
}

/**
 * Guard a transition. `actor` is 'worker' or 'adapter'.
 * Throws a descriptive Error when illegal; returns true when allowed.
 */
export function assertTransition(from, to, actor) {
  if (!isLegalTransition(from, to)) {
    throw new Error(`illegal transition ${from} -> ${to}`);
  }
  if (actor === 'worker' && !WORKER_RECOMMENDABLE.has(to)) {
    // A worker may only ever recommend `review` or `blocked`. Every other
    // target (ready/running/verified/done) is an adapter/orchestrator action.
    throw new Error(`worker may only recommend review|blocked, not '${to}' (adapter-only)`);
  }
  return true;
}
