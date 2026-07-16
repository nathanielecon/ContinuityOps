# Codex Cloud speed — ContinuityOps

Each repository needs its **own** Codex Environment and ~12h cache.

## Facts

- Warm tools on one Environment do not speed up another repo.
- Laptop `codex` ChatGPT login ≠ credentials inside Codex Cloud containers.
- Do **not** reinstall Node/pwsh/Terraform/AWS CLI/Ralphy every task when present.
- Orchestrator warm gate: before any Codex Cloud task, run
  `pwsh -File scripts/Invoke-CodexCloudWarm.ps1 -Repo 'nathanielecon/ContinuityOps'`.
- Register with `scripts/Register-CodexCloudEnvironment.ps1`. Registry:
  `%LOCALAPPDATA%\codex-cloud-warm\environments.json` (never commit).

## Human setup (once)

1. Ensure `.codex/cloud-setup.sh` and `.codex/cloud-maintenance.sh` are on `main`.
2. Codex → Environments → `nathanielecon/ContinuityOps` → caching **On**:
   - Setup: `bash .codex/cloud-setup.sh`
   - Maintenance: `bash .codex/cloud-maintenance.sh`
3. No env vars / secrets. Save → copy ENV_ID → register locally.
4. Warm once (Paste block C below).

## Paste block A — Project prompt addendum

```text
## Codex Cloud speed (required)

This project uses a Codex Cloud Environment with cached setup (~12h).

Rules for Codex Cloud tasks:
1. Do NOT reinstall Node, PowerShell, Terraform, AWS CLI, or Ralphy at session start
   unless `command -v` shows they are missing.
2. Prefer tools already on PATH from Environment setup/maintenance
   (`.codex/cloud-setup.sh` / `.codex/cloud-maintenance.sh`).
3. In-progress tasks keep the container they started with; Environment changes
   apply only to NEW tasks.
4. If tools are missing: run `bash .codex/cloud-setup.sh` once, then continue.
5. Cache is PER REPOSITORY Environment.
6. Nested `codex doctor` / Image2 / laptop ChatGPT auth are NOT available here.
7. Edit the repo only. Live cloud apply is GitOps/CI, not this agent.

Orchestrator (before launching this task): run
`pwsh -File scripts/Invoke-CodexCloudWarm.ps1 -Repo nathanielecon/ContinuityOps`.
```

## Paste block C — Warm-task prompt

```text
Smoke only: print versions for git, node, pwsh, terraform, aws. Make no repo changes.
If a tool is missing, run bash .codex/cloud-setup.sh once, then reprint versions.
```
