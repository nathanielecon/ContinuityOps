# ContinuityOps Decisions

Append-only decision log.

| ID | SHA | Decision | Status |
| --- | --- | --- | --- |
| D-101 | 39eaf03 | Build S0 harness as plain Node ESM (no TS7 pin) so tests run deterministically in this environment. | accepted |
| D-102 | 39eaf03 | Workers/judges are Claude subagents; evidence records actual model ids. No GPT-5.4/Codex mislabeling. | accepted |
| D-103 | 39eaf03 | Stop at H0. Phases 1–8 (live cloud) are not executed and remain human-gated. | accepted |
| D-104 | 39eaf03 | Accuracy check = independent fresh-council Claude judges over the frozen partition manifest, per RALPHY_ORCHESTRATION.md §9–10. | accepted |
