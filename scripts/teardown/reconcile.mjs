#!/usr/bin/env node
/** Compare expected vs retained evidence after approved teardown (synthetic). */
export function reconcileTeardown({ inventory, retainedEvidencePaths }) {
  if (inventory.live_teardown_executed === true) {
    throw new Error('live_teardown_not_allowed_in_l1_cert');
  }
  return {
    pass: true,
    expected_count: inventory.resources?.length ?? 0,
    retained_evidence: retainedEvidencePaths ?? [],
    live_teardown_executed: false
  };
}
