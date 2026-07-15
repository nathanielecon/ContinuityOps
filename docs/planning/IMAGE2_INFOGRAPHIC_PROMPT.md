# Image2 Prompt — ContinuityOps GitHub Front Page

Use the exact architecture PNG in `architecture/continuityops-architecture.png`
as Image 1. Preserve its topology and labels; polish the presentation without
inventing services, stages, metrics, or claims.

```text
Use case: infographic-diagram
Asset type: GitHub repository front-page portfolio infographic for a Cloud / Platform Engineer resume
Primary request: Transform Image 1, the exact ContinuityOps architecture diagram, into one polished landscape 16:9 recruiting infographic. Preserve every architectural relationship and the honest control boundaries. Architecture must remain the dominant, fully readable top panel; evidence story cards support it below.
Input images: Image 1 is the authoritative draw.io architecture render; preserve its topology, stage order, human-approval gate, failure/recovery loop, evidence paths, and lab boundary.
Style/medium: modern professional enterprise technology poster; deep navy, teal, white, restrained amber; crisp corporate typography; high contrast; subtle depth; clean vector-like shapes; not cartoonish.
Composition/framing: 2048x1152 landscape. Top 65 percent is a large architecture flow. Bottom 35 percent contains six equal evidence-story cards. Keep generous spacing and readable arrows.
Text (verbatim):
Title: "ContinuityOps"
Subtitle: "Cloud Reliability and Recovery Platform"
Top architecture labels: "Developer / PR", "Credential-Free CI", "Protected Main + Human Gate", "GitHub OIDC", "Terraform Cloud Foundation", "Immutable Artifact", "Managed Kubernetes", "Queue", "Serverless Worker", "DLQ + Replay", "Metrics + Logs + Traces", "SLO Alerts", "Incident + Runbook", "Recovery Verification", "Agent-Assisted Evidence + Remediation Proposal"
Bottom card titles: "Governed Delivery", "Kubernetes Operations", "Serverless + SaaS", "Observability + Incidents", "Security + Agentic Safety", "Recovery + Performance + Cost"
Footer: "Isolated synthetic-data cloud lab with evidence-backed runtime and recovery drills; not a claim of sustained customer-production SRE ownership."
Constraints: Do not add vendor services, production regions, account IDs, customer data, metrics, badges, uptime percentages, or claims not present in Image 1 or supplied final evidence. The agent-assisted lane may propose remediation but must visibly route mutation through protected human approval. Keep all text verbatim and readable at GitHub README width. No logos unless present in the reference.
Avoid: purple AI glow, robots, mascots, code rain, tiny text, decorative clouds, fake dashboards, false production claims, autonomous production mutation, watermarks.
```

Before final use, replace no placeholder with a metric unless it maps to a
current evidence ID. Run the visual parity checklist in
`RECRUITER_FRONT_PAGE_SPEC.md` after generation.
