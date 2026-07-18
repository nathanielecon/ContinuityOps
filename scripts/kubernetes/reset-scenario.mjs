#!/usr/bin/env node
/**
 * Synthetic scenario reset recorder. Does not mutate a live cluster.
 * Records reset intent for evidence; live kubectl apply is out of scope without kind/EKS.
 */
import { writeFileSync, mkdirSync, existsSync, readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const scenarioId = process.argv[2];
if (!scenarioId) {
  console.error('Usage: node scripts/kubernetes/reset-scenario.mjs <scenario-id>');
  process.exit(2);
}

const scenarioPath = resolve(ROOT, `kubernetes/scenarios/${scenarioId}.json`);
if (!existsSync(scenarioPath)) {
  console.error(`Unknown scenario: ${scenarioId}`);
  process.exit(1);
}
const scenario = JSON.parse(readFileSync(scenarioPath, 'utf8'));
const outDir = resolve(ROOT, 'evidence/slices/S2/scenarios');
mkdirSync(outDir, { recursive: true });
const payload = {
  schema_version: '1.0',
  scenario_id: scenario.scenario_id,
  action: 'reset',
  synthetic: true,
  reset_at: new Date().toISOString(),
  recover: scenario.recover,
  business_check: scenario.business_check,
  note: 'Synthetic reset only; no live cluster mutation'
};
const outPath = resolve(outDir, `${scenarioId}-reset.json`);
writeFileSync(outPath, `${JSON.stringify(payload, null, 2)}\n`);
console.log(JSON.stringify({ ok: true, path: `evidence/slices/S2/scenarios/${scenarioId}-reset.json` }));
