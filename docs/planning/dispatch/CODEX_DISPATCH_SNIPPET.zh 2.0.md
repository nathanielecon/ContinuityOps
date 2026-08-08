# App 路径 `@codex` 派遣必贴片段 2.0(D-034 + 工号/模型自报)

**2.0 新增(不改 1.x,1.x 仍然有效):** 每个 worker 必须在回复开头自报
**工号、模型、推理档位、剩余上下文**。

**为什么加这个。** 监督者一直在派遣里写"all workers are 5.4 medium",但从未
验证过——worker 不报模型,任务链接无法从会话内抓取,环境设置也只是请作者去改
而没有确认。于是"5.4 medium"是一句复述,不是一个事实。同一类错误今天已经让
venue 和 D-034 片段各丢掉了好几轮。**自报把这件事从假设变成记录。**

同时,并发 lane 越来越多(SHORTANS / NUMERIC / SOURCE / STRUCT,各带
judge / nixer / fixer),没有工号就无法区分"同一个 judge 复评"和"另一个
judge 冷读"——而这个区别正是验收规则的核心。

将下列块粘贴到每一次所有者/监督者发布的 `@codex` 评论末尾(任务正文之后)。

```text
身份自报(硬门槛 2.0):回复的**第一行**必须原样输出下列四行,不得省略。

worker_id: <派遣评论里指定的工号,原样抄回>
model: <你实际运行的模型标识>
reasoning: <low|medium|high|unknown>
context_remaining: <pct>

**model 与 reasoning 若无法确定,写 `unknown`。禁止猜测、禁止复述派遣里
提到的型号。** 写 `unknown` 是正确行为且不扣分;编造一个看似合理的型号是
本项目明确记录过的失败模式(把"关于工件的报告"当成"工件"本身)。

工号由监督者在派遣中指定,格式 <LANE>-<ROLE>-<NN>,例如
SHORTANS-JUDGE-03、K6-FIXER-01、STRUCT-NIXER-02。原样抄回,不要改写。

---

完成定义(硬门槛,D-034):最终回复必须包含可机械发布的完整 unified diff。
禁止:仅 make_pr / "PR 元数据" / 无 patch 标记的摘要并宣称完成。
容器内不要尝试 git push / gh pr create(沙箱无 remote/gh,常 403)。

在摘要末尾**原样**输出下列结构(base_sha 为你开工时目标分支 tip 的 40 位 SHA;
可用 `git rev-parse HEAD` 若工作区即该 tip,否则用派遣评论给出的 baseline):

**base_branch 硬规则(BF-2026-014):** 必须是仓库里**已存在**的分支名。
禁止发明不存在的名字(例如 `work`)——否则 `gh pr create` 会以
`Base ref must be a branch` 失败。

<!-- continuityops-patch-v1 -->
base_branch: <已存在的分支名>
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

---

判分角色附加(见 `judge/JUDGE_OUTPUT_CONTRACT 2.0.md`):
判分回复必须另含一行 `verdict: pass|fail`,并在 patch 中写出
`evidence/judges/qti/<SLICE>-<build7>.json`(含 merge_ready / score /
items_worked / findings)。散文仍是主交付物,JSON 只负责机器路由。
**判分者不被告知阈值,也不自行设定阈值**——只报 score 与 findings。
```

详见 `QUEUE.md` D-034、`.github/workflows/codex-patch-publish.yml`、
`.github/workflows/pipeline-zero-hop.yml`(D-047)。
