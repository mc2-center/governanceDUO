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
