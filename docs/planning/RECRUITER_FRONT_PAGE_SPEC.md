# Recruiter-Ready Root README and Front-Page Visual

## Recruiter outcome

A cloud/platform recruiter should understand the project in under 60 seconds:

1. what was built;
2. how code moves safely to an isolated cloud lab;
3. how Kubernetes and serverless are operated;
4. how failures are observed, diagnosed, and recovered;
5. what security, performance, cost, and agentic controls were proven;
6. what was not proven.

## Root README order

```markdown
# ContinuityOps — Cloud Reliability and Recovery Platform

![ContinuityOps architecture and evidence story](docs/portfolio/continuityops-infographic.png)

> One-sentence evidence-backed outcome and honest lab boundary.

[CI] [Security] [Evidence] [Demo status] badges

## Results at a glance
Four to six evidence-backed metrics only.

## Architecture
Short explanation + link to editable draw.io and exact render.

## What I engineered
Cloud foundation, Kubernetes, serverless/SaaS, observability, incidents,
security/agentic, recovery/performance/FinOps.

## Failure and recovery proof
Three strongest incidents with symptom, root cause, recovery, metric/evidence.

## Five-minute recruiter demo
Safe, deterministic path that does not require cloud credentials.

## Evidence map
Direct links to hosted runs, evidence manifests, incident timelines, restore,
load/cost and judge certification.

## Technology
Compact grouped table including TypeScript 7 only if actually present.

## Architecture decisions and tradeoffs
Five concise decisions with rationale.

## Claim boundary
Explicit synthetic-lab versus production-experience statement.
```

## Infographic content

Landscape 16:9, preferably 2048×1152 or 2560×1440.

### Top 65% — primary architecture

Large readable governed flow:

`Developer/PR -> credential-free CI -> protected main/environment -> GitHub
OIDC -> Terraform cloud foundation -> immutable artifact -> managed Kubernetes`

The Kubernetes service publishes an event to `Queue -> Serverless worker ->
DLQ/replay`. Both runtime paths feed `Metrics + Logs + Traces -> SLO alerts ->
Incident/runbook -> Recovery verification`.

A separate agentic lane reads evidence and proposes remediation; any mutation
returns through a protected human approval gate.

### Bottom 35% — six evidence story cards

1. Governed delivery
2. Kubernetes operations
3. Serverless + SaaS
4. Observability + incidents
5. Security + agentic safety
6. Recovery + performance + cost

Each card uses one short sentence and only final evidence-backed metrics.

### Required footer

> Isolated synthetic-data cloud lab with evidence-backed runtime and recovery
> drills; not a claim of sustained customer-production SRE ownership.

## Style

- modern professional cloud/platform engineering poster;
- deep navy, teal, white, restrained amber for human approval/failure;
- architecture dominates, story cards support;
- crisp corporate typography and high contrast;
- no cartoon aesthetic, mascots, purple AI glow, code rain, or decorative
  infrastructure that is not in evidence;
- readable at GitHub README width.

## Asset pipeline

1. Maintain `architecture/continuityops.drawio` as source of truth.
2. Render exact SVG and PNG references.
3. Validate architecture/evidence parity.
4. Give the exact PNG and `IMAGE2_INFOGRAPHIC_PROMPT.md` to Image2.
5. Review generated PNG against source and evidence.
6. Regenerate if Image2 adds, removes, or changes meaning.
7. Commit the approved PNG at
   `docs/portfolio/continuityops-infographic.png`.
8. Root README references the PNG with descriptive alt text.

## Resume-ready copy gates

- Use first-person engineering ownership only for work actually performed.
- Use measured numbers only with direct evidence IDs.
- Prefer verbs such as implemented, deployed, tested, diagnosed, recovered,
  measured, and enforced.
- Avoid enterprise-scale, production-grade, zero-downtime, autonomous, secure,
  or highly available without exact proof and boundary.
- Keep the opening summary to two lines and the core README under roughly 1,500
  words, with detail linked rather than dumped.

## Validation checklist

- [ ] draw.io/XML opens and edits correctly
- [ ] exact SVG/PNG is current for draw.io hash
- [ ] Image2 visual matches source topology
- [ ] every visible service exists in final architecture/evidence
- [ ] every visible metric maps to evidence
- [ ] failure/rollback arrows are directionally correct
- [ ] protected human gate is visible
- [ ] agentic lane does not imply uncontrolled mutation
- [ ] footer is readable
- [ ] README image link and alt text work
- [ ] recruiter can find evidence and demo in under 60 seconds
- [ ] independent visual/evidence reviewer passes
