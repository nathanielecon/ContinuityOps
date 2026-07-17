<#
.SYNOPSIS
  Control-center publish for a Codex Cloud task that cannot push from the App sandbox (D-033).

.DESCRIPTION
  Runs ONLY on the owner's machine (codex CLI + gh + git). Applies the cloud task
  diff locally, pushes a branch, and opens a GitHub PR. Never stores secrets.
  The PR body is finalized with the GitHub-visible PR URL plus context_remaining
  so D-033 publish completion can be verified from the PR itself.
  App sandboxes lack gh and often get CONNECT 403 to github.com — do not expect
  workers to self-publish.

.PARAMETER TaskId
  Codex Cloud task id (from "View task" URL or `codex cloud list --json`).

.PARAMETER BaseBranch
  PR base branch (stream or orchestrator branch — not main unless intended).

.PARAMETER HeadBranch
  Local/remote branch name to push.

.PARAMETER Title
  PR title.

.PARAMETER ContextRemaining
  Context remaining reported by the Codex task, or 'n/a' when unavailable.

.EXAMPLE
  pwsh -File scripts/Publish-CodexCloudTask.ps1 `
    -TaskId 'task_e_...' -BaseBranch 'claude/orchestrator-supervisor-setup-yyd3bu' `
    -HeadBranch 'codex/orch-smoke-01' -Title 'ORCH-SMOKE-01 cold-start smoke evidence'
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$TaskId,

    [Parameter(Mandatory)]
    [string]$BaseBranch,

    [Parameter(Mandatory)]
    [string]$HeadBranch,

    [Parameter(Mandatory)]
    [string]$Title,

    [string]$ContextRemaining = 'n/a',

    [string]$Repo = 'nathanielecon/ContinuityOps'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not (Get-Command codex -ErrorAction SilentlyContinue)) {
    throw 'codex CLI required (control center only).'
}
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw 'gh CLI required.'
}

Write-Host "[publish] applying $TaskId"
codex cloud apply $TaskId
git checkout -B $HeadBranch
git add -A
if (git diff --cached --quiet) {
    throw "No staged changes after apply for $TaskId"
}
git commit -m "$Title"
git push -u origin $HeadBranch
$body = @"
Published from Codex Cloud task via control-center apply (D-033).

Task: $TaskId
"@
$prUrl = gh pr create --repo $Repo --base $BaseBranch --head $HeadBranch --title $Title --body $body
$finalBody = @"
$body

GitHub PR URL: $prUrl
context_remaining: $ContextRemaining
"@
gh pr edit $prUrl --repo $Repo --body $finalBody
Write-Host "[publish] PR URL: $prUrl"
Write-Host '[publish] done'
