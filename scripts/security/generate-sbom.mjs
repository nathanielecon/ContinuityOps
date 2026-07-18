#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { dirname, join, relative, resolve } from 'node:path';

const repoRoot = resolve(new URL('../..', import.meta.url).pathname);
const defaultOutput = 'evidence/hosted/security-sbom-2026-07-18.json';
const outputArg = process.argv.find((arg) => arg.startsWith('--output='));
const outputPath = resolve(repoRoot, outputArg ? outputArg.slice('--output='.length) : defaultOutput);
const recordedAt = process.env.SOURCE_DATE_EPOCH
  ? new Date(Number(process.env.SOURCE_DATE_EPOCH) * 1000).toISOString()
  : new Date().toISOString();

const ignoredDirs = new Set(['.git', 'node_modules', '.terraform']);
const includedExtensions = new Set(['.js', '.mjs', '.json', '.md', '.yml', '.yaml', '.tf', '.sh', '.ps1', '.txt']);
const includeExact = new Set(['Dockerfile', 'Makefile']);

function sha256(path) {
  return createHash('sha256').update(readFileSync(path)).digest('hex');
}

function walk(dir, acc = []) {
  for (const entry of readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
    if (entry.name.startsWith('.') && entry.name !== '.github') continue;
    const abs = join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!ignoredDirs.has(entry.name)) walk(abs, acc);
      continue;
    }
    if (!entry.isFile()) continue;
    if (resolve(abs) === outputPath) continue;
    const rel = relative(repoRoot, abs).replaceAll('\\', '/');
    const ext = entry.name.includes('.') ? entry.name.slice(entry.name.lastIndexOf('.')) : '';
    if (includedExtensions.has(ext) || includeExact.has(entry.name)) {
      const st = statSync(abs);
      acc.push({ path: rel, size_bytes: st.size, sha256: sha256(abs) });
    }
  }
  return acc;
}

function readJsonIfPresent(relPath) {
  const abs = join(repoRoot, relPath);
  if (!existsSync(abs)) return null;
  return JSON.parse(readFileSync(abs, 'utf8'));
}

const files = walk(repoRoot);
const packageManifests = ['package.json', 'package-lock.json', 'tests/package.json']
  .map((path) => ({ path, document: readJsonIfPresent(path) }))
  .filter((entry) => entry.document);
const manifestComponents = packageManifests.map((entry) => {
  const abs = join(repoRoot, entry.path);
  const st = statSync(abs);
  return {
    path: entry.path,
    type: 'npm-manifest',
    size_bytes: st.size,
    sha256: sha256(abs),
    dependencies: Object.keys(entry.document.dependencies ?? {}).sort(),
    devDependencies: Object.keys(entry.document.devDependencies ?? {}).sort()
  };
});

const sbom = {
  bomFormat: 'ContinuityOps-repository-sbom',
  specVersion: '1.0',
  serialNumber: `urn:uuid:${createHash('sha256').update(files.map((f) => `${f.path}:${f.sha256}`).join('\n')).digest('hex').slice(0, 32)}`,
  metadata: {
    component: { name: 'ContinuityOps', type: 'repository' },
    generated_at: recordedAt,
    generator: 'scripts/security/generate-sbom.mjs',
    dependency_sources: packageManifests.map((entry) => entry.path),
    exclusions: [...ignoredDirs].sort()
  },
  components: manifestComponents,
  dependencies: packageManifests.map((entry) => ({
    ref: entry.path,
    name: entry.document.name ?? entry.path,
    type: 'npm-manifest',
    dependencies: Object.keys(entry.document.dependencies ?? {}).sort(),
    devDependencies: Object.keys(entry.document.devDependencies ?? {}).sort()
  }))
};

mkdirSync(dirname(outputPath), { recursive: true });
writeFileSync(outputPath, `${JSON.stringify(sbom, null, 2)}\n`);
console.log(JSON.stringify({ output: relative(repoRoot, outputPath), repository_files_hashed: files.length, components: sbom.components.length, dependencies: sbom.dependencies.length }, null, 2));
