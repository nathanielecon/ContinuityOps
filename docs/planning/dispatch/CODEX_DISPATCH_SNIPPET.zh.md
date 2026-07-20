# App 路径 `@codex` 派遣必贴片段(D-034)

将下列块粘贴到每一次所有者/监督者发布的 `@codex` 评论末尾(任务正文之后)。

> **Tip 可见性(D-CC-001):** 对非 `main` 候选 tip 的派遣，须先通过 [`TIP_VISIBILITY_SMOKE.zh.md`](./TIP_VISIBILITY_SMOKE.zh.md)。权限边界见 [`WORKER_PERMISSIONS.md`](./WORKER_PERMISSIONS.md)。总计划 [`CHIEF_COASTS_FRAMEWORK_PLAN.md`](./CHIEF_COASTS_FRAMEWORK_PLAN.md)。

```text
完成定义(硬门槛,D-034):最终回复必须包含可机械发布的完整 unified diff。
禁止:仅 make_pr / "PR 元数据" / 无 patch 标记的摘要并宣称完成。
容器内不要尝试 git push / gh pr create(沙箱无 remote/gh,常 403)。

在摘要末尾**原样**输出下列结构(base_sha 为你开工时目标分支 tip 的 40 位 SHA;
可用 `git rev-parse HEAD` 若工作区即该 tip,否则用派遣评论给出的 baseline):

**base_branch 硬规则(BF-2026-014):** 必须是仓库里**已存在**的分支名。
默认写 `main`。仅当派遣合同明确给出已存在的 stream/orch 分支时才写该分支。
禁止发明不存在的名字(例如 `work`)——否则 `gh pr create` 会以
`Base ref must be a branch` 失败。

<!-- continuityops-patch-v1 -->
base_branch: main
base_sha: <40_hex>
context_remaining: <pct>

```diff
<完整 git diff -- 相对上述 base_sha;须含 diff --git 头>
```

若 diff 超过评论长度,按块拆分并在每一额外围栏前加:
<!-- continuityops-patch-v1 part=2/N -->
(首块可省略 part= 或写 part=1/N;须覆盖 1..N。)

拒绝写入: .github/**、含 secret 的路径、.env*、二进制 patch。
GitHub Actions `codex-patch-publish` 将提取 patch、apply、开 PR 并回评 URL。
平台 Create PR / 控制中心 Publish-CodexCloudTask.ps1 仅为后备。
```

详见 `QUEUE.md` D-034 与 `.github/workflows/codex-patch-publish.yml`。
