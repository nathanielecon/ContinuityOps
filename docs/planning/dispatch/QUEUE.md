# Codex 派遣队列约定（`codex-dispatch`）

本文件定义云编排器与控制中心之间的派遣队列约定（决策 D-029）。核心原则：
**云侧只发意图，本地车道只做执行,凭据永不移动。**

## 角色

- **云编排器（Opus 4.8，只读派遣权）**：发布派遣请求,永不亲自派遣、永不在容器内
  `codex login`（等同被拒的 CO-005）。
- **控制中心监督者车道**：所有者本机的 Claude Code 会话,与 codex CLI、钥匙串登录、
  暖身注册表（`%LOCALAPPDATA%\codex-cloud-warm\environments.json`）同址。它轮询队列并执行。

## 队列载体

**带 `codex-dispatch` 标签**的开放 GitHub issue。轮询**按标签**进行（`gh issue list
--label codex-dispatch`）——**标题前缀不足以入队**,新 issue 必须打上 `codex-dispatch`
标签。正文须包含两个可解析的执行块：

````text
```warm
pwsh -File scripts/Invoke-CodexCloudWarm.ps1 -Repo 'nathanielecon/ContinuityOps'
```
```exec
codex cloud exec --env <ENV_ID> --branch <target-branch> "<单行简体中文任务文本>"
```
````

并附：ENV_ID、目标分支、契约路径、baseline_sha,以及给控制中心的简体中文说明。

> **当前队列**：issue #2（`[codex-dispatch] P0-T01 — S0 baseline audit`）**已贴
> `codex-dispatch` 标签**,等待下次监督者巡查处理。

## 所需标签（自动创建，四个现已存在）

GitHub 的 issues API 在给 issue 贴一个尚不存在的标签时会**自动创建**该标签
（云侧经 MCP 已实证）。因此**任一拥有 `issues:write` 权限的席位**（云编排器或控制中心）
均可经"贴标签"自动创建,无需专门的 `gh label create` 步骤。四个生命周期标签
（`codex-dispatch`、`dispatching`、`dispatched`、`dispatch-failed`）**现已存在**。
如需显式预建或统一配色/描述,可选执行：

```bash
gh label create codex-dispatch  --color 1d76db --description "待派遣的 Codex 任务队列"
gh label create dispatching     --color fbca04 --description "已被车道认领,派遣进行中"
gh label create dispatched      --color 0e8a16 --description "codex cloud exec 已提交,含任务 ID"
gh label create dispatch-failed --color b60205 --description "温门或派遣失败,人工重排队"
```

## 标签生命周期

`codex-dispatch → dispatching → dispatched → done`（失败分支：`dispatch-failed`）。

| 状态 | 含义 | 由谁设置 |
| --- | --- | --- |
| `codex-dispatch` | 待派遣,等待控制中心轮询 | 云编排器（建 issue 时） |
| `dispatching` | **已认领**,派遣进行中（认领先于执行,防重复派遣） | 控制中心车道 |
| `dispatched` | 已执行 `codex cloud exec`,任务 ID 已评论 | 控制中心车道 |
| `dispatch-failed` | 温门或派遣失败;**不自动重试** | 控制中心车道 |
| `done`（关闭 issue） | diff 已 apply/push 回流分支,结果已评论 | 控制中心 / 编排器（集成后） |
| 重排队 | 把 `dispatch-failed` 改回 `codex-dispatch` | **人工**（修正后） |

## 执行流程（控制中心，幂等）

1. `scripts/Watch-CodexDispatchQueue.ps1 -Once` 拉取 `--label codex-dispatch --state open`；
2. **作者白名单**：非 `-AllowedAuthors`（默认仓库所有者）的 issue 评论并跳过,不执行任何块；
3. 解析 `warm` / `exec` 块（缺失则 `dispatch-failed`）；
4. **先认领**：`codex-dispatch → dispatching`;随后重新拉取标签双重校验,认领失败/丢失竞态即跳过；
5. 运行温门（**不带 `-Force`**）——失败则 `dispatch-failed` + 评论,**不自动重试**；
6. 运行 `codex cloud exec`,评论任务 ID,标签改 `dispatched`；失败则 `dispatch-failed` + 评论；
7. 轮询 `codex cloud status` → `codex cloud diff/apply` 到目标流分支 → `git push`；
8. 评论结果并关闭 issue（`done`）。

## 监督者巡查（sweep）模式

控制中心**不注册自主计划任务**。派遣车道仅在**所有者的实时监督会话在站时**运行:
每次在站巡查一遍队列——可用 `Watch-CodexDispatchQueue.ps1 -Once`,或手工按 issue 的
`warm` / `exec` 执行块逐个处理。队列项在两次巡查之间**等待**;这是"单一明确权威席位"
的既定取舍(以在站时的确定性,换取项目在无人值守时不被自主执行)。

巡查也可能重叠(手工 + `-Once`、或多次触发),故脚本的**幂等/认领标签先行/本机锁互斥/
作者白名单**要求**保持不变**:

- 本机锁文件 `%LOCALAPPDATA%\codex-cloud-warm\queue.lock`(含过期兜底)确保重叠巡查不并发;
- 认领标签 `codex-dispatch → dispatching` 先于执行,避免同一项被重复派遣。

> **会话内的后台循环随应用重启而静默停摆**(邻席项目因此丢过三个 worker,见 BF-PRE-017);
> 巡查模式以"在站才跑"规避了这一失效面,而非依赖长期后台进程。

## 边界

- 该脚本**仅在控制中心运行**,绝不在云容器运行；
- 云容器为 receive-only:无温门、无 `codex cloud exec`、无 `codex login`、无凭据；
- 结果一律经仓库回流（apply 到流分支并推送）,云侧据此可见并继续验证。

## 记录但未启用的备选

Codex GitHub App + `@codex` 提及 + 定时 Action 保暖,作为"监督者车道消失时"的应急方案。
启用前提:把暖戳移出 `%LOCALAPPDATA%`,并对"谁可触发派遣"施加 CODEOWNERS 式门控。
在满足前提前保持关闭。
