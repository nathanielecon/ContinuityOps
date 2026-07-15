# Baseline Scaffold Audit (P0-T01)

- **Baseline SHA:** `39eaf03f749ec828c39d2e3da75efaf3392be2e8`
- **Audited by:** Claude Opus 4.8 (portfolio supervisor / adapter role) — *actual*
  model; the plan's Codex/Grok topology is not invokable in this execution
  environment and is therefore recorded as designed-not-run where referenced.
- **Upstream pins:** `integration/upstreams.lock.json` — Project A
  `nathanielecon/aws-landing-zone-lab` @ `f688065`, Project C
  `nathanielecon/local-first-governed-cicd` @ `0f54def`
  (image digest not yet resolved). These are the renamed repository paths the
  lock actually pins; earlier planning prose used the pre-rename names
  `cloud` / `project-c-cloud`.

## File classification

| Class | Paths | Disposition |
| --- | --- | --- |
| retain | `docs/planning/**`, `docs/architecture/**`, `README.md`, `EVIDENCE_AND_CLAIMS.md`, `PLAN.md`, `AGENTS.md`, `OPERATING_STATE.md`, `BREAK_FIX_LOG.md` | authoritative plan; unchanged |
| generate | `harness/**`, `scripts/**`, `tests/**`, `docs/scaffold-audit.md`, `STATUS.md`, `ISSUES.md`, `DECISIONS.md` | S0 harness built this session |
| retain | `integration/upstreams.lock.json`, `.gitignore` | pins + ignores |
| quarantine | none | — |
| remove | none | — |

## Slice ownership

Construction partition is frozen in `harness/partition-manifest.json`. Every
retained/generated code path has exactly one primary slice owner
(`partition_unique_ownership` validator confirms no duplicates). The shared
interface partition `S0-IFACE` (`harness/schemas/*`) is certified before its
dependents `S0-CLI` and `S0-VALIDATE`.

## Deviations recorded honestly

1. **Worker engine.** The plan specifies Codex 5.4 CLI + Grok Ralphy streams.
   Neither is present or invokable in this container (no CLI, no credentials).
   All workers/judges this session are Claude subagents, recorded with their
   real model ids. The `model_routing` validator fails closed on any evidence
   that claims an uninvokable engine without a `sim`/`planned` marker.
2. **TypeScript 7.0.2 pin.** Not used. The harness is plain Node ESM so tests
   run deterministically here without a questionable compiler pin. A
   `typescript_7` validator is described in the plan but is intentionally not
   registered this session because no TypeScript is present; the live
   `harness/state/tasks.json` references only the 8 validators that are actually
   implemented, so nothing fails closed for a missing validator.
3. **Live cloud.** No AWS/EKS/serverless resources were created. Phases 1–8
   remain unauthorized (`authorized_through_phase = 0`) and human-gated.
