import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

test('signal-path drill is synthetic with full hop coverage', () => {
  const drill = JSON.parse(
    readFileSync(resolve(ROOT, 'operations/incidents/observability/signal-path-drill.json'), 'utf8')
  );
  assert.equal(drill.synthetic, true);
  assert.equal(drill.claim_ceiling, 'L1');
  const hops = drill.path.map((p) => p.hop);
  assert.deepEqual(hops, ['ingress', 'app', 'queue', 'function']);
  assert.ok(drill.fixture_events.length >= 2);
  assert.ok(drill.remaining_boundaries.some((b) => /Synthetic/i.test(b) || /live/i.test(b)));

  const telemetry = JSON.parse(readFileSync(resolve(ROOT, 'observability/otel/telemetry-contract.json'), 'utf8'));
  for (const hop of hops) {
    assert.ok(telemetry.correlation.propagated_across.includes(hop));
  }
  const spans = JSON.parse(readFileSync(resolve(ROOT, 'app-contract/telemetry/spans.json'), 'utf8'));
  for (const step of drill.path) {
    assert.ok(spans.spans.some((s) => s.name === step.trace_span));
  }
});
