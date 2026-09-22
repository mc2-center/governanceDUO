# Derivation policy regression fixture

Inputs for `scripts/check_derivation_policy.py` (`make derivation-policy-check`).
Not examples of real data: a minimal, hand-built case that exercises every branch
of `scripts/build_derivation_policy.py`.

- `provenance.ttl`: `gov:activity-7001` consumes two Synapse files
  (`syn70000001`, `syn70000002`, both not executed) plus an executed script, and
  generates `syn70000003`.
- `governance.ttl`: `syn70000001` is bound to `gov:AR-7001`, `syn70000002` to
  `gov:AR-7002` -- disjoint AccessRequirements.
- `access_requirements/`: the curated records behind those stubs.
  `access_requirement.7001` has `dataTier: Controlled`; `access_requirement.7002`
  has no `dataTier` (fails closed to `Unclassified`).
- `sagebrain.ttl`: a sagebrain-model-shaped `biolink:Association` with
  `sagebrain:derived_from syn:syn70000003`, plus the bridge axiom
  `sagebrain:derived_from rdfs:subPropertyOf prov:wasDerivedFrom`. The axiom is
  declared here only so the fixture is self-contained; sagebrain-model owns it
  (its governance layer module) once `plans/governance_layer_import.md` lands
  there.

Expected results (asserted by the check):
- `syn70000003` is labeled `Unclassified` (the max of Controlled and
  Unclassified), citing both ARs, `computedFrom gov:activity-7001`;
- `syn70000002` keeps an `Unclassified` label citing `gov:AR-7002`;
- exactly one `Flagged` DerivationReview for `gov:activity-7001`;
- the Association inherits `syn70000003`'s label through `sagebrain:derived_from`.
