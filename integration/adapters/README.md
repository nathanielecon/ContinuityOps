# Upstream adapters (Projects A and C)

ContinuityOps consumes pinned upstream SHAs without modifying those repositories.

| Upstream | Pin file | Adapter contracts |
| --- | --- | --- |
| Project A (`aws-landing-zone-lab`) | `integration/upstreams.lock.json` → `project_a` | `integration/contracts/project-a.*.json` |
| Project C (`local-first-governed-cicd`) | `integration/upstreams.lock.json` → `project_c` | `integration/contracts/project-c.*.json`, `app-contract/` |

## Access boundary (CO-006 / D-028)

Worker environments receive **data, not permission**. First validated packet:

`integration/upstreams/packets/2026-07-18-a-c/` (see `manifest.json`).

Refresh with `node scripts/package-upstream-context.mjs` on the control center.
`MC-A-TREE` / `MC-C-TREE` / `MC-C-DIGEST` / `CO-006` / `CO-004` (A2 Option 2)
are resolved by that packet; rollback remains **none proven**.

## Claim honesty

- Adapter JSON and static tests ⇒ **L1** (designed/static validated).
- Hosted workflow stubs that have not run against OIDC ⇒ not L3 for cloud plan/apply.
- Never claim L4 cloud-applied without apply evidence.
