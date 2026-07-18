import test from 'node:test';
import assert from 'node:assert/strict';
import { errorBudget, burnRate, remainingBudget } from '../../operations/slo/error-budget.mjs';

test('error budget math for 99.9% / 30d window', () => {
  const windowRequests = 1_000_000;
  const budget = errorBudget(0.999, windowRequests);
  assert.equal(Math.round(budget.budget_failures), 1000);
  const remaining = remainingBudget({ objective: 0.999, windowRequests, failuresToDate: 200 });
  assert.equal(Math.round(remaining.remaining), 800);
  assert.equal(remaining.exhausted, false);
});

test('burn rate detects fast burn', () => {
  // 1h is 1/720 of 30d; budget 1000 => allowed in 1h ≈ 1.388
  const rate = burnRate({
    objective: 0.999,
    windowRequests: 1_000_000,
    failuresInShortWindow: 20,
    shortWindowFractionOfLong: 1 / 720
  });
  assert.ok(rate > 14);
});
