# Chief-Coasts Framework Plan

**Status:** draft plan (owner-directed 2026-07-20)  
**Goal:** Automate software creation so the **chief coasts** — stream-boundary / pager / constitutional gates only — while **GPT/@codex workers** under junior + orchestrator execute specific contracts at volume.  
**North star:** Reusable control plane for ContinuityOps and future projects that ship **good applications for humanity** (reliability, recovery, honest claims, human gates on irreversible harm).

**Authority:** Amends practical reading of D-028 / D-034 / D-041 / D-047; does **not** weaken human gates H0–H6, production deploy, or secret expansion.

---

## 1. Target operating picture

```text
Owner (human)     → constitutional only (H0–H6, secrets, spend, irreversible)
Chief             → pager, stream boundary, strike≥2 escalate; writes ~0 LOC
Junior            → exception judgment + D-042 intents; tracks orch context
Orchestrator      → ready work, contracts, @codex dispatch, state ≤ review
GPT/@codex workers→ almost all implementation + judge JSON volume
Zero-hop GHA      → routine hops (publish→review→candidate→fresh→main)
Monitor (Grok)    → significant-only to chief
```

**Success metric (overnight):** chief commits **0** product/judge lines; GPT workers produce the volume; tip/data smoke green before fanout; Cursor Grok used only as bottleneck.

---

## 2. Lessons to embed (Emergency package C)

| Failure class | Root cause | Framework embed |
| --- | --- | --- |
| BF-2026-019/020 | App sandbox lacked candidate tip objects / fetch | Hard **tip-visibility smoke** before ×N `@codex` |
| Cursor wrote ~27k judge lines | Strike-2 → chief Grok unblock | Cursor = bottleneck only; GPT→GPT replacement first |
| BF-2026-018 | `GITHUB_TOKEN` publish-ok no retrigger | Zero-hop hardening |
| Claim L4↔L1 rewrite | `writeEvidence` fixture downgrade | Preserve elevated tip-bound claims (landed) |
| “More Mandarin” ≠ fix | Missing **data** in sandbox | D-028 packet + env fetch (read), not write tokens |

Repo scale context: ContinuityOps ~**67k** text lines on `main` (mostly evidence JSON); tipbound delta ~**28k** was almost all `evidence/judges/**`.

---

## 3. Exact permissions — GPT / Codex workers (future project)

### 3.1 Principle

**Workers get data, not authority.**  
Sandbox is **receive-only**. Publish via D-034 GHA (`GITHUB_TOKEN` ephemeral). Never put long-lived PATs or cloud keys in the Codex environment.

### 3.2 Codex Cloud Environment (worker runtime)

| Setting | Required value | Why |
| --- | --- | --- |
| Repository | Target app repo (public preferred for fetch simplicity) | Source of truth |
| Secrets | **none** (ContinuityOps doctrine; future apps same unless owner H-gate) | Prevent CO-005-class credential move |
| Cache | on | Warm + speed |
| Network egress | Allow **read** HTTPS to `github.com` (git fetch/clone) | Prevents CONNECT 403 on tip fetch |
| Branch materialization | Checkout / sync **`base_branch` from the dispatch** (e.g. `candidate/…` or `main`) with history deep enough for `tip` + `tip^` | Prevents tip-object miss |
| Write to remote | **Denied** (no `git push`, no `gh`) | D-034 path |

**Do not grant workers:**

- Fine-grained or classic PAT in env secrets  
- `contents: write` / `pull_requests: write` as a worker-held credential  
- AWS/Azure/GCP long-lived keys  
- Admin / `administration: write`  
- Ability to merge to `main` or change branch protection  

### 3.3 GitHub App — Codex (installation on the repo)

Grant the Codex GitHub App (or equivalent) **only what the product needs to read code and post task results**, typically:

| Permission | Access | Notes |
| --- | --- | --- |
| Contents | **Read** | Clone/fetch code + history |
| Issues | **Read & write** | Receive `@codex` tasks; post replies (product-dependent) |
| Metadata | **Read** | Required |
| Pull requests | **Read** (Write only if product requires App-created draft refs — ContinuityOps prefers **no**; use D-034 GHA) | Prefer read-only + patch-in-comment |

**Explicitly avoid for workers:** Actions secrets access, Environments, Administration, Members, Workflows write from the App sandbox identity.

### 3.4 GitHub Actions (publisher / zero-hop) — not the worker

These are **GHA** identities, not Codex sandbox permissions:

| Actor | Permissions |
| --- | --- |
| `codex-patch-publish` | `contents: write`, `pull-requests: write`, `issues: write` (ephemeral `GITHUB_TOKEN`) |
| `pipeline-zero-hop` | As today: issues/PRs/actions as required for mechanical hops |
| `continuityops-terraform` / cloud apply | OIDC → short-lived cloud role only; never worker keys |

### 3.5 Cursor chief / junior cloud seat (control plane)

| Secret | Required | Notes |
| --- | --- | --- |
| `GH_TOKEN` | Owner fine-grained PAT: `github_pat_…` with Contents + PRs + Issues + Actions + Workflows **R/W** | Gate: `node scripts/assert-cloud-seat-gh-token.mjs` → **PASS** |
| AWS keys in Cursor | **No** | Live AWS = GHA OIDC only |

### 3.6 One-page “grant this” checklist (copy for a new repo)

```text
Codex Cloud Environment
- [ ] Repo attached; cache ON; secrets: NONE
- [ ] Egress: github.com HTTPS read (git) allowed
- [ ] Setup fetches dispatch base_branch + enough history for tip^ 
- [ ] No git push / gh in sandbox (document in agent contract)

Codex GitHub App on repo
- [ ] Contents: Read
- [ ] Issues: Read & write
- [ ] Metadata: Read
- [ ] Pull requests: Read (prefer; avoid Write if using D-034 GHA publish)

GitHub Actions (publisher workflows)
- [ ] Patch-publish workflow with GITHUB_TOKEN write for contents+PRs+issues
- [ ] Zero-hop / actuate workflows as needed
- [ ] Cloud apply via OIDC roles only (no keys in Codex env)

Human / chief seat
- [ ] GH_TOKEN PAT (not gho_/ghs_) with Contents/PRs/Issues/Actions/Workflows R/W
- [ ] Sticky chief-pager issue
- [ ] Keep-warm record issue
```

---

## 4. ContinuityOps framework changes (embed here first)

### P0 — Tip-visibility gate (blocks GPT volume loss)

1. Add `docs/planning/dispatch/TIP_VISIBILITY_SMOKE.zh.md`  
   - Single `@codex` must `git fetch` `base_branch`, `cat-file -t tip`, `rev-parse tip^ == candidate_sha`  
   - Optional: accept D-028 tip-proof if fetch blocked **and** packet present at HEAD  
2. Amend `QUEUE.md` / zero-hop: **no ×N judge/worker fanout** until smoke issue labeled `tip-smoke-ok`  
3. Orch contract: Cursor Grok volume judging **forbidden** until smoke fail + one GPT fixer cohort + strike≥2  

### P1 — Codex env materialization

1. Document ContinuityOps env `6a594ee667608191ab53cae15202815e`: fetch `candidate/*` + deepen  
2. Rehearse smoke on a throwaway tip  
3. Record CONNECT 403 as **platform** page to chief (not worker context-rot)

### P2 — D-028 packet standard

1. Promote `evidence/dispatch-packets/` shape to a schema + generator script  
2. Every tipbound / candidate-only tip ships packet on the **same commit** workers will check out  

### P3 — Zero-hop / publish hardening

1. Fix BF-2026-018 (`publish-ok` → D-037 without relying on forbidden GITHUB_TOKEN retrigger)  
2. Candidate merge path stays mechanical; main only after fresh pass + CI  

### P4 — Role contracts (chief coasts)

1. `CHIEF_SUPERVISOR.md`: success = 0 LOC overnight except constitutional unblock  
2. `JUNIOR_SUPERVISOR.zh.md`: replace orch on low `context_remaining`; never silent Cursor volume  
3. Orch: reject handoffs without `context_remaining`; GPT→GPT on context rot  

### P5 — Portable “Dispatch Kit” (future projects)

Extract (copyable tree, not full ContinuityOps evidence):

```text
dispatch-kit/
  CODEX_DISPATCH_SNIPPET.zh.md
  TIP_VISIBILITY_SMOKE.zh.md
  PAGER_SNIPPET.zh.md
  JUNIOR_ACTUATE_SNIPPET.zh.md
  WORKER_PERMISSIONS.md          # §3 of this plan
  D028_PACKET_SCHEMA.json
  scripts/assert-tip-visibility.sh
  workflows/codex-patch-publish.yml.example
  workflows/pipeline-zero-hop.yml.example
  AGENTS_FRAGMENT.md             # chief-coasts topology
```

Use this kit to stand up a **new human-beneficial app** with the same control plane without carrying 67k evidence lines.

---

## 5. Phased delivery (ContinuityOps then kit)

| Phase | Outcome | Exit check |
| --- | --- | --- |
| **A — Gate** | Tip smoke + QUEUE amend | One GPT smoke green on candidate tip before any ×3 |
| **B — Env** | Codex env fetches candidate history | Smoke green without Cursor |
| **C — Packet** | Generator + schema | Blind App worker U1 pass using packet-only fallback once |
| **D — Zero-hop** | BF-018 class closed | publish-ok → D-037 without human FF |
| **E — Coast drill** | Overnight tipbound-scale or feature batch | Chief 0 LOC; GPT volume; pager quiet |
| **F — Kit** | `dispatch-kit/` published | Second repo bootstrapped from kit alone |

No calendar estimates — sequence and exit checks only.

---

## 6. Humanity / product constraint (keep explicit)

Automation accelerates **build quality and honesty**, not silent production harm:

- Human gates remain for production deploy, credentials, destructive data, external customer comms, residual critical/high security  
- Claim ceilings stay explicit (e.g. Azure live out until evidenced)  
- “Good applications for humanity” = reliable, recoverable, evidence-bound systems — not unattended blast radius  

---

## 7. Immediate owner actions (outside agents)

1. Keep **ChatGPT/Codex subscription** active before overnight GPT volume  
2. Apply §3.6 permissions on ContinuityOps + any new app repo  
3. Confirm Codex env egress to `github.com` and `base_branch` materialization  
4. Refresh Cursor seat `GH_TOKEN` as `github_pat_` until `assert-cloud-seat-gh-token.mjs` → **PASS**  
5. Approve Phase A implementation PR when ready  

---

## 8. Decision register seed

| ID | Decision | Status |
| --- | --- | --- |
| D-CC-001 | Tip-visibility smoke is mandatory before GPT fanout | proposed |
| D-CC-002 | Workers remain receive-only; flexibility = read/fetch + D-028 data | proposed |
| D-CC-003 | Cursor Grok is bottleneck-only for volume work | proposed |
| D-CC-004 | Portable dispatch-kit is the vehicle for future apps | proposed |

---

## 9. References

- Emergency package C / tipbound close: PR #178, `evidence/portfolio/tipbound-s0-s8-aa01454.json`  
- BF-2026-018 / 019 / 020 / 023 / 026  
- `CODEX_DISPATCH_SNIPPET.zh.md`, `QUEUE.md`, `CHIEF_SUPERVISOR.md`, `JUNIOR_SUPERVISOR.zh.md`  
- Live AWS: GHA OIDC → `continuityops-gha` (not CursorCloudAgent)
