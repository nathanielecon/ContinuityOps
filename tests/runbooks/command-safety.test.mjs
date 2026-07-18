import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

test('runbooks match schema required fields', () => {
  const schema = JSON.parse(readFileSync(resolve(ROOT, 'operations/runbooks/schema.json'), 'utf8'));
  for (const name of readdirSync(resolve(ROOT, 'operations/runbooks'))) {
    if (!name.endsWith('.json') || name === 'schema.json') continue;
    const rb = JSON.parse(readFileSync(resolve(ROOT, 'operations/runbooks', name), 'utf8'));
    for (const key of schema.required) {
      assert.ok(rb[key] !== undefined, `${name} missing ${key}`);
    }
  }
});

test('no destructive commands unmarked', () => {
  const DANGEROUS = /\b(rm\s+-rf|mkfs|terraform\s+destroy)\b/i;
  for (const name of readdirSync(resolve(ROOT, 'operations/runbooks'))) {
    if (!name.endsWith('.json') || name === 'schema.json') continue;
    const rb = JSON.parse(readFileSync(resolve(ROOT, 'operations/runbooks', name), 'utf8'));
    for (const c of rb.safe_commands) {
      if (c.destructive) assert.equal(c.requires_approval, true);
      if (DANGEROUS.test(c.cmd)) assert.equal(c.destructive, true);
    }
  }
});
