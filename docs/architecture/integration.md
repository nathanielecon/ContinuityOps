# ContinuityOps integration architecture

## Purpose

Adapt pinned Project A (landing-zone / governance) and Project C (app delivery)
contracts into ContinuityOps without editing upstream repositories.

## Pin authority

Exact SHAs live in `integration/upstreams.lock.json`. Any pin change invalidates
S1+ evidence that embeds the lock hash.

Current Project C pin (A2 Option 2): `376b7e18c5cc94e67ff180ca2f42b8eb05535be3`
with ECR digest `sha256:bffa93adcbe247be118de0726842f673e14310052b3fdcd6ddaa853fbc05c229`.

## Consumed surfaces

### Project A (adapter)

| Contract | Path | Status |
| --- | --- | --- |
| Network boundary | `integration/contracts/project-a.network.json` | stub |
| IAM / OIDC interfaces | `integration/contracts/project-a.iam-oidc.json` | stub |
| State backend interface | `integration/contracts/project-a.state.json` | stub |
| Governance / tagging | `integration/contracts/project-a.governance.json` | stub |

### Project C (adapter)

| Contract | Path | Status |
| --- | --- | --- |
| Release identity | `integration/contracts/project-c.release.json` | digest proven; rollback none proven |
| Smoke endpoints | `integration/contracts/project-c.smoke.json` | from packet (`/health/live`, `/health/ready`, `/version`, `/quotes`) |
| App release contract | `app-contract/release-contract.json` | ContinuityOps-owned |
| Context packet | `integration/upstreams/packets/2026-07-18-a-c/` | D-028 / CO-006 |

## Explicit missing capabilities

`integration/upstreams.lock.json` → `missing_capabilities` is empty after A2 Option 2.

**Resolved by packet:** `MC-A-TREE`, `MC-C-TREE`, `MC-C-DIGEST`, `CO-006`, `CO-004`
(`integration/upstreams/packets/2026-07-18-a-c/manifest.json`).

## Claim level (S1 / P1-T01)

| Component | Claim | Allowed wording |
| --- | --- | --- |
| Lock + adapter JSON + static tests | **L1** | Static validated offline |
| Upstream tree packaging (D-028) | **L1 packet** | `integration/upstreams/packets/2026-07-18-a-c` |
| Project C image digest at pin | **L1 proven** | ECR digest bound to pin via phase-9 governing-manifest |
| Known-good rollback | **none proven** | Explicit; phase-6 fixtures are not ContinuityOps rollback |
| Cloud-applied landing zone from A | **not L4** | Not applied in this slice |

## Remaining boundaries

- No ContinuityOps mutation of A/C repositories.
- No production or multi-account claim.
- Rollback for ContinuityOps pin remains **none proven**.
