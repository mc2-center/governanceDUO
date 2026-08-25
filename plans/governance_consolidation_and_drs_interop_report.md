# Report: Governance consolidation and DRS interoperability

Executed against [`governance_consolidation_and_drs_interop.md`](governance_consolidation_and_drs_interop.md). All three phases were implemented as planned; one implementation detail in Phase 2b diverged from the original plan text in a way that's called out explicitly below, since it changes what "schema-driven" means for that phase.

## Phase 1 — quick fixes: as planned

| Change | File(s) |
| --- | --- |
| Repointed dangling `access_requirement.123` → `access_requirement.42` | `linkml/examples/governance_graph/access_requirement_association.example.yaml`, `data_access_submission.example.yaml` |
| Added `owl:sameAs` bridge (`gov:AR-<n>` ↔ `governanceduo:access_requirement.<n>`) | `scripts/build_governance_graph.py` (`add_access_requirement_association`), `shapes/governance_graph.owl.ttl`, `shapes/governance_graph.shacl.ttl` (new property shape) |
| Fixed `Apache_2`/`GPL_3` → `Apache_2.0`/`GPL_3.0` | `model/valid_values.csv`, comment update in `linkml/mixins.yaml` |
| Added `pattern: '^syn\d+$'` to `entityIdList` | `linkml/access_requirement.yaml` |
| Documentation cross-links (no behavior change) | `linkml/governance_graph.yaml` (sagegov:/gov: equivalence, id-hyphenation), `linkml/mixins.yaml` (`createdBy` divergence), `linkml/props.yaml` + `linkml/resource.yaml` + `linkml/schema.yaml` (why `*Key` slots stay untyped — confirmed this is a real import-cycle constraint, not just style, contradicting one of the two design-pass recommendations), `linkml/policy_fabric.yaml` (`capabilityOperation` vs `AccessTypeEnum`) |

## Phase 2a — `AssetBinding` class: as planned

- New `AssetBinding` class (`synapseId`, `assetDid`) in `linkml/mixins.yaml`; `PolicyFabricMixin.assetDids` replaced by `assetBindings` (inlined list of `AssetBinding`).
- New `sourceField` slot on `ReferenceValueSource` (`linkml/policy_fabric.yaml`) so a `PolicyCardBinding` can extract a sub-field of an inlined class.
- Updated `linkml/policy_fabric_bindings.yaml`'s two `assetDids`-sourced bindings (`collaboration-required`, `publication-required`) to `sourceSlot: assetBindings` / `sourceField: assetDid`.
- Updated `linkml/examples/access_requirement_policy_fabric.example.yaml` (`assetDids: [...]` → `assetBindings: [{synapseId, assetDid}]`) and `scripts/build_policy_fabric.py` (reads `assetBindings[0].assetDid` for `asset_registration.json`'s `did`, and applies `sourceField` extraction generically for any binding).
- Updated `docs/policy-fabric.md` and `README.md`'s Policy Fabric section to describe `assetBindings`.

**Note:** discovered and fixed a second `assetDids`-sourced binding (`publication-required`, DUO:0000019) that the original plan text didn't call out explicitly by name (it only named `collaboration-required`) — both needed the same `sourceSlot`/`sourceField` update.

## Phase 2b — Governance Graph exporter: scope adjusted from the plan during implementation

**What the plan said:** add `class_uri`/`slot_uri` to `governance_graph.yaml`, then have `scripts/convert_examples_to_rdf.py`'s generic `RDFLibDumper` mechanism produce "the ~70% of the script's output that's pure naming," with only a thin (~40-line) post-processing script left for derived triples/joins.

**What was actually built, and why:** prototyping the generic-dump approach surfaced a real blocker the plan hadn't fully accounted for: `Principal` is the one class in `governance_graph.yaml` that is deliberately not `is_a: BaseEntity` for a *domain* reason, not a modeling oversight — `ACL_RESOURCE_ACCESS.GROUP_ID` is already a real, unambiguous, pre-existing natural key (Synapse's own numeric Principal/UserGroup id), unlike `AccessGrant`/`AccessRequirementAssociation`/`DataAccessSubmission`, which mint a *synthetic* `BaseEntity` id specifically because their underlying Synapse tables (`ACL`+`ACL_RESOURCE_ACCESS`+`ACL_RESOURCE_ACCESS_TYPE`, merged) have no single natural key for the first-class thing being modeled here. There's nothing to synthesize for `Principal`, and `principalId` is an integer besides — reusing `BaseEntity.id` would require both a range override and renaming `principalId` to literally `id`, sacrificing the direct `principalId` ↔ `ACL_RESOURCE_ACCESS.GROUP_ID` column traceability this schema preserves everywhere else. (This rationale previously existed only as a script comment that misattributed it to a schema-level "note" that didn't actually exist — now documented directly on `Principal`'s class definition in `governance_graph.yaml`, and the script comment corrected.)

The practical consequence for this rewrite: because `Principal` has no dotted/underscored `BaseEntity` id, `RDFLibDumper`'s CURIE-from-a-dotted-id mechanism (the one that already works for the DUO-core `governanceduo:` examples) can't mint its `gov:principal-<n>` subject URIs — that shape requires custom string formatting no generic dumper option produces. Since `AccessGrant.principal` (and other object-valued slots) reference `Principal` individuals, a genuinely generic dump would have needed a second, non-trivial ID-minting mechanism on top of the one already in `convert_examples_to_rdf.py`.

Given that, the implementation kept `scripts/build_governance_graph.py`'s explicit control flow (which triples get emitted, in what order, with what conditional logic) **unchanged**, but eliminated the actual drift risk the audit flagged — namely, hardcoded Python `GOV.<name>` constants silently diverging from the schema's own declared URIs — by having the script resolve every predicate/type URI **from the schema itself** at runtime, via two small helpers:

```python
PREDICATE(slot_name, class_name)  # SchemaView.induced_slot(...).slot_uri, resolved to a full IRI
TYPE(class_name)                 # SchemaView.get_class(...).class_uri, resolved to a full IRI
```

`governance_graph.yaml` now declares `class_uri`/`slot_uri` (under the schema-registered `sagegov:` prefix, the same IRI the script's `gov:` CURIE resolves to) on every class/slot the script emits, including per-class `slot_usage` overrides where the same shared slot (`createdBy`) needs a different predicate depending on which class uses it. This is a smaller claim than "generic dump" but a real one: **the schema is now the single source of truth for every predicate/type URI in the exported ABox** — a future rename of a `slot_uri` in the schema propagates to the script's output automatically, with no separate Python constant to remember to update. What stays genuinely hand-written (and is now documented as such in the script's module docstring and in `docs/knowledge-graph.md`) is only what has no schema-declarable source: `Principal`'s id minting, the `hasACL`/`hasAccessRequirement`/`hasApproval` derived/conditional triples, and the `.`/`_` → `-` id-hyphenation display convention.

**A useful side effect discovered during this work:** because `governance_graph.yaml`'s classes/slots now declare `sagegov:` URIs, running the *existing* `gen-owl`/`gen-shacl` generators against the umbrella schema picks them up automatically — `governance_duo.owl.ttl` now records each `sagegov:` `class_uri` as a `skos:exactMatch` annotation on the primary `governanceduo:` class (LinkML's standard treatment for a declared external-equivalent URI, the same mechanism already used for DUO term reuse), and `shapes/governance_duo.shacl.ttl`'s `sh:path` entries for these slots now correctly use the `sagegov:` predicates directly. This was not a change to any generator or its invocation — it's a consequence of the schema declarations that fell out for free, and it closes part of the original namespace-fragmentation finding without any script changes at all.

**A second, related fix discovered mid-implementation:** the same URI-resolution pass required `add_data_access_submission`'s reference to the AccessRequirement class not use `TYPE("AccessRequirement")` — that class is defined in `access_requirement.yaml` and its real `class_uri` is (correctly) `governanceduo:AccessRequirement`; the `gov:AccessRequirement` stub type in the ABox is a local, script-only display type for the same real-world thing (bridged via the Phase 1 `owl:sameAs`), not a use of the class's own declared URI. This distinction is now documented inline in the script.

**Files touched:** `linkml/governance_graph.yaml` (added `class_uri`/`slot_uri` to all relevant classes/slots, plus `slot_usage` overrides for `createdBy` on `SynapseEntity`/`DataAccessSubmission` and `createdOn` on `AccessGrant`/`DataAccessSubmission`), `scripts/build_governance_graph.py` (full rewrite around `PREDICATE()`/`TYPE()`), `shapes/governance_graph.owl.ttl` and `shapes/governance_graph.shacl.ttl` (header comments updated to describe the new architecture), `docs/knowledge-graph.md` (section 3 rewritten, Validation section's "structural quirks" list and TBox explanation updated for accuracy).

## Phase 3 — DRS interoperability: as planned, one collision fixed along the way

- New `linkml/drs_alignment.yaml`: `DrsObjectMapping` (`synapseId` reused from `mixins.yaml`'s `AssetBinding` slot rather than redefined; `drsId`, `drsSelfUri`, `aliases`), `DrsAuthorizationBinding` (`dataUseModifier`, `supportedAuthTypes` against a new `DrsAuthTypeEnum`, `passportAuthIssuers`, `notes` reused from `policy_fabric.yaml` rather than redefined), and the file's header comment documenting the Policy-Fabric/GA4GH-Passport structural-analogy design insight.
- New `docs/drs-interop.md`: the mapping explanation plus a hand-written (not generated) worked example reusing the `access_requirement.101`/`syn98765432`/`geographical-restriction`+`institution-specific-restriction` example already used in `docs/policy-fabric.md`.
- Added `drs_alignment` to the umbrella schema's `imports:` (`linkml/governance_duo.linkml.yaml`) and a link to the new doc from `docs/index.md`.
- No generator script, no `drs_export/` directory, no Makefile target — confirmed against the user's explicit scope choice.

**Collisions found and fixed during implementation:** the first draft of `drs_alignment.yaml` redefined `synapseId` and `notes` as new slots, which collided with identically-named (but differently-described) slots already added to `mixins.yaml` (Phase 2a's `AssetBinding.synapseId`) and `policy_fabric.yaml` (`PolicyCardBinding.notes`) — LinkML's schema merge raises `ValueError: Conflicting URIs ... for item: <slot>` when two imported schemas define the same global slot name differently. Fixed by having `drs_alignment.yaml` import `mixins`/`policy_fabric` and reuse those slots directly (broadening their descriptions slightly to cover both uses) rather than redefining them — this is itself a small, additional instance of the kind of consolidation this whole plan is about, caught by the tooling rather than by review.

## Tests / verification performed

All commands run from the repo root; `governance_duo.owl.ttl`/`shapes/governance_duo.shacl.ttl` are generated artifacts with non-deterministic blank-node/list ordering — reruns during Phase 1/2a were spot-checked to confirm the diff was reordering-plus-legitimate-new-content (e.g. the new `entityIdList` pattern, the new `sagegov:` `sh:path`/`skos:exactMatch` entries) before being kept, per this repo's existing convention of committing generated build artifacts.

| Check | Command | Result |
| --- | --- | --- |
| Lint | `make linkml-lint` | Exit 0 throughout (warning count rose from 93 → 96 → 100 as new camelCase slots were added — all `standard_naming` warnings, ignored per this repo's existing `--ignore-warnings` convention; no new error-level problems at any point) |
| Full validation | `make validate-all` (`shacl-validate` + `governance-graph-validate`) | `Conforms: True` for all four validation passes (OWL self-check, DUO-core instance ABox, and the Governance Graph ABox) after every phase |
| Policy Fabric regression | `make policy-fabric`; also a direct `build_policy_fabric.build()` call with a synthetic instance carrying `DUO:0000020` (to exercise the `sourceField` extraction path, which the example instance doesn't otherwise trigger) | `asset_registration.json`'s `did` unchanged (`"did:example:asset123"`); synthetic test correctly produced `datasetID: "did:example:asset123"` via the new `assetBindings[].assetDid` extraction |
| Governance Graph regression (the load-bearing check for Phase 2b) | Saved the pre-rewrite `governance_graph_export/governance_graph.ttl`, regenerated after the rewrite, compared as RDF triple sets (not raw text) via `rdflib` | **Triple-set-identical** (46 triples, `set(g1) == set(g2)` — confirmed twice, once immediately after the rewrite and once again after the subsequent docs-only edits) |
| Docs regeneration | `make docs` (after clearing `docs/reference/` and `docs/example_instances/`) | Succeeded; new `AssetBinding`, `DrsObjectMapping`, `DrsAuthorizationBinding`, `DrsAuthTypeEnum` reference pages generated correctly with embedded examples where applicable |
| Doc link check | Custom script walking `docs/*.md` for `](...)` targets, resolving each against the filesystem | Zero broken links across `docs/index.md`, `docs/linkml-model.md`, `docs/knowledge-graph.md`, `docs/policy-fabric.md`, `docs/drs-interop.md` |
| Case-collision check | Directory walk comparing lowercased paths under `docs/reference/` | Zero collisions (the `--subfolder-type-separation` fix from the prior docs session continues to hold with the new classes) |
| Stray-reference sweep | `grep -rl` for `assetDids` and `access_requirement.123` across `*.py`/`*.yaml`/`*.md`/`*.ttl` | No remaining live references outside `plans/policy_fabric_alignment.md` (an intentionally-untouched historical design doc) and one deliberate historical-context comment in `mixins.yaml` |

Nothing has been committed to git as part of this work; per standing instruction, commits happen only when explicitly requested, using granular per-phase commits.
