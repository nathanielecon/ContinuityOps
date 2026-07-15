// Pinned validator implementations. Each is check-only: it reads the repo and
// returns findings, never mutating tracked or untracked files.

import { execFileSync } from 'node:child_process';
import { readFileSync, existsSync } from 'node:fs';
import { register } from './registry.mjs';
import { verifyUniqueOwnership } from '../partition.mjs';

function readJson(abs) {
  return JSON.parse(readFileSync(abs, 'utf8'));
}

// -- state_schema: task-state store matches its frozen schema shape ----------
register('state_schema', async ({ repoRoot }) => {
  const findings = [];
  const statePath = `${repoRoot}/harness/state/tasks.json`;
  if (!existsSync(statePath)) return { ok: false, findings: ['missing harness/state/tasks.json'] };
  const s = readJson(statePath);
  for (const key of ['schema_version', 'plan_id', 'revision', 'authorized_through_phase', 'baseline_sha', 'tasks']) {
    if (!(key in s)) findings.push(`state missing required key '${key}'`);
  }
  const legal = new Set(['planned', 'ready', 'running', 'blocked', 'review', 'verified', 'done']);
  for (const t of s.tasks || []) {
    if (!/^P[0-9]+-T[0-9]+$/.test(t.id || '')) findings.push(`bad task id '${t.id}'`);
    if (!legal.has(t.state)) findings.push(`task ${t.id} has illegal state '${t.state}'`);
  }
  return { ok: findings.length === 0, findings };
});

// -- partition_unique_ownership: no path owned by two slices ------------------
register('partition_unique_ownership', async ({ repoRoot }) => {
  const manifestPath = `${repoRoot}/harness/partition-manifest.json`;
  if (!existsSync(manifestPath)) return { ok: false, findings: ['missing harness/partition-manifest.json'] };
  const manifest = readJson(manifestPath);
  const { ok, duplicates } = verifyUniqueOwnership(manifest);
  return { ok, findings: duplicates.map((d) => `path ${d.path} owned by ${d.slices.join(', ')}`) };
});

// -- upstream_pin_schema: integration lock has concrete pins ------------------
register('upstream_pin_schema', async ({ repoRoot }) => {
  const lockPath = `${repoRoot}/integration/upstreams.lock.json`;
  if (!existsSync(lockPath)) return { ok: false, findings: ['missing integration/upstreams.lock.json'] };
  const lock = readJson(lockPath);
  const findings = [];
  for (const proj of ['project_a', 'project_c']) {
    const p = lock[proj];
    if (!p) { findings.push(`lock missing ${proj}`); continue; }
    if (!p.repository) findings.push(`${proj} missing repository`);
    if (!p.commit_sha || p.commit_sha === 'REQUIRED') findings.push(`${proj} commit_sha not pinned`);
  }
  return { ok: findings.length === 0, findings };
});

// -- clean_tree: no uncommitted changes (git) --------------------------------
register('clean_tree', async ({ repoRoot }) => {
  try {
    const out = execFileSync('git', ['status', '--porcelain'], { cwd: repoRoot, encoding: 'utf8' });
    return out.trim() === ''
      ? { ok: true, findings: [] }
      : { ok: false, findings: ['working tree not clean:\n' + out.trim()] };
  } catch (err) {
    return { ok: false, findings: [`git status failed: ${err.message}`] };
  }
});

// -- secret_scan: obvious credential patterns in tracked files ---------------
const SECRET_PATTERNS = [
  [/AKIA[0-9A-Z]{16}/, 'AWS access key id'],
  [/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/, 'private key block'],
  [/aws_secret_access_key\s*=\s*['"][^'"]{20,}/i, 'aws secret access key literal'],
  [/xox[baprs]-[0-9A-Za-z-]{10,}/, 'slack token'],
  [/ghp_[0-9A-Za-z]{36}/, 'github PAT'],
];
register('secret_scan', async ({ repoRoot }) => {
  const findings = [];
  let files = [];
  try {
    files = execFileSync('git', ['ls-files'], { cwd: repoRoot, encoding: 'utf8' }).split('\n').filter(Boolean);
  } catch (err) {
    return { ok: false, findings: [`git ls-files failed: ${err.message}`] };
  }
  for (const f of files) {
    if (/\.(png|svg|drawio|p12|jpg|jpeg|gif|ico)$/.test(f)) continue;
    // Skip the scanner's own pattern definitions to avoid self-flagging.
    if (f.endsWith('harness/lib/validators/impl.mjs')) continue;
    let content;
    try { content = readFileSync(`${repoRoot}/${f}`, 'utf8'); } catch { continue; }
    for (const [re, label] of SECRET_PATTERNS) {
      if (re.test(content)) findings.push(`${label} pattern in ${f}`);
    }
  }
  return { ok: findings.length === 0, findings };
});

// -- scope: modified paths stay inside a task's allowed write_scope ----------
export function scopeCheck(modifiedPaths, writeScope) {
  const prefixes = (writeScope || []).map((p) => p.replace(/\*+$/, ''));
  const escapes = modifiedPaths.filter((m) => !prefixes.some((pre) => m === pre || m.startsWith(pre)));
  return { ok: escapes.length === 0, escapes };
}
register('scope', async ({ modifiedPaths = [], writeScope = [] }) => {
  const { ok, escapes } = scopeCheck(modifiedPaths, writeScope);
  return { ok, findings: escapes.map((e) => `path ${e} escapes write_scope`) };
});

// -- model_routing: evidence records an ACTUAL model id, never aspirational --
const ASPIRATIONAL = [/codex/i, /gpt-?5/i, /grok/i];
register('model_routing', async ({ producedBy }) => {
  if (!producedBy || !producedBy.model_id) return { ok: false, findings: ['no producing model_id recorded'] };
  const findings = [];
  // In THIS environment workers are Claude. Reject a recorded id that claims an
  // engine we cannot actually invoke unless it is explicitly marked simulated.
  for (const re of ASPIRATIONAL) {
    if (re.test(producedBy.model_id) && !/sim|planned|not-run/i.test(producedBy.model_id)) {
      findings.push(`model_id '${producedBy.model_id}' claims an uninvokable engine without a simulated/planned marker`);
    }
  }
  return { ok: findings.length === 0, findings };
});

// -- worker_language: worker free-text handoff fields are zh-CN --------------
export function looksSimplifiedChinese(text) {
  if (!text) return false;
  const han = (text.match(/[一-鿿]/g) || []).length;
  return han >= Math.max(1, Math.ceil(text.replace(/\s/g, '').length * 0.3));
}
register('worker_language', async ({ handoff }) => {
  if (!handoff) return { ok: false, findings: ['no handoff provided'] };
  const findings = [];
  if (!looksSimplifiedChinese(handoff.summary_zh)) findings.push('summary_zh is not predominantly Simplified Chinese');
  return { ok: findings.length === 0, findings };
});
