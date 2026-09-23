# Fix the pre-PR review findings

## Context

The independent pre-PR review of `main...kg-conversion` (2026-09-23, framed
as an OWL/PROV-O/SHACL/LinkML/Synapse-governance reviewer) reported 10
findings. Each was re-verified against the code before this plan:

| # | finding | verified by |
|---|---|---|
| 1 | `sync_provenance_graph.build_activity()` warns with an undefined `entity_id`, so an unrecognized `Used.concreteType` raises NameError | reading `:118` |
| 2 | Activity `createdOn`/`modifiedOn` go from the REST payload (ISO-8601 strings) straight into `range: integer` slots | reading `:125`; `sync_governance_graph.to_millis()` already handles this for the other objects |
| 3 | 5 of the 48 hand-written `rdfs:domain` axioms in `shapes/governance_graph.owl.ttl` are contradicted by the repo's own graphs, so a reasoner mis-types nodes | applying all 48 to the exported and provenance graphs: `gov:etag` (ResearchProject, AccessApproval, DataAccessRequest), `gov:submittedBy` (AccessApproval), `gov:modifiedBy` (DataAccessRequest), `gov:hasCondition` (AccessRequirementTemplate), `gov:description` (prov:Activity) |
| 4 | `IRBRequirement.studyId` is `owl:sameAs`, which asserts the IRB requirement *is* the Study | `linkml/governance_graph.yaml:1022` |
| 5 | A matching DerivationRule's `resultingDataTier` replaces the tier, ignoring the entity's own AR binding (fail-open) | `build_derivation_policy.py:237` |
| 6 | Rules are keyed by the exact tuple of all input tiers, so an Activity with 3+ inputs never matches the pairwise rules and required reviews are skipped | `:278` |
| 7 | DUO:0000016 (GSO) is described as "Geographical Restriction - ..." | `linkml/mixins.yaml:500`, `model/valid_values.csv:280` |
| 8 | CI never checks committed artifacts against the schema, and never runs `linkml-validate`, the only enforcer of the DUO `rules:` | `.github/workflows/validate.yml`, Makefile |
| 9 | `gov:hasApproval` is emitted from historical APPROVED Submissions and from APPROVED AccessApprovals without checking `expiredOn` | `build_governance_graph.py:410,552` |
| 10 | The legacy `collate`/`convert`/`generate-json` targets (and default `all`) write to `sage-ar-model/`, which moved to `archive/` | Makefile `:1-20`, `scripts/create_json_from_model.py` |

## Decisions (approved 2026-09-23)

- **#3:** drop the 5 contradicted domains, and add a check that every
  `rdfs:domain` and `rdfs:range` in both TBoxes holds on every exported and
  example graph.
- **#4:** a new plain object property `sagegov:forStudy` replaces `owl:sameAs`.
- **#5/#6:** final tier = max(own direct-binding tier, rule/inherited tier).
  A review is flagged when any *pair* of labeled inputs matches a rule that
  requires review or forbids the combination. Tier overrides still need an
  exact match of all inputs.
- **#9:** `gov:hasApproval` comes only from AccessApprovals with status
  APPROVED whose `expiredOn` is absent or later than the build's as-of time.
  It no longer comes from Submissions.
- **#8:** add `linkml-validate` over every example to `validate-all`. Add a CI
  drift check comparing regenerated artifacts with the committed ones:
  byte-for-byte for the OWL, blank-node-agnostic for the rest.
- **#10:** remove the legacy targets and default `all`; the README marks
  `archive/sage-ar-model/` as archived.
- **DUO:0000017** (the abstract data-use-modifier root, selectable today):
  leave it; record it as a curation follow-up.

## Approach

One commit per step.

1. **Provenance sync (#1, #2).** Warn with the Activity id. Pass timestamps
   through `sync_governance_graph.to_millis()`. Extend the offline fixture in
   `check_sync_provenance.py` with ISO-8601 `createdOn`/`modifiedOn` (assert
   epoch-ms `xsd:integer` literals) and an unrecognized `Used` entry (assert a
   warning, no crash, still 2 Usages).
2. **DUO:0000016 text (#7).** Correct the description in `linkml/mixins.yaml`
   and `model/valid_values.csv` to DUO's own label, "Genetic Studies Only".
   Regenerate the OWL/SHACL/docs/governance graph.
3. **Domains (#3).**
   - Remove the 5 domains.
   - Add `scripts/check_domain_range.py`: for each `rdfs:domain`/`rdfs:range`
     (to a class) in `shapes/governance_graph.owl.ttl`, every subject/object
     in the graphs must already be typed with that class or a subclass (no
     entailment). The graphs are the exported governance graph and the
     provenance and derivation-policy example RDF.
   - Run it from `validate-all`. Confirm it fails with the 5 domains restored.
4. **`sagegov:forStudy` (#4).**
   - `linkml/governance_graph.yaml`: `studyId` gets `slot_uri:
     sagegov:forStudy` and a corrected description.
   - `shapes/governance_graph.owl.ttl`: declare it an `owl:ObjectProperty`
     with domain IRBRequirement, and correct IRBRequirement's comment.
   - `shapes/governance_graph.shacl.ttl`: the IRBRequirement shape's
     `owl:sameAs` path becomes `sagegov:forStudy`.
   - Update the `build_governance_graph.py` docstring. Regenerate.
5. **Derivation policy (#5, #6).**
   - `label_for()` applies the own-binding floor.
   - `compute_derivation_reviews()` evaluates rules pairwise for the review
     flag.
   - Extend the fixture: a Controlled rule; a Private-bound output derived
     from two Controlled inputs (expect Private, not Controlled); a
     3-Controlled-input Activity sharing one AR (expect a review from the
     pairwise rule, not from disjointness).
   - Update the check's assertions, the fixture README and the module
     docstring.
6. **`gov:hasApproval` (#9).**
   - `add_access_approval()` takes `as_of_ms` and emits only for unexpired
     approvals. `add_data_access_submission()` stops emitting it.
   - `build_governance_graph.py --as-of` (default: now). The Makefile pins the
     worked example to a fixed `GOVERNANCE_GRAPH_AS_OF`, so the export doesn't
     change as the calendar moves past its `expiredOn`. The sync passes now.
   - Add an expired approval to the examples and assert it yields no
     `gov:hasApproval` (in the step-3 check's graph set, via a new ASK in
     `check_infra_contract.py`, which already owns the grant/approval
     assertions).
   - Update the docs that describe the Submission-derived edge.
7. **CI (#8).**
   - `scripts/validate_examples.py` runs `linkml-validate` on every example,
     using the converters' own `EXAMPLE_CLASSES` maps, and fails on any
     example with no mapped class. `make linkml-validate-examples` joins
     `validate-all`.
   - `scripts/check_artifact_drift.py` compares each regenerated artifact
     with `HEAD`: byte-for-byte for `governance_duo.owl.ttl`, and a
     blank-node-agnostic comparison (iterated neighborhood hashing, fast on
     the SHACL) for the SHACL, example RDF and governance-graph export. A CI
     step runs it after `validate-all`.
8. **Legacy targets (#10).** Delete `all`/`build-csv`/`collate`/`convert`/
   `generate-json` and the `CSV`/`CONFIG`/`DATA` variables. Move
   `scripts/create_json_from_model.py` to `archive/scripts/`. Mark the README
   row and the "Known follow-up" item as archived.
9. **Report.** Write `plans/pre_pr_review_fixes_report.md`.

## Verification

- `make validate-all` passes, including the new domain/range, example
  `linkml-validate` and extended fixture checks.
- Each new check fails when its bug is reintroduced:
  - the 5 domains restored;
  - an example violating a DUO rule;
  - the old tier logic;
  - the Submission-derived `hasApproval`;
  - a hand-edited committed artifact.
- `make owl-profile` and the PROV-O check still pass.
- `make sagebrain-contract-check` gives the same results as before this plan:
  the DL union fails only on the stale sagebrain import, and the SHACL failure
  is the one that predates this work.
- `mkdocs build --strict` passes.
