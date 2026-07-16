#!/usr/bin/env bash
#
# ContinuityOps — Codex Cloud Environment SETUP script.
#
# CHANGE CONTROL (D-026): this file and cloud-maintenance.sh are the ONLY
# content pasted into the Codex Cloud Environment. Editing them ad hoc is out
# of bounds; every change goes through review and re-warm. Never add secrets or
# environment variables to the Environment — doing so invalidates the ~12h
# warm cache and is a double violation of D-026/D-027.
#
# Purpose: prepare a warm, dependency-verified container for this repo. Runs at
# Environment build time (cold). Keep it idempotent and credential-free.
#
# Note for the owner: written to the described dailydigits warm-start pattern;
# pending owner cross-check against the dailydigits reference.

set -euo pipefail

need_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "SETUP FAIL: required command not found: $1" >&2
    exit 1
  fi
}

echo "[setup] ContinuityOps Codex Cloud Environment — cold setup"

# --- 1. Verify the toolchain this planning/governance repo relies on ---------
# Node 22 is preinstalled by the base image; mermaid rendering is optional and
# is not required for the contract checks.
need_cmd git
need_cmd python3
need_cmd jq

echo "[setup] git:     $(git --version)"
echo "[setup] python3: $(python3 --version 2>&1)"
echo "[setup] jq:      $(jq --version)"
if command -v node >/dev/null 2>&1; then
  echo "[setup] node:    $(node --version)  (optional, mermaid render only)"
fi

# --- 2. Install dependencies ONLY if a manifest later appears ----------------
# This repo currently has no package.json / requirements.txt / go.mod. The
# install steps are intentionally no-ops until a manifest exists.
if [ -f package.json ]; then
  echo "[setup] package.json found — installing npm deps"
  need_cmd npm
  npm ci
fi
if [ -f requirements.txt ]; then
  echo "[setup] requirements.txt found — installing pip deps"
  python3 -m pip install -r requirements.txt
fi
if [ -f go.mod ]; then
  echo "[setup] go.mod found — downloading modules"
  need_cmd go
  go mod download
fi

# --- 3. Warm/smoke step: validate the JSON contracts -------------------------
# The closest thing this repo has to a test suite: every standalone *.json and
# every fenced ```json block in Markdown must parse.
echo "[setup] validating JSON contracts (warm smoke)"
bash "$(dirname "$0")/cloud-maintenance.sh"

echo "[setup] done — Environment is warm"
