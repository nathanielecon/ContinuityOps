# Model, Cloud-Agent, Stream, and Bottleneck Topology

## Requested default

| Layer | Default | Responsibility |
| --- | --- | --- |
| Portfolio supervision | Claude 5 cloud (minimal intervention) | Global objective, stream creation, co-orchestrator appointment, convergence; reviews branches only on completion signal |
| Co-orchestration | Claude Sonnet/Opus cloud | One bounded stream when appointed |
| Ralphy orchestration/councils | Claude Opus 4.8 cloud | Stream control, judges, nixers, fixers, bottleneck reasoning (supersedes Grok 4.5 High Fast; D-022) |
| Code execution | Warm Codex 5.4 CLI Cloud Agent, default mode (not `/high`, not `/fast`) | Complete bounded implementation and tests; pre-set-up environment; reports `context_remaining` on handoff (D-023/D-024) |
| Cloud apply | Protected GitHub Actions OIDC | Live cloud mutation and evidence, never Cloud Agent credentials |

All worker-facing instructions and communication are Simplified Chinese.
Recruiter-facing repository surfaces are English.

## Concurrent Ralphy streams

- Default maximum: three implementation streams plus the supervisor.
- Each stream is sequential and has one mutation owner.
- Streams must own disjoint logical construction partitions.
- Shared interfaces are content-addressed and frozen before dispatch.
- Each stream uses a distinct branch/workspace and evidence namespace.
- Integration is serialized by the lead orchestrator.
- A shared-interface change pauses all dependent streams and invalidates their
  affected evidence.

Suggested construction waves:

| Wave | Stream A | Stream B | Stream C |
| --- | --- | --- | --- |
| 0 | harness/authority | model/proxy/language contracts | upstream inventory |
| 1 | Terraform/GitOps | application contract | architecture/evidence schemas |
| 2 | Kubernetes | serverless/SaaS | observability instrumentation |
| 3 | incidents/runbooks | security/agentic | recovery/performance/FinOps |
| 4 | post-build repartition | recruiter assets | integrated evidence |

The exact wave map is produced from the repository dependency graph; this table
does not authorize overlapping interfaces.

## Warm Codex Cloud environment

The authoritative worker specification (D-026). Five points:

1. **One Environment per repo.** Create it in the Codex UI with caching On.
2. **Two in-repo scripts only.** `.codex/cloud-setup.sh` (Setup) and
   `.codex/cloud-maintenance.sh` (Maintenance) are the only content pasted into
   the Environment; they are versioned and change-controlled in the repo.
3. **Zero credentials in the container.** Adding any environment variable or
   secret to the Environment invalidates the ~12h cache and is out of bounds.
4. **Warm gate before every dispatch.** `scripts/Invoke-CodexCloudWarm.ps1`
   (control-center only) re-warms through a smoke task when `lastWarmUtc` is
   missing or older than ~10h, then stamps the machine-local registry.
5. **Dispatch pattern.** `codex cloud exec --env <ENV_ID> --branch <branch>
   "<task>"`, then poll status, local diff/apply, verify, and open a PR. The
   task never runs git itself; the orchestrator owns integration. Warmth is
   isolated per Environment/repo (~12h) and never carried across repos.

Red lines: adding a secret to the Environment, editing the setup scripts ad
hoc, or bypassing the warm gate are all out of bounds.

## Dispatch topology

The owner's Windows control-center session (local Claude Code, codex-cli,
`pwsh`, machine-local `environments.json` registry) is the sole dispatch point
(D-027). Cloud containers and cloud workers are receive-only: no warm gate, no
`codex cloud exec`, no Codex credentials. A cloud orchestrator requests a Codex
cloud task either in its report to the control center or by leaving a durable
GitHub marker (issue/comment) as the dispatch backlog the control center polls.

Cross-repo material follows "the worker gets data, not permission" (D-028):
context packaging (default) or a read-only vendored snapshot with recorded
source SHA, never a widened worker-container repository grant.

The earlier Cursor Cloud Agent framing of this workflow is **superseded** by the
control-center dispatch topology above.

## Bottleneck subagents

The lead orchestrator provisions a bottleneck subagent in the current
supervisory session when a stream cannot reach a necessary surface.

| Profile | Typical trigger | Default authority |
| --- | --- | --- |
| `auth` | missing/incorrect identity, login or token boundary | read-only diagnosis |
| `github-actions` | hosted check/log/runner-only failure | inspect runs/logs, propose fix |
| `aws-gitops` | OIDC, plan/apply, state or cloud evidence blocker | hosted-path diagnosis; no local keys |
| `kubernetes` | cluster scheduling, policy, ingress, DNS, rollout | lab diagnostics within approved scope |
| `observability-dashboard` | alert/dashboard/trace surface unavailable | inspect signal path and evidence |
| `toolchain` | missing compiler/scanner/runtime or version mismatch | pinned bootstrap/compatibility diagnosis |
| `browser-evidence` | public dashboard or rendered visual verification | read-only capture/verification |

Diagnosis does not grant mutation. Any fix becomes a separately scoped task.

## Claude proxy experiment

Cloud-only Claude agents may run the pinned profile:

```bash
npx --yes pxpipe-proxy@0.9.0
export ANTHROPIC_BASE_URL=http://127.0.0.1:47821
```

Required gates:

1. package integrity/provenance and dependency review;
2. provider and organizational-policy approval;
3. no credential or raw sensitive prompt logging;
4. direct and proxy health checks;
5. direct fallback for every critical orchestration step;
6. measured input tokens, latency, failures, and output quality;
7. no claim that the proxy guarantees a 2–3× quota increase;
8. no proxy-compressed artifact accepted as source evidence unless the original
   repository/evidence remains directly inspectable.

## TypeScript 7

Where TypeScript is used:

- pin `typescript@7.0.2` initially;
- enable strict type checking;
- pin Node and package-manager versions;
- prohibit mutable `next`/unbounded ranges;
- validate build, tests, lint, typecheck, runtime compatibility, and generated
  declarations;
- route a compiler upgrade through dependency review and all affected final
  partition councils.

## Saved and fresh council experiment

The saved remediation cohort persists until provisional pass. It cannot certify.
Three fresh judges certify without saved context. A fresh failure retires the
repair cohort and triggers fresh nixers/fixers, a new SHA, fresh evidence, and
another new judge council.

The break/fix log is updated on every loop and every stream.
