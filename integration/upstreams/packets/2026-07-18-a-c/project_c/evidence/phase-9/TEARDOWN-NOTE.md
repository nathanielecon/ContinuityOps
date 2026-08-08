# Teardown note — `service_base_url` in this packet is no longer reachable

The vendored Project C phase-9 evidence in this directory records:

```
service_base_url = http://project-c-stg-117678206.us-east-1.elb.amazonaws.com
smoke            = PASS
```

That ALB and its Fargate service were **torn down on 2026-08-08** during the
ContinuityOps cost investigation (BF-2026-029…032). They measured ~$25/month in
Cost Explorer — ALB $0.540/day, Fargate task $0.296/day — and had been running
since 2026-07-14.

**Following that URL now returns nothing.** The DNS name is released with the load
balancer, and a rebuilt ALB gets a different hash.

## The evidence is unaffected

Per `README.md`, hosted evidence here is *tip-inherited from recorded runs, not
re-applied on every tip*. This packet is a **dated record of a run that happened**,
not an assertion that the endpoint is live now. Nothing in
`docs/claims/matrix.json` depended on the URL resolving.

Before teardown, a final live capture was taken and committed **to Project C's own
repository**, where the claim belongs:

- `evidence/phase-9/20260808T191039Z-manifest.json`
- `evidence/phase-9/20260808T191039Z-smoke-final-preteardown.txt`
- `evidence/phase-9/20260808T191039Z-openapi.json`
- `evidence/phase-9/20260808T191039Z-aws-state.txt`

in `nathanielecon/local-first-governed-cicd`.

The strongest item in that capture: `GET /version` returned `git_sha`
`376b7e18c5cc94e67ff180ca2f42b8eb05535be3` — byte-identical to the `commit_sha`
pinned in `app-contract/release-contract.json`. The running service was provably the
claimed commit, which is a stronger statement than "the URL responded".

## Which hostname was live

Two hostnames appear across the phase-9 manifests. The live one was
`project-c-stg-117678206`; `project-c-stg-1738567119` was superseded. The ALB's
creation time (2026-07-14T01:18:54Z) falls between the two records, so the first was
destroyed and replaced before the governing manifest was written.

## Reproducing

The container image is pinned by digest and the ECR repository was outside the
teardown scope, so the stack is rebuildable from Project C's
`infra/terraform`. Only the hostname changes.
