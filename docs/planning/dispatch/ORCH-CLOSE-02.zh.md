# ORCH-CLOSE-02 — 范围内收口编排包

## 调度元数据

```yaml
task_id: ORCH-CLOSE-02
role: orchestrator
model: codex-5.4-default
provider: OpenAI Codex App
mode: default
baseline_sha: 560d542ec3f194d59b3fe23d54c2755e6745faf3
base_branch: main
status: amended_complete
context_remaining: 74%
```

## 收口判定（修订 — 竞态后）

初始编排包曾与 WORKER-SEC-01 / WORKER-AGENTIC-01 并行并写 keep L1。下列为合并 D-037 通过后的修订收口：

- `security-sbom`：**提升至 L2**（PR #66 + REVIEW-SEC-02 pass）— 可复现仓库 SBOM；非 live scanner / live IAM。
- `agentic-workflow`：**提升至 L3 hosted-control**（PR #67 + REVIEW-AGENTIC-03 pass）— D-034/D-042/OIDC/keep-warm；非 in-pod AWS。
- `performance`：保持诚实 L1；无 live load 对比。
- `upstream`：`CO-004` / `CO-006` 继续 blocked；禁止发明 digest（D-028）。
- `azure-governance`：按 D-046 保持 L1 非 live。

## Worker 任务清单

按以下顺序派遣，所有自由文本简体中文；实现 worker 必须返回标准 handoff，并包含 `context_remaining`。

### 1. ORCH-CLOSE-02-CLAIMS

```yaml
task_id: ORCH-CLOSE-02-CLAIMS
role: Codex implementation worker
base_branch: main
baseline_sha: 560d542ec3f194d59b3fe23d54c2755e6745faf3
write_scope:
  - docs/claims/matrix.json
  - evidence/slices/S6/
  - evidence/slices/S7/performance/
objective: |
  只做声明清晰化：为 security-sbom、agentic-workflow、performance 增加或校正
  L1 备注/证据索引，不提升 claim_level，不引入新 live 证据。
acceptance:
  - security-sbom 与 agentic-workflow 均明确 L1 证据边界
  - performance 明确仍为 L1，并给出可测计划入口而非成功声明
  - CO-004/CO-006 不被关闭
validators:
  - node --test tests/
  - node scripts/project.mjs validate P8-T04
```

### 2. ORCH-CLOSE-02-UPSTREAM-GAPS

```yaml
task_id: ORCH-CLOSE-02-UPSTREAM-GAPS
role: Codex implementation worker
base_branch: main
baseline_sha: 560d542ec3f194d59b3fe23d54c2755e6745faf3
write_scope:
  - OPERATING_STATE.md
  - BREAK_FIX_LOG.md
  - docs/claims/
objective: |
  确认 CO-004/CO-006 仍为 blocked/open，并把禁止发明 digest、禁止扩大上游权限、
  D-028 数据包路径写成可审计的剩余缺口。
acceptance:
  - CO-004/CO-006 状态未被关闭
  - 缺口有可复现下一步：提供只读上下文包或 verified sha256 digest 后再提升
  - 无 AWS/Azure/上游凭据变更
validators:
  - node --test tests/
```

### 3. REVIEW-ORCH-CLOSE-02-CLAIMS

```yaml
task_id: REVIEW-ORCH-CLOSE-02-CLAIMS
role: D-037 reviewer
base_branch: main
candidate_source: ORCH-CLOSE-02-CLAIMS PR
write_scope:
  - evidence/judges/REVIEW-ORCH-CLOSE-02-CLAIMS.json
objective: |
  只读应用候选 patch，运行 worker 声明的检查，裁决 security-sbom、
  agentic-workflow、performance 是否保持诚实 L1。不得改实现。
verdict_schema:
  verdict: pass|fail
  candidate_sha: <40_hex>
  checks: []
  findings: []
  context_remaining: <pct>
```

### 4. REVIEW-ORCH-CLOSE-02-UPSTREAM-GAPS

```yaml
task_id: REVIEW-ORCH-CLOSE-02-UPSTREAM-GAPS
role: D-037 reviewer
base_branch: main
candidate_source: ORCH-CLOSE-02-UPSTREAM-GAPS PR
write_scope:
  - evidence/judges/REVIEW-ORCH-CLOSE-02-UPSTREAM-GAPS.json
objective: |
  只读确认 CO-004/CO-006 未被误关，且没有凭据、上游权限或 digest 幻觉。
  不得改实现。
verdict_schema:
  verdict: pass|fail
  candidate_sha: <40_hex>
  checks: []
  findings: []
  context_remaining: <pct>
```

## D-037 派遣顺序

1. 先合入并验证 `ORCH-CLOSE-02-CLAIMS`；CI 绿后派 `REVIEW-ORCH-CLOSE-02-CLAIMS`。
2. 仅当评审 `verdict: pass` 后，派 `ORCH-CLOSE-02-UPSTREAM-GAPS`。
3. `ORCH-CLOSE-02-UPSTREAM-GAPS` CI 绿后派 `REVIEW-ORCH-CLOSE-02-UPSTREAM-GAPS`。
4. 两个 D-037 均 pass 后，junior 才可按 D-042 发 merge intent；若任一 fail，派独立 fixer，不让 reviewer 改实现。

## 标准 handoff

```yaml
task_id: ORCH-CLOSE-02
role: orchestrator
status: complete
candidate_sha: 560d542ec3f194d59b3fe23d54c2755e6745faf3
baseline_sha: 560d542ec3f194d59b3fe23d54c2755e6745faf3
completed:
  - 已制定范围内声明收口判定。
  - 已列出 worker task_ids 与 D-037 评审顺序。
  - 已保留 CO-004/CO-006 blocked 与 D-046 Azure 非 live 边界。
modified_files:
  - docs/planning/dispatch/ORCH-CLOSE-02.zh.md
  - evidence/judges/ORCH-CLOSE-02-orchestrator.json
  - OPERATING_STATE.md
  - BREAK_FIX_LOG.md
validation_commands:
  - command: node --test tests/
  - command: node scripts/project.mjs validate P8-T04
validation_results:
  - command: node --test tests/
    exit_code: 1
    time: 2026-07-18T14:28:05Z
    evidence_path: terminal-output
  - command: node scripts/project.mjs validate P8-T04
    exit_code: 0
    time: 2026-07-18T14:28:50Z
    evidence_path: terminal-output
failed_checks:
  - node --test tests/ 在当前环境中因 terraform fmt -check -recursive terraform 发现既有 Terraform 格式漂移而失败；本轮未改 Terraform 路径，且按 ORCH-CLOSE-02 写入范围已回滚格式化尝试。
remaining_risks:
  - CO-004 仍缺 Project C immutable digest/rollback verified contract。
  - CO-006 仍缺控制中心提供并验证的 Project A/C context package。
  - performance 仍为 L1，尚未跑 live load/capacity 对比。
issue_ids:
  - CO-004
  - CO-006
evidence_paths:
  - docs/planning/dispatch/ORCH-CLOSE-02.zh.md
  - evidence/judges/ORCH-CLOSE-02-orchestrator.json
recommended_next_step:
  - 按 D-034 派 ORCH-CLOSE-02-CLAIMS，然后派 D-037 reviewer；通过后再派 ORCH-CLOSE-02-UPSTREAM-GAPS。
requires_escalation: false
context_remaining: 74%
```
