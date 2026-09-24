# Downstream changes from the graph-layer refactor

This page lists the changes the graph-layer refactor
([`plans/model_refactor.md`](https://github.com/mc2-center/governanceDUO/blob/main/plans/model_refactor.md),
decision 4) identified as needed in other repositories, without making them:
this repository edits only itself. `authorizer_v1` (see
[graph design, section 6](graph-design.md#projections)) exists specifically so
none of these are required before the refactor can ship — sagebrain-infra keeps
reading the contract it already has.

None of the items below are prerequisites for anything in this repository.
They are recorded here so the work isn't lost, and so whoever picks each one up
in the other repository knows why it matters.

## sagebrain-infra

The authorizer (`src/lambda_rebac/authorize.py`, commit `fc6de51`) can, at its
own pace, move off the pinned `authorizer_v1` compatibility contract and onto
the canonical graph directly:

- Read the current namespace (`https://w3id.org/synapse/governance#`), or keep
  reading `authorizer_v1` — either is fine as long as one of them is pinned and
  versioned, so a refactor here can't silently break it again.
- Join `acl:agentGroup` through `vcard:hasMember` for team grants, and handle
  `acl:agentClass` (`foaf:Agent`/`acl:AuthenticatedAgent`) for PUBLIC and
  AUTHENTICATED_USERS. Both are currently invisible to the authorizer:
  `authorizer_v1_teams.rq` is an opt-in, flag-gated stopgap, and `scripts/project.py`
  prints a count of `acl:agentClass` authorizations neither projection can
  express. Doing this in infra directly retires the need for the teams
  projection.
- Allow inferred-only grants. The authorizer's `intersection` binding mode
  currently denies a request unless every inherited grant is also satisfied;
  since most files inherit their ACL rather than carrying one of their own,
  this makes `intersection` mode stricter than intended for the common case.
- Evaluate `gov:Approval` from the graph directly (status, `gov:expiresAt`)
  instead of failing open when the caller omits approval evidence.
- Select the latest snapshot of a resource's grants, not a cached one, so a
  revoked ACL or expired approval takes effect immediately rather than on the
  next cache cycle.
- Make the ACL rewriter (whatever writes ACL changes back to Synapse-facing
  systems) use IRIs consistently, rather than mixing IRIs and bare ids.
- Fix the org name in `tests/infra_contract/authorize_query.rq`'s header
  comment in *this* repository's pinned copy, once the canonical source in
  sagebrain-infra is corrected — this repo's copy is a verbatim mirror and
  should not diverge from it.

## sagebrain-model

- Re-point `scripts/import.sh` at this repository's single graph TBox and
  shape set (`shapes/governance.owl.ttl`, `shapes/governance.shacl.ttl`) and
  adopt the current namespace (`https://w3id.org/synapse/governance#`). As of
  this repository's `HEAD`, this has been done — see sagebrain-model's own
  `plans/governance_layer_realignment.md` — but the pin will drift again the
  next time this repository's graph layer changes; `make sagebrain-contract-check`
  is what catches that.
- Drop `gov:SynapseEntity`'s `skos:closeMatch prov:Entity`, which sagebrain-model
  previously asserted on this repository's behalf. This repository now declares
  it directly (`linkml/graph/governance.yaml`'s `SynapseEntity.close_mappings`),
  so sagebrain-model's own copy is a duplicate, not a gap-filler.

## w3id

- **R1** (`plans/model_refactor.md`) chose `https://w3id.org/synapse/governance#`
  as the graph layer's namespace. Resolving it needs a w3id redirect entry (an
  outward pull request to [`perma-id/w3id.org`](https://github.com/perma-id/w3id.org)),
  which has not been filed. Until it is, the namespace resolves nowhere; every
  check in this repository validates the IRIs as strings, not by dereferencing
  them, so this doesn't block anything here.
