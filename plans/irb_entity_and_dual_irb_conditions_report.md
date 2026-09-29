# Report: IRB entity and dual-IRB conditions

Executed against [`irb_entity_and_dual_irb_conditions.md`](irb_entity_and_dual_irb_conditions.md). All ten target changes (Part A items 1-6, Part B items 7-10) were implemented as planned, with no design deviations. Two files not named in the plan needed small, mechanical wiring changes — see "Deviations" below.

## Part A — record-layer `IRB` entity and `IRBKey` rule

**Item 1 — `IRBKey` slot in `linkml/props.yaml`**: added immediately after `StudyKey`, exact shape specified (multivalued, pattern `^irb\.[A-Za-z0-9_-]+$`, `annotations: {foreign_key: true}`).

**Items 2-3 — `GovernanceMixin` wiring in `linkml/mixins.yaml`**: `IRBKey` added to `GovernanceMixin.slots` (not per-class), and a new rule appended matching the existing 35: `dataUseModifiers equals_string DUO:0000021` → `IRBKey required: true`. Since every class mixing in `GovernanceMixin` inherits the slot, `AccessRequirement`, `Study`, and `Resource` all gained `IRBKey` automatically; `Schema` did not (confirmed it does not mix in `GovernanceMixin`, so this is correct, not a gap).

**Item 4 — `linkml/irb.yaml`**: new file, structured on `linkml/study.yaml`'s pattern — `is_a BaseEntity`, `mixins: [ContributionMixin]` (reused for curator provenance, not reinvented), `tree_root: true`, id pattern `^irb\.[A-Za-z0-9_-]+$`. Slots: `AccessRequirementKey`, `StudyKey` (both reused, for bidirectional cross-referencing matching `Study`'s own use of `AccessRequirementKey`), plus new `irbProtocolNumber` (required), `irbName` (required), `irbApprovalStatus` (new `IRBApprovalStatusEnum`: Approved/Pending/Expired/Withdrawn), `irbApprovalDate`, `irbExpirationDate`, `irbAssociatedProjects` (multivalued Synapse Project id, for IRB approvals not reachable through a Study record).

**Item 5 — umbrella import**: `- irb` added to `linkml/governance_duo.linkml.yaml`'s `imports:`, alongside `access_requirement`/`resource`/`schema`/`study`.

**Item 6 — worked examples**: `linkml/examples/irb.example.yaml` / `docs/example_instances/IRB-001.yaml` (Mount Sinai IRB record, identical content per the existing duplication convention), and `linkml/examples/access_requirement_two_irbs.example.yaml` / `docs/example_instances/AccessRequirement-003-two-irbs.yaml`:
```yaml
id: access_requirement.201
dataUseModifiers: [DUO:0000021]
IRBKey: [irb.mount-sinai-001, irb.jax-002]
```
— the direct, worked answer to "can one AR need two IRB approvals" at the record layer.

## Part B — graph-layer `Condition.approvingIRB`

**Item 7**: new slot `approvingIRB` added to `linkml/graph/governance.yaml` immediately after `forStudy`, same untyped-`uriorcurie` treatment (single-valued, no typed class range, since the record-layer `IRB` individual it points at is never itself asserted in this ABox). Added to `Condition`'s slot list.

**Item 8 — regeneration**: `make graph-tbox` / `make graph-owl-profile` regenerated `shapes/governance.owl.ttl` / `shapes/governance.shacl.ttl`. `ConditionShape` gained exactly the expected property: `gov:approvingIRB`, `sh:maxCount 1`, `sh:nodeKind sh:IRI` — byte-for-byte the same shape `forStudy` already gets. `ConditionShape` is `sh:closed true`, so this addition was required for the mechanism in item 9 below to validate at all (confirmed: it does).

**Item 9 — two-IRB worked example**: `linkml/examples/graph/governance_graph.example.yaml`'s `conditions:` list extended with two new `DUO:0000021` Condition instances (`..._mount-sinai`, `..._jax`), differing only in `approvingIRB`, both attached to `govid:ar/42` via `hasCondition` alongside the existing `DUO:0000007` condition — the literal RDF-level proof that two distinct IRB approvals now attach to one Access Requirement.

**Item 10 — doc touch-ups**: one sentence added to `docs/graph-design.md` section 4 (Conditions bullet) describing the two-`Condition`/`approvingIRB` mechanism, and one row + one sentence added to `docs/linkml-model.md`'s class inventory and rules-count note (35 → 36).

## Deviations from the plan (both mechanical, not design changes)

The plan didn't anticipate that three scripts hardcode per-class lists that needed the new class/example added to keep the existing pipelines working:

- `scripts/build_json_schemas.py`: `CURATOR_CLASSES` list — added `"IRB"`, so `make json-schemas` generates `json_schemas/IRB.json`.
- `scripts/convert_examples_to_rdf.py`: `EXAMPLE_CLASSES` dict — added `"irb": "IRB"` and `"access_requirement_two_irbs": "AccessRequirement"`, so the new examples convert to RDF and get picked up by `validate_examples.py` (which imports this same dict).
- `scripts/prepare_doc_examples.py`: `EXAMPLE_MAP` dict — added the two new example → `docs/example_instances/*.yaml` mappings.

All three are one-line-per-entry additions to existing lookup tables, following the exact pattern every other curator class/example already uses in the same tables. No script logic changed.

## Verification — all passed

- **`make json-schemas`**: `json_schemas/IRB.json` generated. `json_schemas/AccessRequirement.json` gained exactly one new `if`/`then` conditional (36 total, up from 35 — confirmed by direct diff inspection, not just count). `Study.json`/`Resource.json` gained the same conditional (both mix in `GovernanceMixin`); `Schema.json` unaffected.
- **`make owl shacl`, `make docs`**: regenerated clean. `docs/reference/classes/IRB.md`, `docs/reference/enums/IRBApprovalStatusEnum.md`, and seven new/updated slot pages generated correctly (spot-checked `IRB.md`'s rendered class diagram and slot list).
- **Structural SHACL diff (not just line diff)**: the raw `git diff` on `shapes/governance_duo.shacl.ttl` is large (~1350 lines) because inserting `irb` into the schema's import list shifts the generator's internal class/property iteration order — but this is cosmetic. A blank-node-aware structural comparison (parsed both versions with `rdflib`, compared per-`sh:path` constraint sets per class rather than raw triples/line diffs) found **exactly 15 property-level differences, all additions, zero removals or changes**: `IRBKey` added to `AccessRequirement`/`GovernanceMixin`/`Resource`/`Study`, and the 8 new properties (`identifier`, `AccessRequirementKey`, `StudyKey`, `contributionDate`, `contributorName`, `irbApprovalDate`, `irbApprovalStatus`, `irbAssociatedProjects`, `irbExpirationDate`, `irbName`, `irbProtocolNumber`) on the new `IRB` shape. The smaller `shapes/governance.shacl.ttl` (graph layer) diff was reviewed directly (not just structurally) and is exactly the expected `gov:approvingIRB` addition to `ConditionShape` plus a cosmetic `sh:order` renumbering of its two sibling properties.
- **Negative-case rule check**: constructed an in-memory `AccessRequirement` record with `dataUseModifiers: [DUO:0000021]` and no `IRBKey` (via `linkml.validator.Validator`, not a committed fixture file) — **fails validation** (`'IRBKey' is a required property`), confirming the new rule actually fires. The equivalent record with `IRBKey: [irb.mount-sinai-001, irb.jax-002]` added — **validates clean**, confirming the two-IRB case is fully supported at the record layer.
- **`make graph-tbox graph-owl-profile graph-validate`**: all passed, `Conforms: True` on the extended `governance_graph.example.yaml` (the two-`DUO:0000021`-Condition case).
- **`make validate-all`**: full regression pass, every target green — `shacl-validate`, `governance-graph-validate`, `derivation-policy-validate`, `sync-provenance-check`, `sync-governance-check`, `derivation-policy-check`, `infra-contract-check`, `projections-check`, `linkml-validate-examples`, `owl-profile` (OWL 2 DL profile conformant, both TBox alone and merged with every canonical ABox), `graph-validate`, `graph-owl-profile`. The "Duplicate tree_root: IRB with PolicyCardBindingCollection" informational message that appears during example-to-RDF conversion is the same pre-existing warning the other four curator classes (`AccessRequirement`/`Resource`/`Schema`/`Study`) already trigger against `PolicyCardBindingCollection` — not a new issue.

## Files touched

`linkml/props.yaml`, `linkml/mixins.yaml`, `linkml/irb.yaml` (new), `linkml/governance_duo.linkml.yaml`, `linkml/graph/governance.yaml`, `linkml/examples/irb.example.yaml` (new), `linkml/examples/access_requirement_two_irbs.example.yaml` (new), `linkml/examples/graph/governance_graph.example.yaml`, `docs/example_instances/IRB-001.yaml` (new), `docs/example_instances/AccessRequirement-003-two-irbs.yaml` (new), `docs/graph-design.md`, `docs/linkml-model.md`, `scripts/build_json_schemas.py`, `scripts/convert_examples_to_rdf.py`, `scripts/prepare_doc_examples.py`, plus regenerated artifacts: `json_schemas/{AccessRequirement,Study,Resource,IRB}.json`, `shapes/governance_duo.{owl,shacl}.ttl`, `shapes/governance.{owl,shacl}.ttl`, `docs/reference/**` (regenerated), `governance_graph_export/governance_graph.ttl`, `linkml/examples/rdf/**`, `linkml/examples/graph/rdf/governance_graph.ttl`.

## Left open

- **Policy Fabric wiring** (explicitly out of scope in the plan): `linkml/policy_fabric_bindings.yaml`'s `ethics-approval-required` binding for `DUO:0000021` still has `referenceValueKeys: []`. Teaching it to check a specific `IRBKey`/`approvingIRB` value would be a natural follow-on, not done here.
- Nothing else from the plan was deferred.
