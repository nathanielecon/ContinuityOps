# QTI 构建阶段交接书(Codex army handoff)

**这份文件是给作者贴进 Codex 的。** 它不是计划,是一份**无状态 worker 可以独立
执行的规格**——容器里查不到的东西,全部内联在这里。

**目标:先过构建门,再开 judge loop。** judge 之所以慢,一半是因为它们在重新推导
一个 gate 本可以直接告诉它们的事实。先把仪器建好,judge 的每一轮就只花在数学和
源文档忠实度上。

**语言约定:用简体中文推理,交付物用英文。** 代码、注释、accepted strings、stem
文本一律英文且不得缩写。

---

## 0. 前置条件——作者必须先决定,否则以下全部无效

`origin/main` 停在 `6944234`,打包的是 build `2eea45c03ca61ddf`。
当前分支 `claude/deep-scan-typo-check-xuxtgw`(`5ab313d`,领先 6 个 commit)
打包的是 build `4830e942eb6762fb`。

**Codex worker 检出的是 `main`。** 在合并之前派遣任何一个 worker,它构建的是
一个没有 spacing 修复、没有 semantic ledger 的语料——会重新"发现"已经修好的缺陷,
并把 verdict 钉在错误的 hash 上。

> **这是作者的决定,不是 worker 的。合并之前不要派遣。**

---

## 1. 通用硬门槛——每一次派遣都必须原样包含

### 1.1 派遣场所(venue)

- 派遣必须建在 **issue** 上,不能是 PR。`classify-comment` 要求
  `github.event.issue.pull_request == null`;建在 PR 上的派遣不会路由到任何地方。
  这一条曾经让本项目手工驱动了十一轮才被发现。
- issue 必须带 `codex-dispatch` label。
- `@codex` 必须作为**评论**发出,写在 issue **正文**里不会触发 App。曾有三条 lane
  因此空转十四分钟。
- issue 正文第一行必须是可解析的 PR 引用,且**必须是正文里第一个 `#数字`**:

  ```
  Worker PR: #<n>
  ```

  路由器用 `grep -oE 'pull/[0-9]+|#[0-9]+' | head -1` 取第一个匹配
  (`pipeline-zero-hop.yml:263`、`:290`),正文里任何一个先出现的 issue 编号都会
  抢走它。这是**静默误路由**,比缺 PR 报警更危险。

### 1.2 身份自报(硬门槛)

回复的**第一行**必须原样输出下列四行,不得省略:

```
worker_id: <派遣评论里指定的工号,原样抄回>
model: <你实际运行的模型标识>
reasoning: <low|medium|high|unknown>
context_remaining: <pct>
```

**model 与 reasoning 若无法确定,写 `unknown`。禁止猜测、禁止复述派遣里提到的
型号。** 写 `unknown` 是正确行为且不扣分;编造一个看似合理的型号是本项目明确记录
过的失败模式(把"关于工件的报告"当成"工件"本身)。

工号格式 `<UNIT>-<ROLE>-<NN>`,例如 `B1-FIXER-01`。

### 1.3 完成定义(D-034)

最终回复必须包含可机械发布的完整 unified diff。禁止:仅 make_pr、"PR 元数据"、
无 patch 标记的摘要并宣称完成。容器内不要尝试 `git push` / `gh pr create`
(沙箱无 remote/gh,常 403)。

在摘要末尾**原样**输出:

```
<!-- continuityops-patch-v1 -->
base_branch: <已存在的分支名>
base_sha: <40_hex>
context_remaining: <pct>

```diff
<完整 git diff——相对上述 base_sha;须含 diff --git 头>
```
```

`base_branch` 必须是仓库里**已存在**的分支名(BF-2026-014)。发明不存在的名字
(例如 `work`)会让 `gh pr create` 以 `Base ref must be a branch` 失败。

diff 超长时按块拆分,每一额外围栏前加
`<!-- continuityops-patch-v1 part=2/N -->`,须覆盖 `1..N`。

### 1.4 拒绝写入

`.github/**`、任何含 secret 的路径、`.env*`、二进制 patch。
**`codex-patch-publish` 会拒绝整个 patch,不是只拒绝那一个文件。**

> 这一条有一个直接后果:**下面 B9–B12 四个 router 修复,Codex 做不了**,因为它们
> 全在 `.github/workflows/pipeline-zero-hop.yml` 里。那四项归监督者。派遣时不要
> 把它们发给 worker——patch 会被整体拒收。

### 1.5 构建与验证

```bash
cd docs/math-corrections/qti && ./build.sh
sha256sum zips/sha256sums.txt | cut -c1-16      # 必须是 4830e942eb6762fb
```

hash 不符就**停下来报告**,不要继续。钉在错误 build 上的结论没有价值。

所有 shell 命令加 `rtk` 前缀,`&&` 链里也要加。RTK 只过滤工具输出,少了它只会更慢,
不会更错。

### 1.6 证伪是强制的(AGENTS-2.0 §7)

> **A gate that cannot fail proves nothing.**

每个单元都必须交两样东西:

1. **阳性对照**——干净语料通过,先跑,并且要证明你的探测器真的看见了语料
   (曾有一个 trial 目录名带 `[...]`,被 `glob` 当作字符类,14 个包全部不可见,
   而 197 个 mutation 全报"已捕获")。
2. **注入证明**——把缺陷注入进去,gate 必须以它自己声明的理由失败。
   mutation 必须断言落在**解析后的树**里,不是文本里。

只有阳性对照没有注入证明的单元,视为未完成。

---

## 2. 工作单元——按文件互斥,可并行派遣

每个单元 = 一个 issue、一个 worker、一个 patch。**没有两个单元碰同一个文件**,
所以并行派遣的 patch 之间不会冲突。

---

### B1 · `recompute.py` —— 独立重算 125 个数值键

**文件:** `docs/math-corrections/qti/recompute.py`(新建)、
`docs/math-corrections/qti/build.sh`(加一行)

**为什么。** 目前**没有任何代码**独立验算数值。`battery.py` 的探针是**从 key 派生**
的,所以它按构造就同意 key;`ledger.py` 冻结 (stem, key) 这一对,但 `LEDGER.md`
自己写明*"Freezing a wrong answer makes it permanent, not correct."* 125 个 key,
零次独立重算。

**不变量。** 对每一个 `numerical_question`:从**显示出来的 stem** 里解析算式,
独立求值,与 key 比较。

**硬性约束:**

- **不得 import `finalize.py`。** 理由与 `check_ledger_independence()` 对 ledger
  的约束相同:生成器检查自己的输出,只是一种昂贵的自我比较。
- 三种结果必须**分开报告**:`MATCH` / `MISMATCH` / `UNPARSEABLE`。
- **`UNPARSEABLE` 必须列出并计数,绝不能静默通过。** 一个"读不懂就跳过"的重算器
  正是 AGENTS-2.0 §8 里的 *guard never asserted* 形状,它会打印一行自己没有挣到的
  绿字。输出必须能让人算清:`parsed + unparseable == 125`。
- 接进 `build.sh`,放在 `validate.py` 之后;任何 `MISMATCH` 让 build 失败。

**证伪。**
阳性对照:干净语料 → `0 MISMATCH`,且 parsed 数与 census 对得上。
注入:把 `g6_s1_b1` 的 stem 从 `8 + 3 × 4` 改成 `8 + 3 × 5`,key 保持 `20`
→ 必须 `MISMATCH`。这正是 `LEDGER.md` 记录的、今天能通过全部 1,497 个探针的那个
mutation。

**验收。** build 绿;注入失败;`UNPARSEABLE` 清单显式列出且每一条附原因。

---

### B2 · `sweep_validate.py` —— 把证伪扫描推广到整个 gate

**文件:** `docs/math-corrections/qti/sweep_validate.py`(新建)

**为什么。** `validate.py` 有约 119 处 `fails.append`,大部分在一个 1200 行的
`check()` 里(`validate.py:612`)。`sweep_ledger.py` 证明了 ledger 的 6 条规则,
其余的没有。AGENTS-2.0 §7 要求每条规则都由注入证明,大约十条从来没有过。

**不变量。** 逐条规则:一个应当触发它的 mutation;先跑阳性对照;mutation 断言落在
**解析后的树**里。输出 `PROVED` / `UNPROVED` / `HOLED`。

**关键:`UNPROVED` 清单必须打印出来,不能省略。** 这个工具的价值就在于把"覆盖率"
从散文声明换成机械答案——包括 `CHECKLIST-NUMERIC 2.0` 自己标注的那句
*"per-rule coverage counts are the judge's own claims and are not independently
verified"*。

照抄 `sweep_ledger.py` 的结构(自建 baseline 树,不依赖 fixture;全部 `os.walk`
不用 `glob`;命名空间安全地用 `e.tag.split('}')[-1]`)。

**证伪。** 这个工具本身也要阳性对照:先在**未改动**的语料上跑,报告必须是
"零 mutation 被捕获"以外的合理结果;再确认它能区分 `HOLED`(注入了但 gate 没抓到)
与 `UNPROVED`(没写 mutation)。二者混为一谈就等于把"没查"报成"查过了"。

**验收。** 报告可读;`UNPROVED` 与 `HOLED` 分列;不虚报。

---

### B3 · `validate.py` —— 补 R8 与 R9

**文件:** `docs/math-corrections/qti/validate.py`

原文在 `docs/math-corrections/qti/judge/CHECKLIST-NUMERIC-81e700c3.md:108-127`,
**以那里的措辞为准,不要以本节摘要为准**。

**R8 —— key、评分树、response 绑定三者一致。**
每个数值 item 的 response declaration、response ident、`<varequal>` 值、
`<respcondition>`、置分分支必须绑定到**同一个** student response。每个预期接受值都要
能到达满分分支,任何非预期值都不能。
*若为假:* 学生打出包里写着的正确 key 却拿不到分(评分条件读的是另一个 response
ident),或者一个错误值通过非预期的替代分支拿到了分。

**R9 —— 拆分守恒。**
凡是由源题拆分产生的数值 item,拆分族必须**恰好一次**地保留每一个源子问题,保留源题
的承重措辞与共享语境,且不新增数学要求。每一半都能独立作答,所有半题合起来问的正好
是源题问的。
*若为假:* 学生答对了作业,却在一个被改过题意的半题上被判错;或者某个源子问题在拆分
中消失,从未被考到;或者重复的半题让同一份正确工作被扣两次分。

**证伪。** 每条各一个注入 + 阳性对照。R8:把某个 item 的 `<respcondition>` 指到另一个
respident,gate 必须失败且报出 R8 自己的理由。R9:删掉一个拆分半题,或把某半题的
数字改成与源题不符,gate 必须失败。

**验收。** 两条规则都 `PROVED`(用 B2 的扫描确认,如果 B2 已落地)。

---

### B4 · `acceptance.py` —— 用生成器取代手写验收账本

**文件:** `docs/math-corrections/qti/acceptance.py`(新建)、
`docs/math-corrections/qti/ACCEPTANCE.md`(生成)、
`docs/math-corrections/qti/CHANGES.md`(只改语料规模数字)

**为什么(这是本轮最难看的一处)。** `ACCEPTANCE.md` 不只是过期,而是**无据**:

- 它钉了三个已被取代的 hash(`2728bd5a` / `775b3982` / `4ee5bb50`,`:141`),
  `4830e942` 一次都没出现;
- 它声称语料是 177 项,而 gate 期望 199(`validate.py:73`);
- **它的 answer-format 表格在磁盘上没有任何支撑报告**——六行、约三十个 verdict 格,
  `judge/` 下不存在 `SELECTALL*`、`SHORTANS*`、`NUMERIC*`、`AUTHORED*`、`STRUCT*`
  任何一个报告文件;
- 它与实时看板直接矛盾:它说 SHORTANS 与 NUMERIC 已验收,`LANES.md` 显示两者都
  `fail`;
- `SOURCE` 这个 slice 在表里**根本没有行**。

(表一,即 format round 之前那张表,是对得上的:52 个报告对 52 个格,无孤儿也无幻引。)

**不变量。** 生成器读 `judge/*.md` 与 `evidence/judges/qti/*.json`,产出
`ACCEPTANCE.md`,每个 verdict 都钉在它被渲染时的 build hash 上。

**关键:磁盘上没有对应文件的行,渲染成 `unbacked`,而不是渲染成一个分数。**
手工维护的账本正是"五个 slice 被标成已验收而背后什么都读不到"的成因。理由与
`lanes.py:6-10` 已经写下的完全一样。

**顺带修:三个语料规模同时活着**——175(`CHANGES.md:534`)、177
(`ACCEPTANCE.md:148`)、199(`validate.py:73` 与四份 checklist)。统一成由
artifact 推导出来的那一个。

**证伪。** 造一行引用不存在报告的验收声明 → 必须渲染成 `unbacked`;把一个真实报告
移走 → 对应行必须从有分数变成 `unbacked`。

---

### B5 · 重新推导四份冻结 checklist

**文件:** `docs/math-corrections/qti/judge/CHECKLIST-{NUMERIC,SHORTANS,SOURCE,STRUCT}-4830e942.md`(新建)

现有四份钉在 `81e700c3f40bb7b5`,且每一份都自己写明:
*"a changed build hash invalidates the counts and requires re-derivation rather
than amendment."*

**重新推导,不是修订。** 规则条文延续(NUMERIC R1–R10、SHORTANS R1–R15、
SOURCE R1–R10、STRUCT S-01…S-52);**计数必须对着 `4830e942eb6762fb` 重新数**。
旧文件保留不动。

"规则延续、计数重绑"是对 `MASTER_PROMPT` §6 的一处**有意偏离**,请在文件里写明
这一点,不要让它看起来像疏忽。

---

### B6 · `evidence/judges/qti/` —— 给 judge loop 一个落点

**文件:** `evidence/judges/qti/README.md`、`evidence/judges/qti/SCHEMA.json`(新建)

目录存在但**是空的**。`lanes.py:120` 读
`evidence/judges/qti/<SLICE>-<build7>.json`;`pipeline-zero-hop.yml:16`、`:440`
在 `pull_request` 上读 `evidence/judges/**`。**从来没有一份 QTI judge 证据落到过
这个位置**,所以 PR 侧那一跳(`judge-merge-ready-no`)对本工作流是死的。

**Schema 字段:** `worker_id`、`model`、`reasoning`、`build`、`slice`、`score`、
`items_worked`、`merge_ready`(`yes|no|provisional`)、`findings[]`。
`extract-merge-ready.mjs` 读 `merge_ready`,字段名不得改。

README 要写清:散文报告仍然是主交付物,JSON 只负责机器路由。

---

### B7 · `scripts/pipeline/parse-verdict.mjs` —— 放宽单一 bot 过滤

**文件:** `scripts/pipeline/parse-verdict.mjs` 及其测试

现在硬过滤 `if (login !== 'chatgpt-codex-connector[bot]') continue;`,任何其他作者
的 verdict 一律返回 `null`。改成 allowlist(默认仍含 Codex App bot),保留既有优先级
(JSON → `verdict:` 行 → 宽松匹配)与全部测试。

对纯 Codex army 这一条不是瓶颈,但它是"这条流水线只认得 Codex"的原因,值一个单元。

**证伪。** 一条来自 allowlist 外作者的评论仍返回 `null`;allowlist 内的返回
`pass|fail`;既有测试全绿。

---

## 3. 监督者自留项(Codex 不能做)

以下四项全在 `.github/workflows/pipeline-zero-hop.yml`,落在 §1.4 的拒绝写入清单里
——发给 worker 会导致 **patch 被整体拒收**。

| # | 缺陷 | 位置 | 修法 |
|---|---|---|---|
| **B8** | **没有 re-score 路由,循环在物理上无法闭合。** `classify-comment` 只能发出五个 action:`page-chief`、`nixer-to-fixer`、`publish-ok-d037`、`publish-failed-renudge`、`d037-verdict`。规定的循环是 *judge → nixer → fixer → **同一个 judge 复评** → cold judge*;fixer 的 patch 发布时没有任何东西把它送回找出缺陷的那个 judge——`publish-ok-d037` 开的是独立的 D-037 reviewer。**每一个 fixer patch 都会让 lane 停下来等人。** | `:72-141` | 新增 `fixer-to-judge`:issue 标题匹配 `FIXER` 且 `publish-ok` 时,在原 judge lane issue 上重新 `@codex` 评论,带上新 PR 与 D-034 片段。按 PR 号幂等。 |
| **B9** | **`d037-verdict` 可能静默打到错误的 PR。** `head -1` 取正文里第一个 `#数字`,散文里先出现的任何 issue 编号都会抢走它。 | `:263`、`:290` | grep 锚定 `^Worker PR:`,找不到再退回宽松匹配,并记录走了哪条分支。 |
| **B10** | **`judge-merge-ready-no` 对 QTI 是死的。** 读 `evidence/judges/**`,而 `evidence/judges/qti/` 从未收到过文件。 | `:16`、`:440` | B6 建好目录后,用注入确认这一跳真的会触发。 |
| **B11** | **路由器自动开出的每一个 fixer 都用 1.x 派遣片段。** 共 **10 处** `cat CODEX_DISPATCH_SNIPPET.zh.md`,横跨五个 job;没有任何 workflow 引用 `2.0`。于是路由器自动开出的工作全都没有身份自报门槛,不可归属——而手工派遣有。**修一处会漏九处**,这正是 AGENTS-2.0 §8 的第一个形状。 | `:219`、`:320`、`:328`、`:374`、`:410`、`:419`、`:476`、`:486`、`:553`、`:563` | 十处全部指向 `CODEX_DISPATCH_SNIPPET.zh 2.0.md`;改完后 grep 断言 `zh.md` 的引用数归零。 |

另记:`.github/workflows/` 与 `scripts/pipeline/` 里**没有任何 Cursor 接线**。
那十一条 `cursor/*` 分支是手推的,没有路由器看得见它们。所谓 "Codex-Cursor
pipeline" 目前是 Codex-only。

---

## 4. 本阶段的验收门(过了才开 judge loop)

1. `./build.sh` 绿,**零 warning**,连续两次字节一致。
2. `recompute.py`:每个 key 要么 `MATCH`,要么显式列在 `UNPARSEABLE` 里并附原因。
   零静默跳过。
3. `sweep_validate.py`:每条规则要么 `PROVED`,要么列在 `UNPROVED` 里并说明为什么。
4. 每条新规则**双向证伪**:干净语料通过,注入的缺陷以它自己声明的理由失败。
5. semantic ledger **0 drifted**。若有 drift,必须**逐分量复核后**再冻结
   (0 added/removed、0 contract drift、**0 accepted strings lost**)。
   *为了把红的 build 变绿而重新冻结,会摧毁这个文件存在的全部意义。*
6. `ACCEPTANCE.md` 由生成器产出,钉在实际发布的 hash 上,没有任何无据声明被渲染成
   分数。
7. 全仓一个语料规模数字。

到这一步,关于语料的每一个断言都由一个**被证明过会失败**的仪器作出。judge loop 才
开始,而且 judge 的每一轮只花在数学与源文档忠实度上。

---

## 5. 本阶段明确不做

- **SOURCE 源文档忠实度**——需要源 PDF 和数学判断,是 judge 的活,机械化不了。
- **任何语料内容修改。** 仪器发现的缺陷记录下来,留到 judge loop 里修,不在这里修。
- **Canvas 实机导入**——需要 URL、token 和 scratch course。它们不在本仓库里,
  **也不得进入任何模型的上下文**。见 `TEACHER_ACTIONS.md`。
- **三处纸面缺陷**——需要拿着源文档的人。
- **QTI 独立仓库拆分**——作者已说明是最终目标;值得在后续流水线工作之前做,而不是之后。
