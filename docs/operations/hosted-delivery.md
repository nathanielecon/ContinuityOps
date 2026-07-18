# Hosted delivery (GitHub Actions + OIDC)

## Purpose (P1-T03)

Provide **workflow stubs** for PR validation, plan, apply, drift, evidence
upload, and teardown. Existing D-034 / D-042 workflows are left intact.

## Workflow inventory (new files only)

| Workflow | Trigger intent | Credentials |
| --- | --- | --- |
| `terraform-pr.yml` | PR — fmt/validate/static | none (read-only) |
| `terraform-plan.yml` | plan on protected ref | OIDC placeholder |
| `terraform-apply.yml` | apply to staging / recovery-lab | OIDC + environment protection |
| `drift.yml` | scheduled drift detect | OIDC placeholder (read) |
| `evidence-upload.yml` | attach evidence artifacts | contents read + artifact write |
| `teardown.yml` | lab teardown | OIDC + protected environment + confirmation input |

## Pinning

Third-party actions use commit SHA pins (not floating `latest`).

## Untrusted PR posture

PR jobs request `contents: read` only and never configure AWS credentials.
Mutation jobs require `id-token: write` and GitHub Environment protection.

## Claim honesty

| Claim | Level |
| --- | --- |
| Workflow YAML + static permission/pin tests | **L1** |
| Hosted run of `validate.yml` contracts (existing) | eligible for **L3** when CI is green on the candidate SHA |
| OIDC plan/apply/drift/teardown | **not proven** — stubs; not L3 cloud plan / not L4 apply |

## Remaining boundaries

- AWS account / role ARNs are placeholders (CO-003).
- Protected environments must be created in GitHub Settings before mutation jobs succeed.
- Safe blocked-change demo is represented by the PR read-only job refusing credentials (see `scripts/ci/assert-pr-readonly.mjs`).
