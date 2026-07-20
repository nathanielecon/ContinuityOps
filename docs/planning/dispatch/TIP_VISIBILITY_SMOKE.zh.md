# Tip 可见性冒烟（强制门 — D-CC-001 提案）

在对任一 `base_branch` 上的 tip 发起 **×N `@codex` 评判/实现扇出之前**，监督者/编排器必须先开 **一条** `codex-dispatch` 冒烟 issue 并取得绿色结果。

## 通过标准

工人在摘要中证明（exit 0）：

```bash
git fetch origin <base_branch>
git cat-file -t <tip_under_review>    # 期望: commit
git rev-parse <tip_under_review>^     # 必须等于派遣的 candidate_sha（parent-of-tip 模型时）
```

可选回退（仅当 fetch 被拒 **且** 工作区已含 D-028 包）：核对  
`evidence/**/tip-proof-*.json` 与 `TIP_PARENT_PROOF.txt` 中 tip/parent 与派遣一致。

## 标签

- 通过后打 `tip-smoke-ok`（或等价）于冒烟 issue  
- **无此标签不得** 开 provisional/fresh ×3+ 扇出  

## 失败

同 class 两次 → 寻呼首席；禁止改派 Cursor 做体积评判，除非首席记录瓶颈替换。

## 权限

工人仍为 receive-only；冒烟失败优先修 **env fetch / base_branch 物化 / D-028 包**，不授予 push。
