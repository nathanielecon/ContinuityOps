# Codex Cloud Environment (keep-warm) — ContinuityOps

Codex Cloud agents use the Codex universal image plus the dashboard **setup
script**; Codex caches that container state ~12 hours. Warmth is **per
Environment/repo** — another project's warm cache does not help this one.

## Wire once (owner, Codex web UI)

1. Codex → Environments → `nathanielecon/ContinuityOps` → caching **On**.
2. Setup script: `bash .codex/cloud-setup.sh`
3. Maintenance script: `bash .codex/cloud-maintenance.sh`
4. Pin Node 24 in the UI if offered (or closest; setup upgrades). Save.
5. **No** environment variables. **No** secrets.
6. Register the Environment id on the orchestrator machine (local only, never
   committed):

```powershell
pwsh -File scripts/Register-CodexCloudEnvironment.ps1 `
  -Repo 'nathanielecon/ContinuityOps' `
  -EnvId '<ENV_ID>'
```

## Warm gate (orchestrator, forever)

Before **any** Codex Cloud task for this repo:

```powershell
pwsh -File scripts/Invoke-CodexCloudWarm.ps1 -Repo 'nathanielecon/ContinuityOps'
```

If `lastWarmUtc` is missing/older than ~10 h it submits a smoke task via
`codex cloud exec` and stamps `%LOCALAPPDATA%\codex-cloud-warm\environments.json`.

## What gets installed

| Tool | Version |
| --- | --- |
| Node.js | 24.x |
| PowerShell | 7.x |
| Terraform | 1.15.5 |
| AWS CLI | v2 |
| Ralphy CLI | 4.7.2 |
| git / jq / Docker (when apt provides it) | distro |

Notes: laptop `codex` ChatGPT login ≠ credentials inside cloud containers —
this system warms the **toolchain cache** only. Don't reinstall tools per task;
don't edit the setup script casually (cache invalidation). Live cloud apply is
GitOps/CI, not the Cloud agent.
