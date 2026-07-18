# Codex 派遣队列约定（`codex-dispatch`）

本文件定义派遣队列约定（决策 D-029,经 D-031 修订）。核心原则不变：
**凭据永不移动。**

> **D-031 生效(主路径变更)**:Codex GitHub App 已安装于本仓。派遣主路径改为
> **云监督者在其本人(或所有者)所建的 `codex-dispatch` issue 上发布 `@codex` 提及**,
> 经 App 触发 Codex Cloud 任务;结果以 Codex 创建的 PR/分支回流,由监督者集成到
> **流分支**(合并 `main` 与全部 D-012 门仍属人工)。门控:只有监督者/所有者所建
> 队列 issue 上的提及才算派遣。暖新鲜度改以保暖记录上最近一次 Codex 任务时间戳为证,
> 由监督者的定时自查约每 9 小时发布一次 `@codex` 保暖冒烟。
> 本文其余"控制中心巡查"流程(warm/exec 围栏块、`Watch-CodexDispatchQueue.ps1`、
> 本机注册表与温门脚本)自 D-031 起为**后备路径**,仅在 App 路径不可用时启用。

> **D-033**(历史):App 沙箱无法自发布;`make_pr` 仅元数据;平台 Create PR /
> 控制中心 apply 曾为过夜发布面。
>
> **D-034 生效(主发布面)**:过夜/无人值守发布改为 **patch-in-comment + GHA**。
> 工人最终回复须含 `<!-- continuityops-patch-v1 -->`、`base_branch`、`base_sha`
> 与完整 fenced unified diff。工作流
> `.github/workflows/codex-patch-publish.yml` 由 `chatgpt-codex-connector[bot]`
> 的 `issue_comment` 触发,用 ephemeral `GITHUB_TOKEN` apply/push/开 PR,并回评
> URL。平台 Create PR 与 `scripts/Publish-CodexCloudTask.ps1` 降为**后备**。
> 监督者心跳以 PR 评审/集成为主:有 `publish-ok`/开放 PR → 派遣 D-037 GPT
> reviewer 轮;reviewer 在声明 `base_sha` 应用该 PR patch、亲自跑声明验证命令、
> 结构化 verdict 回评;**CI green + reviewer verdict pass** 后监督者才集成。若有
> bot 摘要但无 patch 标记且无 PR → 重催 D-034 片段;有 `publish-failed` → 诊断或
> 后备路径。勿把 `make_pr` 文本当完成。`github-actions[bot]` `@codex` 保暖仍未验证。

## App 路径完成契约(每次 `@codex` 派遣必贴)

完整模板见 [`CODEX_DISPATCH_SNIPPET.zh.md`](./CODEX_DISPATCH_SNIPPET.zh.md)。

目标分支填 issue 正文指定的流/编排分支(例如 `stream/S0-baseline-audit` 或
`claude/orchestrator-supervisor-setup-yyd3bu`),写入 `base_branch` 字段。

## 初级监督者心跳 — D-034/D-035/D-041(评审 PR;发布由 GHA 完成;保暖云原生)

> **D-047（amends D-041/D-042 例行 hop）:** 机械 phase hop 由
> `.github/workflows/pipeline-zero-hop.yml` **零跳变**完成，**不经 junior 定时器**。
> Junior 只处理**例外**（范围冲突、模糊 stop/escalate、两连同 class、跨车道锁、
> 路由包）。寻呼见 [`PAGER_SNIPPET.zh.md`](./PAGER_SNIPPET.zh.md)。
> 候选分支约定：`candidate/portfolio-<7sha>`；**仅** fresh council 通过后才合 `main`。
>
> **D-041 / D-042（仍有效，范围收窄）:** 例外判断仍由 **junior supervisor**
> （GPT-5.6 Sol med）作出；动手经 D-042 意图标记 → `junior-actuate`。
> **Chief** 处理 `STREAM_COMPLETE` / `chief-pager` / monitor 显著瓶颈。
> 片段见 [`JUNIOR_ACTUATE_SNIPPET.zh.md`](./JUNIOR_ACTUATE_SNIPPET.zh.md)。

### Zero-hop 机械表（D-047，GHA 拥有）

| 触发 | 动作 |
| --- | --- |
| `publish-ok` | 创建/确保 D-037 `codex-dispatch` + `@codex` + D-034 片段 |
| D-037 bot `verdict: pass` + CI green | 合并 PR → **candidate**（非 main） |
| D-037 bot `verdict: fail` | 开 fixer issue + `@codex` |
| Judge PR `evidence/judges/**` 且 `merge_ready: no` | **B:** 开 nixer + `@codex`（按 candidate SHA 去重） |
| Nixer `publish-ok` | 开 fixer，绑定 nixer issue IDs |
| Fixer 合入 candidate | 派遣 provisional 三 judge |
| Provisional 全 `merge_ready: yes` | 派遣 **fresh** 三 judge |
| Fresh 全通过 + CI | candidate → `main` |
| Provisional/fresh 失败 | 新 nixer cohort（新 issue IDs），禁止盲重试同 tip |
| `publish-failed` | 自动重催一次 `@codex` + D-034 |
| #4 暖戳 >9h | `#4` 冒烟 `@codex` |

幂等标签：`zh-dispatching` / `zh-dispatched` / `fail-class:<hash>`。
两连同 class（strike≥2）→ 停止自动重试，寻呼 junior/chief。

### Junior 例外心跳（非机械 hop）

每次被 `JR-EXCEPTION-*` 唤醒时：

1. 校验 wake packet（缺字段 → `failed` + 寻呼首席，不得猜 hop）。
2. 模糊 write_scope：只许 `reject` | `rebind_scope` | `escalate`。
3. 跨车道须引用 lock/interface 路径，否则 escalate。
4. 需 actuation 时必须带 D-042 意图标记；无标记不得标 `complete`。
5. **禁止**在 App 容器内直接 `gh`；**禁止**把 `make_pr` 当完成。

保暖(D-035/D-047):暖戳为 issue **#4** 最近 Codex 任务时间戳。Zero-hop 在 >9h 时冒烟；禁止把真实工作派进冷环境。Grok **monitor** 向首席汇报显著瓶颈（见 `MONITOR.zh.md`）。

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
>
> **P0-T01 契约真实所在（消除"按路径读落空"）**：定稿的 P0-T01 工作者契约**不在**
> 本编排分支,而在流分支 `origin/stream/S0-baseline-audit` 的
> `docs/planning/dispatch/P0-T01.zh.md`（pinned commit `648791d`）。
> 用 `git show origin/stream/S0-baseline-audit:docs/planning/dispatch/P0-T01.zh.md` 读取。
> 权威*任务定义*仍是 `PLAN.md` 中的 `P0-T01`。验证器实现来源与运行方式见
> `harness/README.md`（候选实现分支 `claude/cloud-gpt-ralphy-validation-6m0gkz`）。

## 所需标签（自动创建 + D-047 扩展）

GitHub 的 issues API 在给 issue 贴一个尚不存在的标签时会**自动创建**该标签
（云侧经 MCP 已实证）。四个生命周期标签
（`codex-dispatch`、`dispatching`、`dispatched`、`dispatch-failed`）**现已存在**。
D-047 另需：`zh-dispatching`、`zh-dispatched`、`chief-pager`、`junior-exception`；
`fail-class:<hash>` 由 zero-hop 按失败类动态贴。可选预建：

```bash
gh label create codex-dispatch  --color 1d76db --description "待派遣的 Codex 任务队列"
gh label create dispatching     --color fbca04 --description "已被车道认领,派遣进行中"
gh label create dispatched      --color 0e8a16 --description "codex cloud exec 已提交,含任务 ID"
gh label create dispatch-failed --color b60205 --description "温门或派遣失败,人工重排队"
gh label create zh-dispatching  --color f9d0c4 --description "zero-hop 认领中(D-047)"
gh label create zh-dispatched   --color c2e0c6 --description "zero-hop 已完成该 hop(D-047)"
gh label create chief-pager     --color b60205 --description "首席 durable pager(D-047)"
gh label create junior-exception --color d93f0b --description "初级例外唤醒(D-047)"
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

## 执行流程（后备车道：控制中心，幂等）

1. `scripts/Watch-CodexDispatchQueue.ps1 -Once` 拉取 `--label codex-dispatch --state open`；
2. **作者白名单**：非 `-AllowedAuthors`（默认仓库所有者）的 issue 评论并跳过,不执行任何块；
3. 解析 `warm` / `exec` 块（缺失则 `dispatch-failed`）；
4. **先认领**：`codex-dispatch → dispatching`;随后重新拉取标签双重校验,认领失败/丢失竞态即跳过；
5. 运行温门（**不带 `-Force`**）——失败则 `dispatch-failed` + 评论,**不自动重试**；
6. **持久化温门快照(preflight 权威来源)**：把温门结果作为持久工件写回目标流分支
   `evidence/slices/<slice>/preflight-<taskid>.json`,至少含 `lastWarmUtc` 与 `verdict`。
   编排器随后据此文件填充 `STREAM_COMPLETE.json` 的 `preflight_ok`
   （见 BF-PRE-015.8 与 `harness/schemas/stream-complete.schema.json`）。
   **issue 评论不是 `preflight_ok` 的权威来源**——评论仅供人读,权威一律取仓内持久工件；
7. 运行 `codex cloud exec`,评论任务 ID,标签改 `dispatched`；失败则 `dispatch-failed` + 评论；
8. 轮询 `codex cloud status` → `codex cloud diff/apply` 到目标流分支 → `git push`；
9. 评论结果并关闭 issue（`done`）。

## 后备车道：监督者巡查（sweep）模式

控制中心巡查是**后备车道**,仅当 App/GHA 主路径不可用时使用。控制中心**不注册自主计划任务**。派遣车道仅在**所有者的实时监督会话在站时**运行:
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

## 后备状态说明（D-031→D-035）

原"记录但未启用"的 Codex GitHub App 路径**已启用为主路径**(见文首 D-031 段):
D-035 确认暖戳已移出 `%LOCALAPPDATA%`:以保暖记录 issue **#4** 上最近一次 Codex 任务时间戳为证;派遣时旧于约 10h 先冒烟,心跳旧于 >9h 冒烟。触发门控为"仅监督者/所有者所建队列 issue 上的提及"。定时保暖工作流
`.github/workflows/codex-keepwarm.yml` 已编写(约每 8 小时在 #4 发 `@codex` 冒烟;
仅用临时 GITHUB_TOKEN,零机密):**合并到默认分支后激活**,激活后须以一次
`workflow_dispatch` 实测 App 是否响应 bot 作者的提及——若不响应,禁用该工作流,
保暖回落到监督者心跳(约 3–4 小时一次的后备唤醒,兼作看门失效兜底)。
控制中心巡查明确降为后备车道。
