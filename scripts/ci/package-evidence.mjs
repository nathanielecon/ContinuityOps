#!/usr/bin/env node
import { mkdirSync, writeFileSync, existsSync, readdirSync, statSync, readFileSync } from 'node:fs';
import { resolve, dirname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const outDir = resolve(ROOT, 'evidence/_bundle');
mkdirSync(outDir, { recursive: true });

function walk(dir, acc = []) {
  if (!existsSync(dir)) return acc;
  for (const name of readdirSync(dir)) {
    if (name === '_bundle') continue;
    const full = join(dir, name);
    const st = statSync(full);
    if (st.isDirectory()) walk(full, acc);
    else if (name.endsWith('.json')) acc.push(full);
  }
  return acc;
}

const files = walk(resolve(ROOT, 'evidence'));
const index = {
  schema_version: '1.0',
  generated_at: new Date().toISOString(),
  files: files.map((file) => ({
    path: relative(ROOT, file).replaceAll('\\', '/'),
    sha256: createHash('sha256').update(readFileSync(file)).digest('hex')
  }))
};

writeFileSync(resolve(outDir, 'index.json'), `${JSON.stringify(index, null, 2)}\n`);
console.log(JSON.stringify({ ok: true, count: index.files.length, out: 'evidence/_bundle/index.json' }, null, 2));
