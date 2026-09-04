Governance Graph ingestion: sourcing, sequencing, resolved design decisions, and
curator-table schemas

This plan supersedes and merges two prior documents, whose content now lives here in
full rather than split across two places: `docs/governance-graph-sync.md` (the
original per-class Synapse-sourcing design, deleted as part of this plan — see
Housekeeping at the end) and `plans/governance_graph_ingestion_sourcing.md` (pull
order + Synapse/spreadsheet/derived split, deleted and replaced by this file). Nothing
below is implemented yet.

Context

Every class in `governance_graph.yaml` was verified column-by-column against real
Synapse REST objects/tables specifically so a real sync could exist, but
`scripts/build_governance_graph.py` only ever runs against hand-authored examples
under `linkml/examples/governance_graph/` today — nothing in this repo actually calls
Synapse. This plan answers three things: (1) where each piece of data should come
from, prioritizing the Synapse REST API, (2) exactly which attributes have no live
Synapse source and must be curator-supplied instead, at the individual-attribute
level, and (3) concrete LinkML schema designs for the curator-facing tables that
residual data needs — the "I'd like to get to a point where we have schemas that
define these tables for curators" goal driving this consolidation.

Resolved design decisions

`docs/governance-graph-sync.md`'s five open design questions are now answered:

1. **Sync script location**: this repo (alongside `build_governance_graph.py`), not
   the external `mc2-center-dcc` repo.
2. **Sync cadence**: on-demand CLI run to start, against specific entities — not a
   scheduled batch job or webhook-driven trigger (those remain possible future work,
   not built now).
3. **Incomplete parsed records** (a record parsed purely from Synapse annotations
   missing a companion-condition slot `GovernanceMixin`'s `rules:` require): emit a
   **warning**, don't block. Policy Fabric generation proceeds against whatever data
   is available rather than halting the pipeline.
4. **Auth**: the invoking curator's own Synapse credentials (a `synapseclient`
   session under their identity), not a shared service account/PAT, for this first
   version.
5. **Program/Site/AR-template reuse** (multi-site consortium structure): already
   resolved directly by the user in an earlier session — no real Synapse or repo data
   source exists for this; it's curator-owned data, addressed by the curator-table
   schemas below, not a future Synapse feature to wait for.

Guiding principle

Pull from Synapse everywhere Synapse actually has the data — every class below with a
real REST/table source should never be hand-typed. Spreadsheets are for the residual:
data Synapse's schema has no field for at all (verified directly, not assumed, in
every case below), not a substitute for calling the API where it works.

1. Real data sources, per class (verified against rest-docs.synapse.org)

| Governance Graph class | Synapse REST source |
| --- | --- |
| `SynapseEntity` | `GET /entity/{id}` (structural fields); `GET /entity/{id}/annotations2` for DUO-related annotations |
| `AccessGrant` + `Principal` | `GET /entity/{id}/acl` → `AccessControlList.resourceAccess[]` (each entry: `principalId`, `accessType[]`) — one `AccessGrant` per `resourceAccess` entry, one `Principal` per distinct `principalId` |
| `AccessRequirementAssociation` | `GET /entity/{id}/accessRequirement` (Access Requirements bound to that entity); `bindingType` (Direct/Inherited) resolved by comparing the entity's own ACL/AR listing against `GET /entity/{id}/benefactor` |
| `DataAccessSubmission` + `DataAccessSubmissionStatus` | `POST /accessRequirement/{requirementId}/submissions` (list) + `GET /dataAccessSubmission/{submissionId}` |
| The `gov:AR-<n>` stub (`AccessRequirementReference`) / `owl:sameAs` target | `GET /accessRequirement/{requirementId}` itself |
| `Condition` | Not sourced from Synapse directly for every field — see Section 3 below for exactly how much of it is recoverable from annotations vs. curator-only |
| `AccessApproval` | `GET /accessApproval/{approvalId}`, or `GET /dataAccessSubmission/{submissionId}/userAccessApproval` from a known submission — a real, separate Synapse object from `DataAccessSubmission`/`DataAccessSubmissionStatus` |
| `ResearchProject` | Embedded directly in `POST /accessRequirement/{requirementId}/submissions`'s `researchProjectSnapshot`, or independently via the (undocumented in this pass) ResearchProject endpoints — open item #1 |
| `DataAccessRequest`/`DataAccessRenewal` | `GET /dataAccessRequest/{requestId}` (rest-docs.synapse.org's page for this object 403'd during review; verified via the OpenAPI spec instead — open item #2) |
| `Site` | Not a Synapse object at all — derived by slugifying `ResearchProject.institution`/`DataAccessRequest.institution`/`Principal`'s `UserProfile.company` (see `site_node_for()`) |
| `AccessRequirementTemplate`/`IRBRequirement`/`Program` | **No real Synapse or repo source exists.** Curator-table schemas below |

**Full entity-coverage audit** (every Synapse governance-domain REST object checked
against what this repo models, not just the ones above): see
`plans/governance_graph_open_questions.md` Section A. Reviewed-and-out-of-scope, not
gaps: `RestrictableObjectDescriptor` (already served by
`AccessRequirementAssociation.resource`/`entityIdList`), `VerificationSubmission`
(identity verification, a different domain), `AccessorGroup`/`AccessApprovalInfo`
(batch/report DTOs, not persisted entities), `EvaluationRound` (Synapse's
challenge/Evaluation-queue domain, not data-access governance).

2. Recommended pull order (dependency-ordered)

A sync run starts from one or more seed Synapse entity ids (a project, or an
individual file/folder) — scope selection itself is an open item, #4 in Section 6.

1. `GET /entity/{id}` → `SynapseEntity` structural fields.
2. `GET /entity/{id}/annotations2?includeDerived=true` → DUO-related annotations
   (feeds the `Condition` partial-parse in step 8).
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
   a. `GET /accessRequirement/{requirementId}` → the `AccessRequirementReference`
      stub's structural fields (the `owl:sameAs` target).
   b. `POST /accessRequirement/{requirementId}/submissions` → `DataAccessSubmission`
      list; per submission, `GET /dataAccessSubmission/{submissionId}` →
      `DataAccessSubmissionStatus`.
   c. Per submission: `GET /accessApproval/{approvalId}` or
      `GET /dataAccessSubmission/{submissionId}/userAccessApproval` → `AccessApproval`.
   d. `ResearchProject` — from the submissions response's `researchProjectSnapshot`
      where present, else the standalone endpoint (open item #1).
   e. `DataAccessRequest` — `GET /dataAccessRequest/{requestId}`, `requestId` taken
      from the `DataAccessSubmission` record fetched in (b).
8. Run `parse_duo_annotations()` (proposed below) against step 2's annotation
   payload, using `DataUseModifierEnum`'s `duo_shorthand` reverse-lookup (read from
   the schema at runtime, not hardcoded) → a partial `governanceduo:AccessRequirement`
   (`id`, `dataUseModifiers`, `entityIdList`) for each of the 24 real DUO terms that
   have a shorthand. Merge in the curator-supplied `AccessRequirementConditionSupplement`
   row for this AR (Section 4) for everything annotations can't carry — emit a
   warning (per resolved decision #3) for any `GovernanceMixin` rule still unsatisfied
   after the merge.
9. `Site` — not fetched at all; derive deterministically by slugifying the
   `institution`/`company` strings already collected in steps 6-7.

3. Fully Synapse-API-sourced (call these; never hand-type)

| Class | Slots | Endpoint(s) |
| --- | --- | --- |
| `SynapseEntity` | `name`, `nodeType`, `parentId`, `alias`, `currentRevNum`, `maxRevNum`, `etag`, `createdBy` (raw literal userId), `createdOn` | `GET /entity/{id}` |
| `Principal` | `principalId`, `principalType`, `company` (User only) | ACL `resourceAccess[].principalId`; `GET /userProfile/{id}` / `GET /team/{id}` |
| `AccessGrant` | `resource`, `principal`, `permission`, `bindingType`, `createdOn` | `GET /entity/{id}/acl`; `GET /entity/{id}/benefactor` for `bindingType` |
| `AccessRequirementAssociation` | `resource`, `accessRequirement`, `bindingType` | `GET /entity/{id}/accessRequirement`; `GET /entity/{id}/benefactor` |
| `AccessRequirementReference` stub | structural AR fields | `GET /accessRequirement/{requirementId}` |
| `DataAccessSubmission` | `accessRequirementId`, `accessRequirementVersion`, `requestId`, `researchProjectId`, `submittedBy`, `submittedOn`, `modifiedBy`, `etag` | `POST /accessRequirement/{id}/submissions`; `GET /dataAccessSubmission/{id}` |
| `DataAccessSubmissionStatus` | `submissionId`, `state`, `rejectedReason`, `modifiedOn` | same submission fetch |
| `AccessApproval` | `requirementId`, `requirementVersion`, `submitterId`, `accessorId`, `status`, `expiredOn`, `createdOn`, `sourceApprovalId`, `etag` | `GET /accessApproval/{id}` / `GET /dataAccessSubmission/{id}/userAccessApproval` — `AccessApproval.id` is a real top-level field on this object, unlike the ACL row ids in Section 6 |
| `ResearchProject` | `institution`, `projectLead`, `intendedDataUseStatement`, `createdBy`, `createdOn`, `etag` | submissions' `researchProjectSnapshot`, or standalone endpoint (open item #1) |
| `DataAccessRequest` | `institution`, `requestPrincipalInvestigatorName/Email`, `requestSigningOfficialName/Email`, `createdBy`, `createdOn`, `modifiedBy`, `modifiedOn`, `requestConcreteType`, `publication`, `summaryOfUse` | `GET /dataAccessRequest/{id}` (open item #2) |
| `Condition` (partial) | `id`, `dataUseModifiers`, `entityIdList` — 24 real DUO terms only | `GET /entity/{id}/annotations2?includeDerived=true`, via `duo_shorthand` reverse lookup |

Derived, not fetched or typed anywhere: `Site` (slugified from `institution`/`company`
strings already pulled above — Synapse gives no stable Site id at all);
`gov:affiliatedWith`/`gov:hasACL`/`gov:hasAccessRequirement`/`gov:hasApproval`
(convenience/join triples computed from data already pulled, never independently
sourced — `gov:hasCondition` is the one exception, now a real
`AccessRequirementReference` slot, see `plans/access_requirement_reference_class.md`);
`source` on `AccessGrant`/`AccessRequirementAssociation` (always the literal
`"Synapse"`, hardcoded by the ingestion script, not looked up).

4. What belongs in a spreadsheet — attribute-level, with why each one can't be pulled
   live

**4a. DUO conditions are not on Synapse's `AccessRequirement` object at all.**
Confirmed directly against rest-docs.synapse.org: Synapse's native
`AccessRequirement` interface has no data-use-condition fields — `id`,
`concreteType`, `accessType`, `subjectIds`, `subjectsDefinedByAnnotations`, plus audit
fields, nothing else. `dataUseModifiers` and its companion slots are Sage's own
extension, implemented as **entity annotations**
(`GET /entity/{id}/annotations2?includeDerived=true`), populated today by a
curator-authored CSV → `generate_duo_schema.py` (now archived, at
`archive/scripts/generate_duo_schema.py` — see Housekeeping note below) → a
conditional JSON schema bound with `derivedAnnotations = TRUE`.

**4b. What's recoverable from those annotations, and what genuinely isn't.** The
archived Data Dictionary CSV format (`archive/access_requirement_JSON/README.md`)
stores `dataUseModifiers` as DUO **shorthand** codes (`IRB`, `NPU`, `HMB`, ...) — the
exact shorthand `mixins.yaml`'s `DataUseModifierEnum` already tags onto every one of
its 24 real DUO permissible values via `annotations.duo_shorthand` (e.g. `IRB` →
`duo_shorthand: "IRB"` → `meaning: DUO:0000021`). Combined with two mechanical
transforms already used elsewhere in this repo (`accessRequirementId` needs only the
`access_requirement.` id-prefix; `entityIdList` needs no transform, since both sides
already share the `^syn\d+$` pattern), a real, partial `governanceduo:AccessRequirement`
instance (`id`, `dataUseModifiers`, `entityIdList`) genuinely can be parsed straight
out of that annotation response — no curator input needed for these three fields, for
the 24 real DUO terms.

**Where it stops being complete, for two concrete reasons:**

1. Only the 24 real DUO terms have a `duo_shorthand`. The 7 Sage-local
   `DUOPlus1`–`DUOPlus7` extensions don't — they aren't part of the external DUO
   vocabulary Synapse's shorthand convention covers — so any AccessRequirement whose
   real `dataUseModifiers` includes a DUOPlus code needs that value
   spreadsheet-sourced; the annotation-parsing path can structurally never recover it,
   no matter how complete Synapse's own data is.
2. `GovernanceMixin`'s own conditional `rules:` require companion slots for many DUO
   codes that the Data Dictionary CSV has no column for at all, and — this is a
   correction from the prior version of this plan, checked directly this session, not
   assumed — **neither does any other curator artifact that currently exists**:
   `model/AccessRequirement.model.csv` (the live `schematic manifest` template) has
   exactly five columns (`AccessRequirement`, `AccessRequirement_id`,
   `contributorName`, `contributionDate`, `entityIdList`) and the archived Data
   Dictionary CSV's only DUO-related columns are `dataUseModifiers`,
   `accessRequirementId`, `entityIdList`, plus a few unrelated configurable
   annotation columns (`grantNumber`, `studyKey`, `dataType`, `speciesType`). **None
   of the 24 companion slots below have ever had a curator-facing home in this repo.**
   This is a real, currently-unfilled gap, not a hypothetical one — Section 5 proposes
   closing it with a new table.

   The 24 companion slots, and the DUO code(s) each is a postcondition for
   (`GovernanceMixin.rules` in `linkml/mixins.yaml`, 35 rules total —
   `requiredAgreementDocumentId`/`allowedPurposes`/`prohibitedPurposes` are each
   required by more than one code):

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

**4c. `AccessRequirementTemplate`/`Program`/`IRBRequirement`'s organizational
fields.** Zero Synapse source exists for AR-template reuse or multi-site Program
grouping at all — verified directly that Synapse's `AccessRequirement` has only
`subjectIds` as a compositional mechanism, nothing above the individual-entity level.
This isn't a gap a future Synapse feature closes on its own; it's organizational data
Synapse's object model doesn't represent. Per-attribute breakdown (excluding anything
derived or reused from elsewhere, which needs no curator entry):

- **`Program`**: `id`, `name`. That's the entire curator-facing surface — no other
  slots exist on this class.
- **`AccessRequirementTemplate`**: `id`, `domain` only. `hasCondition` is *not*
  curator-typed here — `add_access_requirement_template()` reuses the real `Condition`
  nodes `add_access_requirement()` already minted from a real AccessRequirement's
  `dataUseModifiers` (confirmed by reading the function directly), so a template's
  conditions come from an existing AR record, not fresh curator input. If a future
  template needs conditions with no backing real AR, that reuse mechanism would need
  to change — out of scope here.
- **`IRBRequirement`**: `id`, `extendsTemplate` (FK to `AccessRequirementTemplate`),
  `arType`, `studyId` (FK to the existing, real `Study` class — already curator-owned
  via the schematic/CSV pipeline, see 4d), `language`, `scopedToProgram` (FK to
  `Program`), `institution` (plain string). `scopedToSite` needs **no** direct
  curator entry: per this class's own description, `institution` already drives it
  the same way it drives `gov:affiliatedWith` elsewhere — populating both from one
  field would be redundant re-entry, not two independent facts.

**4d. `Study`.** Already sourced from the DCC's schematic/CSV Data Dictionary
pipeline (`Makefile`'s `build-csv`/`collate`/`convert` targets over
`model/Study.model.csv`), not from Synapse REST calls at all. No new work — flagged
only so it's clear this class is already spreadsheet-native by design.

5. Proposed curator-table schemas

Two different mechanisms, matched to what each table actually is:

**5a. `Program`/`AccessRequirementTemplate`/`IRBRequirement` — reuse the existing
classes, don't duplicate them.** These are already real LinkML classes in
`governance_graph.yaml` with the right slots; the only thing missing is
`tree_root: true`, which is what makes a class a top-level curator-manifest target
(the same flag `Study`/`AccessRequirement`/`Resource`/`Schema` already carry).
Defining a second, parallel schema for the same three classes would recreate exactly
the two-sources-of-truth risk this session has spent most of its effort eliminating
elsewhere in this schema. Proposed:

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
```

**5b. A new `AccessRequirementConditionSupplement` class — genuinely new, because
nothing curator-facing covers this today (Section 4b).** Proposed for
`linkml/access_requirement.yaml` (sibling to the real `AccessRequirement` class it
supplements, not `governance_graph.yaml` — this data belongs to the DUO-core model,
not the graph-export layer, matching how `Condition` individuals are already
described as surfacing "already-real DUO-core data," not new data invented at the
graph layer):

```yaml
# linkml/access_requirement.yaml
  AccessRequirementConditionSupplement:
    is_a: BaseEntity
    tree_root: true
    description: >-
      Curator-supplied companion values for one real AccessRequirement's
      dataUseModifiers -- covers exactly the data GovernanceMixin's conditional
      rules: require but Synapse's own entity annotations can never carry (companion
      condition slots for every DUO code that has one, and any DUOPlus1-7 codes,
      which have no duo_shorthand and so can't be recovered from annotations at
      all -- see plans/governance_graph_ingestion.md Section 4b for the full,
      checked-not-assumed grounding). One row per real AccessRequirement that needs
      any of this; ARs whose dataUseModifiers have no companion requirement at all
      need no row.
    slot_usage:
      id:
        description: >-
          A synthetic identifier for this supplement record.
        pattern: '^access_requirement_condition_supplement\.[A-Za-z0-9_-]+$'
    slots:
      - accessRequirementId       # FK, reuses the existing slot -- see below
      - dataUseModifiers          # curator-known DUOPlus codes only; real DUO
                                   # codes are already recoverable from annotations
                                   # and listing them again here is harmless but
                                   # redundant, not required
      - diseaseSpecificResearch
      - researchSpecificRestrictions
      - collaborationRequired
      - geographicalRestriction
      - publicationMoratorium
      - timeLimitOnUse
      - userSpecificRestriction
      - institutionSpecificRestriction
      - sourceGeography
      - populationType
      - deidentificationType
      - dataPermission
      - dataTier
      - license
      - attribution
      - requiredAgreementDocumentId
      - notAfter
      - allowedPurposes
      - prohibitedPurposes
      - nonprofitLegalForms
      - approvedProjects
      - approvedUsers
      - allowedAccountTypes
      - requiredProfileStatuses
```

Every slot listed is already declared once, on `GovernanceMixin`
(`linkml/mixins.yaml`) — this class reuses them by name rather than redeclaring
types/descriptions a second time, so a merge at sync time is a plain "copy matching
keys onto the real AccessRequirement record" operation with no field-name mapping
logic to maintain. `accessRequirementId` needs a `range`/description check against
how it's already used elsewhere in this schema (it's presently declared inside
`governance_graph.yaml`, ranging over `AccessRequirementReference` — this new use, a
plain FK to the real `AccessRequirement`'s dotted id, is a different thing with the
same name; resolving that naming collision, or minting a distinctly-named FK slot
instead, is left as an implementation detail, not decided here).

Not proposed: expanding `model/AccessRequirement.model.csv` itself, or reviving the
archived Data Dictionary CSV format, to carry these columns instead of a new table.
That CSV feeds the separate, already-existing Synapse-annotation/JSON-schema
pipeline (`use-cases.md`'s documented flow) — folding governance-graph-only curator
input into it would couple two pipelines that don't otherwise need to be coupled, and
risks affecting consumers of that CSV this plan hasn't audited. **Open question, not
resolved here:** should it be folded in anyway, once someone who owns that pipeline
weighs in? Left for a follow-up, not decided unilaterally by this plan.

6. Open items — need a live Synapse check before implementation, not guessed here

1. **ResearchProject's standalone endpoint path** — left "undocumented in this pass";
   the `researchProjectSnapshot` embedded in `POST /accessRequirement/{id}/submissions`
   may be sufficient on its own, or a direct `GET` may be needed for research
   projects not tied to a specific submission response.
2. **DataAccessRequest's rest-docs.synapse.org page 403'd** during the original
   review; sourcing there was verified against the OpenAPI spec only. Worth a live
   spot-check against a real request id before building the sync script.
3. **`sourceAclId`/`sourceAclResourceAccessId`** (on `AccessGrant`) — these slots'
   grounding traces to Synapse's internal `ACL`/`ACL_RESOURCE_ACCESS` relational
   tables (the "sagebrain governance graph ACL_AR data" CSVs
   `governance_graph.yaml`'s own intro cites), not necessarily to anything the public
   REST API's `AccessControlList` DTO exposes as a row-level id. Needs a live check
   against a real `GET /entity/{id}/acl` response before deciding whether these two
   fields are pullable, must stay blank from a REST-only sync, or need an alternate
   source.
4. **Sync scope** — one entity, an entity subtree (`GET /entity/{id}/children`
   walked recursively), or every entity governed by a given AccessRequirement
   (working backward from `subjectIds` on `GET /accessRequirement/{id}`)? Not decided
   by anything currently in the repo.

Housekeeping (as part of this consolidation, not a separate future step)

- `docs/governance-graph-sync.md` deleted — its content is fully absorbed above.
  `docs/index.md`'s table row and `docs/use-cases.md`'s cross-reference for it
  updated to link to this plan's GitHub blob URL instead (this repo's own convention
  for narrative pages linking outside `docs_dir`, per `Makefile`'s `docs-build`
  comment).
- `plans/governance_graph_ingestion_sourcing.md` deleted — fully superseded by this
  file.
- `archive/scripts/generate_duo_schema.py`/`archive/access_requirement_JSON/`
  referenced above by their new archived paths, not as if still live at their
  original locations.
