#!/usr/bin/env node
/** Read-only first-five-minute diagnostic checklist runner (local/synthetic). */
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const id = process.argv[2] || 'linux-pressure';
const rb = JSON.parse(readFileSync(resolve(ROOT, `operations/runbooks/${id}.json`), 'utf8'));
const unsafe = rb.safe_commands.filter((c) => c.destructive && !c.requires_approval);
if (unsafe.length) {
  console.error('Unsafe unmarked destructive commands', unsafe);
  process.exit(2);
}
console.log(JSON.stringify({
  runbook: rb.id,
  first_five_minutes: rb.first_five_minutes,
  safe_command_count: rb.safe_commands.length,
  claim_level: 'L1',
  note: 'Commands listed only; not executed against live fleets'
}, null, 2));
