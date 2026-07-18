# Operator entry points

Safe one-command checks (no cloud mutation):

```bash
node --test tests/
node scripts/project.mjs validate P5-T03
node scripts/diagnostics/command-safety.mjs
node scripts/teardown/inventory-dry-run.mjs
```

**A3 lab status:** lab destroyed after drill; re-apply only via hosted workflows /
`continuityops-gha` (staging lab — not production).

Never run teardown apply workflows without an explicit human confirmation string.
