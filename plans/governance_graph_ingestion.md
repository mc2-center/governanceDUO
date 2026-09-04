Governance Graph ingestion: sourcing, sequencing, resolved design decisions, and
curator-table schemas

This plan supersedes and merges two prior documents, whose content now lives here in
full: `docs/governance-graph-sync.md` (deleted) and
`plans/governance_graph_ingestion_sourcing.md` (deleted). It also revises several
things a first pass got wrong or left open — corrected live against
rest-docs.synapse.org this session, not left as stubs — see "Corrections from the
prior pass" below.

**Section 5's schema changes are implemented, and so is the sync script**
(2026-09-04) — `scripts/sync_governance_graph.py`, following Sections 2/4/6's
design; see `governance_graph_ingestion_report.md` for both phases, including two
pull-order simplifications and one real bug the build surfaced that this plan text
didn't anticipate. Untested against live Synapse (no credentials in this
environment) — verified instead with mocked REST responses and a real pySHACL pass
against the hand-authored shapes; a live smoke test is still the right next step
before trusting this in production.

Context

Every class in `governance_graph.yaml` was verified column-by-column against real
Synapse REST objects/tables so a real sync could exist, but
`scripts/build_governance_graph.py` only ever runs against hand-authored examples
under `linkml/examples/governance_graph/` today. This plan answers three things: (1)
where each piece of data should come from, prioritizing the Synapse REST API, (2)
exactly which attributes have no live Synapse source and must be captured separately,
and (3) the LinkML schema each of those separately-captured attributes belongs to —
either an existing class (nothing new to build) or a concrete proposed addition.

Ground rules for this plan, per explicit direction

- **LinkML is the sole source of truth for every existing data model.**
  `model/*.model.csv` (`Study.model.csv`, `AccessRequirement.model.csv`, etc.) and the
  `schematic`-driven Makefile targets that build from them (`build-csv`, `collate`,
  `convert`) are legacy and are not treated as authoritative anywhere in this plan —
  where they're mentioned at all below, it's only to note that a class described
  there is now fully described by its LinkML schema instead, never as a design input.
- **The archived Data Dictionary / `generate_duo_schema.py` framework is ignored
  entirely**, per direction that it was a pilot process being superseded, not a
  design to stay compatible with. It is not cited anywhere below as a source of
  requirements, format, or precedent. (One consequence: the previous version of this
  plan leaned on that framework's `duo_shorthand` annotation format to argue DUO
  conditions could be *partially* recovered from Synapse annotations. That argument
  is dropped in this version — see Section 3.)
- **Every attribute that needs separate capture must have an underlying LinkML
  schema** — no informal spreadsheet formats. Section 4 below states, for every such
  attribute, which existing class already covers it (most of them — no new schema
  needed) versus what's genuinely new.

1. Corrections from the prior pass (checked directly this session, not left open)

Four of the six items the prior version of this plan flagged as "needs a live
check" were actually checkable without Synapse credentials — rest-docs.synapse.org
is public API documentation, not an authenticated endpoint. Checked directly:

- **`sourceAclId`/`sourceAclResourceAccessId` (on `AccessGrant`) do not exist in the
  public REST API at all — confirmed, not just suspected.** `AccessControlList.id`
  *is* the entity id, not a separate ACL-record id; `ResourceAccess` has exactly two
  fields, `principalId` and `accessType` — no row id of any kind. **Resolution:**
  remove both slots from `AccessGrant` in `governance_graph.yaml`. They can never be
  populated by any REST-based sync, under any credential — keeping them would just
  be two fields permanently documented as "traceability," never traceable to
  anything. (Listed as a target schema change in Section 5.)
- **`ResearchProject` has no general-purpose GET endpoint — and the one endpoint
  that exists is a hard blocker for a DCC-wide sync.** The only GET is
  `GET /accessRequirement/{requirementId}/researchProjectForUpdate`, and its own
  documentation states plainly: "Only the owner of the researchProject can perform
  this action" — it returns *the caller's own* ResearchProject only, never anyone
  else's. **Resolution:** don't use this endpoint at all. Instead, source
  `ResearchProject` from `researchProjectSnapshot` — a **full embedded
  `ResearchProject` object** on every `Submission` returned by
  `POST /accessRequirement/{requirementId}/submissions` (confirmed by inspecting
  `Submission`'s own field list). That endpoint's own authorization is "Only an ACT
  member can perform this action" — broader than any individual owner, and it's
  already the endpoint this plan pulls `DataAccessSubmission`/`DataAccessSubmissionStatus`
  from, so no new call is needed at all. One correction to the class's field list
  along the way: `ResearchProject` also has `modifiedOn`/`modifiedBy`, missing from
  the prior version of this plan.
- **`DataAccessRequest` has the identical owner-only restriction, and — unlike
  ResearchProject — `Submission` does *not* embed a full snapshot of it, only a bare
  `requestId` reference.** This is a real, unavoidable gap: there is no REST path,
  under any credential (including ACT), to fetch another user's
  `DataAccessRequest`. **Resolution, not left open:** two of its fields
  (`publication`, `summaryOfUse`) are also present directly on `Submission` itself
  and are recoverable from the same `POST .../submissions` call — no gap there. The
  rest (`institution`, `requestPrincipalInvestigatorName/Email`,
  `requestSigningOfficialName/Email`, `requestConcreteType`, and the request's own
  `createdBy`/`createdOn`/`modifiedBy`/`modifiedOn`) have no REST source for any
  submission the syncing credential doesn't itself own. This is **not** proposed as
  a spreadsheet/curator-table item — it's high-cardinality, per-submitter data
  covering every researcher who ever submits an AR request, not a small set of
  DCC-owned facts a curator can reasonably re-type. The correct handling is to
  accept it as a documented platform limitation: the sync populates these fields
  when it can (self-owned submissions) and leaves them null otherwise, consistent
  with the warn-don't-block posture below — not an error, not something this plan
  can close.
- **The submissions-list endpoint itself requires ACT membership.** This changes the
  auth answer below (item 4).

The other two checks need live Synapse access this environment doesn't have, and are
not guessable from public docs alone — narrowed as much as possible, not left as
open-ended "needs a check":

- Whether `GET /entity/{id}/acl`/`GET /entity/{id}/accessRequirement`/
  `GET /entity/{id}/benefactor` behave as expected for an entity the ACT-credentialed
  sync account can read but doesn't own (standard Synapse permission model says yes —
  these are ordinary read-scoped entity endpoints, not owner-restricted like the two
  above — but this is inference from the general permission model, not a
  direct per-endpoint confirmation the way the items above are).
- Exact request/response shapes in practice (field presence/nullability under real
  data) — public docs describe the schema; only a live call confirms real-world
  behavior matches it exactly.

2. Resolved design decisions

1. **Sync script location**: this repo, alongside `build_governance_graph.py`.
2. **Sync cadence**: on-demand CLI run, not scheduled or event-driven.
3. **Incomplete data**: warn, don't block — applies to any AccessRequirement missing
   companion-condition data (Section 3) and to `DataAccessRequest`'s unreachable
   fields (Section 1) alike.
4. **Auth — corrected from the prior pass, not merely re-asked.** "The curator's own
   credentials," the prior resolution, cannot work: it would make
   `POST /accessRequirement/{id}/submissions` return 403 (ACT-only), while gaining
   nothing on `DataAccessRequest`/`ResearchProject`'s owner-only endpoints (which
   this plan no longer calls anyway, since `researchProjectSnapshot` supersedes the
   `ResearchProject` one and there's no comparable path for `DataAccessRequest`).
   **The sync must run under a credential with ACT membership** (or, per
   `GET /dataAccessSubmission/{id}`'s own documented alternative, a validated
   reviewer for the specific ARs in scope) — that single requirement satisfies every
   endpoint this plan actually calls, including the plain-entity ones, since ACT
   membership is a superset of ordinary read access.
5. **Program/Site/AR-template reuse**: no real Synapse or repo data source exists;
   addressed by the curator-table schemas in Section 4, not a future Synapse feature.

3. DUO conditions: 100% curator-authored, and already fully schema-defined

Confirmed directly against rest-docs.synapse.org, independent of any pilot process:
Synapse's native `AccessRequirement` interface has **no data-use-condition fields at
all** — `id`, `concreteType`, `accessType`, `subjectIds`,
`subjectsDefinedByAnnotations`, plus audit fields, nothing else.
`dataUseModifiers`/companion slots have never been part of that object and never will
be from Synapse's own data model — this isn't a temporary sourcing gap, it's a
structural fact about what Synapse's `AccessRequirement` is.

There is therefore no partial-recovery mechanism to design here (the prior version of
this plan proposed reverse-parsing a `duo_shorthand` convention out of Synapse entity
annotations — that convention was produced by the archived Data Dictionary pilot,
which is out of scope per the ground rules above, and nothing guarantees future
annotations follow it). Instead: **`dataUseModifiers` and every one of
`GovernanceMixin`'s 24 companion slots are curator-authored data, full stop**, and —
checked directly — the schema for this already exists and needs no changes:
`linkml/access_requirement.yaml`'s `AccessRequirement` class already declares every
one of these slots (via the `GovernanceMixin` mixin) and is already `tree_root: true`
— it is already a valid top-level curator-input target. **No new schema is proposed
for this.** The 24 companion slots, for reference (`GovernanceMixin.rules` in
`linkml/mixins.yaml`, 35 rules total — `requiredAgreementDocumentId`/
`allowedPurposes`/`prohibitedPurposes` are each required by more than one DUO code):

| Companion slot | Required by |
| --- | --- |
| `diseaseSpecificResearch` | `DUO:0000007` |
| `researchSpecificRestrictions` | `DUO:0000012` |
| `collaborationRequired` | `DUO:0000020` |
| `geographicalRestriction` | `DUO:0000022` |
| `publicationMoratorium` | `DUO:0000024` |
| `timeLimitOnUse` | `DUO:0000025` |
| `userSpecificRestriction` | `DUO:0000026` |
| `institutionSpecificRestriction` | `DUO:0000028` |
| `sourceGeography` | `DUOPlus1` |
| `populationType` | `DUOPlus2` |
| `deidentificationType` | `DUOPlus3` |
| `dataPermission` | `DUOPlus4` |
| `dataTier` | `DUOPlus5` |
| `license` | `DUOPlus6` |
| `attribution` | `DUOPlus7` |
| `requiredAgreementDocumentId` | `DUO:0000042`, `DUO:0000024`, `DUO:0000029`, `DUO:0000025` |
| `notAfter` | `DUO:0000025` |
| `allowedPurposes` | `DUO:0000016`, `DUO:0000006`, `DUO:0000011`, `DUO:0000012` |
| `prohibitedPurposes` | `DUO:0000006`, `DUO:0000015`, `DUO:0000046`, `DUO:0000018`, `DUO:0000044` |
| `nonprofitLegalForms` | `DUO:0000018`, `DUO:0000045` |
| `approvedProjects` | `DUO:0000027` |
| `approvedUsers` | `DUO:0000026` |
| `allowedAccountTypes` | `DUO:0000026` |
| `requiredProfileStatuses` | `DUO:0000026` |

A curator-authored `AccessRequirement` record either satisfies `GovernanceMixin`'s
`rules:` for the DUO codes it declares, or it doesn't — that's exactly what
`linkml-validate` already checks (per `scripts/validate_graph.py`'s own docstring).
The sync's job is to read this already-real, already-validated record and merge it
onto the `AccessRequirementReference` stub via `owl:sameAs` (already built — see
`plans/access_requirement_reference_class.md`) — not to reconstruct it from Synapse.

4. What's fully Synapse-sourced vs. what's captured separately — the delineation

**Fully Synapse-sourced (pull order, dependency-ordered; call these, never
hand-type):**

A sync run starts from one or more explicitly-supplied Synapse entity ids (Section 6,
item 1 below — no implicit recursive walk in this version).

1. `GET /entity/{id}` → `SynapseEntity`: `name`, `nodeType`, `parentId`, `alias`,
   `currentRevNum`, `maxRevNum`, `etag`, `createdBy` (raw literal userId),
   `createdOn`.
2. `GET /entity/{id}/acl` → one `AccessGrant` (`resource`, `principal`, `permission`,
   `createdOn`) per `resourceAccess[]` entry, one `Principal` stub (bare
   `principalId`) per distinct id seen.
3. `GET /entity/{id}/accessRequirement` → `AccessRequirementAssociation` (`resource`,
   `accessRequirement`) bindings and the set of `accessRequirement` ids in scope.
4. `GET /entity/{id}/benefactor`, compared against steps 2-3 → resolves
   `bindingType` (Direct vs. Inherited) for both `AccessGrant` and
   `AccessRequirementAssociation`.
5. For every distinct `principalId` from step 2: resolve `principalType` (User vs.
   Team — `GET /userProfile/{id}` succeeding vs. `GET /team/{id}`, or a batch
   `/userGroupHeaders/batch` call) and, for User principals only, `company`
   (`UserProfile.company`).
6. For every distinct `accessRequirement` id from step 3:
   a. `GET /accessRequirement/{requirementId}` → the `AccessRequirementReference`
      stub's structural fields (the `owl:sameAs` target).
   b. `POST /accessRequirement/{requirementId}/submissions` (ACT-authorized — see
      Section 2, item 4) → `DataAccessSubmission` (`accessRequirementVersion`,
      `requestId`, `researchProjectId`, `submittedBy`, `submittedOn`, `modifiedBy`,
      `etag`, plus `publication`/`summaryOfUse` sourced from here rather than
      `DataAccessRequest` — Section 1) and, per submission,
      `GET /dataAccessSubmission/{submissionId}` → `DataAccessSubmissionStatus`
      (`state`, `rejectedReason`, `modifiedOn`).
   c. Per submission: `GET /accessApproval/{approvalId}` or
      `GET /dataAccessSubmission/{submissionId}/userAccessApproval` →
      `AccessApproval` (`requirementId`, `requirementVersion`, `submitterId`,
      `accessorId`, `status`, `expiredOn`, `createdOn`, `etag` — not
      `sourceApprovalId`; see below).
   d. `ResearchProject` (`institution`, `projectLead`, `intendedDataUseStatement`,
      `createdBy`, `createdOn`, `modifiedBy`, `modifiedOn`, `etag`) — read directly
      from step 6b's `Submission.researchProjectSnapshot`, per the Section 1
      correction. No separate call.
7. `Site` — not fetched at all; derive deterministically by slugifying the
   `institution`/`company` strings already collected in steps 5-6
   (`site_node_for()`, already built).

**Note on `AccessApproval.sourceApprovalId`**: unlike the two `AccessGrant` fields
removed in Section 1, `AccessApproval.id` *is* a real top-level field on the actual
`AccessApproval` REST object (confirmed by its own class description in
`governance_graph.yaml`, not re-verified this session but not contradicted by
anything checked) — this one stays, and is populated directly.

**Derived, not fetched or typed anywhere:** `Site`;
`gov:affiliatedWith`/`gov:hasACL`/`gov:hasAccessRequirement`/`gov:hasApproval`
(convenience/join triples computed from data already pulled, never independently
sourced — `gov:hasCondition` is the one exception, already a real
`AccessRequirementReference` slot); `source` on `AccessGrant`/
`AccessRequirementAssociation` (always the literal `"Synapse"`, hardcoded by the
script).

**Captured separately, with the LinkML schema that already covers it, per attribute:**

| Data | LinkML schema | New schema needed? |
| --- | --- | --- |
| `dataUseModifiers` + all 24 companion condition slots (Section 3) | `access_requirement.yaml`'s `AccessRequirement` (`GovernanceMixin`) | No — already `tree_root: true`, already declares every slot |
| `Study` (everything `IRBRequirement.studyId` bridges to) | `study.yaml`'s `Study` | No — already `tree_root: true` |
| `Program` (`id`, `name` — its entire surface) | `governance_graph.yaml`'s `Program` | Needs `tree_root: true` added (Section 5) — no new class |
| `AccessRequirementTemplate` (`id`, `domain` — `hasCondition` is reused from a real AR's already-curator-authored conditions, not independently typed here, confirmed by reading `add_access_requirement_template()`) | `governance_graph.yaml`'s `AccessRequirementTemplate` | Needs `tree_root: true` added — no new class |
| `IRBRequirement` (`id`, `extendsTemplate`, `arType`, `studyId`, `language`, `scopedToProgram`, `institution` — `scopedToSite` is derived from `institution`, not separately entered) | `governance_graph.yaml`'s `IRBRequirement` | Needs `tree_root: true` added — no new class |
| `DataAccessRequest`'s owner-only-restricted fields (Section 1) | N/A | **Not a spreadsheet candidate** — per-submitter, high-cardinality, accepted platform-gap, not curator-owned data |

Every row either already has a `tree_root: true` LinkML class, or needs only that
one flag added to an existing class — this plan proposes **zero new LinkML classes**,
a simplification from the prior version (which proposed a new
`AccessRequirementConditionSupplement` class that turned out to be unnecessary once
the DUO-conditions question was resolved cleanly in Section 3).

5. Target schema changes

```yaml
# linkml/governance_graph.yaml
  Program:
    is_a: BaseEntity
    class_uri: sagegov:Program
    tree_root: true          # new
    ...
  AccessRequirementTemplate:
    is_a: BaseEntity
    class_uri: sagegov:AccessRequirementTemplate
    tree_root: true          # new
    ...
  IRBRequirement:
    is_a: BaseEntity
    class_uri: sagegov:IRBRequirement
    tree_root: true          # new
    ...
  AccessGrant:
    ...
    slots:
      - resource
      - principal
      - permission
      - source
      - bindingType
      - createdOn
      # sourceAclId / sourceAclResourceAccessId removed -- confirmed (Section 1) not
      # exposed by the public REST API under any credential; kept them would mean
      # two fields permanently, structurally unpopulatable by any real sync.
```

`sourceAclId`/`sourceAclResourceAccessId` also need their slot definitions removed
(or left orphaned/unused — removal is cleaner) and any hand-authored shapes
(`shapes/governance_graph.shacl.ttl`'s `AccessGrantShape`) and example instance data
(`linkml/examples/governance_graph/access_grant.example.yaml`) updated to match —
listed here so implementation doesn't miss them, not decided differently from the
removal itself.

6. Remaining implementation decisions (stated as decisions, not questions)

1. **Sync scope**: the CLI takes one or more entity ids as an explicit, required
   argument. No default recursive subtree walk and no "every entity under a given
   AccessRequirement" enumeration mode in this version — both are straightforward to
   add later behind an explicit flag (`--recursive`, `--for-access-requirement`) once
   the basic single/multi-entity flow is proven, but starting with implicit
   broad-scope traversal risks an accidental full-instance crawl on first use.
2. Everything else structural about the sync (module location, cadence, auth,
   warn-vs-block) is resolved in Section 2 — nothing left pending there.

7. Impact on graph content: do these changes create edge gaps, and can we still
   determine access?

Checked directly against what the graph's own access-determination logic actually
needs — none of Sections 1-6's changes weaken it. "Effective access = ACL permits AND
applicable Access Requirements are satisfied" (the design doc's own formula) resolves
from exactly three things, all fully Synapse-sourced and untouched by anything above:

1. `AccessGrant` (`GET /entity/{id}/acl`) — does an ACL grant give principal P (or a
   Team P belongs to) permission on resource R?
2. `AccessRequirementAssociation` (`GET /entity/{id}/accessRequirement`) — is an AR
   bound to R?
3. `gov:hasApproval` — asserted directly from `DataAccessSubmissionStatus.state ==
   APPROVED` (`add_data_access_submission()`) *or* `AccessApproval.status ==
   APPROVED` (`add_access_approval()`) — has P specifically satisfied that AR?

Per change:

- **`sourceAclId`/`sourceAclResourceAccessId` removal**: no impact at all. These are
  leaf literals on `AccessGrant`, not edges — `resource`/`principal`/`permission`/
  `bindingType` are untouched.
- **`ResearchProject` via `Submission.researchProjectSnapshot`**: a net improvement,
  not a gap — covers every submitter's `ResearchProject`, where the original
  owner-only endpoint would only ever have populated the sync credential's own.
- **`DataAccessRequest`'s owner-only fields**: a real gap, but a thin node, not a
  broken edge. `add_data_access_submission()` already emits
  `gov:data-access-submission-555 gov:requestId gov:data-access-request-7001` as a
  real edge, because the bare `requestId` comes from `Submission` itself, which the
  sync does have. What's missing is everything *on* that target node for a request
  the sync doesn't own (`institution`, PI/signing-official contacts,
  `requestConcreteType`) — pure reviewer-facing justification/context, never read by
  the three-step determination above.
- **Dropping annotation-parsed Conditions**: a real gap only for an AR with no
  curator-authored `AccessRequirement` record yet — its
  `AccessRequirementReference` stub exists with no `Condition`/`hasCondition` data
  attached (a warning, not a broken query, per the warn-don't-block decision). Where
  a curator-authored record *does* exist, `Condition` minting is unchanged.
  `Condition`/`dataUseModifiers` describe what an AR's terms *are* (for Policy
  Fabric, compliance review, human-readable display) — never read to decide whether
  an approval already on file counts.

Bottom line: the honest gaps this plan accepts (`DataAccessRequest` context data,
`Condition` data for not-yet-curated ARs) sit one layer outside the "who can access
what" query — they cost auditability/compliance-narrative completeness, not
authorization correctness.

Housekeeping (already done as part of the consolidation)

- `docs/governance-graph-sync.md` and `plans/governance_graph_ingestion_sourcing.md`
  deleted; `docs/index.md`, `docs/use-cases.md`, and `docs/.pages` repointed at this
  file's GitHub blob URL.
