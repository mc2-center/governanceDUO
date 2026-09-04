# Report: AccessRequirementReference class

Executed against [`access_requirement_reference_class.md`](access_requirement_reference_class.md). All six target changes were implemented as planned, with no scope deviations.

## Target change 1 — new `AccessRequirementReference` class: as planned

Added to `linkml/governance_graph.yaml`, placed directly after `AccessRequirementAssociation`: not `is_a: BaseEntity`, `class_uri: sagegov:AccessRequirement` (the exact IRI the script already emitted as `GOV.AccessRequirement` — no change to what's on the wire), two slots:

- `sameAs` — `slot_uri: owl:sameAs`, `range: uriorcurie`, `required: true`. Same pattern as `IRBRequirement.studyId` (added earlier this session): `uriorcurie` rather than a class-typed range, since the real `AccessRequirement` individual it points at is never itself asserted/typed in this ABox.
- `hasCondition` — reused the slot already declared for `AccessRequirementTemplate` (`slot_uri: sagegov:hasCondition`, `range: Condition`, `multivalued: true`); its description was broadened to cover both classes rather than duplicated.

## Target change 2 — repointed the three stub-referencing slots: as planned

`AccessRequirementAssociation.accessRequirement`, the shared `accessRequirementId` (`DataAccessSubmission`/`ResearchProject`/`DataAccessRequest`), and `AccessApproval.requirementId` all changed `range: AccessRequirement` → `range: AccessRequirementReference`. `slot_uri`/`close_mappings`/`comments` left untouched; only `range` changed, plus a one-line addition to each description noting the range now points at the stub, not the real class.

## Target changes 3 & 4 — script updates: as planned

`add_access_requirement_association()`: `RDF.type` now resolves via `TYPE("AccessRequirementReference")`; the `owl:sameAs` assertion now resolves via `PREDICATE("sameAs", "AccessRequirementReference")` instead of a hardcoded `OWL.sameAs` constant. The comment block above these two lines was rewritten to describe the new class instead of "no governance_graph.yaml class of its own."

`add_access_requirement()`: the `gov:hasCondition` assertion now resolves via `PREDICATE("hasCondition", "AccessRequirementReference")`. Its docstring's import-cycle explanation was rewritten to say the constraint no longer applies to this predicate specifically, since `AccessRequirementReference` (unlike the real `AccessRequirement`) is owned by `governance_graph.yaml`, the same file that defines `Condition`.

The module-level docstring's schema-undeclarable-decisions list also dropped its `owl:sameAs` bullet, since that bridge is now a real, schema-resolved slot like everything else the script emits — it no longer belongs in a list of things a generic dump can't reproduce.

## Target change 5 — regenerated artifacts: as planned

`make owl shacl` regenerated `shapes/governance_duo.owl.ttl`/`.shacl.ttl`. `shapes/governance_graph.owl.ttl`'s hand-authored shapes were left untouched (its header comment already only listed `hasACL`/`hasAccessRequirement`/`hasApproval` as residual gaps — it never claimed `hasCondition`/this stub's `owl:sameAs` were unfixable, so needed no correction). `shapes/governance_graph.shacl.ttl`'s header *did* need a correction: it previously said "AccessRequirement itself ... accounts for all 5 ClassConstraintComponent misses on its own" as a still-open problem — rewritten to note `AccessRequirementReference` now closes those, and the violation count in the header updated from 48 to 42 (see Verification below).

## Target change 6 — documentation updates: as planned

- `docs/knowledge-graph.md`'s "What's still hand-written" list: dropped `hasCondition` from the `hasACL`/`hasAccessRequirement`/`hasCondition` bullet (now just the first two, with an explanation of why those two specifically resist this same fix — see the "Explicitly out of scope" resolution added to the plan during review), and added a note that `hasCondition` and the stub's `owl:sameAs` are now real slots.
- `make docs` regenerated `docs/reference/**` from the updated schema: new `AccessRequirementReference.md`/`sameAs.md` pages, updated cross-references on `AccessApproval`, `AccessRequirement`, `AccessRequirementAssociation`, `AccessRequirementTemplate`, `Condition`, `DataAccessRequest`, `DataAccessSubmission`, `IRBRequirement`, `ResearchProject`, and the `accessRequirement`/`accessRequirementId`/`hasCondition`/`requirementId`/`studyId` slot pages.

## Verification — all passed

- `python3 scripts/build_governance_graph.py ...` then `git diff governance_graph_export/governance_graph.ttl`: **empty** — the exported ABox is byte-identical to before this change, confirming this was a pure schema/script-annotation refactor with no output change.
- `make shacl-validate`: `Conforms: True` on both the schema build and the example instances.
- `make governance-graph-validate`: `Conforms: True`.
- Direct pySHACL check (validating `governance_graph_export/governance_graph.ttl` against `shapes/governance_duo.shacl.ttl`/`.owl.ttl` alone, `inference="none"` — the same ad hoc check that originally found 48 violations, then 47 after the `IRBRequirement.studyId` fix): now **42 violations**, a clean drop of 5. The `ClassConstraintComponent` category is gone entirely (was 5), and no violation on `sagegov:AR-42` itself remains at all — confirming the fix closed exactly the targeted gaps with no new ones introduced. The remaining 42 (8 `ClosedConstraintComponent`, 18 `DatatypeConstraintComponent`, 5 `InConstraintComponent`, 2 `MinCountConstraintComponent`, 9 `NodeKindConstraintComponent`) are the deliberate RDF-convention divergences documented in `shapes/governance_graph.shacl.ttl`'s header (enum-as-IRI-individuals, integer-range slots populated with `Principal` IRI references, `DataAccessSubmission`/`DataAccessSubmissionStatus` merged onto one subject, `rdf:type`-based Team/User subtyping) — explicitly out of scope for this plan.

## Files touched

`linkml/governance_graph.yaml`, `scripts/build_governance_graph.py`, `shapes/governance_duo.owl.ttl`, `shapes/governance_duo.shacl.ttl`, `shapes/governance_graph.shacl.ttl` (header only), `docs/knowledge-graph.md`, `docs/reference/**` (regenerated).
