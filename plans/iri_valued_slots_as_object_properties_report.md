# Report: iri_valued_slots_as_object_properties.md

The six `range: uriorcurie` slots (`prov:generated`, `prov:entity`,
`sagegov:subject`, `sagegov:sourceAccessRequirements`, `sagegov:computedFrom`,
`sagegov:activity`) are now `owl:ObjectProperty` in
`shapes/governance_duo.owl.ttl`. The OWL now agrees with the data (IRI nodes),
gen-shacl (`sh:nodeKind sh:IRI`) and W3C PROV-O. Two new checks keep it that way.

## Review findings (before implementation, 2026-09-23)

- **Upstream (step 1).** 1.11.1 is the newest LinkML release on PyPI, and
  linkml `main` still has the bug. No upgrade fixes it, so step 1 needed no
  commit.
- **Root cause is narrower than the plan said.** The spurious
  `owl:allValuesFrom xsd:string` isn't produced by the restriction path
  itself. `add_class()` asks `slot_node_owltypes()` whether a slot ranges over
  individuals, and that method ignores `xsd_anyuri_as_iri`. With no filler,
  `add_class()` falls back to the schema's `default_range: string`. A minimal
  schema reproduces it (below); without `default_range` the filler is
  `owl:Thing` instead.
- **Filing an issue** conflicted with the earlier "don't file" decision.

Decisions (approved): fix `slot_node_owltypes()` in a generator subclass rather
than deleting triples afterwards; don't file the LinkML issue (draft below).
Recorded in the plan (`22d293d`).

## Changes

| step | commit | change |
|---|---|---|
| plan | `22d293d` | Record the approved D1 route and the upstream check. |
| 2 | `17a0cea` | `scripts/build_owl.py`: `xsd_anyuri_as_iri=True`; `IriRangeOwlGenerator` overrides `slot_node_owltypes()` to report `owl:Thing` (not `rdfs:Datatype`) for `xsd:anyURI` ranges when the flag is on. The filler becomes `owl:Thing`, which `skip_vacuous_local_range_axioms` drops. Module docstring explains the flag and the workaround ("remove once fixed upstream"). |
| 3 | `24a168f` | `linkml/provenance.yaml`, `linkml/derivation_policy.yaml`: the six slot descriptions and both schema descriptions say the values are IRI nodes, typed `owl:ObjectProperty`. |
| 4 | `bad5f1c` | Regenerated `shapes/governance_duo.owl.ttl`, `.shacl.ttl` and `docs/reference/`. |
| 5 | `c647dda` | `scripts/check_prov_alignment.py` plus a `make owl-profile` step: every `prov:` term both TBoxes declare must carry a type PROV-O gives it, and must be declared in PROV-O at all. PROV-O (the 2013-04-30 Recommendation) is fetched once to `build/prov-o-20130430.ttl` (`PROV_O`, `PROV_O_URL` overridable). |
| 6 | `35b6f62` | `scripts/check_sagebrain_contract.py`: new part 2 runs the same `type_mismatches()` against sagebrain-model's `ontology/imports/prov.ttl`. The comment on `EXTERNAL_VOCABULARIES` explains why leaving `prov.ttl` out of the DL union no longer hides this conflict. |
| — | `5c6f2ab` | README, `docs/graph-design.md`: describe the new checks. CI caches `build/prov-o-20130430.ttl` alongside ROBOT. |

**OWL diff.** Exactly the six properties change: `owl:DatatypeProperty` becomes
`owl:ObjectProperty`, and each loses `rdfs:range xsd:anyURI`. No class
restriction is added. The only other changes are the updated
`skos:definition` text. The `Repairs:` log's `reserved_removed` count drops from
5 to 3: owlgen no longer writes `allValuesFrom xsd:anyURI` on the two
`owl:sameAs` slots, so there are fewer restrictions to remove.

**SHACL.** Same 7,593 triples. The only differences are the six updated
`sh:description` literals (compared with blank nodes abstracted away), so no
constraint changed.

## Verification

- **`make owl-profile`:** passes. `governance_duo`, `governance_graph` and their
  merge are each OWL 2 DL. The PROV-O check passes.
- **The new check catches the old OWL.** Run against the OWL as of `22d293d`,
  `check_prov_alignment.py` exits 1 and names exactly `prov:entity` and
  `prov:generated` ("is owl:DatatypeProperty, PROV-O declares it
  owl:ObjectProperty").
- **DL with PROV-O loaded.** ROBOT 1.9.8 DL run on the new OWL +
  `governance_graph.owl.ttl` + sagebrain-model's `ontology/imports/prov.ttl`:
  - before: 35 violations, 21 of them this repo's puns on
    `prov:entity`/`prov:generated` (the plan's 14 + 7);
  - after: 14 violations, the same 14 that `prov.ttl` gives on its own
    (`prov:specializationOf`/`prov:wasRevisionOf`). Nothing comes from this
    repo.
- **`make validate-all`:** exit 0. That covers every SHACL validation, including
  `provenance-validate` and `derivation-policy-validate`, plus
  `sync-provenance-check`, `derivation-policy-check` (6 assertions),
  `infra-contract-check` and `owl-profile`. The example-RDF and SHACL rebuilds
  gave reordering-only diffs (isomorphic or same signature), which were
  discarded, per the earlier "accept the churn" decision.
- **Determinism:** two consecutive `make owl` builds are byte-identical.
- **`linkml-lint`:** exit 0. `mkdocs build --strict`: passes.
- **`make sagebrain-contract-check`** against `~/sagebrain-model`
  (branch `governance-layer-import`, working tree as found):
  - PROV type agreement: **pass**.
  - ControlLabel reaches the Association: **pass**.
  - OWL 2 DL union: **fails, as expected until the follow-up.** sagebrain's
    `ontology/imports/governance_layer.ttl` is still the MIREOT extract from
    `9e398af`, which declares `prov:generated`/`prov:entity` as
    `owl:DatatypeProperty`. Alongside this repo's new object properties, those
    are 7 puns. They go away once the import is regenerated.
  - SHACL on the joined example: **fails, but not because of this work.** It
    fails identically at `22d293d`, before this work:
    - "A Usage must be either a Synapse entity reference ... or an external
      tool reference";
    - "An Activity needs at least one prov:qualifiedUsage input".

    The sagebrain-model working tree has uncommitted
    `ontology/shacl/governance_layer.shacl.ttl` and
    `ontology/governance/provenance_bridge.ttl`, so this likely belongs to that
    in-progress import work.

## Follow-up in sagebrain-model (unchanged from the plan)

Push this branch, then:
1. Bump `GOVERNANCEDUO_COMMIT` in sagebrain-model's `scripts/import.sh` to the
   new head.
2. Re-run `scripts/import.sh governance_graph governance_layer governance_layer_shapes`.
3. Re-run `make sagebrain-contract-check`; the DL union should then pass.

`plans/governance_layer_import.md` then resumes at step 2. Look into its SHACL
failure separately.

## Draft linkml issue (not filed, per decision)

> **owlgen: `xsd_anyuri_as_iri` slots get `owl:allValuesFrom <default_range>`**
>
> With linkml 1.11.1 (and `main`), `gen-owl --xsd-anyuri-as-iri` on
>
> ```yaml
> id: https://example.org/mini
> name: mini
> prefixes: {linkml: https://w3id.org/linkml/, ex: https://example.org/}
> imports: [linkml:types]
> default_prefix: ex
> default_range: string
> classes:
>   Activity: {slots: [generated]}
> slots:
>   generated: {range: uriorcurie}
> ```
>
> declares `ex:generated a owl:ObjectProperty` but restricts
> `Activity` with `[ owl:allValuesFrom xsd:string ; owl:onProperty ex:generated ]`:
> a datatype filler on an object property, which OWLAPI can't parse.
> `slot_node_owltypes()` doesn't consult `xsd_anyuri_as_iri`, so for these
> slots it never reports `owl:Thing`. `transform_class_slot_expression()`
> returns no filler, and `add_class()` falls back to `default_range` because
> `OWL.Thing not in owltypes`. Without `default_range` the filler is `owl:Thing`.
> Suggested fix: in `slot_node_owltypes()`, add `OWL.Thing` (not
> `RDFS.Datatype`) when `self.xsd_anyuri_as_iri and is_xsd_anyuri_range(sv, range)`.
