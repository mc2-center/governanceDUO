# Report: sagebrain contract and OWL 2 DL fixes

Executed against [`sagebrain_contract_and_owl_dl_fixes.md`](sagebrain_contract_and_owl_dl_fixes.md)
(plan committed on its own as `1ddd3c1`). All 22 steps were implemented in 25
commits on `kg-conversion`, `f0dec17`..`7622ae2`. Deviations from the plan are
listed per step and summarized at the end, along with the problems found along the
way that are **not** fixed and need a decision.

Before starting, the uncommitted `shapes/governance_duo.{owl,shacl}.ttl` diffs were
discarded. They held identical triples in a different order, checked by comparing
triple counts, non-blank-node triples, and blank-node triple shapes.

## Phase A — provenance IRIs and sync correctness

| Step | Commit | Change |
|---|---|---|
| 1 | `f0dec17` | `scripts/graph_iris.py`: the shared graph-IRI policy (`activity.N` → `sagegov:activity-N`, `derivation_review.N` → `sagegov:derivation-review-N`, everything else `governanceduo:<id>`). `convert_examples_to_rdf.py`'s `to_curie()` delegates to it. |
| 2 | `889471c` | `linkml/provenance.yaml`: `syn:` prefix, `generated` multivalued, `name` → `sagegov:name` on Activity/Usage, `Activity.modifiedBy` → `governanceduo:modifiedBy` integer. |
| 3 | `5c3e7f5` | Provenance examples use `syn:` CURIEs; new `activity_multi_output.example.yaml` (two outputs, a UsedURL and a versioned UsedEntity). |
| 4 | `0b29f82` | `scripts/sync_provenance_graph.py`: gov: Activity ids at dump time, `syn:` references, one node per Activity across requested entities, accurate derived-edge count, corrected docstring. |
| 4a | `a0c7149` | **Added beyond the plan:** `scripts/check_sync_provenance.py` + `make sync-provenance-check`, an offline regression check running the script's real `main()` against a fake Synapse client. |

**Deviations.**
- **Step 2:** `syn:` also had to be declared in the root schema
  (`governance_duo.linkml.yaml`). `SchemaView.namespaces()` only includes imported
  schemas' prefixes once imports are processed, and caches the result, so a prefix
  declared only in `provenance.yaml` never resolved: `syn:syn1` serialized as the
  literal IRI `<syn:syn1>`. The prefix value also has to be quoted in YAML, since a
  scalar ending in `:` is read as a mapping key.
- **Step 4a:** added because the step-4 bug (the `@base` crash) had shipped behind
  a throwaway check, the exact gap the pre-PR directive asks to close systemically.

**Verification.**
- `make sync-provenance-check` passes: one `gov:activity-9606` with 2 `prov:generated`, exactly 2 Usage nodes, `gov:name` on the URL Usage, no `file:` IRIs, 2 derived edges reported.
- It fails on the pre-fix script with the original `Unknown CURIE prefix: @base`.
- Provenance examples conform to SHACL regenerated from the schema.
- `linkml-lint` output unchanged.

## Phase B — derivation policy as a graph layer

| Step | Commit | Change |
|---|---|---|
| 5 | `67cfa0d` | `derivation_policy.yaml`: `ControlLabel`/`DerivationReview` and all their slots → `sagegov:`; example references are graph CURIEs. |
| 6 | `62093ed` | `Unclassified` added to `DataTierEnum`; mirrored in `model/shared.model.csv`, `model/valid_values.csv`, and the docs' `sh:in` example. |
| 7 | `33f8777` | `build_derivation_policy.py`: `local_id()` deleted (full-IRI joins); fail-closed `Unclassified` ranking; labels kept without a known tier; ancestry over `prov:wasDerivedFrom` and its sub-properties; `--extra-graph`; gov: output IRIs; `computedFrom` from the generating Activity; deterministic output order. |
| 8 | `f5b9256` | Fixture in `linkml/examples/derivation_policy/fixture/` + `scripts/check_derivation_policy.py` + `make derivation-policy-check`. |

**Deviations.**
- **Step 5:** `reviewedBy`/`reviewedOn` also moved to `sagegov:`. They are
  DerivationReview slots, and the plan's list simply missed them.
- **Step 7:** ControlLabel nodes for non-Synapse subjects are keyed by the subject's
  prefixed name (e.g. `control-label-association-fixture-assoc-01`), or by a short
  hash when no prefix is bound. This keeps the node IRIs unique across namespaces.

**Verification.**
- `make derivation-policy` on the shipped examples now writes 19 triples (was 0):
  `syn10081783` carries `Unclassified` citing `gov:AR-42`, and its three derived
  outputs inherit it, each with `computedFrom` pointing at its Activity. The output
  conforms to regenerated SHACL.
- `make derivation-policy-check` passes all 6 assertions.
- It fails when the sub-property traversal is broken (the Association assertion) or
  when fail-closed ranking is broken (4 assertions). Both edits were reverted.

## Phase C — governance graph output

| Step | Commit | Change |
|---|---|---|
| 9 | `453421c` | DUOPlus1–7 get `meaning: sagegov:DUOPlusN`; `gov:duoCode` emitted as the code's IRI (`obo:DUO_…` or `gov:DUOPlusN`); hand TBox makes it an ObjectProperty and declares the DUOPlus individuals (text generated from the enum); SHACL requires an IRI. |
| 10 | `bca7346` | `submittedBy`/`modifiedBy`/`accessorId` → range `Principal`; `source` → new `SourceSystemEnum` (`Synapse` → `sagegov:Synapse`), resolved through the enum's meaning by the builder; hand TBox `gov:source` → ObjectProperty. |
| 10a | `c2e0b99` | `submitterId` → range `Principal` (see deviations). |
| 10b | `383e4b5` | `ResearchProject`/`DataAccessRequest` `createdBy` slot_usage → range `Principal` (see deviations). |
| 11 | `69ae58a` | Builder derives `gov:permission gov:ACCESS` on grants carrying `DOWNLOAD`; hand TBox declares `gov:ACCESS`; SHACL allows it; documented in `docs/knowledge-graph.md`. |
| 12 | `bcb24bc` | `tests/infra_contract/authorize_query.rq` (verbatim, pinned to sagebrain-infra `fc6de51`), `scripts/check_infra_contract.py`, `make infra-contract-check`. |

**Deviations.**
- **Steps 10a/10b:** added. They only surfaced once the OWL was generated with real
  IRIs (step 13). Each is the same D3 alignment as step 10: `AccessApproval.submitterId`
  shares `gov:submittedBy`, and two `createdBy` overrides map to `gov:createdBy`, all
  emitted as Principal IRIs but still typed integer. Left as they were, they punned
  `gov:submittedBy` in the generated OWL and `gov:createdBy` in the merged TBoxes.
- **Step 10:** `SourceSystemEnum` holds only `Synapse`. The design doc's
  `gov:SynapseACL` is used by neither the sync nor the examples, so it wasn't
  invented.

**Verification.**
- Governance graph rebuilt after each step. The only content changes were
  `gov:duoCode` (step 9) and the added `gov:ACCESS` (step 11); steps 10/10a/10b
  left it byte-identical. `make governance-graph-validate` conforms throughout.
- A DUOPlus and Pending Annotation case was exercised in memory: `DUOPlus1` →
  `gov:DUOPlus1`. The DUO IRI (`DUO_0000007`) is present in sagebrain-model's
  `duo.ttl`.
- `linkml-validate` on the 14 governance examples: the same 5 failures before and
  after, with identical messages (pre-existing, see open items).
- `make infra-contract-check` passes in both modes:
  - default: the pinned query copy;
  - `--infra`: infra's real `_authorize_resource()` from `fc6de51`, with Neptune
    replaced by a local query and Cedar/AVP stubbed.

  Both modes fail against the export from before step 11 (`principal 9000001:
  expected ALLOW, got DENY`).

## Phase D — OWL 2 DL conformance

| Step | Commit | Change |
|---|---|---|
| 13 | `9325654` | `build_owl.py`: `use_native_uris=False`, `metaclasses=False`, `type_objects=False`; rules removed from the import-merged schema before generation (D2); `repair_generator_output()` (approved workaround); `declare_annotation_properties()` run after DUO stamping. |
| 14 | `1071ca4` | Regenerated OWL/SHACL, `docs/reference/`, and `linkml/examples/rdf/` (record-level DUOPlus values are now IRIs). |
| 15 | `d67f02e` | `make owl-profile` (governance_duo, governance_graph, their merge); ROBOT 1.9.8 fetched to gitignored `tools/robot.jar` (sagebrain-model's rule); added to `validate-all`; `.github/workflows/validate.yml` (Python 3.11, Java 21) runs `make validate-all` on pushes to main and PRs. |
| 15a | `75eb1b3` | `owl-profile`'s merged check now merges to a file, then validates (see deviations). |
| 16 | `8862f40` | `build_owl.py` relabels blank nodes canonically before serializing: consecutive builds are byte-identical, about 10 s added to `make owl`. |

**Deviations.**
- **Step 13 — gen-owl's `slot_usage` handling (approved as a schema-derived repair
  pass).** With `use_native_uris=False`, owlgen:
  - never declares a property that a `slot_usage` gives its own `slot_uri`
    (8 properties, e.g. `sagegov:name`);
  - writes restrictions for `slot_usage`s with no `slot_uri` against
    `governanceduo:<name>` instead of the declared IRI (34 `id` restrictions vs
    `dcterms:identifier`);
  - declares and restricts `owl:sameAs`, which OWL 2 DL forbids.

  `repair_generator_output()` fixes all three from the schema alone. The linkml
  issue to file upstream is drafted below; **not filed**, because filing is public.
- **Step 15a:** chaining `robot merge … validate-profile` in one call reports
  violations that don't exist when the merge is written out and validated
  separately. Found in step 19. The chained check had passed, but it now uses the
  reliable form.
- **Step 16:** covers `build_owl.py` only, as planned. The SHACL (`gen-shacl`) and
  the example RDF still reorder blank nodes on every rebuild. The same
  canonicalization takes about 108 s on the SHACL, over the plan's 30-second
  budget, so it's brought back as a decision (open item 1).

**Verification.**
- `robot validate-profile --profile DL` exits 0 on `governance_duo.owl.ttl`, on
  `governance_graph.owl.ttl`, and on their merge. Before: 103 puns and about 1,600
  undeclared-entity violations.
- 0 rule-derived axioms (was 35).
- `prov:Activity`/`prov:Usage` declared as classes;
  `sagegov:wasExecuted` is `owl:DatatypeProperty` with range `xsd:boolean`.
- 24 DUO `skos:scopeNote` stamps still applied.
- `make owl-profile` fails with exit 2 and prints the 103 original puns on the
  pre-fix OWL.
- Two consecutive `build_owl.py` runs are byte-identical. A later full rebuild
  (during `release-check`) also reproduced the committed OWL exactly.
- `linkml-validate` still rejects an AR carrying `DUO:0000007` without
  `diseaseSpecificResearch` ("'diseaseSpecificResearch' is a required property"),
  so the rules stay enforced after leaving the OWL.

## Phase E — publishing the layer

| Step | Commit | Change |
|---|---|---|
| 17 | `0dec71f` | `shapes/provenance_layer.shacl.ttl` (`gov:UsageShape` with `sh:xone`, `gov:ActivityShape`), moved from sagebrain-model and owned here; checked by `make provenance-validate`. |
| 18 | `a6a5300` | owl:Ontology version headers on the hand-written TBox and both shapes files; `VERSION` in the Makefile; `scripts/check_release.py` + `make release-check`; README "Release artifacts and IRI policy". |
| 19 | `854a63a` | `scripts/check_sagebrain_contract.py` + `make sagebrain-contract-check SAGEBRAIN_MODEL=<path>`; `tests/sagebrain_contract/governance_binding.ttl`. |

**Deviations.**
- **Step 17:** entity references are checked as absolute Synapse IRIs
  (`sh:pattern` on `https://www.synapse.org/Synapse:syn\d+`) instead of
  sagebrain's `sh:class gov:SynapseEntity`. The pattern works on the provenance
  ABox alone and rejects relative IRIs directly; the class check only works with
  the governance graph merged in.
- **Step 19, what the union DL check covers:** sagebrain-model's own DL test
  checks only `ontology/main` plus its biolink/governance_graph imports, and its
  vendored `prov.ttl`/`duo.ttl` are not DL-clean on their own (e.g. puns inside
  `prov.ttl`). The union is therefore sagebrain's DL-checked set plus its
  governance modules plus this repo's TBoxes, excluding those two vendored
  vocabularies. It must be fully in profile.
- **Step 19, the SHACL part's ontology:** it uses sagebrain's ontology plus
  `governance_graph.owl.ttl`, not `governance_duo.owl.ttl`. Mixing the latter's
  ~5,000 triples into the data graph made pyshacl run past 10 minutes; without it
  every configuration takes under a second. `governance_duo.owl.ttl` describes
  LinkML records, not this graph, and `governance-graph-validate` already makes
  the same choice.
- **Step 19, the fixture:** `governance_binding.ttl` binds sagebrain's raw pipeline
  file to `gov:AR-42`, so the joined example has a governed source whose label
  must reach the Association.

**Verification.**
- The shapes: current examples conform; the pre-fix ABox (`file:///` references)
  and a Usage carrying both branches are rejected.
- The release check: `make release-check` passes; a version mismatch reports all
  eight header mismatches plus the tag.
- The contract check against sagebrain-model `provenance-features` (`8d04715`)
  runs in 3.8 s and fails on exactly the known items: `rdfs:label` vs `gov:name`
  in both directions, the "exactly one output" limit, and the missing bridge. The
  union DL part already passes.
- Against a scratch copy with the follow-up applied it passes all three parts.
  That copy had examples using `gov:name`/`gov:activity-*`, sagebrain's
  governance shapes removed, and the bridge axiom **plus a declaration of
  `prov:wasDerivedFrom` as an ObjectProperty** (see open item 5).

## Phase F — documentation

| Step | Commit | Change |
|---|---|---|
| 20 | `fc9d04b` | `docs/knowledge-graph.md`, `docs/linkml-model.md`, `README.md`, `shapes/governance_graph.shacl.ttl` header; Corrections section appended to `plans/prov_o_integration_report.md`. |
| 21 | `7622ae2` | `plans/identifier_update.md`'s inline report moved to `plans/identifier_update_report.md`. |
| 22 | this file | |

**Deviations.**
- **Step 20:** also fixed docs statements that were already stale before this
  work: "8 real DUO terms" (it's 24), and the example-RDF snippet showing
  `"DUOPlus1"` as a string.
- **Step 20:** `prov_o_integration_report.md` gets an appended Corrections
  section rather than edits in place, so the original record stays readable.

**Verification.** `mkdocs build --strict` builds cleanly.

## Final verification (on `7622ae2`)

- `make release-check` (which runs `validate-all`) exits 0:
  - 5 SHACL validations pass;
  - `sync-provenance-check`, `derivation-policy-check` (6 assertions) and
    `infra-contract-check` pass;
  - OWL 2 DL passes for governance_duo, governance_graph and their merge;
  - all 4 release artifacts are at version 0.1.0.
- `make linkml-lint`: output identical to the pre-change baseline.
- `linkml-validate` still enforces the DUO rules (above).
- `make sagebrain-contract-check`: fails against sagebrain's current branch on the
  known items; passes against the simulated follow-up.
- **Not yet run:** the independent expert-framed pre-PR review the plan's
  Verification requires before `gh pr create`. No PR has been opened.

## Open items — need a decision, not fixed here

1. **SHACL and example-RDF rebuilds still reorder blank nodes.** `make shacl`
   (gen-shacl) and `make example-rdf`/`provenance-example-rdf`/
   `derivation-policy-example-rdf` write reordering-only diffs on every rebuild,
   and `make validate-all` rebuilds them. Canonicalizing the SHACL the way
   `build_owl.py` does takes about 108 s. The alternatives are a fast
   deterministic relabeling written for these tree-shaped blank nodes (new code),
   or accepting the churn.
2. **An AR marked "Pending Annotation" mints an invalid IRI** (existing bug). The
   builder names each Condition node `gov:AR-<n>-condition-<code>`, so "Pending
   Annotation" yields a space in the IRI, which breaks serialization and Neptune
   loads. The choice: skip Conditions for "Pending Annotation" (a curation state,
   not a data-use condition), or encode the name.
3. **Five governance examples fail `linkml-validate`** (existing). These are
   `access_requirement_association`, `data_access_submission`, `access_approval`,
   `research_project` and `data_access_request`. Each fails with
   "'access_requirement.42' is not of type 'object'": references to
   AccessRequirement are expected as inline objects. The failures are identical
   before and after this work.
4. **Filing the linkml owlgen issue** (draft below) needs your go-ahead. Once fixed
   upstream, `repair_generator_output()` can be deleted.
5. **The sagebrain-model follow-up plan needs one more item.** The module that adds
   `sagebrain:derived_from rdfs:subPropertyOf prov:wasDerivedFrom` must also
   declare `prov:wasDerivedFrom a owl:ObjectProperty`. sagebrain's DL-checked set
   doesn't import `prov.ttl`, so without the declaration OWLAPI reads the axiom as
   an annotation sub-property and the union check fails.
6. **Minor:** on Activity, `createdOn` serializes as `governanceduo:createdOn` but
   `modifiedOn` as `sagegov:modifiedOn`. This predates this work and wasn't in scope.

### Draft linkml issue (not filed)

> **owlgen: slot_usage overrides produce undeclared or misdirected properties with
> `use_native_uris=False`**
>
> With `use_native_uris=False` (linkml 1.11.1):
> 1. A `slot_usage` that sets its own `slot_uri` (e.g. `name: {slot_uri: ex:name}`
>    on one class) is used in that class's restrictions, but the property is never
>    declared, so OWLAPI can't tell object from data property. `add_slot()` skips
>    induced slots by design ("should not be used for global properties"), but
>    nothing declares the override's IRI either.
> 2. A `slot_usage` with no `slot_uri` (e.g. only a `pattern` on `id`) is restricted
>    under `<default_prefix>:<slot name>` rather than the base slot's declared
>    `slot_uri` (here `dcterms:identifier`).
> 3. Slots whose `slot_uri` is built-in vocabulary (`owl:sameAs`) are declared as
>    data properties and restricted, which OWL 2 DL forbids.
>
> Separately, in rule translation `add_constraints()` receives `is_literal=None`,
> so every `equals_string` precondition is dropped and each rule becomes an
> unconditional axiom.
