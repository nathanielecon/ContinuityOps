# Serverless DLQ incident playbook (synthetic)

1. Confirm DLQ depth alarm from synthetic fixture or future lab metric.
2. Inspect poison message schema against `serverless/event-contract.json`.
3. Replay only with approval (`Dlq.replay({ approved: true })`).
4. Verify idempotency store prevents duplicate side effects.

Claim: L1 unit/synthetic. No live Lambda/SQS runtime claimed.
