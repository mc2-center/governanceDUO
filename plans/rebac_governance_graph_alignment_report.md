# Report: Align the governance graph pipeline with sagebrain-infra PR #54's ReBAC concept

## Summary

Implemented the additive changes from `plans/rebac_governance_graph_alignment.md`:
surfaced `GovernanceMixin`'s existing DUO-condition data as first-class `gov:Condition`
graph nodes, reachable from the `gov:AR-<n>` stub via a new `gov:hasCondition` edge —
closing the one real, already-partially-built gap the sagebrain-infra PR #54 review
comment pointed at. `authorize.py`'s live SPARQL contract was left untouched throughout
(confirmed, see Verification).

## Schema changes (`linkml/governance_graph.yaml`)

- New `Condition` class (`class_uri: sagegov:Condition`, not `is_a: BaseEntity` — like
  `DataAccessSubmissionStatus`, it has no independent Synapse identifier; it's keyed
  structurally by `(AccessRequirement, duoCode)`), with slots:
  - `conditionType` — the DUO code's `duo_shorthand` annotation (e.g. `"GRU"`, `"DS"`)
    for the 24 real DUO codes; the bare `DataUseModifierEnum` key (e.g. `"DUOPlus1"`)
    for the 7 Sage-local extensions, which have no `duo_shorthand`.
  - `duoCode` — the real DUO CURIE (range `DataUseModifierEnum`), absent for DUOPlus
    extensions.
  - `description` — sourced directly from `DataUseModifierEnum.permissible_values[code]`'s
    own `description:` text.
  - `conditionDetail` — multivalued; zero or more companion-slot values, since
    `GovernanceMixin.rules` is genuinely many-to-many (e.g. `DUO:0000026` alone has 4
    postcondition slots; `requiredAgreementDocumentId` is itself the postcondition for
    4 different codes) — verified directly against the schema's real `rules:` block
    before finalizing this design, not assumed.

## Script changes (`scripts/build_governance_graph.py`)

- New `--access-requirement-example` CLI arg (default
  `linkml/examples/access_requirement.example.yaml`) — deliberately separate from
  `--examples-dir`, since it bridges a *different* source of truth (the real
  `access_requirement.yaml` `AccessRequirement` instance, not a governance-graph-only
  stub example).
- New `add_access_requirement()`: for each `dataUseModifiers` entry on the loaded
  instance, mints one `gov:Condition` individual on the existing `gov:AR-<n>` node
  (from `add_access_requirement_association()`). Reads
  `_schemaview.get_class("GovernanceMixin").rules` at runtime (real `ClassRule`
  objects — API shape confirmed directly against a live `SchemaView` before writing
  any code) and iterates **every** matching rule per DUO code, not just the first, to
  correctly handle the many-to-many shape.
- **Deviation from the plan's literal wording, required by an import-cycle
  constraint**: the plan said to declare `hasCondition` "on `AccessRequirement`
  (declared in `access_requirement.yaml`)". That's not possible as written:
  `access_requirement.yaml` does not import `governance_graph.yaml` (it's the other
  way around), so a slot declared there could never range over `Condition`. Instead,
  `gov:hasCondition` is a bare derived-convenience triple in the script — exactly the
  same treatment as the pre-existing `gov:hasACL`/`gov:hasAccessRequirement` (also
  undeclared in any LinkML `slots:` list). Same intent as the plan, adjusted
  implementation.

## Shapes (`shapes/governance_graph.{shacl,owl}.ttl`)

- `shacl.ttl`: new `gov:ConditionShape` (`conditionType` required/single,
  `duoCode`/`description` optional/single, `conditionDetail` unconstrained
  cardinality); added `gov:hasCondition` to the existing `AccessRequirementShape`.
- `owl.ttl`: new `gov:Condition` class declaration; new `gov:hasCondition`
  (ObjectProperty, domain `AccessRequirement`, range `Condition`) and
  `gov:conditionType`/`gov:duoCode`/`gov:description`/`gov:conditionDetail`
  (DatatypeProperties, domain `Condition`) declarations.

## Docs

- `docs/governance-graph-sync.md`: added a `Condition` row to the Synapse-source
  table (honestly marked as "not sourced from Synapse directly yet"), and a 5th open
  design question (Program/Site/template reuse) with what was actually checked
  (Synapse's `AccessRequirement` REST object has no template/Program/Site field;
  `access_requirement_JSON/README.md` has no such language either) and where to look
  next (tracked in `plans/governance_graph_open_questions.md`).
- `docs/knowledge-graph.md`: updated the "what's hand-written" bullet list
  (`hasCondition` added alongside `hasACL`/`hasAccessRequirement`, plus a new bullet
  explaining `Condition`'s cross-schema sourcing). Checked its one mermaid diagram —
  pipeline-level (which script produces which file), not class-level — no diagram
  change needed.
- `docs/reference/`, `docs/example_instances/`, `shapes/governance_duo.{owl,shacl}.ttl`:
  regenerated via `make docs`/`make owl`/`make shacl` (umbrella schema now includes
  `Condition`); no hand-editing.

## Tests / verification

All from the plan's own Verification section, run after implementation:

1. `make linkml-lint` — exit 0, 0 errors; only the pre-existing, expected
   `standard_naming` warnings (the new camelCase slots trigger the same category,
   not a new one).
2. `make shacl-validate` — `Conforms: True` (both `shapes/governance_duo.owl.ttl` and
   `linkml/examples/rdf/all_examples.ttl`).
3. `make governance-graph-validate` — `Conforms: True` against the new
   `ConditionShape`/OWL declarations.
4. Grepped the regenerated `governance_graph.ttl` directly: `gov:hasACL`/
   `gov:AccessGrant`/`gov:principal`/`gov:permission`/`gov:bindingType`/
   `gov:hasAccessRequirement` triples are unchanged — `authorize.py`'s live SPARQL
   contract is unaffected.
5. Ran the plan's own smoke query —
   `SELECT ?duo WHERE { gov:AR-42 gov:hasCondition ?c . ?c gov:duoCode ?duo }` —
   returned `DUO:0000007`, confirming the new node is reachable from the existing AR
   stub.

Triple count: `governance_graph_export/governance_graph.ttl` went from 44 to 50
triples (one new `gov:Condition` node — 4 property triples + `rdf:type` — plus the
`gov:hasCondition` edge from `gov:AR-42`).

## Left unchanged (in scope for a separate, tracked follow-up)

- `gov:Approval`/`expiresAt` (plan's original point 3) and the `Program`/`Site`/
  `AccessRequirementTemplate` question (point 4) — both intentionally not built here;
  see `plans/governance_graph_open_questions.md`.
- No PR #54 comment was posted (explicitly reviewed out of the plan).
