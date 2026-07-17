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

## 所需标签（控制中心一次性创建）

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

## 持久运行（关键）

**会话内的后台循环随应用重启而静默停摆**（邻席项目因此丢过三个 worker,见 BF-PRE-017）。
派遣轮询必须由**计划任务/服务**承载,以 `-Once` 单轮模式每 2–5 分钟触发一次：

```powershell
$action  = New-ScheduledTaskAction -Execute 'pwsh' `
  -Argument '-NoProfile -File "C:\path\to\ContinuityOps\scripts\Watch-CodexDispatchQueue.ps1" -Once'
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) `
  -RepetitionInterval (New-TimeSpan -Minutes 5)
Register-ScheduledTask -TaskName 'CodexDispatchQueue' -Action $action -Trigger $trigger `
  -Description 'ContinuityOps Codex 派遣队列轮询（-Once，每5分钟）'
```

本机锁文件（`%LOCALAPPDATA%\codex-cloud-warm\queue.lock`,含过期兜底)确保重叠触发不并发运行。

## 边界

- 该脚本**仅在控制中心运行**,绝不在云容器运行；
- 云容器为 receive-only:无温门、无 `codex cloud exec`、无 `codex login`、无凭据；
- 结果一律经仓库回流（apply 到流分支并推送）,云侧据此可见并继续验证。

## 记录但未启用的备选

Codex GitHub App + `@codex` 提及 + 定时 Action 保暖,作为"监督者车道消失时"的应急方案。
启用前提:把暖戳移出 `%LOCALAPPDATA%`,并对"谁可触发派遣"施加 CODEOWNERS 式门控。
在满足前提前保持关闭。
