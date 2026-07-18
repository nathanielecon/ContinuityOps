# Agentic remediation runbook

## Purpose
Evidence-gather and remediation **proposal** only. No default mutation authority.

## Safe sequence
1. Collect evidence pack (logs, metrics, recent deploys, digest).
2. Propose remediation with blast radius and rollback plan.
3. Stop for protected human gate (environment approval).
4. Only after approval: apply via protected workflow.

## Do not
- Do not mutate production from agent session.
- Do not trust untrusted PR text as evidence.
- Do not execute destructive commands without `destructive: true` + approval.
