#!/usr/bin/env node
/**
 * kind preflight gate. Labels environment local-only.
 * If kind is unavailable, emits L1 template evidence (not L2 runtime).
 */
import { writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

function toolAvailable(bin) {
  try {
    execFileSync(bin, ['version'], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
    return true;
  } catch {
    try {
      execFileSync(bin, ['--help'], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
      return true;
    } catch {
      return false;
    }
  }
}

const kindOk = toolAvailable('kind');
const helmOk = toolAvailable('helm');
const outDir = resolve(ROOT, 'evidence/slices/S2/runtime');
mkdirSync(outDir, { recursive: true });

const scenario = existsSync(resolve(ROOT, 'kubernetes/scenarios/kind-local.json'));
const claim_level = kindOk && helmOk ? 'L2' : 'L1';
const payload = {
  schema_version: '1.0',
  label: 'local-only',
  environment: 'local',
  kind_available: kindOk,
  helm_available: helmOk,
  scenario_present: scenario,
  claim_level,
  remaining_boundaries: ['managed_cluster_apply', 'No OIDC EKS apply executed'],
  note: kindOk
    ? 'kind available — operator may run local preflight for L2'
    : 'kind/helm absent — L1 template contract only'
};

writeFileSync(resolve(outDir, 'kind-preflight.json'), `${JSON.stringify(payload, null, 2)}\n`);
console.log(JSON.stringify(payload, null, 2));
process.exit(0);
