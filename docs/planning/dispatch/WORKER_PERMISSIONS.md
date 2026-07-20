# GPT / Codex Worker Permissions (exact)

Canonical narrative: [`CHIEF_COASTS_FRAMEWORK_PLAN.md`](./CHIEF_COASTS_FRAMEWORK_PLAN.md) §3.  
Tip gate: [`TIP_VISIBILITY_SMOKE.zh.md`](./TIP_VISIBILITY_SMOKE.zh.md).

**Principle:** workers get **data**, not **authority**. Sandbox is receive-only; GHA publishes.

---

## 1. Codex Cloud Environment (worker runtime)

| Setting | Exact requirement |
| --- | --- |
| Secrets | **None** — do not store PAT, `GH_TOKEN`, or cloud keys |
| Network | Allow HTTPS **read** to `github.com` (git fetch / clone) |
| Git remote write | **Denied** — no `git push`, no `gh` in sandbox |
| Checkout | Materialize dispatch `base_branch` with history for `tip` and `tip^` |
| Cache | On (warm path) |

---

## 2. Codex GitHub App — install on the target repo

Grant **only** these App permissions:

| Permission | Access | Exact purpose |
| --- | --- | --- |
| **Contents** | **Read** | Clone / fetch code and commit history |
| **Issues** | **Read and write** | Receive `@codex` task comments; post replies / patches |
| **Metadata** | **Read** | Required by GitHub for App installs |
| **Pull requests** | **Read** | Prefer read-only; ContinuityOps opens PRs via D-034 GHA |

**Do not grant the App (for the worker path):**

- Contents **Write**
- Pull requests **Write** (unless product cannot use GHA publish)
- Actions / Workflows / Environments / Secrets access
- Administration, Members, Organization admin
- Any cloud provider credentials

---

## 3. Do not put in the worker environment

- Fine-grained or classic PAT  
- `GH_TOKEN` / `GITHUB_TOKEN` as a durable secret  
- Contents or PR **write** credentials held by the sandbox  
- AWS / Azure / GCP long-lived keys  
- Merge-to-`main` or branch-protection authority  

---

## 4. Grant to GHA publishers (not the sandbox)

| Actor | Exact permissions |
| --- | --- |
| `codex-patch-publish` | Ephemeral `GITHUB_TOKEN`: `contents: write`, `pull-requests: write`, `issues: write` |
| Zero-hop / junior-actuate | As required for mechanical hops only |
| Cloud apply | OIDC → short-lived role (e.g. `continuityops-gha`); never worker keys |

---

## 5. Chief / Cursor seat (control plane — not a worker)

Fine-grained PAT (`github_pat_…`, not `gho_` / `ghs_`) on the repo:

| Permission | Access |
| --- | --- |
| Contents | Read and write |
| Pull requests | Read and write |
| Issues | Read and write |
| Actions | Read and write |
| Workflows | Read and write |
| Metadata | Read |

Assert: `node scripts/assert-cloud-seat-gh-token.mjs` → **PASS**.

---

## 6. Copy-paste grant checklist (new repo / future project)

```text
Codex Environment
- [ ] secrets: NONE
- [ ] egress: github.com HTTPS git read
- [ ] materialize dispatch base_branch + tip^ history
- [ ] no git push / gh in sandbox

Codex GitHub App
- [ ] Contents: Read
- [ ] Issues: Read and write
- [ ] Metadata: Read
- [ ] Pull requests: Read (prefer)

GHA (publisher)
- [ ] patch-publish with GITHUB_TOKEN write (contents + PRs + issues)
- [ ] cloud via OIDC only

Chief seat
- [ ] github_pat_ with Contents/PRs/Issues/Actions/Workflows R/W
```

## Flexibility that prevents tip-miss (not more write power)

1. Env materializes dispatch `base_branch` + history for `tip` and `tip^`  
2. Tip-visibility smoke green before ×N `@codex`  
3. D-028 tip-proof packet on that same commit  
