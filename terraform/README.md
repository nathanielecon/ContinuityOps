# ContinuityOps Terraform

Live AWS control plane (2026-07-18): **GitHub OIDC → `continuityops-gha`** via
`.github/workflows/continuityops-terraform.yml`. Cloud Agents stay repo-only
(`NoCredentials` expected). Do not use `CursorCloudAgent` or
`project-a-lzlab-gha` for these roots.

## Loop

1. Edit `terraform/**` on a PR → CI **plan**
2. Merge to `main` → CI **apply** (Environment `continuityops`)
3. Workflow runs `terraform/ci-bootstrap/ensure-tfstate.sh` then S3 backend init

## Environments

| Env | Purpose | Mutation |
| --- | --- | --- |
| `staging` | non-destructive integration | auto-apply on push to `main` |
| `recovery-lab` | destructive drills | `workflow_dispatch` apply |

## Backend

- Bucket: `continuityops-tfstate-000000000000`
- Lock table: `continuityops-tf-locks`
- Ensured idempotently by `ci-bootstrap/ensure-tfstate.sh` under OIDC

## Claim level

Stay at **L1** until `cloud_apply_evidence` is recorded for a green apply
(caller identity `assumed-role/continuityops-gha/...` + resource proof).
