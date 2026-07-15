#!/usr/bin/env node
// ContinuityOps orchestrator CLI. The single authorized surface for task-state
// transitions, phase authorization, validation, and evidence appends. Workers
// never edit state directly; they return a handoff and the adapter runs this.
//
// Usage:
//   node scripts/project.mjs status
//   node scripts/project.mjs ready <task_id>
//   node scripts/project.mjs run <task_id> --stream A
//   node scripts/project.mjs review <task_id> [--actor worker]
//   node scripts/project.mjs verify <task_id>
//   node scripts/project.mjs authorize-phase <n>
//   node scripts/project.mjs validate <task_id> [--modified a,b] [--scope x,y]
//   node scripts/project.mjs partition-verify

import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { readFileSync, existsSync } from 'node:fs';
import { StateStore } from '../harness/lib/state.mjs';
import { verifyUniqueOwnership, hashSlices } from '../harness/lib/partition.mjs';
import { runAll, listValidators } from '../harness/lib/validators/registry.mjs';
import '../harness/lib/validators/impl.mjs'; // registers pinned validators

const REPO = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const STATE_PATH = `${REPO}/harness/state/tasks.json`;

function parseFlags(args) {
  const flags = {};
  const positional = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) flags[args[i].slice(2)] = args[++i];
    else positional.push(args[i]);
  }
  return { flags, positional };
}

function store() {
  if (!existsSync(STATE_PATH)) throw new Error(`no state at ${STATE_PATH}; run 'init' first`);
  return new StateStore(STATE_PATH);
}

const cmds = {
  status() {
    const s = store();
    console.log(`plan=${s.data.plan_id} revision=${s.data.revision} authorized_through_phase=${s.data.authorized_through_phase}`);
    for (const t of s.data.tasks) {
      console.log(`  ${t.id} [${t.state}]${t.stream ? ' stream=' + t.stream : ''}  ${t.title || ''}`);
    }
  },
  ready([id]) { console.log(store().transition(id, 'ready', { actor: 'adapter' })); },
  run([id], flags) { console.log(store().transition(id, 'running', { actor: 'adapter', stream: flags.stream })); },
  review([id], flags) { console.log(store().transition(id, 'review', { actor: flags.actor || 'adapter' })); },
  verify([id]) { console.log(store().transition(id, 'verified', { actor: 'adapter' })); },
  done([id]) { console.log(store().transition(id, 'done', { actor: 'adapter' })); },
  'authorize-phase'([n]) { console.log(store().authorizePhase(Number(n))); },
  'partition-verify'() {
    const manifest = JSON.parse(readFileSync(`${REPO}/harness/partition-manifest.json`, 'utf8'));
    const uniq = verifyUniqueOwnership(manifest);
    if (!uniq.ok) {
      console.error('DUPLICATE OWNERSHIP:', uniq.duplicates);
      process.exit(1);
    }
    const hashes = hashSlices(manifest, REPO);
    console.log('partition ok; slices:', Object.keys(hashes).length);
    for (const [id, h] of Object.entries(hashes)) console.log(`  ${id} ${h.slice_sha256.slice(0, 12)} (${h.files.length} paths)`);
  },
  async validate([id], flags) {
    const s = store();
    const task = s.task(id);
    const ctx = {
      repoRoot: REPO,
      task,
      writeScope: flags.scope ? flags.scope.split(',') : task.write_scope || [],
      modifiedPaths: flags.modified ? flags.modified.split(',') : [],
      producedBy: { role: 'adapter', model_id: 'claude-opus-4-8' },
    };
    const ids = task.validators || [];
    const { ok, results } = await runAll(ids, ctx);
    for (const r of results) console.log(`  [${r.ok ? 'PASS' : 'FAIL'}] ${r.id}${r.findings.length ? ' :: ' + r.findings.join('; ') : ''}`);
    console.log(ok ? 'VALIDATE OK' : 'VALIDATE FAIL');
    if (!ok) process.exit(1);
  },
  validators() { console.log(listValidators().join('\n')); },
};

const [, , cmd, ...rest] = process.argv;
const { flags, positional } = parseFlags(rest);
if (!cmd || !cmds[cmd]) {
  console.error(`unknown command '${cmd || ''}'. commands: ${Object.keys(cmds).join(', ')}`);
  process.exit(2);
}
try {
  await cmds[cmd](positional, flags);
} catch (err) {
  console.error('ERROR:', err.message);
  process.exit(1);
}
