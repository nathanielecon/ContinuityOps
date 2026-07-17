import { readFileSync, writeFileSync, mkdtempSync, rmSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

const root = new URL('../..', import.meta.url);
const readJson = (path) => JSON.parse(readFileSync(new URL(path, root), 'utf8'));
const sha256Text = (text) => createHash('sha256').update(text).digest('hex');
const sha256File = (path) => sha256Text(readFileSync(new URL(path, root), 'utf8'));
const fail = (code, message) => { const error = new Error(message); error.code = code; throw error; };

export function validateRubricSchema(rubric) {
  if (rubric.schema_version !== '1.0') fail('rubric_schema', 'rubric schema_version 必须是 1.0');
  if (rubric.rubric_id !== 'S0-freeze-v1' || rubric.slice !== 'S0') fail('rubric_schema', 'rubric id 或 slice 不匹配');
  if (rubric.status !== 'frozen_pending_H0') fail('rubric_schema', 'rubric 必须冻结且等待 H0');
  if (rubric.authority?.human_gate !== 'H0' || rubric.authority?.draft_is_authoritative !== false) fail('rubric_schema', 'H0 或草案权威声明错误');
  const dimensions = rubric.scoring?.dimensions ?? [];
  const total = dimensions.reduce((sum, item) => sum + item.weight, 0);
  if (total !== 100) fail('rubric_schema', `rubric 权重总和必须为 100，实际为 ${total}`);
  for (const item of dimensions) {
    if (!item.id || !item.title || !Array.isArray(item.required_checks) || item.required_checks.length === 0) fail('rubric_schema', `维度 ${item.id ?? '<missing>'} 缺少必检项`);
  }
  if (!Array.isArray(rubric.automatic_failures) || !rubric.automatic_failures.some((item) => item.includes('H0'))) fail('rubric_schema', '自动失败条件必须包含 H0 防伪造规则');
  if (rubric.mutation_policy?.frozen !== true) fail('rubric_schema', 'mutation policy 必须声明 frozen=true');
  return true;
}

export function validateApprovalBinding(binding) {
  if (binding.status !== 'waiting_human') fail('approval_binding', '没有真实 H0 receipt 时状态必须是 waiting_human');
  if (binding.receipt !== null || binding.receipt_sha256 !== null) fail('approval_binding', '代理不得填入 H0 receipt 或 receipt hash');
  if (!binding.binding_rule?.includes('真实人类')) fail('approval_binding', 'binding_rule 必须要求真实人类 receipt');
  return true;
}

export function validateBundleHashes(evidence) {
  const pinned = evidence.bundle_hashes;
  for (const key of ['plan_sha256', 'execution_contract_sha256', 'validator_bundle_sha256', 'rubric_sha256', 'partition_bundle_sha256']) {
    if (!/^[0-9a-f]{64}$/.test(pinned?.[key] ?? '')) fail('bundle_hashes', `${key} 缺少 SHA-256`);
  }
  const actual = {
    plan_sha256: sha256File('PLAN.md'),
    execution_contract_sha256: sha256File('docs/planning/dispatch/P0-T04.zh.md'),
    validator_bundle_sha256: sha256Text([sha256File('scripts/validators/core.mjs'), sha256File('evidence/schema/validator-contract.schema.json')].join('\n')),
    rubric_sha256: sha256File('harness/rubrics/S0.freeze.v1.json'),
    partition_bundle_sha256: sha256File('integration/upstreams.lock.json')
  };
  for (const [key, value] of Object.entries(actual)) {
    if (pinned[key] !== value) fail('bundle_hashes', `${key} 与当前文件不匹配`);
  }
  return true;
}

export function validateMutationPolicy(evidence) {
  const rubricText = readFileSync(new URL('harness/rubrics/S0.freeze.v1.json', root), 'utf8');
  const originalHash = sha256Text(rubricText);
  if (originalHash !== evidence.bundle_hashes.rubric_sha256) fail('rubric_mutated', '原始 rubric hash 未匹配 pinned hash');
  const tempDir = mkdtempSync(join(tmpdir(), 'co-rubric-mut-'));
  try {
    const mutatedPath = join(tempDir, 'S0.freeze.v1.json');
    writeFileSync(mutatedPath, rubricText.replace('"pass_threshold": 90', '"pass_threshold": 89'));
    const mutatedHash = sha256Text(readFileSync(mutatedPath, 'utf8'));
    if (mutatedHash === evidence.bundle_hashes.rubric_sha256) fail('rubric_mutation_negative', '负向篡改测试未改变 hash');
  } finally {
    rmSync(tempDir, { recursive: true, force: true });
  }
  return true;
}

export function runAll() {
  const rubric = readJson('harness/rubrics/S0.freeze.v1.json');
  const binding = readJson('harness/approvals/H0.binding.json');
  const evidence = readJson('evidence/slices/S0/rubric-freeze.json');
  validateRubricSchema(rubric);
  validateApprovalBinding(binding);
  validateBundleHashes(evidence);
  validateMutationPolicy(evidence);
  return { pass: true, validators: ['rubric_schema', 'bundle_hashes', 'approval_binding', 'rubric_mutation_policy'] };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  console.log(JSON.stringify(runAll(), null, 2));
}
