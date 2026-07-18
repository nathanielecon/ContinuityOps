# Upstream adapters (Projects A and C)

ContinuityOps consumes pinned upstream SHAs without modifying those repositories.

| Upstream | Pin file | Adapter contracts |
| --- | --- | --- |
| Project A (`aws-landing-zone-lab`) | `integration/upstreams.lock.json` → `project_a` | `integration/contracts/project-a.*.json` |
| Project C (`local-first-governed-cicd`) | `integration/upstreams.lock.json` → `project_c` | `integration/contracts/project-c.*.json`, `app-contract/` |

## Access boundary (CO-006 / D-028)

Worker environments receive **data, not permission**. If the pinned trees are not
readable in the worker container, adapters remain stubs with explicit
`missing_capabilities` entries. The control center must supply a context package
or read-only vendored snapshot before raising claim levels above L1 for
upstream-derived runtime facts.

## Claim honesty

- Adapter JSON and static tests ⇒ **L1** (designed/static validated).
- Hosted workflow stubs that have not run against OIDC ⇒ not L3 for cloud plan/apply.
- Never claim L4 cloud-applied without apply evidence.
