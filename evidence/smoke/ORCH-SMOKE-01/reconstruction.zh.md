# ORCH-SMOKE-01 冷启动重建演练

## 读取顺序

本演练按仓库权威顺序冷启动读取并重建状态：

1. `AGENTS.md`：确认权威顺序、简体中文通信要求、云容器 receive-only 边界、D-033 App 发布硬门槛、工作者 handoff 必含 `context_remaining`。
2. `PLAN.md`：确认当前授权只到 Phase 0，`P0-T01` 为 `ready`，写范围为 `docs/scaffold-audit.md`、`integration/upstreams.lock.json`、`harness/partition-manifest.json`，验证器为 `state_schema`、`partition_unique_ownership`、`upstream_pin_schema`、`clean_tree`。
3. `OPERATING_STATE.md`：确认当前阶段为 Phase 0，已注册零机密 Codex Cloud Environment，后续动作要求只把 GitHub 可见 PR URL 视作 App 路径完成。
4. `BREAK_FIX_LOG.md`：确认 BF-PRE-015 系列要求，监督者只在流边界审查候选完成信号，修复会使先前候选绑定证据失效。
5. `docs/planning/RALPHY_ORCHESTRATION.md` 与 `docs/planning/MODEL_AND_STREAM_TOPOLOGY.md`：确认 Ralphy 轮次、角色隔离、顺序流与跨流分区隔离。
6. `docs/planning/dispatch/QUEUE.md`：确认 D-033 发布契约；App 路径完成必须有 GitHub 可见分支与针对目标分支的开放 PR URL，不能停在 `make_pr` 或 issue 评论。
7. `harness/README.md`：确认 P0-T01 的验证器来源、候选实现分支、精确运行命令与退出码约定。
8. `harness/schemas/stream-complete.schema.json`：确认 `STREAM_COMPLETE.json` 顶层 `additionalProperties: false`，演练标记只能由本文件名承载，不新增顶层字段。

## 当前状态重建摘要

- 仓库仍是 Phase 0 治理与计划仓；尚无应用服务、依赖清单或已授权的运行时能力。
- `PLAN.md` 中 `authorized_through_phase` 为 `0`；不得推进 Phase 1。
- `P0-T01` 当前为可启动任务，目标是审计并冻结已完成候选基线。
- P0-T01 工作者契约不在本分支普通路径中；按 `harness/README.md` 与队列约定，应从 `origin/stream/S0-baseline-audit` 的 `docs/planning/dispatch/P0-T01.zh.md`、固定提交 `648791d4ec88fde914b0f8c17be8f94cc4da2b62` 读取。
- P0-T01 验证器实现来源为候选分支 `claude/cloud-gpt-ralphy-validation-6m0gkz` 的固定提交 `2c9026b29e96e37c768db9737e2d9539fdeb7003`。
- 本冒烟产物只供监督者按 BF-PRE-015 严格度评审，不进入任何切片证据链。

## P0-T01 worker diff 返回后的整轮执行程序

1. **冻结输入**：记录 worker 返回的 `candidate_sha`、`baseline_sha`、修改文件清单、验证命令、验证结果、证据路径与 `context_remaining`。若任一必填字段缺失，直接拒收 handoff。
2. **范围检查**：确认 worker 只修改 `PLAN.md` 允许的 P0-T01 写范围：`docs/scaffold-audit.md`、`integration/upstreams.lock.json`、`harness/partition-manifest.json`。任何越界修改均作废并记录 break/fix。
3. **候选来源检查**：确认候选实现分支来自受管 worker diff，而不是由编排器自行实现；编排器只集成、验证、记录，不替代实现工人。
4. **预检证据读取**：从仓内持久工件 `evidence/slices/S0/preflight-P0-T01.json` 读取温门快照，并据此填写真实 `preflight_ok`。issue 评论不是权威来源；若该持久工件不存在，不能伪造温门，只能记录缺失并阻断正式完成信号。
5. **准备验证器工作区**：按 `harness/README.md` 拉取候选验证器实现：
   ```bash
   git fetch origin claude/cloud-gpt-ralphy-validation-6m0gkz
   git worktree add ../co-harness 2c9026b29e96e37c768db9737e2d9539fdeb7003
   ```
6. **运行确定性验证**：在包含候选 harness 的工作区中，对 P0-T01 运行唯一权威命令：
   ```bash
   node scripts/project.mjs validate P0-T01
   ```
   退出码约定：`0` 表示 `VALIDATE OK` 且全部验证器通过；`1` 表示 `VALIDATE FAIL` 或执行错误；`2` 表示未知或缺失 CLI 命令。
7. **证据绑定**：把每条验证结果记录为含 `command`、`exit`、`time`、`evidence_path` 的对象；所有证据必须绑定到同一个候选 SHA。
8. **失败处理**：任一验证失败、证据缺失、候选 SHA 不一致、温门持久证据缺失或工作范围越界时，更新 `BREAK_FIX_LOG.md`，派发 nixer/fixer 或瓶颈子代理；不得关闭轮次。
9. **成功完成信号**：所有验证通过后，由编排器在流分支提交正式 `evidence/slices/S0/STREAM_COMPLETE.json`，其结构必须符合 `harness/schemas/stream-complete.schema.json`，并包含真实 `context_remaining` 与真实 `preflight_ok`。
10. **监督者边界审查**：监督者只在流边界读取完成信号并审查；不得把每轮检查替代给监督者，也不得把 UI 元数据当作完成。
11. **D-033 发布**：App 路径回流必须推送 GitHub 可见分支并打开针对目标分支的 PR；没有可观察 PR URL 时，本任务未完成。

## 本演练样例说明

- `stream-complete.dryrun.json` 是 schema 形状演练，不是正式 `STREAM_COMPLETE.json`。
- 按触发契约，本演练的 `candidate_sha` 与 `baseline_sha` 均使用触发中给定的当前目标分支真实 tip：`a62aa3e429ebe72351356c13486ff6af92612d5a`。
- 温门持久数据在本 worker 容器内不可得，且本演练不能伪造；因此 `preflight_ok.context_package_ready` 使用 schema 允许的 `"n/a"`，`preflight_ok.last_warm_utc` 使用 `null`，`preflight_ok.preflight_evidence_path` 指向预期持久路径，`notes_zh` 明确标注这是演练占位。
- `preflight_ok.warm_fresh` 是必填布尔字段；本演练无法证明温门新鲜，因此填 `false`，并不声称温门通过。

context_remaining: 74%
