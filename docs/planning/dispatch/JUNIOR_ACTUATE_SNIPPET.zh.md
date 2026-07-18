# Junior App 路径 actuation 片段（D-042）

App 沙箱**不能** `git push` / `gh`。Junior 在 `codex-dispatch` issue 上发出意图标记；
GitHub Actions `junior-actuate` 用 ephemeral `GITHUB_TOKEN` 执行。

## 合并意图（CI green + D-037 pass 之后）

在队列 issue 评论中原样输出：

```
<!-- continuityops-merge-v1 -->
pr: 44
d037_issue: 45
```

工作流核验后合并：PR open；D-037 issue 上 bot 最新 `verdict` 为 `pass`；PR head 的 `contracts`/`validate` check-run 为 success；然后回评 `actuate-ok` 或 `actuate-failed`。

## 派遣意图（代发 `@codex`）

```
<!-- continuityops-dispatch-v1 -->
target_issue: 46
```

紧接着再贴一个 fenced 代码块，正文必须含 `@codex`（可含 D-034 patch 片段）。`target_issue` 必须已有 `codex-dispatch` 标签。疑似 secret 载荷会被拒绝。

## 仓库 Settings 前提（与 D-034 相同）

Settings → Actions → General → Workflow permissions:

1. **Read and write permissions**
2. **Allow GitHub Actions to create and approve pull requests**

当前 owner PAT 对 Actions permissions API 返回 403（需 Administration 能力或 UI）。若发布/actuate 失败指向权限，由所有者在 UI 勾选。

## 明确非目标

- 不向 Codex Cloud Environment 注入凭据（D-026）
- 不宣称 App 沙箱获得 `gh`
- 不绕过 D-037 / CI 绿灯
