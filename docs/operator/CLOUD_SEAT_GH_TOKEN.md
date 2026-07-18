# Cloud seat GitHub token contract (portable)

**Purpose:** One owner bootstrap so Cursor Cloud Agents can run the full
GitOps loop — open PR → confirm Actions → merge → confirm apply — **without**
AWS keys, Cursor STS, or per-change human dispatch.

**Control-plane split (do not conflate):**

| Plane | Who has it | Secret? |
| --- | --- | --- |
| Live AWS | GitHub Actions OIDC → repo CI role (e.g. `continuityops-gha`) | No AWS keys in Cloud |
| GitHub actuation | Cloud seat `GH_TOKEN` (fine-grained PAT) | Yes — GitHub only |
| Cursor STS / `CursorCloudAgent` | Not used on Pro+ | Do not chase |

`NoCredentials` for `aws sts` in the Cloud seat is **expected**. Missing
**GitHub** power (Actions / PR merge 403) is the gap this contract closes.

## One-time owner setup (reuse across repos)

### 1. Fine-grained PAT (preferred)

GitHub → Settings → Developer settings → Personal access tokens → Fine-grained.

| Field | Value |
| --- | --- |
| Token name | `cursor-cloud-seat-gha-loop` (or similar) |
| Resource owner | `nathanielecon` |
| Repository access | **All repositories** (so new projects inherit) **or** add each new private repo |
| Expiration | Your policy (rotate before expiry) |

**Repository permissions** (minimum):

| Permission | Access | Why |
| --- | --- | --- |
| Contents | Read and write | `git push` / branch updates |
| Pull requests | Read and write | `gh pr merge` / merge API |
| Actions | Read and write | List/view runs, confirm plan/apply, `gh workflow run` fallback |
| Commit statuses | Read | Know when checks are green |
| Workflows | Read and write | Push/update `.github/workflows/*` |
| Issues | Read and write | Queue / `@codex` / comments |
| Environments | Read | Optional; inspect deploy environments |

Classic PAT alternative: scopes `repo` + `workflow` (broader; fine-grained preferred).

### 2. Inject into Cursor Cloud Agents

Cursor Dashboard → Cloud Agents → Secrets / Environment variables:

| Name | Type | Value | Apply to |
| --- | --- | --- | --- |
| `GH_TOKEN` | Environment variable (exact name) | the fine-grained PAT | **All repositories** |

Then **start a new Cloud Agent** (or re-inject and restart) so the token is picked up.
App install tokens (`ghs_`) are often down-scoped; do not rely on them for Issues/Actions.

### 3. Per-repo AWS OIDC (separate, once each)

Still required once per AWS lab repo (not this PAT):

1. CloudShell / local aws: create CI role trusted to that repo’s `repository_id`
2. GitHub Environment for apply (no required reviewers if you want unattended apply)
3. Workflow: PR plan + **push to `main` apply**

See ContinuityOps `terraform/ci-bootstrap/` and `.github/workflows/continuityops-terraform.yml`.

## New repo checklist (copy)

When creating `nathanielecon/<new-repo>`:

- [ ] PAT already has **All repositories** → no PAT change
- [ ] Else: edit PAT → add repository → save (no Cursor change if secret already `GH_TOKEN`)
- [ ] Cursor secret `GH_TOKEN` already “All repositories” → no Cursor change
- [ ] Copy OIDC bootstrap + terraform workflow pattern; CloudShell once for that repo id
- [ ] Create GitHub Environment (no reviewers if auto-apply desired)
- [ ] In the new Cloud Agent: `node scripts/assert-cloud-seat-gh-token.mjs` (or copy script) must exit 0

## Assert (any seat)

```bash
# ContinuityOps:
node scripts/assert-cloud-seat-gh-token.mjs
# or target another repo:
node scripts/assert-cloud-seat-gh-token.mjs nathanielecon/other-repo
```

Exit 0 = Contents, Pull requests, Actions, Commit statuses, Workflows, Issues
(and Environments if present) are readable/writable enough for the loop.
Exit 1 = owner must expand PAT / re-inject `GH_TOKEN` and restart the agent.

## What you do **not** need

- Teams / Bedrock External ID / `CursorCloudAgent`
- Long-lived AWS keys in Cloud secrets
- Reusing another project’s CI role (e.g. `project-a-lzlab-gha`) for ContinuityOps
- In-pod `aws sts` success

## After token is live, agents autonomously

1. Open Terraform (or code) PRs  
2. Confirm **plan** green on Actions  
3. Merge to `main`  
4. Confirm **apply** green (OIDC role)  
5. Record evidence  

Until then: agents may edit/push; humans confirm Actions / merge if Merge API 403.
