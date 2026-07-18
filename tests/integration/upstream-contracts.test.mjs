import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const PIN_C = '376b7e18c5cc94e67ff180ca2f42b8eb05535be3';
const DIGEST = 'sha256:bffa93adcbe247be118de0726842f673e14310052b3fdcd6ddaa853fbc05c229';
const PACKET = 'integration/upstreams/packets/2026-07-18-a-c';

function loadJson(rel) {
  return JSON.parse(readFileSync(resolve(ROOT, rel), 'utf8'));
}

test('upstreams.lock pins concrete SHAs and proven image_digest', () => {
  const lock = loadJson('integration/upstreams.lock.json');
  assert.equal(lock.schema_version, '1.0');
  assert.match(lock.project_a.commit_sha, /^[0-9a-f]{40}$/);
  assert.equal(lock.project_c.commit_sha, PIN_C);
  assert.equal(lock.project_a.repository, 'nathanielecon/aws-landing-zone-lab');
  assert.equal(lock.project_c.repository, 'nathanielecon/local-first-governed-cicd');
  assert.equal(lock.project_c.image_digest, DIGEST);
  assert.equal(lock.project_c.rollback_target, 'none proven');
  assert.ok(Array.isArray(lock.project_a.consumed_contracts) && lock.project_a.consumed_contracts.length > 0);
  assert.ok(Array.isArray(lock.project_c.consumed_contracts) && lock.project_c.consumed_contracts.length > 0);
  assert.ok(Array.isArray(lock.missing_capabilities));
  assert.equal(lock.missing_capabilities.length, 0);
});

test('consumed contract files exist and declare pinned_sha alignment', () => {
  const lock = loadJson('integration/upstreams.lock.json');
  for (const rel of lock.project_a.consumed_contracts) {
    assert.ok(existsSync(resolve(ROOT, rel)), `missing ${rel}`);
    const contract = loadJson(rel);
    assert.equal(contract.pinned_sha, lock.project_a.commit_sha);
    assert.equal(contract.upstream, 'project_a');
  }
  for (const rel of lock.project_c.consumed_contracts) {
    assert.ok(existsSync(resolve(ROOT, rel)), `missing ${rel}`);
    if (rel.startsWith('integration/contracts/')) {
      const contract = loadJson(rel);
      assert.equal(contract.pinned_sha, lock.project_c.commit_sha);
      assert.equal(contract.upstream, 'project_c');
    }
  }
});

test('app-contract release contract carries proven digest and lab boundary', () => {
  const app = loadJson('app-contract/release-contract.json');
  assert.equal(app.artifact.image_digest, DIGEST);
  assert.equal(app.artifact.rollback_target, 'none proven');
  assert.equal(app.identity.git_commit, PIN_C);
  assert.ok(app.remaining_boundaries.some((b) => /rollback/i.test(b)));
});

test('CO-006 context packet exists with A/C SHAs and manifest', () => {
  const lock = loadJson('integration/upstreams.lock.json');
  const packetRel = lock.context_packet?.path;
  assert.equal(packetRel, PACKET);
  const manifestRel = `${packetRel}/manifest.json`;
  assert.ok(existsSync(resolve(ROOT, manifestRel)), `missing ${manifestRel}`);
  const manifest = loadJson(manifestRel);
  assert.equal(manifest.decision, 'D-028');
  assert.equal(manifest.a2_option, 2);
  const byId = Object.fromEntries(manifest.sources.map((s) => [s.id, s]));
  assert.equal(byId.project_a.commit_sha, lock.project_a.commit_sha);
  assert.equal(byId.project_c.commit_sha, PIN_C);
  assert.ok(byId.project_a.file_count > 0);
  assert.ok(byId.project_c.file_count > 0);
  assert.ok((byId.project_c.evidence_overlays ?? []).length >= 1);
  assert.ok(existsSync(resolve(ROOT, `${packetRel}/project_a`)));
  assert.ok(existsSync(resolve(ROOT, `${packetRel}/project_c/evidence/phase-9/governing-manifest.json`)));
  const resolved = new Set((lock.resolved_capabilities ?? []).map((r) => r.id));
  assert.ok(resolved.has('CO-006'));
  assert.ok(resolved.has('CO-004'));
  assert.ok(resolved.has('MC-A-TREE'));
  assert.ok(resolved.has('MC-C-TREE'));
  assert.ok(resolved.has('MC-C-DIGEST'));
});

test('CO-004 proof records proven digest and none proven rollback for pin', () => {
  const lock = loadJson('integration/upstreams.lock.json');
  const proofRel = `${PACKET}/co-004-digest-proof.json`;
  assert.ok(existsSync(resolve(ROOT, proofRel)));
  const proof = loadJson(proofRel);
  assert.equal(proof.commit_sha, lock.project_c.commit_sha);
  assert.equal(proof.image_digest, DIGEST);
  assert.equal(proof.rollback_target, 'none proven');
  assert.match(proof.one_line, new RegExp(DIGEST.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
  assert.match(proof.one_line, /rollback:\s*none proven/i);
  assert.ok(existsSync(resolve(ROOT, `${PACKET}/CO-004.txt`)));
  const governing = loadJson(`${PACKET}/project_c/evidence/phase-9/governing-manifest.json`);
  assert.equal(governing.git_sha, PIN_C);
  assert.ok(String(governing.image_ref).includes(DIGEST));
});

test('project-c smoke paths match packaged smoke_test.py', () => {
  const smoke = loadJson('integration/contracts/project-c.smoke.json');
  assert.equal(smoke.exports.liveness_path, '/health/live');
  assert.equal(smoke.exports.readiness_path, '/health/ready');
  assert.equal(smoke.exports.version_path, '/version');
  assert.equal(smoke.exports.business_smoke_path, '/quotes');
  const src = readFileSync(resolve(ROOT, `${PACKET}/project_c/scripts/smoke_test.py`), 'utf8');
  assert.match(src, /\/health\/live/);
  assert.match(src, /\/health\/ready/);
  assert.match(src, /\/quotes/);
});
