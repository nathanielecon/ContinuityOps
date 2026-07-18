# ContinuityOps Terraform scaffold (S1)

This directory is a **static scaffold**. Terraform CLI is not required to parse
HCL in CI yet; Node static tests assert required files and invariants.

## Environments

| Env | Purpose | Mutation |
| --- | --- | --- |
| `staging` | non-destructive integration | OIDC staging roles (placeholders) |
| `recovery-lab` | destructive drills | protected environment + human/OIDC gate |

## Backend

See `modules/state`. State is designed to be isolated, versioned, encrypted,
and locked. Placeholder names must be replaced before any apply.

## Claim level

**L1** static only unless `evidence/slices/S1/terraform.json` records a higher
honest level with command evidence.
