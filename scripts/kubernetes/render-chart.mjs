#!/usr/bin/env node
/**
 * Static chart contract check when helm is unavailable.
 * Verifies required template files and digest-pin shape in values.yaml.
 */
import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const required = [
  'kubernetes/chart/Chart.yaml',
  'kubernetes/chart/values.yaml',
  'kubernetes/chart/templates/deployment.yaml',
  'kubernetes/chart/templates/service.yaml',
  'kubernetes/chart/templates/hpa.yaml',
  'kubernetes/chart/templates/pdb.yaml',
  'kubernetes/chart/templates/rbac.yaml',
  'kubernetes/chart/templates/networkpolicy.yaml',
  'kubernetes/chart/templates/ingress.yaml',
  'kubernetes/chart/templates/serviceaccount.yaml'
];

const missing = required.filter((rel) => !existsSync(resolve(ROOT, rel)));
if (missing.length) {
  console.error(JSON.stringify({ ok: false, missing }));
  process.exit(1);
}

const values = readFileSync(resolve(ROOT, 'kubernetes/chart/values.yaml'), 'utf8');
if (!/digest:\s*"sha256:[0-9a-f]{64}"/.test(values)) {
  console.error(JSON.stringify({ ok: false, error: 'digest pin missing or invalid' }));
  process.exit(1);
}
const helpers = readFileSync(resolve(ROOT, 'kubernetes/chart/templates/_helpers.tpl'), 'utf8');
if (!helpers.includes('repository') || !helpers.includes('digest')) {
  console.error(JSON.stringify({ ok: false, error: 'image helper must use digest' }));
  process.exit(1);
}

console.log(JSON.stringify({ ok: true, files: required.length, digest_pin: true }));
