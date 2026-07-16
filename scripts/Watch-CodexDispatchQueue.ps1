<#
.SYNOPSIS
  ContinuityOps — Codex dispatch queue watcher (control center ONLY).

.DESCRIPTION
  Polls the GitHub `codex-dispatch` queue and executes each request on the
  control-center machine, where codex CLI, the ChatGPT keychain login, and the
  machine-local warm registry (%LOCALAPPDATA%\codex-cloud-warm\environments.json)
  are co-located. Per D-027/D-029: the cloud emits intent only, the local lane
  executes, credentials never move.

  DO NOT RUN THIS IN A CLOUD CONTAINER. Cloud containers are receive-only and
  must never run the warm gate, `codex cloud exec`, or `codex login`.

  Each queue issue body must contain fenced blocks the watcher parses:
    ```warm
    pwsh -File scripts/Invoke-CodexCloudWarm.ps1 -Repo 'nathanielecon/ContinuityOps'
    ```
    ```exec
    codex cloud exec --env <ENV_ID> --branch <branch> "<single-line task>"
    ```
  Label lifecycle: codex-dispatch -> dispatched (after exec) -> done (after
  apply/push/close, set by whoever integrates).
#>

param(
  [string]$Repo = 'nathanielecon/ContinuityOps',
  [int]$IntervalSeconds = 60
)

$ErrorActionPreference = 'Stop'

function Get-FencedBlock {
  param([string]$Body, [string]$Tag)
  $m = [regex]::Match($Body, "(?s)``````$Tag\s*\r?\n(.*?)``````")
  if ($m.Success) { return $m.Groups[1].Value.Trim() }
  return $null
}

Write-Host "[queue] watching $Repo label=codex-dispatch (control center only)"

while ($true) {
  try {
    $issues = gh issue list --repo $Repo --label codex-dispatch --state open `
      --json number,title,body | ConvertFrom-Json
  } catch {
    Write-Warning "[queue] gh issue list failed: $_"; Start-Sleep -Seconds $IntervalSeconds; continue
  }

  foreach ($issue in $issues) {
    $n = $issue.number
    Write-Host "[queue] #$n $($issue.title)"
    $warm = Get-FencedBlock -Body $issue.body -Tag 'warm'
    $exec = Get-FencedBlock -Body $issue.body -Tag 'exec'
    if (-not $warm -or -not $exec) {
      gh issue comment $n --repo $Repo --body "自动跳过：未在正文找到 ```warm``` / ```exec``` 执行块。"
      continue
    }

    # 1) Warm gate (no -Force). Skip the issue on warm failure.
    try {
      Invoke-Expression $warm
    } catch {
      gh issue comment $n --repo $Repo --body "温门失败，已跳过本轮：$_"
      continue
    }

    # 2) Dispatch. Capture the task ID from codex output.
    try {
      $out = Invoke-Expression $exec 2>&1 | Out-String
      Write-Host $out
      $taskId = ([regex]::Match($out, 'task[_ ]?id[:=]?\s*([A-Za-z0-9\-]+)')).Groups[1].Value
      if (-not $taskId) { $taskId = '(见下方输出)' }
      gh issue comment $n --repo $Repo --body "已派遣。任务 ID：$taskId`n`n``````$out``````"
      gh issue edit $n --repo $Repo --remove-label codex-dispatch --add-label dispatched
    } catch {
      gh issue comment $n --repo $Repo --body "派遣失败：$_"
    }
  }

  Start-Sleep -Seconds $IntervalSeconds
}
