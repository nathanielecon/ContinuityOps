import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const WF = resolve(ROOT, '.github/workflows');

const S1_WORKFLOWS = [
  'terraform-pr.yml',
  'terraform-plan.yml',
  'terraform-apply.yml',
  'drift.yml',
  'evidence-upload.yml',
  'teardown.yml'
];

const PROTECTED = [
  'codex-patch-publish.yml',
  'junior-actuate.yml',
  'validate.yml',
  'codex-keepwarm.yml'
];

function load(rel) {
  return readFileSync(resolve(ROOT, rel), 'utf8');
}

test('S1 workflow stubs exist and protected workflows remain', () => {
  for (const name of S1_WORKFLOWS) {
    assert.ok(existsSync(join(WF, name)), `missing ${name}`);
  }
  for (const name of PROTECTED) {
    assert.ok(existsSync(join(WF, name)), `must not remove ${name}`);
  }
});

test('third-party actions are commit-SHA pinned', () => {
  for (const name of S1_WORKFLOWS) {
    const text = load(`.github/workflows/${name}`);
    const uses = [...text.matchAll(/uses:\s*([^\s]+)/g)].map((m) => m[1]);
    assert.ok(uses.length > 0, `${name} has no uses:`);
    for (const ref of uses) {
      if (ref.startsWith('./')) continue;
      assert.match(ref, /@[0-9a-f]{40}$/, `${name} unpinned action: ${ref}`);
    }
  }
});

test('PR workflow is read-only and credential-free', () => {
  const text = load('.github/workflows/terraform-pr.yml');
  assert.match(text, /permissions:\s*\n\s*contents:\s*read/);
  assert.doesNotMatch(text, /id-token:\s*write/);
  assert.doesNotMatch(text, /configure-aws-credentials/);
  assert.match(text, /assert-pr-readonly/);
});

test('mutation workflows require OIDC id-token and environment', () => {
  for (const name of ['terraform-plan.yml', 'terraform-apply.yml', 'teardown.yml', 'drift.yml']) {
    const text = load(`.github/workflows/${name}`);
    assert.match(text, /id-token:\s*write/, `${name} missing id-token`);
    assert.match(text, /configure-aws-credentials@[0-9a-f]{40}/, `${name} missing pinned OIDC action`);
    assert.match(text, /environment:/, `${name} missing environment gate`);
  }
});

test('assert-pr-readonly script passes locally without AWS keys', () => {
  const out = execFileSync('node', ['scripts/ci/assert-pr-readonly.mjs'], {
    cwd: ROOT,
    encoding: 'utf8',
    env: { ...process.env, AWS_ACCESS_KEY_ID: '', AWS_SECRET_ACCESS_KEY: '', AWS_SESSION_TOKEN: '' }
  });
  const json = JSON.parse(out);
  assert.equal(json.ok, true);
});

test('assert-pr-readonly fails when AWS key present', () => {
  assert.throws(() => {
    execFileSync('node', ['scripts/ci/assert-pr-readonly.mjs'], {
      cwd: ROOT,
      encoding: 'utf8',
      env: { ...process.env, AWS_ACCESS_KEY_ID: 'AKIATEST' }
    });
  });
});
