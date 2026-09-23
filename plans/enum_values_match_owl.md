# Make enum values agree with the OWL

## Context

This is open item 1 of `plans/pre_pr_review_fixes_report.md`. Of the schema's
17 enums, only `DataUseModifierEnum` (DUO codes) and `SourceSystemEnum` give
their permissible values `meaning:` IRIs. For the other 15, owlgen invents
member IRIs (`governanceduo:<Enum>#<value>`) that no data uses, types every
enum-ranged slot `owl:ObjectProperty`, and models the enum as a class. The
data does one of two other things:

- **Graph enums** (`AccessTypeEnum`, `ApprovalStateEnum`, `BindingTypeEnum`,
  `SubmissionStateEnum`, `PrincipalTypeEnum`): `build_governance_graph.py`
  writes `gov:<value>` IRIs (`gov:DOWNLOAD`, `gov:Direct`, `gov:APPROVED`; the
  principal type as `rdf:type gov:User`). The hand-written
  `governance_graph.shacl.ttl` expects those IRIs, and sagebrain-infra's
  authorizer reads `gov:permission` by local name.
- **Literal enums** (the other 10: AccessRequirementConcreteType, Credential
  Type, DataPermission, DataTier, DeidentificationType, DerivationReviewStatus,
  DrsAuthType, GeographicalRegion, License, StudyIndexDate): the RDF dumper and
  `build_derivation_policy.py` write plain strings (`"Controlled"`,
  `"Flagged"`, `"US"`), and gen-shacl already constrains them with `sh:in`
  string lists. A literal on an object property is not OWL 2 DL wherever the
  data meets the TBox.

In both cases only the OWL disagrees.

### Why a generator workaround is needed (LinkML 1.11.1 and `main`)

LinkML's switch for a string-valued enum is `implements: [rdfs:Literal]`.
owlgen honors it only partly:

1. The enum is still declared `owl:Class` as well as `rdfs:Datatype`, which is
   an illegal pun.
2. `owl:oneOf` is attached directly to the named datatype rather than through
   a datatype definition (`owl:equivalentClass [ a rdfs:Datatype ; owl:oneOf
   (...) ]`).
3. `slot_owl_type()` returns `owl:ObjectProperty` for every enum range.

A scratch generator subclass that corrects all three gives a DL-valid OWL on
a one-enum schema (the only violations left are the undeclared annotation
properties that `build_owl.py` already declares).

## Decisions (approved 2026-09-23)

- **Graph enums:** permissible values get `meaning: sagegov:<value>`: the IRIs
  the builders already write, so the exported graph doesn't change.
  - Known trade-off: `ApprovalStateEnum.APPROVED` and
    `SubmissionStateEnum.APPROVED` share `gov:APPROVED`, as the data already
    does. The predicate (`gov:status` vs `gov:state`) keeps them apart. Giving
    them different definitions, or declaring the enums disjoint, would later
    need distinct IRIs.
  - `PrincipalTypeEnum` gets `sagegov:User`/`sagegov:Team`, the classes the
    builder already asserts.
- **Literal enums:** marked `implements: [rdfs:Literal]` in the schema. The
  OWL models each as a named `rdfs:Datatype` defined by `owl:oneOf` its strings,
  and its slots become `owl:DatatypeProperty`. The generator subclass carries
  the three corrections (approved workaround; remove once fixed upstream).
- **Out of scope:** `DataUseModifierEnum`'s `Pending Annotation` has no
  `meaning:`, so the dumper writes it as a literal on an object property. No
  example uses it, and the builder mints no Condition for it. It's recorded,
  not fixed.

## Approach

One commit per step.

1. **Schema.**
   - `meaning: sagegov:<value>` on every value of the five graph enums.
   - `implements: [rdfs:Literal]` on the ten literal enums.
   - Enum descriptions updated where they claim otherwise.
2. **`scripts/build_owl.py`.** The generator subclass (renamed
   `GovernanceOwlGenerator`, since it now carries two fixes) adds:
   - `add_enum()`: for a literal enum, drop `owl:Class` and move its
     `owl:oneOf` into an `owl:equivalentClass` datatype definition;
   - `slot_owl_type()`: `owl:DatatypeProperty` for a literal-enum range;
   - `slot_node_owltypes()`: `rdfs:Datatype` for a literal-enum range.

   Update the module docstring.
3. **Builders.** `build_governance_graph.py` resolves every graph-enum value
   through `enum_iri()` (its `meaning:`) instead of `GOV[value]`, so the schema
   decides the IRI. The output must be unchanged. Update the module docstring
   paragraph that says these enums carry no `meaning:`.
4. **Enum check.** `check_domain_range.py` stops skipping enum ranges and
   checks membership instead:
   - an object property ranging over a class-union enum must take member IRIs;
   - a datatype property ranging over a literal enum must take one of its
     `owl:oneOf` strings.

   It must fail on the OWL from before this plan.
5. **Regenerate** the OWL, SHACL, example RDF, governance-graph export and
   docs. Any changes to example RDF or SHACL must come only from the graph
   enums' new IRIs (e.g. a record's `accessType` becomes `gov:DOWNLOAD`).
   Confirm with the drift check against the pre-change head.
6. **Report.** Write `plans/enum_values_match_owl_report.md`.

## Verification

- `make validate-all` passes, including the extended domain/range check.
- `make owl-profile` passes: governance_duo, governance_graph and their merge
  are DL, and the PROV-O check passes.
- The OWL has no `governanceduo:<Enum>#` IRIs left for any of the 15 enums.
- A DL run over the merged TBoxes plus the exported and example graphs
  reports no violations caused by enum values.
- The exported governance graph is unchanged (drift check).
- `make sagebrain-contract-check` passes.
