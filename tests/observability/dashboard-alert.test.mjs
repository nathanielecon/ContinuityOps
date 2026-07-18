import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

function assertRequired(obj, required) {
  for (const key of required) {
    assert.ok(obj[key] !== undefined, `missing ${key}`);
  }
}

test('dashboard matches schema required fields', () => {
  const schema = JSON.parse(readFileSync(resolve(ROOT, 'observability/dashboards/schema.json'), 'utf8'));
  const dash = JSON.parse(readFileSync(resolve(ROOT, 'observability/dashboards/service-overview.json'), 'utf8'));
  assertRequired(dash, schema.required);
  assert.ok(dash.panels.length >= 1);
  assert.ok(dash.links?.some((l) => l.purpose === 'symptom-to-root-cause'));
});

test('alert matches schema and links runbook', () => {
  const schema = JSON.parse(readFileSync(resolve(ROOT, 'observability/alerts/schema.json'), 'utf8'));
  const alert = JSON.parse(readFileSync(resolve(ROOT, 'observability/alerts/burn-rate.json'), 'utf8'));
  assertRequired(alert, schema.required);
  assert.ok(alert.runbook.includes('signal-path-drill'));
  assert.ok(alert.negative_tests?.missing_signal);
  assert.ok(alert.negative_tests?.noisy_flap);
});
