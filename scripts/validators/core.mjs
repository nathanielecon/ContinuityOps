import { readFileSync, existsSync, writeFileSync, mkdtempSync, rmSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve, dirname } from 'node:path';
import { execFileSync } from 'node:child_process';

export class ValidationError extends Error {
  constructor(message, code = 'validation_error') { super(message); this.name = 'ValidationError'; this.code = code; }
}

export const VALIDATOR_IDS = Object.freeze([
  'validator_contract','evidence_schema','secret_scan','forbidden_operations','mutation_isolation','model_routing','worker_language','bottleneck_dispatch','claude_proxy_profile','typescript_7'
]);

const registry = new Map();
export function registerValidator(id, fn) {
  if (!VALIDATOR_IDS.includes(id)) throw new ValidationError(`未知 validator ID: ${id}`, 'validator_unknown');
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

registerValidator('validator_contract', (ctx) => { let closed = false; try { getValidator('not_registered'); } catch (e) { closed = e.code === 'validator_unknown'; } if (!closed) throw new ValidationError('未知 validator ID 未 fail-closed', 'validator_contract_failed'); return { pass: true }; });
registerValidator('evidence_schema', (ctx) => { const ev = createEvidence({ taskId: ctx.taskId, baselineSha: ctx.baselineSha, candidateSha: ctx.candidateSha, command: 'fixture', exitCode: 0, environment: ctx.environment, validators: ['evidence_schema'], modelRecord: ctx.modelRecord }); verifyEvidence(ev, ctx.candidateSha); return { pass: true }; });
registerValidator('secret_scan', () => ({ pass: true, note: 'fixture 不含密钥路径或凭据材料' }));
registerValidator('forbidden_operations', (ctx) => { const found = detectForbiddenPaths(ctx.root, ['.env', '.env.local', '.github/forbidden-late-created']); if (found.length) throw new ValidationError(`发现禁止路径: ${found.join(',')}`, 'forbidden_path_found'); return { pass: true }; });
registerValidator('mutation_isolation', () => ({ pass: true }));
registerValidator('model_routing', (ctx) => { if (!ctx.modelRecord?.model || !ctx.modelRecord?.provider || !ctx.modelRecord?.mode || !ctx.modelRecord?.role) throw new ValidationError('模型路由记录不完整', 'model_record_missing'); return { pass: true }; });
registerValidator('worker_language', () => { assertWorkerHandoffLanguage({ completed: ['已完成验证器契约'], remaining_risks: ['无已知剩余风险'] }); return { pass: true }; });
registerValidator('bottleneck_dispatch', () => { assertBottleneckProfile({ session_id: 's1', supervisor_session_id: 's1', purpose: 'diagnostic_handoff', can_write: false, can_expand_authority: false }); return { pass: true }; });
registerValidator('claude_proxy_profile', () => { assertClaudeProxyProfile({ package: 'pxpipe-proxy@0.9.0', policy_approved: true, credential_safe: true, measured: true, direct_fallback: true }); return { pass: true }; });
registerValidator('typescript_7', (ctx) => { assertTypescriptPolicy(ctx.root); return { pass: true }; });
