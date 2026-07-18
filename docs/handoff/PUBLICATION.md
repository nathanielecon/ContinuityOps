# Option A — Public repository publication checklist

Owner-executed checklist to publish `nathanielecon/ContinuityOps` as a
**public** portfolio repository. Workers must **not** run visibility changes;
the lead orchestrator (or human owner) executes the `gh` / UI steps below.

## 1. Set visibility to public

### Primary (GitHub CLI)

```bash
gh repo edit nathanielecon/ContinuityOps --visibility public
```

Confirm when prompted. Re-check:

```bash
gh repo view nathanielecon/ContinuityOps --json isPrivate,visibility,url
```

Expect `isPrivate: false` and `visibility: "PUBLIC"`.

### Fallback (GitHub UI)

1. Open https://github.com/nathanielecon/ContinuityOps/settings
2. Scroll to **Danger Zone** → **Change repository visibility**
3. Choose **Make public** and confirm the repository name
4. Verify the repo badge shows **Public** on the main page

Do **not** change default branch protections, environments, or secrets as part of
this Option A step unless a separate human gate authorizes it.

## 2. Proposed GitHub description

Replace the current description (still wording “Phase 0 bootstrap”) with a
claim-safe line aligned to engagement **A3** and the root README ceiling:

**Proposed description (≤350 chars):**

```text
Scoped AWS lab L4 portfolio: evidence-gated OIDC apply, lab drill/RTO, and teardown under A3 ceilings — not production, not Azure live.
```

Optional longer variant if the UI allows more room:

```text
ContinuityOps — scoped AWS lab L4 (apply + lab drill/RTO + teardown) via protected GitHub OIDC. Evidence-gated claims under engagement A3; Azure live out; performance L1.
```

Apply with CLI (owner only) or About → Description in the UI:

```bash
gh repo edit nathanielecon/ContinuityOps \
  --description "Scoped AWS lab L4 portfolio: evidence-gated OIDC apply, lab drill/RTO, and teardown under A3 ceilings — not production, not Azure live."
```

## 3. Homepage

Leave **homepage** empty (`""`). No marketing URL is required for Option A.

```bash
# optional explicit clear — only if a stale homepage was set
gh repo edit nathanielecon/ContinuityOps --homepage ""
```

## 4. Forbidden overclaims

When writing About text, READMEs linked from social posts, or recruiter copy,
**do not** claim any of the following:

| Forbidden overclaim | Correct A3 / evidence stance |
| --- | --- |
| Production ownership or production customer drills | Lab drills only; no production (customer) incident ownership |
| Azure live apply / live Azure control plane | Azure governance L1 design/static; live Azure **out** (D-046) |
| Known-good ContinuityOps rollback digest | Rollback digest **not** proven for ContinuityOps |
| In-pod AWS / CursorCloudAgent credentials | OIDC control plane only; no in-pod AWS credentials |
| Performance beyond L1 | Performance remains **L1** (no live load proof) |

Also avoid implying every component is L4: under A3, ceilings differ
(security-sbom **L2**, agentic-workflow **L3**, upstream-integration **L2**,
performance **L1**, Azure live **out**). Source of truth:
[`docs/claims/matrix.json`](../claims/matrix.json).

## 5. Post-publish verification (anonymous)

After visibility is public, verify from a logged-out browser or `curl` without
auth that these paths open with HTTP 200:

| Check | URL |
| --- | --- |
| README | https://github.com/nathanielecon/ContinuityOps |
| Claims matrix | https://github.com/nathanielecon/ContinuityOps/blob/main/docs/claims/matrix.json |
| Hosted evidence index dir | https://github.com/nathanielecon/ContinuityOps/tree/main/evidence/hosted |
| Example hosted elevation | https://github.com/nathanielecon/ContinuityOps/blob/main/evidence/hosted/cloud-apply-staging-elevation-2026-07-18.json |
| Example lab drill/RTO | https://github.com/nathanielecon/ContinuityOps/blob/main/evidence/hosted/lab-drill-rto-29645042815.json |

Quick unauthenticated probe (expect non-404 HTML for the repo home):

```bash
curl -sI "https://github.com/nathanielecon/ContinuityOps" | head -n 1
curl -sI "https://raw.githubusercontent.com/nathanielecon/ContinuityOps/main/docs/claims/matrix.json" | head -n 1
curl -sI "https://raw.githubusercontent.com/nathanielecon/ContinuityOps/main/evidence/hosted/cloud-apply-staging-elevation-2026-07-18.json" | head -n 1
```

If any path 404s after publish, stop and fix default-branch content or path typos
before announcing the repo publicly.

## Execution note

- **This checklist only.** Visibility change and description edit are owner /
  lead-orchestrator actions.
- Workers on this task must **not** run `gh repo edit … --visibility public`.
