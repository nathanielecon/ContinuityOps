#!/usr/bin/env node
/** Fail if any runbook command is destructive without requires_approval. */
import { readdirSync, readFileSync } from 'node:fs';
import { resolve, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const dir = resolve(dirname(fileURLToPath(import.meta.url)), '../../operations/runbooks');
const DANGEROUS = /\b(rm\s+-rf|mkfs|dd\s+if=|kubectl\s+delete\s+ns|terraform\s+destroy|DROP\s+TABLE)\b/i;
let failures = [];
for (const name of readdirSync(dir)) {
  if (!name.endsWith('.json') || name === 'schema.json') continue;
  const rb = JSON.parse(readFileSync(join(dir, name), 'utf8'));
  for (const c of rb.safe_commands || []) {
    if (c.destructive === true && c.requires_approval !== true) {
      failures.push({ file: name, cmd: c.cmd, reason: 'destructive without requires_approval' });
    }
    if (DANGEROUS.test(c.cmd) && c.destructive !== true) {
      failures.push({ file: name, cmd: c.cmd, reason: 'dangerous pattern unmarked' });
    }
  }
}
if (failures.length) {
  console.error(JSON.stringify({ pass: false, failures }, null, 2));
  process.exit(1);
}
console.log(JSON.stringify({ pass: true, scanned: readdirSync(dir).filter((n) => n.endsWith('.json')).length }));
