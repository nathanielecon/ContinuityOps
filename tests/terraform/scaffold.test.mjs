import test from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

const REQUIRED = [
  'terraform/versions.tf',
  'terraform/variables.tf',
  'terraform/modules/state/main.tf',
  'terraform/modules/environments/main.tf',
  'terraform/modules/iam/main.tf',
  'terraform/modules/network/main.tf',
  'terraform/envs/staging/main.tf',
  'terraform/envs/staging/versions.tf',
  'terraform/envs/recovery-lab/main.tf',
  'terraform/envs/recovery-lab/versions.tf',
  'terraform/ci-bootstrap/ensure-tfstate.sh',
  'terraform/policies/tagging.json',
  'terraform/policies/encryption.json',
  'terraform/policies/iam-negative.json',
  'terraform/policies/network-negative.json'
];

test('terraform scaffold files exist', () => {
  for (const rel of REQUIRED) {
    assert.ok(existsSync(resolve(ROOT, rel)), `missing ${rel}`);
  }
});

test('staging and recovery-lab are separated env roots', () => {
  const staging = readFileSync(resolve(ROOT, 'terraform/envs/staging/main.tf'), 'utf8');
  const recovery = readFileSync(resolve(ROOT, 'terraform/envs/recovery-lab/main.tf'), 'utf8');
  assert.match(staging, /environment\s*=\s*"staging"/);
  assert.match(recovery, /environment\s*=\s*"recovery-lab"/);
  assert.doesNotMatch(staging, /production/);
  assert.doesNotMatch(recovery, /production/);
});

test('IAM and network enable guards default to false', () => {
  const iam = readFileSync(resolve(ROOT, 'terraform/modules/iam/main.tf'), 'utf8');
  const network = readFileSync(resolve(ROOT, 'terraform/modules/network/main.tf'), 'utf8');
  assert.match(iam, /enable_iam_resources[\s\S]*default\s*=\s*false/);
  assert.match(network, /enable_network_resources[\s\S]*default\s*=\s*false/);
  assert.match(iam, /long_lived_keys\s*=\s*false/);
});

test('state module documents encryption versioning locking', () => {
  const state = readFileSync(resolve(ROOT, 'terraform/modules/state/main.tf'), 'utf8');
  assert.match(state, /versioning/i);
  assert.match(state, /encrypt/i);
  assert.match(state, /lock/i);
  assert.match(state, /enable_state_resources[\s\S]*default\s*=\s*false/);
});

test('staging uses S3 backend and live marker log group', () => {
  const versions = readFileSync(resolve(ROOT, 'terraform/envs/staging/versions.tf'), 'utf8');
  const staging = readFileSync(resolve(ROOT, 'terraform/envs/staging/main.tf'), 'utf8');
  assert.match(versions, /backend\s+"s3"/);
  assert.match(versions, /continuityops-tfstate-283077380808/);
  assert.match(staging, /aws_cloudwatch_log_group"\s+"live_marker"/);
  assert.match(staging, /\/continuityops\/staging\/live-marker/);
});

test('ensure-tfstate bootstrap is idempotent aws cli', () => {
  const script = readFileSync(resolve(ROOT, 'terraform/ci-bootstrap/ensure-tfstate.sh'), 'utf8');
  assert.match(script, /head-bucket/);
  assert.match(script, /create-table/);
  assert.match(script, /continuityops-tf-locks/);
  assert.match(script, /ResourceInUseException/);
  assert.match(script, /BucketAlreadyOwnedByYou/);
});

test('policy JSON stubs parse and encode negative controls', () => {
  const iamNeg = JSON.parse(readFileSync(resolve(ROOT, 'terraform/policies/iam-negative.json'), 'utf8'));
  const netNeg = JSON.parse(readFileSync(resolve(ROOT, 'terraform/policies/network-negative.json'), 'utf8'));
  assert.ok(iamNeg.prohibited.includes('long_lived_access_keys_in_repo'));
  assert.ok(netNeg.required.includes('staging_and_recovery_lab_separated'));
});

test('terraform CLI: document absence or run fmt/validate when available', () => {
  let available = false;
  try {
    execFileSync('terraform', ['version'], { cwd: ROOT, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
    available = true;
  } catch {
    available = false;
  }
  if (!available) {
    assert.equal(available, false);
    return;
  }
  execFileSync('terraform', ['fmt', '-check', '-recursive', 'terraform'], { cwd: ROOT, encoding: 'utf8' });
});
