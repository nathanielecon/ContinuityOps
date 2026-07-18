#!/usr/bin/env node
/**
 * D-028 / CO-006 control-center packager.
 * Fetches pinned Project A/C trees via gh (no browser) into
 * integration/upstreams/packets/<id>/ and writes CO-004 digest proof.
 *
 * Usage: node scripts/package-upstream-context.mjs
 */
import { spawnSync } from 'node:child_process';
import {
  mkdirSync,
  writeFileSync,
  readFileSync,
  existsSync,
  rmSync,
  cpSync,
  readdirSync,
  statSync,
} from 'node:fs';
import { join, resolve, dirname, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { tmpdir } from 'node:os';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const TAR = process.env.TAR_EXE || 'C:\\Windows\\System32\\tar.exe';
const PACKET_ID = process.env.PACKET_ID || '2026-07-18-a-c';
const PACKET_DIR = join(ROOT, 'integration', 'upstreams', 'packets', PACKET_ID);
const DATE = PACKET_ID.slice(0, 10);

const PROJECT_A = {
  id: 'project_a',
  repository: 'nathanielecon/aws-landing-zone-lab',
  commit_sha: 'f688065c7705ab7d3febcd9ec2842bea4d8bed87',
  extracted_paths: [
    'README.md',
    'platform/README.md',
    'platform/SOURCES.md',
    'platform/evidence-index.md',
    'platform/docs/architecture',
    'platform/docs/guardrails',
    'platform/environments',
    'platform/harness',
    'evidence/platform',
  ],
};

/** A2 Option 2: ContinuityOps pin = deploy SHA with proven ECR digest. */
const PROJECT_C = {
  id: 'project_c',
  repository: 'nathanielecon/local-first-governed-cicd',
  commit_sha: '376b7e18c5cc94e67ff180ca2f42b8eb05535be3',
  extracted_paths: [
    'STATUS.md',
    'docs/decisions/0002-promote-digests.md',
    'evidence/phase-6/manifest.json',
    'scripts/smoke_test.py',
    'src/delivery_api',
  ],
  /**
   * Phase-9 governing evidence was committed after the deploy SHA.
   * Overlay those paths from the evidence commit; pin remains 376b7e18….
   */
  evidence_overlays: [
    {
      commit_sha: 'c6ca45425244323ee90be5b7b02d511f54976b2b',
      extracted_paths: ['evidence/phase-9'],
      reason: 'phase-9 staging smoke + ECR digest recorded against pin 376b7e18…',
    },
  ],
};

function die(msg) {
  console.error(msg);
  process.exit(1);
}

function run(cmd, args, opts = {}) {
  const r = spawnSync(cmd, args, {
    encoding: 'utf8',
    maxBuffer: 64 * 1024 * 1024,
    ...opts,
  });
  if (r.status !== 0) {
    die(`${cmd} ${args.join(' ')} failed:\n${r.stderr || r.stdout}`);
  }
  return r;
}

function ghApiRaw(repoPath) {
  const r = run('gh', ['api', repoPath, '-H', 'Accept: application/vnd.github.raw'], {
    encoding: 'buffer',
    maxBuffer: 256 * 1024 * 1024,
  });
  return r.stdout;
}

function downloadTarball(repository, commitSha, outFile) {
  const bytes = ghApiRaw(`repos/${repository}/tarball/${commitSha}`);
  writeFileSync(outFile, bytes);
  console.log(`downloaded ${repository}@${commitSha.slice(0, 12)}… (${bytes.length} bytes)`);
}

function listTopDir(extractRoot) {
  const entries = readdirSync(extractRoot).filter((n) => {
    try {
      return statSync(join(extractRoot, n)).isDirectory();
    } catch {
      return false;
    }
  });
  if (entries.length !== 1) {
    die(`expected one top-level dir under ${extractRoot}, got: ${entries.join(', ')}`);
  }
  return join(extractRoot, entries[0]);
}

function extractSelected(tarball, extractRoot, destRoot, selectedPaths) {
  rmSync(extractRoot, { recursive: true, force: true });
  mkdirSync(extractRoot, { recursive: true });
  run(TAR, ['-xzf', tarball, '-C', extractRoot]);
  const repoRoot = listTopDir(extractRoot);
  const kept = [];
  for (const rel of selectedPaths) {
    const src = join(repoRoot, rel);
    if (!existsSync(src)) {
      console.warn(`WARN missing path in tarball: ${rel}`);
      continue;
    }
    const dst = join(destRoot, rel);
    mkdirSync(dirname(dst), { recursive: true });
    cpSync(src, dst, { recursive: true });
    kept.push(rel.replace(/\\/g, '/'));
  }
  return kept;
}

function walkFiles(dir, base = dir) {
  const out = [];
  if (!existsSync(dir)) return out;
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    const st = statSync(p);
    if (st.isDirectory()) out.push(...walkFiles(p, base));
    else out.push(relative(base, p).replace(/\\/g, '/'));
  }
  return out;
}

function buildCo004(projectCDir, overlays) {
  const pin = PROJECT_C.commit_sha;
  const governingPath = join(projectCDir, 'evidence', 'phase-9', 'governing-manifest.json');
  let governing = null;
  if (existsSync(governingPath)) {
    governing = JSON.parse(readFileSync(governingPath, 'utf8'));
  }

  const proven = governing
    ? {
        image_digest: String(governing.image_ref || '').includes('@')
          ? governing.image_ref.split('@')[1]
          : null,
        image_ref: governing.image_ref ?? null,
        bound_git_sha: governing.git_sha ?? null,
        evidence: 'evidence/phase-9/governing-manifest.json',
        evidence_commit_sha: overlays?.[0]?.commit_sha ?? null,
        smoke: governing.smoke ?? null,
      }
    : null;

  const pinMatchesProven =
    proven?.bound_git_sha && proven.bound_git_sha.toLowerCase() === pin.toLowerCase() && proven.image_digest;

  if (!pinMatchesProven) {
    die(
      `CO-004 A2 Option 2 failed: expected governing-manifest digest bound to pin ${pin}; got ${JSON.stringify(proven)}`
    );
  }

  const rollback_evidence =
    'integration/upstreams/packets/2026-07-18-a-c/project_c/evidence/phase-6/manifest.json (fixture only; not ContinuityOps known-good)';
  const one_line = `image_digest: ${proven.image_digest} | rollback: none proven | source: ${proven.image_ref} (packet ${proven.evidence}; evidence_commit ${proven.evidence_commit_sha}; pin ${pin})`;

  return {
    schema_version: '1.0',
    issue: 'CO-004',
    a2_option: 2,
    repository: PROJECT_C.repository,
    commit_sha: pin,
    one_line,
    image_digest: proven.image_digest,
    registry: proven.image_ref.split('@')[0],
    rollback_target: 'none proven',
    rollback_evidence,
    provenance: {
      phase9_governing_manifest: proven,
      phase6_manifest_note:
        'Phase 6 manifest uses localhost fixture digests; ContinuityOps records rollback as none proven with this evidence path.',
      pin_matches_proven_digest: true,
      evidence_overlays: overlays ?? [],
    },
    packaged_at: DATE,
  };
}

function packProject(work, proj) {
  const tarball = join(work, `${proj.id}.tar.gz`);
  const extractRoot = join(work, `${proj.id}-extract`);
  const destRoot = join(PACKET_DIR, proj.id);
  mkdirSync(destRoot, { recursive: true });
  downloadTarball(proj.repository, proj.commit_sha, tarball);
  const kept = extractSelected(tarball, extractRoot, destRoot, proj.extracted_paths);

  const overlayRecords = [];
  for (const overlay of proj.evidence_overlays ?? []) {
    const otar = join(work, `${proj.id}-overlay-${overlay.commit_sha.slice(0, 12)}.tar.gz`);
    const oextract = join(work, `${proj.id}-overlay-${overlay.commit_sha.slice(0, 12)}`);
    downloadTarball(proj.repository, overlay.commit_sha, otar);
    const overlayKept = extractSelected(otar, oextract, destRoot, overlay.extracted_paths);
    overlayRecords.push({
      commit_sha: overlay.commit_sha,
      extracted_paths: overlayKept,
      reason: overlay.reason,
    });
    console.log(`overlay ${proj.id}@${overlay.commit_sha.slice(0, 12)}…: ${overlayKept.join(', ')}`);
  }

  return {
    id: proj.id,
    repository: proj.repository,
    commit_sha: proj.commit_sha,
    extracted_paths: kept,
    evidence_overlays: overlayRecords,
    file_count: walkFiles(destRoot).length,
  };
}

function main() {
  if (!existsSync(TAR)) die(`tar not found: ${TAR}`);

  const work = join(tmpdir(), `continuityops-upstream-${PACKET_ID}`);
  rmSync(work, { recursive: true, force: true });
  mkdirSync(work, { recursive: true });
  rmSync(PACKET_DIR, { recursive: true, force: true });
  mkdirSync(PACKET_DIR, { recursive: true });

  const sources = [packProject(work, PROJECT_A), packProject(work, PROJECT_C)];
  for (const s of sources) {
    console.log(`packed ${s.id}: ${s.extracted_paths.length} path roots, ${s.file_count} files`);
  }

  const projectCSource = sources.find((s) => s.id === 'project_c');
  const co004 = buildCo004(join(PACKET_DIR, 'project_c'), projectCSource.evidence_overlays);
  writeFileSync(join(PACKET_DIR, 'co-004-digest-proof.json'), `${JSON.stringify(co004, null, 2)}\n`);
  writeFileSync(join(PACKET_DIR, 'CO-004.txt'), `${co004.one_line}\n`);

  const manifest = {
    schema_version: '1.0',
    packet_id: PACKET_ID,
    packaged_at: DATE,
    packager: 'control-center',
    decision: 'D-028',
    a2_option: 2,
    method: 'gh api repos/.../tarball/<sha> + Windows tar.exe selective extract (+ evidence overlay)',
    sources,
    co_004: {
      one_line: co004.one_line,
      proof: 'co-004-digest-proof.json',
      image_digest: co004.image_digest,
      registry: co004.registry,
      rollback_target: co004.rollback_target,
      rollback_evidence: co004.rollback_evidence,
    },
    notes:
      'Read-only vendored snapshot. Project C pin is the phase-9 deploy SHA; phase-9 evidence paths overlay from the later evidence commit. Upstream repos unmodified.',
  };
  writeFileSync(join(PACKET_DIR, 'manifest.json'), `${JSON.stringify(manifest, null, 2)}\n`);

  console.log('\nCO-004:', co004.one_line);
  console.log(`packet: ${relative(ROOT, PACKET_DIR)}`);
}

main();
