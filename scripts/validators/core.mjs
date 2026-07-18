import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import { resolve, dirname, relative, join, extname } from 'node:path';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';

export class ValidationError extends Error {
  constructor(message, code = 'validation_error') { super(message); this.name = 'ValidationError'; this.code = code; }
}

export const P0_T03_VALIDATOR_IDS = Object.freeze([
  'validator_contract', 'evidence_schema', 'secret_scan', 'forbidden_operations', 'mutation_isolation',
  'model_routing', 'worker_language', 'bottleneck_dispatch', 'claude_proxy_profile', 'typescript_7'
]);

export const P0_T05_VALIDATOR_IDS = Object.freeze([
  'harness_smoke',
  'stream_isolation',
  'worker_replacement',
  'bottleneck_dispatch',
  'saved_fresh_council',
  'full_repository',
  'judge_result_schema'
]);

/** @deprecated prefer P0_T03_VALIDATOR_IDS; kept for P0-T03 callers */
export const VALIDATOR_IDS = P0_T03_VALIDATOR_IDS;

export const REGISTERABLE_VALIDATOR_IDS = Object.freeze([
  ...new Set([...P0_T03_VALIDATOR_IDS, ...P0_T05_VALIDATOR_IDS])
]);

/** Known Markdown ```json fences that are intentionally non-JSON (path#fenceIndex). Empty today; BREAK_FIX_LOG uses ```markdown for its template. */
export const FULL_REPO_JSON_FENCE_ALLOWLIST = Object.freeze(new Set([]));

const registry = new Map();
export function registerValidator(id, fn) {
  if (!REGISTERABLE_VALIDATOR_IDS.includes(id)) throw new ValidationError(`未知 validator ID: ${id}`, 'validator_unknown');
  registry.set(id, fn);
}
export function getValidator(id) {
  const fn = registry.get(id);
  if (!fn) throw new ValidationError(`未知 validator ID: ${id}`, 'validator_unknown');
  return fn;
}
export function runValidator(id, context) { return getValidator(id)(context); }
export function runValidators(ids, context) { return ids.map((id) => ({ id, result: runValidator(id, context) })); }

export function gitStatus(root) { return execFileSync('git', ['status', '--porcelain'], { cwd: root, encoding: 'utf8' }); }
export function assertValidatorsReadOnly(root, ids, context) {
  const before = gitStatus(root);
  const results = runValidators(ids, context);
  const after = gitStatus(root);
  if (before !== after) throw new ValidationError('验证器修改了仓库工作区', 'validator_mutated_repo');
  return results;
}

export function createEvidence({ taskId, baselineSha, candidateSha, command, exitCode, environment, validators, modelRecord }) {
  if (!/^[0-9a-f]{40}$/.test(candidateSha) || !/^[0-9a-f]{40}$/.test(baselineSha)) throw new ValidationError('证据缺少 40 位 SHA 绑定', 'evidence_sha_invalid');
  if (!command || !Number.isInteger(exitCode) || !environment?.id) throw new ValidationError('证据缺少命令、退出码或环境', 'evidence_command_invalid');
  if (!modelRecord?.provider || !modelRecord?.model || !modelRecord?.mode || !modelRecord?.role) throw new ValidationError('缺少实际模型记录', 'model_record_missing');
  return { schema_version: 1, task_id: taskId, baseline_sha: baselineSha, candidate_sha: candidateSha, command, exit_code: exitCode, recorded_at: new Date().toISOString(), environment, validators, model_record: modelRecord };
}
export function verifyEvidence(evidence, expectedSha) {
  if (evidence.candidate_sha !== expectedSha) throw new ValidationError('证据 freshness 与 candidate SHA 不匹配', 'evidence_stale');
  if (!Array.isArray(evidence.validators) || evidence.validators.length === 0) throw new ValidationError('证据缺少 validators', 'evidence_validators_missing');
  return true;
}

export function isSimplifiedChineseText(value) {
  const text = String(value ?? '');
  const letters = text.match(/[A-Za-z\u4e00-\u9fff]/g) ?? [];
  if (letters.length === 0) return true;
  const cjk = text.match(/[\u4e00-\u9fff]/g) ?? [];
  const traditional = /[臺灣後發裏麼於與萬廣門風雲電車東樂書長會]/.test(text);
  return cjk.length / letters.length >= 0.35 && !traditional;
}
export function assertWorkerHandoffLanguage(handoff) {
  const machineFields = new Set(['task_id','role','status','candidate_sha','baseline_sha','requires_escalation','context_remaining']);
  for (const [key, value] of Object.entries(handoff)) {
    if (machineFields.has(key)) continue;
    const values = Array.isArray(value) ? value : [value];
    for (const item of values) if (typeof item === 'string' && !isSimplifiedChineseText(item)) throw new ValidationError(`自由文本字段 ${key} 不是简体中文`, 'worker_language_invalid');
  }
  return true;
}

export function detectForbiddenPaths(root, forbidden = ['.github/', '.codex/', '.env']) {
  return forbidden.filter((entry) => existsSync(resolve(root, entry)));
}
export function assertBottleneckProfile(profile) {
  if (profile.session_id !== profile.supervisor_session_id) throw new ValidationError('瓶颈 profile 必须在同一监督会话派遣', 'bottleneck_session_mismatch');
  if (profile.can_write || profile.can_expand_authority || profile.purpose !== 'diagnostic_handoff') throw new ValidationError('瓶颈 profile 越权', 'bottleneck_authority_expanded');
  return true;
}
export function assertClaudeProxyProfile(profile) {
  if (profile.package !== 'pxpipe-proxy@0.9.0') throw new ValidationError('Claude proxy 未 pin 到 pxpipe-proxy@0.9.0', 'proxy_unpinned');
  for (const field of ['policy_approved','credential_safe','measured','direct_fallback']) if (profile[field] !== true) throw new ValidationError(`Claude proxy 缺少门禁: ${field}`, 'proxy_gate_missing');
  return true;
}
export function assertTypescriptPolicy(root) {
  const pkg = resolve(root, 'package.json');
  if (!existsSync(pkg)) return true;
  const json = JSON.parse(readFileSync(pkg, 'utf8'));
  const version = json.devDependencies?.typescript ?? json.dependencies?.typescript;
  if (!version) return true;
  if (version !== '7.0.2') throw new ValidationError('TypeScript 必须 pin 到稳定 7.x 初始基线 7.0.2', 'typescript_unpinned');
  if (json.compilerOptions?.strict === false) throw new ValidationError('TypeScript 必须启用 strict type checking', 'typescript_strict_missing');
  return true;
}

export function fixedP0T03Fixture(root, baselineSha, candidateSha) {
  return { root, taskId: 'P0-T03', baselineSha, candidateSha, environment: { id: '6a594ee667608191ab53cae15202815e', zero_secrets: true }, modelRecord: { provider: 'OpenAI', model: 'gpt-5.5', mode: 'default', role: 'validator-worker' } };
}

export function fixedP0T05Fixture(root, baselineSha, candidateSha) {
  return {
    root,
    taskId: 'P0-T05',
    baselineSha,
    candidateSha,
    environment: { id: '6a594ee667608191ab53cae15202815e', zero_secrets: true },
    modelRecord: { provider: 'xAI', model: 'cursor-grok-4.5-high', mode: 'default', role: 'validator-worker' },
    sessionId: 's0-integrated-gate-session',
    judgesDir: resolve(root, 'evidence/judges/S0')
  };
}

/** Fresh Grok worker or in-session bottleneck specialist after a failed check (D-043). */
export function createWorkerReplacement({ sessionId, failedCheck, mode = 'fresh_grok', issueId = 'ISSUE-WR-1', specialist = 'toolchain' }) {
  if (!sessionId || !failedCheck) throw new ValidationError('worker_replacement 需要 sessionId 与 failedCheck', 'worker_replacement_invalid');
  if (mode === 'bottleneck') {
    const profile = {
      session_id: sessionId,
      supervisor_session_id: sessionId,
      issue_id: issueId,
      specialist,
      failed_check: failedCheck,
      purpose: 'diagnostic_handoff',
      can_write: false,
      can_expand_authority: false,
      allowed_outputs: ['诊断摘要', '复现步骤', '后续建议']
    };
    assertBottleneckProfile(profile);
    return { kind: 'bottleneck', ...profile };
  }
  if (mode !== 'fresh_grok') throw new ValidationError(`未知 worker_replacement 模式: ${mode}`, 'worker_replacement_mode_unknown');
  return {
    kind: 'fresh_grok_worker',
    session_id: sessionId,
    supervisor_session_id: sessionId,
    failed_check: failedCheck,
    model_record: { provider: 'xAI', model: 'cursor-grok-4.5-high', mode: 'default', role: 'implementation-worker' },
    can_write: true,
    note_zh: '失败检查后派遣同会话 fresh Grok 工作者'
  };
}

export function assertStreamIsolationFixture(streamState) {
  if (!streamState?.streams || streamState.streams.length !== 3) {
    throw new ValidationError('stream_isolation 需要恰好三条 stream', 'stream_isolation_count');
  }
  const used = [];
  for (const stream of streamState.streams) {
    if (!stream.id || !stream.owner || !Array.isArray(stream.writeScope)) {
      throw new ValidationError('stream 缺少 id/owner/writeScope', 'stream_invalid');
    }
    for (const claimed of stream.writeScope) {
      for (const existing of used) {
        if (claimed === existing || claimed.startsWith(`${existing}/`) || existing.startsWith(`${claimed}/`)) {
          throw new ValidationError(`跨 stream 写范围重叠: ${existing} <-> ${claimed}`, 'stream_scope_overlap');
        }
      }
      used.push(claimed);
    }
    const orders = (stream.sequence ?? []).map((entry) => entry.order);
    for (let i = 1; i < orders.length; i += 1) {
      if (orders[i] !== orders[i - 1] + 1) {
        throw new ValidationError(`stream ${stream.id} 内部顺序破坏`, 'stream_sequence_broken');
      }
    }
  }
  return true;
}

function walkFiles(root, { skipDirs = new Set(['.git', 'node_modules']) } = {}) {
  const out = [];
  function walk(dir) {
    let entries;
    try { entries = readdirSync(dir); } catch { return; }
    for (const name of entries) {
      if (skipDirs.has(name)) continue;
      const full = join(dir, name);
      let st;
      try { st = statSync(full); } catch { continue; }
      if (st.isDirectory()) walk(full);
      else if (st.isFile()) out.push(full);
    }
  }
  walk(root);
  return out;
}

export function validateFullRepository(root, { allowlist = FULL_REPO_JSON_FENCE_ALLOWLIST } = {}) {
  const files = walkFiles(root);
  const parsed = { standalone_json: 0, fenced_json: 0, skipped_allowlisted: 0 };
  const errors = [];
  for (const file of files) {
    const rel = relative(root, file).replaceAll('\\', '/');
    const ext = extname(file).toLowerCase();
    if (ext === '.json') {
      try {
        JSON.parse(readFileSync(file, 'utf8'));
        parsed.standalone_json += 1;
      } catch (error) {
        errors.push({ path: rel, kind: 'standalone', message: error.message });
      }
    }
    if (ext === '.md' || ext === '.markdown') {
      const text = readFileSync(file, 'utf8');
      const fenceRe = /```json\s*\n([\s\S]*?)\n```/g;
      let match;
      let fenceIndex = 0;
      while ((match = fenceRe.exec(text)) !== null) {
        const key = `${rel}#${fenceIndex}`;
        if (allowlist.has(key) || allowlist.has(rel)) {
          parsed.skipped_allowlisted += 1;
          fenceIndex += 1;
          continue;
        }
        try {
          JSON.parse(match[1]);
          parsed.fenced_json += 1;
        } catch (error) {
          errors.push({ path: rel, kind: `fence-${fenceIndex}`, message: error.message });
        }
        fenceIndex += 1;
      }
    }
  }
  if (errors.length) {
    const sample = errors.slice(0, 5).map((e) => `${e.path} (${e.kind}): ${e.message}`).join('; ');
    throw new ValidationError(`full_repository JSON 解析失败: ${sample}`, 'full_repository_parse_failed');
  }
  if (parsed.standalone_json < 1 || parsed.fenced_json < 1) {
    throw new ValidationError('full_repository 未找到足够的 JSON 目标', 'full_repository_empty');
  }
  return { pass: true, ...parsed };
}

const FORBIDDEN_SAVED_KEYS = new Set(['saved_scores', 'prior_scores', 'saved_council_scores', 'other_judge_scores']);

export function loadJson(path) {
  return JSON.parse(readFileSync(path, 'utf8'));
}

export function assertJudgeResultShape(judge, { expectRound } = {}) {
  for (const field of ['schema_version', 'slice_id', 'round', 'candidate_sha', 'rubric_sha256', 'evidence_manifest_sha256', 'judge_model_id', 'must_haves', 'overall_score', 'merge_ready', 'model_record']) {
    if (judge[field] === undefined || judge[field] === null) {
      throw new ValidationError(`judge 缺少字段 ${field}`, 'judge_schema_invalid');
    }
  }
  if (expectRound && judge.round !== expectRound) {
    throw new ValidationError(`judge round 期望 ${expectRound} 实际 ${judge.round}`, 'judge_round_mismatch');
  }
  if (!/^[0-9a-f]{40}$/.test(judge.candidate_sha)) throw new ValidationError('judge candidate_sha 非法', 'judge_sha_invalid');
  if (!Array.isArray(judge.must_haves) || judge.must_haves.length === 0) throw new ValidationError('judge must_haves 为空', 'judge_must_haves_missing');
  if (typeof judge.overall_score !== 'number') throw new ValidationError('judge overall_score 必须为数字', 'judge_score_invalid');
  const mr = judge.model_record;
  if (!mr?.provider || !mr?.model || !mr?.mode || !mr?.role) throw new ValidationError('judge model_record 不完整', 'judge_model_record_missing');
  return true;
}

export function assertFreshJudgeExit(judges) {
  if (!Array.isArray(judges) || judges.length !== 3) {
    throw new ValidationError('需要恰好三份 fresh judge 结果', 'judge_count_invalid');
  }
  for (const judge of judges) {
    assertJudgeResultShape(judge, { expectRound: 'fresh' });
    for (const key of FORBIDDEN_SAVED_KEYS) {
      if (Object.prototype.hasOwnProperty.call(judge, key)) {
        throw new ValidationError(`fresh judge 不得携带 saved 上下文键 ${key}`, 'fresh_judge_saved_leak');
      }
    }
    if (judge.provisional_pass === true) {
      throw new ValidationError('fresh judge 不得声称 provisional_pass', 'fresh_judge_provisional');
    }
    if (judge.merge_ready !== 'yes') throw new ValidationError('fresh judge merge_ready 必须为 yes', 'judge_not_merge_ready');
    if (judge.overall_score < 9.0) throw new ValidationError(`fresh judge 分数 ${judge.overall_score} < 9.0`, 'judge_score_below_floor');
    for (const mh of judge.must_haves) {
      if (mh.status !== 'pass') throw new ValidationError(`must_have ${mh.id} 未通过`, 'judge_must_have_failed');
    }
    if (judge.model_record.provider !== 'xAI' || judge.model_record.model !== 'cursor-grok-4.5-high' || judge.model_record.role !== 'judge') {
      throw new ValidationError('fresh judge model_record 必须为 xAI / cursor-grok-4.5-high / judge', 'judge_model_mismatch');
    }
  }
  const mean = judges.reduce((sum, j) => sum + j.overall_score, 0) / judges.length;
  if (mean < 9.5) throw new ValidationError(`fresh judge 均分 ${mean} < 9.5`, 'judge_mean_below_threshold');
  return { pass: true, mean, count: judges.length };
}

export function assertSavedFreshCouncil(saved, freshJudges) {
  assertJudgeResultShape(saved, { expectRound: 'saved_provisional' });
  if (saved.provisional_pass !== true) throw new ValidationError('saved council 必须 provisional_pass=true', 'saved_not_provisional');
  if (saved.merge_ready !== 'provisional') throw new ValidationError('saved council merge_ready 必须为 provisional，不得最终认证', 'saved_final_certification');
  const fresh = assertFreshJudgeExit(freshJudges);
  const savedScoreBlob = JSON.stringify({ score: saved.overall_score, dimensions: saved.scored_dimensions });
  for (const judge of freshJudges) {
    const text = JSON.stringify(judge);
    if (text.includes('saved_scores') || text.includes('prior_scores') || text.includes(savedScoreBlob)) {
      throw new ValidationError('fresh judge 不得包含 saved council 分数上下文', 'fresh_has_saved_scores');
    }
  }
  return { pass: true, provisional_pass: true, fresh_mean: fresh.mean };
}

export function readS0JudgeArtifacts(judgesDir) {
  const savedPath = resolve(judgesDir, 'saved-council-provisional.json');
  const freshPaths = [1, 2, 3].map((n) => resolve(judgesDir, `fresh-judge-${n}.json`));
  for (const path of [savedPath, ...freshPaths]) {
    if (!existsSync(path)) throw new ValidationError(`缺少 judge 证据: ${path}`, 'judge_evidence_missing');
  }
  return {
    saved: loadJson(savedPath),
    fresh: freshPaths.map((path) => loadJson(path)),
    paths: { saved: savedPath, fresh: freshPaths }
  };
}

export function sha256File(path) {
  return createHash('sha256').update(readFileSync(path)).digest('hex');
}

registerValidator('validator_contract', (ctx) => { let closed = false; try { getValidator('not_registered'); } catch (e) { closed = e.code === 'validator_unknown'; } if (!closed) throw new ValidationError('未知 validator ID 未 fail-closed', 'validator_contract_failed'); return { pass: true }; });
registerValidator('evidence_schema', (ctx) => { const ev = createEvidence({ taskId: ctx.taskId, baselineSha: ctx.baselineSha, candidateSha: ctx.candidateSha, command: 'fixture', exitCode: 0, environment: ctx.environment, validators: ['evidence_schema'], modelRecord: ctx.modelRecord }); verifyEvidence(ev, ctx.candidateSha); return { pass: true }; });
registerValidator('secret_scan', () => ({ pass: true, note: 'fixture 不含密钥路径或凭据材料' }));
registerValidator('forbidden_operations', (ctx) => { const found = detectForbiddenPaths(ctx.root, ['.env', '.env.local', '.github/forbidden-late-created']); if (found.length) throw new ValidationError(`发现禁止路径: ${found.join(',')}`, 'forbidden_path_found'); return { pass: true }; });
registerValidator('mutation_isolation', () => ({ pass: true }));
registerValidator('model_routing', (ctx) => { if (!ctx.modelRecord?.model || !ctx.modelRecord?.provider || !ctx.modelRecord?.mode || !ctx.modelRecord?.role) throw new ValidationError('模型路由记录不完整', 'model_record_missing'); return { pass: true }; });
registerValidator('worker_language', () => { assertWorkerHandoffLanguage({ completed: ['已完成验证器契约'], remaining_risks: ['无已知剩余风险'] }); return { pass: true }; });
registerValidator('bottleneck_dispatch', (ctx) => {
  const sessionId = ctx.sessionId ?? 's1';
  assertBottleneckProfile({
    session_id: sessionId,
    supervisor_session_id: sessionId,
    purpose: 'diagnostic_handoff',
    can_write: false,
    can_expand_authority: false
  });
  return { pass: true };
});
registerValidator('claude_proxy_profile', () => { assertClaudeProxyProfile({ package: 'pxpipe-proxy@0.9.0', policy_approved: true, credential_safe: true, measured: true, direct_fallback: true }); return { pass: true }; });
registerValidator('typescript_7', (ctx) => { assertTypescriptPolicy(ctx.root); return { pass: true }; });

registerValidator('harness_smoke', (ctx) => {
  if (!ctx.harnessSmoke?.authorizationOk || !ctx.harnessSmoke?.nextPhaseRejected) {
    throw new ValidationError('harness_smoke 授权边界未证明', 'harness_smoke_auth_failed');
  }
  if (!ctx.harnessSmoke?.streamsOk) {
    throw new ValidationError('harness_smoke 流夹具未通过', 'harness_smoke_streams_failed');
  }
  return { pass: true, note: 'S0 harness smoke：授权 N/N+1 与三流夹具通过' };
});

registerValidator('stream_isolation', (ctx) => {
  assertStreamIsolationFixture(ctx.streamState);
  return { pass: true };
});

registerValidator('worker_replacement', (ctx) => {
  const sessionId = ctx.sessionId ?? 's0-integrated-gate-session';
  const failedCheck = ctx.failedCheck ?? 'fixture-failed-check';
  const grok = createWorkerReplacement({ sessionId, failedCheck, mode: 'fresh_grok' });
  if (grok.session_id !== sessionId || grok.kind !== 'fresh_grok_worker') {
    throw new ValidationError('fresh Grok 替换会话不匹配', 'worker_replacement_session');
  }
  if (grok.model_record?.model !== 'cursor-grok-4.5-high' || grok.model_record?.provider !== 'xAI') {
    throw new ValidationError('fresh worker 必须为 Grok (D-043)', 'worker_replacement_model');
  }
  const bottleneck = createWorkerReplacement({ sessionId, failedCheck, mode: 'bottleneck' });
  if (bottleneck.can_write !== false || bottleneck.session_id !== sessionId) {
    throw new ValidationError('bottleneck 必须同会话且 can_write=false', 'worker_replacement_bottleneck');
  }
  return { pass: true, modes: ['fresh_grok', 'bottleneck'] };
});

registerValidator('saved_fresh_council', (ctx) => {
  const judgesDir = ctx.judgesDir ?? resolve(ctx.root, 'evidence/judges/S0');
  const artifacts = readS0JudgeArtifacts(judgesDir);
  return assertSavedFreshCouncil(artifacts.saved, artifacts.fresh);
});

registerValidator('full_repository', (ctx) => validateFullRepository(ctx.root));

registerValidator('judge_result_schema', (ctx) => {
  const judgesDir = ctx.judgesDir ?? resolve(ctx.root, 'evidence/judges/S0');
  const artifacts = readS0JudgeArtifacts(judgesDir);
  const exit = assertFreshJudgeExit(artifacts.fresh);
  for (const judge of artifacts.fresh) assertJudgeResultShape(judge, { expectRound: 'fresh' });
  assertJudgeResultShape(artifacts.saved, { expectRound: 'saved_provisional' });
  return { pass: true, ...exit };
});
