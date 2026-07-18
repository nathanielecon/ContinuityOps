# Dispatch review packets (D-028)

These unified diffs are packaged for Codex App D-037 reviewers that cannot
fetch private GitHub `.patch` URLs (BF-2026-015).

Apply against `main` tip recorded in the companion review issue:

```bash
git apply evidence/dispatch-packets/pr-66-worker-sec-01.diff
git apply evidence/dispatch-packets/pr-67-worker-agentic-01.diff
```

Packets are disposable after the corresponding worker PRs merge.
