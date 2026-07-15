# ContinuityOps

## Cloud Reliability and Recovery Platform

**ContinuityOps** is the professional name for the former “Project F.” It is a
production-style cloud operations capstone built around an already-completed
application and cloud foundation.

The project does not rewrite Projects A or C:

- **Project A** is an upstream infrastructure and governance reference. It
  contributes approved network, IAM, audit, Terraform, and cloud-control
  contracts where those outputs genuinely exist.
- **Project C** is the upstream application and delivery reference. It
  contributes a versioned container artifact, release identity, hosted PR
  validation, and later an immutable promotion/rollback contract where those
  outputs genuinely exist.
- **ContinuityOps** owns runtime operations: Kubernetes, serverless event
  processing, observability, SaaS operations, networking diagnosis, incident
  response, recovery, security operations, agent-assisted GitHub workflows,
  performance, and cost control.

This package is an implementation and certification plan, not a claim that the
described cloud system has already been deployed.

## Recruiter-facing repository contract

The implemented repository opens with a polished 16:9 ContinuityOps infographic
derived from the editable draw.io architecture source. The architecture panel
dominates; evidence-backed outcome cards support it. The first screen must make
the project understandable to a recruiter in under 60 seconds and link directly
to verification, incident, recovery, performance, and cost evidence.

The infographic footer must state that ContinuityOps is an isolated synthetic-
data lab and does not claim sustained customer-production SRE ownership.

## Start here

1. Read `MASTER_PLAN.md` for product scope, architecture, phases, and exit
   criteria.
2. Read `RALPHY_ORCHESTRATION.md` before running any agentic implementation or
   judge loop.
3. Load `PLAN.md` as the authoritative task manifest and authorize only Phase 0.
4. Install the repository contracts from `AGENTS.md` and
   `EVIDENCE_AND_CLAIMS.md`.
5. Freeze the applicable slice rubric from `JUDGE_RUBRICS.md` before a worker
   changes that slice.
6. Use `PROMPT_PACK.md` for orchestrator, worker, judge, nixer, fixer, and final
   clean-rejudge prompts.
7. Append every failure and remediation to `BREAK_FIX_LOG.md`.

## Package contents

| File | Purpose |
| --- | --- |
| `MASTER_PLAN.md` | Complete end-to-end build and certification plan |
| `PLAN.md` | Machine-readable task authority and state-transition rules |
| `RALPHY_ORCHESTRATION.md` | Concurrent disjoint Ralphy streams, bottleneck agents, saved/fresh councils, approvals, and post-build certification |
| `JUDGE_RUBRICS.md` | Frozen must-haves and 10-point scoring contracts for every slice |
| `PROMPT_PACK.md` | Short, context-safe prompts for every orchestration role |
| `MANDARIN_PROMPT_PACK.md` | Executable Simplified-Chinese prompts for every agent role |
| `AGENTS.md` | Repository authority, write-scope, handoff, safety, and escalation rules |
| `EVIDENCE_AND_CLAIMS.md` | Append-only evidence schema, freshness rules, claim levels, and portfolio wording |
| `OPERATING_STATE.md` | Initial status, decision register, issue schema, and human-gate ledger |
| `BREAK_FIX_LOG.md` | Seeded prevention rules and append-only break/fix template |
| `SOURCE_ANALYSIS.md` | Design decisions derived from Projects A and C |
| `MODEL_AND_STREAM_TOPOLOGY.md` | Opus/Grok/Codex cloud routing, Mandarin protocol, proxy, concurrent streams, and bottleneck roles |
| `RECRUITER_FRONT_PAGE_SPEC.md` | Resume-ready root README and Image2 infographic contract |
| `REPO_README_TEMPLATE.md` | Evidence-gated recruiter-ready root README scaffold |
| `IMAGE2_INFOGRAPHIC_PROMPT.md` | Evidence-constrained prompt for the polished front-page PNG |
| `../architecture/continuityops.drawio` | Editable source-of-truth architecture diagram (repo path) |
| `../architecture/continuityops-architecture.svg` | Exact recruiter-readable vector render |
| `../architecture/continuityops-architecture.png` | Exact Image2 reference render |

## Non-negotiable completion definition

ContinuityOps is complete only when:

- every task follows `planned -> ready -> running -> blocked|review -> verified
  -> done`;
- every completed code partition passes deterministic validation;
- every construction and post-build partition passes the saved-remediation
  council experiment and then a fresh independent three-judge round with all must-haves,
  average score at least **9.5/10**, no judge below **9.0**, and three explicit
  `merge_ready: yes` verdicts;
- hosted checks pass on the exact candidate commit;
- cloud and recovery claims are supported by live, commit-bound evidence;
- critical/high security issues are closed or explicitly block release;
- the break/fix log contains every failed attempt and verified repair;
- concurrent Ralphy streams remain disjoint and sequential internally;
- all worker communication is Simplified Chinese and recruiter artifacts are English;
- the root README and architecture visual pass recruiter/evidence review;
- a final clean-room council rejudges the integrated repository without access
  to implementation transcripts or earlier scores.

## Claims boundary

Creating these planning files proves only that a detailed execution plan exists.
It does **not** prove Kubernetes, serverless, SaaS, incident-response, recovery,
Azure, AWS, GitHub-hosted, or production behavior. Those claims become eligible
only through the evidence levels defined in `EVIDENCE_AND_CLAIMS.md`.
