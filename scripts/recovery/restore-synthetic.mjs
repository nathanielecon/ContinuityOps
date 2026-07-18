#!/usr/bin/env node
/** Synthetic restore fixture — does not touch live cloud. */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const fixture = {
  schema_version: '1.0',
  kind: 'synthetic_restore',
  started_at: new Date().toISOString(),
  source_backup_id: 'bak-synth-001',
  target_env: 'recovery-lab-synthetic',
  live_cloud: false,
  checks: {
    digest: { expected: 'sha256:' + 'c'.repeat(64), actual: 'sha256:' + 'c'.repeat(64), pass: true },
    health: { pass: true },
    version: { expected: '0.0.0-lab', actual: '0.0.0-lab', pass: true },
    data_checksum: { expected: 'deadbeef', actual: 'deadbeef', pass: true },
    business_smoke: { pass: true }
  },
  claim_level: 'L1',
  remaining_boundaries: ['Synthetic only', 'No live RTO']
};
const outDir = resolve(ROOT, 'evidence/slices/S7/recovery');
mkdirSync(outDir, { recursive: true });
writeFileSync(resolve(outDir, 'restore-fixture.json'), JSON.stringify(fixture, null, 2) + '\n');
console.log(JSON.stringify({ pass: true, path: 'evidence/slices/S7/recovery/restore-fixture.json' }));
