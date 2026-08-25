# Plan: Close alignment gaps across DUO / Policy Fabric / Governance Graph, and design DRS interoperability

## Context

Two prior sessions built out `docs/` (narrative + auto-generated reference) and a TBox/SHACL pair for the Governance Graph's `gov:`/`syn:` ABox. Writing that documentation surfaced — and a two-agent audit of the repo confirmed — that the three sections (DUO core, Policy Fabric, Governance Knowledge Graph) had accumulated real, concrete misalignments: namespace splits with no declared identity links, three parallel identifier schemes for "the same Synapse entity," inconsistent referential-integrity rigor, and a structural asymmetry where Policy Fabric's crosswalk is schema-first but the Governance Graph's RDF was hand-written in Python with shapes retrofitted afterward. Separately, the user wanted to know whether this harmonized graph could interoperate with the GA4GH Data Repository Service (DRS) API — research showed DRS's `Authorizations`/Passport-Visa discovery model is a close structural cousin of Policy Fabric's Verifiable-Credential model, and DRS explicitly leaves the authorization *decision* logic (which Policy Fabric already implements) out of scope for implementers to fill.

Two independent design passes (pragmatic minimal-fix vs. structural unification) converged on most items; where they diverged, the user chose: **(1)** the majority schema-driven rewrite of the Governance Graph exporter, **(2)** replacing `assetDids`/`entityIdList`'s comment-only pairing with an inlined `AssetBinding` class, and **(3)** DRS interoperability as design + docs only (no generator script, no live server).

Goal: three phases — quick low-risk fixes, two chosen structural consolidations, and an additive DRS-alignment design — that leave the repo genuinely more consistent without breaking any currently-passing `make validate-all`/`make policy-fabric`/`make governance-graph` output.

## Phase 1 — Quick, low-risk fixes

1. **Fix the dangling `access_requirement.123` reference.** `linkml/examples/governance_graph/access_requirement_association.example.yaml` and `data_access_submission.example.yaml` both referenced an AR id with no matching example instance anywhere. Repoint both to `access_requirement.42` (the existing, real example).
2. **Add the missing `owl:sameAs` bridge.** In `scripts/build_governance_graph.py`, wherever an `AccessRequirement` stub node is minted, also emit `gov:AR-<n> owl:sameAs governanceduo:access_requirement.<n>`. Update `shapes/governance_graph.owl.ttl`'s comment.
3. **Fix the `LicenseEnum` spelling mismatch.** Align `model/valid_values.csv` to the `.0`-suffixed spelling (`Apache_2.0`/`GPL_3.0`) already used by `model/shared.model.csv` and the enum itself.
4. **`entityIdList` gets a real pattern.** Add `pattern: '^syn\d+$'` to `entityIdList` in `linkml/access_requirement.yaml`.
5. **Documentation cross-links** (comments only, no behavior change) in `governance_graph.yaml` (sagegov:/gov: equivalence, id-hyphenation convention), `mixins.yaml` (`createdBy`'s per-class RDF-shape divergence), `props.yaml`/`resource.yaml`/`schema.yaml` (why the `*Key` foreign-key slots stay untyped strings — a real import-cycle constraint, confirmed technically necessary, not just a stylistic choice), and `policy_fabric.yaml` (`capabilityOperation` vs. `AccessTypeEnum`).

## Phase 2 — Chosen structural consolidations

### 2a. Replace `assetDids`/`entityIdList` positional pairing with an inlined `AssetBinding` class

Add `AssetBinding` to `mixins.yaml` (slots `synapseId`, `assetDid`). `PolicyFabricMixin` gets a new `assetBindings` slot (inlined list of `AssetBinding`), replacing `assetDids`. `linkml/policy_fabric.yaml`'s `ReferenceValueSource` gets a new `sourceField` slot to say which sub-field of an inlined class to extract. Update `policy_fabric_bindings.yaml`'s two `assetDids`-sourced bindings, the example instance, and `scripts/build_policy_fabric.py`.

### 2b. Majority schema-driven rewrite of the Governance Graph exporter

Add `class_uri`/`slot_uri` LinkML annotations to `governance_graph.yaml`'s classes/slots pointing at the `sagegov:` prefix (same IRI the script hardcodes as `gov:`). Rewrite `scripts/build_governance_graph.py` to resolve every predicate/type it emits from those declarations at runtime (`SchemaView.induced_slot()`/`get_class()`) instead of hardcoding independent Python constants — closing the schema/script drift risk. Keep hand-written only what has no schema-declarable source: Principal's bare-integer id minting, the `hasACL`/`hasAccessRequirement`/`hasApproval` derived/conditional triples, and the id-hyphenation display convention. **Required verification**: diff the regenerated ABox against the pre-change committed version — must be triple-set-identical.

## Phase 3 — DRS interoperability: design + docs only

New `linkml/drs_alignment.yaml` module: `DrsObjectMapping` (how a Synapse entity maps onto a DRS `DrsObject`'s `id`/`self_uri`/`aliases` — Synapse ids become the canonical DRS id, everything else rides in `aliases`) and `DrsAuthorizationBinding` (crosswalks a DUO code to DRS's `Authorizations` discovery shape). Document the core insight: GA4GH Passports/Visas and Policy Fabric's Verifiable-Credential model are structurally analogous, so Policy Fabric's Rego evaluator is a plausible drop-in for the authorization-decision logic DRS explicitly leaves out of scope. New `docs/drs-interop.md` with a hand-written illustrative worked example built from data already in the repo. No generator script, no `drs_export/` directory, no Makefile target, per explicit scope choice.

## Verification

1. `make linkml-lint` after every schema-touching phase.
2. `make validate-all` (both `shacl-validate` and `governance-graph-validate`) must keep passing after Phases 1 and 2b.
3. `make policy-fabric`, diff `policy_fabric_export/*.json` — Phase 2a must preserve identical output values.
4. `make governance-graph`, diff `governance_graph_export/governance_graph.ttl` against the pre-Phase-2b version — must be triple-set-identical.
5. `make docs`, then a doc-link-check pass across all narrative docs including the new `docs/drs-interop.md`.
6. Spot-check the new `AssetBinding`/`DrsObjectMapping`/`DrsAuthorizationBinding` classes render correctly in `docs/reference/classes/`.

See [`governance_consolidation_and_drs_interop_report.md`](governance_consolidation_and_drs_interop_report.md) for what was actually changed and the verification results.
