#!/usr/bin/env node
import { mkdirSync, writeFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const kind = process.argv[2] || 'unknown';
const outDir = resolve(ROOT, 'evidence/_bundle');
mkdirSync(outDir, { recursive: true });
const payload = {
  schema_version: '1.0',
  stub: true,
  kind,
  recorded_at: new Date().toISOString(),
  claim_level: 'L1',
  note: 'Hosted stub only — not proof of OIDC plan/apply success'
};
writeFileSync(resolve(outDir, `${kind}-stub.json`), `${JSON.stringify(payload, null, 2)}\n`);
console.log(JSON.stringify(payload, null, 2));
