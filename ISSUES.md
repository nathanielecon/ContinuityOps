# Issues

Machine-readable ContinuityOps issue ledger (S1 refresh).

```json
{
  "schema_version": "1.0",
  "revision": 2,
  "open_issues": [
    {
      "id": "CO-002",
      "status": "partial",
      "summary": "Pins and adapter contracts present; upstream tree verification still blocked by CO-006.",
      "owner": "P1-T01/control-center"
    },
    {
      "id": "CO-003",
      "status": "open",
      "summary": "Cloud account, OIDC roles, regions, state ownership, cost cap, protected environments unset.",
      "owner": "optional tooling (D-044 clears H1 receipt wait)"
    },
    {
      "id": "CO-004",
      "status": "open",
      "summary": "Project C image_digest remains UNAVAILABLE.",
      "owner": "P1-T01 / D-028 packaging"
    },
    {
      "id": "CO-006",
      "status": "open",
      "summary": "Worker token metadata-only; A/C trees not packaged yet.",
      "owner": "control-center"
    }
  ],
  "resolved_in_s1": [
    "CO-002 pins recorded with consumed_contracts and missing_capabilities"
  ]
}
```
