# NIX-TIPBOUND-001 tip/parent proof packet

This read-only packet binds review tip
`0606812354dae2e23356278f10f9b76b7ebd010b` to its expected parent and S2
candidate `aa01454f8808c173deb43cc4b9b803287eec851e`.

The canonical proof is [`../../tip-proof-aa01454.json`](../../tip-proof-aa01454.json).
The D-028 dispatch copy is
[`../../../dispatch-packets/tipbound-aa01454/packet.json`](../../../dispatch-packets/tipbound-aa01454/packet.json).

Verify the relationship in a clone that contains the review tip:

```bash
git cat-file -t 0606812354dae2e23356278f10f9b76b7ebd010b
test "$(git rev-parse 0606812354dae2e23356278f10f9b76b7ebd010b^)" = \
  "aa01454f8808c173deb43cc4b9b803287eec851e"
```

This packet supplies commit identities and verification instructions only. It
does not grant repository, GitHub, cloud, or merge authority, and it does not
raise the A3 claim ceiling.
