#!/usr/bin/env node
/**
 * ContinuityOps cloud-seat gate: prove GH_TOKEN can see Actions / merge path.
 * Expect PASS after owner refreshes Cursor Secrets (repo + workflow).
 *
 * Live AWS stays GHA OIDC → continuityops-gha.
 * Do not invent AWS keys. Do not chase Cursor STS / CursorCloudAgent.
 */
import { spawnSync } from 'node:child_process';

const REPO = process.env.COPS_GH_REPO || 'nathanielecon/ContinuityOps';
const token = process.env.GH_TOKEN || '';

function fail(msg, detail) {
  console.error('FAIL:', msg);
  if (detail) console.error(detail);
  console.error(
    'Remediation: refresh fine-grained PAT (Contents/PRs/Issues/Actions/Workflows R/W) as Cursor Secret GH_TOKEN, then start a NEW Cloud Agent.'
  );
  process.exit(1);
}

function ghApi(path) {
  const r = spawnSync('gh', ['api', path], {
    encoding: 'utf8',
    env: process.env
  });
  return {
    ok: r.status === 0,
    status: r.status,
    stdout: (r.stdout || '').trim(),
    stderr: (r.stderr || '').trim()
  };
}

if (!token) fail('GH_TOKEN unset');
if (token.startsWith('ghs_')) {
  fail('GH_TOKEN is a GitHub App install token (ghs_). Need owner fine-grained PAT (github_pat_).');
}
if (!token.startsWith('github_pat_') && !token.startsWith('ghp_')) {
  fail('GH_TOKEN does not look like a PAT (expected github_pat_ or ghp_)');
}

const user = ghApi('user');
if (!user.ok) fail('gh api user failed', user.stderr || user.stdout);
let login = '';
try {
  login = JSON.parse(user.stdout).login || '';
} catch {
  fail('gh api user returned non-JSON', user.stdout);
}
if (!login) fail('gh api user returned empty login');

const workflows = ghApi(`repos/${REPO}/actions/workflows`);
if (!workflows.ok) {
  fail(
    `Actions API denied for ${REPO} — PAT needs Actions: Read and write (or start a NEW agent after secret refresh)`,
    workflows.stderr || workflows.stdout
  );
}
let names = [];
try {
  names = (JSON.parse(workflows.stdout).workflows || []).map((w) => w.name);
} catch {
  fail('Actions workflows response not JSON', workflows.stdout);
}
if (!names.length) fail('Actions workflows list empty unexpectedly');

const pulls = ghApi(`repos/${REPO}/pulls?state=open&per_page=1`);
if (!pulls.ok) {
  fail(
    `Pulls API denied for ${REPO} — PAT needs Pull requests: Read and write`,
    pulls.stderr || pulls.stdout
  );
}

console.log('PASS');
console.log(
  JSON.stringify(
    {
      ok: true,
      login,
      repo: REPO,
      token_kind: token.startsWith('github_pat_') ? 'fine-grained' : 'classic',
      actions_workflows_sample: names.slice(0, 8),
      doctrine: {
        live_aws: 'GHA OIDC → continuityops-gha',
        no_aws_keys: true,
        no_cursor_sts: true
      }
    },
    null,
    2
  )
);
