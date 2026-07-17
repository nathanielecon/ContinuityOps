# S0 Baseline Scaffold Audit

- task_id: P0-T01
- baseline_sha: `6ed243564ddb46f4a46608496d6f05db53c93788`
- workspace_head_at_audit_start: `7e8a525f131859ce08ee8e108d2c0bb877b311ab`
- claim_ceiling: `repo-only`
- contract_read_status: `blocked_missing_in_workspace`

## Scope note

本审计仅使用当前仓库工作区可读内容。任务要求的 `docs/planning/dispatch/P0-T01.zh.md` 在当前工作区不存在，因此未伪造契约内容；执行仍受触发文本、AGENTS.md 与四路径写入范围约束。

## Upstream pins

- Project A: `f688065c7705ab7d3febcd9ec2842bea4d8bed87`（来自既有 `integration/upstreams.lock.json`；未直接读取上游仓库）。
- Project C: `0f54def53fbfda9747c8ea27235eaac1da831aec`（来自既有 `integration/upstreams.lock.json`；镜像 digest 为 `UNAVAILABLE`；未直接读取上游仓库）。

## Shared interfaces

- `PLAN.md` — machine-readable task authority and phase gate；消费者：all-slices。
- `OPERATING_STATE.md` — current state and issue ledger；消费者：all-slices。
- `integration/upstreams.lock.json` — Project A/C upstream pin contract；消费者：S0-governance-control-plane, future-integration-slices。
- `harness/partition-manifest.json` — unique path ownership partition contract；消费者：all-implementation-streams。
- `EVIDENCE_AND_CLAIMS.md` — claim-level evidence policy；消费者：evidence-review, qa-review, security-review。
- `docs/planning/JUDGE_RUBRICS.md` — frozen review rubric source；消费者：judge, nixer, fixer。

## Retained path classification

| Path | Category | Primary slice | SHA-256 |
| --- | --- | --- | --- |
| `.codex/PROMPT-SPEED-ADDENDUM.md` | `markdown-governance-or-documentation` | `S0-control-lane-tooling` | `de2610d9087a05c12024eb9c8f7f4d8f7e2f15b4191bbc5906a6155890d2beab` |
| `.codex/README.md` | `markdown-governance-or-documentation` | `S0-control-lane-tooling` | `7aba3de90347531b5ff4d60b045a105b008aeb9317fb15ad862bb71a3b96f7fd` |
| `.codex/cloud-maintenance.sh` | `operator-script` | `S0-control-lane-tooling` | `cf6ea0b903864abc617e873cd555ed76de0b69472574edd0083ef6eaebc03523` |
| `.codex/cloud-setup.sh` | `operator-script` | `S0-control-lane-tooling` | `cd199ff11805e2331c05d81a290420360e862497155dfdf31cc378cc4ba30c7a` |
| `.gitignore` | `repository-metadata` | `S0-repository-foundation` | `428370bc460ab31e7549a18b44f46c5c254acf935ee54c2bafa813e3b6fac75a` |
| `AGENTS.md` | `markdown-governance-or-documentation` | `S0-repository-foundation` | `7e53501e4600afd5c8305356af47f27935c1ab156bca8fd04f91b4765c3eb956` |
| `BREAK_FIX_LOG.md` | `markdown-governance-or-documentation` | `S0-governance-control-plane` | `26486d996bca3ccd8907eaf97774294b6be5f082817be4d1beb43787a123fd4f` |
| `EVIDENCE_AND_CLAIMS.md` | `markdown-governance-or-documentation` | `S0-governance-control-plane` | `862941082919dbfe2907e9aae5a7875867209905bcadc69f9750d3f269c63adf` |
| `OPERATING_STATE.md` | `markdown-governance-or-documentation` | `S0-governance-control-plane` | `7e8f5a4f378d3a7833c521e8577fdb113f6c9103187db732dd17b6f5055c7de1` |
| `PLAN.md` | `markdown-governance-or-documentation` | `S0-governance-control-plane` | `68081ca9f091984bfe2609db06714b779f9c8004ded4f99e9a1bdea121dfda2c` |
| `README.md` | `markdown-governance-or-documentation` | `S1-portfolio-documentation` | `c5e2252ab346a05263d9abb1ca98a887a0b8a130224d91e1dbe37a54dbefdc57` |
| `docs/architecture/continuityops-architecture.png` | `architecture-or-portfolio-asset` | `S1-architecture-assets` | `0008b3d26478826d9ae4351003f412baa6845d1769bc5041bbb749f5348a4799` |
| `docs/architecture/continuityops-architecture.svg` | `architecture-or-portfolio-asset` | `S1-architecture-assets` | `0da8f058b8ef18cf4d6cd35bd4ef7ae819f69dc06bc27fbb68dd4f55e8872917` |
| `docs/architecture/continuityops.drawio` | `architecture-or-portfolio-asset` | `S1-architecture-assets` | `a447db8d8f870ef944b1412019790949cd2ba21dea6ce578ac03e3f45879b4e0` |
| `docs/decisions/README.md` | `markdown-governance-or-documentation` | `S1-portfolio-documentation` | `b6c50f966d39b6c4ecfe18b4ab988e08483cad04479fdb1201777c1b167bb07c` |
| `docs/evidence-index.md` | `markdown-governance-or-documentation` | `S1-portfolio-documentation` | `8047533bd0b7b716f4908745ea0faa3073e24d9d2adaff78c0d4f3779ebdcf89` |
| `docs/planning/AGENTS.md` | `markdown-governance-or-documentation` | `S0-governance-control-plane` | `efa7227eb0dce847c29ed90b6fe22c24379cb4a4960ac375a091f4fa941a7989` |
| `docs/planning/BREAK_FIX_LOG.md` | `markdown-governance-or-documentation` | `S0-governance-control-plane` | `26486d996bca3ccd8907eaf97774294b6be5f082817be4d1beb43787a123fd4f` |
| `docs/planning/EVIDENCE_AND_CLAIMS.md` | `markdown-governance-or-documentation` | `S0-governance-control-plane` | `862941082919dbfe2907e9aae5a7875867209905bcadc69f9750d3f269c63adf` |
| `docs/planning/IMAGE2_INFOGRAPHIC_PROMPT.md` | `markdown-governance-or-documentation` | `S0-governance-control-plane` | `f40114d55481f89c519de0b2b7851f0758dd060dda7b884848fe57701f5febe6` |
| `docs/planning/JUDGE_RUBRICS.md` | `markdown-governance-or-documentation` | `S0-governance-control-plane` | `f122c1d0d37fd279dad499ba2149d95ce916cf33e0e651554c59dc1714423a31` |
| `docs/planning/MANDARIN_PROMPT_PACK.md` | `markdown-governance-or-documentation` | `S0-governance-control-plane` | `8a043b52b5d5135bb6c28ddb2e9c6ee837a547eaada32b627323f14adf029f40` |
| `docs/planning/MASTER_PLAN.md` | `markdown-governance-or-documentation` | `S0-governance-control-plane` | `800a056b04b11e41548e6a0b02c292c9cb772de09a14ae448f1f68e3df496c7a` |
| `docs/planning/MODEL_AND_STREAM_TOPOLOGY.md` | `markdown-governance-or-documentation` | `S0-governance-control-plane` | `725fbcba4159ec0ea7fb0e261d6637ac21fe6f36d8b89a615f21d724d32763b8` |
| `docs/planning/OPERATING_STATE.md` | `markdown-governance-or-documentation` | `S0-governance-control-plane` | `7e8f5a4f378d3a7833c521e8577fdb113f6c9103187db732dd17b6f5055c7de1` |
| `docs/planning/PLAN.md` | `markdown-governance-or-documentation` | `S0-governance-control-plane` | `68081ca9f091984bfe2609db06714b779f9c8004ded4f99e9a1bdea121dfda2c` |
| `docs/planning/PROMPT_PACK.md` | `markdown-governance-or-documentation` | `S0-governance-control-plane` | `db938dc44fb3e483e8ebb4db0fc9a7f9cdc117af74183776bf65e38cfaf47168` |
| `docs/planning/RALPHY_ORCHESTRATION.md` | `markdown-governance-or-documentation` | `S0-governance-control-plane` | `3b0d9bb8537fc4a2605613c049d63856f49b57b3249e7a540e2daf1a2d16d41c` |
| `docs/planning/README.md` | `markdown-governance-or-documentation` | `S0-governance-control-plane` | `56e677b0a2afae205ca2acf9c3322f38c0180d6af0c22f889235ad5a81ca11b9` |
| `docs/planning/RECRUITER_FRONT_PAGE_SPEC.md` | `markdown-governance-or-documentation` | `S0-governance-control-plane` | `34dd734fce7dca3cc77a2aef48776280021ff22e4ab52b7b298f35b6a034d1fa` |
| `docs/planning/REPO_README_TEMPLATE.md` | `markdown-governance-or-documentation` | `S0-governance-control-plane` | `afcf517a87ae5d170e4f280befb0ebe55284273ab5c5f7b1c031f063f9e0f659` |
| `docs/planning/SOURCE_ANALYSIS.md` | `markdown-governance-or-documentation` | `S0-governance-control-plane` | `16fe0ca42862468da32f617bade4c9cc94f6f14eb159307658d733ab7c05cf21` |
| `docs/portfolio/continuityops-infographic.png` | `architecture-or-portfolio-asset` | `S1-portfolio-documentation` | `0008b3d26478826d9ae4351003f412baa6845d1769bc5041bbb749f5348a4799` |
| `evidence/README.md` | `markdown-governance-or-documentation` | `S0-evidence-ledger` | `06783de1ea6199ab003c37f4d8d7e6bf2c858e4751496207b58736ae94eec969` |
| `integration/upstreams.lock.json` | `machine-readable-json-contract` | `S0-integration-contracts` | `52c4aefe62b7355e5abea13f4ee79967b5a28363b8f1866cde6b399c1fcbeab3` |
| `scripts/Invoke-CodexCloudWarm.ps1` | `operator-script` | `S0-control-lane-tooling` | `1ce9f61ccf1afd86b8020de503b7602789c7564e161f12c0f8b772bd5ba6d9fb` |
| `scripts/Register-CodexCloudEnvironment.ps1` | `operator-script` | `S0-control-lane-tooling` | `1913464f98e7b0ee839dfcd92bcf0580bb63360e12c4a3c8f7b6dcda2b10813d` |
