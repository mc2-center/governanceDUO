# governanceDUO

LinkML model, knowledge graph representation, Policy Fabric integration, and a
design-only GA4GH Data Repository Service (DRS) interoperability crosswalk for Sage
Bionetworks' DUO-based data governance model on Synapse. See [`docs/`](docs/index.md)
for the full documentation site, or the collapsed archive at the bottom of this file
for the original DUO background and the legacy schematic CSV/Synapse-submission
workflow.

# Repository layout

| Path | Contents |
| --- | --- |
| [`linkml/`](linkml/governance_duo.linkml.yaml) | The **record layer**: curated `AccessRequirement`/`Study`/`Resource`/`Schema`/`DerivationRule` records, the Policy Fabric crosswalk, and the DUO vocabulary (`governance_duo.linkml.yaml`), plus hand-written example instances under `linkml/examples/` |
| [`linkml/graph/`](linkml/graph/governance.yaml) | The **graph layer**: `governance.yaml` + `vocabularies.yaml`, a separate, independently-versioned schema for every `gov:` term — see [Governance graph design](docs/graph-design.md) |
| [`json_schemas/`](json_schemas/) | Generated Synapse Curator-compatible JSON Schema, one per curated class (`AccessRequirement`/`Study`/`Resource`/`Schema`, `make json-schemas`, `scripts/build_json_schemas.py`) — bind one to a folder to drive a Record Set |
| [`shapes/`](shapes/) | Generated OWL/SHACL for both schemas: `governance_duo.{owl,shacl}.ttl` (record layer, `make owl`/`make shacl`) and `governance.{owl,shacl}.ttl` (graph layer, `make graph-tbox`) — nothing under `shapes/` is hand-authored any more |
| [`archive/model/`](archive/model/) | Archived: the modular [`schematic`](https://github.com/Sage-Bionetworks/schematic)-style CSV data model (one file per class, `shared.model.csv`, `valid_values.csv`) the record layer was originally derived from. `schematic` itself is deprecated; LinkML is the sole source of truth now — nothing generates from these CSVs any more |
| [`archive/sage-ar-model/`](archive/sage-ar-model/) | Archived, no longer built: outputs of the former schematic pipeline (the collated CSV and JSON-LD, per-class Synapse JSON schemas, and the AR conditional validation schema) |
| [`governance_graph_export/`](governance_graph_export/) | Generated Turtle: the canonical graph example (`make governance-graph`) and the `authorizer_v1` projection sagebrain-infra reads (`make projections`) |
| [`policy_fabric_export/`](policy_fabric_export/) | Generated Policy Fabric input JSON (`make policy-fabric`) |
| [`derivation_policy_export/`](derivation_policy_export/) | Generated Turtle export of computed `ControlLabel`/`DerivationReview` individuals (`make derivation-policy`) — see `linkml/graph/governance.yaml` and `plans/model_refactor.md` |
| [`docs/`](docs/index.md) | The mkdocs documentation site — narrative pages plus an auto-generated schema reference (`make docs`); published to GitHub Pages via `.github/workflows/docs.yml` |
| [`scripts/`](scripts/) | The Python build/export/validate scripts the `Makefile` drives |
| [`scripts/provision_curator_infrastructure.py`](scripts/provision_curator_infrastructure.py) | Not Makefile-driven, and not read-only like everything else above: provisions real, live Synapse infrastructure (folders, Record Sets, curation tasks, a unified view) for a given program/class — see `plans/synapse_curation_infrastructure.md` |
| [`plans/`](plans/) | Design plans for major changes to this repo, each with a companion `*_report.md` |
| [`archive/`](archive/) | Legacy, pre-LinkML reference material kept for history — see the collapsed archive section below |

All generated artifacts above can be rebuilt from `linkml/` alone via the
`Makefile` (`pip install -r requirements.txt` first); see `make linkml-lint`,
`make owl`/`shacl`/`example-rdf`/`shacl-validate`, `make policy-fabric`,
`make json-schemas`, `make governance-graph`/`governance-graph-validate`,
`make validate-all`, and `make docs`/`docs-build`/`docs-serve`.

# Resources
 - [GA4GH Products](https://www.ga4gh.org/product/data-use-ontology-duo/)
 - [EBISPOT DUO](https://github.com/EBISPOT/DUO/blob/master/README.md)
 - [Extension of Data Access Management](https://sagebionetworks.jira.com/wiki/spaces/PLFM/pages/2597617665/API+Changes+to+support+Extension+of+Data+Access+Management+to+Users+outside+of+Sage+ACT)


# Related Publications
 - The Data Use Ontology to streamline responsible access to human biomedical datasets. Lawson, Jonathan et al., Cell Genomics, Volume 1, Issue 2, 100028, doi: https://doi.org/10.1016/j.xgen.2021.100028
 - Aligning NIH’s existing data use restrictions to the GA4GH DUO standard. Lawson, Jonathan et al., Cell Genomics, Volume 3, Issue 9, 100381, doi: https://doi.org/10.1016/j.xgen.2023.100381
 - Enhancing Data Use Ontology (DUO) for health-data sharing by extending it with ODRL and DPV. Pandit HJ, Esteves B., Semantic Web. 2024;15(4):1473-1498, doi: https://doi.org/10.3233/SW-243583
 - Getting your DUCs in a row - standardising the representation of Digital Use Conditions. Jeanson, F., Gibson, S.J., Alper, P. et al., Sci Data 11, 464 (2024), doi: https://doi.org/10.1038/s41597-024-03280-6


# Documentation

Deeper, example-backed docs on the LinkML model, its knowledge-graph representations,
the Policy Fabric integration, and a design-only GA4GH Data Repository Service (DRS)
interoperability crosswalk — including an auto-generated schema reference
(`make docs`) — live under [`docs/`](docs/index.md), starting at
[`docs/index.md`](docs/index.md). The **Governance Graph alignment** section below
is a short summary only; [Governance graph design](docs/graph-design.md) and
[Technical implementation](docs/graph-design-implementation.md) are the current,
authoritative source for that layer following its 2026-09 graph-layer refactor
(`plans/model_refactor.md`). The LinkML/Policy Fabric sections below describe the
record layer, unaffected by that refactor; the docs/ pages add diagrams, worked
examples, and full per-class/slot/enum reference on top of them.

The docs site (`mkdocs build`) is also published automatically to GitHub Pages on
every push to `main` that touches `docs/`, `mkdocs.yml`, or `requirements.txt` (see
[`.github/workflows/docs.yml`](.github/workflows/docs.yml)); once Pages is enabled in
the repo settings (source: GitHub Actions) it's served at
`https://mc2-center.github.io/governanceDUO/`.

# LinkML representation

This repository's record layer is a [LinkML](https://github.com/linkml/linkml-model)
schema under `linkml/`, entry point `linkml/governance_duo.linkml.yaml`, and is the
**sole source of truth** for its model. It is architecturally aligned with
[SageCommonDataModel](https://github.com/Sage-Bionetworks/SageCommonDataModel): one
file per entity (`access_requirement.yaml`, `resource.yaml`, `schema.yaml`,
`study.yaml`), a shared abstract `BaseEntity` + `slot_usage`-narrowed `id` slot
(`base_entity.yaml`), and cross-cutting concerns factored into `props.yaml`
(generic cross-class slots/enums) and `mixins.yaml` (`GovernanceMixin` — the DUO data-
use-modifier vocabulary plus the conditional-requirement rules that enforce it;
`ContributionMixin` — contributor tracking). It was originally derived from a
[`schematic`](https://github.com/Sage-Bionetworks/schematic)-style modular CSV model
(`archive/model/*.model.csv`); both `schematic` and that CSV model are now archived
and deprecated — nothing generates from them, and the LinkML schema is not obligated
to stay aligned with them going forward.

The archived schematic CSV kept class-prefixed identifier attribute names
(`AccessRequirement_id`, `Resource_id`, `Schema_id`, `Study_id`) because schematic's
model CSV has one flat, global `Attribute` namespace with no per-class scoping — four
classes couldn't share a bare `id` attribute there without colliding. The LinkML schema
uses one shared `id` slot on `BaseEntity`, narrowed per class via `slot_usage`
(a legacy from that CSV convention, kept because it still works well, not because
anything requires it now).

Real Data Use Ontology (DUO) terms are reused by IRI (`meaning: DUO:0000007`, etc.) —
never re-minted — matching the "reuse external terms by IRI" convention
[sagebrain-model](https://github.com/Sage-Bionetworks/sagebrain-model) documents for
its own ontology. `linkml/governance_duo.linkml.yaml` also declares `sagebrain:`
(`https://w3id.org/synapse/sagebrain#`) and `biolink:` prefixes so generated OWL
output's namespaces already line up with sagebrain-model's, and
`scripts/build_owl.py` stamps the same `skos:scopeNote`/`owl:versionInfo` annotations
on reused external terms that sagebrain-model's own convention uses for classes it
doesn't mint itself. The governance graph is a layer of sagebrain-model's graph:
this repository owns the governance-layer terms and shapes and publishes them for
sagebrain-model to import (see "Release artifacts and IRI policy" below);
`make sagebrain-contract-check` verifies the two work together. Interoperation with
SageCommonDataModel is not yet wired up.

Beyond DUO, several slots carry `exact_mappings`/`close_mappings` to other terms
found and verified live via the EBI OLS4 API (see the `ols-term-annotator` skill and
`comments` on each mapped slot for the verification rationale) — `exact_mappings`
where the concept genuinely matches, `close_mappings` where the shape differs (e.g. a
literal-valued slot mapped to an object property whose range is an ontology class):

| Slot | Mapping | Term |
|---|---|---|
| `ContributionMixin.contributorName` | close | `prov:wasAttributedTo` |
| `ContributionMixin.contributionDate` | close | `prov:generatedAtTime` |
| `GovernanceMixin.collaborationRequired` | exact | `NCIT:C221739` (synonyms include "COL", this repo's own DUO:0000020 shorthand) |
| `GovernanceMixin.dataTier` | exact | `NCIT:C175887` "Open or Controlled Data Access Indicator" |
| `GovernanceMixin.deidentificationType` / `Study.studyDeidentificationType` | close | `T4FS:0000414` "de-identification" |
| `GovernanceMixin.attribution` | close | `ebiswo:9000006` "Attribution clause" |
| `Study.studyInvestigator` | close | `NCIT:C19924` "Principal Investigator" |
| `Study.studyDbgapAccessionId` | exact | `NCIT:C173940` "dbGaP Accession Number" |
| `Study.grantNumber` | exact | `EVORAO:grantNumber` |
| `Resource.registeredSchemaUrl` / `Schema.schemaUrl` | exact | `dcterms:conformsTo` |

Note the `ebiswo:` prefix (`http://www.ebi.ac.uk/swo/SWO_`) is deliberately not
called `SWO:` — that would collide with the *canonical* OBO Foundry Software
Ontology namespace (`http://purl.obolibrary.org/obo/SWO_`), which is a different,
unrelated resolution for the same three letters; `linkml-lint`'s `canonical_prefixes`
check caught this during review. Slots checked against OLS with no confident match
(DUO-covered detail fields like `timeLimitOnUse`/`userSpecificRestriction`, Synapse
annotation-key/value mechanism slots, and `license`/`dataPermission`, whose SPDX/CC
identifiers aren't OLS ontology terms) were left unmapped rather than forced.

Build/validate targets (see `Makefile`; require `pip install -r requirements.txt`).
Record layer:
```
make linkml-lint      # lint both schemas (--ignore-warnings: the camelCase attribute
                       # names are intentional, see above)
make owl              # generate shapes/governance_duo.owl.ttl (scripts/build_owl.py)
make shacl            # generate shapes/governance_duo.shacl.ttl (linkml gen-shacl)
make example-rdf      # convert linkml/examples/*.example.yaml to RDF individuals
                       # under linkml/examples/rdf/ (scripts/convert_examples_to_rdf.py)
make json-schemas      # generate json_schemas/{AccessRequirement,Study,Resource,Schema}.json
                       # (scripts/build_json_schemas.py, LinkML's own JsonSchemaGenerator --
                       # no schematic dependency); bind one to a folder to drive a Record Set
make shacl-validate   # validate BOTH governance_duo.owl.ttl and the example RDF
                       # individuals against the SHACL shapes, via pyshacl with
                       # inference disabled and the ontology passed as ont_graph —
                       # the exact invocation discipline sagebrain-model's own
                       # tests/validate.py requires, since RDFS entailment on
                       # rdfs:range would otherwise manufacture the very types
                       # SHACL's sh:class checks are meant to verify
```
Graph layer (`linkml/graph/`, independently versioned — see
[Technical implementation](docs/graph-design-implementation.md)):
```
make graph-tbox        # generate shapes/governance.{owl,shacl}.ttl (scripts/build_graph_tbox.py)
make governance-graph  # build governance_graph_export/governance_graph.ttl from the
                        # canonical example (scripts/graph_rdf.py)
make graph-validate    # the canonical example against the generated shapes, plus
                        # scripts/check_graph.py's deliberate-defect/TBox-convention checks
make derivation-policy       # compute ControlLabel/DerivationReview (scripts/build_derivation_policy.py)
make derivation-policy-check # regression check against a committed fixture
make projections             # run projections/authorizer_v1.rq (+ _teams.rq with TEAMS=1)
                              # over the canonical graph (scripts/project.py)
make projections-check       # golden diff, approval expiry, team/descendant grant checks
make infra-contract-check    # sagebrain-infra's pinned authorizer query against the projection
make sagebrain-contract-check SAGEBRAIN_MODEL=<path>  # opt-in: this layer inside a
                                                       # sagebrain-model checkout
```
Both layers:
```
make validate-all     # everything above (record and graph layers alike) plus the
                       # OWL 2 DL profile check on both TBoxes — what CI runs
make owl-profile       # record-layer OWL 2 DL profile check (ROBOT, fetched to
                       # tools/robot.jar), plus prov: types vs W3C PROV-O (fetched to build/)
make graph-owl-profile # graph-layer OWL 2 DL, alone and merged with every canonical ABox
make release-check    # validate-all + every published artifact carries its own version
                      # (VERSION for the record layer, GRAPH_VERSION for the graph layer —
                      # they release independently)
make linkml-validate-examples  # linkml-validate every example (the only DUO-rules check)
make sync-governance-check     # sync_governance_graph.py offline, against a fake Synapse
make sync-provenance-check     # sync_provenance_graph.py offline, against a fake Synapse
make artifact-drift-check      # committed generated artifacts match a fresh rebuild
                               # (run after validate-all; CI does)
```
Example instances validating the DUO conditional-requirement rules live under
`linkml/examples/` (e.g. `linkml-validate -s linkml/governance_duo.linkml.yaml -C
AccessRequirement linkml/examples/access_requirement.example.yaml`). Note that
`gen-shacl` does not compile those `rules:` conditionals into SHACL, and
`scripts/build_owl.py` deliberately leaves them out of the OWL — only
`linkml-validate`'s JSON Schema path enforces them (`make linkml-validate-examples`,
part of `validate-all`); `make shacl-validate` covers
everything else (required fields, enum membership, regex patterns, datatypes,
cardinality) against real instance data, converted via
`scripts/convert_examples_to_rdf.py`. This schema's ids are dotted, colon-free
strings (`access_requirement.42` — the SageCommonDataModel-style convention this
schema deliberately follows), and linkml_runtime's RDF dumper can only mint a
subject URI for such an id via a special `"@base"` namespace entry that has to be
supplied externally at dump time — the schema's own `prefixes:` block can't declare
it at all (`Prefix('@base', ...)` is rejected as "not a valid NCName"), and
`linkml-convert`'s `-P/--prefix` CLI flag hits that same rejection trying to set it.
Rather than route around this with a made-up `@base` IRI (which also needs a
second workaround, since the dumper then binds the literal string `"@base"` itself
as an invalid Turtle prefix), `scripts/convert_examples_to_rdf.py` instead
temporarily rewrites each loaded instance's id to a real CURIE
(`governanceduo:access_requirement.42`; a curated `AccessRequirement` gets its
shared graph-layer IRI instead, `govid:ar/<n>` via `scripts/graph_iris.py`'s
`record_iri()` — decision R5 of `plans/model_refactor.md`) only for the dump call —
which `Namespaces.uri_for()` resolves directly via the schema's own already-declared
`governanceduo:` prefix, no `@base` involved — then restores the bare id
afterward. The *stored* id in every example YAML file and every class's
`slot_usage.id.pattern` are completely unaffected, preserving interoperability with
SageCommonDataModel's bare-id convention everywhere except this one transient
export step. See the script's docstring for the full explanation. This script only
ever handles record-layer examples (`AccessRequirement`/`Study`/`DerivationRule`);
the graph layer's own examples go through a completely different, generic path —
`scripts/graph_rdf.py` — described in
[Technical implementation](docs/graph-design-implementation.md).

The schematic pipeline's outputs (`archive/sage-ar-model/`) and its generator
(`archive/scripts/create_json_from_model.py`) are archived and no longer built, so
they don't reflect later `model/*.model.csv` changes such as the `Pattern`
additions.

## Policy Fabric alignment

[Policy Fabric](https://github.com/hasan7n/tmp-policies) (docs:
[hasan7n.github.io/tmp-policies](https://hasan7n.github.io/tmp-policies/); architecture
paper: "A Technical Policy Blueprint for Trustworthy Decentralized AI") is a
decentralized-AI governance framework whose reference policies (`policy_cards/`) are
each authored against a specific DUO code — the same Data Use Ontology this repo's
`GovernanceMixin`/`DataUseModifierEnum` already encode. `linkml/policy_fabric.yaml`
and `linkml/policy_fabric_bindings.yaml` add the missing structured link: for every
one of the 21 `policy_cards/` in that repo (verified by reading each folder's actual
`policy.rego` and `policy_data_schema.json`, not inferred from naming), a
`PolicyCardBinding` records its DUO code, its Reference Values Schema key(s), which
Verifiable Credential type(s)/claim(s) it requires, and — critically — which existing
governanceDUO slot (if any) already collects that reference value.

Each `PolicyCardBinding` maps its `referenceValueKeys` to governanceDUO slots via
`referenceValueSources` (a list, not a single scalar — several bindings need two
keys from two different slots, e.g. `time-limit-on-use`'s `requiredDocumentID` and
`notAfter`), each tagged `keyIsMultivalued` since some Policy Fabric keys are lists
(`allowedCountries`) and some are scalars (`datasetID`, `requiredDocumentID`,
`notAfter`) — `scripts/build_policy_fabric.py` honors this per key rather than
uniformly wrapping every value in an array, which was a real bug caught and fixed
while closing the gaps below.

5 of the 21 bindings had a working `sourceSlot` from the start:
`geographicalRestriction` and `diseaseSpecificResearch` already collected exactly
what's needed (ISO country codes, MONDO codes); `institutionSpecificRestriction`
didn't — Policy Fabric's `AffiliationCredential.isMemberOf` and
`allowedInstitutions` expect organization **DIDs**, not ROR ids, so a new companion
slot `institutionDids` was added rather than reinterpreting the existing ROR-pattern
field; `collaboration-required` and `publication-required` both key on a `datasetID`
sourced from `PolicyFabricMixin.assetBindings[].assetDid`. A new `PolicyFabricMixin`
(`assetBindings`, `guardianDataSource`, `guardianUrl`, `policyContractDid`,
`trustedIssuerDids`), applied to `AccessRequirement`, mirrors the real (minimal)
Django `Asset` model's `did`/`metadata` fields and the per-record trust choices
Policy Fabric's "expose" step captures. `assetBindings` is an inlined
`{synapseId, assetDid}` list — rather than a flat DID list positionally aligned with
`entityIdList` by convention only — so which DID registers which Synapse entity is
structural, not a documented-but-unenforced invariant.

The remaining 16 were **documented gaps, not silent guesses**, and have since been
closed by adding 9 new, deliberately reusable `GovernanceMixin` slots — each with
its own DUO-conditional `rules:` entry, matching this repo's existing pattern —
rather than repurposing an existing narrative field into the wrong shape:
`allowedPurposes`/`prohibitedPurposes` (reused across 8 codes), `nonprofitLegalForms`
(ISO 20275 ELF codes, 2 codes), `requiredAgreementDocumentId` (4 codes),
`approvedProjects`, `notAfter`, and `approvedUsers`/`allowedAccountTypes`/
`requiredProfileStatuses` (all three for `user-specific-restriction` alone, since its
Reference Values Schema has three independent keys that don't decompose from the
pre-existing free-text `userSpecificRestriction` field). Two of these are real shape
corrections, not just additions: `publicationMoratorium` (an end-date) and
`timeLimitOnUse` (a number of months) are left as-is, and the new
`requiredAgreementDocumentId`/`notAfter` slots source those two `policy_cards/`
instead, since the old fields never held what those policies actually check. All 21
bindings now have every `referenceValueKey` mapped except
`ethics-approval-required`, whose Reference Values Schema is genuinely empty (a pure
credential-chain check) — nothing to source, not a gap.

`scripts/build_policy_fabric.py` exports an `AccessRequirement` instance into Policy
Fabric's actual input shape: `policy_data.json` (merged reference values),
`associated_credentials.json`, and `asset_registration.json`. Run against
`linkml/examples/access_requirement_policy_fabric.example.yaml` (DUO:0000022 +
DUO:0000028 together, mirroring the tutorial's own worked example) via
`make policy-fabric`, its `policy_data.json` output is byte-for-byte the tutorial's
literal `{"allowedCountries": ["US"], "allowedInstitutions":
["did:example:best_university"]}`. **No changes have been made to
`hasan7n/tmp-policies` itself.**

## Governance Graph alignment

**This section is a short summary; it is not the current source of truth.** The
Governance Graph design described here was originally built as `AccessGrant`/
`AccessRequirementAssociation`/`DataAccessSubmissionStatus` classes inside the
record layer (`linkml/governance_graph.yaml`), verified column-by-column against
Synapse's real relational tables and REST enums. A 2026-09 graph-layer refactor
(`plans/model_refactor.md`, report in `plans/model_refactor_report.md`) replaced
that design with a separate, independently-versioned schema,
`linkml/graph/governance.yaml` + `vocabularies.yaml`, built on standard RDF
vocabularies instead of bespoke classes:

- **ACLs are W3C Web Access Control** (`acl:Authorization`), not a bespoke
  `AccessGrant`; teams are vCard groups (`vcard:Group`).
- **One Access Requirement is one IRI**, shared by its curated record and its
  graph node (no `owl:sameAs` bridge, no stub class) — a curator-authored
  `AccessRequirement` in this repo's record layer and its graph representation
  describe the same subject.
- **Inheritance is walked, not materialized**: `gov:benefactor`/`gov:parent` are
  recorded once; nothing copies an ACL or AR onto every descendant the way the
  original design did.
- **Provenance and derivation policy** (`Activity`/`Usage`/`ControlLabel`/
  `DerivationReview`) live in this same graph schema now, not
  `linkml/provenance.yaml`/`linkml/derivation_policy.yaml` (deleted; only
  `DerivationRule` stays in the record layer, as curator configuration).
- **The namespace changed**: `https://w3id.org/synapse/governance#` (`gov:`), not
  `https://sagebionetworks.org/governance/`. sagebrain-infra's existing authorizer
  keeps working unchanged regardless, via a projection built specifically to
  reproduce its exact prior contract — see "How the graph is used" in
  [Governance graph design](docs/graph-design.md).
- **DUO conditions are moving toward being sourced from the AR itself** (ACT
  annotates the Access Requirement directly; entities inherit the annotation the
  same way they inherit the AR) rather than a separately-maintained curator
  record — see `plans/ar_level_duo_annotations.md`. This isn't wired in yet,
  pending a confirmed Synapse mechanism.

For the current model in full — every class, predicate, the build pipeline, ReBAC
alignment, and the relationship to sagebrain-model — see
[Governance graph design](docs/graph-design.md) and
[Technical implementation](docs/graph-design-implementation.md). For the exact RDF
artifact each build step produces, see
[Knowledge graph representation](docs/knowledge-graph.md).

## Release artifacts and IRI policy

The governance graph is a layer of the graph defined in
[sagebrain-model](https://github.com/Sage-Bionetworks/sagebrain-model): it is loaded
into the same store, joined on the same IRIs, and read by sagebrain-infra's
authorizer. This repository owns every governance-layer term and shape, and
publishes them for other repositories to import rather than copy. The two schemas
release independently, each with its own version and published artifacts:

| Artifact | What it is |
|---|---|
| `shapes/governance_duo.owl.ttl` / `.shacl.ttl` | Record layer, generated from `linkml/governance_duo.linkml.yaml` (`make owl`/`make shacl`), versioned `VERSION` |
| `shapes/governance.owl.ttl` / `.shacl.ttl` | Graph layer, generated from `linkml/graph/governance.yaml` (`make graph-tbox`), versioned `GRAPH_VERSION` |

Each carries an `owl:Ontology` header with `owl:versionIRI` and `owl:versionInfo`.
`make release-check` runs `make validate-all` and verifies every artifact carries
its own version (and, with `TAG=v<version>`, that the tag agrees with `VERSION`).
Until a release is tagged on `main`, consumers pin a commit hash in the raw GitHub
URL; afterwards, a tag.

IRIs follow one policy for the graph layer, implemented in `scripts/graph_iris.py`
— the only place graph-layer IRIs are minted:

- **`gov:`** (`https://w3id.org/synapse/governance#`) for graph-layer terms:
  classes, slots, and vocabulary concepts.
- **`govid:`** (`https://w3id.org/synapse/governance/`) for everything the layer
  mints, shaped `<kind>/<id>`, beside the namespace above rather than inside it:
  `govid:ar/42`, `govid:authorization/syn10081783-9000001`,
  `govid:control-label/syn10081783`, `govid:derivation-review/1001`.
- **`governanceduo:`** for record-layer schema terms and non-AR record ids
  (`governanceduo:study.mc2-jax-5xfad`) — a curated `AccessRequirement` is the one
  exception, sharing its graph node's `govid:ar/<n>` IRI directly.
- **`syn:`**/**`synuser:`**/**`synteam:`** (Synapse's own URLs) for entities,
  users and teams.
- **External terms by their own IRIs, never re-minted**: `acl:`/`vcard:`/`foaf:`
  for the WAC ACL model, `prov:` for provenance, `obo:DUO_` for real DUO codes
  (`gov:DUOPlus1`–`7` for the Sage-local extensions).

The one deliberate exception is the `authorizer_v1` projection
(`projections/authorizer_v1.rq`), which re-mints its output entirely under the
pre-refactor namespace, `https://sagebionetworks.org/governance/`, to match
sagebrain-infra's existing, unmodified authorizer contract — see
[Governance graph design](docs/graph-design.md) for why.

`make owl-profile`/`make graph-owl-profile` check both schemas' OWL against the
OWL 2 DL profile, alone and merged with every canonical ABox, and check that
every `prov:` term declared has the type W3C PROV-O gives it
(`scripts/check_prov_alignment.py`); both run in CI
(`.github/workflows/validate.yml`). Two deliberate gaps between the record-layer
LinkML schema and its generated OWL are documented in `scripts/build_owl.py`: the
`rules:` conditionals are enforced by `linkml-validate`, not expressed in the OWL,
and a small schema-derived repair pass fills gaps in LinkML's OWL generator.

# Materials available in this repository

The content below predates this repository's current `linkml/`-based model (see
[LinkML representation](#linkml-representation) above) and, in places, links to files
on a separate `ar-dictionary-schema` branch rather than the current model files
described in [Repository layout](#repository-layout). It's kept for historical
reference. Two pieces of it are superseded, not just historical:

- **`schematic` is deprecated.** The CSV-based submission workflow described below
  (download/generate a CSV, validate and submit it via the `schematic` CLI) is no
  longer how records get into Synapse. **Curator Record Sets, bound to a JSON
  Schema generated straight from the LinkML model (`make json-schemas`,
  `json_schemas/`), are now the sole submission mechanism** for every class —
  including `AccessRequirement`, so a Record Set built against its schema is also
  where DUO conditions are captured (see the next point).
- **Deriving an AR's DUO annotation from a conditional JSON schema bound to a
  folder** (the mechanism the "Creating conditional JSON schemas" step below once
  described) was never put into practice and is deprecated. The adopted direction
  instead treats the `AccessRequirement` Curator Record Set itself as the DUO
  source: it's populated the same way as any other class, and the graph reads its
  DUO fields from there rather than deriving them from annotations on entities
  beneath it. See `plans/ar_level_duo_annotations.md` and
  [Use cases and data sources](docs/use-cases.md).

<details>
<summary><b>Archive</b></summary>

# governanceDUO

The Data Use Ontology (DUO) provides a helpful framework for gating access to data managed by Sage Bionetworks on the Synapse platform. 

[DUO was developed by members of the Global Alliance for Genomic Health (GA4GH)](https://github.com/EBISPOT/DUO/blob/master/README.md): "DUO allows [users] to semantically tag datasets with restriction about their usage, making them discoverable automatically based on the authorization level of users, or intended usage".

At Sage, we extended DUO modifiers for our use cases and incorporated [derived annotations](https://sagebionetworks.jira.com/wiki/spaces/PLFM/pages/2597617665/API+Changes+to+support+Extension+of+Data+Access+Management+to+Users+outside+of+Sage+ACT) as a way of scaling governance support on projects by assigning access requirements (ARs)* to entities based on its DUO annotation. 

_*ARs are applied in the form of a clickwrap (i.e., the user must agree to terms) and/or a managed access requirement (i.e., the user must provide evidence). Managed ARs may require evidence in the form of **Authentication** (e.g., training certification, profile validation, two-factor authorization) and/or **Authorization** (e.g., intended data use (IDU) statement, data use certificate (DUC), ethics approval letter from an institutional review board (IRB) or independent ethics committee (IEC))._

 - The modular data model CSV source files are archived under `archive/model/`
   (the `schematic`-driven Makefile targets that once generated artifacts from them
   were removed along with the rest of the schematic pipeline; see `Makefile`'s own
   top comment)
 - The entirety of the Sage Governance-related metadata model is available in two formats:
   - [CSV](https://github.com/mc2-center/governanceDUO/blob/ar-dictionary-schema/sage-ar.model.csv) (column format compatible with Curator tools / schematic)
   - [JSON-LD](https://github.com/mc2-center/governanceDUO/blob/ar-dictionary-schema/sage-ar.model.jsonld)


 - Empty CSV templates are available for each model type:
   - [Access Requirement](https://github.com/mc2-center/governanceDUO/blob/ar-dictionary-schema/sage-ar.AccessRequirement.manifest.csv)
   - [Resource](https://github.com/mc2-center/governanceDUO/blob/ar-dictionary-schema/sage-ar.Resource.manifest.csv)
   - [Study](https://github.com/mc2-center/governanceDUO/blob/ar-dictionary-schema/sage-ar.Study.manifest.csv)
   - [Schema](https://github.com/mc2-center/governanceDUO/blob/ar-dictionary-schema/sage-ar.Schema.manifest.csv)


 - Synapse-compatible JSON schemas are available for each model type. These can be associated or "bound" to a Synapse container and/or used to create views, Record Sets, Curator tasks, and working sessions. Current versions are linked below and numbered versions are available in the [sage-ar.model folder](https://github.com/mc2-center/governanceDUO/tree/ar-dictionary-schema/sage-ar.model)
   - [Access Requirement](https://github.com/mc2-center/governanceDUO/blob/ar-dictionary-schema/AccessRequirement_validation_schema-updated.json)
   - [Resource](https://github.com/mc2-center/governanceDUO/blob/ar-dictionary-schema/Resource_validation_schema-updated.json)
   - [Study](https://github.com/mc2-center/governanceDUO/blob/ar-dictionary-schema/Study_validation_schema-updated.json)
   - [Schema](https://github.com/mc2-center/governanceDUO/blob/ar-dictionary-schema/Schema_validation_schema-updated.json)

## Submitting metadata to the database
- A dedicated [Synapse Project](https://www.synapse.org/Synapse:syn71723047/files/) is available for programs at Sage Bionetworks to contribute Study, Resource, and AR information
- Records will be stored in the following folders on a per-program basis (one folder per program)
   - [requirements](https://www.synapse.org/Synapse:syn71723125)
   - [resources](https://www.synapse.org/Synapse:syn71723130)
   - [studies](https://www.synapse.org/Synapse:syn71723121)
   >**Note**: If a subfolder with the name of your program/DCC (e.g., "mc2", "elite") is not present in a folder linked above, please request that a new subfolder is created and configured to store your submissions.
   >**Migration note**: these type-first folders are being superseded by an automated, program-first provisioning tool (`scripts/provision_curator_infrastructure.py` — folder, Record Set, curation task, and a unified queryable view, all created in one step; see `plans/synapse_curation_infrastructure.md`), live-piloted under a test program as of 2026-09-25. This section will be updated once the older folders are archived and the new tool is the documented path for every program.
- Curation tasks associated with your program's records will be listed in the project [Metadata tab](https://www.synapse.org/Synapse:syn71723047/metadata/)
  - task names will use the format `program.dataType` (e.g., mc2.Study, adkp.Resource)
  - after accessing a task, record the requested metadata in the grid and allow it to validate
    - add as many rows as necessary to represent your program records, using the `+ Add` button
    - alternatively, document your entries in a CSV and use the `Upload` button to populate the grid
  - once you've finished adding information, select `Apply Changes` to store the entries

## Using schemas to record governance metadata (Study example)
 - **Note**: It is recommended that separate tables, Record Sets, and/or curation tasks are created within each Synapse Project under consideration.
 - Curator Record Sets are the sole mechanism (schematic-CLI CSV submission is
   deprecated — see "Materials available in this repository" above):
   - Bind the selected schema (generated by `make json-schemas`) to the folder where you intend to store the associated Record Set
   - Create a Record Set and record-based curation task using either the applicable schema URI or a path to a local version of the JSON schema
   - Select the curation task from the `Metadata` tab
   - Add Study information, one Study per row
     - If it isn't clear how to define a Study for your project, the examples in section **What should be considered a Study?** may be helpful.

<n></n>

## Additional information

<details>
<summary><b>What should be considered a Study?</b></summary>

>**In this context, a Study can be considered any one grant, publication, data source, or other grouping(s) that apply to resources (files, code, etc.) stored in a Synapse Project.** 

**Note**: If you have previously defined Studies within your program (via a Data Landscape/intake process, governance review, etc.), it is recommended that you reuse the same groupings, to ensure consistency between records.  

</details>

<n></n>
   
  - <details>

    <summary><b>Example 1</b></summary>
	  
	  - Synapse Project A has data from lab 1, lab 2, and lab 3
		- Each lab is supported by the same grant, but each data submission represents a different sub-project within the parent grant
		- Each lab belongs to an independent institution. 
	  - Suggested Study grouping: Study entries should be created for each lab (1, 2, and 3), to represent distinct data types or sharing conditions associated with the independent labs
	  
	  </details>

<n></n>

  - <details>

    <summary><b>Example 2</b></summary>

      - Synapse Projects B, C, and D have data from lab 4, lab 5, and lab 6, respectively.
	  - Suggested Study grouping: A Study Record Set should be created in each Project and populated with an entry for the single associated Study.
	
	</details>

<n></n>
  
  - <details>

    <summary><b>Example 3</b></summary>

	  - Synapse Projects E and F have data from lab 7, lab 8, and lab 9.
	    - Project E has data from lab 7 and lab 8
	    - Project F has data from lab 8 and lab 9
	    - Project E and F store distinct kinds of data

	  - Suggested Study grouping:
	    - A Study Record Set should be created in each Project
		- Lab 8 is responsible for data in both Projects, but the data is distinct and intentionally stored separately, so independent Study entries should be captured in both Projects E and F, for the data submitted by lab 8
		- Study entries for labs 7 and 9 should only be created in Synapse Projects E and F, respectively
	
	</details>

</details>
