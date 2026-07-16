# Codex 派遣队列约定（`codex-dispatch`）

本文件定义云编排器与控制中心之间的派遣队列约定（决策 D-029）。核心原则：
**云侧只发意图，本地车道只做执行,凭据永不移动。**

## 角色

- **云编排器（Opus 4.8，只读派遣权）**：发布派遣请求,永不亲自派遣、永不在容器内
  `codex login`（等同被拒的 CO-005）。
- **控制中心监督者车道**：所有者本机的 Claude Code 会话,与 codex CLI、钥匙串登录、
  暖身注册表（`%LOCALAPPDATA%\codex-cloud-warm\environments.json`）同址。它轮询队列并执行。

## 队列载体

带 **`codex-dispatch`** 标签、或标题以 **`[codex-dispatch]`** 开头的 GitHub issue。
正文须包含两个可解析的执行块：

````text
```warm
pwsh -File scripts/Invoke-CodexCloudWarm.ps1 -Repo 'nathanielecon/ContinuityOps'
```
```exec
codex cloud exec --env <ENV_ID> --branch <target-branch> "<单行简体中文任务文本>"
```
````

并附：ENV_ID、目标分支、契约路径、baseline_sha,以及给控制中心的简体中文说明。

## 标签生命周期

| 状态 | 含义 | 由谁设置 |
| --- | --- | --- |
| `codex-dispatch` | 待派遣,等待控制中心轮询 | 云编排器（建 issue 时） |
| `dispatched` | 已执行 `codex cloud exec`,任务 ID 已评论 | 控制中心车道（`Watch-CodexDispatchQueue.ps1`） |
| `done`（关闭 issue） | diff 已 apply/push 回流分支,结果已评论 | 控制中心 / 编排器（集成后） |

## 执行流程（控制中心）

1. `scripts/Watch-CodexDispatchQueue.ps1` 循环 `gh issue list --label codex-dispatch --state open`；
2. 逐个解析正文的 `warm` / `exec` 块；
3. 运行温门（**不带 `-Force`**）——失败则评论并跳过本轮；
4. 运行 `codex cloud exec`,把返回任务 ID 评论回 issue,标签改 `dispatched`；
5. 轮询 `codex cloud status` → `codex cloud diff/apply` 到目标流分支 → `git push`；
6. 评论结果并关闭 issue（`done`）。

## 边界

- 该脚本**仅在控制中心运行**,绝不在云容器运行；
- 云容器为 receive-only:无温门、无 `codex cloud exec`、无 `codex login`、无凭据；
- 结果一律经仓库回流（apply 到流分支并推送）,云侧据此可见并继续验证。

## 记录但未启用的备选

Codex GitHub App + `@codex` 提及 + 定时 Action 保暖,作为"监督者车道消失时"的应急方案。
启用前提:把暖戳移出 `%LOCALAPPDATA%`,并对"谁可触发派遣"施加 CODEOWNERS 式门控。
在满足前提前保持关闭。
