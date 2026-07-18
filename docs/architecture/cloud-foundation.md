# Cloud foundation (Terraform scaffold)

## Scope (P1-T02)

Scaffold Terraform for:

- remote state (S3 + DynamoDB lock placeholders);
- environment separation (`staging`, `recovery-lab`);
- IAM / GitHub OIDC role composition;
- network composition suitable for a single-account lab.

## Layout

```text
terraform/
  modules/state/          # backend bucket, encryption, versioning, lock table
  modules/environments/   # env naming, tags, cost drivers
  modules/iam/            # OIDC provider + least-privilege roles
  modules/network/        # VPC/subnet boundary scaffold
  envs/staging/
  envs/recovery-lab/
  policies/               # static policy stubs (tagging, encryption)
  versions.tf
  README.md
```

## Claim honesty

| Check | Status in this environment |
| --- | --- |
| `terraform fmt` / `terraform validate` | **Not run** — Terraform CLI not installed |
| Static structure + Node tests | **L1** |
| Hosted plan via OIDC | **Not proven** (stubs only; not L3 plan) |
| Cloud apply | **Not L4** — no apply evidence |

## Cost drivers and teardown

Explicit cost drivers: NAT gateways, EKS (later phases), CloudWatch retention,
state bucket versioning. Teardown is a protected workflow stub
(`.github/workflows/teardown.yml`) — destructive execution remains gated.

## Remaining boundaries

- Placeholder account IDs / ARNs / bucket names.
- No live AWS resources created in S1.
- Recovery-lab mutations require protected environment + approval when OIDC is wired.
