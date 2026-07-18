# Operator entry points

Safe one-command checks (no cloud mutation):

```bash
node --test tests/
node scripts/project.mjs validate P5-T03
node scripts/diagnostics/command-safety.mjs
node scripts/teardown/inventory-dry-run.mjs
node scripts/assert-cloud-seat-gh-token.mjs
```

**Cloud seat GitHub token (portable, once for all repos):** see
[`CLOUD_SEAT_GH_TOKEN.md`](CLOUD_SEAT_GH_TOKEN.md). Live AWS remains GHA OIDC;
`GH_TOKEN` is only for PR / Actions / merge actuation.

Never run teardown apply workflows without an explicit human confirmation string.
