import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

import {
  assessVersion,
  readPinnedVersion,
  suggestVersions,
} from '../../scripts/ci/assert-eks-standard-support.mjs';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const read = (p) => readFileSync(resolve(ROOT, p), 'utf8');

// --- BF-2026-029 regression guards -----------------------------------------

test('apply never triggers on push to main', () => {
  const wf = read('.github/workflows/continuityops-terraform.yml');
  // The literal cause: a fmt-only commit matched terraform/** and applied.
  assert.doesNotMatch(wf, /refs\/heads\/main/);
  assert.doesNotMatch(wf, /^\s{2}push:/m);
});

test('apply is gated on a plan that reports actual changes', () => {
  const wf = read('.github/workflows/continuityops-terraform.yml');
  assert.match(wf, /steps\.guard\.outputs\.changes\s*==\s*'true'/);
  // Decision must come from the plan file, not an exit code: the
  // setup-terraform wrapper silently swallowed -detailed-exitcode's exit 2 on
  // run 31267293441, reading "10 to add" as "no changes" and skipping apply.
  assert.match(wf, /terraform show -json tfplan/);
  // Check executable lines only — comments documenting the defect are expected.
  const executable = wf
    .split('\n')
    .filter((l) => !/^\s*#/.test(l))
    .join('\n');
  assert.doesNotMatch(executable, /-detailed-exitcode/);
});

test('terraform wrapper is disabled wherever exit status matters', () => {
  // The wrapper does not reliably propagate terraform's exit status. On apply
  // that silently no-ops; on destroy a failure could report success and leave
  // resources billing.
  for (const f of [
    '.github/workflows/continuityops-terraform.yml',
    '.github/workflows/teardown.yml',
  ]) {
    const wf = read(f);
    const setups = wf.match(/hashicorp\/setup-terraform/g) ?? [];
    const disabled = wf.match(/terraform_wrapper:\s*false/g) ?? [];
    assert.equal(
      disabled.length,
      setups.length,
      `${f}: ${setups.length} setup-terraform step(s) but ${disabled.length} with terraform_wrapper: false`,
    );
  }
});

test('teardown runs on a schedule so nothing survives unattended', () => {
  const wf = read('.github/workflows/teardown.yml');
  assert.match(wf, /schedule:/);
  assert.match(wf, /cron:/);
  // Scheduled runs carry no inputs and must not be blocked by the confirm gate.
  assert.match(wf, /github\.event_name == 'schedule'/);
  assert.match(wf, /COPS_LAB_KEEP_ALIVE/);
});

test('teardown cannot destroy the account guardrails root', () => {
  const wf = read('.github/workflows/teardown.yml');
  const options = wf.match(/options:\s*\[([^\]]+)\]/);
  assert.ok(options, 'teardown must declare an explicit env option list');
  assert.doesNotMatch(options[1], /account/);
});

// --- Account-level guardrails ----------------------------------------------

test('guardrails live in their own root, separate from the disposable lab', () => {
  const versions = read('terraform/envs/account/versions.tf');
  assert.match(versions, /key\s*=\s*"envs\/account\/terraform\.tfstate"/);
});

test('budget limit is sourced from budgets.json, not duplicated', () => {
  const main = read('terraform/envs/account/main.tf');
  assert.match(main, /jsondecode\(file\(/);
  assert.match(main, /operations\/finops\/budgets\.json/);
});

test('budget action denies creates but never deletes', () => {
  const main = read('terraform/envs/account/main.tf');
  const policy = main.slice(
    main.indexOf('deny_provisioning'),
    main.indexOf('budget_action_assume'),
  );
  assert.match(policy, /eks:CreateCluster/);
  assert.match(policy, /ec2:RunInstances/);
  // Denying deletes would trap the account in the expensive state the guardrail
  // exists to escape.
  assert.doesNotMatch(policy, /Delete/);
  assert.doesNotMatch(policy, /Terminate/);
});

test('alert email is never committed to this public repo', () => {
  const main = read('terraform/envs/account/main.tf');
  assert.doesNotMatch(main, /@gmail\.com/);
  assert.doesNotMatch(main, /@[a-z0-9-]+\.(com|org|net)"/i);
  // No default => apply fails closed when the address is not supplied.
  const block = main.slice(main.indexOf('variable "alert_email"'));
  const decl = block.slice(0, block.indexOf('variable "gha_role_name"'));
  assert.doesNotMatch(decl, /^\s*default\s*=/m);
});

test('deploy role gets its addon by attachment, never by import', () => {
  const tf = read('terraform/envs/account/iam-gha-addon.tf');
  // Attaching by name means the role's OIDC trust policy is never read, planned
  // or modified. Importing or redeclaring it risks locking CI out of the account.
  assert.match(tf, /aws_iam_role_policy_attachment"\s+"gha_finops_addon"/);
  assert.doesNotMatch(tf, /resource\s+"aws_iam_role"\s+"gha/);
  assert.doesNotMatch(tf, /assume_role_policy/);
  assert.doesNotMatch(tf, /import\s*\{/);
});

test('addon policy is sourced from the JSON file, not duplicated in HCL', () => {
  const tf = read('terraform/envs/account/iam-gha-addon.tf');
  assert.match(tf, /continuityops-gha-finops-addon\.json/);
  // Only Version + Statement forwarded — IAM rejects the file's _comment keys.
  assert.match(tf, /Version\s+=\s+local\.gha_addon_raw\.Version/);
  assert.match(tf, /Statement\s+=\s+local\.gha_addon_raw\.Statement/);
});

test('guardrails wait for the permission that creates them', () => {
  const main = read('terraform/envs/account/main.tf');
  // Both failed twice on AccessDenied before this ordering existed.
  for (const res of ['aws_budgets_budget" "monthly', 'aws_ce_anomaly_monitor" "service']) {
    const start = main.indexOf(res);
    assert.ok(start > 0, `${res} not found`);
    const block = main.slice(start, start + 400);
    assert.match(
      block,
      /depends_on\s*=\s*\[aws_iam_role_policy_attachment\.gha_finops_addon\]/,
      `${res} must depend on the addon attachment`,
    );
  }
});

test('addon grants no data access', () => {
  const raw = JSON.parse(read('terraform/policies/continuityops-gha-finops-addon.json'));
  const flat = JSON.stringify(raw.Statement);
  const forbidden = ['s3:GetObject', 'kms:Decrypt', 'secretsmanager:', 'dynamodb:GetItem'];
  const bad = forbidden.filter((a) => flat.includes(a));
  assert.deepEqual(bad, [], `addon must not grant data access: ${bad}`);
  // PassRole must be constrained to the budgets service, not open.
  const pass = raw.Statement.find((s) => JSON.stringify(s.Action).includes('iam:PassRole'));
  assert.ok(pass, 'PassRole statement expected');
  assert.equal(pass.Condition.StringEquals['iam:PassedToService'], 'budgets.amazonaws.com');
});

test('anomaly threshold fires below one day of an idle extended-support cluster', () => {
  const main = read('terraform/envs/account/main.tf');
  assert.match(main, /aws_ce_anomaly_monitor/);
  assert.match(main, /aws_ce_anomaly_subscription/);
  const threshold = Number(main.match(/values\s*=\s*\["(\d+)"\]/)[1]);
  assert.ok(threshold < 14.4, `threshold ${threshold} must be under $14.40/day`);
});

// --- EKS support calendar --------------------------------------------------

test('pinned EKS version is in standard support today', () => {
  const version = readPinnedVersion(read('terraform/modules/eks/main.tf'));
  assert.ok(version, 'cluster_version default must be discoverable');
  const result = assessVersion(version);
  assert.equal(result.known, true, `${version} missing from support calendar`);
  assert.equal(
    result.inStandardSupport,
    true,
    `EKS ${version} left standard support on ${result.endOfStandardSupport} ` +
      `and bills $0.60/hr instead of $0.10`,
  );
});

test('1.32 is correctly identified as extended support', () => {
  // The exact version that caused BF-2026-029.
  const result = assessVersion('1.32', new Date('2026-08-08T00:00:00Z'));
  assert.equal(result.inStandardSupport, false);
  assert.equal(result.hourlyRate, 0.6);
});

test('a version still in standard support is priced at the cheap rate', () => {
  const result = assessVersion('1.35', new Date('2026-08-08T00:00:00Z'));
  assert.equal(result.inStandardSupport, true);
  assert.equal(result.hourlyRate, 0.1);
});

test('expiry warning arrives before the rate changes, not after', () => {
  // 1.34 ends 2026-11-26; 30 days earlier must warn while still passing.
  const result = assessVersion('1.34', new Date('2026-10-27T00:00:00Z'));
  assert.equal(result.inStandardSupport, true);
  assert.equal(result.expiringSoon, true);
});

test('unknown versions fail closed rather than silently passing', () => {
  const result = assessVersion('1.99');
  assert.equal(result.known, false);
  assert.equal(result.inStandardSupport, null);
});

test('suggestions only include versions still in standard support', () => {
  const today = new Date('2026-08-08T00:00:00Z');
  const suggestions = suggestVersions(today);
  assert.ok(suggestions.length > 0);
  for (const s of suggestions) {
    assert.ok(
      new Date(`${s.endOfStandardSupport}T00:00:00Z`) > today,
      `${s.version} is not actually in standard support`,
    );
  }
});
