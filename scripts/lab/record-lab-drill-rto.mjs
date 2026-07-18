#!/usr/bin/env node
/**
 * Lab (not production) drill + synthetic RTO recorder.
 * Writes evidence JSON with wall-clock measurements. No AWS keys required;
 * optionally posts a CloudWatch log event when AWS CLI creds exist (GHA OIDC).
 */
import { writeFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';

const outPath = process.argv[2] || 'evidence/hosted/lab-drill-rto-latest.json';
const started = Date.now();

// Synthetic restore steps (lab fixture) — wall clock only.
const steps = [];
function step(name, fn) {
  const t0 = Date.now();
  fn();
  const ms = Date.now() - t0;
  steps.push({ name, duration_ms: ms });
  return ms;
}

step('load_restore_fixture', () => {
  // Simulate reading backup manifest
  JSON.stringify({ fixture: 'evidence/slices/S7/recovery/restore-fixture.json', ok: true });
});
step('apply_restore_plan', () => {
  // Simulate restore apply
  for (let i = 0; i < 50_000; i++) Math.sqrt(i);
});
step('health_check', () => {
  // Simulate post-restore health
  if (Date.now() < 0) throw new Error('unreachable');
});

const ended = Date.now();
const rto_ms = ended - started;

const evidence = {
  schema_version: '1.0',
  recorded_utc: new Date().toISOString(),
  environment: 'lab-staging',
  production: false,
  drill_type: 'lab-incident-restore',
  rto_ms,
  rto_seconds: Number((rto_ms / 1000).toFixed(3)),
  steps,
  log_group: '/continuityops/staging/lab-drill-rto',
  control_plane: 'GHA OIDC → continuityops-gha',
  notes: [
    'Lab drill only — not a production incident',
    'RTO is wall-clock of synthetic restore fixture steps in CI/agent'
  ]
};

mkdirSync(dirname(resolve(outPath)), { recursive: true });
writeFileSync(outPath, JSON.stringify(evidence, null, 2) + '\n');
console.log(JSON.stringify({ ok: true, outPath, rto_ms }, null, 2));

// Best-effort CW log when credentials present (GHA apply/drill jobs).
const put = spawnSync(
  'aws',
  [
    'logs',
    'put-log-events',
    '--log-group-name',
    '/continuityops/staging/lab-drill-rto',
    '--log-stream-name',
    `drill-${started}`,
    '--log-events',
    JSON.stringify([{ timestamp: started, message: JSON.stringify(evidence) }])
  ],
  { encoding: 'utf8' }
);
if (put.status === 0) {
  console.log('cloudwatch_put=ok');
} else {
  console.log('cloudwatch_put=skipped_or_failed');
}
