# Type IRI-valued slots as OWL object properties

## Context

sagebrain-model's `plans/governance_layer_import.md` MIREOT-imports this repo's
`shapes/governance_duo.owl.ttl` at `9e398af`. That import is paused: the
imported terms can't be loaded next to W3C PROV-O without breaking OWL 2 DL.

`build_owl.py` declares every `range: uriorcurie` slot as
`owl:DatatypeProperty` with `rdfs:range xsd:anyURI`. That's LinkML's default for
`uri`/`uriorcurie`. The data never uses these slots as literals. The RDF dumper
and the builders write IRI nodes (`prov:generated syn:syn26999999`), and this
repo's own generated SHACL already says `sh:nodeKind sh:IRI` for them
(`shapes/governance_duo.shacl.ttl`, the `prov:generated` property shape). So
the OWL contradicts the ABox and its own shapes. The slots affected:

| slot | slot_uri | defined in |
|---|---|---|
| `generated` | `prov:generated` | `linkml/provenance.yaml:134` |
| `entity` | `prov:entity` | `linkml/provenance.yaml:167` |
| `subject` | `sagegov:subject` | `linkml/derivation_policy.yaml:184` |
| `sourceAccessRequirements` | `sagegov:sourceAccessRequirements` | `linkml/derivation_policy.yaml:191` |
| `computedFrom` | `sagegov:computedFrom` | `linkml/derivation_policy.yaml:201` |
| `activity` | `sagegov:activity` | `linkml/derivation_policy.yaml:214` |

(`sameAs` and `studyId` are also `uriorcurie`, but map to `owl:sameAs`, whose
declaration `repair_generator_output()` already leaves out.)

The two `prov:` slots also contradict W3C PROV-O, which declares
`prov:generated` and `prov:entity` as `owl:ObjectProperty`. sagebrain-model
loads PROV-O (`ontology/imports/prov.ttl`) in its governance build. Measured
with ROBOT 1.9.8 `validate-profile --profile DL` on
`governance_duo.owl.ttl` + `governance_graph.owl.ttl` + that `prov.ttl`:

- 14 puns on `prov:entity` and 7 on `prov:generated`, all caused by this repo;
- 6 on `prov:specializationOf` and 7 on `prov:wasRevisionOf`. These come from
  PROV-O itself and occur without this repo's files loaded. They are out of
  scope.

`scripts/check_sagebrain_contract.py` didn't catch this because its union
leaves out `prov.ttl`/`duo.ttl` (`EXTERNAL_VOCABULARIES`, `:68`) to avoid
PROV-O's own puns. That also skips the one conflict this repo can cause.

### Why the generator options don't work as-is (LinkML 1.11.1)

Tested on scratch builds of `build_owl.py`, with no repo changes:

1. **`OwlSchemaGenerator(xsd_anyuri_as_iri=True)`.** This is LinkML's intended
   switch: `uri`/`uriorcurie` slots become `owl:ObjectProperty` with no
   `rdfs:range`, matching gen-shacl's `sh:nodeKind sh:IRI`. It retypes all six
   slots correctly. But its class-restriction path also adds
   `[ owl:allValuesFrom xsd:string ; owl:onProperty <slot> ]` on each of them
   (an object property restricted to a datatype). OWLAPI can't parse those,
   and the output gets 39 `owlapi/error#ErrorN` classes plus about 100
   cascading puns on unrelated slots (`dcterms:identifier`, `synapseId`, every
   `*Key`). It's much worse than today.
2. **Per-slot `implements: [owl:ObjectProperty]`.** This changes the declared
   type only. It keeps `rdfs:range xsd:anyURI`, which is a datatype range on an
   object property and still not DL.

Before choosing a workaround, check whether a LinkML release after 1.11.1
fixes (1). `pip index versions linkml` returned nothing from this machine, so
this hasn't been checked. `requirements.txt` pins only `linkml>=1.8`.

## Decisions (open, need approval)

- **D1, route.** Recommended: turn on `xsd_anyuri_as_iri=True` in `build()`.
  - If a newer LinkML release fixes the spurious `allValuesFrom xsd:string`
    restrictions, raise the `requirements.txt` floor to it. No workaround.
  - Otherwise add a fourth repair to `repair_generator_output()`: remove class
    restrictions whose `owl:onProperty` is an `xsd_anyuri_as_iri`-promoted
    slot and whose filler is an XSD datatype. It's the same kind of fix as the
    existing three, uses only the schema, and is marked "remove once fixed
    upstream". File a LinkML issue with a minimal schema and link it from the
    docstring. **This is a workaround and needs approval before it ships.**
  - Rejected: `range: SynapseEntity` (or `Activity`/
    `AccessRequirementReference`). That would bring back the `sh:class` failure
    `provenance.yaml`'s description gives as the reason for `uriorcurie`: the
    referenced individual isn't in this schema's example ABox.
- **D2, scope.** All six slots, not just the two `prov:` ones. The four
  `sagegov:` slots carry IRIs too (`build_derivation_policy.py` emits
  `URIRef`s since `sagebrain_contract_and_owl_dl_fixes` step 7), so leaving
  them as datatype properties keeps the OWL/data contradiction for no reason.
  A global flag covers them anyway.
- **D3, version.** Keep `owl:versionInfo` 0.1.0: no tag exists yet, so
  consumers pin commits, and the new commit is the new pin. Bump instead if a
  `v0.1.0` tag lands before this does.

## Approach

Each numbered step is one commit. The plan itself is committed first on its
own.

1. **Upstream check.** Try the newest LinkML release on a scratch build. If it
   emits no `allValuesFrom <xsd:*>` on the promoted slots, record the version
   for step 2. If not, file the LinkML issue (minimal schema: one class, one
   `range: uriorcurie` slot, `xsd_anyuri_as_iri=True`) and bring the D1
   workaround back for approval before step 2.
2. **`scripts/build_owl.py`.**
   - Pass `xsd_anyuri_as_iri=True`.
   - Either raise `requirements.txt`'s LinkML floor, or add the approved
     repair to `repair_generator_output()` with its count in the `Repairs:`
     log line.
   - Module docstring: add a bullet for the flag and why (OWL agreeing with
     the ABox, gen-shacl and W3C PROV-O).
3. **Slot descriptions.** In `linkml/provenance.yaml` and
   `linkml/derivation_policy.yaml`, the six descriptions say "range is
   uriorcurie, not X". Add that the value is an IRI node, typed
   `owl:ObjectProperty` in the OWL. Update the matching paragraph of
   `provenance.yaml`'s schema description.
4. **Regenerate** `shapes/governance_duo.owl.ttl`/`.shacl.ttl` (`make owl`
   and `make shacl`) and `docs/reference/` (`make docs`). The
   SHACL should be unchanged; confirm it.
5. **PROV-O agreement check.** Add `scripts/check_prov_alignment.py` and call
   it from the `owl-profile` target. It:
   - fetches W3C PROV-O (the 2013-04-30 REC, `https://www.w3.org/ns/prov-o-20130430`)
     into `build/`, cached like `tools/robot.jar`;
   - for every `prov:` IRI declared in `governance_duo.owl.ttl`, asserts its
     `owl:ObjectProperty`/`owl:DatatypeProperty`/`owl:Class` type matches
     PROV-O's;
   - fails with the offending terms listed.

   This checks declared types directly, not a DL run over a union with
   PROV-O, so PROV-O's own puns don't make it noisy.
6. **Contract check.** In `scripts/check_sagebrain_contract.py`, add the
   same type-agreement assertion against sagebrain-model's
   `ontology/imports/prov.ttl`. The DL union still leaves out
   `EXTERNAL_VOCABULARIES`. Update the comment at `:67` to say why the
   conflict this repo could cause is covered anyway.
7. **Report.** Write `plans/iri_valued_slots_as_object_properties_report.md`.

## Verification

- `make owl-profile`: `governance_duo.owl.ttl`, `governance_graph.owl.ttl` and
  their merge each pass DL. The new PROV-O check passes. If step 2's build is
  temporarily reverted to the old setting, the check fails and names
  `prov:generated` and `prov:entity`.
- A DL run over the merge plus sagebrain-model's `ontology/imports/prov.ttl`
  reports only PROV-O's own `prov:specializationOf`/`prov:wasRevisionOf` puns,
  with none on `prov:entity`/`prov:generated`.
- `make validate-all`, `make provenance-validate` and
  `make derivation-policy-check` pass unchanged (entailment is off, so the
  SHACL results shouldn't move).
- `make sagebrain-contract-check SAGEBRAIN_MODEL=<path>` passes, including
  the new type-agreement assertion.
- Rebuilding twice gives byte-identical `governance_duo.owl.ttl` (the
  `stable_graph()` guarantee still holds).

## Follow-up in sagebrain-model

Push, then bump `GOVERNANCEDUO_COMMIT` in sagebrain-model's
`scripts/import.sh` to the new commit and re-run
`scripts/import.sh governance_graph governance_layer governance_layer_shapes`.
`ontology/imports/governance_layer.ttl` should then declare
`prov:generated`/`prov:entity` as `owl:ObjectProperty`. After that,
`plans/governance_layer_import.md` resumes at step 2.
