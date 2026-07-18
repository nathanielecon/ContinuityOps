# 寻呼片段（D-047）

机械 hop 由 `pipeline-zero-hop` 完成。下列标记用于**例外寻呼**。

## 寻呼首席（durable pager）

在 `codex-dispatch` 或 sticky `[pager] chief-supervisor` issue 评论中原样输出，并确保 issue 带 `chief-pager` 标签：

```text
<!-- continuityops-chief-page-v1 -->
reason: <简体中文一句话>
issue_ids: [88, 91]
recommended_action: replace_junior|ask_owner|observe|intervene_pipeline
context_remaining: <pct_or_unknown>
```

首席每次开席首条命令：`gh issue list --label chief-pager --state open`。

## 寻呼初级（例外唤醒）

GHA 或首席创建 `[codex-dispatch] JR-EXCEPTION-<slug>`，贴 `codex-dispatch` + `junior-exception` 标签，正文含强制 wake packet（JSON），再 `@codex`。

### Wake packet（强制字段）

````text
```json
{
  "schema_version": "1.0",
  "kind": "junior_exception_wake",
  "tip_sha": "<40_hex>",
  "fail_evidence_paths": ["evidence/judges/portfolio/fresh-judge-1.json"],
  "write_scope": [],
  "allowed_decisions": ["reject", "rebind_scope", "escalate"],
  "fail_class": "<stable_hash_or_label>",
  "strike_count": 1,
  "lock_or_interface_cite": "integration/upstreams.lock.json|null",
  "notes_zh": "简体中文上下文"
}
```
````

缺少强制字段时初级必须 `status: failed` 并寻呼首席，不得猜测下一 hop。

## 初级完成硬规则（需 actuation 时）

当合同要求合并/派遣时，仅 Mandarin handoff **不算** complete。必须同时输出 D-042 意图标记（见 `JUNIOR_ACTUATE_SNIPPET.zh.md`），否则 GHA/巡检视为不完整并重催。
