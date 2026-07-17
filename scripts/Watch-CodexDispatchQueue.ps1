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

  Hardening (BF-PRE-017):
    - CLAIM FIRST: relabel codex-dispatch -> dispatching before doing any work;
      on success -> dispatched; on warm/exec failure -> dispatch-failed plus a
      comment, and NEVER auto-retry (a human moves it back to codex-dispatch to
      requeue).
    - DOUBLE IDEMPOTENCY: a machine-local lock file mutex (with stale fallback)
      prevents overlapping scheduled runs, and each issue's labels are re-fetched
      after the claim so a lost race is skipped.
    - AUTHOR ALLOWLIST: only issues opened by -AllowedAuthors are executed;
      others are commented and skipped without running any block.
    - -Once: single pass then exit, for a Windows Scheduled Task (every 2-5 min).
      This is the durable carrier; an in-session background loop dies on app
      restart (BF-PRE-017).

  Queue issue body must contain fenced blocks the watcher parses:
    ```warm
    pwsh -File scripts/Invoke-CodexCloudWarm.ps1 -Repo 'nathanielecon/ContinuityOps'
    ```
    ```exec
    codex cloud exec --env <ENV_ID> --branch <branch> "<single-line task>"
    ```
  Label lifecycle: codex-dispatch -> dispatching -> dispatched -> done
  (failure: dispatch-failed; a human requeues by relabeling to codex-dispatch).
#>

param(
  [string]$Repo = 'nathanielecon/ContinuityOps',
  [int]$IntervalSeconds = 60,
  [string[]]$AllowedAuthors = @(),
  [switch]$Once,
  [int]$LockStaleMinutes = 30
)

$ErrorActionPreference = 'Stop'

# Default the author allowlist to the repository owner.
if (-not $AllowedAuthors -or $AllowedAuthors.Count -eq 0) {
  $AllowedAuthors = @($Repo.Split('/')[0])
}

$lockDir  = Join-Path $env:LOCALAPPDATA 'codex-cloud-warm'
$lockPath = Join-Path $lockDir 'queue.lock'

function Get-FencedBlock {
  param([string]$Body, [string]$Tag)
  $m = [regex]::Match($Body, "(?s)``````$Tag\s*\r?\n(.*?)``````")
  if ($m.Success) { return $m.Groups[1].Value.Trim() }
  return $null
}

function Acquire-Lock {
  if (-not (Test-Path $lockDir)) { New-Item -ItemType Directory -Path $lockDir -Force | Out-Null }
  if (Test-Path $lockPath) {
    $age = (Get-Date) - (Get-Item $lockPath).LastWriteTime
    if ($age.TotalMinutes -lt $LockStaleMinutes) {
      Write-Host "[queue] another run holds the lock (age $([int]$age.TotalMinutes)m); exiting"
      return $false
    }
    Write-Warning "[queue] stale lock ($([int]$age.TotalMinutes)m) — stealing"
  }
  Set-Content -Path $lockPath -Value "$PID $(Get-Date -Format o)" -Force
  return $true
}

function Release-Lock {
  if (Test-Path $lockPath) { Remove-Item $lockPath -Force -ErrorAction SilentlyContinue }
}

function Invoke-QueuePass {
  try {
    $issues = gh issue list --repo $Repo --label codex-dispatch --state open `
      --json number,title,body,author | ConvertFrom-Json
  } catch {
    Write-Warning "[queue] gh issue list failed: $_"; return
  }

  foreach ($issue in $issues) {
    $n = $issue.number
    Write-Host "[queue] #$n $($issue.title)"

    # --- Author allowlist: comment and skip, do not execute or relabel --------
    $author = $issue.author.login
    if ($AllowedAuthors -notcontains $author) {
      gh issue comment $n --repo $Repo --body "已跳过：作者 @$author 不在派遣白名单（$($AllowedAuthors -join ', ')）。不执行任何块。"
      continue
    }

    $warm = Get-FencedBlock -Body $issue.body -Tag 'warm'
    $exec = Get-FencedBlock -Body $issue.body -Tag 'exec'
    if (-not $warm -or -not $exec) {
      gh issue edit $n --repo $Repo --remove-label codex-dispatch --add-label dispatch-failed 2>$null
      gh issue comment $n --repo $Repo --body "已标记 dispatch-failed：未找到 ```warm``` / ```exec``` 执行块。请人工修正后改回 codex-dispatch 重新入队。"
      continue
    }

    # --- CLAIM FIRST: codex-dispatch -> dispatching ---------------------------
    try {
      gh issue edit $n --repo $Repo --remove-label codex-dispatch --add-label dispatching
    } catch {
      Write-Warning "[queue] #$n claim failed (likely taken): $_"; continue
    }

    # --- Double-check: re-fetch labels; skip if we do not hold the claim ------
    try {
      $labels = (gh issue view $n --repo $Repo --json labels | ConvertFrom-Json).labels.name
    } catch {
      Write-Warning "[queue] #$n re-fetch failed: $_"; continue
    }
    if (($labels -contains 'codex-dispatch') -or ($labels -notcontains 'dispatching')) {
      Write-Warning "[queue] #$n lost the claim race; skipping"; continue
    }

    # --- Warm gate (no -Force). Failure -> dispatch-failed, NO retry ----------
    try {
      Invoke-Expression $warm
    } catch {
      gh issue edit $n --repo $Repo --remove-label dispatching --add-label dispatch-failed 2>$null
      gh issue comment $n --repo $Repo --body "温门失败，已标记 dispatch-failed（不自动重试）：$_"
      continue
    }

    # --- Dispatch. Success -> dispatched; failure -> dispatch-failed ----------
    try {
      $out = Invoke-Expression $exec 2>&1 | Out-String
      Write-Host $out
      $taskId = ([regex]::Match($out, 'task[_ ]?id[:=]?\s*([A-Za-z0-9\-]+)')).Groups[1].Value
      if (-not $taskId) { $taskId = '(见下方输出)' }
      gh issue comment $n --repo $Repo --body "已派遣。任务 ID：$taskId`n`n``````$out``````"
      gh issue edit $n --repo $Repo --remove-label dispatching --add-label dispatched
    } catch {
      gh issue edit $n --repo $Repo --remove-label dispatching --add-label dispatch-failed 2>$null
      gh issue comment $n --repo $Repo --body "派遣失败，已标记 dispatch-failed（不自动重试）：$_"
    }
  }
}

# --- Entry point -------------------------------------------------------------
if (-not (Acquire-Lock)) { exit 0 }
try {
  Write-Host "[queue] watching $Repo label=codex-dispatch (control center only); authors=$($AllowedAuthors -join ',')"
  if ($Once) {
    Invoke-QueuePass
  } else {
    while ($true) { Invoke-QueuePass; Start-Sleep -Seconds $IntervalSeconds }
  }
}
finally {
  Release-Lock
}
