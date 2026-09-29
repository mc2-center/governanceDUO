A first-class IRB record, and a structural fix for two IRBs on one dataset

Status: proposed (user, 2026-09-28), not yet implemented. This plan answers two
questions raised in that discussion: (1) can the model represent a dataset that
needs two different IRB approvals, and (2) can we add an entity to represent an
IRB itself (identifier, associated studies/projects). Both are additive changes;
neither touches `dataUseModifiers`' existing flat-list semantics or any other
DUO-code's companion-slot mechanism.

Context

This repo has two independent schemas for DUO conditions (`docs/linkml-model.md`),
and they currently answer "can one AR need two IRB approvals?" differently:

- **Graph layer** (`linkml/graph/governance.yaml`) already models a `Condition`
  as a first-class node (`Condition:`, line 193), attached to an
  `AccessRequirement` via `hasCondition` (line 527), which is multivalued with
  no `maxCount` in either LinkML or the generated SHACL (`shapes/governance.shacl.ttl`
  line 606-609: `sh:path gov:hasCondition` carries no `sh:maxCount`). Nothing
  today stops two `Condition` nodes, both `dataUseTerm: DUO:0000021` ("Ethics
  Approval Required" — `linkml/graph/vocabularies.yaml:269-271`), from being
  attached to the same `AccessRequirement`. This already works structurally; it
  has just never been exercised in the canonical example.
- **Record layer** (`linkml/mixins.yaml`) cannot represent it at all today.
  `GovernanceMixin.dataUseModifiers` (line 35) is a flat multivalued *enum* list
  — a set of codes, not inlined objects — so a second occurrence of
  `DUO:0000021` carries no additional information. Every other DUO code that
  needs a parameter (disease, geography, agreement id, ...) gets a dedicated
  companion slot on `GovernanceMixin`, wired up by one of the ~35 conditional
  `rules:` entries in `linkml/mixins.yaml` (lines 730-1010: e.g. line 731-738,
  `DUO:0000007` → `diseaseSpecificResearch` required). **`DUO:0000021` has no
  companion slot and no rule anywhere in that block** — confirmed independently
  by the Policy Fabric crosswalk (`linkml/policy_fabric_bindings.yaml`, the
  `ethics-approval-required` binding for `DUO:0000021`, `referenceValueKeys: []`
  — a pure credential-chain check with no structured IRB data expected either).
  So today a curated `AccessRequirement` record can say "IRB approval required"
  but has nowhere to put even one IRB's identifying information, let alone two.

Separately, an IRB-*shaped* class already exists — `IRBRequirement`
(`linkml/graph/governance.yaml` line 179), a subclass of `AccessRequirement` —
but it is not a standalone entity for "the IRB itself." It represents *a
requirement that demands IRB approval*, single-scoped to one
`extendsTemplate`/`forStudy`/`scopedToProgram`/`scopedToSite` (all
`maxCount: 1`, confirmed in `shapes/governance.shacl.ttl` lines 605-614 and the
surrounding `IRBRequirementShape` block). There is no record-layer or
graph-layer entity today for "IRB #4821 at Mount Sinai," reusable across
studies and queryable by its own identifier — the record layer has no `IRB`
class at all, unlike its `Study` class (`linkml/study.yaml`), which is the
closest existing template for what one should look like.

Target changes

**Part A — a first-class `IRB` record-layer entity**

1. New shared cross-reference slot `IRBKey` in `linkml/props.yaml`, immediately
   after `StudyKey` (line 39-46), following the exact same shape as
   `AccessRequirementKey` (line 15-38) and `StudyKey`:
   ```yaml
   IRBKey:
     description: >-
       The IRB record id(s) associated with this object. Provide multiple
       values as a comma-separated list.
     multivalued: true
     pattern: '^irb\.[A-Za-z0-9_-]+$'
     annotations:
       foreign_key: true
   ```
   Pattern-matched string, not a typed `range`, for the same cycle-avoidance
   reason `props.yaml`'s existing comment gives for `AccessRequirementKey`
   (`plans/identifier_update.md`) — this file has no import relationship with
   the new `irb.yaml` below and shouldn't need one.

2. Add `IRBKey` to **`GovernanceMixin`'s own `slots:` list**
   (`linkml/mixins.yaml`, the block at lines 703-729), not to `AccessRequirement`
   or `Study` individually. This is a deliberate difference from how
   `StudyKey`/`AccessRequirementKey` are wired (added per-class, since they're
   always-present entity-to-entity links): `IRBKey` behaves exactly like the
   other ~26 DUO-triggered companion slots already in `GovernanceMixin`
   (`diseaseSpecificResearch`, `geographicalRestriction`, etc.) — conditionally
   required by one specific `dataUseModifiers` code — so it belongs at the same
   level they're declared at. This also means every class that already mixes in
   `GovernanceMixin` (`AccessRequirement`, `Study`, `Resource` — per the
   docstring at `linkml/mixins.yaml:700`) gets it for free, since IRB approval
   can in principle attach to any of them, not just `AccessRequirement`.

3. New rule appended to `GovernanceMixin.rules:` (`linkml/mixins.yaml`, after
   the last entry in the 730-1010 block), matching the exact shape of the
   existing 35:
   ```yaml
   - preconditions:
       slot_conditions:
         dataUseModifiers:
           equals_string: DUO:0000021
     postconditions:
       slot_conditions:
         IRBKey:
           required: true
   ```
   Because `IRBKey` is already multivalued, this is the entire fix for "two
   IRBs" at the record layer: a curator lists two IRB record ids
   (`IRBKey: [irb.mount-sinai-001, irb.jax-002]`) instead of one.

4. New file `linkml/irb.yaml`, structured directly on `linkml/study.yaml`'s
   pattern (`is_a: BaseEntity`, `tree_root: true`, own id pattern):
   ```yaml
   id: https://w3id.org/sage-bionetworks/governance-duo/irb
   name: governance_duo_irb
   description: LinkML representation of the IRB (Institutional Review Board) component.
   prefixes:
     governanceduo: https://w3id.org/sage-bionetworks/governance-duo/
     linkml: https://w3id.org/linkml/
   default_prefix: governanceduo
   default_range: string
   imports:
     - linkml:types
     - base_entity
     - mixins
     - props
   classes:
     IRB:
       description: >-
         An Institutional Review Board (or equivalent Ethics Review Board)
         approval record: the body that granted it, its protocol identifier,
         and the studies/projects/access requirements it covers.
       is_a: BaseEntity
       mixins:
         - ContributionMixin
       tree_root: true
       slot_usage:
         id:
           description: A unique identifier for the IRB approval record.
           pattern: '^irb\.[A-Za-z0-9_-]+$'
           examples:
             - value: irb.mount-sinai-001
       slots:
         - AccessRequirementKey
         - StudyKey
         - irbProtocolNumber
         - irbName
         - irbApprovalStatus
         - irbApprovalDate
         - irbExpirationDate
         - irbAssociatedProjects
   slots:
     irbProtocolNumber:
       description: >-
         The IRB's own protocol or registration number for this approval, as
         assigned by the reviewing board.
       required: true
     irbName:
       description: >-
         The name of the reviewing IRB or Ethics Review Board (e.g. "Mount
         Sinai IRB").
       required: true
     irbApprovalStatus:
       description: The current status of this IRB approval.
       range: IRBApprovalStatusEnum
     irbApprovalDate:
       description: The date this IRB approval was granted.
     irbExpirationDate:
       description: The date this IRB approval expires, if applicable.
     irbAssociatedProjects:
       description: >-
         Synapse Project id(s) this IRB approval covers directly, for cases not
         already reachable through a linked Study record. Provide multiple
         values as a comma-separated list.
       multivalued: true
       pattern: '^syn\d+$'
   enums:
     IRBApprovalStatusEnum:
       permissible_values:
         Approved: {}
         Pending: {}
         Expired: {}
         Withdrawn: {}
   ```
   `AccessRequirementKey`/`StudyKey` are reused (not reinvented) for the
   IRB→AR and IRB→Study back-references, the same bidirectional pattern
   `Study.yaml` already uses for `AccessRequirementKey` (line 33). Mixing in
   `ContributionMixin` (`linkml/mixins.yaml:1011-1018`, explicitly documented
   as factored out "so any class that later needs the same fields reuses it
   instead of duplicating") gives curator-provenance tracking (`contributorName`,
   `contributionDate`) for free — no new mixin needed. `IRB` does **not** mix in
   `GovernanceMixin`: an IRB approval record isn't itself a data-governed
   entity, so it has no `dataUseModifiers` of its own.

5. Add `- irb` to `linkml/governance_duo.linkml.yaml`'s `imports:` list,
   alongside `access_requirement`/`resource`/`schema`/`study` — this is what
   makes `make json-schemas`, `make owl`, and `make docs` pick the new class up
   automatically; no other file needs to reference it directly.

6. New worked examples: `linkml/examples/irb.example.yaml` /
   `docs/example_instances/IRB-001.yaml` (identical content, matching the
   existing `Study-001.yaml`/`study.example.yaml` duplication), and a new
   `linkml/examples/access_requirement_two_irbs.example.yaml` /
   `docs/example_instances/AccessRequirement-003-two-irbs.yaml` demonstrating
   the actual answer to the original question:
   ```yaml
   id: access_requirement.201
   contributorName: Jane Doe
   contributionDate: "2026-09-28"
   StudyKey: [study.mc2-jax-5xfad]
   entityIdList: [syn12345678]
   dataUseModifiers: [DUO:0000021]
   IRBKey: [irb.mount-sinai-001, irb.jax-002]
   ```

**Part B — a typed IRB reference on the graph layer's `Condition`**

7. New slot `approvingIRB` in `linkml/graph/governance.yaml`'s slot
   definitions, immediately after `forStudy` (line 540-543), following the
   exact same treatment (untyped `uriorcurie`, not a typed class range, because
   — like `Study` — the record-layer `IRB` individual it points at is never
   itself asserted/typed in this ABox):
   ```yaml
   approvingIRB:
     slot_uri: gov:approvingIRB
     range: uriorcurie
     description: >-
       The IRB (a record-layer IRB IRI) that approves this condition.
   ```
   Add `approvingIRB` to `Condition`'s `slots:` list (line 193-198, alongside
   `dataUseTerm`/`diseaseContext`/`conditionDetail`/`description`).

   This — not a change to `IRBRequirement` — is the graph-layer fix for two
   IRBs on one dataset: two `Condition` instances, both `dataUseTerm:
   DUO:0000021`, differing only in `approvingIRB`, both attached to the same
   `AccessRequirement` (or `IRBRequirement`) via `hasCondition`. `ConditionShape`
   is `sh:closed true` (`shapes/governance.shacl.ttl:299`), so without this
   step a `Condition` carrying `gov:approvingIRB` would fail validation even
   though `hasCondition` itself already permits multiple `Condition` instances
   — the schema addition is what unlocks the mechanism that's already
   structurally present.

8. Regenerate the graph-layer TBox/SHACL (`make graph-tbox`,
   `make graph-owl-profile`) so `shapes/governance.owl.ttl`/
   `shapes/governance.shacl.ttl` pick up the new `gov:approvingIRB` property
   shape on `ConditionShape` (expected: `sh:maxCount 1; sh:nodeKind sh:IRI`,
   matching `forStudy`'s own generated shape exactly, `shapes/governance.shacl.ttl:610-614`).

9. Extend `linkml/examples/graph/governance_graph.example.yaml`'s `conditions:`
   list with a second `DUO:0000021` Condition and attach both to `govid:ar/42`
   via `hasCondition`:
   ```yaml
   conditions:
     - id: govid:ar/42/condition/DUO_0000007
       dataUseTerm: DUO:0000007
       diseaseContext:
         - http://purl.obolibrary.org/obo/MONDO_0004975
       description: >-
         Disease Specific Research - This data use permission indicates that use
         is allowed provided it is related to the specified disease.
     - id: govid:ar/42/condition/DUO_0000021_mount-sinai
       dataUseTerm: DUO:0000021
       approvingIRB: https://w3id.org/sage-bionetworks/governance-duo/irb.mount-sinai-001
       description: Ethics Approval Required — Mount Sinai IRB.
     - id: govid:ar/42/condition/DUO_0000021_jax
       dataUseTerm: DUO:0000021
       approvingIRB: https://w3id.org/sage-bionetworks/governance-duo/irb.jax-002
       description: Ethics Approval Required — JAX IRB.
   accessRequirements:
     - id: govid:ar/42
       ...
       hasCondition:
         - govid:ar/42/condition/DUO_0000007
         - govid:ar/42/condition/DUO_0000021_mount-sinai
         - govid:ar/42/condition/DUO_0000021_jax
   ```
   This is the literal, RDF-level proof that the model now represents two
   distinct IRB approvals on one dataset's Access Requirement.

10. Documentation touch-ups: `docs/graph-design.md` section 4 ("The model")
    and `docs/linkml-model.md`'s class inventory get one sentence each noting
    the new `IRB` record-layer class and `Condition.approvingIRB`. No
    structural rewrite — these are additive facts, not a change to the four-
    layer design already documented.

Explicitly out of scope

- **Policy Fabric wiring.** `linkml/policy_fabric_bindings.yaml`'s
  `ethics-approval-required` binding for `DUO:0000021` currently has
  `referenceValueKeys: []` (pure credential-chain check). Teaching that
  binding to check a specific `IRBKey`/`approvingIRB` value would be a natural
  follow-on but belongs to Policy Fabric's own binding file and operational
  model (`docs/policy-fabric.md`) — not required to answer either of the two
  questions this plan addresses, and not touched here.
- **A graph-layer `IRB` Node class** (mirroring `Program`/`Site`). Not needed:
  `approvingIRB` as an untyped `uriorcurie`, exactly like `forStudy`, is
  sufficient, and keeps this change additive rather than introducing a second
  place (a graph node) to keep in sync with the record-layer `IRB` class.
- **Making `IRBRequirement`'s `forStudy`/`scopedToProgram`/`scopedToSite`/
  `extendsTemplate` multivalued.** The two-IRB case is handled at the
  `Condition` level (one `AccessRequirement`/`IRBRequirement`, two `Condition`
  instances), not by widening `IRBRequirement`'s own single-valued scoping
  slots. If a future case needs one IRB requirement scoped to multiple
  programs/sites simultaneously (a different question from "two IRBs approve
  one dataset"), that's a separate plan.
- **Restructuring `dataUseModifiers` itself** (e.g. turning it from a flat enum
  list into inlined objects, mirroring the graph layer's `Condition`). The
  additive `IRBKey` companion-slot approach follows the exact precedent every
  other DUO code already uses; a structural rewrite of `dataUseModifiers` would
  be a much larger, breaking change to the curator-facing JSON Schema
  (`json_schemas/AccessRequirement.json`, already live-piloted per
  `plans/synapse_curation_infrastructure.md`) for a problem the companion-slot
  pattern already solves.

Verification plan

- `make json-schemas` — confirm `json_schemas/IRB.json` is generated, and that
  `json_schemas/AccessRequirement.json` (and `Study.json`/`Resource.json`)
  gain exactly one new `allOf`/`if`/`then` conditional (36 total, up from the
  35 `plans/ar_level_duo_annotations.md:157-158` and
  `docs/linkml-model.md:136` cite).
- `make owl shacl` (record layer) and `make docs` — confirm
  `docs/reference/classes/IRB.md` and `docs/reference/slots/IRBKey.md` are
  generated, and no unrelated diff appears in previously-generated reference
  pages.
- `linkml-validate` against the new `linkml/examples/irb.example.yaml` and the
  new two-IRB `AccessRequirement` example — both must validate clean. Also
  confirm the **negative** case: an `AccessRequirement` with
  `dataUseModifiers: [DUO:0000021]` and no `IRBKey` must fail validation (the
  new rule actually firing), the same way the existing 35 rules are already
  exercised.
- `make graph-tbox graph-owl-profile graph-validate` — confirm
  `shapes/governance.owl.ttl`/`shapes/governance.shacl.ttl` regenerate with
  only the expected new `gov:approvingIRB` property (on `ConditionShape`) and
  no other diff, and that the extended `governance_graph.example.yaml` (two
  `DUO:0000021` Conditions on one `AccessRequirement`) validates with
  `Conforms: True`.
- `git diff` on every regenerated artifact (JSON Schemas, OWL, SHACL, docs) —
  confirm the diff is limited to the intended additions, same discipline
  `plans/access_requirement_reference_class.md`'s verification plan used.
- `make validate-all` — full regression pass, must stay green.

Report

Once implemented, report the same way
`plans/access_requirement_reference_class_report.md` reports on
`plans/access_requirement_reference_class.md`: what changed, exact
verification command output (including the negative-case rule check and the
two-IRB SHACL validation), and anything left open (e.g. whether Policy Fabric
wiring is wanted as a follow-on).
