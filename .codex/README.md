# ContinuityOps — Codex Cloud Environment

This directory holds the **only** two scripts pasted into the ContinuityOps
Codex Cloud Environment. They are versioned and change-controlled in the repo
(decision **D-026**). Editing them ad hoc, adding a secret to the Environment,
or bypassing the warm gate are all out of bounds.

> Note: these scripts follow the described dailydigits warm-start pattern. The
> reference repository was not readable when they were authored; they are
> **pending owner cross-check against the dailydigits reference**.

## Environment configuration (Codex UI)

- **One Environment for this repo**, created in the Codex UI under the owner's
  ChatGPT login.
- **Caching: On.**
- **Setup script:** `bash .codex/cloud-setup.sh`
- **Maintenance script:** `bash .codex/cloud-maintenance.sh`
- **Zero secrets / zero environment variables.** Codex Cloud is authenticated
  through the platform (owner ChatGPT account); the container needs no
  credentials. Adding any variable or secret invalidates the ~12h warm cache
  and violates D-026/D-027.

## What the scripts do

- `cloud-setup.sh` (cold, at Environment build): verifies the toolchain this
  planning/governance repo relies on (`git`, `python3`, `jq`; Node 22 is
  preinstalled, mermaid rendering optional), installs dependencies **only if** a
  manifest later appears (`package.json` / `requirements.txt` / `go.mod`), then
  runs the warm smoke step.
- `cloud-maintenance.sh` (warm refresh + warm-gate smoke): validates every
  standalone `*.json` and every fenced ```json block in Markdown. This is the
  repo's closest thing to a test suite; it exits non-zero on any parse failure.

## Bootstrap order (four steps)

1. **Land the scripts** on a branch and get them merged to the default branch
   (merge is human-owned, D-012).
2. **Owner creates the Environment** in the Codex UI (cache On, the two scripts
   above, zero secrets) — this is the one unavoidable human step,
   gate `H-codex-env-create` (resolves the CO-007 creation step).
3. **Control center registers** the Environment `ENV_ID` in the machine-local
   `environments.json` registry (never committed) and runs the `-Force` first
   warm.
4. **Control center warm-gates and dispatches** work with
   `codex cloud exec --env <ENV_ID> --branch <branch> "<task>"`. Tasks never run
   git; the orchestrator owns integration.

## Dispatch topology (recap)

The owner's Windows control-center session is the sole dispatch point (D-027).
Cloud containers and workers are **receive-only**: no warm gate, no
`codex cloud exec`, no credentials. Cross-repo material reaches a worker as
**data, not permission** (D-028) — via context packaging or a read-only vendored
snapshot, never a widened repository grant.
