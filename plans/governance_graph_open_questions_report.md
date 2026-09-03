# Report: Resolve open governance-graph design questions

## Summary

Implemented all of `plans/governance_graph_open_questions.md`'s execution list:
`AccessApproval`, `ResearchProject`, `Site`, `DataAccessRequest`, and the
`AccessRequirementTemplate`/`IRBRequirement`/`Program` target-ontology direction are
now real classes in `governance_graph.yaml`, wired end-to-end through
`build_governance_graph.py`, `shapes/governance_graph.{shacl,owl}.ttl`, and
`docs/governance-graph-sync.md`. `authorize.py`'s live SPARQL contract is unaffected
throughout (verified by direct grep of the regenerated graph).

## Schema changes (`linkml/governance_graph.yaml`)

- New `ApprovalStateEnum` (`APPROVED`/`REVOKED`) — verified directly against the
  OpenAPI spec as a *distinct* enum from `SubmissionStateEnum`, not a reuse.
- New `AccessApproval` class (`is_a: BaseEntity`): `requirementId`
  (`slot_uri: sagegov:satisfies`), `requirementVersion`, `submitterId`
  (`slot_uri: sagegov:submittedBy`, reused), `accessorId`
  (`slot_uri: sagegov:heldBy`), `status` (new slot, range `ApprovalStateEnum` —
  deliberately not the shared `state` slot, which ranges over the unrelated
  `SubmissionStateEnum`), `expiredOn` (`slot_uri: sagegov:expiresAt`), `createdOn`,
  `sourceApprovalId`, `etag`.
- New `ResearchProject` class (`is_a: BaseEntity`): `accessRequirementId`,
  `institution`, `projectLead`, `intendedDataUseStatement`, `createdBy` (revived
  `sagegov:createdBy` predicate — freed up by the earlier `DataAccessSubmission`
  field-name fix, now used for the "who authored this record" concept, distinct
  from `sagegov:submittedBy`'s "workflow action" concept), `createdOn`, `etag`.
- New `Site` class (not `is_a: BaseEntity` — no stable Synapse id exists, only a
  free-text institution/company name): `institution`, `participatesIn`
  (illustrative-only, → `Program`).
- `Principal`: new `company` slot (`slot_uri: sagegov:company`), mirroring
  Synapse's real `UserProfile.company` field — only meaningful for
  `principalType: User`.
- New `DataAccessRequest` class (`is_a: BaseEntity`): uses its own real field names
  (`createdBy`/`createdOn`/`modifiedBy`/`modifiedOn`, reusing `createdBy` and the
  existing `modifiedBy`/`modifiedOn` slots — **not** `submittedBy`/`submittedOn`,
  confirmed against the spec as a different real object with different field
  names than `Submission`), `accessRequirementId`, `researchProjectId`,
  `institution`, four flattened `requestPrincipalInvestigator*`/
  `requestSigningOfficial*` slots (the live API's nested sub-objects have no
  independent identifier, so flattened rather than given nested classes),
  `requestConcreteType` (a *new*, distinct slot — reusing the existing
  `concreteType` slot would have been wrong: it already has an incompatible
  range, `AccessRequirementConcreteTypeEnum`, for a different real object),
  `publication`/`summaryOfUse` (renewal-only).
- New `AccessRequirementTemplate`, `IRBRequirement`, `Program` classes (all
  `is_a: BaseEntity`) plus `domain`, `hasCondition` (range `Condition` — reusing
  the alignment plan's class directly), `extendsTemplate`, `arType`, `studyId`
  (bridges to the real `governanceduo:Study` via `owl:sameAs`, not its own
  `slot_uri`), `language`, `scopedToProgram`, `scopedToSite`, `participatesIn`.
  `Program`/the `Program`-`Site` pairing are explicitly documented as
  illustrative-only in both the schema docstrings and `docs/governance-graph-sync.md`.
- `DataAccessSubmission.requestId`/`researchProjectId`: range changed from
  `integer` to `DataAccessRequest`/`ResearchProject` respectively, now that those
  are real classes — emitted as IRI references instead of literals.
- Fixed a missing `slot_uri` on `modifiedOn` (previously resolved to the wrong
  `governanceduo:` default prefix if ever looked up via `PREDICATE()`) while
  wiring `DataAccessRequest` to reuse it.

## Script changes (`scripts/build_governance_graph.py`)

- New `site_node_for()` helper: slugifies an institution/company string into a
  deterministic `gov:site-<slug>` node, shared across all three real sources
  (`ResearchProject.institution`, `DataAccessRequest.institution`,
  `Principal.company`).
- `add_access_requirement()` now returns the list of `Condition` nodes it mints,
  so `add_access_requirement_template()` can reuse the *exact same* nodes rather
  than re-deriving or duplicating them — verified via query that
  `gov:AR-42-condition-DUO-0000007` is reachable from both `gov:AR-42` and the
  illustrative template.
- `add_principal()`: emits `gov:affiliatedWith` to the shared `Site` node when
  `company` is present (User-type Principals only).
- New `add_access_approval()`, `add_research_project()`, `add_data_access_request()`,
  `add_access_requirement_template()`, `add_program()`, `add_irb_requirement()`.
- `add_data_access_submission()`: now emits `requestId`/`researchProjectId` as
  real IRI edges (previously declared in the schema but never actually emitted
  at all).
- `main()`: wired in the correct dependency order (Principals → AR stub/Condition
  → ResearchProject → DataAccessRequest → AccessApproval → Program →
  AccessRequirementTemplate → IRBRequirement → DataAccessSubmission/Status).

## Example instances

New: `access_approval.example.yaml`, `research_project.example.yaml`,
`data_access_request.example.yaml`, `program.example.yaml` (illustrative, header
comment says so), `access_requirement_template.example.yaml` (illustrative),
`irb_requirement.example.yaml` (illustrative). Updated:
`principal_user_2000001.example.yaml` (added `company: Mount Sinai`),
`data_access_submission.example.yaml` (`requestId`/`researchProjectId` changed
from bare integers to the real dotted-id strings). All institution values
deliberately set to `"Mount Sinai"` across `ResearchProject`, `DataAccessRequest`,
`Principal.company`, and `IRBRequirement.institution` specifically to exercise
real `Site`-node convergence, not just individually-valid data.

## Shapes (`shapes/governance_graph.{shacl,owl}.ttl`)

New `NodeShape`s/class-and-property declarations for all six new classes;
extended `PrincipalShape` (`affiliatedWith`) and `DataAccessSubmissionShape`
(`requestId`/`researchProjectId`, now IRI-typed). Fixed the `gov:name` OWL
declaration's `rdfs:domain` (was `SynapseEntity`-only; now also used by `Program`).

## Docs

`docs/governance-graph-sync.md`: full entity-coverage table extended with
`AccessApproval`/`ResearchProject`/`DataAccessRequest`/`Site`/
`AccessRequirementTemplate`/`IRBRequirement`/`Program` rows plus the
reviewed-and-out-of-scope objects; open design question #5 marked
resolved-in-direction (with what's still honestly illustrative-only). Regenerated
`docs/reference/*` and `shapes/governance_duo.{owl,shacl}.ttl` via `make docs`/
`make owl`/`make shacl` — no hand-editing of generated files.

## Tests / verification

1. `make linkml-lint` — exit 0, only pre-existing `standard_naming` warnings.
2. `make shacl-validate` and `make governance-graph-validate` — both
   `Conforms: True`.
3. Query-verified (not just asserted): `principal-2000001`,
   `research-project-8001`, and `data-access-request-7001` all resolve
   `gov:affiliatedWith` to the identical `gov:site-mount-sinai` node — four
   independent real/illustrative sources genuinely converging in the graph, not
   four disconnected stubs.
4. Query-verified: the same `gov:AR-42-condition-DUO-0000007` node is reachable
   from both `gov:AR-42` and `gov:access-requirement-template-ar-genomics` via
   `gov:hasCondition` — confirmed by a single join query, not two separate
   lookups that happened to match.
5. Query-verified: `gov:irb-requirement-irb-genomics-adkp owl:sameAs
   governanceduo:study.mc2-jax-5xfad` resolves to the real `Study` individual.
6. Grepped the regenerated graph directly: `gov:hasACL`/`gov:AccessGrant`/
   `gov:principal`/`gov:permission`/`gov:bindingType`/`gov:hasAccessRequirement`
   triples are byte-for-byte unchanged — `authorize.py`'s live SPARQL contract is
   unaffected.

Triple count: `governance_graph_export/governance_graph.ttl` went from 50 to 100
triples.

## Left honestly unresolved (by design, not oversight)

- `Program` and the `Program`/`Site` pairing on `IRBRequirement`: no real Synapse
  or repo data source exists — shipped as structural capability with one
  clearly-illustrative example only, exactly as planned.
- Section D's 4 sync-cadence questions in `docs/governance-graph-sync.md`: left
  as documented, unresolved decisions (tagged `[Skip for now]` in the plan).
- Section E (`institutionDids`/ROR gap): required a *correction*, not new work —
  `plans/policy_fabric_alignment.md` was already fully implemented in this repo
  before this session; see the plan's own corrected Section E text.
