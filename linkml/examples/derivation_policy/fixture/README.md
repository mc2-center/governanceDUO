# Derivation policy regression fixture

Inputs for `scripts/check_derivation_policy.py` (`make derivation-policy-check`).
Not examples of real data: a minimal, hand-built case that exercises every branch
of `scripts/build_derivation_policy.py`, in the canonical graph layer's model
(`linkml/graph/governance.yaml`, plans/model_refactor.md).

- `provenance.ttl`: `govid:activity/7001` consumes two Synapse files
  (`syn70000001`, `syn70000002`, both not executed) plus an executed script, and
  generates `syn70000003`.
  `govid:activity/7002` consumes `syn70000011` and `syn70000012` and generates
  `syn70000013`; `govid:activity/7003` consumes those two plus `syn70000014` and
  generates `syn70000015`. `govid:activity/7004` consumes `syn70000011` and
  `syn70000013` and generates `syn70000016`; `govid:activity/7005` consumes
  `syn70000011`, `syn70000012`, `syn70000013` and `syn70000017` and generates
  `syn70000018`. Every `prov:Usage` carries its own IRI
  (`govid:activity/<n>/usage/<m>`), not a blank node -- every graph node needs one
  (shapes/governance.shacl.ttl).
- `governance.ttl`: `syn70000001` is bound to `govid:ar/7001`, `syn70000002` to
  `govid:ar/7002` -- disjoint AccessRequirements. `syn70000011`, `syn70000012` and
  `syn70000014` share `govid:ar/7003` (not disjoint); the output `syn70000013` is
  itself bound to `govid:ar/7004`, as is `syn70000017`. `govid:ar/7001` and
  `govid:ar/7003` carry `gov:dataTier gov:ControlledTier`; `govid:ar/7004` carries
  `gov:dataTier gov:PrivateTier`; `govid:ar/7002` carries no `gov:dataTier` (fails
  closed to Unclassified). The AR's tier is a property of its own graph node now
  (R5), not a curated record bridged by `owl:sameAs` -- there is no
  `access_requirements/` directory any more. `syn70000019` has no `requiresAR`
  of its own, only `gov:parent syn70000011` (bound to `ar/7003`); `govid:activity/7006`
  (one input, `syn70000019`, so no review) exists only to bring it into the
  entity set, exercising the `gov:parent` ancestor walk
  (`entity_access_requirements()`) on its own, not through derivation ancestry.
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
  Unclassified), citing both ARs, `computedFrom govid:activity/7001`;
- `syn70000002` keeps an `Unclassified` label citing `govid:ar/7002`;
- `syn70000013` is labeled `Private`: the rule lowers what it inherits, never its
  own binding;
- `syn70000016` is labeled `Controlled`: the Controlled + Private rule lowers the
  Private it would inherit, since it has no binding of its own;
- exactly four `Flagged` DerivationReviews: `govid:activity/7001` (disjoint ARs),
  `govid:activity/7002` (the rule) and `govid:activity/7003` (the rule, matched on
  a pair of its three inputs), both with notes naming the rule and not
  disjointness; and `govid:activity/7005`, whose notes lead with the forbidding
  Private + Private rule, ahead of the Controlled + Controlled one;
- `syn70000019` is labeled `Controlled`, citing `govid:ar/7003`, inherited purely
  through `gov:parent syn70000011` (no `requiresAR` of its own);
- the Association inherits `syn70000003`'s label through `sagebrain:derived_from`.

The output is checked two ways: SPARQL ASK assertions on the specific labels and
reviews above, and SHACL conformance of the output merged with its three input
graphs against `shapes/governance.shacl.ttl` (ont `shapes/governance.owl.ttl`) --
replacing the pre-refactor pipeline's separate domain/range check, now that both
TBoxes are one generated TBox and shape set.
