# NIX-TIPBOUND-001 — tip/parent visibility packet (D-028)

## Required before U1

```bash
git fetch origin candidate/portfolio-aa01454
git cat-file -t 0606812354dae2e23356278f10f9b76b7ebd010b   # expect: commit
git rev-parse 0606812354dae2e23356278f10f9b76b7ebd010b^  # expect: aa01454f8808c173deb43cc4b9b803287eec851e
```

Machine proof: `evidence/portfolio/tip-proof-aa01454.json`  
Commit object dump: `COMMIT_OBJECTS.txt`

Clean-room: do not open prior judge score files under `evidence/judges/**`.
