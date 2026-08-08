# Frozen STRUCT Checklist — Build `81e700c3f40bb7b5`

## Scope and decision standard

This checklist governs the structural certification instrument formed by `validate.py`, `battery.py`, `permute.py`, `repackage.py`, `finalize.py`, and `build.sh`. It is frozen against build `81e700c3f40bb7b5`.

A later STRUCT judge may award at least 9.5/10 only after every applicable rule below is decided true or false against the unchanged build. A structural hole that admits a mathematical error, a stem/key mismatch, or rejection of a correct answer is a full-severity mathematics finding rather than a minor structural deduction.

The derivation results recorded below are not a completed mutation score. A rule described as "asserted but not mutation-proved" remains mandatory, but this derivation did not establish its falsifiability by injecting the named defect and observing the intended gate failure.

## Established build and census results

- The SHA-256 prefix of `zips/sha256sums.txt` was confirmed as `81e700c3f40bb7b5`.
- Two consecutive executions of `./build.sh` produced byte-identical `sha256sums.txt`; `cmp` returned clean. Byte reproducibility is therefore established for this build.
- An independent census followed the QTI resource selected by each package manifest rather than trusting a shared total. It found 14 packages, 199 unique package/item pairs, 199 globally unique item identifiers, 125 `numerical_question` items, and 74 `short_answer_question` items.
- That independent result reconciles the package count, global identifier count, response-type partition, validator total, and battery total. The two-censuses-reconciled check passed.

## Frozen atomic rules

### Trial integrity and falsifiability

**S-01 — Isolated trial.** Every injected trial must operate on a fresh private copy of the complete candidate package set, never on the accepted artifacts or on a directory shared with another trial. This exposes false passes or failures caused by cross-trial residue.

**S-02 — Safe trial pathname.** Every rule must behave identically when the trial path contains spaces, brackets, glob metacharacters, and directory names such as `metadata` or `manifests`. This exposes tools that interpret a pathname as a glob or reject files because of an ancestor-directory substring.

**S-03 — Positive control.** Before interpreting a mutation sweep, the harness must run a known-valid candidate and observe success with all 14 packages and 199 items discovered. This exposes a harness that finds no packages or no items and consequently reports every mutation as caught.

**S-04 — Parsed-tree landing assertion.** After an XML mutation, the harness must parse the mutated resource and prove that the intended element, attribute, or text value changed at the intended item. This exposes namespace errors, text-only edits, and mutations that land outside the structure read by the gate.

**S-05 — Defect-preserving control.** The injected candidate must remain XML- and ZIP-readable unless malformed syntax is the defect under test. This prevents a broad parse failure from being mistaken for detection of the narrower invariant.

**S-06 — Passing and failing witnesses.** Each rule requires one conforming witness that passes and one otherwise-conforming witness containing only the target defect that fails. This exposes rules that cannot fail or diagnostics triggered by an unrelated defect.

**S-07 — Diagnostic correspondence.** The failing witness must produce a diagnostic naming the violated property and affected package or item. This exposes a rule whose message claims a stronger or different invariant than the condition that actually failed.

**S-08 — Candidate-space sweep.** Where a property can occur at multiple packages, resources, items, response conditions, or attributes, the mutation must be swept across every applicable site or a justified exhaustive equivalence partition. This exposes the recurring defect in which a rule works at one site but not the others.

### Corpus discovery, census, and partition

**S-09 — Complete package discovery.** The pipeline must discover exactly the 14 manifest-rooted packages and must fail, rather than silently continue, if any expected package is absent or any unexpected package is included. This exposes a glob or directory filter that turns missing input into apparent success.

**S-10 — Manifest-selected item census.** A census must follow the unique `imsqti_xmlv1p2` resource selected by each manifest and count the items in that resource. This exposes a tag census over an XML file that Canvas will not import.

**S-11 — Global item identity.** The 199 item identifiers must be globally unique, not merely unique within each package. This exposes cross-package identifier collisions hidden by per-package validation.

**S-12 — Package/item-pair identity.** The corpus must contain exactly 199 unique package/item pairs, and the pair set must equal the set processed by the validator and battery. This exposes duplicate processing, skipped resources, or two tools reading different corpora while reporting the same total.

**S-13 — Exact response-type partition.** The 199 items must partition into exactly 125 numerical and 74 short-answer items, with no overlap and no residual type. This exposes a coverage assertion that checks only `125 + 74 = 199` without proving disjointness and exhaustion.

**S-14 — Independent expected total.** `EXPECT_ITEMS` must be an independently fixed expectation and must be compared with a census computed from discovered item elements; the same computed value may not both set and check the expectation. This exposes a total that trusts itself.

**S-15 — Reconciled independent censuses.** At least one census independent of `validate.py` and `battery.py` must compare exact package/item identities and response types, not merely reconcile the number 199. This exposes two instruments that go blind together.

### Manifest binding and containment

**S-16 — Unique quiz resource.** Each manifest must contain exactly one resource whose type is exactly `imsqti_xmlv1p2`. This exposes packages that import no quiz or leave Canvas an ambiguous choice.

**S-17 — Unique quiz href.** The selected quiz resource must identify exactly one distinct QTI XML path after combining its resource `href` and child `<file href>` values. This exposes a resource that points at multiple possible assessments.

**S-18 — Validated-file binding.** The exact QTI resource selected by the manifest must be the resource whose items were validated and battery-tested. This exposes validation of a decoy XML file while Canvas imports a different file.

**S-19 — Declared-to-packaged direction.** Every manifest `href` must resolve to a regular packaged file contained below the package root. This exposes missing resources and path traversal through declared names.

**S-20 — Packaged-to-declared direction.** Every packaged file other than the root `imsmanifest.xml` must be declared by the manifest. This exposes undeclared files that exist in the ZIP but are not published by Canvas.

**S-21 — Canonical containment.** Manifest hrefs, ZIP members, staging paths, and output paths must remain within their intended roots after normalization, including rejection of absolute paths and `..` traversal. This exposes checks that compare strings but not resolved containment.

**S-22 — Root manifest identity.** Each archive must contain exactly one `imsmanifest.xml`, at the archive root and with the bytes that were parsed during packaging. This exposes a valid nested manifest or a second manifest shadowing the checked one.

**S-23 — Resource identifier uniqueness.** Manifest resource identifiers must be nonempty and unique, and each dependency must resolve to exactly one resource. This exposes ambiguous or dangling dependency graphs.

### XML metadata and attribute reading

**S-24 — Item metadata cardinality.** Each item must contain exactly one effective `question_type` field and exactly one effective assessment-question identifier field at the required structural location. This exposes duplicate metadata where a substring search happens to see the desired value.

**S-25 — Attribute equality, not substring presence.** Rules concerning `ident`, `respident`, `rcardinality`, `action`, `varname`, resource `type`, or `href` must parse and compare the complete attribute value. This exposes magic-string or substring checks that accept the value in the wrong attribute or as part of a longer value.

**S-26 — Direct-child granularity.** Where QTI requires an element to be a direct child, the rule must inspect direct children rather than arbitrary descendants. This exposes structurally misplaced metadata that remains visible to `.iter()`.

**S-27 — Namespace-safe parsing.** Element discovery must work with the QTI default namespace and must prove a nonzero expected count before accepting a trial. This exposes `root.iter("item")`-style empty traversals that silently pass everything.

**S-28 — Parsed content used.** If a file is parsed to establish a structural property, the parsed nodes and relationships must actually drive the decision rather than being discarded after a well-formedness check. This exposes a parse that proves only syntax while its diagnostic claims semantic validation.

### Response and scoring tree

**S-29 — Response declaration cardinality.** Each written-response item must have exactly one effective response declaration with the expected response identifier and cardinality for its type. This exposes duplicate or shadow response declarations.

**S-30 — Scoring-reference binding.** Every `<varequal>` used to award credit must reference the declared response identifier, and no scoring reference may target a missing response. This exposes accepted strings attached to a response Canvas never reads.

**S-31 — Positive scoring branch structure.** Every accepted answer must lie in a response condition that awards the intended score, with the required `setvar` action and variable. This exposes an accepted-looking string in a dead or non-scoring branch.

**S-32 — No contradictory scoring branch.** No answer may be simultaneously accepted and rejected, reset after being awarded, or made dependent on an unrelated response condition. This exposes a flat accepted-string census that ignores execution order and tree semantics.

**S-33 — Exact accepted-string extraction.** The validator and battery must extract accepted strings only from operative scoring nodes, preserving internal bytes while applying only Canvas's documented trim and case-fold behavior. This exposes regex extraction from comments, negated branches, or unrelated metadata.

**S-34 — Numerical accepted shape.** Every numerical item's accepted values must be bare numbers permitted by the frozen format gate, and the structural instrument must reject units, labels, malformed signs, or symbolic expressions. This exposes a type census that never validates the actual accepted bytes.

**S-35 — Short-answer finite closure structure.** Every short-answer item must contain a finite, nonempty accepted set and a stem instruction that constrains student input to that set; structural green must not be represented as proof of mathematical completeness. This exposes an enumerated list used as a proxy for semantic closure.

**S-36 — Semantic limitation disclosure.** Validator and battery output must not claim to prove that a stem and key agree mathematically, because neither instrument recomputes the mathematics. This exposes a diagnostic broader than the property tested.

### Battery independence and branch reachability

**S-37 — Independent probe derivation.** `battery.py` must derive plausible correct probes from QTI canonical answers using logic independent of `finalize.py`'s accepted-set generator. This exposes a generator rubber-stamping its own omissions.

**S-38 — Positive branch execution.** Every written-response item must contribute at least one positive probe, and aggregate and per-item counters must prove that the positive membership branch executed. This exposes a guard that silently filters away every correct probe.

**S-39 — Positive branch falsifiability.** Removing a required accepted variant while retaining its canonical counterpart must make `battery.py` fail and name the rejected correct string. This exposes a positive branch that exists textually but cannot reject a defective item.

**S-40 — Negative branch execution.** Every written-response item must contribute fixed-invalid or independently derived near-miss probes, and counters must prove that the negative membership branch executed. This exposes the BF-2026-069 shape in which probes are filtered against the accepted set before membership is tested.

**S-41 — Negative branch falsifiability.** Adding a known-wrong probe to an accepted set must make `battery.py` fail and name the false accept. This exposes a negative branch that cannot detect over-acceptance.

**S-42 — Per-item battery accounting.** Battery success must reconcile the exact 199-item identity set and record nonzero applicable probe counts per item, not merely print a global total. This exposes one heavily tested item masking an entirely skipped item.

### Transformation integrity

**S-43 — Finalization scope preservation.** `finalize.py` must change only the intended item, metadata, and media sites, while every untouched item and file remains byte-identical except for explicitly permitted normalization. This exposes unbounded regular-expression replacement or a correction applied at the wrong granularity.

**S-44 — Item-count preservation or declared split accounting.** Every finalization operation must preserve item identities unless it performs an explicitly declared split, and split additions and parent replacements must reconcile exactly. This exposes silent item loss, duplication, or identifier collision.

**S-45 — Permutation conservation.** `permute.py` must preserve each item's choice multiset, scoring tree, keyed identifier set, item identity, and all non-choice bytes while changing only choice order. This exposes a visual shuffle that changes scoring or content.

**S-46 — Deterministic permutation.** Permutation must be a deterministic function of stable item identity and must produce the documented positional constraints for every eligible item. This exposes dependence on filesystem order, process randomness, or a check applied only to one lesson.

**S-47 — Media location identity.** Every required media basename must exist at exactly the three intended resolution locations, including the quiz-folder-derived location, and not merely at any three paths. This exposes coverage asserted where an exact location partition is required.

**S-48 — Media byte identity.** All mirrors of one media asset must be byte-identical and bound to the references used by the item stem. This exposes three resolvable files that render different questions.

### Build, publication, and reproducibility

**S-49 — Immutable source provenance.** With no explicit argument, `build.sh` must obtain every input ZIP from git ref `f63d392`; it must not read package inputs from the working tree, `zips/`, or an earlier work directory. This exposes self-feeding transformations and non-reproducible rebuilds.

**S-50 — Fixed stage order and fail-fast behavior.** The pipeline must execute `finalize.py`, `permute.py`, `validate.py`, `battery.py`, and `repackage.py` in that order and must stop before publication when any stage fails. This exposes validation of pre-transform bytes or publication after a failed gate.

**S-51 — Transactional publication and checksum binding.** `repackage.py` must stage the complete candidate outside the published output, publish nothing on any failure, remove stale unvouched ZIPs on success, and generate `sha256sums.txt` from exactly the ZIPs published in that transaction. This exposes mixed old/new output or a surviving checksum that vouches for different bytes.

**S-52 — Byte reproducibility.** Two consecutive builds from the same git ref, scripts, interpreter/toolchain, and environment must produce byte-identical ZIP checksum manifests, with deterministic member order, timestamps, permissions, and contents. This exposes artifacts whose identity changes despite unchanged source.

## Findings and direct answers from this derivation

### Rule narrower than its own message

No new presently reachable rule/message mismatch was established by a passing injection during this re-dispatch. Therefore this checklist does **not** claim a current gate hole in the manifest-binding, containment, metadata-cardinality, attribute-reading, scoring-tree, media-identity, transactional-publication, stage-ordering, or hostile-path families.

The source records historical examples in those families, but their comments describe repaired defects rather than evidence that the current build still admits them. Repeating those historical cases as current findings would be inaccurate.

The following families were inspected and converted into frozen requirements, but were **not mutation-proved exhaustively in this derivation**:

- S-02 hostile-path behavior;
- S-08 full candidate-space sweep;
- S-16 through S-23 manifest identity, both-direction completeness, containment, and dependency integrity;
- S-24 through S-28 metadata cardinality, exact attribute reading, direct-child granularity, namespace handling, and use of parsed content;
- S-29 through S-35 response and scoring-tree structure;
- S-43 through S-48 transformation and media identity;
- S-49 through S-51 provenance, stage ordering, and transactional publication.

A later judge must not mark those rules passed merely because no hole is listed here. They remain asserted but not proved.

### `EXPECT_ITEMS`

`validate.py` sets `EXPECT_ITEMS` to the literal constant `199`. Its runtime comparison computes the observed total from the resources it discovers; it does not assign `EXPECT_ITEMS` from that same runtime total. Thus the validator is not literally setting and checking the value with one computation.

A literal constant alone is not strong independence, however: both the constant and the validating traversal could be wrong in a coordinated way. The independent manifest-following census closes that gap for this frozen build. It separately found 199 unique package/item pairs and 199 globally unique identifiers and reconciled the exact 125/74 response-type partition. S-14 and S-15 therefore pass for the frozen build.

### Bidirectional `repackage.py` manifest check

Yes. The current `repackage.py` implements both directions:

1. it collects every manifest `href` and reports any href absent from the packaged file set; and
2. it walks every packaged file other than the root `imsmanifest.xml` and reports any file absent from the declared href set.

No present hole was found in those two direction checks by this derivation. Their basic source implementation is clean. Full adversarial mutation proof of normalization, containment, duplicate href semantics, and all package sites was not completed, so S-19 through S-22 still require later falsifiability evidence.

### `battery.py` branch execution and falsifiability

Both branches execute, and each was independently made to fail.

**Positive branch proof.** In an isolated extracted copy, the U+2212 accepted variant was removed from `topic-1-3-independent-practice-accuracy-check-qti`, item `Part 1 Question 1b`, while the canonical ASCII answer `-2` remained. `battery.py` exited 1 after exercising 199 items and 1,500 answers and reported:

`correct form '−2' rejected (canonical '-2')`

This proves the positive branch executes and can reject a missing correct notation variant.

**Negative branch proof.** In another isolated extracted copy, `xyzzy`, one of the battery's fixed invalid probes, was inserted into the accepted scoring set of `topic-sc-1-independent-practice-accuracy-check-qti`, item `Part 1 Question 1`. `battery.py` exited 1 after exercising 199 items and 1,500 answers and reported:

`wrong answer 'xyzzy' accepted`

This proves the negative branch executes and can reject an accepted wrong answer. It also proves the former BF-2026-069 unreachable-branch shape is not present in this current path.

The negative injection made `xyzzy` the shortest accepted value and therefore the battery displayed it as the derived canonical value. That diagnostic oddity does not invalidate the reachability proof — the fixed-invalid membership branch still observed `xyzzy` in the real accepted set and failed — but it shows why S-33 and S-42 require later item-level structural accounting rather than relying only on a global probe total.

### Build provenance and reproducibility

Source inspection establishes that the default `REF` is `f63d392`, inputs are enumerated with `git ls-tree`, and each source ZIP is read with `git show "$REF:$path"`. The pipeline does not use the working-tree packages or `zips/` as its extraction source.

Two consecutive complete builds produced byte-identical `sha256sums.txt`, and `cmp` was clean. S-52 passes for this frozen build. The broader provenance and stage-failure claims in S-49 through S-51 were not exhaustively mutation-proved here.

## Acceptance evidence required from the scoring judge

For each S-rule, the scoring report must record one of:

- `PASS`, with the positive and negative evidence or an established result explicitly carried above;
- `FAIL`, in `found / why / fix` form, including the minimal passing injection for any claimed gate hole; or
- `NOT PROVED`, identifying the missing mutation or observation.

A `NOT PROVED` rule may not be silently converted to `PASS`. Any change to the six instrument files, the package corpus, manifest bindings, accepted-answer trees, build source ref, or published ZIP bytes invalidates the applicable established results and requires fresh validation against a new build hash.
