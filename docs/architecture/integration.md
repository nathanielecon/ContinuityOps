# ContinuityOps integration architecture

## Purpose

Adapt pinned Project A (landing-zone / governance) and Project C (app delivery)
contracts into ContinuityOps without editing upstream repositories.

## Pin authority

Exact SHAs live in `integration/upstreams.lock.json`. Any pin change invalidates
S1+ evidence that embeds the lock hash.

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
| Release identity | `integration/contracts/project-c.release.json` | stub (`image_digest=UNAVAILABLE`) |
| Smoke endpoints | `integration/contracts/project-c.smoke.json` | stub |
| App release contract | `app-contract/release-contract.json` | ContinuityOps-owned |

## Explicit missing capabilities

Recorded in `integration/upstreams.lock.json` → `missing_capabilities`:

1. **MC-A-TREE / MC-C-TREE** — worker GitHub token cannot read private upstream
   tree contents (API contents 403). Pins are recorded; trees are not vendored.
2. **MC-C-DIGEST** — immutable image digest and rollback target are `UNAVAILABLE`
   until a verified `sha256:...` is packaged (CO-004).

## Claim level (S1 / P1-T01)

| Component | Claim | Allowed wording |
| --- | --- | --- |
| Lock + adapter JSON + static tests | **L1** | Static validated offline |
| Upstream live export verification | **not claimed** | Waiting on D-028 packaging |
| Cloud-applied landing zone from A | **not L4** | Not applied in this slice |

## Remaining boundaries

- No ContinuityOps mutation of A/C repositories.
- No production or multi-account claim.
- Digest promotion and rollback verification deferred (CO-004).
