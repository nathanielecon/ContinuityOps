# DRAFT：S0 rubric 草案（非冻结、非批准、非打分依据）

> **DRAFT / 草案 / 不可作为冻结 rubric 使用。** 本文件仅为 `P0-T04` 冻结 S0 rubric 前的提案输入。它不是 H0 人工批准，不是 judge 打分依据，也不得被用来声明 S0 通过。

## 草案目标

S0 的核心目标是证明 ContinuityOps Phase 0 治理与编排底座成立：仓库分区清晰、任务状态可原子推进、验证器 fail-closed、证据 SHA 绑定、rubric 可冻结且受 H0 门禁约束，并且三流并发与 fresh judge 退出路径可被可靠验证。

## 必须项提案

1. **权威状态一致性**：`PLAN.md`、`OPERATING_STATE.md`、状态文件与任务 handoff 不得互相矛盾。
2. **分区与写范围**：每个 changed path 必须属于任务 write_scope；共享接口必须显式记录。
3. **授权边界**：Phase 0 当前任务可执行；Phase 1 必须保持拒绝，直到人类改写授权。
4. **验证器可信度**：未知 validator ID fail closed；验证器运行不得修改仓库。
5. **证据绑定**：所有证据绑定 candidate SHA、baseline SHA、命令、退出码、时间与环境。
6. **人类门禁**：H0 只能由真实人类批准 receipt 满足；代理不得伪造。
7. **并发编排**：最多三个 disjoint streams 可并行，但每个 stream 内部顺序执行且不得自合并。
8. **fresh 判断**：saved remediation council 只能给出 provisional pass；最终退出需要 fresh judges。

## 评分维度提案

- 状态机与授权边界：25%
- 验证器与证据 schema：25%
- 分区、并发与集成队列：20%
- Rubric freeze、bundle hash 与 H0 绑定：15%
- Break/fix 记录、handoff 完整性与简体中文通信：15%

## 自动失败条件提案

- 任何 worker 或工具伪造、暗示或替代人类批准。
- Phase 1 在未授权情况下被接受。
- 验证器删除或修改仓库内容。
- 证据缺少 candidate SHA 或命令退出码。
- Changed path 超出 write_scope。
- Judge 能看到实现 transcript、目标阈值或其他 judge 报告。
- 出现 secrets、凭据、用户数据或外部账户材料。

## 证据索引提案

- `evidence/slices/S0/baseline-audit.json`
- `evidence/slices/S0/harness.json`
- `evidence/slices/S0/validator-contract.json`
- `evidence/slices/S0/rubric-freeze.json`
- `evidence/slices/S0/integrated-gate.json`
- `evidence/judges/S0/`
- `BREAK_FIX_LOG.md`

## 冻结前确认清单

- [ ] `P0-T01` baseline audit 与 partition manifest 已通过。
- [ ] `P0-T02` harness 与状态合约已通过。
- [ ] `P0-T03` validator framework 与 evidence schema 已通过。
- [ ] `P0-T04` 生成 frozen rubric，并记录 bundle hashes。
- [ ] H0 人工批准 receipt 已由人类提供并 hash-bound。
- [ ] 本草案未被误用为 frozen rubric、approval 或 judge scoring target。
