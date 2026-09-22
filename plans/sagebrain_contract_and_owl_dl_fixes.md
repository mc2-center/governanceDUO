# sagebrain-model contract and OWL 2 DL fixes

## Context

The governance graph is meant to be a layer of the graph defined in
sagebrain-model: loaded into the same Neptune store, joined on the same IRIs,
and queried by sagebrain-infra's authorization code. This plan brings this repo
in line with that goal. A review of `kg-conversion` against sagebrain-model's
`provenance-features` branch was run under the standing review and
implementation directives (plans with companion reports, granular commits, no
silent workarounds, and an expert-framed review before any PR, including the
OWL 2 DL check sagebrain-model added after its PR #3). sagebrain-model pins this
repo at `abf8c9f`; the only changes since then are LICENSE/CODEOWNERS, so the
pin is accurate. A follow-up pass checked the same graph against sagebrain-infra
(`origin/policy-engine`, `fc6de51`).

### What's broken in this repo

**The provenance pipeline doesn't work end to end.**

- `scripts/sync_provenance_graph.py` can't produce output. Running
  `build_activity()` offline against a fake Synapse Activity fails in
  `RDFLibDumper` with `ValueError: Unknown CURIE prefix: @base`. The cause is the
  bare `activity.<n>` id (`:99`), the same dumper limit
  `convert_examples_to_rdf.py` already handles with `to_curie()`. The script
  docstring's "confirmed empirically" claim is wrong.
- `Activity.generated` and `Usage.entity` serialize as relative IRIs
  (`<syn30000001>`). These resolve against whatever file is being parsed
  (`file:///…/syn30000001`), so they never match the governance graph's
  `syn:syn…` (`https://www.synapse.org/Synapse:`) nodes. They also can't be
  loaded into Neptune. `build_derivation_policy.py`'s `local_id()` (`:75`) works
  around this by comparing trailing names only. That workaround was documented
  in the report, but not flagged for approval.
- Synapse lets one Activity have several outputs. This was verified against
  Synapse's OpenAPI spec (`rest-docs.synapse.org/rest/openapi/openapispecification.json`):
  `GET /activity/{id}/generated` returns a paginated list of references, and
  `PUT /entity/{id}/generatedBy?generatedBy=<activityId>` attaches an existing
  Activity to another entity. The sync script builds a graph per entity and
  merges them. That gives one Activity several `prov:generated` values, while
  `generated` is single-valued in `provenance.yaml`, and every `prov:Usage` blank
  node is duplicated once per output. `add_was_derived_from()` also counts
  duplicate adds (it reported 4 for 2 distinct triples).

**`make derivation-policy` writes 0 triples.**

- `emit_control_label()` (`:260`) drops any label with no `dataTier`, and its
  `sourceAccessRequirements` go with it. `syn10081783`, which is bound to AR-42,
  therefore reads as unrestricted downstream. That fails open, and those AR
  bindings are what `plans/prov_integration_an_9-8-26.md`'s question 1
  (access computed from source ARs) depends on.
- The label algorithm was only checked by an uncommitted throwaway test.

**`shapes/governance_duo.owl.ttl` fails the OWL 2 DL profile.**

`robot validate-profile --profile DL` reports 103 property-punning violations
(80 were already on the branch, `5b30a90` added 17, the PROV-O wiring `22f83ee`
added 6), plus about 1,600 undeclared-entity violations. The file doesn't exist
on `main`, so all of them would ship in the PR. `governance_graph.owl.ttl`
passes cleanly. Nothing in the Makefile or CI runs this check. Root causes,
confirmed by rebuilding with changed `OwlSchemaGenerator` settings:

1. `type_objects=True` (the default) types `id`, `synapseId`, the `*Key` slots
   and other pattern-constrained slots as ObjectProperties. Their `xsd:string`
   pattern restrictions then pun them. Also `sagegov:wasExecuted` (boolean)
   comes out as an ObjectProperty.
2. The 35 `rules:` blocks on `GovernanceMixin` (`linkml/mixins.yaml:779`) become
   wrong axioms. In `owlgen.py`'s `add_constraints()`, `is_literal` is `None` in
   rule context, so `equals_string: DUO:0000007` is logged ("ignoring
   equals_string … unable to tell if literal") and dropped. Each rule becomes
   `GovernanceMixin ⊓ ∃dataUseModifiers.xsd:string ⊑ ∃<postcondition>`, meaning
   any AR with any modifier requires every rule's postcondition. These axioms
   cause the remaining 45 puns. No generator option fixes this. gen-shacl
   doesn't translate rules at all; `linkml-validate` is the only enforcer.
3. `use_native_uris=True` (the default) mints `governanceduo:Usage`,
   `governanceduo:wasExecuted` and so on, while the SHACL and all ABoxes use the
   `prov:`/`sagegov:` IRIs from `class_uri`/`slot_uri`. The OWL doesn't describe
   the data it ships with. Setting it to `False` fixes that, but then five `gov:`
   slots are typed differently from the hand-written
   `shapes/governance_graph.owl.ttl`. In each case the builder script
   re-serializes the slot:

   | slot | LinkML today | what the graph builder emits | hand TBox |
   |---|---|---|---|
   | `submittedBy`, `modifiedBy`, `accessorId`→`gov:heldBy` | `integer` | `gov:principal-<n>` IRI | ObjectProperty → `gov:Principal` |
   | `duoCode` | `DataUseModifierEnum` | `"DUO:0000007"` literal | DatatypeProperty `xsd:string` |
   | `source` | `string` (`Synapse`) | `gov:Synapse` / `gov:SynapseACL` IRI | `rdf:Property` |

   The shared `modifiedBy` slot is also used by `Activity`
   (`provenance.yaml:84`), so the provenance ABox currently emits
   `gov:modifiedBy` as an integer literal, contradicting the hand TBox.

### Where it breaks against the other two repos

**sagebrain-model.**

- Neither this repo's provenance example ABox nor a simulated sync output
  conforms to sagebrain's `ontology/shacl/governance-shapes.ttl`.
- A name is written three different ways: `governanceduo:name` (provenance),
  `gov:name` (governance graph), `rdfs:label` (sagebrain `UsageShape`).
- Activity IRIs differ: `governanceduo:activity.N` here, `syn:activity.*` in
  sagebrain's examples, `gov:activity.N` in its plan.
- **Duplicate ownership.** sagebrain hand-copies `gov:SynapseEntity` and
  re-declares `gov:wasExecuted`/`gov:url`/`gov:entityVersionNumber` in its own
  `ontology/governance/pipeline_provenance.ttl`, because this repo publishes no
  importable release. It also writes its own Activity/Usage shapes, which have
  already drifted from this repo's.
- **No bridge between the two derivation edges.** `sagebrain:derived_from`
  (Association or MaterialSample → `gov:SynapseEntity`) isn't a sub-property of
  `prov:wasDerivedFrom`. The derivation builder here only walks
  `prov:wasDerivedFrom`, so control labels stop at Synapse files and never reach
  sagebrain's knowledge nodes.
- **DUO codes don't join.** sagebrain imports DUO as IRIs
  (`ontology/imports/duo.ttl`); this repo writes DUO codes as strings.
- The union of sagebrain's merged ontology, its governance module and both
  governance TBoxes (built with the new gen-owl settings) has only the five
  conflicts above plus the rule-derived puns. Once those are fixed, it should
  pass DL, but nothing keeps it passing.

**sagebrain-infra** (`src/lambda_rebac/authorize.py`, `src/lambda/query.py`).

- `query.py` runs a query, collects every Synapse id in the results, and calls
  `authorize.py` with `action: "ACCESS"`.
- `authorize.py` queries `gov:hasAccessRequirement`, `gov:hasACL`,
  `gov:AccessGrant`, `gov:principal`, `gov:permission` and `gov:bindingType`. It
  matches principals by a `…principal-<id>` IRI suffix and approves only if a
  grant's permission local name equals the action.
- Running that query and matching logic against
  `governance_graph_export/governance_graph.ttl` for `syn10081783`: AR-42, the
  grant, the binding type and the principal all match. The permission doesn't:
  the grant carries `DOWNLOAD`. So every real check would be denied.
- Synapse has no `ACCESS` permission (its `ACCESS_TYPE` values run from
  CREATE and READ through DOWNLOAD to EXEMPTION_ELIGIBLE). `ACCESS` is
  SageBrain's abstract Cedar action.
- Correction to the earlier review: the literal
  `gov:principal "user:9000001"` / `gov:permission "ACCESS"` pattern is a sketch
  of a future query-rewrite mode in infra's `CLAUDE.md` and
  `docs/governance_hybrid_architecture.md`. It isn't running code.
- `query.py`'s filter only gates results that contain a Synapse id. A query
  returning sagebrain Associations derived from controlled files passes
  unfiltered: the leakage case from the 9-8-26 note.
- Inheritance is compatible: `sync_governance_graph.py` attaches each entity's
  inherited ACL directly to that entity (`bindingType Inherited`), which is what
  `authorize.py` expects.

### Housekeeping

The uncommitted `shapes/*.ttl` diffs contain identical triples in a different
order (gen-owl output isn't stable between runs). `plans/identifier_update.md`
has its report appended inline instead of the `_report.md` companion file this
repo uses.

## Decisions (recorded 2026-09-22)

- **D1, name predicate:** `gov:name` (`sagegov:name`) everywhere, reusing the
  `slot_usage` pattern `governance_graph.yaml` already applies to SynapseEntity
  (`:116`) and Program (`:596`).
- **D2, OWL rule axioms:** strip them from the OWL permanently. `linkml-validate`
  stays the enforcer of the DUO conditional requirements. This is an approved
  deviation from full schema-to-OWL fidelity, documented in `build_owl.py` and
  the README.
- **D3, the five conflicting `gov:` slots:** align the LinkML schema to the
  graph, except `duoCode`.
  - **`duoCode` (revised):** the graph changes instead. `gov:duoCode` points to
    the DUO IRI (`obo:DUO_…`, joining sagebrain's DUO import). DUOPlus1–7 get
    `sagegov:DUOPlusN` IRIs. The hand TBox and builder change to match.
  - `gov:permission` stays an IRI (`gov:DOWNLOAD`) for the same reason.
- **D4, instance IRIs (revised):** graph instances are minted in `gov:`,
  starting with `gov:activity-N`, matching `gov:AR-42`, `gov:principal-N` and
  `gov:grant-…`. `governanceduo:` is kept for schema terms and LinkML record ids.
- **D5, unknown tier:** fail closed. Add `Unclassified` to `DataTierEnum`, ranked
  above `Private`, and always emit the ControlLabel with its
  `sourceAccessRequirements`.
- **D6, graph-facing derivation classes:** `ControlLabel` and `DerivationReview`
  (and the slots they carry) move to `gov:` IRIs, since infra will read them.
  `DerivationRule` stays `governanceduo:`: it's curator configuration, not graph
  content.
- **D7, infra contract:** the exported graph must satisfy `authorize.py` and
  `query.py` as they are. A contract test runs infra's SPARQL against this
  repo's export.
- **D8, `ACCESS` permission:** the builder keeps each Synapse permission and
  also emits `gov:permission gov:ACCESS` on any grant that includes `DOWNLOAD`.
  This fails closed: graph answers expose content derived from files, which
  Synapse gates at DOWNLOAD, not READ.
- **D9, one owner per term and shape:** this repo owns every `gov:` and
  governance-layer term and shape, and publishes them as a versioned release.
  sagebrain-model imports that release instead of keeping copies. sagebrain
  owns the bridge from its own edges into the layer.

## Approach

Each numbered step is one commit, in dependency order. The plan itself is
committed first on its own.

### Phase A: provenance IRIs and sync correctness

1. **Shared graph-IRI helper.** Add `scripts/graph_iris.py`, used by both the
   dump scripts and the builders. It maps a LinkML record to its graph IRI:
   - `Activity` `activity.N` → `sagegov:activity-N` (D4);
   - every other record → `governanceduo:<id>` (today's `to_curie()` behavior).

   `convert_examples_to_rdf.py` switches to it, and its `to_curie()` becomes a
   thin wrapper.
2. **`linkml/provenance.yaml`:**
   - Add `syn: https://www.synapse.org/Synapse:` to `prefixes`.
   - Make `generated` `multivalued: true`.
   - `Activity`/`Usage` `slot_usage`: `name` → `slot_uri: sagegov:name` (D1).
   - `Activity` `slot_usage`: `modifiedBy` → `range: integer`,
     `slot_uri: governanceduo:modifiedBy`. This mirrors `createdBy`, which is
     already `governanceduo:createdBy` integer, and is needed because step 10
     makes the shared `modifiedBy` a Principal reference the dumper can't
     serialize from an integer key.
   - Rewrite the description paragraphs about bare/relative `uriorcurie` values.
3. **`linkml/examples/provenance/activity.example.yaml`:** use `syn:syn…` CURIEs
   and a list for `generated`. Add a second example: one Activity with two
   outputs and a UsedURL input (`url` + `name`). Regenerate
   `linkml/examples/provenance/rdf/`.
4. **`scripts/sync_provenance_graph.py`:**
   - Emit `syn:<id>` for `generated`/`entity`.
   - Mint Activity IRIs through `graph_iris.py`.
   - Accumulate Activities by id across the requested entities, building each
     once with all of its outputs before dumping (no duplicate Usage nodes).
   - Make `add_was_derived_from()` count only triples that weren't already
     present.
   - Replace the docstring's "confirmed empirically" claim with what was
     actually verified.

### Phase B: derivation policy as a graph layer

5. **`linkml/derivation_policy.yaml` (D6):**
   - `ControlLabel` → `class_uri: sagegov:ControlLabel`;
     `DerivationReview` → `class_uri: sagegov:DerivationReview`.
   - Their slots `subject`, `sourceAccessRequirements`, `computedFrom`,
     `computedOn`, `activity`, `inputLabels`, `reviewStatus`, `reviewNotes` get
     `sagegov:` slot URIs.
   - `ControlLabel`'s `dataTier` slot_usage: `governanceduo:dataTier` →
     `sagegov:dataTier`.
6. **`linkml/mixins.yaml` (D5):** add `Unclassified` to `DataTierEnum` ("Tier not
   yet determined by a curator; treated as more restrictive than Private until
   set"). Mirror it in `model/shared.model.csv:17` and `model/valid_values.csv`.
   Check `drs_alignment.yaml` and `docs/drs-interop.md` for tier handling that
   needs a case.
7. **`scripts/build_derivation_policy.py`:**
   - Delete `local_id()` and join on full IRIs.
   - Traverse `prov:wasDerivedFrom` and every property declared
     `rdfs:subPropertyOf` it in the loaded graphs (`rdfs:subPropertyOf*`). With
     sagebrain's bridge axiom loaded, labels then reach sagebrain Associations
     and Samples.
   - Mint `gov:control-label-<local>` / `gov:derivation-review-<n>` nodes.
   - Emit `subject` as the entity IRI (a `syn:` file or a sagebrain node),
     `sourceAccessRequirements` as the graph's `gov:AR-<n>` IRIs (the nodes
     `authorize.py` already returns), and `computedFrom` as the `gov:activity-N`
     IRI, not `Literal`s.
   - Add `Unclassified: 4` to `DATA_TIER_RANK`. An entity with AR bindings but no
     curated tier ranks `Unclassified`. Stop skipping labels with no tier. An
     entity with neither ARs nor ancestry still gets no label.
   - Accept `--extra-graph` (repeatable) so a sagebrain ABox and ontology can be
     loaded alongside.
   - Rewrite the module docstring's cross-file-matching paragraph.
8. **Committed regression fixture:** `linkml/examples/derivation_policy/fixture/`,
   containing:
   - a provenance ABox with a two-input Activity;
   - a governance graph binding the inputs to two different ARs;
   - curated ARs, one with `dataTier: Controlled` and one with none;
   - a small sagebrain-shaped ABox: one `biolink:Association` with
     `sagebrain:derived_from` the Activity's output, plus the bridge axiom
     (declared locally in the fixture, pinned to the sagebrain-model follow-up
     that will own it).

   Add `scripts/check_derivation_policy.py`, which runs the builder on the
   fixture and asserts with SPARQL ASK that:
   - the output file carries the max-rank label;
   - an `Unclassified` label keeps its `sourceAccessRequirements`;
   - there is exactly one `Flagged` DerivationReview;
   - **the Association inherits the output file's label.**

   Add a `make derivation-policy-check` target.

### Phase C: governance graph output (D3, D7, D8)

9. **DUO IRIs (D3, revised):**
   - `linkml/mixins.yaml`: give DUOPlus1–7 `meaning: sagegov:DUOPlusN`.
   - `scripts/build_governance_graph.py:321`: emit `gov:duoCode` as
     `URIRef(expand_curie(meaning))`, not `Literal`. DUOPlus Conditions now get
     a `duoCode` too; `Pending Annotation` still mints no code.
   - `shapes/governance_graph.owl.ttl`: `gov:duoCode` → `owl:ObjectProperty`.
     Declare `sagegov:DUOPlus1`–`7` as individuals with label and definition
     from the enum. Update `governance_graph.shacl.ttl` (`sh:nodeKind sh:IRI`).
   - Check whether AR-level `dataUseModifiers` values anywhere reach the graph as
     literals, and convert them the same way.
10. **`linkml/governance_graph.yaml` (D3, the remaining four slots):**
    - `submittedBy`, `modifiedBy`, `accessorId` → `range: Principal`.
      `Principal` is keyed by integer `principalId`, so YAML records still carry
      the Synapse id and the OWL range becomes `gov:Principal`.
    - `source` → a new `SourceSystemEnum` whose values map, via `meaning`, to the
      IRIs the builder emits (`Synapse` → `sagegov:Synapse`,
      `SynapseACL` → `sagegov:SynapseACL`). In `shapes/governance_graph.owl.ttl`,
      retype `gov:source` from `rdf:Property` to `owl:ObjectProperty`.
    - Update each slot description, any sync or builder code that reads these
      fields, and run `linkml-validate` on `linkml/examples/governance_graph/`.
11. **`ACCESS` permission (D8):**
    - `build_governance_graph.py` `add_access_grant()` (`:222`): after the
      Synapse permissions, add `gov:permission gov:ACCESS` when `DOWNLOAD` is
      among them, with a comment stating the mapping and why.
    - `shapes/governance_graph.owl.ttl`: declare `gov:ACCESS` as an individual
      ("SageBrain authorization action, derived from Synapse DOWNLOAD; not a
      Synapse ACCESS_TYPE"). Allow it in `governance_graph.shacl.ttl`.
    - `AccessTypeEnum` stays a pure mirror of Synapse's enum. The derived value
      is builder-only, following the same convention as the derived
      `prov:wasDerivedFrom` edge.
    - Document the mapping in `docs/knowledge-graph.md`.
12. **Infra contract test (D7):**
    - Add `tests/infra_contract/authorize_query.rq`: `authorize.py`'s query,
      copied verbatim with its source pinned (sagebrain-infra `fc6de51`,
      `src/lambda_rebac/authorize.py`), the same way sagebrain-model pins
      imports.
    - Add `scripts/check_infra_contract.py`, which runs that query against the
      exported governance graph and re-implements only `authorize.py`'s
      comparison rules (principal suffix, permission local name equals
      `"ACCESS"`). It asserts that the example principal is permitted on
      `syn10081783` with AR-42 returned, and that an unlisted principal and a
      READ-only grant are not.
    - With `SAGEBRAIN_INFRA=<path>` set, it instead imports `authorize.py`
      itself (AWS modules stubbed, as in the review) to catch drift from the
      copy.
    - Add a `make infra-contract-check` target and include it in `validate-all`.

### Phase D: OWL 2 DL conformance

13. **`scripts/build_owl.py`:**
    - Pass `use_native_uris=False`, `metaclasses=False`, `type_objects=False`.
    - Remove `rules` from every class in the loaded `SchemaDefinition` before
      handing it to `OwlSchemaGenerator` (D2). The rules are removed from the
      generator's input, not cut out of the output afterwards. Add a comment
      pointing at `owlgen.add_constraints()`'s `is_literal=None` behavior.
    - Declare every annotation property the output uses (`skos:*`, `dcterms:*`,
      any remaining `linkml:*`) as `owl:AnnotationProperty`. gen-owl omits these
      declarations, and DL requires them.
    - Keep the DUO-term stamping; verify it still finds its terms under the new
      settings.
14. **Regenerate** `shapes/governance_duo.owl.ttl`/`.shacl.ttl` and
    `docs/reference/`. This replaces the uncommitted reordering-only diffs;
    discard those first.
15. **DL check.**
    - Makefile: add `ROBOT_VERSION ?= 1.9.8`, a `tools/robot.jar` download rule
      copied from sagebrain-model's (the jar is gitignored), and an `owl-profile`
      target. The target runs `validate-profile --profile DL` on
      `governance_duo.owl.ttl`, on `governance_graph.owl.ttl`, and on a merge of
      the two.
    - Add `owl-profile` to `validate-all`.
    - Add `.github/workflows/validate.yml`: `setup-java@v4` (Java 21), then
      `make validate-all`.
16. **Stable build output.** Make `build_owl.py`'s serialization stable between
    runs by canonicalizing blank nodes before serializing. Time it. If it adds
    more than about 30 seconds to `make owl`, stop and bring it back as a
    decision rather than shipping a slow build.

### Phase E: publishing the layer (D9)

17. **One owner for the provenance-layer shapes.** Add
    `shapes/provenance_layer.shacl.ttl` to this repo: sagebrain's hand-written
    `UsageShape` (exactly one of entity reference or URL + `gov:name`, via
    `sh:xone`) and `ActivityShape` (one or more `prov:generated`), moved here
    with their tests' intent. gen-shacl can't express the `xone` constraint.
    Add it to `provenance-validate`.
18. **Release artifacts.** Define the published set in the README:
    - `shapes/governance_duo.owl.ttl`, `shapes/governance_graph.owl.ttl`,
      `shapes/governance_graph.shacl.ttl`, `shapes/provenance_layer.shacl.ttl`,
      each carrying `owl:versionIRI`/`owl:versionInfo`;
    - the IRI policy: `gov:` for graph terms and instances (`<type>-<id>`),
      `governanceduo:` for schema terms and LinkML record ids, `syn:` for
      Synapse entities, external terms by their own IRIs (`prov:`, `obo:DUO_`).

    Until a tag exists on `main`, consumers pin a commit hash in the raw GitHub
    URL; after merge, a tag. Add a `make release-check` that runs `validate-all`
    plus `owl-profile` and verifies version IRIs match the tag.
19. **Combined check with sagebrain-model.** Add an opt-in
    `make sagebrain-contract-check SAGEBRAIN_MODEL=<path>`. It stays opt-in
    because it needs a sibling checkout (sagebrain's own CI runs the equivalent
    check from the other side). It runs:
    - DL on the union of sagebrain's merged ontology, its governance module
      (with the bridge axiom) and both governance TBoxes;
    - SHACL over one joined worked example: sagebrain's `examples/AD-cohort.ttl`
      and `examples/pipeline_provenance.ttl`, merged with this repo's governance
      and provenance examples, validated against both repos' shapes;
    - `build_derivation_policy.py` over that joined example, asserting
      `association:apoe-expr-samp01` receives a ControlLabel.

    Document it in the README's validation section.

### Phase F: documentation

20. Update `README.md`, `docs/knowledge-graph.md` and
    `plans/prov_o_integration_report.md`:
    - the IRI policy, `Unclassified`, rules-not-in-OWL, the DL check, the
      `ACCESS` mapping, and the governance graph's role as a sagebrain layer;
    - correct the report's statements about `local_id()` and the sync script's
      verification status.
21. Split `plans/identifier_update.md`'s inline report into
    `plans/identifier_update_report.md`.
22. Write `plans/sagebrain_contract_and_owl_dl_fixes_report.md`.

### sagebrain-model follow-up (separate plan, in that repo)

Written as `plans/governance_layer_import.md` in sagebrain-model under its own
conventions (plan committed first, Implementation Report appended). It starts
after Phases A–E are committed here, so the pin moves once.

- **Import instead of copy.** Fetch this repo's release artifacts by pinned URL
  through `scripts/import.sh`, with a ROBOT extract to keep the rendered graph
  small, as sagebrain already does for Biolink.
  - Delete the hand extract in `ontology/imports/governance_graph.ttl` and the
    `gov:` re-declarations in `ontology/governance/pipeline_provenance.ttl`.
  - Replace the Activity/Usage shapes in `ontology/shacl/governance-shapes.ttl`
    with this repo's `provenance_layer.shacl.ttl`.
- **Bridge axiom (sagebrain owns it):** add
  `sagebrain:derived_from rdfs:subPropertyOf prov:wasDerivedFrom` in
  `ontology/governance/`, not `ontology/main/`. The default build doesn't import
  PROV, so putting it in main would add an undeclared property to its DL check.
  Add a shape or test confirming derived Associations resolve to
  `gov:SynapseEntity` ancestors.
- **Fixtures and examples:**
  - `rdfs:label` → `gov:name`; `syn:activity.*` → `gov:activity-*`.
  - Add a two-output Activity to the conforming fixture.
  - `tests/validate.py`: update defect (o)'s focus-node check.
  - Add a test running the joined worked example against both repos' shapes and
    the union DL check.
- **Docs:** `plans/pipeline_provenance_layer.md` — correct the
  "mirrors governanceDUO" claims (`rdfs:label`, exactly one output).

## Verification

- **Sync (offline):** the simulation harness from the review (fake REST payloads
  for one Activity with two outputs, a UsedURL and a UsedEntity) completes. The
  output has one `gov:activity-N` node with 2 `prov:generated`, exactly 2 Usage
  nodes, only absolute IRIs (a SPARQL check that no IRI starts with `file:`), and
  `gov:name` on the URL Usage. It reports 2 derived edges.
- **Joins:** `prov:entity syn:syn10081783` in the provenance examples is the same
  IRI as the governance graph node, and `gov:duoCode` objects are the same IRIs
  as sagebrain's `duo.ttl` terms (SPARQL joins return rows). `local_id` no longer
  appears anywhere in `scripts/`.
- **Derivation policy:**
  - `make derivation-policy` writes a non-empty graph: `syn10081783` has an
    `Unclassified` `gov:ControlLabel` citing `gov:AR-42`.
  - `make derivation-policy-check` passes, including the Association-inherits
    assertion.
  - Temporarily breaking the rank logic or the sub-property traversal makes the
    check fail; that edit is reverted.
- **Infra contract:**
  - `make infra-contract-check` passes. With
    `SAGEBRAIN_INFRA=~/sage-bionetworks/sagebrain-infra` it also passes using
    infra's real `authorize.py`.
  - Before step 11 it fails on the permission comparison, confirming the check
    works.
- **DL:** `make owl-profile` exits 0 with 0 violations on
  `governance_duo.owl.ttl`, on `governance_graph.owl.ttl`, and on their merge.
  - The OWL contains no rule-derived axioms (SPARQL for `rdfs:subClassOf` with an
    anonymous `owl:intersectionOf` subject returns 0, against 35 today).
  - `prov:Activity`, `prov:Usage` and `sagegov:wasExecuted` (DatatypeProperty,
    `xsd:boolean`) are declared under their real IRIs.
- **Regressions:**
  - `make validate-all` passes.
  - `make linkml-lint` doesn't get worse.
  - `linkml-validate` still rejects an AR violating one of the DUO rules,
    confirming the rules are still enforced after leaving the OWL.
  - DUO stamping still adds its `skos:scopeNote`s.
- **Stability:** two consecutive `make owl shacl` runs give byte-identical files.
- **Combined graph:**
  `make sagebrain-contract-check SAGEBRAIN_MODEL=~/sagebrain-model` fails against
  sagebrain's current branch on the known items (`rdfs:label`, the
  `prov:generated` limit, the missing bridge). It passes once the sagebrain-model
  follow-up lands: union DL clean, joined example conforms, and
  `association:apoe-expr-samp01` is labeled.
- **Pre-PR:** run an independent expert-framed review (OWL/SHACL/PROV-O, the
  Synapse API, and the infra authorization contract) on the branch and address
  its findings before `gh pr create`.

## Process

Store this plan for review, then implement in the granular commits above.
Afterwards, write `plans/sagebrain_contract_and_owl_dl_fixes_report.md` with what
was actually changed, per phase and file, and the verification actually run with
its results, including any deviations from this plan.
