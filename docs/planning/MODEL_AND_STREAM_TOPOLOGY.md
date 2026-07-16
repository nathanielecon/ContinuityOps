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
