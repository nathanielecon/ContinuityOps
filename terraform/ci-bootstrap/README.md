# ContinuityOps CI bootstrap (GitHub OIDC)

One-time root in account `283077380808`. Creates IAM role `continuityops-gha`
trusted by GitHub Actions via the existing OIDC provider
(`token.actions.githubusercontent.com`).

**Control plane:** Cloud Agents edit this repo; live AWS is
**GHA OIDC → `continuityops-gha`**, not CursorCloudAgent (BF-PRE-002 / BF-2026-010).

Trust uses immutable subject claims (post–2026-07-15 renames):

`repo:nathanielecon@177059064/*@1301990908:...`

Do **not** trust `aws-landing-zone-lab` id `1296742987`.

## Apply once (AWS CloudShell / break-glass)

```bash
# Discover ContinuityOps repository_id, then CloudShell one-liner:
gh api repos/nathanielecon/ContinuityOps -q .id   # expect 1301990908
REPO_ID=1301990908 curl -fsSL https://paste.rs/gHlj9 | bash

# or from checkout:
REPO_ID=1301990908 bash terraform/ci-bootstrap/bootstrap-oidc-cloudshell.sh

# or Terraform (same REPO_ID defaults in main.tf):
cd terraform/ci-bootstrap
terraform init -backend=false -input=false
terraform apply -input=false -auto-approve
terraform output gha_role_arn
```

Then create GitHub Environment `continuityops` (no reviewers / wait timer).

Ongoing loop (no dispatch): PR → plan → merge `main` → **apply on push**.
`workflow_dispatch` is fallback only.

## Do not

- Chase `CURSOR_AWS_ASSUME_IAM_ROLE_ARN` / CursorCloudAgent for ContinuityOps apply
- Reuse `project-a-lzlab-gha` or `landing-zone-lab.yml` for ContinuityOps roots
- Put long-lived access keys in Cloud secrets
- Bootstrap with the monorepo repository id
