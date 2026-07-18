#!/usr/bin/env node
/**
 * Assert Cloud seat GH_TOKEN has GitHub power for the GitOps loop.
 * Portable: pass owner/repo as argv[2] (default nathanielecon/ContinuityOps).
 * Does not mutate the repository. Exit 0 = ok; 1 = missing power / no token.
 *
 * Usage:
 *   node scripts/assert-cloud-seat-gh-token.mjs
 *   node scripts/assert-cloud-seat-gh-token.mjs nathanielecon/other-repo
 */
import { execFileSync } from 'node:child_process';

const target = process.argv[2] || 'nathanielecon/ContinuityOps';
const [owner, repo] = target.split('/');
if (!owner || !repo) {
  console.error('usage: node scripts/assert-cloud-seat-gh-token.mjs [owner/repo]');
  process.exit(1);
}

const envToken = Boolean(process.env.GH_TOKEN || process.env.GITHUB_TOKEN);
let ghAuthed = false;
try {
  execFileSync('gh', ['auth', 'status'], {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  ghAuthed = true;
} catch {
  ghAuthed = false;
}
if (!envToken && !ghAuthed) {
  console.error('FAIL: no GH_TOKEN/GITHUB_TOKEN and gh is not authenticated.');
  console.error(
    'Cloud seat: inject fine-grained PAT as GH_TOKEN (docs/operator/CLOUD_SEAT_GH_TOKEN.md), then new Cloud Agent.',
  );
  process.exit(1);
}
if (!envToken && ghAuthed) {
  console.log(
    'WARN: using gh keychain auth (control-center). Cloud Agents still need env GH_TOKEN injected.',
  );
}

function ghJson(path) {
  try {
    const out = execFileSync('gh', ['api', path], {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
      maxBuffer: 4 * 1024 * 1024,
    });
    return { ok: true, status: 200, data: JSON.parse(out) };
  } catch (err) {
    const msg = String(err.stderr || err.stdout || err.message || err);
    const m = msg.match(/\bHTTP\s+(\d{3})\b/i) || msg.match(/\b(\d{3})\b/);
    return { ok: false, status: m ? Number(m[1]) : 0, data: null, msg };
  }
}

const checks = [
  { id: 'contents', path: `repos/${owner}/${repo}`, need: 'Contents read' },
  {
    id: 'pull_requests',
    path: `repos/${owner}/${repo}/pulls?per_page=1&state=open`,
    need: 'Pull requests read (write needed for merge)',
  },
  {
    id: 'actions',
    path: `repos/${owner}/${repo}/actions/runs?per_page=1`,
    need: 'Actions read (write needed for workflow_dispatch)',
  },
  {
    id: 'workflows',
    path: `repos/${owner}/${repo}/actions/workflows`,
    need: 'Workflows / Actions metadata',
  },
  {
    id: 'issues',
    path: `repos/${owner}/${repo}/issues?per_page=1&state=open`,
    need: 'Issues read (write needed for queue/@codex)',
  },
  {
    id: 'environments',
    path: `repos/${owner}/${repo}/environments`,
    need: 'Environments read (optional)',
    optional: true,
  },
];

const commits = ghJson(`repos/${owner}/${repo}/commits?per_page=1`);
const headSha = commits.ok && Array.isArray(commits.data) && commits.data[0]?.sha
  ? commits.data[0].sha
  : null;
if (headSha) {
  checks.push({
    id: 'commit_statuses',
    path: `repos/${owner}/${repo}/commits/${headSha}/status`,
    need: 'Commit statuses read',
  });
}

console.log(`Cloud seat GH token assert → ${owner}/${repo}`);
console.log(
  `auth: ${process.env.GH_TOKEN ? 'GH_TOKEN' : process.env.GITHUB_TOKEN ? 'GITHUB_TOKEN' : 'gh-keychain'}`,
);

let failed = 0;
let optionalFailed = 0;
for (const c of checks) {
  const res = ghJson(c.path);
  const label = res.ok ? 'OK' : `FAIL(${res.status || '?'})`;
  console.log(`${label.padEnd(10)} ${c.id.padEnd(18)} ${c.need}`);
  if (!res.ok) {
    if (c.optional) optionalFailed += 1;
    else failed += 1;
  }
}

if (failed > 0) {
  console.error('');
  console.error(`${failed} required check(s) failed. Expand fine-grained PAT and re-inject GH_TOKEN.`);
  console.error('See docs/operator/CLOUD_SEAT_GH_TOKEN.md');
  process.exit(1);
}

if (optionalFailed > 0) {
  console.log(`WARN: ${optionalFailed} optional check(s) failed.`);
}

console.log('PASS: Cloud seat GitHub power looks sufficient for PR → Actions → merge loop.');
console.log('Remember: live AWS is still GHA OIDC, not this seat.');
process.exit(0);
