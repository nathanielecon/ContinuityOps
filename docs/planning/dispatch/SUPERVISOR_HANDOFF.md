# 监督者交接 — ORCH-ROUND-06 治理修复后（2026-07-17）

> 面向所有者 / 控制中心的持久交接。机器字段英文；自由文本简体中文。

## 当前基线

| 字段 | 值 |
| --- | --- |
| `baseline_sha_before_repair` | `94f4e331de6fbd23b5991e531e61beb83da79551`（revert of accidental PR #30 merge） |
| `branch` | `cursor/orch-round-06-governance-2d6f`（并尝试直推 `main`） |
| `status_revision` | `20`（跳过 19：#29 publish-failed） |
| `P0-T03.state` | `ready`（未 verified） |

## 阻塞：issues:write（CO-011 / D-040）

本 Cursor 监督席位的 App token **可 push/merge，但 Issues API 403**。因此：

- 无法从本席创建/评论 `codex-dispatch` 队列 issue；
- 无法在保暖 issue **#4** 上发布 `@codex` 冒烟；
- App 主路径派遣与云原生保暖对本席不可用，直至所有者授予 Issues 写权限。

**所有者动作（二选一或并行）：**

1. 为监督者 App/token 授予 `issues:write`；或
2. 由所有者/控制中心亲自在队列 issue 与 #4 上发布 `@codex` / keep-warm。

## 所有者待办（仍开放）

- `REPO_SETTINGS_ADMIN_TOKEN`（settings-as-code / 受保护设置）
- PR **#20**
- **H0**（在 P0-T04 之后）
- **D-039** write_scope 扩展：人工可否决；未否决则作为后续 fixer 的权威范围
- 在 S0 与 H0 通过前，**不要**授权 Phase 1

## 已落地（本修复）

- #29 ORCH-ROUND-06 治理内容经监督者 git-push 后备落地：D-037、D-038、会话回顾表、BF-2026-004、心跳 D-037 步骤
- D-039：P0-T03 `write_scope` 扩展以匹配所有者 issue #28 + CO-010
- D-040 / CO-011：记录 Issues 权限缺口
- BF-2026-005 / CO-012：PR #30 误合并已在 `94f4e33` 回滚；禁止用 merge API 做权限探测
- `scripts/Watch-CodexRefs.sh`：约 3.5h 心跳用的单次 ls-remote 观察器

## 明确禁止

- **不要**把 PR #30 内容直接重合并回 `main`（D-037 SCOPE-001 仍成立，直至 D-039 生效后的新 fixer/reviewer 轮次）
- **不要**在本席对 Issues 调用失败时改用 Opus 顶替编排（本任务禁止 Opus）
- **不要** `codex login` 或发明机密

## 下一步派遣顺序（issues:write 恢复后）

1. 保暖：检查 #4 暖戳；必要时所有者/`@codex` 冒烟
2. **fixer**：按 D-039 扩展后的 `write_scope` 重做/收束 P0-T03（不得整树写入 `evidence/slices/`）
3. **D-037 reviewer**：独立 GPT reviewer；**CI green + verdict pass** 才合并
4. **P0-T04** → 人工 **H0**
5. 仅在 S0 + H0 通过后考虑 Phase 1

## 相关证据

- `evidence/slices/S0/SUPERVISOR_ACTUATION-2026-07-17.json`
- `BREAK_FIX_LOG.md` — BF-2026-004 / BF-2026-005
- `OPERATING_STATE.md` — revision 20；D-037..D-040；CO-011/CO-012
