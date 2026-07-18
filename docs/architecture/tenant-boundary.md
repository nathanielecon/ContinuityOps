# Tenant boundary assumptions

ContinuityOps SaaS lifecycle assumes **logical tenant isolation** keyed by
`tenant_id` on events and storage rows.

## Explicit assumptions

- Tenants share compute where filters enforce isolation.
- Cross-tenant reads are prohibited by contract tests.
- Export and deprovision are tenant-scoped and audited.
- No customer production data is used in lab scenarios (D-009).

## Not claimed

- Physical VPC-per-tenant isolation
- Live multi-tenant AWS account partitioning
