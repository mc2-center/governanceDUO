# Model refactor: report

Plan: `plans/model_refactor.md`. R1–R6 approved 2026-09-23.

## Phase 0: golden baseline and spike

### Golden baselines (`tests/golden/`)

The governance export, derivation-policy export and offline sync output, frozen
at `caa1590`. See `tests/golden/README.md`.

Regenerating the provenance example RDF along the way reordered its blank-node
`prov:Usage`s, so serialization is nondeterministic. The files were restored
rather than committed. This confirms the plan's all-IRI rule for Phase 2: blank
nodes also duplicate on every Neptune reload.

### Spike (`plans/model_refactor_spike/`)

Throwaway code that proves the risky parts. Phases 1 and 3 reimplement it
properly.

| # | Question | Result |
|---|---|---|
| 1 | Can owlgen emit enums as SKOS vocabularies? | **Yes.** `skosgen.py` subclasses `OwlSchemaGenerator.add_enum` for enums marked `implements: [skos:Concept]`, the same marker style as the existing `implements: [rdfs:Literal]` for literal enums. It writes a concept class `⊑ skos:Concept`, a `<Enum>Scheme`, and `prefLabel`/`notation`/`definition`/`inScheme`/`hasTopConcept`. A value shared by two enums (`gov:Approved`) sits in both schemes. A value's `implements: [acl:Read]` becomes `rdfs:subClassOf acl:Read` (a WAC mode). |
| 2 | Is WAC-mode punning (class + concept individual) OWL 2 DL? | **Yes.** The TBox merged with the instance data is in profile (ROBOT 1.9.8). The TBox alone reports only undeclared `skos:` annotation properties and the external classes `skos:Concept` and `acl:Control`, which `build_owl.py`'s existing declaration pass will cover. |
| 3 | Does pySHACL stay fast on SKOS vocabularies? | **Yes.** Fixture: 0.01 s. A bogus `acl:mode` is rejected. 5,000 authorizations (30k triples): 1.4 s. `shaclgen` checks vocabulary slots with `sh:in` over the concept IRIs, so the data doesn't need to restate concept types. |
| 4 | Can `RDFLibDumper` write full-IRI principals? | **Yes.** An identifier slot of range `uriorcurie` holding `https://www.synapse.org/Profile:<id>` becomes the subject. Values are written as concept IRIs and `datetime` as `xsd:dateTime`. This removes the blocker behind the dropped emitter consolidation. |
| + | Can a SPARQL projection satisfy the pinned authorizer query? | **Yes.** `authorizer_v1.rq` and `authorizer_v1_teams.rq`, run over the canonical graph, give the pinned `authorize_query.rq` Direct grants on the benefactor and Inferred ones on the descendant, with `ACCESS` only where `DOWNLOAD` is granted. A team member gets the team's permissions (READ only) with the same binding type. |

### Things Phase 1 has to handle, found by the spike

- **Shape names:** `shaclgen` names shapes by class IRI, which would declare
  shapes inside other vocabularies (`acl:Authorization a sh:NodeShape`,
  `vcard:Group a sh:NodeShape`). Shapes need their own namespace, as the plan's
  Phase 4 says; moved into Phase 1.
- **Identifier slot:** it leaks into the OWL (`gov:iri`, with a max-cardinality
  restriction) and into the SHACL. It needs the same suppression the current
  build applies to `id`.
- **Missing ranges:** vocabulary-valued slots get no `rdfs:range`. Repair 1 in
  `build_owl.py` already adds induced ranges; it must treat a vocabulary enum as
  its concept class.
- **Tree-root container:** `RDFLibDumper` writes it as a blank node. The emitter
  should dump the top-level objects instead of the container.
- **ROBOT jar:** `tools/robot.jar` isn't present locally (it's fetched by
  `make`). The spike used sagebrain-model's copy of the same version, 1.9.8.

### Verification

No repo code changed, and `validate-all` isn't affected. The spike checks above
were run by hand from the spike directory.

## Phase 1: graph-layer schema and SKOS vocabularies

### What was added

| File | What it is |
|---|---|
| `linkml/graph/vocabularies.yaml` | The layer's vocabularies. Six SKOS ones (`implements: [skos:Concept]`): Permission (Synapse's 18 ACCESS_TYPEs, each also `⊑` a WAC mode), ApprovalStatus, SubmissionState (sharing `gov:Approved`), AccessRequirementType, DataTier (with `rank`), DerivationReviewStatus. Two class-valued ones (`implements: [owl:Class]`): AgentClass (`foaf:Agent`, `acl:AuthenticatedAgent`) and DataUseTerm (23 DUO terms, plus DUOPlus1–7 as classes `⊑ DUO:0000017`). |
| `linkml/graph/governance.yaml` | Every graph class and slot under `https://w3id.org/synapse/governance#` (R1), including the five predicates the hand TBox had with no slot, `ControlLabel` and `DerivationReview`, `acl:Authorization` (R4), `vcard:Group` teams with `vcard:hasMember`, `gov:benefactor`/`gov:parent`, `gov:requiresAR` (R6), one AR node for record and graph (R5), and `gov:Approval`. A `GovernanceGraph` container bundles nodes for examples and emitters. |
| `scripts/build_graph_tbox.py` | Runs owlgen and shaclgen, then applies the layer's conventions (see its docstring) → `shapes/governance.owl.ttl`, `shapes/governance.shacl.ttl`. |
| `scripts/graph_rdf.py` | The one path from graph-layer objects to Turtle. Dumps the container's members, and refuses blank nodes. |
| `linkml/examples/graph/governance_graph.example.yaml` → `rdf/governance_graph.ttl` | The pre-refactor examples' facts in the new model, including provenance and a derivation review. |
| `scripts/check_graph.py` | 8 deliberate defects, each caught by its intended constraint (sh:in, sh:xone ×2, sh:closed, sh:minCount, sh:class, sh:in, sh:datatype). Plus TBox conventions: SKOS completeness, no axioms on non-`gov:` terms, labels, blank nodes only in domain unions, no legacy namespace. Also checks that `to_rdf` refuses a node with no IRI. |
| Makefile | `graph-tbox`, `graph-example-rdf`, `graph-validate`, `graph-owl-profile`, all in `validate-all`. `linkml-lint` covers the graph schema. The drift check covers the new artifacts: TBox byte-exact, shapes and example graph-equal, `linkml/examples/graph/rdf` as a generated directory. |
| `scripts/validate_examples.py` | Validates examples under `linkml/examples/graph/` as `GovernanceGraph` against the graph schema. |

### Decisions made while implementing

- **Sequencing:** Phase 1 runs *beside* the old pipeline rather than replacing
  it. The old builders still write the old graph, so the hand TBox and shapes,
  `provenance_layer.shacl.ttl`, `GrantPermissionEnum` and `enum-sync-check` stay
  until Phase 2 swaps the builders. So do the record OWL's assertions on
  `prov:` classes and `DATA_TIER_RANK`, and the record enums that duplicate the
  graph vocabularies.
- **Two schema files, not four.** The plan's split (vocabularies, access,
  requirements, provenance) would recreate the import cycle that forced the AR
  stub class: `SynapseEntity.requiresAR` needs `AccessRequirement`, and ARs name
  entities. Classes are one module; the vocabularies are the other.
- **The "not ours" rule, made general.** The OWL declares terms outside `gov:`
  (acl, vcard, foaf, prov, DUO, skos) and makes no axioms about them. owlgen's
  cardinality and range restrictions aren't kept at all: constraints live in
  SHACL, which is sagebrain's split. Every `gov:` property gets `rdfs:domain`
  (a union when shared) and `rdfs:range`. The closed shapes come from the same
  schema, so these can't contradict the data, which is what the old
  hand-domain bugs did.
- **Binding type is gone from the canonical graph.** The graph records
  `gov:benefactor` and `gov:parent`; Direct/Inferred is the projection's to
  compute (decision 2 lands there). `SourceSystemEnum` is dropped for the same
  reason; the projection writes its constant.
- **IRIs** (R2, R3): entities `syn:`, users `synuser:` (`…/Profile:`), teams
  `synteam:` (`…/Team:`), minted nodes `govid:<kind>/<id>`. The approval is keyed
  by Synapse's AccessApproval id. Patterns on IRI-valued slots accept the CURIE
  (linkml-validate sees the YAML) or the full IRI (SHACL sees the graph).
- **Open items closed:** `DUO:0000017` (abstract) and `Pending Annotation` (an
  absence, not a term) aren't data-use terms. The shared `gov:APPROVED` is one
  concept in two schemes, with one definition; the builder fails if a shared
  concept's descriptions ever differ. The review's input labels are nodes, not
  inlined.
- **Dropped:** `Condition.conditionType` (the DUO shorthand, derivable from the
  term) and the GA4GH visa as a `close_mapping`, since it has no RDF IRI; the
  Approval description names it instead. `createdBy`/`modifiedBy` are User
  IRIs, not raw ids.
- **To verify in Phase 2:** the PUBLIC (273949) and AUTHENTICATED_USERS
  (273948) principal ids in AgentClass's descriptions, against Synapse.

### Generator fixes found along the way

- The shape renaming first rewrote object positions too, turning
  `sh:class vcard:Group` into `sh:class shape:TeamShape`. Shapes are now
  renamed only as subjects and `sh:node` targets.
- shaclgen drops `exactly_one_of`, so `build_graph_tbox.py` adds the
  `sh:xone` itself.
- shaclgen gives abstract classes closed shapes (`foaf:Agent` would have been
  targeted), so those are removed.
- shaclgen writes `sh:ignoredProperties` in set order, so it's sorted. The
  TBox, shapes and example RDF are byte-identical over three rebuilds.
- `skos:ConceptScheme` needed declaring. Every class used as an `rdf:type` or
  `rdfs:subClassOf` object is now declared.
