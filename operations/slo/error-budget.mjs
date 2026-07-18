/**
 * Error budget / burn-rate math for unit tests (synthetic).
 */
export function errorBudget(objective, windowRequests) {
  if (!(objective > 0 && objective < 1)) throw new Error('objective must be in (0,1)');
  if (windowRequests < 1) throw new Error('windowRequests must be >= 1');
  const budget = (1 - objective) * windowRequests;
  return { budget_failures: budget, objective, windowRequests };
}

export function burnRate({ objective, windowRequests, failuresInShortWindow, shortWindowFractionOfLong }) {
  const { budget_failures } = errorBudget(objective, windowRequests);
  const allowedInShort = budget_failures * shortWindowFractionOfLong;
  if (allowedInShort <= 0) throw new Error('invalid short window fraction');
  return failuresInShortWindow / allowedInShort;
}

export function remainingBudget({ objective, windowRequests, failuresToDate }) {
  const { budget_failures } = errorBudget(objective, windowRequests);
  return {
    budget_failures,
    failures_to_date: failuresToDate,
    remaining: budget_failures - failuresToDate,
    exhausted: failuresToDate >= budget_failures
  };
}
