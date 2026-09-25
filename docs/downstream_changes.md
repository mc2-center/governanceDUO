# Downstream changes from the graph-layer refactor

This page lists the changes the graph-layer refactor
([`plans/model_refactor.md`](https://github.com/mc2-center/governanceDUO/blob/main/plans/model_refactor.md),
decision 4) identified as needed in other repositories, without making them:
this repository edits only itself. `authorizer_v1` (see
[graph design, section 7](graph-design.md#7-rebac-alignment), and
[the technical detail](graph-design-implementation.md#3-how-the-graph-is-built))
exists specifically so none of these are required before the refactor can ship —
sagebrain-infra keeps reading the contract it already has.

None of the items below are prerequisites for anything in this repository.
They are recorded here so the work isn't lost, and so whoever picks each one up
in the other repository knows why it matters. Status, checked against each
repository directly (2026-09-25): **sagebrain-infra** — still open, unchanged;
**sagebrain-model** — done, on a branch not yet merged; **w3id** — still open,
unfiled.

## sagebrain-infra — still open

The authorizer's `policy-engine` branch (`origin/policy-engine`) hasn't moved
past the pinned commit, `fc6de51`, since this list was written. At its own pace,
`src/lambda_rebac/authorize.py` can move off the pinned `authorizer_v1`
compatibility contract and onto the canonical graph directly:

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

## sagebrain-model — done, on a branch not yet merged to `main`

Both items below are complete, verified directly against sagebrain-model's
`governance-layer-import` branch (2026-09-25) — but that branch is not an
ancestor of `origin/main` yet, so this counts as done-in-progress, not shipped:

- ~~Re-point `scripts/import.sh` at this repository's single graph TBox and
  shape set, and adopt the current namespace.~~ **Done** — see
  `plans/governance_layer_realignment.md` on that branch. The pin will drift
  again the next time this repository's graph layer changes regardless;
  `make sagebrain-contract-check` is what catches that, on both sides.
- ~~Drop `gov:SynapseEntity`'s `skos:closeMatch prov:Entity`.~~ **Done**,
  commit `63564c0` ("sagebrain.ttl: drop the gov:SynapseEntity closeMatch
  governanceDUO now asserts").

## w3id — still open

- **R1** (`plans/model_refactor.md`) chose `https://w3id.org/synapse/governance#`
  as the graph layer's namespace. Resolving it needs a w3id redirect entry (an
  outward pull request to [`perma-id/w3id.org`](https://github.com/perma-id/w3id.org)),
  which has not been filed. Until it is, the namespace resolves nowhere; every
  check in this repository validates the IRIs as strings, not by dereferencing
  them, so this doesn't block anything here.
