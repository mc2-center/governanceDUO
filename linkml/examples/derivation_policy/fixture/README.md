# Derivation policy regression fixture

Inputs for `scripts/check_derivation_policy.py` (`make derivation-policy-check`).
Not examples of real data: a minimal, hand-built case that exercises every branch
of `scripts/build_derivation_policy.py`.

- `provenance.ttl`: `gov:activity-7001` consumes two Synapse files
  (`syn70000001`, `syn70000002`, both not executed) plus an executed script, and
  generates `syn70000003`.
  `gov:activity-7002` consumes `syn70000011` and `syn70000012` and generates
  `syn70000013`; `gov:activity-7003` consumes those two plus `syn70000014` and
  generates `syn70000015`. `gov:activity-7004` consumes `syn70000011` and
  `syn70000013` and generates `syn70000016`; `gov:activity-7005` consumes
  `syn70000011`, `syn70000012`, `syn70000013` and `syn70000017` and generates
  `syn70000018`.
- `governance.ttl`: `syn70000001` is bound to `gov:AR-7001`, `syn70000002` to
  `gov:AR-7002` -- disjoint AccessRequirements. `syn70000011`, `syn70000012` and
  `syn70000014` share `gov:AR-7003` (not disjoint); the output `syn70000013` is
  itself bound to `gov:AR-7004`, as is `syn70000017`.
- `access_requirements/`: the curated records behind those stubs.
  `access_requirement.7001` has `dataTier: Controlled`; `access_requirement.7002`
  has no `dataTier` (fails closed to `Unclassified`); `access_requirement.7003` is
  `Controlled` and `access_requirement.7004` is `Private`.
- `derivation_rule.controlled-pair.yaml`: Controlled + Controlled stays
  Controlled and requires review.
- `derivation_rule.controlled-private.yaml`: Controlled + Private yields
  Controlled (an override that lowers the inherited tier), no review.
- `derivation_rule.private-pair.yaml`: Private + Private is forbidden.
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
- `syn70000013` is labeled `Private`: the rule lowers what it inherits, never its
  own binding;
- `syn70000016` is labeled `Controlled`: the Controlled + Private rule lowers the
  Private it would inherit, since it has no binding of its own;
- exactly four `Flagged` DerivationReviews: `gov:activity-7001` (disjoint ARs),
  `gov:activity-7002` (the rule) and `gov:activity-7003` (the rule, matched on a
  pair of its three inputs), both with notes naming the rule and not
  disjointness; and `gov:activity-7005`, whose notes lead with the forbidding
  Private + Private rule, ahead of the Controlled + Controlled one;
- the Association inherits `syn70000003`'s label through `sagebrain:derived_from`.
