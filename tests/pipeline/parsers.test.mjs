import test from 'node:test';
import assert from 'node:assert/strict';
import {
  detectPublish,
  parseLatestVerdict,
  parseVerdictFromBody,
  extractMergeReady,
  extractMergeReadyFromJudgeFiles,
  validateWakePacket,
  validateCrossLaneCite,
  extractJsonPacket,
  failClassHash,
  failClassLabel,
  countFailClassStrikes,
  nextStrikeLabel,
  hopKey,
  evaluateIdempotency,
  claimMarker,
  doneMarker,
  candidateBranchName,
  isCandidateBranch,
  parseChiefPage,
} from '../../scripts/pipeline/index.mjs';

test('detectPublish publish-ok with PR URL', () => {
  const r = detectPublish(
    'publish-ok (D-034): https://github.com/nathanielecon/ContinuityOps/pull/93'
  );
  assert.equal(r.kind, 'publish-ok');
  assert.equal(r.prNumber, 93);
});

test('detectPublish publish-failed', () => {
  const r = detectPublish('publish-failed (D-034): could not extract');
  assert.equal(r.kind, 'publish-failed');
});

test('parseLatestVerdict prefers last bot verdict', () => {
  const v = parseLatestVerdict([
    { user: { login: 'chatgpt-codex-connector[bot]' }, body: '{"verdict":"fail"}' },
    {
      user: { login: 'chatgpt-codex-connector[bot]' },
      body: '### x\n```json\n{"verdict":"pass"}\n```',
    },
  ]);
  assert.equal(v, 'pass');
});

test('parseVerdictFromBody', () => {
  assert.equal(parseVerdictFromBody('verdict: fail'), 'fail');
});

test('extractMergeReady from JSON and yaml-ish', () => {
  assert.equal(extractMergeReady('{"merge_ready":"no","overall_score":7.1}'), 'no');
  assert.equal(extractMergeReady('merge_ready: yes\n'), 'yes');
  assert.equal(extractMergeReady('{"merge_ready":"provisional"}'), 'provisional');
});

test('extractMergeReadyFromJudgeFiles filters paths', () => {
  const rows = extractMergeReadyFromJudgeFiles([
    { path: 'evidence/judges/portfolio/fresh-judge-1.json', content: '{"merge_ready":"no"}' },
    { path: 'README.md', content: '{"merge_ready":"yes"}' },
  ]);
  assert.equal(rows.length, 1);
  assert.equal(rows[0].merge_ready, 'no');
});

test('validateWakePacket accepts complete packet', () => {
  const packet = {
    schema_version: '1.0',
    kind: 'junior_exception_wake',
    tip_sha: '760827dbb46c803475fa095c19984db61c8a6995',
    fail_evidence_paths: ['evidence/judges/portfolio/fresh-judge-1.json'],
    write_scope: [],
    allowed_decisions: ['reject', 'rebind_scope', 'escalate'],
    fail_class: 'abc',
    strike_count: 1,
    lock_or_interface_cite: null,
    notes_zh: '测试',
  };
  const r = validateWakePacket(packet);
  assert.equal(r.ok, true);
});

test('validateWakePacket rejects missing fields', () => {
  const r = validateWakePacket({ schema_version: '1.0' });
  assert.equal(r.ok, false);
  assert.ok(r.errors.some((e) => e.includes('missing')));
});

test('extractJsonPacket from fenced block', () => {
  const text = '前置\n```json\n{"schema_version":"1.0","kind":"junior_exception_wake"}\n```\n';
  const p = extractJsonPacket(text);
  assert.equal(p.schema_version, '1.0');
});

test('validateCrossLaneCite requires lock cite for multi-root scope', () => {
  const bad = validateCrossLaneCite({
    write_scope: ['docs/a.md', 'scripts/b.mjs'],
    lock_or_interface_cite: null,
  });
  assert.equal(bad.ok, false);
  const good = validateCrossLaneCite({
    write_scope: ['docs/a.md', 'scripts/b.mjs'],
    lock_or_interface_cite: 'integration/upstreams.lock.json',
  });
  assert.equal(good.ok, true);
});

test('failClassHash stable and strike halt at 2', () => {
  const h1 = failClassHash(['a', 'b']);
  const h2 = failClassHash(['b', 'a']);
  assert.equal(h1, h2);
  assert.equal(failClassLabel(h1), `fail-class:${h1}`);
  const one = countFailClassStrikes({
    labels: [failClassLabel(h1)],
    hash: h1,
  });
  assert.equal(one.strike_count, 1);
  assert.equal(one.halt, false);
  const two = countFailClassStrikes({
    labels: [failClassLabel(h1), `fail-class:${h1}-2`],
    hash: h1,
  });
  assert.equal(two.halt, true);
  assert.equal(nextStrikeLabel(h1, 1), `fail-class:${h1}-2`);
});

test('idempotency hop keys and markers', () => {
  const key = hopKey({ hop: 'd037', subject: 88, tip_sha: '760827dabc' });
  assert.equal(key, 'zh:d037:88@760827d');
  const claim = claimMarker(key);
  const done = doneMarker(key);
  assert.match(claim, /zh-claim:/);
  assert.match(done, /zh-done:/);
  const blocked = evaluateIdempotency({
    labels: ['zh-dispatched'],
    markerBodies: [done],
    key,
  });
  assert.equal(blocked.proceed, false);
  const ok = evaluateIdempotency({ labels: [], markerBodies: [], key });
  assert.equal(ok.proceed, true);
});

test('candidate branch convention', () => {
  assert.equal(
    candidateBranchName('760827dbb46c803475fa095c19984db61c8a6995'),
    'candidate/portfolio-760827d'
  );
  assert.equal(isCandidateBranch('candidate/portfolio-760827d'), true);
  assert.equal(isCandidateBranch('main'), false);
  assert.throws(() => candidateBranchName('abc'), /7 hex/);
});

test('parseChiefPage marker', () => {
  const p = parseChiefPage(`<!-- continuityops-chief-page-v1 -->
reason: 卡住了
issue_ids: [88, 91]
recommended_action: intervene_pipeline
context_remaining: 40%
`);
  assert.ok(p);
  assert.equal(p.reason, '卡住了');
  assert.deepEqual(p.issue_ids, [88, 91]);
  assert.equal(p.recommended_action, 'intervene_pipeline');
  assert.equal(parseChiefPage('no marker'), null);
});
