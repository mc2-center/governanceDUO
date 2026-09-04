# Report: Governance Graph ingestion plan — Section 5 schema changes

Executed against [`governance_graph_ingestion.md`](governance_graph_ingestion.md) Section 5 ("Target schema changes"). This report covers only that section — the plan's remaining scope (an actual `scripts/sync_governance_graph.py`, following Sections 2/4/6's pull order/auth/scope design) is not implemented and isn't claimed to be.

## `AccessGrant.sourceAclId`/`sourceAclResourceAccessId` removal: as planned

Confirmed directly against rest-docs.synapse.org (documented in the plan's Section 1) that neither field is exposed by the public REST API under any credential: `AccessControlList.id` is the entity id, not a separate ACL-record id, and `ResourceAccess` has only `principalId`/`accessType` — no row id at all. Removed:

- Both slot definitions and their two `AccessGrant.slots` entries in `linkml/governance_graph.yaml`; `AccessGrant.id`'s description updated to explain why (rather than pointing at fields that no longer exist).
- The corresponding `g.add(...)` calls in `scripts/build_governance_graph.py`'s `add_access_grant()`.
- The two example values in `linkml/examples/governance_graph/access_grant.example.yaml`.
- `gov:sourceAclId`/`gov:sourceAclResourceAccessId`'s property declarations in the hand-authored `shapes/governance_graph.owl.ttl`, and their property shapes in `shapes/governance_graph.shacl.ttl`'s `AccessGrantShape`.
- The worked example in `docs/knowledge-graph.md`.

## `tree_root: true` on `Program`/`AccessRequirementTemplate`/`IRBRequirement`: as planned

Added to all three classes in `linkml/governance_graph.yaml`, no other changes — they were already correctly shaped LinkML classes, matching `Study`/`AccessRequirement`/`Resource`/`Schema`'s existing pattern.

## Verification — all passed

- `governance_graph_export/governance_graph.ttl` regenerated: 98 triples, down from 100 — exactly the two removed assertions on the one example `AccessGrant` instance, nothing else changed.
- `make shacl-validate`: `Conforms: True` on both the schema build and the example instances.
- `make governance-graph-validate`: `Conforms: True`.
- `make linkml-lint`: exit 0, same pre-existing `standard_naming` camelCase warning category as before (no regression, no new warnings).
- `make docs-build`: `mkdocs build --strict` passes with no broken links.

## Files touched

`linkml/governance_graph.yaml`, `scripts/build_governance_graph.py`, `linkml/examples/governance_graph/access_grant.example.yaml`, `governance_graph_export/governance_graph.ttl`, `shapes/governance_duo.owl.ttl`, `shapes/governance_duo.shacl.ttl`, `shapes/governance_graph.owl.ttl`, `shapes/governance_graph.shacl.ttl`, `docs/knowledge-graph.md`, `docs/reference/**` (regenerated).
