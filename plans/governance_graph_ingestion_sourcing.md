Governance Graph data ingestion: source-by-source plan, prioritizing the Synapse
REST API, with what needs a spreadsheet instead

Context

`docs/governance-graph-sync.md` already identified, per class, where real Governance
Graph data should come from, and confirmed (against rest-docs.synapse.org and the
OpenAPI spec) that `scripts/build_governance_graph.py` only ever runs against
hand-authored examples today — nothing in this repo actually calls Synapse. This plan
takes that design doc as grounding (it is not re-verified here; two items it already
flagged as unconfirmed — the standalone ResearchProject endpoint, and
DataAccessRequest's rest-docs.synapse.org page having 403'd — are carried forward
below as open items, not resolved) and turns it into: (1) a concrete pull order, (2)
an explicit split of every class/slot into Synapse-API-sourced vs. spreadsheet-sourced
vs. derived, and (3) the specific fields to pre-populate in a spreadsheet before a
sync ever runs, which is what was asked for and which the design doc left implicit.

No implementation is proposed here beyond what docs/governance-graph-sync.md's own
"Proposed script changes" section already sketches (`scripts/sync_governance_graph.py`,
`parse_duo_annotations()`) — this plan is about *sourcing and sequencing*, not new
script architecture.

Guiding principle

Pull from Synapse everywhere Synapse actually has the data — every class below that
has a real REST/table source should never be hand-typed. Spreadsheets are for the
residual: data Synapse's schema has no field for at all (verified directly, not
assumed, in every case below), not a substitute for calling the API where it works.

1. Recommended pull order (dependency-ordered)

A sync run starts from one or more seed Synapse entity ids (a project, or an
individual file/folder) — scope selection itself is an open item, #4 below.

1. `GET /entity/{id}` → `SynapseEntity` structural fields.
2. `GET /entity/{id}/annotations2?includeDerived=true` → DUO-related annotations
   (feeds the `Condition` partial-parse in step 6, and `SynapseEntity`'s own
   DUO-relevant annotation fields per docs/governance-graph-sync.md's row 1).
3. `GET /entity/{id}/acl` → one `AccessGrant` per `resourceAccess[]` entry, one
   `Principal` stub (bare `principalId`) per distinct id seen.
4. `GET /entity/{id}/accessRequirement` → `AccessRequirementAssociation` bindings
   and the set of `accessRequirement` ids in scope for this entity.
5. `GET /entity/{id}/benefactor`, compared against the entity's own ACL/AR listing
   from steps 3-4 → resolves `bindingType` (Direct vs. Inherited) for both.
6. For every distinct `principalId` collected in step 3: resolve `principalType`
   (User vs. Team — via `GET /userProfile/{id}` succeeding vs. `GET /team/{id}`, or
   a batch `/userGroupHeaders/batch` call) and, for User principals only,
   `company` (`UserProfile.company`).
7. For every distinct `accessRequirement` id collected in step 4:
   a. `GET /accessRequirement/{requirementId}` → the `gov:AR-<n>` stub's structural
      fields (the `owl:sameAs` target).
   b. `POST /accessRequirement/{requirementId}/submissions` → `DataAccessSubmission`
      list; per submission, `GET /dataAccessSubmission/{submissionId}` →
      `DataAccessSubmissionStatus`.
   c. Per submission: `GET /accessApproval/{approvalId}` or
      `GET /dataAccessSubmission/{submissionId}/userAccessApproval` → `AccessApproval`
      (a separate real object, not derived from the submission itself).
   d. `ResearchProject` — from the submissions response's `researchProjectSnapshot`
      where present, else the standalone endpoint (path unconfirmed — see open item
      #1).
   e. `DataAccessRequest` — `GET /dataAccessRequest/{requestId}`, `requestId` taken
      from the `DataAccessSubmission` record fetched in (b).
8. Run `parse_duo_annotations()` (docs/governance-graph-sync.md's proposed function)
   against step 2's annotation payload, using `DataUseModifierEnum`'s
   `duo_shorthand` reverse-lookup (read from the schema at runtime, not hardcoded) →
   a partial `governanceduo:AccessRequirement` (`id`, `dataUseModifiers`,
   `entityIdList`) for each of the 24 real DUO terms that have a shorthand.
9. `Site` — not fetched at all; derive deterministically by slugifying the
   `institution`/`company` strings already collected in steps 6-7 (`site_node_for()`
   pattern already in `build_governance_graph.py`).

2. Fully Synapse-API-sourced (call these; never hand-type)

| Class | Slots | Endpoint(s) |
| --- | --- | --- |
| `SynapseEntity` | `name`, `nodeType`, `parentId`, `alias`, `currentRevNum`, `maxRevNum`, `etag`, `createdBy` (raw literal userId), `createdOn` | `GET /entity/{id}` |
| `Principal` | `principalId`, `principalType`, `company` (User only) | ACL `resourceAccess[].principalId`; `GET /userProfile/{id}` / `GET /team/{id}` |
| `AccessGrant` | `resource`, `principal`, `permission`, `bindingType`, `createdOn` | `GET /entity/{id}/acl`; `GET /entity/{id}/benefactor` for `bindingType` |
| `AccessRequirementAssociation` | `resource`, `accessRequirement`, `bindingType` | `GET /entity/{id}/accessRequirement`; `GET /entity/{id}/benefactor` |
| `gov:AR-<n>` stub (`owl:sameAs` target) | structural AR fields | `GET /accessRequirement/{requirementId}` |
| `DataAccessSubmission` | `accessRequirementId`, `accessRequirementVersion`, `requestId`, `researchProjectId`, `submittedBy`, `submittedOn`, `modifiedBy`, `etag` | `POST /accessRequirement/{id}/submissions`; `GET /dataAccessSubmission/{id}` |
| `DataAccessSubmissionStatus` | `submissionId`, `state`, `rejectedReason`, `modifiedOn` | same submission fetch |
| `AccessApproval` | `requirementId`, `requirementVersion`, `submitterId`, `accessorId`, `status`, `expiredOn`, `createdOn`, `sourceApprovalId`, `etag` | `GET /accessApproval/{id}` / `GET /dataAccessSubmission/{id}/userAccessApproval` — `AccessApproval.id` is a real top-level field on this object, unlike the ACL row ids below |
| `ResearchProject` | `institution`, `projectLead`, `intendedDataUseStatement`, `createdBy`, `createdOn`, `etag` | submissions' `researchProjectSnapshot`, or standalone endpoint (open item #1) |
| `DataAccessRequest` | `institution`, `requestPrincipalInvestigatorName/Email`, `requestSigningOfficialName/Email`, `createdBy`, `createdOn`, `modifiedBy`, `modifiedOn`, `requestConcreteType`, `publication`, `summaryOfUse` | `GET /dataAccessRequest/{id}` (open item #2) |
| `Condition` (partial) | `id`, `dataUseModifiers`, `entityIdList` — 24 real DUO terms only | `GET /entity/{id}/annotations2?includeDerived=true`, via `duo_shorthand` reverse lookup |

3. Derived, not fetched or typed anywhere

- `Site` — slugified from `institution`/`company` strings already pulled above; no
  independent existence in Synapse (confirmed: Synapse gives no stable Site id at
  all, per `governance_graph.yaml`'s `Site` class description).
- `gov:affiliatedWith`, `gov:hasACL`, `gov:hasAccessRequirement`, `gov:hasCondition`,
  `gov:hasApproval` — convenience/join triples computed by
  `build_governance_graph.py` from data already pulled above, never independently
  sourced.
- `source` (on `AccessGrant`/`AccessRequirementAssociation`) — always the literal
  `"Synapse"` for anything this pipeline produces; the ingestion script should
  hardcode it, not look it up per record.

4. What belongs in a spreadsheet, curated *before* any sync runs, and why each one
   can't just be pulled live

This is the direct answer to "which pieces make more sense to capture in a
spreadsheet instead of pulling from Synapse" — every item below was checked directly
(not assumed) to have no live source, per `docs/governance-graph-sync.md` and
`plans/governance_graph_open_questions.md` Section C.2:

1. **`AccessRequirementTemplate`, `Program`, and `IRBRequirement`'s
   `extendsTemplate`/`arType`/`language`/`scopedToProgram`** — zero Synapse source
   exists for AR-template reuse or multi-site Program grouping at all: verified
   directly that Synapse's `AccessRequirement` has only `subjectIds` as a
   compositional mechanism, nothing above the individual-entity level. A DCC-curated
   spreadsheet (one row per Program, one per AccessRequirementTemplate, one per
   IRBRequirement instance with its `extendsTemplate`/`scopedToProgram`/`scopedToSite`
   foreign keys) is the only source these fields can ever have — this isn't a gap a
   future Synapse feature would close on its own, it's organizational data Synapse's
   object model doesn't represent.
2. **`Condition` companion slots** (`nonprofitLegalForms`, `geographicalRestriction`,
   and every other slot `GovernanceMixin`'s conditional `rules:` require for a
   specific DUO code) — confirmed absent from the Data Dictionary CSV that seeds
   Synapse's derived annotations, so no annotation pull, however complete, will ever
   surface them. Needs a curator spreadsheet keyed by AccessRequirement id (or by DUO
   code, since the same companion slot can be required by multiple codes — e.g.
   `requiredAgreementDocumentId` is the postcondition for 4 different codes) supplying
   just these values, merged with the Synapse-parsed `dataUseModifiers`/`entityIdList`
   from step 8 above before Policy Fabric generation runs.
3. **`DUOPlus1`–`DUOPlus7` usage on any AccessRequirement** — these 7 Sage-local DUO
   extensions have no `duo_shorthand` tag (only the 24 real DUO terms do), so the
   annotation-parsing path in step 8 can structurally never recover them, regardless
   of how complete Synapse's own data is. Any AccessRequirement whose real
   `dataUseModifiers` includes a DUOPlus code needs that value spreadsheet-sourced
   (or at minimum spreadsheet-confirmed against the parsed annotation output) rather
   than trusted to automatic parsing.
4. **`Study` and everything `IRBRequirement.studyId` bridges to** — already sourced
   from the DCC's schematic/CSV Data Dictionary pipeline (`Makefile`'s
   `build-csv`/`collate`/`convert` targets over `model/*.model.csv`), not from
   Synapse REST calls at all. No change needed here — flagging only so it's clear
   this class is already spreadsheet-native by design and isn't a sync-script
   candidate.

5. Open items — need a live Synapse check before implementation, not guessed here

1. **ResearchProject's standalone endpoint path** — docs/governance-graph-sync.md
   left this "undocumented in this pass"; the `researchProjectSnapshot` embedded in
   `POST /accessRequirement/{id}/submissions` may be sufficient on its own, or a
   direct `GET` may be needed for research projects not tied to a specific
   submission response.
2. **DataAccessRequest's rest-docs.synapse.org page 403'd** during the original
   review; sourcing there was verified against the OpenAPI spec only. Worth a live
   spot-check against a real request id before building the sync script.
3. **`sourceAclId`/`sourceAclResourceAccessId`** (on `AccessGrant`) — these slots'
   grounding traces to Synapse's internal `ACL`/`ACL_RESOURCE_ACCESS` relational
   tables (the "sagebrain governance graph ACL_AR data" CSVs
   `governance_graph.yaml`'s own intro cites), not necessarily to anything the public
   REST API's `AccessControlList` DTO exposes as a row-level id — Synapse's ACL
   object may not carry a per-`resourceAccess`-entry numeric id at all. This needs a
   live check against a real `GET /entity/{id}/acl` response before deciding whether
   these two fields are pullable, must stay blank from a REST-only sync, or need an
   alternate source. Do not assume either answer without checking.
4. **Sync scope** — one entity, an entity subtree (`GET /entity/{id}/children`
   walked recursively), or every entity governed by a given AccessRequirement
   (working backward from `subjectIds` on `GET /accessRequirement/{id}`)? Determines
   whether the pull order in Section 1 runs once per manually-supplied id or is
   driven by a broader enumeration query. Not decided by anything currently in the
   repo.
5. Everything already listed as unresolved in docs/governance-graph-sync.md's own
   "Open design questions" (sync script location, cadence, auth, and whether
   Policy-Fabric generation should block on an incomplete parsed record) still
   applies here and isn't re-litigated by this plan.
