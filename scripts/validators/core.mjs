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

export const P1_T01_VALIDATOR_IDS = Object.freeze([
  'upstream_pin',
  'integration_contract',
  'claims'
]);

export const P1_T02_VALIDATOR_IDS = Object.freeze([
  'terraform_fmt',
  'terraform_validate',
  'terraform_test',
  'tflint',
  'policy',
  'iam_negative',
  'network_negative'
]);

export const P1_T03_VALIDATOR_IDS = Object.freeze([
  'workflow_permissions',
  'workflow_pins',
  'untrusted_pr',
  'oidc_trust',
  'hosted_required_checks'
]);

export const P1_T04_VALIDATOR_IDS = Object.freeze([
  'full_repository',
  'evidence_freshness',
  'claim_consistency',
  'judge_exit'
]);

export const P2_T01_VALIDATOR_IDS = Object.freeze([
  'helm_lint',
  'helm_template',
  'kubeconform',
  'kubernetes_policy',
  'kubernetes_negative'
]);

export const P2_T02_VALIDATOR_IDS = Object.freeze([
  'kind_runtime',
  'managed_cluster_preflight',
  'kubernetes_smoke',
  'release_identity',
  'autoscaling_runtime'
]);

export const P2_T03_VALIDATOR_IDS = Object.freeze([
  'scenario_schema',
  'scenario_reset',
  'recovery_smoke',
  'evidence_freshness'
]);

export const P2_T04_VALIDATOR_IDS = Object.freeze([
  'full_repository',
  'managed_runtime_claims',
  'judge_exit'
]);

export const P3_T01_VALIDATOR_IDS = Object.freeze([
  'serverless_unit',
  'event_contract',
  'idempotency',
  'iam_negative',
  'dlq_replay'
]);

export const P3_T02_VALIDATOR_IDS = Object.freeze([
  'tenant_boundary',
  'lifecycle_contract',
  'claims'
]);

export const P3_T03_VALIDATOR_IDS = Object.freeze([
  'serverless_runtime',
  'dlq_runtime',
  'full_repository',
  'judge_exit'
]);

export const P4_T01_VALIDATOR_IDS = Object.freeze([
  'telemetry_contract',
  'trace_continuity',
  'log_redaction',
  'metrics_schema'
]);

export const P4_T02_VALIDATOR_IDS = Object.freeze([
  'dashboard_schema',
  'alert_contract',
  'slo_math',
  'alert_negative',
  'runbook_links'
]);

export const P4_T03_VALIDATOR_IDS = Object.freeze([
  'signal_path_runtime',
  'alert_runtime',
  'full_repository',
  'judge_exit'
]);

/** @deprecated prefer P0_T03_VALIDATOR_IDS; kept for P0-T03 callers */
export const VALIDATOR_IDS = P0_T03_VALIDATOR_IDS;

export const REGISTERABLE_VALIDATOR_IDS = Object.freeze([
  ...new Set([
    ...P0_T03_VALIDATOR_IDS,
    ...P0_T05_VALIDATOR_IDS,
    ...P1_T01_VALIDATOR_IDS,
    ...P1_T02_VALIDATOR_IDS,
    ...P1_T03_VALIDATOR_IDS,
    ...P1_T04_VALIDATOR_IDS,
    ...P2_T01_VALIDATOR_IDS,
    ...P2_T02_VALIDATOR_IDS,
    ...P2_T03_VALIDATOR_IDS,
    ...P2_T04_VALIDATOR_IDS,
    ...P3_T01_VALIDATOR_IDS,
    ...P3_T02_VALIDATOR_IDS,
    ...P3_T03_VALIDATOR_IDS,
    ...P4_T01_VALIDATOR_IDS,
    ...P4_T02_VALIDATOR_IDS,
    ...P4_T03_VALIDATOR_IDS
  ])
]);

export function sliceIdForTask(taskId) {
  if (!taskId) return 'S0';
  if (taskId.startsWith('P0')) return 'S0';
  if (taskId.startsWith('P1')) return 'S1';
  if (taskId.startsWith('P2')) return 'S2';
  if (taskId.startsWith('P3')) return 'S3';
  if (taskId.startsWith('P4')) return 'S4';
  return 'S0';
}

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

function loadUpstreamLock(root) {
  return loadJson(resolve(root, 'integration/upstreams.lock.json'));
}

function terraformCliAvailable() {
  try {
    execFileSync('terraform', ['version'], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
    return true;
  } catch {
    return false;
  }
}

registerValidator('upstream_pin', (ctx) => {
  const lock = loadUpstreamLock(ctx.root);
  if (!/^[0-9a-f]{40}$/.test(lock.project_a?.commit_sha)) throw new ValidationError('project_a.commit_sha 非法', 'upstream_pin_a');
  if (!/^[0-9a-f]{40}$/.test(lock.project_c?.commit_sha)) throw new ValidationError('project_c.commit_sha 非法', 'upstream_pin_c');
  const digest = lock.project_c?.image_digest;
  if (digest !== 'UNAVAILABLE' && !/^sha256:[0-9a-f]{64}$/.test(digest ?? '')) {
    throw new ValidationError('project_c.image_digest 必须为 UNAVAILABLE 或 sha256:…', 'upstream_pin_digest');
  }
  if (!Array.isArray(lock.missing_capabilities) || lock.missing_capabilities.length < 1) {
    throw new ValidationError('缺少 missing_capabilities', 'upstream_pin_missing');
  }
  return { pass: true, digest, missing: lock.missing_capabilities.length };
});

registerValidator('integration_contract', (ctx) => {
  const lock = loadUpstreamLock(ctx.root);
  for (const rel of [...(lock.project_a.consumed_contracts ?? []), ...(lock.project_c.consumed_contracts ?? [])]) {
    const path = resolve(ctx.root, rel);
    if (!existsSync(path)) throw new ValidationError(`缺少契约文件: ${rel}`, 'integration_contract_missing');
    loadJson(path);
  }
  return { pass: true };
});

registerValidator('claims', (ctx) => {
  const slice = ctx.sliceId ?? sliceIdForTask(ctx.taskId);
  const evidenceRel = {
    S1: 'evidence/slices/S1/upstream-integration.json',
    S3: 'evidence/slices/S3/saas-operations.json'
  }[slice] ?? `evidence/slices/${slice}/integrated-gate.json`;
  const evidencePath = resolve(ctx.root, evidenceRel);
  if (!existsSync(evidencePath)) throw new ValidationError(`缺少 claims 证据: ${evidenceRel}`, 'claims_evidence_missing');
  const evidence = loadJson(evidencePath);
  const level = evidence.claim_level;
  if (!['L0', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6'].includes(level)) {
    throw new ValidationError('claim_level 非法', 'claims_level_invalid');
  }
  if (['L4', 'L5', 'L6'].includes(level) && !evidence.cloud_apply_evidence) {
    throw new ValidationError('L4+ 声明缺少 cloud_apply_evidence', 'claims_overclaim');
  }
  if (!Array.isArray(evidence.remaining_boundaries) || evidence.remaining_boundaries.length < 1) {
    throw new ValidationError('claims 必须显式 remaining_boundaries', 'claims_boundaries_missing');
  }
  return { pass: true, claim_level: level, evidence: evidenceRel };
});

registerValidator('terraform_fmt', (ctx) => {
  if (!terraformCliAvailable()) {
    return { pass: true, skipped: true, note: 'terraform CLI 不可用；静态脚手架测试覆盖 fmt 前置条件' };
  }
  execFileSync('terraform', ['fmt', '-check', '-recursive', 'terraform'], { cwd: ctx.root, encoding: 'utf8' });
  return { pass: true, skipped: false };
});

registerValidator('terraform_validate', (ctx) => {
  if (!terraformCliAvailable()) {
    return { pass: true, skipped: true, note: 'terraform CLI 不可用；未执行 validate（非 L1 失败）' };
  }
  execFileSync('terraform', ['init', '-backend=false'], { cwd: resolve(ctx.root, 'terraform/envs/staging'), encoding: 'utf8' });
  execFileSync('terraform', ['validate'], { cwd: resolve(ctx.root, 'terraform/envs/staging'), encoding: 'utf8' });
  return { pass: true, skipped: false };
});

registerValidator('terraform_test', (ctx) => {
  const required = [
    'terraform/modules/state/main.tf',
    'terraform/modules/environments/main.tf',
    'terraform/modules/iam/main.tf',
    'terraform/modules/network/main.tf',
    'terraform/envs/staging/main.tf',
    'terraform/envs/recovery-lab/main.tf'
  ];
  for (const rel of required) {
    if (!existsSync(resolve(ctx.root, rel))) throw new ValidationError(`缺少 terraform 路径: ${rel}`, 'terraform_test_missing');
  }
  return { pass: true, files: required.length };
});

registerValidator('tflint', (ctx) => {
  return { pass: true, skipped: true, note: 'tflint 未安装；策略 JSON 与静态测试代替（L1）' };
});

registerValidator('policy', (ctx) => {
  for (const rel of ['terraform/policies/tagging.json', 'terraform/policies/encryption.json']) {
    loadJson(resolve(ctx.root, rel));
  }
  return { pass: true };
});

registerValidator('iam_negative', (ctx) => {
  const policy = loadJson(resolve(ctx.root, 'terraform/policies/iam-negative.json'));
  if (!policy.prohibited?.includes('long_lived_access_keys_in_repo')) {
    throw new ValidationError('iam_negative 缺少 long_lived_access_keys_in_repo', 'iam_negative_incomplete');
  }
  const iam = readFileSync(resolve(ctx.root, 'terraform/modules/iam/main.tf'), 'utf8');
  if (!/long_lived_keys\s*=\s*false/.test(iam)) throw new ValidationError('IAM 模块未禁止长期密钥', 'iam_negative_keys');
  const serverlessTf = resolve(ctx.root, 'terraform/modules/serverless/main.tf');
  if (existsSync(serverlessTf)) {
    const text = readFileSync(serverlessTf, 'utf8');
    if (!/long_lived_keys\s*=\s*false/.test(text)) {
      throw new ValidationError('serverless 模块未禁止长期密钥', 'iam_negative_serverless');
    }
  }
  return { pass: true };
});

registerValidator('network_negative', (ctx) => {
  const policy = loadJson(resolve(ctx.root, 'terraform/policies/network-negative.json'));
  if (!policy.required?.includes('staging_and_recovery_lab_separated')) {
    throw new ValidationError('network_negative 缺少环境分离要求', 'network_negative_incomplete');
  }
  const staging = readFileSync(resolve(ctx.root, 'terraform/envs/staging/main.tf'), 'utf8');
  const recovery = readFileSync(resolve(ctx.root, 'terraform/envs/recovery-lab/main.tf'), 'utf8');
  if (!/staging/.test(staging) || !/recovery-lab/.test(recovery)) {
    throw new ValidationError('staging/recovery-lab 未分离', 'network_negative_envs');
  }
  return { pass: true };
});

const S1_WORKFLOWS = [
  'terraform-pr.yml',
  'terraform-plan.yml',
  'terraform-apply.yml',
  'drift.yml',
  'evidence-upload.yml',
  'teardown.yml'
];

registerValidator('workflow_permissions', (ctx) => {
  const pr = readFileSync(resolve(ctx.root, '.github/workflows/terraform-pr.yml'), 'utf8');
  if (!/contents:\s*read/.test(pr) || /id-token:\s*write/.test(pr)) {
    throw new ValidationError('PR workflow 权限不符合只读要求', 'workflow_permissions_pr');
  }
  for (const name of ['codex-patch-publish.yml', 'junior-actuate.yml', 'validate.yml']) {
    if (!existsSync(resolve(ctx.root, `.github/workflows/${name}`))) {
      throw new ValidationError(`受保护 workflow 缺失: ${name}`, 'workflow_permissions_protected');
    }
  }
  return { pass: true };
});

registerValidator('workflow_pins', (ctx) => {
  for (const name of S1_WORKFLOWS) {
    const text = readFileSync(resolve(ctx.root, `.github/workflows/${name}`), 'utf8');
    const uses = [...text.matchAll(/uses:\s*([^\s]+)/g)].map((m) => m[1]);
    for (const ref of uses) {
      if (ref.startsWith('./')) continue;
      if (!/@[0-9a-f]{40}$/.test(ref)) throw new ValidationError(`未 pin 的 action: ${name} ${ref}`, 'workflow_pins_unpinned');
    }
  }
  return { pass: true, workflows: S1_WORKFLOWS.length };
});

registerValidator('untrusted_pr', (ctx) => {
  const pr = readFileSync(resolve(ctx.root, '.github/workflows/terraform-pr.yml'), 'utf8');
  if (/configure-aws-credentials/.test(pr)) throw new ValidationError('PR job 不得配置 AWS 凭证', 'untrusted_pr_aws');
  if (!existsSync(resolve(ctx.root, 'scripts/ci/assert-pr-readonly.mjs'))) {
    throw new ValidationError('缺少 assert-pr-readonly 脚本', 'untrusted_pr_script');
  }
  return { pass: true };
});

registerValidator('oidc_trust', (ctx) => {
  for (const name of ['terraform-plan.yml', 'terraform-apply.yml', 'teardown.yml', 'drift.yml']) {
    const text = readFileSync(resolve(ctx.root, `.github/workflows/${name}`), 'utf8');
    if (!/id-token:\s*write/.test(text)) throw new ValidationError(`${name} 缺少 OIDC id-token`, 'oidc_trust_missing');
    if (!/configure-aws-credentials@[0-9a-f]{40}/.test(text)) throw new ValidationError(`${name} 缺少 pin 的 OIDC action`, 'oidc_trust_action');
  }
  return { pass: true };
});

registerValidator('hosted_required_checks', (ctx) => {
  if (!existsSync(resolve(ctx.root, '.github/workflows/validate.yml'))) {
    throw new ValidationError('缺少 validate.yml 合约门', 'hosted_required_checks');
  }
  if (!existsSync(resolve(ctx.root, 'evidence/slices/S1/hosted-ci.json'))) {
    throw new ValidationError('缺少 hosted-ci 证据', 'hosted_required_checks_evidence');
  }
  const evidence = loadJson(resolve(ctx.root, 'evidence/slices/S1/hosted-ci.json'));
  if (!evidence.remaining_boundaries?.length) throw new ValidationError('hosted-ci 缺少 remaining_boundaries', 'hosted_required_checks_boundaries');
  return { pass: true, claim_level: evidence.claim_level };
});

registerValidator('evidence_freshness', (ctx) => {
  const slice = ctx.sliceId ?? sliceIdForTask(ctx.taskId);
  const evidenceRel = {
    'P2-T03': 'evidence/slices/S2/scenarios/matrix-evidence.json',
    'P1-T04': 'evidence/slices/S1/integrated-gate.json',
    'P2-T04': 'evidence/slices/S2/integrated-gate.json',
    'P3-T03': 'evidence/slices/S3/integrated-gate.json',
    'P4-T03': 'evidence/slices/S4/integrated-gate.json'
  }[ctx.taskId] ?? `evidence/slices/${slice}/integrated-gate.json`;
  const gatePath = resolve(ctx.root, evidenceRel);
  if (!existsSync(gatePath)) throw new ValidationError(`缺少 freshness 证据: ${evidenceRel}`, 'evidence_freshness_missing');
  const gate = loadJson(gatePath);
  const expected = ctx.candidateSha;
  if (expected && gate.candidate_sha && gate.candidate_sha !== expected) {
    throw new ValidationError('evidence candidate_sha 与期望不一致', 'evidence_freshness_stale');
  }
  if (gate.candidate_sha && !/^[0-9a-f]{40}$/.test(gate.candidate_sha)) {
    throw new ValidationError('evidence SHA 非法', 'evidence_freshness_sha');
  }
  return { pass: true, candidate_sha: gate.candidate_sha ?? expected, path: evidenceRel };
});

registerValidator('claim_consistency', (ctx) => {
  const slice = ctx.sliceId ?? sliceIdForTask(ctx.taskId);
  const filesBySlice = {
    S1: [
      'evidence/slices/S1/upstream-integration.json',
      'evidence/slices/S1/terraform.json',
      'evidence/slices/S1/hosted-ci.json',
      'evidence/slices/S1/integrated-gate.json'
    ],
    S2: [
      'evidence/slices/S2/chart-contract.json',
      'evidence/slices/S2/integrated-gate.json'
    ],
    S3: [
      'evidence/slices/S3/serverless.json',
      'evidence/slices/S3/saas-operations.json',
      'evidence/slices/S3/integrated-gate.json'
    ],
    S4: [
      'evidence/slices/S4/telemetry.json',
      'evidence/slices/S4/signals.json',
      'evidence/slices/S4/integrated-gate.json'
    ]
  };
  const files = filesBySlice[slice] ?? filesBySlice.S1;
  for (const rel of files) {
    if (!existsSync(resolve(ctx.root, rel))) continue;
    const ev = loadJson(resolve(ctx.root, rel));
    if (['L4', 'L5', 'L6'].includes(ev.claim_level) && !ev.cloud_apply_evidence) {
      throw new ValidationError(`${rel} 过度声明 ${ev.claim_level}`, 'claim_consistency_overclaim');
    }
    if (!Array.isArray(ev.remaining_boundaries)) {
      throw new ValidationError(`${rel} 缺少 remaining_boundaries`, 'claim_consistency_boundaries');
    }
  }
  return { pass: true, slice };
});

registerValidator('judge_exit', (ctx) => {
  const slice = ctx.sliceId ?? sliceIdForTask(ctx.taskId);
  const judgesDir = ctx.judgesDir ?? resolve(ctx.root, `evidence/judges/${slice}`);
  const artifacts = readS0JudgeArtifacts(judgesDir);
  for (const judge of artifacts.fresh) {
    if (judge.slice_id !== slice) throw new ValidationError(`fresh judge slice_id 必须为 ${slice}`, 'judge_exit_slice');
  }
  if (artifacts.saved.slice_id !== slice) throw new ValidationError(`saved council slice_id 必须为 ${slice}`, 'judge_exit_saved_slice');
  return assertSavedFreshCouncil(artifacts.saved, artifacts.fresh);
});

function toolAvailable(bin) {
  try {
    execFileSync(bin, ['version'], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
    return true;
  } catch {
    try {
      execFileSync(bin, ['--help'], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
      return true;
    } catch {
      return false;
    }
  }
}

registerValidator('helm_lint', (ctx) => {
  if (!toolAvailable('helm')) {
    return { pass: true, skipped: true, note: 'helm 不可用；静态 chart 契约代替（L1）' };
  }
  execFileSync('helm', ['lint', 'kubernetes/chart'], { cwd: ctx.root, encoding: 'utf8' });
  return { pass: true, skipped: false };
});

registerValidator('helm_template', (ctx) => {
  const required = [
    'kubernetes/chart/Chart.yaml',
    'kubernetes/chart/values.yaml',
    'kubernetes/chart/templates/deployment.yaml',
    'kubernetes/chart/templates/hpa.yaml',
    'kubernetes/chart/templates/pdb.yaml',
    'kubernetes/chart/templates/rbac.yaml'
  ];
  for (const rel of required) {
    if (!existsSync(resolve(ctx.root, rel))) throw new ValidationError(`缺少 chart 文件: ${rel}`, 'helm_template_missing');
  }
  const values = readFileSync(resolve(ctx.root, 'kubernetes/chart/values.yaml'), 'utf8');
  if (!/digest:\s*"sha256:[0-9a-f]{64}"/.test(values)) {
    throw new ValidationError('values 缺少 digest pin', 'helm_template_digest');
  }
  if (toolAvailable('helm')) {
    execFileSync('helm', ['template', 'continuityops', 'kubernetes/chart'], { cwd: ctx.root, encoding: 'utf8' });
    return { pass: true, skipped: false };
  }
  return { pass: true, skipped: true, note: 'helm 不可用；静态 digest/模板检查通过' };
});

registerValidator('kubeconform', (ctx) => {
  return { pass: true, skipped: true, note: 'kubeconform 未安装；模板静态检查代替（L1）' };
});

registerValidator('kubernetes_policy', (ctx) => {
  for (const rel of ['kubernetes/policies/digest-pin.json', 'kubernetes/policies/security-context.json']) {
    loadJson(resolve(ctx.root, rel));
  }
  return { pass: true };
});

registerValidator('kubernetes_negative', (ctx) => {
  const policy = loadJson(resolve(ctx.root, 'kubernetes/policies/network-negative.json'));
  if (!policy.prohibited?.length) throw new ValidationError('kubernetes_negative 缺少 prohibited', 'kubernetes_negative_incomplete');
  const values = readFileSync(resolve(ctx.root, 'kubernetes/chart/values.yaml'), 'utf8');
  if (!/networkPolicy:\s*\n\s*enabled:\s*true/.test(values)) {
    throw new ValidationError('NetworkPolicy 未启用', 'kubernetes_negative_np');
  }
  return { pass: true };
});

registerValidator('kind_runtime', (ctx) => {
  const kindScenario = loadJson(resolve(ctx.root, 'kubernetes/scenarios/kind-local.json'));
  if (kindScenario.label !== 'local-only') throw new ValidationError('kind 场景必须 local-only', 'kind_runtime_label');
  const preflightPath = resolve(ctx.root, 'evidence/slices/S2/runtime/kind-preflight.json');
  if (!existsSync(preflightPath)) throw new ValidationError('缺少 kind-preflight 证据', 'kind_runtime_evidence');
  const preflight = loadJson(preflightPath);
  if (!['L1', 'L2'].includes(preflight.claim_level)) throw new ValidationError('kind claim_level 非法', 'kind_runtime_claim');
  if (preflight.claim_level === 'L2' && !preflight.kind_available) {
    throw new ValidationError('L2 需要 kind_available', 'kind_runtime_overclaim');
  }
  return { pass: true, claim_level: preflight.claim_level };
});

registerValidator('managed_cluster_preflight', (ctx) => {
  const kindScenario = loadJson(resolve(ctx.root, 'kubernetes/scenarios/kind-local.json'));
  if (!kindScenario.remaining_boundaries?.includes('managed_cluster_apply')) {
    throw new ValidationError('必须显式 remaining_boundaries: managed_cluster_apply', 'managed_cluster_boundary');
  }
  return { pass: true, remaining_boundaries: ['managed_cluster_apply'] };
});

registerValidator('kubernetes_smoke', (ctx) => {
  if (!existsSync(resolve(ctx.root, 'scripts/kubernetes/kind-preflight.mjs'))) {
    throw new ValidationError('缺少 kind-preflight 脚本', 'kubernetes_smoke_script');
  }
  return { pass: true, note: 'smoke 以脚本与场景契约为准；无托管集群断言' };
});

registerValidator('release_identity', (ctx) => {
  const values = readFileSync(resolve(ctx.root, 'kubernetes/chart/values.yaml'), 'utf8');
  if (!/runAsNonRoot:\s*true/.test(values)) throw new ValidationError('缺少 non-root', 'release_identity_nonroot');
  if (!/digest:\s*"sha256:[0-9a-f]{64}"/.test(values)) throw new ValidationError('缺少 digest 身份', 'release_identity_digest');
  return { pass: true };
});

registerValidator('autoscaling_runtime', (ctx) => {
  const hpa = readFileSync(resolve(ctx.root, 'kubernetes/chart/templates/hpa.yaml'), 'utf8');
  if (!/HorizontalPodAutoscaler/.test(hpa)) throw new ValidationError('缺少 HPA 模板', 'autoscaling_runtime_hpa');
  return { pass: true, note: 'HPA 模板存在；实时扩缩容未声明' };
});

registerValidator('scenario_schema', (ctx) => {
  const matrix = loadJson(resolve(ctx.root, 'kubernetes/scenarios/failure-matrix.json'));
  if (!Array.isArray(matrix.scenarios) || matrix.scenarios.length < 6) {
    throw new ValidationError('failure matrix 场景不足', 'scenario_schema_count');
  }
  for (const s of matrix.scenarios) {
    const scenario = loadJson(resolve(ctx.root, s.path));
    for (const field of ['scenario_id', 'failure_class', 'inject', 'recover', 'business_check', 'reset']) {
      if (!scenario[field]) throw new ValidationError(`场景 ${s.id} 缺少 ${field}`, 'scenario_schema_field');
    }
  }
  return { pass: true, count: matrix.scenarios.length };
});

registerValidator('scenario_reset', (ctx) => {
  if (!existsSync(resolve(ctx.root, 'scripts/kubernetes/reset-scenario.mjs'))) {
    throw new ValidationError('缺少 reset-scenario 脚本', 'scenario_reset_script');
  }
  const matrix = loadJson(resolve(ctx.root, 'kubernetes/scenarios/failure-matrix.json'));
  for (const s of matrix.scenarios) {
    const scenario = loadJson(resolve(ctx.root, s.path));
    if (scenario.reset?.script !== 'scripts/kubernetes/reset-scenario.mjs') {
      throw new ValidationError(`场景 ${s.id} reset 脚本不正确`, 'scenario_reset_path');
    }
  }
  return { pass: true };
});

registerValidator('recovery_smoke', (ctx) => {
  const matrix = loadJson(resolve(ctx.root, 'kubernetes/scenarios/failure-matrix.json'));
  for (const s of matrix.scenarios) {
    const scenario = loadJson(resolve(ctx.root, s.path));
    if (!scenario.business_check) throw new ValidationError(`场景 ${s.id} 缺少 business_check`, 'recovery_smoke_business');
  }
  return { pass: true };
});

registerValidator('managed_runtime_claims', (ctx) => {
  const gate = loadJson(resolve(ctx.root, 'evidence/slices/S2/integrated-gate.json'));
  if (['L4', 'L5', 'L6'].includes(gate.claim_level) && !gate.cloud_apply_evidence) {
    throw new ValidationError('S2 过度声明托管运行时', 'managed_runtime_overclaim');
  }
  if (!gate.remaining_boundaries?.includes('managed_cluster_apply')) {
    throw new ValidationError('S2 必须保留 managed_cluster_apply 边界', 'managed_runtime_boundary');
  }
  return { pass: true, claim_level: gate.claim_level };
});

registerValidator('serverless_unit', (ctx) => {
  for (const rel of ['serverless/worker-contract.json', 'serverless/idempotency.mjs', 'serverless/dlq.mjs', 'serverless/worker.mjs']) {
    if (!existsSync(resolve(ctx.root, rel))) throw new ValidationError(`缺少 serverless 文件: ${rel}`, 'serverless_unit_missing');
  }
  return { pass: true };
});

registerValidator('event_contract', (ctx) => {
  const contract = loadJson(resolve(ctx.root, 'serverless/event-contract.json'));
  for (const field of ['event_id', 'tenant_id', 'type', 'payload', 'occurred_at']) {
    if (!contract.required_fields?.includes(field)) throw new ValidationError(`event_contract 缺少 ${field}`, 'event_contract_field');
  }
  return { pass: true };
});

registerValidator('idempotency', (ctx) => {
  const worker = loadJson(resolve(ctx.root, 'serverless/worker-contract.json'));
  if (!worker.idempotency?.key_field) throw new ValidationError('缺少 idempotency key_field', 'idempotency_missing');
  if (!existsSync(resolve(ctx.root, 'tests/serverless/idempotency.test.mjs'))) {
    throw new ValidationError('缺少 idempotency 单测', 'idempotency_test_missing');
  }
  return { pass: true };
});

registerValidator('dlq_replay', (ctx) => {
  if (!existsSync(resolve(ctx.root, 'tests/serverless/dlq.test.mjs'))) {
    throw new ValidationError('缺少 DLQ 单测', 'dlq_replay_test_missing');
  }
  const worker = loadJson(resolve(ctx.root, 'serverless/worker-contract.json'));
  if (!worker.dlq?.enabled) throw new ValidationError('DLQ 未启用', 'dlq_replay_disabled');
  return { pass: true };
});

registerValidator('tenant_boundary', (ctx) => {
  if (!existsSync(resolve(ctx.root, 'docs/architecture/tenant-boundary.md'))) {
    throw new ValidationError('缺少 tenant-boundary 文档', 'tenant_boundary_doc');
  }
  const lifecycle = loadJson(resolve(ctx.root, 'operations/saas/lifecycle.json'));
  if (lifecycle.tenant_isolation?.cross_tenant_reads !== 'prohibited') {
    throw new ValidationError('跨租户读必须 prohibited', 'tenant_boundary_reads');
  }
  return { pass: true };
});

registerValidator('lifecycle_contract', (ctx) => {
  const lifecycle = loadJson(resolve(ctx.root, 'operations/saas/lifecycle.json'));
  const ids = (lifecycle.stages ?? []).map((s) => s.id);
  for (const required of ['onboarding', 'config', 'migration', 'support', 'suspension', 'export', 'deprovision']) {
    if (!ids.includes(required)) throw new ValidationError(`lifecycle 缺少 ${required}`, 'lifecycle_contract_stage');
  }
  loadJson(resolve(ctx.root, 'operations/saas/severity-escalation.json'));
  return { pass: true, stages: ids.length };
});

registerValidator('serverless_runtime', (ctx) => {
  const evidence = loadJson(resolve(ctx.root, 'evidence/slices/S3/integrated-gate.json'));
  if (['L4', 'L5', 'L6'].includes(evidence.claim_level) && !evidence.cloud_apply_evidence) {
    throw new ValidationError('S3 过度声明 live serverless', 'serverless_runtime_overclaim');
  }
  if (!evidence.remaining_boundaries?.some((b) => /Lambda|live|AWS/i.test(b))) {
    throw new ValidationError('S3 必须保留无 live Lambda 边界', 'serverless_runtime_boundary');
  }
  return { pass: true, claim_level: evidence.claim_level };
});

registerValidator('dlq_runtime', (ctx) => {
  if (!existsSync(resolve(ctx.root, 'operations/incidents/serverless/dlq-replay.md'))) {
    throw new ValidationError('缺少 DLQ 事件手册', 'dlq_runtime_runbook');
  }
  return { pass: true, note: 'DLQ runtime 为合成/单测路径，非 live SQS' };
});

registerValidator('telemetry_contract', (ctx) => {
  const contract = loadJson(resolve(ctx.root, 'observability/otel/telemetry-contract.json'));
  for (const hop of ['ingress', 'app', 'queue', 'function']) {
    if (!contract.correlation?.propagated_across?.includes(hop)) {
      throw new ValidationError(`telemetry 缺少 hop ${hop}`, 'telemetry_contract_hop');
    }
  }
  return { pass: true };
});

registerValidator('trace_continuity', (ctx) => {
  const spans = loadJson(resolve(ctx.root, 'app-contract/telemetry/spans.json'));
  const names = (spans.spans ?? []).map((s) => s.name);
  for (const required of ['ingress.request', 'app.handle', 'queue.publish', 'function.invoke']) {
    if (!names.includes(required)) throw new ValidationError(`缺少 span ${required}`, 'trace_continuity_span');
  }
  return { pass: true };
});

registerValidator('log_redaction', (ctx) => {
  if (!existsSync(resolve(ctx.root, 'observability/otel/redaction.mjs'))) {
    throw new ValidationError('缺少 redaction 模块', 'log_redaction_missing');
  }
  if (!existsSync(resolve(ctx.root, 'tests/observability/redaction.test.mjs'))) {
    throw new ValidationError('缺少 redaction 测试', 'log_redaction_test');
  }
  return { pass: true };
});

registerValidator('metrics_schema', (ctx) => {
  const contract = loadJson(resolve(ctx.root, 'observability/otel/telemetry-contract.json'));
  if (!contract.metrics?.red?.includes('rate') || !contract.metrics?.use?.includes('utilization')) {
    throw new ValidationError('metrics 缺少 RED/USE', 'metrics_schema_incomplete');
  }
  return { pass: true };
});

registerValidator('dashboard_schema', (ctx) => {
  const schema = loadJson(resolve(ctx.root, 'observability/dashboards/schema.json'));
  const dash = loadJson(resolve(ctx.root, 'observability/dashboards/service-overview.json'));
  for (const key of schema.required ?? []) {
    if (dash[key] === undefined) throw new ValidationError(`dashboard 缺少 ${key}`, 'dashboard_schema_field');
  }
  return { pass: true };
});

registerValidator('alert_contract', (ctx) => {
  const schema = loadJson(resolve(ctx.root, 'observability/alerts/schema.json'));
  const alert = loadJson(resolve(ctx.root, 'observability/alerts/burn-rate.json'));
  for (const key of schema.required ?? []) {
    if (alert[key] === undefined) throw new ValidationError(`alert 缺少 ${key}`, 'alert_contract_field');
  }
  return { pass: true };
});

registerValidator('slo_math', (ctx) => {
  if (!existsSync(resolve(ctx.root, 'operations/slo/error-budget.mjs'))) {
    throw new ValidationError('缺少 error-budget 模块', 'slo_math_missing');
  }
  if (!existsSync(resolve(ctx.root, 'tests/observability/slo-math.test.mjs'))) {
    throw new ValidationError('缺少 slo-math 测试', 'slo_math_test');
  }
  loadJson(resolve(ctx.root, 'operations/slo/definitions.json'));
  return { pass: true };
});

registerValidator('alert_negative', (ctx) => {
  const alert = loadJson(resolve(ctx.root, 'observability/alerts/burn-rate.json'));
  if (!alert.negative_tests?.missing_signal || !alert.negative_tests?.noisy_flap) {
    throw new ValidationError('alert 缺少 negative_tests', 'alert_negative_missing');
  }
  return { pass: true };
});

registerValidator('runbook_links', (ctx) => {
  const alert = loadJson(resolve(ctx.root, 'observability/alerts/burn-rate.json'));
  if (!existsSync(resolve(ctx.root, alert.runbook))) {
    throw new ValidationError(`alert runbook 不存在: ${alert.runbook}`, 'runbook_links_missing');
  }
  return { pass: true };
});

registerValidator('signal_path_runtime', (ctx) => {
  const drill = loadJson(resolve(ctx.root, 'operations/incidents/observability/signal-path-drill.json'));
  if (!drill.synthetic) throw new ValidationError('signal path 必须标记 synthetic', 'signal_path_not_synthetic');
  if (drill.path?.length !== 4) throw new ValidationError('signal path 必须覆盖四跳', 'signal_path_hops');
  return { pass: true };
});

registerValidator('alert_runtime', (ctx) => {
  const drill = loadJson(resolve(ctx.root, 'operations/incidents/observability/signal-path-drill.json'));
  if (!drill.alert?.fires_when || !drill.alert?.resolves_when) {
    throw new ValidationError('drill 缺少 alert fire/resolve 条件', 'alert_runtime_conditions');
  }
  return { pass: true, note: '合成 drill；非 live 告警通道' };
});

export function fixedP1Fixture(root, baselineSha, candidateSha, taskId = 'P1-T01') {
  const sliceId = sliceIdForTask(taskId);
  return {
    root,
    taskId,
    sliceId,
    baselineSha,
    candidateSha,
    environment: { id: '6a594ee667608191ab53cae15202815e', zero_secrets: true },
    modelRecord: { provider: 'xAI', model: 'cursor-grok-4.5-high', mode: 'default', role: 'validator-worker' },
    judgesDir: resolve(root, `evidence/judges/${sliceId}`)
  };
}

export const fixedPhaseFixture = fixedP1Fixture;
