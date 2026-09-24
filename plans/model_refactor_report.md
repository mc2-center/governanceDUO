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

### Verification (on `d8a9db7`)

- `make validate-all`: exit 0. That includes the new `graph-validate` and
  `graph-owl-profile`: the example conforms, all 8 defects are caught, and the
  TBox is OWL 2 DL both alone and merged with the example graph.
  `linkml-validate-examples` now covers 30 records (was 29).
- `make artifact-drift-check`: all 262 generated artifacts match HEAD (was
  259; the graph TBox, shapes and example RDF are new).
- `make sagebrain-contract-check`: all four parts pass. The old artifacts it
  reads are unchanged.
- The old pipeline's regenerated SHACL and example RDF still reorder their
  blank nodes on each build. Graph-equal, so they were restored rather than
  committed. The graph layer's own outputs have no blank nodes, apart from the
  TBox's domain unions, which are canonicalized, and are byte-stable.

## Phase 2: derivation builder, projections, canonical example, retire the old pipeline

Plan: `plans/model_refactor_phase2_handoff.md` (steps 1-5). Commits `5046914`
(step 1, plus the carried-forward emitter work), `c88e538` (step 2),
`481857c` (step 3), `2df3fba` (docs), `c42579b` (step 4), `3b1f247` (a
Turtle/SPARQL CURIE syntax fix to the step-4 sagebrain-contract rewrite).

### Step 1: derivation builder on the canonical graph

`scripts/build_derivation_policy.py` rewritten against `--graph`/`--extra-graph`
(repeatable), replacing `--provenance-graph`/`--governance-graph`/
`--access-requirement-dir`. An entity's Access Requirements are its own
`gov:requiresAR` plus every ancestor's over `gov:parent+` (the graph layer
doesn't materialize inheritance the way the old one did). AR tiers come off
the AR node's `gov:dataTier` concept via the DataTier enum's `meaning`s
(`Unclassified` when absent); `DATA_TIER_RANK` is gone, ranks come from
`GraphBuilder.rank()`. Derivation edges are `projections/provenance.rq`'s
`prov:wasDerivedFrom` plus its declared `rdfs:subPropertyOf*` properties.
`compute_control_labels`/`compute_derivation_reviews` keep their original
logic, as the plan required.

`linkml/examples/derivation_policy/fixture/` converted to the new namespace:
real IRIs, no blank nodes, AR tiers on the AR nodes directly (the
`access_requirements/` curated-record bridge is gone).
`scripts/check_derivation_policy.py` rewritten with 13 assertions (the
original 11, the new-namespace SHACL-validation assertion replacing the old
domain/range check, plus a Step 2 addition below) and a review count of 4.

### Step 2: projections (moved up from Phase 3)

`projections/authorizer_v1.rq` and `authorizer_v1_teams.rq`, from the Phase 0
spike: per-entity `gov:AccessGrant`s (Direct on the benefactor, Inferred on a
materialized descendant), `gov:hasAccessRequirement` over `gov:parent*`,
`gov:hasApproval` for unexpired Approved approvals, built in the old namespace
to match the infra `fc6de51` contract. Team grants stay in
`authorizer_v1.rq` itself (keyed by the team's own principal id, the existing
contract); `authorizer_v1_teams.rq` is the separate, `TEAMS=1`-gated
flattening to per-member grants.

`scripts/project.py` runs a projection over given graphs plus the graph
TBox, binding `--as-of` through SPARQL `initBindings` (never spliced into
query text), and reports how many `acl:agentClass` authorizations
`authorizer_v1` can't express.

New `scripts/check_projections.py`, replacing the retired
`check_approval_expiry.py`: a golden diff against `tests/golden/governance_graph.ttl`
restricted to authorizer-relevant facts (`Inherited`->`Inferred` and extra
`hasAccessRequirement` on an AR's own subject are the only allowed
differences), approval expiry, team-member-only-via-teams-projection, and
descendant-grant-is-Inferred. Each assertion was confirmed able to fail by
breaking its projection/script and restoring.

`check_derivation_policy.py` gained a 12th assertion (syn70000019, fixture
data): an AR attached to a parent via `gov:requiresAR` reaches a child's
ControlLabel through `gov:parent` -- Step 1's ancestor walk, untested until
then.

### Step 3: the canonical example is the governance export

`make governance-graph` now writes `governance_graph_export/governance_graph.ttl`
from `linkml/examples/graph/*.example.yaml` via `scripts/graph_rdf.py`, not
`scripts/build_governance_graph.py`'s hand-written examples.
`governance-graph-validate` and `sync-governance-graph-validate` validate
against the one generated graph TBox and shape set instead of the hand-written
`shapes/governance_graph.*.ttl`.

### Step 4: retire the old pipeline

Deleted: the pre-refactor pipeline's schema (`linkml/governance_graph.yaml`,
`linkml/provenance.yaml`, `ControlLabel`/`DerivationReview` from
`linkml/derivation_policy.yaml` -- `DerivationRule` stays, record layer),
shapes (`governance_graph.owl.ttl`, `governance_graph.shacl.ttl`,
`provenance_layer.shacl.ttl`), scripts and Makefile targets
(`build_governance_graph.py`, `check_enum_sync.py`/`enum-sync-check`,
`check_domain_range.py`/`domain-range-check` -- SHACL over the one generated
TBox does their job now), and the old examples (their facts already live in
the canonical example).

Record enums moved onto the graph vocabularies: `mixins.yaml` imports
`graph/vocabularies`; `AccessTypeEnum`/`AccessRequirementConcreteTypeEnum`/
`DataTierEnum` are replaced by the graph's
`Permission`/`AccessRequirementType`/`DataTier`. `build_owl.py`'s
`GovernanceOwlGenerator` now skips full per-value generation for any
vocabulary-marked enum and declares only a bare class -- the same "not ours to
give" treatment already used for `prov:`/DUO: terms, since those SKOS
vocabularies are owned and fully declared once, by `shapes/governance.owl.ttl`.
The record OWL no longer asserts on `prov:` at all (Activity/Usage moved to
the graph layer in Step 1); `check_prov_alignment.py` now checks
`shapes/governance.owl.ttl` by default.

`convert_examples_to_rdf.py`: record examples only (AccessRequirement, Study,
DerivationRule), subjects minted via `graph_iris.record_iri()` (the
`graph_curie` stopgap is gone) -- a curated AccessRequirement lands on its
graph node's IRI (`.../ar/<n>`, R5).

`check_sagebrain_contract.py` rewritten against the single graph TBox/shapes
(see "Stopped on" below for its current live-checkout result).
`tests/sagebrain_contract/governance_binding.ttl` moved to the new namespace;
`3b1f247` fixed a syntax error in it and in the check (`govid:ar/42` isn't a
valid CURIE local name in either Turtle or SPARQL -- `/` isn't allowed
unescaped -- both now use the full IRI).

Makefile: `owl-profile` no longer merges two TBoxes; `graph-owl-profile` also
merges the derivation output and the projections' inputs into its ABox check,
replacing the deleted `owl-profile-abox`. `check_release.py` checks the
record and graph layers against their own independent versions
(`--graph-version`). `check_artifact_drift.py` and `prepare_doc_examples.py`
updated for the deleted files/classes. `docs/reference` regenerated;
`docs/knowledge-graph.md` had three relative links to now-deleted class pages
un-linked (`mkdocs build --strict` was failing on them; no other prose
changed).

### Decisions taken while implementing

- **Stopped on, per spec:** `DataUseModifierEnum` is *not* folded into the
  graph's `DataUseTerm`. "Pending Annotation" and `DUO:0000017` are still
  needed for curation -- left as their own record-layer enum, unchanged, per
  the handoff's stop condition.
- Binding type (Direct/Inferred) stays out of the canonical graph and the
  derivation builder's own labels; it's purely a projection concern
  (`authorizer_v1.rq`), matching Phase 1's decision.
- `check_projections.py` replaces `check_approval_expiry.py` rather than
  extending it, since the golden diff and expiry check now share one fixture
  and one graph-shaped comparison instead of two.

### Verification (on `3b1f247`, working tree clean)

- `make validate-all`: exit 0. `check_derivation_policy.py`: 13 assertions
  pass. `project.py`: 10 triples written to `authorizer_v1.ttl`, 0
  `acl:agentClass` authorizations `authorizer_v1` can't express.
  `check_infra_contract.py`: 3 principals on `syn10081783`.
  `check_projections.py`: golden diff, approval expiry, team-member and
  descendant grants all pass. `validate_examples.py`: 9 examples plus fixture
  records conform, including the DUO rules. `check_graph.py`: 8 defects
  caught. `build_derivation_policy.py` over the canonical example: 5
  ControlLabels (5 entities), 0 DerivationReviews. Both `robot
  validate-profile` calls (the graph TBox alone, and merged with every
  canonical ABox -- the example, derivation output and `authorizer_v1.ttl`)
  report OWL 2 DL. The old pipeline's regenerated `governance_duo.shacl.ttl`
  again reordered its blank nodes (graph-equal); restored, not committed.
- `make artifact-drift-check`: all 167 generated artifacts match HEAD (was
  262 after Phase 1; Step 4 deleted the old pipeline's generated files).
- `make sagebrain-contract-check SAGEBRAIN_MODEL=/Users/obanks/sagebrain-model`:
  **2 of 4 parts fail.** `OWL 2 DL (union)` and `prov: types match
  sagebrain's prov.ttl` pass. `SHACL (joined worked example)` and
  `ControlLabel reaches sagebrain Association` fail.

  **Root cause, diagnosed, not a governanceDUO defect:** sagebrain-model
  vendors governanceDUO's provenance terms as a MIREOT extract
  (`ontology/imports/governance_layer.ttl`, `ontology/shacl/governance_layer.shacl.ttl`)
  pinned to governanceDUO commit `240a1628a14f6f08d6e86444030ab20beddc5b4d`
  and sourced from `shapes/governance_duo.owl.ttl` -- a commit that predates
  even Phase 1's R1 namespace move. Its vendored `UsageShape` and
  `examples/pipeline_provenance.ttl` still use
  `https://sagebionetworks.org/governance/wasExecuted` etc., not the current
  `https://w3id.org/synapse/governance#`. Two effects:
  - Merging that stale shape graph with the current
    `shapes/governance.shacl.ttl` gives `prov:Usage` two closed shapes in two
    namespaces, so pySHACL rejects the joined example's Usage nodes for
    having (correct, new-namespace) `gov:name`/`gov:url`/`gov:wasExecuted`
    properties the stale shape doesn't know about.
  - `build_derivation_policy.py` looks for `gov:wasExecuted` under the new
    namespace, finds none in `pipeline_provenance.ttl` (old namespace), so
    the derivation chain never reaches the pipeline's output, and
    `association:apoe-expr-samp01` gets no ControlLabel.

  The equivalent path is exercised and passes entirely within this repo:
  `check_derivation_policy.py`'s fixture already asserts a sagebrain-shaped
  Association inherits a label through `sagebrain:derived_from` (a declared
  sub-property of `prov:wasDerivedFrom`). This is specifically the live
  sagebrain-model checkout's vendored copy being stale relative to Phase 1 and
  Phase 2. **Fix is on sagebrain-model's side:** re-run its `scripts/import.sh`
  against current governanceDUO HEAD to refresh
  `ontology/imports/governance_layer.ttl`, `ontology/shacl/governance_layer.shacl.ttl`,
  and update `examples/pipeline_provenance.ttl` to the current namespace and
  `gov:name`/`gov:url` Usage shape. Per the handoff's stop condition (a change
  to sagebrain-model is needed), this was not touched from here.

  **Follow-up, resolved on `41c17e1` (this repo) and sagebrain-model's
  `governance-layer-import` branch:** re-checking against a re-realigned
  sagebrain-model checkout (its `plans/governance_layer_realignment.md`,
  re-pinning `scripts/import.sh` to this repo's current HEAD) surfaced a real
  regression the diagnosis above didn't cover, in this repo's own schema: the
  Phase 1/2 refactor of `Usage` and `Activity`
  (`linkml/graph/governance.yaml`) had silently dropped the pre-refactor
  hand-written `sh:xone` (exactly one of an entity reference or a url+name
  pair) and `sh:minCount 1` on `Activity.generated`/`qualifiedUsage` --
  neither this repo's own fixtures nor `make validate-all` exercised the
  "wrong branch" cases that catch it, only the cross-repo joined example did.
  Fixed in three commits, in order:
  - `060308d` restores `exactly_one_of`/required `generated`/`qualifiedUsage`
    on the LinkML classes (`add_exactly_one_of()` in
    `scripts/build_graph_tbox.py` already supported emitting the `sh:xone`;
    it just wasn't declared on these classes after the refactor);
  - `41c17e1` fixes `add_exactly_one_of()` itself: it emitted each
    alternative's own `sh:minCount 1` but no `sh:maxCount 0` on the *other*
    alternative's slots, so a node satisfying one branch still conformed
    while also setting the other's slots (a Usage with both `prov:entity` and
    `gov:name` passed). Mutual exclusion is now generated, matching the
    pre-refactor hand-written shape;
  - `04825a2` fixes the sagebrain-contract fixture itself (a second, unrelated
    gap the joined example exposed once the namespace mismatch stopped
    masking it): `tests/sagebrain_contract/governance_binding.ttl`'s
    `syn:syn26999999` needed its own `gov:benefactor` to satisfy
    `shape:SynapseEntityShape`'s closed shape, the same pattern
    `syn:syn27000001` already had.

  With those three commits here and sagebrain-model's re-pin,
  `make sagebrain-contract-check SAGEBRAIN_MODEL=/Users/obanks/sagebrain-model`
  passes all four parts again (re-verified on `41c17e1`, no fixture or schema
  changes needed beyond the three commits above). `make validate-all` and
  `make artifact-drift-check` still pass unchanged (same counts as above;
  `shapes/governance.shacl.ttl` grew from 1294 to 1337 triples with the
  restored/strengthened constraints).

### Unverified against live Synapse

Per the handoff's step 5, not exercised against a live Synapse endpoint in
this phase, only against `scripts/check_sync_governance.py`'s recorded
fixtures:
- the `/teamMembers` page shape (assumed `PaginatedResults<TeamMember>`,
  `scripts/sync_governance_graph.py`'s own docstring flags the assumption);
- the `/entity/{id}/path` root handling;
- the `/accessApproval/search` request/response field names.
