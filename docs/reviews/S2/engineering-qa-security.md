# S2 engineering / QA / security / evidence review

## Scope

Phase 2 slice S2: Helm workload contract (P2-T01), kind local-only preflight (P2-T02),
failure matrix (P2-T03), integrated gate (P2-T04).

## Engineering

- Digest-pinned Helm chart with probes, resources, PDB, HPA, RBAC, NetworkPolicy, Ingress/TLS placeholders.
- kind scenario labeled `local-only` with `managed_cluster_apply` remaining boundary.
- Synthetic failure matrix + reset recorder (no live cluster mutation).

## QA

- `node --test` covers chart contract and scenarios.
- `node scripts/project.mjs validate P2-T0{1,2,3,4}` wired.

## Security

- Non-root, read-only root FS, drop ALL capabilities.
- Workload identity annotation placeholder; no long-lived cluster credentials in repo.

## Evidence / claims

| Component | Claim |
| --- | --- |
| Helm/policy static | L1 |
| kind runtime | L1 (L2 only if kind+helm present) |
| Managed EKS apply | not claimed (`managed_cluster_apply`) |

## Residual issues

- Managed cluster OIDC apply remains blocked without AWS/GitHub environment credentials.
