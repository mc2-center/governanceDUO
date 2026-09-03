Resolve open governance-graph design questions (AccessApproval, Program/Site,
and full Synapse governance-entity coverage)

Context

This follows `plans/rebac_governance_graph_alignment.md`, which deliberately
deferred two things rather than build them speculatively: a real `gov:Approval`/
`expiresAt` implementation (its point 3) and the `Program`/`Site`/
`AccessRequirementTemplate` question raised by thomasyu888's PR #54 comment (its
point 4). Separately, the user asked to confirm *every* real Synapse governance
entity is modeled here, not just the two flagged above. This plan resolves what
Synapse's public REST API docs (rest-docs.synapse.org — checkable without live
credentials) can actually settle, and turns the rest into concrete, scoped
decision points instead of open-ended questions.

Section A — Full governance-entity coverage audit (verified against
rest-docs.synapse.org, and cross-checked field-by-field against the authoritative
OpenAPI spec at `~/Downloads/SynapseOpenApiSpec (1).json` where noted)

| Synapse object | Modeled here? | Where | Gap? |
| --- | --- | --- | --- |
| `AccessRequirement` | Yes | `access_requirement.yaml`, bridged into the graph via `owl:sameAs` | No |
| `AccessControlList` / `ResourceAccess` | Yes | `AccessGrant` class = one `ResourceAccess` grant; `gov:hasACL` edge = the ACL | No |
| `DataAccessSubmission` | Yes | `DataAccessSubmission`/`DataAccessSubmissionStatus` classes | No |
| `AccessApproval` | **No** | Not modeled at all — grepped clean across `linkml/`, `docs/`, `model/`, `scripts/`, `shapes/`, `plans/` | **Yes** — real fields verified: `id`, `etag`, `createdOn`, `modifiedOn`, `createdBy`, `modifiedBy`, `requirementId`, `requirementVersion`, `submitterId`, `accessorId`, `expiredOn`, `state`. Resolved in Section B. |
| `ResearchProject` | **No** | Only a dangling FK string (`researchProjectId` on `DataAccessSubmission`), no node | **Yes** — real fields verified: `id`, `accessRequirementId`, `institution`, `projectLead`, `intendedDataUseStatement`, `createdOn`/`modifiedOn`/`createdBy`/`modifiedBy`, `etag`. `institution` is directly relevant to Section C. Resolved in Section C. |
| `DataAccessRequest`/`DataAccessRenewal` | **No** | Only a dangling FK string (`dataAccessRequestId` on `DataAccessSubmission`), no node | **Yes.** Its rest-docs.synapse.org page 403'd earlier; now pulled directly from the OpenAPI spec instead (`org.sagebionetworks.repo.model.dataaccess.RequestInterface`, concrete types `Request`/`Renewal`). Real fields: `id`, `accessRequirementId`, `researchProjectId`, `createdOn`/`modifiedOn`/`createdBy`/`modifiedBy`, `etag`, `concreteType`, `ducFileHandleId`, `irbFileHandleId`, `attachments`, `accessorChanges`, `institution`, `principalInvestigator` (nested: `userId`/`name`/`institutionalEmail`), `signingOfficial` (nested: `name`/`institutionalEmail`), `eDucSignatureEnvelopeId`, `schemaData`; `Renewal` adds `publication`/`summaryOfUse`. **Note:** the live `Submission` object's actual FK field is named `requestId`, not `dataAccessRequestId` — this repo's existing `DataAccessSubmission.dataAccessRequestId` slot name is a naming drift from the current API, not a match (see the new flag below). **Also note:** `institution`/`principalInvestigator`/`signingOfficial` here are a second, independently-verified real signal bearing on the Program/Site question (Section C) — a *request* (not just its `ResearchProject`) carries its own institution + a named signing official, i.e. real per-institution structure exists in Synapse's schema even though template/site *reuse* across requests does not. |
| `RestrictableObjectDescriptor` | Effectively yes | `AccessRequirementAssociation.resource` / `entityIdList` already serves this purpose | No |
| `VerificationSubmission` | No | Not referenced anywhere | Different domain (user identity verification, not resource governance). No current consumer (`authorize.py` included) needs it. **Recommend: explicitly out of scope**, not a gap. |
| `AccessorGroup`, `AccessApprovalInfo` | No | — | Batch/report DTOs, not persisted entities with their own identity. **Not a gap.** |
| `EvaluationRound` | No | — | Belongs to Synapse's challenge/Evaluation-queue domain, not data-access governance (the REST-index prompt over-matched on "submission round"). **Not a gap.** |

Section A.1 — New finding: existing `DataAccessSubmission`/`DataAccessSubmissionStatus`
modeling has drifted from Synapse's *current* API (not previously flagged; found
while cross-checking Section A against the OpenAPI spec, not something either plan
proposed changing)

`governance_graph.yaml`'s `DataAccessSubmission`/`DataAccessSubmissionStatus`
classes predate this review and weren't in question — but the spec check above
surfaced a real mismatch worth flagging rather than silently carrying forward.
The current live API's equivalent objects are named `Submission`/`SubmissionStatus`
(under `org.sagebionetworks.repo.model.dataaccess`), and their real fields differ
from what's modeled here:

| This repo's slot | Live API's actual field | 
| --- | --- |
| `DataAccessSubmission.dataAccessRequestId` | `Submission.requestId` |
| `DataAccessSubmission.createdBy`/`createdOn` | `Submission.submittedBy`/`submittedOn` (no `createdBy`/`createdOn` at all) |
| `DataAccessSubmissionStatus.reason` | `SubmissionStatus.rejectedReason` |
| `DataAccessSubmissionStatus.createdBy`/`createdOn`/`modifiedBy` | **Don't exist** on the live `SubmissionStatus` — it only has `submissionId`/`submittedBy`/`rejectedReason`/`state`/`modifiedOn` |
| — | `Submission.researchProjectSnapshot` embeds the **full `ResearchProject` object**, not just an ID — relevant to Section C: a real sync wouldn't need a separate fetch for it |

**Resolved** (2026-09-03): `linkml/governance_graph.yaml`'s `DataAccessSubmission`/
`DataAccessSubmissionStatus` classes, `scripts/build_governance_graph.py`,
`linkml/examples/governance_graph/data_access_submission*.example.yaml`, and the
hand-authored `shapes/governance_graph.{shacl,owl}.ttl` were all corrected to match
the live `Submission`/`SubmissionStatus` REST objects (`dataAccessRequestId` →
`requestId`; `createdBy`/`createdOn` → `submittedBy`/`submittedOn`; `reason` →
`rejectedReason`; `DataAccessSubmissionStatus.createdBy`/`createdOn`/`modifiedBy`
removed — `modifiedBy` moved to `DataAccessSubmission`, matching where the live API
actually places it). `docs/knowledge-graph.md`'s prose was updated to match, and
`make validate-all` / `make governance-graph-validate` both still conform.
`authorize.py`'s live SPARQL contract was confirmed untouched (it never referenced
any of these slots). This was a standalone fix, not part of either plan's execution
list.

Section B — Resolving alignment-plan point 3 (`gov:Approval` / `expiresAt`)

Add a real `AccessApproval` class to `governance_graph.yaml`
(`class_uri: sagegov:AccessApproval`), slots mirroring the verified REST object:
`requirementId` (→ the `gov:AR-<n>` node, same edge shape as
`AccessRequirementAssociation.accessRequirement`), `accessorId` (→ a
`gov:principal-<n>` node, same minting convention `add_principal()` already uses),
`state`, `expiredOn`, plus `createdOn`/`createdBy`/`etag` for parity with the
other Synapse-mirroring classes here. Map directly onto the target ontology:
`gov:satisfies` (`requirementId`), `gov:heldBy` (`accessorId`), `gov:status`
(`state`), `gov:expiresAt` (`expiredOn`).

- No committed example data exists for this (unlike `DataAccessSubmission`), so
  author one new `linkml/examples/governance_graph/access_approval.example.yaml`,
  keyed to the same AR/principal ids the existing `data_access_submission*`
  examples already use, so the two connect in the rendered graph.
- Wire into `build_governance_graph.py`: add `"access_approval"` to
  `EXAMPLE_CLASSES` and a new `add_access_approval()`.
- Decide (flag, don't silently pick): should the existing derived `gov:hasApproval`
  edge (Principal → AR, emitted when `DataAccessSubmissionStatus.state ==
  APPROVED`) stay sourced from `DataAccessSubmissionStatus` as today, or be
  re-derived from the new, more authoritative `AccessApproval` node once it
  exists? Recommendation: re-derive from `AccessApproval` — it's the object
  Synapse itself treats as the actual grant of approval; `DataAccessSubmission`/
  `Status` is the workflow/audit trail that produces one. Keep both edges during
  a transition period rather than removing `hasApproval`'s current source
  outright, since `authorize.py`'s SPARQL contract doesn't touch either.
- Add a `sagegov:AccessApproval` `sh:NodeShape` (per the alignment plan's own
  additive-safe pattern) and the matching OWL TBox declaration.

Section C — Resolving alignment-plan point 4 (`Program`/`Site`/
`AccessRequirementTemplate`)

New finding narrows, but doesn't resolve, this question: `ResearchProject`
(behind every `DataAccessSubmission`) carries a real, verified `institution`
field — i.e. Synapse *does* capture a per-request institution/site signal, just
not the `Program`→`Site`→`IRBRequirement`→`extendsTemplate` reuse structure
thomasyu888's example illustrates.

- Model `ResearchProject` as its own class (same treatment as `AccessApproval`
  above): `institution`, `projectLead`, `intendedDataUseStatement` as literal
  slots for now — not yet a full `gov:Site` node with its own
  `affiliatedWith`/`participatesIn` edges, since nothing here yet establishes
  that institutions recur across multiple `AccessRequirement`s in a
  structured way. This replaces the current dangling `researchProjectId` FK
  string on `DataAccessSubmission` with a real node + edge.
- The bigger question — template/condition reuse across sites/programs — is a
  business-process fact, not something in Synapse's own schema (confirmed:
  `AccessRequirement`'s only compositional mechanism is `subjectIds`, scoped to
  individual entities, not organizational units). Before treating this as
  something only a stakeholder can answer, check two more concrete, already-
  reachable sources first (neither requires contacting anyone):
  1. The external `mc2-center-dcc` repo referenced in
     `docs/governance-graph-sync.md` — not checked in this session.
  2. AD Knowledge Portal's and NF-OSI's own public governance/data-use-agreement
     documentation (both named directly in thomasyu888's example) — do their
     published DUC/IRB language actually get reused verbatim across
     participating sites? Public, checkable without credentials.
- If neither source shows a real reuse pattern, leave this as a documented open
  design question in `docs/governance-graph-sync.md` (not built) — do not
  default to modeling `Program`/`Site`/`AccessRequirementTemplate` off one
  illustrative PR comment alone.

Section D — The 4 pre-existing open questions in
`docs/governance-graph-sync.md`

Sync script location, sync cadence, incomplete-parsed-record handling, and auth.
The doc is explicit that "none of this can be verified end-to-end without live
Synapse credentials, which this environment doesn't have" — these remain
decisions for you/Sage, not something this plan can resolve by reading docs.
One recommendation, not a decision: for "incomplete parsed records" (#3),
`scripts/build_policy_fabric.py` already has a documented three-way convention
(error/warning/silent-skip) for unmapped `referenceValueKeys`; defaulting the
new sync's behavior to `warning` (surface, don't block, don't hide) would be
consistent with that existing precedent — but confirm before implementing,
don't assume.

Section E — `institutionDids`/ROR gap (from `plans/policy_fabric_alignment.md`)

Still an open, intentionally-documented gap (Policy Fabric's `AffiliationCredential`
expects org DIDs; this repo has ROR ids). No new action proposed here — flagged
only because it's one of "the other documented gaps." Revisit only if the user
wants it prioritized.

Execution task list

1. Add `AccessApproval` class + example instance + `build_governance_graph.py`
   wiring + SHACL/OWL shapes (Section B).
2. Add `ResearchProject` class (`institution`/`projectLead`/
   `intendedDataUseStatement`) + example instance + `build_governance_graph.py`
   wiring (replace the dangling `researchProjectId` FK with a real edge) +
   SHACL/OWL shapes (Section C).
3. Check the `mc2-center-dcc` repo and ADKP/NF-OSI public governance docs for
   AR-template-reuse evidence; record the outcome either way in
   `docs/governance-graph-sync.md`'s open-questions section. (`DataAccessRequest`'s
   schema is now fully verified via the OpenAPI spec — see Section A — so this task
   is scoped to the Program/Site business-process question only, not a data lookup.)
4. Update `docs/governance-graph-sync.md`: add the full entity-coverage table
   from Section A, explicitly marking `RestrictableObjectDescriptor`/
   `AccessorGroup`/`AccessApprovalInfo`/`EvaluationRound`/`VerificationSubmission`
   as reviewed-and-out-of-scope (one-line reason each) so this doesn't get
   re-asked later.
5. Regenerate `governance_graph_export/governance_graph.ttl`.
6. Leave Section D's 4 questions and Section E's ROR/DID gap as documented,
   unresolved decisions — no code changes; just confirm the doc text describing
   them is still accurate after tasks 1-2 land.

Verification

1. `make linkml-lint`, `make shacl-validate`, `make governance-graph-validate` —
   same convention as the alignment plan, confirm no regressions.
2. Smoke queries confirming `AccessApproval`/`ResearchProject` nodes are
   reachable, analogous to the alignment plan's `Condition`/`duoCode` query.
3. Confirm `authorize.py`'s live SPARQL-contract triples
   (`gov:hasACL`/`gov:AccessGrant`/`gov:principal`/`gov:permission`/
   `gov:bindingType`/`gov:hasAccessRequirement`) stay byte-for-byte unchanged —
   same additive-safety bar as the alignment plan.
