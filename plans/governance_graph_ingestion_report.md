# Report: Governance Graph ingestion plan

Executed against [`governance_graph_ingestion.md`](governance_graph_ingestion.md). Two phases: Section 5's schema changes, and the sync script itself (Sections 2/4/6's design).

## Phase 1 — Section 5 schema changes: as planned

### `AccessGrant.sourceAclId`/`sourceAclResourceAccessId` removal: as planned

Confirmed directly against rest-docs.synapse.org (documented in the plan's Section 1) that neither field is exposed by the public REST API under any credential: `AccessControlList.id` is the entity id, not a separate ACL-record id, and `ResourceAccess` has only `principalId`/`accessType` — no row id at all. Removed:

- Both slot definitions and their two `AccessGrant.slots` entries in `linkml/governance_graph.yaml`; `AccessGrant.id`'s description updated to explain why (rather than pointing at fields that no longer exist).
- The corresponding `g.add(...)` calls in `scripts/build_governance_graph.py`'s `add_access_grant()`.
- The two example values in `linkml/examples/governance_graph/access_grant.example.yaml`.
- `gov:sourceAclId`/`gov:sourceAclResourceAccessId`'s property declarations in the hand-authored `shapes/governance_graph.owl.ttl`, and their property shapes in `shapes/governance_graph.shacl.ttl`'s `AccessGrantShape`.
- The worked example in `docs/knowledge-graph.md`.

### `tree_root: true` on `Program`/`AccessRequirementTemplate`/`IRBRequirement`: as planned

Added to all three classes in `linkml/governance_graph.yaml`, no other changes — they were already correctly shaped LinkML classes, matching `Study`/`AccessRequirement`/`Resource`/`Schema`'s existing pattern.

### Verification — all passed

- `governance_graph_export/governance_graph.ttl` regenerated: 98 triples, down from 100 — exactly the two removed assertions on the one example `AccessGrant` instance, nothing else changed.
- `make shacl-validate`: `Conforms: True` on both the schema build and the example instances.
- `make governance-graph-validate`: `Conforms: True`.
- `make linkml-lint`: exit 0, same pre-existing `standard_naming` camelCase warning category as before (no regression, no new warnings).
- `make docs-build`: `mkdocs build --strict` passes with no broken links.

### Files touched

`linkml/governance_graph.yaml`, `scripts/build_governance_graph.py`, `linkml/examples/governance_graph/access_grant.example.yaml`, `governance_graph_export/governance_graph.ttl`, `shapes/governance_duo.owl.ttl`, `shapes/governance_duo.shacl.ttl`, `shapes/governance_graph.owl.ttl`, `shapes/governance_graph.shacl.ttl`, `docs/knowledge-graph.md`, `docs/reference/**` (regenerated).

## Phase 2 — `scripts/sync_governance_graph.py`: as planned, with corrections the build itself surfaced

Implements plans/governance_graph_ingestion.md Sections 2 (resolved decisions), 4 (pull order/delineation), and 6 (scope) exactly — one entity id per CLI argument, ACT-credentialed `synapseclient` login via default credential resolution, warn-don't-block on every per-item Synapse call, DUO conditions sourced only from curator-authored records (never derived from Synapse), reuses `build_governance_graph.py`'s `add_*()`/`PREDICATE()`/`TYPE()`/`gov_id()`/`site_node_for()` unchanged rather than reimplementing graph assembly. Writes to a separate `governance_graph_export/governance_graph_synced.ttl` by default so it never clobbers the example-driven build.

### Two pull-order simplifications the plan didn't anticipate

Checked directly against rest-docs.synapse.org while writing the actual REST calls (the plan's own endpoint checks stopped at "does this endpoint exist and who can call it," not full response-schema inspection):

- `GET /dataAccessSubmission/{submissionId}` returns a full `Submission` object — the exact same type already embedded in `POST .../submissions`'s own result list, `state`/`rejectedReason`/`modifiedOn` included. The plan's step 6b called for both; the second, per-submission call turned out to be unneeded, so this script never makes it.
- `GET /entity/{id}/accessRequirement`'s `PaginatedResults<AccessRequirement>` already returns full `AccessRequirement` objects, `subjectIds` included — enough for the Direct/Inherited heuristic on its own. The plan's step 6a's separate `GET /accessRequirement/{requirementId}` call is therefore also unneeded (nothing else in this schema's `AccessRequirementReference` class needs that object's other structural fields).

### One real bug the mock-based verification caught

`add_research_project()` and `add_access_approval()` do a plain `principal_nodes[id]` dict lookup (unlike `add_data_access_submission()`, which constructs a `gov:principal-<n>` IRI directly and needs no pre-existing entry) — an early draft resolved `submittedBy`/`modifiedBy` before calling `add_research_project()`, but not the embedded `ResearchProjectSnapshot`'s own `createdBy` (which can legitimately differ from the submission's submitter — e.g. a coordinator submitting on a PI's behalf), which would have raised `KeyError` the first time real data exercised that path. Fixed by resolving every principal a submission and its snapshot reference in one batch before any `add_*()` call that needs them.

### Two accepted-gap thin-node fixes, both verified necessary via pySHACL, not assumed

Running the script's output through pySHACL against the real hand-authored `shapes/governance_graph.shacl.ttl`/`.owl.ttl` (see Verification below) surfaced two real violations a purely-manual review missed:

- A `parentId` reference to an entity outside the CLI's explicit entity-id list (this sync's scope has no recursive walk, per Section 6 item 1) was completely untyped, failing `SynapseEntityShape`'s `sh:class gov:SynapseEntity` check on `gov:parentId`. Fixed by asserting a bare `rdf:type` stub for any `parentId` not among the requested entity ids.
- `DataAccessRequest`'s thin stub (Section 1's accepted gap: no REST path exists for another user's request) failed `DataAccessRequestShape`'s own `minCount 1` requirement on `gov:accessRequirement` — a real, separate constraint from `DataAccessSubmissionShape`'s `sh:class` check on the `requestId` edge pointing at it. Fixed by also asserting the one fact about the request that genuinely is known without fetching it: which AccessRequirement it belongs to (the same `ar_node` already in scope).

### Verification — all passed (mocked; no live Synapse credentials in this environment)

- `python3 -m py_compile scripts/sync_governance_graph.py` — compiles cleanly.
- End-to-end run against a hand-built mock `synapseclient.Synapse` (`restGET`/`restPOST` monkeypatched with realistic responses matching every confirmed field shape in this session's rest-docs.synapse.org checks) — completes with no exceptions, produces a plausible graph (SynapseEntity, AccessGrant, Principal×3, AccessRequirementAssociation, the AccessRequirementReference stub with real `Condition` data pulled from the repo's actual `linkml/examples/access_requirement.example.yaml`, DataAccessSubmission/Status, AccessApproval, ResearchProject, the DataAccessRequest thin stub, Sites).
- That mocked output validated against the real `shapes/governance_graph.shacl.ttl`/`shapes/governance_graph.owl.ttl` with pySHACL, `inference="none"`: **`Conforms: True`** — this is what caught the `parentId`/`DataAccessRequest` gaps above; both are fixed and re-verified conforming.
- Also exercised the warn-don't-block path directly: pointing `--access-requirement-dir` at an empty directory produces the expected warning and a valid (if condition-less) graph, no exception.
- **Not verified**: real Synapse call semantics under live data (no credentials available in this environment) — one endpoint in particular, `POST /accessApproval/search`'s exact request/response field names, is flagged inline in the code as inferred rather than confirmed (its class-level docs pages 403'd repeatedly). A live smoke test against a real, permissioned AccessRequirement is the right next step before production use.

### Files touched

`scripts/sync_governance_graph.py` (new), `requirements.txt` (added `synapseclient>=4.0`), `Makefile` (`sync-governance-graph`/`sync-governance-graph-validate` targets), `plans/governance_graph_ingestion.md` (implementation status note).
