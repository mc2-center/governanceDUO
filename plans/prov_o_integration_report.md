# Report: PROV-O integration (Provenance Graph + Derivation Policy Graph)

Executed against [`prov_o_integration.md`](prov_o_integration.md). All four phases
from Section 8 were implemented (Phase 5 — enforcement/revocation — remains
explicit future work, as the plan itself specifies). Two implementation-time
refinements to the written plan, both discovered while building rather than
anticipated in advance — see their own sections below.

## Phase 1 — Provenance Graph schema + example-driven RDF/SHACL: as planned, one refinement

Added `linkml/provenance.yaml` (`Activity`/`Usage`), imported into
`governance_duo.linkml.yaml` alongside `derivation_policy.yaml` (new). Both stay in
the `governanceduo:` namespace — no `gov:`/`syn:` reserialization — so `make owl`/
`make shacl` already regenerate their shapes as part of
`shapes/governance_duo.owl.ttl`/`.shacl.ttl`; **no separate `shapes/provenance.*`/
`shapes/derivation_policy.*` files were created**, unlike what the written plan's
Section 10 table proposed. This is the first refinement: empirically confirmed this
session that `class_uri` annotations (e.g. `Activity`'s `prov:Activity`) *are*
honored by `RDFLibDumper` for instance typing (`governanceduo:activity.1001 a
prov:Activity` came out of a plain dump with no extra code) — the exact mechanism
`docs/knowledge-graph.md` already documents as working generically, just not
previously exercised for a schema-owned-but-externally-typed class. That made a
`build_governance_graph.py`-style bespoke exporter unnecessary for this layer:
`scripts/convert_examples_to_rdf.py` (already schema-agnostic — derives its CURIE
prefix from `schemaview.schema.default_prefix`) works unmodified for
`linkml/examples/provenance/`/`linkml/examples/derivation_policy/`, needing only two
new `EXAMPLE_CLASSES` entries (`activity`, `derivation_rule`, `derivation_review`).

Second refinement: `Activity.generated`/`Usage.entity` are `prov:generated`/
`prov:entity` (the Activity-to-Entity direction), not a `wasGeneratedBy` slot added
onto `SynapseEntity` itself — the written plan assumed the latter. Adding a slot to
`SynapseEntity` from `provenance.yaml` would need `governance_graph.yaml` to import
`provenance.yaml` for the slot's range, while `provenance.yaml` already imports
`governance_graph.yaml` for `SynapseEntity`/`Principal` — a circular import LinkML
doesn't allow. `prov:generated`/`prov:wasGeneratedBy` are formally inverse
properties describing the same fact, so this direction needed no edit to
`governance_graph.yaml` at all.

New example: `linkml/examples/provenance/activity.example.yaml` — an `Activity`
with one non-executed input (`syn10081783`, already exemplified in
`linkml/examples/governance_graph/`) and one executed input (a pipeline script).
`make provenance-example-rdf`/`make provenance-validate` both pass
(`Conforms: True` against `shapes/governance_duo.owl.ttl`/`.shacl.ttl`).

## Phase 2 — live sync extension: as planned, simpler than sync_governance_graph.py's own precedent

`scripts/sync_provenance_graph.py` (new) calls `GET /entity/{id}/generatedBy`
(confirmed to exist against rest-docs.synapse.org this session, OAuth `view` scope)
and builds one `linkml_runtime` `Activity`/`Usage` object per entity, dumped via
`RDFLibDumper` — no manual `PREDICATE()`/`TYPE()` triple construction needed, since
(per Phase 1's refinement) this layer needs no reserialization. `add_was_derived_from()`
derives `prov:wasDerivedFrom` as a script-computed convenience edge (no LinkML slot
backs it, same treatment as `gov:hasACL`), reused unchanged by
`build_derivation_policy.py` (Phase 4). Untested against live Synapse in this
environment (no credentials) — same caveat the plan itself carries forward from
`governance_graph_ingestion_report.md`'s own sync script.

## Phase 3 — Derivation Policy Graph schema: as planned, plus one required schema fix

Added `linkml/derivation_policy.yaml` (`DerivationRule`, `ControlLabel`,
`DerivationReview`, `DerivationReviewStatusEnum`). One thing the written plan didn't
anticipate: `scripts/build_governance_graph.py`'s reusable `PREDICATE()`/`TYPE()`
helpers (which `build_derivation_policy.py` reuses, per Section 4's own intent to
reuse rather than reinvent) require an explicit `slot_uri`/`class_uri` on every
slot/class they resolve — confirmed empirically that a slot with no explicit
`slot_uri` (including the shared `dataTier` slot from `mixins.yaml`, which declares
none of its own) comes back `None` from `induced_slot()`, not a computed default.
Added explicit `slot_uri: governanceduo:<name>` to every new `derivation_policy.yaml`
slot (including a `slot_usage` override for the reused `dataTier` slot on
`ControlLabel`) and explicit `class_uri: governanceduo:<Name>` to all three new
classes, rather than relying on LinkML's implicit default. `make owl`/`make shacl`/
`linkml-lint` all still pass cleanly (140 pre-existing camelCase warnings only, exit
0) after this fix.

Illustrative examples added: `derivation_rule.example.yaml` (Controlled+Controlled →
requires review) and `derivation_review.example.yaml` (a hand-authored composite-risk
case, referencing `activity.1001` and two `Controlled`-tier `ControlLabel`s bound to
different `AccessRequirement`s) — both explicitly flagged in-file as illustrative,
matching `AccessRequirementTemplate`/`Program`/`Site`'s own "honest grounding note"
treatment. `make derivation-policy-example-rdf`/`make derivation-policy-validate`
both pass.

## Phase 4 — `build_derivation_policy.py`'s two computations: as planned, one honest gap surfaced

`scripts/build_derivation_policy.py` (new) implements `compute_control_labels()`
(memoized ancestry walk over `prov:wasDerivedFrom`, taking max `DataTierEnum` rank
across an entity and its full ancestry, consulting `DerivationRule` for an explicit
`resultingDataTier` override at each join point) and `compute_derivation_reviews()`
(one `DerivationReview` per multi-input `Activity` whose inputs' `ControlLabel`s cite
disjoint `sourceAccessRequirements`, and/or whose input-tier combination a
`DerivationRule` marks `requiresReview`/not-`permitted`) — kept as two explicitly
separate passes per the plan's own instruction.

`local_id()` was added to handle a real cross-file join problem the written plan
didn't call out: `Usage.entity`/`Activity.generated`/`ControlLabel.subject` serialize
as bare relative IRIs (per `provenance.yaml`'s own documented `uriorcurie` choice),
which rdflib resolves against *each file's own path* as base when parsed
independently — confirmed empirically that the same conceptual id
(`syn10081783`) comes back as a different absolute URI depending on which file it
was read from. `local_id()` strips every value back to its bare trailing local name
before comparison, sidestepping the inconsistency rather than forcing a shared
parse-time base across independently-built files.

`make derivation-policy` runs end-to-end against this repo's real example data
(`linkml/examples/provenance/rdf/all_examples.ttl` +
`governance_graph_export/governance_graph.ttl`) and produces an honest, correctly-computed
**empty** result: 2 `ControlLabel`s computed but neither has a populated `dataTier`
(the one real curated `AccessRequirement`, `access_requirement.42`, has no `dataTier`
set — it was never required to, since its `dataUseModifiers` don't include
`DUOPlus5`), and 0 `DerivationReview`s (the one real `Activity` example has only one
non-executed input, so no multi-input join exists to flag). This is not a bug — it
correctly reflects that no real curated AR in this repo has a populated `dataTier`
yet, the same "structural capability, not yet real-data-complete" honesty this
schema's own "Honest grounding note" already flags for `DerivationRule`. The
algorithm itself was verified independently with a synthetic disjoint-AR
two-Controlled-input case (not committed to the repo — a throwaway check this
session), which correctly produced one `Flagged` `DerivationReview` and a max-rank
`ControlLabel` on the output entity; see this report's own construction for the
exact inputs/assertions if that check needs reproducing.

## Verification — all passed

- `linkml-lint --ignore-warnings linkml/governance_duo.linkml.yaml`: exit 0, 140
  pre-existing camelCase warnings only, no new problems.
- `make owl` / `make shacl`: regenerate cleanly (only pre-existing DUO-term/
  deprecation warnings).
- `make shacl-validate`: `Conforms: True` (unchanged from before this change).
- `make governance-graph-validate`: `Conforms: True` (unchanged).
- `make provenance-validate`: `Conforms: True` on both
  `shapes/governance_duo.owl.ttl` and `linkml/examples/provenance/rdf/all_examples.ttl`.
- `make derivation-policy-validate`: `Conforms: True` on both
  `shapes/governance_duo.owl.ttl` and `linkml/examples/derivation_policy/rdf/all_examples.ttl`.
- `make validate-all`: all four validate targets pass together.
- `make derivation-policy`: runs end-to-end, computes 2 `ControlLabel`s / 0
  `DerivationReview`s (see Phase 4's honest-gap note above).
- `make docs` / `make docs-build` (`mkdocs build --strict`): exit 0, new
  `docs/reference/classes/{Activity,Usage,DerivationRule,ControlLabel,DerivationReview}.md`
  generated, no broken links or strict-mode errors.

## Files touched

New: `linkml/provenance.yaml`, `linkml/derivation_policy.yaml`,
`linkml/examples/provenance/activity.example.yaml`,
`linkml/examples/derivation_policy/derivation_rule.example.yaml`,
`linkml/examples/derivation_policy/derivation_review.example.yaml`,
`scripts/sync_provenance_graph.py`, `scripts/build_derivation_policy.py`.
Modified: `linkml/governance_duo.linkml.yaml` (imports + description),
`scripts/convert_examples_to_rdf.py` (`EXAMPLE_CLASSES`), `Makefile` (new targets:
`provenance-example-rdf`, `provenance-validate`, `sync-provenance-graph`,
`derivation-policy-example-rdf`, `derivation-policy-validate`, `derivation-policy`;
`validate-all` extended), `shapes/governance_duo.owl.ttl`/`.shacl.ttl`
(regenerated), `docs/knowledge-graph.md` (new Section 4), `README.md` (layout table
+ prov: mappings paragraph), `docs/reference/**` (regenerated), `docs/example_instances/**`
(regenerated, unchanged content for pre-existing files).
Not modified: `shapes/governance_graph.owl.ttl`/`.shacl.ttl` (hand-authored,
out of scope — neither layer touches the `gov:`/`syn:` namespace),
`scripts/build_governance_graph.py`/`scripts/sync_governance_graph.py` (reused via
import, unchanged).
