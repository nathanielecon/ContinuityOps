# Post-H0 Resume Order (portfolio supervisor)

Use only after a **human** H0 receipt is bound into `harness/approvals/H0.binding.json`.

## Immediate

1. Keep-warm check on issue #4 (>9h → `@codex` smoke).
2. Bind human receipt (do not invent fields); re-run `node harness/rubrics/validate-rubric-freeze.mjs`.
3. Mark P0-T04 `verified` via PLAN/state update with evidence.
4. Dispatch **P0-T05** from [`P0-T05.zh.md`](./P0-T05.zh.md): concurrent streams, worker replacement, saved/fresh councils, unauthorized Phase-1 rejection proof.
5. D-037 every worker PR; ≤3 disjoint streams; Mandarin worker free text.
6. On S0 certification: human advances `authorized_through_phase` (N/N+1 authorization tests).

## Phases 1–8 (only after authorization)

| Phase | Focus | Human gate |
| --- | --- | --- |
| 1 | A/C adapters, Terraform/OIDC, hosted workflows | H1 |
| 2 | Helm + live EKS | H2 |
| 3 | Serverless + SaaS lifecycle | slice council |
| 4 | Observability / SLOs | slice council |
| 5 | Incident drills | H3 |
| 6 | Security / agentic ops | H4 |
| 7 | DR / perf / FinOps / teardown | H5 |
| 8 | Portfolio certification | H6 |

Routing (binding for this engagement): warm Codex Cloud only; no Opus; Grok bottleneck only for true local necessity (+ browser on auth fail).

## Pointers

- [`H0_PACKAGE.md`](../../../evidence/slices/S0/H0_PACKAGE.md)
- [`QUEUE.md`](./QUEUE.md)
- [`CODEX_DISPATCH_SNIPPET.zh.md`](./CODEX_DISPATCH_SNIPPET.zh.md)
- Root `PLAN.md` / `OPERATING_STATE.md`
