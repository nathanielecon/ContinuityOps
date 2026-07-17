# H0 Human Approval Package — S0 Rubric Freeze

**Status:** `waiting_human`  
**Packaged at:** 2026-07-17T21:55:00Z  
**Main tip at package:** see `git rev-parse origin/main` after hash refresh  
**Agents cannot mint this receipt.**  
**Hash refresh:** `plan_sha256` refreshed after PLAN.md P0-T04 `review` state bump so the validator matches the tree you sign.

## What to approve

Human gate **H0**: project scope, architecture, cost cap, upstream pins, and the frozen S0 rubric / execution bundles produced by P0-T04.

## Bound artifacts

| Artifact | Path | Notes |
| --- | --- | --- |
| Frozen rubric | `harness/rubrics/S0.freeze.v1.json` | status `frozen_pending_H0` |
| H0 binding shell | `harness/approvals/H0.binding.json` | `receipt: null` until you sign |
| Rubric freeze evidence | `evidence/slices/S0/rubric-freeze.json` | includes bundle hashes |
| Rubric review notes | `docs/reviews/rubric-review.md` | English reviewer notes |
| Validator | `harness/rubrics/validate-rubric-freeze.mjs` | exit 0 on main tip |

## Bundle hashes (from `evidence/slices/S0/rubric-freeze.json`)

```text
plan_sha256:                72e21d7e58e351d2bd4b22cfcd73d5a0fc5d6c1ce29f73843375674ad31e2026
execution_contract_sha256:  5a3eff5d41baf5afac2a8c82d9b0312df1e65d86bce142ba07ed088f3cc184bf
validator_bundle_sha256:    b8c1b48235315d183e34978f79544294d958cc0b95dd520f9005002be9d3c6bc
rubric_sha256:              724232f475e99749b5fc58098dc6e1eb8956748602332938ef1a106bc0ec8205
partition_bundle_sha256:    52c4aefe62b7355e5abea13f4ee79967b5a28363b8f1866cde6b399c1fcbeab3
```

Re-verify before signing: `node harness/rubrics/validate-rubric-freeze.mjs` (must exit 0).

`partition_bundle_note`: main currently lacks `harness/partition-manifest.json`; P0-T04 used `integration/upstreams.lock.json` as the available partition/upstream pin input inside write_scope.

## Suggested receipt fields

Use the schema in root `OPERATING_STATE.md` (Human receipt schema) / `H0.binding.json` `required_receipt_fields`:

- `gate_id`: `H0`
- `decision`: `approve` | `reject` | `defer`
- `approver`: your identity
- `approved_at`: ISO-8601
- `baseline_sha` / `candidate_sha`: bind to the exact SHAs you reviewed
- `approved_bundle_sha256` / `approved_rubric_sha256`: must match the hashes above (or re-run validator and use fresh digests)
- `signature_or_signed_comment_url`: durable proof (signed comment / external receipt store outside worker write scope)

After you sign, a supervisor/orchestrator round may fill `harness/approvals/H0.binding.json` `receipt` + `receipt_sha256` from that **human** artifact only.

## Merge / verification evidence for this package

- P0-T03 verified: main includes validators; D-037 issue #38 `verdict: pass`
- P0-T04 integrated: PR #40 content on main `9a58cbd`; CI `contracts` success; D-037 issue #41 `verdict: pass`
- Explicit non-claim: **no Phase 1 authorization** until S0 certification (P0-T05) **and** this H0 receipt

## Owner parallel items (unchanged)

- `REPO_SETTINGS_ADMIN_TOKEN`
- PR #20
