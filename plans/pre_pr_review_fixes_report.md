# Report: pre_pr_review_fixes.md

All 10 findings of the pre-PR review were verified and addressed as decided on
2026-09-23. Each fix comes with a check that fails when the bug comes back.
There's one new open item: enum values don't match the OWL (below).

## Changes

| # | commit | change | new/extended check (fails on the old code) |
|---|---|---|---|
| 1, 2 | `bcf7889` | `sync_provenance_graph.py`: the unrecognized-`Used` warning names the Activity (was an undefined `entity_id` → NameError); `createdOn`/`modifiedOn` go through `to_millis()`. | `check_sync_provenance.py`: the fixture now has ISO-8601 timestamps (asserts epoch-ms `xsd:integer`) and an unknown `Used` subtype (asserts a warning and still 2 Usages). The old code raises the NameError. |
| 7 | `9df344a` | DUO:0000016's description label is now "Genetic Studies Only", matching DUO's own label (checked in OLS), in `linkml/mixins.yaml` and `model/valid_values.csv`. Regenerated the OWL and docs. | (text fix) |
| 3 | `fae356b` | Dropped `rdfs:domain` from `gov:etag`, `gov:submittedBy`, `gov:modifiedBy`, `gov:hasCondition` and `gov:description`. Each property's comment now says which classes share it. | `check_domain_range.py` (`make domain-range-check`, in `validate-all`): every `rdfs:domain` and class-valued `rdfs:range` in both TBoxes must hold on the exported and example graphs. It reports 7 violations on the old TBox. |
| 4 | `d97936f` | `IRBRequirement.studyId` now maps to `sagegov:forStudy` (a plain `owl:ObjectProperty`, domain IRBRequirement), not `owl:sameAs`. Updated the schema, hand-written OWL/SHACL and builder, then regenerated. | The domain/range check covers the new domain. The OWL stays in DL. |
| 5, 6 | `c8c08ce` | `build_derivation_policy.py`: a rule's `resultingDataTier` can lower what an entity inherits, never its own direct binding. The review flag now evaluates rules on every pair of labeled inputs as well as the whole set. | `check_derivation_policy.py` (6 → 9 assertions). The fixture gains a Controlled+Controlled rule, a Private-bound output derived from two Controlled inputs, and a 3-input Activity whose inputs share one AR. The old logic fails 3 assertions: tier Controlled instead of Private, no review for the 3-input Activity, and 2 reviews instead of 3. |
| 9 | `86e3eee` | `gov:hasApproval` comes only from an AccessApproval with status APPROVED and `expiredOn` absent or later than `--as-of`; Submissions no longer emit it. A sync uses the current time. The worked example is pinned to `GOVERNANCE_GRAPH_AS_OF` = 2026-01-01, because its approval's `expiredOn` (2026-08-14) has already passed. Docs, OWL/SHACL comments and the AccessApproval description are updated. | `check_approval_expiry.py` (`make approval-expiry-check`, in `validate-all`) builds the example 1 ms before and after `expiredOn`, with its Submission status set to APPROVED. The old builder still emits the edge for the long-expired approval. |
| 8 | `98adb37` | Added `validate_examples.py` (`make linkml-validate-examples`, in `validate-all`): LinkML validation of all 21 examples, with target classes taken from the converters' own maps. It fails on an unmapped example. Also added `check_artifact_drift.py` (`make artifact-drift-check`, run by CI after `validate-all`). | Removing `diseaseSpecificResearch` from the AR example fails the validation on the DUO rule. A one-value edit to the committed SHACL fails the drift check. A clean rebuild passes. |
| 10 | `109c4f1` | Removed `all`/`build-csv`/`collate`/`convert`/`generate-json` and their variables. `create_json_from_model.py` moved to `archive/scripts/`. `make` now defaults to `validate-all`. The README row and "Known follow-up" now describe `archive/sage-ar-model/` as archived. | — |

## Deviations from the plan

- **Approval expiry check (#9).** The plan put it in `check_infra_contract.py`.
  That script is about the sagebrain-infra authorizer, so the check went into
  its own `check_approval_expiry.py`. It builds the real example rather than
  asserting on an in-memory edit.
- **Enum ranges (#3).** `check_domain_range.py` skips ranges over LinkML enums.
  This exposed a new issue (open item 1).
- **Drift check normalization (#8).** A clean rebuild of the SHACL doesn't
  just reorder blank nodes: gen-shacl writes one 126-member
  `sh:ignoredProperties` list in a different order each run. SHACL reads that
  list, and `sh:in`, as a set, so the drift check sorts their members before
  comparing. This also refines the earlier "accept the churn" note: the churn
  includes list order, which has no meaning.
- **`make` default (#10).** With `all` gone, `.DEFAULT_GOAL := validate-all`,
  so a bare `make` runs what CI runs rather than whichever target happens to
  come first.

## Verification (on `109c4f1`)

- **`make validate-all`:** exit 0. That covers every SHACL validation, the sync,
  derivation-policy (9 assertions) and infra-contract checks, and the new
  domain/range, approval-expiry and example-validation checks.
  `owl-profile` passes (DL alone and merged) along with the PROV-O check.
- **`make artifact-drift-check` after `validate-all`:** all 12 artifacts match
  HEAD.
- **`mkdocs build --strict`:** passes.
- **`make sagebrain-contract-check`:** all four parts pass. The two earlier
  failures were not fixed here: sagebrain-model has since landed the
  governance import (its `scripts/import.sh` pins
  `GOVERNANCEDUO_COMMIT=240a162`, which declares `prov:generated`/`prov:entity`
  as object properties) and fixed its SHACL.

## Open items

1. **Enum-valued slots don't use the OWL's enum IRIs (new, not fixed).** The
   generated OWL types each enum slot `owl:ObjectProperty` with an enum class
   as range. That class is the union of `governanceduo:<Enum>#<value>` IRIs
   (or `meaning:` IRIs, e.g. `obo:DUO_0000007`). The data doesn't match:
   - **Literals on object properties:** `governanceduo:inputDataTiers`/
     `resultingDataTier` `"Controlled"`, `studyDeidentificationType`
     `"SafeHarbor"`, `sourceGeography` `"US"`, `sagegov:reviewStatus`
     `"Flagged"`. That is not DL wherever the ABox meets the TBox. It's the
     same kind of issue as `plans/iri_valued_slots_as_object_properties.md`.
   - **Different IRIs:** `gov:permission` `gov:DOWNLOAD`/`gov:ACCESS`,
     `gov:state` `gov:SUBMITTED`, `gov:status` `gov:APPROVED`, `gov:bindingType`
     `gov:Direct`/`gov:Inherited`. The OWL's members are
     `governanceduo:AccessTypeEnum#DOWNLOAD`, etc.

   Only the DUO codes agree. The fix needs a decision per enum:
   - give the permissible values `meaning:` IRIs matching what the builders
     write (`gov:<value>`), and have the example-RDF converter emit IRIs;
   - or make these slots datatype properties.

   This is the next thing to plan.
2. **DUO:0000017 (DUM)** stays selectable, as decided. It's the abstract
   data-use-modifier root, so selecting it yields a Condition that restricts
   nothing. This is a curation follow-up.
3. **sagebrain-model pins an unpushed commit.** `GOVERNANCEDUO_COMMIT=240a162`
   isn't on `origin` yet. Pushing `kg-conversion` makes it resolvable. The
   commits here change terms sagebrain imports (`gov:forStudy`, the dropped
   domains, the `gov:hasApproval` comment), so re-bumping the import to this
   head keeps the two in step.
