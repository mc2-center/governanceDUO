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

**Revision (2026-09-03)**: the user reviewed this plan directly and added notes
that meaningfully expand its scope -- all three `Gap? == Yes` rows from
Section A now get an execution-ready section (adding new Section C.1 for
`DataAccessRequest`/`DataAccessRenewal`, not just the two already covered); a
real `Site` class is now in scope alongside `ResearchProject` (Section C); and,
critically, the user directly confirmed -- as the domain authority, not as a
sourcing question this plan could resolve on its own -- that the target
ontology's `Program`/`Site`/`IRBRequirement`/`AccessRequirementTemplate`
structure is the intended direction to build toward, so new Section C.2 designs
that now rather than leaving it as an open question. Sections D and E were
reviewed and mostly left as-is: Section D's sync-cadence recommendation is
explicitly deferred (`[Skip for now]`), and Section E turned out to already be
fully implemented (see its own corrected text) -- not something the user's note
needed to newly request.

Section A — Full governance-entity coverage audit (verified against
rest-docs.synapse.org, and cross-checked field-by-field against the authoritative
OpenAPI spec at `~/Downloads/SynapseOpenApiSpec (1).json` where noted)

**Reviewed** (tagged `[REVIEW: implement fixes associated with Gap? == Yes]`):
all three `Gap? == **Yes**` rows are now covered by an execution-ready section
below -- `AccessApproval` (Section B), `ResearchProject`/`Site` (Section C), and
`DataAccessRequest`/`DataAccessRenewal` (new Section C.1, added specifically to
close this gap -- it wasn't covered by either plan before this review pass).

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

**Verified while drafting this section**: `AccessApproval.state` ranges over a
*different* enum than `DataAccessSubmission`'s (`org.sagebionetworks.repo.model.ApprovalState`
— `APPROVED`/`REVOKED` only, not `SubmissionStateEnum`'s
`SUBMITTED`/`APPROVED`/`REJECTED`/`CANCELLED`). Needs its own new
`ApprovalStateEnum` in `governance_graph.yaml`, not a reuse of
`SubmissionStateEnum` — a real, easy-to-miss distinction confirmed directly
against the OpenAPI spec before finalizing this design.

- No committed example data exists for this (unlike `DataAccessSubmission`), so
  author one new `linkml/examples/governance_graph/access_approval.example.yaml`,
  keyed to the same AR/principal ids the existing `data_access_submission*`
  examples already use, so the two connect in the rendered graph. **Confirmed.**
- Wire into `build_governance_graph.py`: add `"access_approval"` to
  `EXAMPLE_CLASSES` and a new `add_access_approval()`. **Confirmed.**
- **Decided** (tagged `[CONFIRM: agree with using AccessApproval as source
  node]`): `gov:hasApproval` is re-derived from the new `AccessApproval` node
  (`state == APPROVED`, mirroring `AccessApproval.state`'s own real enum, not
  `DataAccessSubmissionStatus.state`) as the primary, authoritative source going
  forward. The existing `DataAccessSubmissionStatus`-sourced edge in
  `add_data_access_submission_status()` is left as-is rather than removed --
  `authorize.py`'s SPARQL contract doesn't touch either, so this is a pure
  addition, not a breaking change to the workflow/audit-trail signal that
  already exists.
- Add a `sagegov:AccessApproval` `sh:NodeShape` (per the alignment plan's own
  additive-safe pattern) and the matching OWL TBox declaration. **Confirmed.**

Section C — Resolving alignment-plan point 4 (`Program`/`Site`/
`AccessRequirementTemplate`)

New finding narrows, but doesn't resolve, this question: `ResearchProject`
(behind every `DataAccessSubmission`) carries a real, verified `institution`
field — i.e. Synapse *does* capture a per-request institution/site signal, just
not the `Program`→`Site`→`IRBRequirement`→`extendsTemplate` reuse structure
thomasyu888's example illustrates.

- **Revised** (tagged `[REVIEW: implement site node, too]`): model `ResearchProject`
  as its own class (same treatment as `AccessApproval` above) *and* add a real
  `gov:Site` class, rather than leaving `institution` as a bare literal.
  `ResearchProject`: `institution`, `projectLead`, `intendedDataUseStatement` as
  slots, replacing the dangling `researchProjectId` FK string on
  `DataAccessSubmission` with a real node + edge. `Site` (`class_uri:
  sagegov:Site`): not `is_a: BaseEntity` -- Synapse never gives a stable Site
  id, only a free-text institution *name* string, so `gov:Site` nodes are
  minted deterministically by slugifying that name (e.g. `"Mount Sinai"` →
  `gov:site-mount-sinai`), the same "derive a stable node from real but
  non-id-shaped data" pattern `add_principal()` already uses for bare integer
  ids. `ResearchProject` (and `DataAccessRequest`, per Section C.1) get a
  `gov:affiliatedWith` edge to the matching `Site` node.
- **Corrected** (tagged `[REVIEW: we should expect to associate people with
  sites]` -- the plan's first draft was wrong here, not just narrow, and the
  fix was to go check a real object I hadn't looked at yet, not to soften the
  language): Synapse's `UserProfile` REST object has a real `company` field
  ("This person's current affiliation") -- a genuine per-`Principal`
  institution signal, verified directly against the OpenAPI spec. This
  resolves the target ontology's `gov:affiliatedWith` on `Principal` (a person
  affiliated with a site) as real, not just an `AffiliationCredential`
  aspiration: add a `company` slot to the existing `Principal` class (named to
  match the live field, despite the term reading oddly for an academic
  institution) and a `gov:affiliatedWith` edge from `Principal` to the same
  `Site` node `ResearchProject`/`DataAccessRequest` mint from their own
  `institution` string -- one `Site` concept, fed by three independent real
  Synapse signals. **Real, narrower caveat this time** (type-scoped, not
  absent): `UserProfile`/`company` only applies to `principalType: User` --
  `Team` (per the real `Team` object's fields: `id`/`name`/`description`/
  `icon`/`canPublicJoin`/`canRequestMembership`/audit fields) has no
  institution/affiliation field at all, so `Team`-type `Principal`s never get
  a `company`/`affiliatedWith` edge. Update `principal_user_2000001.example.yaml`
  with a real `company` value (picking the same institution name used for the
  `ResearchProject`/`DataAccessRequest` examples, so the `Site` node they
  produce visibly converges in the rendered graph, not just in the schema);
  leave `principal_team_x.example.yaml` (a `Team`) without one.
- **Resolved directly by the user** (tagged `[REVIEW: language is not standard
  across AR templates, but things can be reused... this target schema
  represents the ideal state... we should be integrating these features]`):
  checking `mc2-center-dcc` was marked `[NOT NECESSARY]` and the public-docs
  check is superseded by this direct domain answer -- AR template language
  isn't standardized across sites, but reuse does happen in practice, and the
  target ontology (`Program`/`Site`/`IRBRequirement`/`AccessRequirementTemplate`/
  `extendsTemplate`) is confirmed as the direction to build toward, not a
  speculative one-off to reject. New Section C.2 below designs this,
  deliberately wired into the modeling already done in this repo and in the
  alignment plan, rather than built from nothing.

Section C.1 — Modeling `DataAccessRequest`/`DataAccessRenewal` (new; closes
Section A's `DataAccessRequest`/`DataAccessRenewal` gap, per the
`[REVIEW: implement fixes associated with Gap? == Yes]` note on Section A)

Add a `DataAccessRequest` class (`class_uri: sagegov:DataAccessRequest`,
`is_a: BaseEntity` -- like `AccessGrant`/`DataAccessSubmission`, no natural key
of its own, mints a synthetic dotted id) mirroring the real, OpenAPI-verified
`RequestInterface`/`Request`/`Renewal` object. **Important field-shape note,
confirmed directly against the spec so this class doesn't repeat
`DataAccessSubmission`'s original mistake**: `RequestInterface` uses
`createdBy`/`createdOn`/`modifiedBy`/`modifiedOn` -- *not*
`submittedBy`/`submittedOn` -- unlike `Submission`. These two live Synapse
objects use different field names for a similar concept; don't copy
`DataAccessSubmission`'s (corrected) field names onto this class by analogy.

Slots: `accessRequirementId` (→ `gov:AR-<n>`, reusing the `gov:accessRequirement`
predicate per the existing cross-class-reuse convention), `researchProjectId`
(→ the new `ResearchProject` node from Section C), `institution` (→ a `gov:Site`
node via `gov:affiliatedWith`, same as `ResearchProject`), `createdBy`/`createdOn`/
`modifiedBy`/`modifiedOn`/`etag`, `concreteType` (literal `"Request"` or
`"Renewal"`). `Renewal`'s extra `publication`/`summaryOfUse` fields: add as
optional slots, populated only on renewal instances.

`principalInvestigator` (`userId`/`name`/`institutionalEmail`) and
`signingOfficial` (`name`/`institutionalEmail`) are real nested sub-objects in
the live API, not flat strings. **Scope decision**: flatten them into
`requestPrincipalInvestigatorName`/`requestPrincipalInvestigatorEmail`/
`requestSigningOfficialName`/`requestSigningOfficialEmail` literal slots for
this pass -- they have no independent identifier of their own and nothing else
in this graph needs to reference them individually, so a full nested class
would be premature structure. Documented as a flattening decision, not a
faithfulness gap: `signingOfficial` in particular is a plausible seed for
richer Site-level-authority modeling later (an institution's signing official
is exactly the kind of Site-affiliated Principal Section C.2's `Site` doesn't
yet capture), noted as future work rather than built now. **Confirmed**
(tagged `[AGREE]`) -- staying future work; not folded into this pass now that
`Principal.company`/`affiliatedWith` (above) covers the more general
per-Principal case with real data already.

`DataAccessSubmission.requestId`: now that `DataAccessRequest` is a real class,
change this slot's `range` from `integer` to `DataAccessRequest` (was added as
a bare integer in the field-name-fix commit specifically because no `Request`
node existed yet) -- `build_governance_graph.py`'s emission for it becomes an
IRI reference to the real `gov:DataAccessRequest-<n>` node instead of a literal.

Section C.2 — `Program`/`Site`/`AccessRequirementTemplate`/`IRBRequirement`
(new; the target-ontology direction the user confirmed above, deliberately
wired into `Condition` (alignment plan) and `governanceduo:Study` (already in
this repo), not built as a disconnected new layer)

**Honest grounding check, done before design, not skipped**: no real Synapse
REST object or existing repo data gives Program-level (multi-site consortium)
grouping or AR-template-reuse structure -- this is unchanged from the earlier
finding. What's different now is the user's direct confirmation that this is
the intended direction, so the response here is to build the *structural*
capability now, integrated with real data everywhere real data exists, and
explicitly flagged as illustrative-only exactly where it doesn't.

- `gov:AccessRequirementTemplate` (`class_uri: sagegov:AccessRequirementTemplate`):
  `domain` (free-text research domain, e.g. `"genomics"`), `hasCondition` →
  **reuses the `Condition` class from `plans/rebac_governance_graph_alignment.md`
  directly** -- a template's reusable conditions are `gov:Condition` nodes, the
  same DUO-code-backed nodes already minted from real `dataUseModifiers` data.
  This is the concrete "integrate what we've already done" connection: real
  `Condition` data (e.g. `gov:AR-42-condition-DUO-0000007`, from the alignment
  plan) can attach to a template exactly the way it attaches to an
  `AccessRequirement` stub today.
- `gov:IRBRequirement` (`class_uri: sagegov:IRBRequirement`): `extendsTemplate`
  → `AccessRequirementTemplate`, `arType`, `studyId`, `language`,
  `scopedToProgram` → `Program`, `scopedToSite` → `Site` (Section C).
  `studyId` **bridges to this repo's existing `governanceduo:Study`** via the
  same `owl:sameAs` pattern `add_access_requirement_association()` already uses
  for `gov:AR-<n>` ↔ `governanceduo:access_requirement.<n>` -- `Study` already
  has a real example (`study.mc2-jax-5xfad`) and a real `AccessRequirementKey`
  link to an `AccessRequirement`, so this is a genuine integration point, not
  an invented one. **Caveat, stated plainly**: `Study` (per `linkml/study.yaml`'s
  own description, "Studies associated with a grant") models a single research
  study, one level more granular than the target ontology's `Program`
  (a multi-site consortium like AD Knowledge Portal or NF-OSI spanning many
  studies) -- `Study` is the right bridge target for `IRBRequirement.studyId`,
  but it is *not* itself a `Program` equivalent. Don't conflate the two.
- `gov:Program` (`class_uri: sagegov:Program`): `name`. **No real data source
  exists for this one** (confirmed above) -- ship the class definition so the
  schema can represent Program-level scoping once DCC-curated data exists, but
  populate only one clearly-labeled illustrative example instance (not
  presented as sourced from a specific real AR), mirroring how thomasyu888's
  own PR #54 comment used illustrative `ex:program-adkp`/`ex:site-jhu`-style
  data for the same reason -- the whole PR is explicitly a concept/PoC.
- `gov:participatesIn` (`Site` → `Program`): same illustrative-only status as
  `Program` itself.
- Example data: one new `linkml/examples/governance_graph/irb_requirement.example.yaml`
  extending the real `ar-genomics`-equivalent template (reusing `access_requirement.42`'s
  real `Condition` data per above) with an illustrative `Program`/`Site` pairing,
  clearly commented as illustrative in the file header and in
  `docs/governance-graph-sync.md`.

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
don't assume. **Tagged `[Skip for now]`** -- not part of this pass's execution
list; still a live recommendation whenever the sync work itself is picked up.

Section E — `institutionDids`/ROR gap (from `plans/policy_fabric_alignment.md`)

**Correction** (tagged `[REVIEW: okay, implement as in policy fabric alignment
plan]` -- checked before implementing anything further, since the tag implied
this wasn't done yet): `plans/policy_fabric_alignment.md` is **already fully
implemented** in this repo, verified directly, not assumed -- `institutionDids`
exists in `mixins.yaml` with exactly the specified pattern/multivalued/comment;
`linkml/policy_fabric.yaml`, `linkml/policy_fabric_bindings.yaml`,
`PolicyFabricMixin` (applied to `AccessRequirement`), `scripts/build_policy_fabric.py`,
and the `make policy-fabric` target all exist and match that plan's execution
list. There is nothing left to implement here -- the "gap" this section
originally described is the *intentional, permanent* design outcome of that
plan (ROR ids and DIDs both kept as separate fields, since no automatic
ROR→DID resolution exists), not unfinished work. No action needed; flagging
this correction explicitly rather than silently adding a redundant task.

Execution task list — IMPLEMENTED (2026-09-03)

1. **Done.** Added `AccessApproval` class (+ new `ApprovalStateEnum` --
   verified `APPROVED`/`REVOKED` directly against the spec while
   implementing) + example instance + `add_access_approval()` (re-derives
   `gov:hasApproval`, per Section B's decision) + SHACL/OWL shapes.
2. **Done.** Added `ResearchProject` class + `Site` class + a `company` slot
   on `Principal` + example instances (`principal_user_2000001.example.yaml`
   now has `company: Mount Sinai`, matching `ResearchProject`/
   `DataAccessRequest`'s institution) + `site_node_for()` helper (slugifies
   institution/company) + `gov:affiliatedWith` edges from `ResearchProject`,
   `DataAccessRequest`, and `User`-type `Principal` + SHACL/OWL shapes.
   Verified all four converge on the identical `gov:site-mount-sinai` node.
3. **Done.** Added `DataAccessRequest` class using its own real field names
   (`createdBy`/`createdOn`/`modifiedBy`/`modifiedOn` -- confirmed not
   `submittedBy`/`submittedOn`) + example instance + wiring, and changed
   `DataAccessSubmission.requestId`/`researchProjectId`'s range from
   `integer` to `DataAccessRequest`/`ResearchProject` respectively + SHACL/OWL
   shapes.
4. **Done.** Added `AccessRequirementTemplate`/`IRBRequirement`/`Program`
   classes + `extendsTemplate`/`scopedToProgram`/`scopedToSite`/
   `participatesIn` predicates + one illustrative example. Verified the
   *same* real `Condition` node (`gov:AR-42-condition-DUO-0000007`) is
   reachable from both `gov:AR-42` and the template -- genuine reuse, not a
   duplicate. `IRBRequirement`'s `owl:sameAs` bridge to
   `governanceduo:study.mc2-jax-5xfad` resolves correctly. `Program`/the
   Program-Site pairing marked explicitly illustrative in the schema
   docstrings and `docs/governance-graph-sync.md`.
5. **Done.** Skipped the `mc2-center-dcc`/ADKP/NF-OSI documentation check
   entirely, per the user's direct domain answer.
6. **Done.** Updated `docs/governance-graph-sync.md`: full entity-coverage
   table added (with the reviewed-and-out-of-scope rows) plus new
   `AccessApproval`/`ResearchProject`/`DataAccessRequest`/`Site`/
   `AccessRequirementTemplate`/`IRBRequirement`/`Program` rows; open design
   question #5 marked resolved-in-direction with what's still honestly
   illustrative-only.
7. **Done.** Regenerated `governance_graph_export/governance_graph.ttl` (100
   triples, up from 50) and the downstream umbrella artifacts (`make owl`/
   `make shacl`/`make docs`).
8. **Done.** Left Section D's 4 sync questions and Section E as documented --
   Section E required a correction (see its own text) rather than new work.

Not part of this execution list: Section E (already fully implemented,
verified above -- no task needed).

Verification

All passed (2026-09-03):

1. `make linkml-lint` (exit 0, only expected `standard_naming` warnings),
   `make shacl-validate`, `make governance-graph-validate` — all
   `Conforms: True`.
2. Ran the exact smoke queries: `principal-2000001`, `research-project-8001`,
   and `data-access-request-7001` all resolve `gov:affiliatedWith` to the
   identical `gov:site-mount-sinai` node — real convergence, verified by
   query, not asserted. `gov:access-requirement-template-ar-genomics
   gov:hasCondition ?c` and `gov:AR-42 gov:hasCondition ?c` both resolve to
   the same `gov:AR-42-condition-DUO-0000007` node (`gov:duoCode
   "DUO:0000007"`) — confirmed via a query joining both paths, not just two
   separate queries that happened to return the same string.
3. Grepped the regenerated graph directly: `gov:hasACL`/`gov:AccessGrant`/
   `gov:principal`/`gov:permission`/`gov:bindingType`/
   `gov:hasAccessRequirement` triples are unchanged.
4. `gov:irb-requirement-irb-genomics-adkp owl:sameAs
   governanceduo:study.mc2-jax-5xfad` — confirmed via query, resolves to the
   real Study individual, not a stub.
