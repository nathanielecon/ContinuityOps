# Kubernetes failure and recovery matrix

Synthetic scenario contracts live under `kubernetes/scenarios/`. Each scenario
records inject / observe / recover / business_check and a reset script.

## Claim boundary

- Scenario JSON + reset recorder: L1 (static / synthetic)
- kind local execution: L2 when kind+helm available
- Managed EKS apply and live failure injection: not claimed (`managed_cluster_apply`)

## Reset

```bash
node scripts/kubernetes/reset-scenario.mjs <scenario-id>
```

Does not mutate a live cluster; writes evidence under `evidence/slices/S2/scenarios/`.
