Align the governance graph pipeline with sagebrain-infra PR #54's ReBAC concept

Context

sagebrain-infra PR #54 ("Add governance ReBAC concept API and AVP artifacts," open,
authored by thomasyu888, explicitly a "concept"/PoC) stands up a Neptune-backed
`/authorize` Lambda (`src/lambda_rebac/authorize.py`) that runs a SPARQL query
against a governance graph and combines the result with an Amazon Verified
Permissions (Cedar) policy decision. That Neptune graph is meant to be populated by
*this* repo's `scripts/build_governance_graph.py` — i.e. governanceDUO's export is
supposed to be a functional input to sagebrain-infra's authorizer, not just a
documentation artifact.

A review comment on that PR (thomasyu888, docs/governance_rebac_concept.md line 38,
https://github.com/Sage-Bionetworks-IT/sagebrain-infra/pull/54#discussion_r3926030399)
replaces the PR's own doc example (a Synapse-ACL-style snippet: `gov:AccessGrant`,
`gov:bindingType`, `gov:permission`, `gov:hasACL`, `gov:hasAccessRequirement`) with a
richer turtle example built from `gov:AccessRequirementTemplate`, `gov:Condition`,
`gov:IRBRequirement`, `gov:Program`, `gov:Site`, `gov:Principal`, `gov:Approval`,
`gov:Resource`, plus a `gx:` genomics domain extension — predicates
`gov:hasCondition`/`gov:conditionType`/`gov:duoCode`/`gov:extendsTemplate`/
`gov:scopedToProgram`/`gov:scopedToSite`/`gov:requiresAR`/`gov:participatesIn`/
`gov:affiliatedWith`/`gov:satisfies`/`gov:heldBy`/`gov:status`/`gov:expiresAt`.

Grounding: what was verified directly (not assumed) in PR #54 and this repo

- `authorize.py`'s real SPARQL query (`_governance_query()`, line 61) is:
  ```sparql
  PREFIX gov: <https://sagebionetworks.org/governance/>
  SELECT ?grant ?grantPrincipal ?permission ?bindingType ?accessRequirement
  WHERE {
    VALUES ?resource { <resource_iri> }
    OPTIONAL { ?resource gov:hasAccessRequirement ?accessRequirement . }
    OPTIONAL {
      ?resource gov:hasACL ?grant .
      ?grant a gov:AccessGrant ;
             gov:principal ?grantPrincipal ;
             gov:permission ?permission ;
             gov:bindingType ?bindingType .
    }
  }
  ```
  This hardcodes the **old ACL-style vocabulary**, not thomasyu888's target ontology.
  `_resource_iri()` also hardcodes the `https://www.synapse.org/Synapse:` prefix.
  Nothing in PR #54's code (authorize.py, neptune_rebac_concept_stack.py, the AVP
  schema/Cedar policy, or the tests) reads or expects
  `AccessRequirementTemplate`/`Condition`/`IRBRequirement`/`Program`/`Site`/
  `duoCode`/`arType`/`studyId`/`extendsTemplate` — those exist only in the one doc
  comment. `arSatisfied` is computed from a client-supplied
  `approved_access_requirements` array in the request body, not from any Approval/
  Condition graph traversal — a gap Copilot flagged independently in the same PR
  (comment 3919758492: "the resolver accepts `approved_access_requirements` ... this
  input/semantics aren't described in the flow"). The `gx:` genomics triples appear
  nowhere else in the PR; they illustrate that a domain ontology can
  `rdfs:subClassOf gov:Resource`, not a concrete requirement.
- **governanceDUO's current export already satisfies the PR's real, literal SPARQL
  contract.** `scripts/build_governance_graph.py` was written against the same
  "SageBrain Governance Graph Design" doc the PR's *original* example mirrored — its
  own module docstring says so — and `governance_graph_export/governance_graph.ttl`
  emits exactly `gov:hasACL`/`gov:AccessGrant`/`gov:principal`/`gov:permission`/
  `gov:bindingType`/`gov:hasAccessRequirement` under `syn:<https://www.synapse.org/Synapse:>`,
  using the *same example IDs* (`gov:grant-001`, `syn:syn10081783`) as the doc. This is
  not a coincidence to fix; it's confirmation the two were built from the same source.
- **The real gap is conceptual, not functional-today**: `linkml/access_requirement.yaml`
  + `mixins.yaml`'s `GovernanceMixin` already models DUO conditions
  (`dataUseModifiers` + companion slots like `geographicalRestriction`,
  `diseaseSpecificResearch`) — and `linkml/examples/access_requirement.example.yaml`
  already has real values (`dataUseModifiers: [DUO:0000007]`,
  `diseaseSpecificResearch: [MONDO:0004975]`) — but
  `build_governance_graph.py`'s `EXAMPLE_CLASSES` manifest never loads that example
  file at all. Every `gov:AccessRequirement` node the script emits today is a bare stub
  (`gov:AR-42 a gov:AccessRequirement ; owl:sameAs governanceduo:access_requirement.42`,
  per `add_access_requirement_association()`), carrying **no DUO conditions as graph
  edges whatsoever**. thomasyu888's target ontology models exactly this as first-class
  `gov:Condition` nodes (`gov:hasCondition`/`gov:conditionType`/`gov:duoCode`) — i.e. the
  richer example is pointing at a real, already-partially-built piece of this repo that
  the graph-export script simply doesn't surface yet.
- `docs/governance-graph-sync.md` (this repo's own design doc, "nothing here is
  implemented yet") already independently identified this same gap from the opposite
  direction — "The critical finding: DUO conditions are not on Synapse's
  `AccessRequirement` object" — and already designs a `duo_shorthand` reverse-lookup
  (`DataUseModifierEnum.annotations.duo_shorthand`) for recovering them. That
  machinery is the natural source for populating `gov:Condition.duoCode`.
- `gov:Approval`/`heldBy`/`satisfies`/`status`/`expiresAt`: this repo's
  `DataAccessSubmission`/`DataAccessSubmissionStatus` classes plus
  `add_data_access_submission()`'s existing `gov:hasApproval` edge
  (Principal → AR, emitted when `state == APPROVED`) already cover `heldBy`/
  `satisfies`/`status` conceptually as an edge, just not as its own node.
  **Correction to this plan's first draft**: `expiresAt` is *not* a genuine
  upstream data gap — verified directly against
  [rest-docs.synapse.org's `AccessApproval` object](https://rest-docs.synapse.org/rest/org/sagebionetworks/repo/model/AccessApproval.html),
  which is a *separate* Synapse object from `DATA_ACCESS_SUBMISSION_STATUS`
  (fetchable via `GET /accessApproval/{approvalId}`, and linked to a submission
  via `GET /dataAccessSubmission/{submissionId}/userAccessApproval`), and has a
  real `expiredOn` field, alongside `requirementId`/`accessorId`/`state` — i.e.
  exactly `gov:Approval`'s `satisfies`/`heldBy`/`status`/`expiresAt` shape, from a
  real Synapse source. This repo simply has no `AccessApproval` class at all yet
  (grepped clean across `linkml/`, `docs/`, `model/`, `scripts/`, `shapes/`,
  `plans/`). Modeling it properly (new class, new example instance — no existing
  committed data sources it) is bigger than an additive tweak to
  `DataAccessSubmissionStatus`, so it's tracked as its own item in
  `plans/governance_graph_open_questions.md` rather than folded into this plan.
- `gov:Program`/`gov:Site`/`gov:IRBRequirement`/`gov:extendsTemplate`/
  `gov:scopedToProgram`/`gov:scopedToSite`/`gov:participatesIn`/`gov:affiliatedWith`:
  grepped for `Program`/`Site`/`IRBRequirement`/`extendsTemplate`/
  `AccessRequirementTemplate` across `linkml/`, `model/`, `docs/` — **no match**.
  governanceDUO has no concept today of an AR *template* reused across
  programs/sites with per-site conditions layered on top (thomasyu888's
  `IRBRequirement extendsTemplate ar-genomics` pattern); every `AccessRequirement`
  here is one independent record scoped to its own `entityIdList`. This is the
  biggest, most speculative gap and the one this repo's own stated methodology (every
  class verified against a real Synapse/schematic source before modeling it) says
  should not be reverse-engineered from one illustrative example alone.

Target changes (additive; no existing slot/class renamed or removed; no change to
`authorize.py`'s current SPARQL contract, which stays satisfied throughout)

1. `linkml/governance_graph.yaml` — add a `Condition` class
   (`class_uri: sagegov:Condition`, slots `conditionType`, `duoCode`, `description`,
   `conditionDetail`) and a multivalued inlined `hasCondition` slot on
   `AccessRequirement` (declared in `access_requirement.yaml`, since that's where
   `AccessRequirement` itself lives).
   **Revised** (tagged `[CONFIRM]`; read `GovernanceMixin.rules:` directly rather
   than trust the original "companion slot" framing, which didn't survive
   inspection):
   - `duoCode` ranges over the *real* DUO CURIEs already in `DataUseModifierEnum`
     (`meaning:`-mapped ones only); `conditionType` is the `annotations.duo_shorthand`
     value for those 24 real codes (e.g. `"GRU"`, `"COL"`) and the bare enum key
     itself (e.g. `"DUOPlus1"`) for the 7 Sage-local extensions, which have no
     `duo_shorthand`/`meaning:` at all — verified directly (their only annotation is
     `sage_extension: true`) — mirroring `governance-graph-sync.md`'s own documented
     DUOPlus-extension boundary.
   - `description` — sourced from `DataUseModifierEnum.permissible_values[code]`'s
     own `description:` text (real, already-written prose for all 31 values, e.g.
     "General Research Use - This data use permission indicates..."), not invented.
   - `conditionDetail` (**renamed from the original singular `value`; multivalued**)
     — `GovernanceMixin.rules:` is genuinely many-to-many, not one companion slot
     per code: e.g. `DUO:0000026` alone has 4 postcondition slots
     (`userSpecificRestriction`/`approvedUsers`/`allowedAccountTypes`/
     `requiredProfileStatuses`), and `requiredAgreementDocumentId` is itself the
     postcondition for 4 *different* codes. A singular `value` slot can't represent
     this faithfully; `conditionDetail` holds zero-to-many literal values, one per
     matching rule's postcondition slot that's actually populated on the source
     instance. This is the same tension `governance-graph-sync.md` already flags as
     its own "Incomplete parsed records" open question (#3) — not a new problem,
     just given a concrete graph shape here.
2. `scripts/build_governance_graph.py` — add `"access_requirement"` to
   `EXAMPLE_CLASSES` (range `AccessRequirement`) and a new `add_access_requirement()`
   that, for the loaded example, mints one `gov:Condition` individual per
   `dataUseModifiers` entry on the existing `gov:AR-<n>` stub node.
   **Revised** (tagged `[CONFIRM]`; confirmed the mechanism, corrected the
   cardinality): read `_schemaview.get_class("GovernanceMixin").rules` at runtime
   (real LinkML `ClassRule` objects — confirmed this is genuinely structured,
   parseable data, not prose) — for each rule whose
   `preconditions.slot_conditions["dataUseModifiers"].equals_string` matches the
   Condition's DUO code, if the instance has a non-empty value for that rule's
   `postconditions.slot_conditions` key, emit it as one `gov:conditionDetail`
   triple. Iterate *all* matching rules per code (several codes match more than
   one, per point 1) rather than assuming exactly one. This still reads
   `GovernanceMixin.rules:` as the single source of truth rather than a second
   hardcoded DUO-code-to-slot map — same principle as the original draft, now
   implemented against the map's real (many-to-many) shape.
3. **Dropped from this plan** (tagged `[CONFIRM]`; did not survive verification).
   Minting a `gov:Approval` node now, sourced from `DataAccessSubmissionStatus`,
   would build the wrong thing: Synapse's real approval-expiration data
   (`expiredOn`) lives on a *separate* `AccessApproval` object this repo doesn't
   model at all (see the corrected Grounding bullet above), not on
   `DataAccessSubmissionStatus`. Minting a stub `gov:Approval` from the wrong
   source now would just need reworking once `AccessApproval` is modeled properly.
   The existing derived `gov:hasApproval` edge (Principal → AR, emitted on
   `state == APPROVED`) is left exactly as-is; a real `gov:Approval` class with a
   working `expiresAt` is tracked as its own item in
   `plans/governance_graph_open_questions.md` instead of being partially built
   here.
4. `docs/governance-graph-sync.md` — add a new open design question: does Sage's real
   governance model reuse one AR template across multiple programs/sites the way
   thomasyu888's `IRBRequirement`/`extendsTemplate` example shows? If yes, `Program`/
   `Site`/`AccessRequirementTemplate` classes would need real Synapse/schematic source
   verification (this repo's existing, stated bar for every class it models) before
   being added — flag as future work, don't add speculative classes now.
   **Confirmed** (tagged `[CONFIRM]`): verified directly against Synapse's own
   `AccessRequirement` REST object (rest-docs.synapse.org) that it has no
   template/inheritance/Program/Site-scoping field of any kind — `subjectIds` is its
   only compositional mechanism, and that scopes to individual entities, not
   organizational units. So this can only be a real concept if it's DCC-side/
   curated, not something derivable from Synapse's schema — also checked
   `access_requirement_JSON/README.md` for template/Program/Site language directly
   (no match). Resolution path tracked in `plans/governance_graph_open_questions.md`.
5. Leave the `gx:` genomics-domain pattern alone: `SynapseEntity`/`Resource` are
   already open for `rdfs:subClassOf` extension by any downstream ontology without any
   change here. **Confirmed** (tagged `[CONFIRM]`): neither class carries an
   `sh:closed`/disjoint SHACL constraint that would block this.
6. `shapes/governance_graph.owl.ttl` / `governance_graph.shacl.ttl` — add TBox/shape
   declarations for the new `Condition` class and its properties (not `Approval` —
   dropped per point 3), following the existing convention (see the file's own
   comments on `hasACL`/`hasAccessRequirement`/`hasApproval`). **Confirmed** (tagged
   `[CONFIRM]`): every existing `sh:NodeShape` in `governance_graph.shacl.ttl`
   targets exactly one class via `sh:targetClass` with no `sh:closed`, so a new
   `Condition` shape needs no changes to the existing five.

Execution task list — IMPLEMENTED (2026-09-03)

1. **Done.** Added `Condition` class (`conditionType`/`duoCode`/`description`/
   `conditionDetail`) to `governance_graph.yaml`. **Deviation from the plan's literal
   wording**: `hasCondition` was *not* added as a declared slot on `AccessRequirement`
   in `access_requirement.yaml` — that would require `access_requirement.yaml` to
   range over `Condition` (defined in `governance_graph.yaml`), which
   `governance_graph.yaml` already imports (not the other way around), creating an
   import cycle. Instead `gov:hasCondition` is a bare derived-convenience triple in
   the script, exactly matching the existing `gov:hasACL`/`gov:hasAccessRequirement`
   precedent (also undeclared in any LinkML `slots:` list) — same intent, a
   technically-required implementation adjustment. Documented inline in
   `governance_graph.yaml`, `build_governance_graph.py`, and `shapes/governance_graph.owl.ttl`.
2. **Done.** Added `--access-requirement-example` (default
   `linkml/examples/access_requirement.example.yaml`) and `add_access_requirement()`
   to `build_governance_graph.py` — reads `GovernanceMixin.rules` via `SchemaView` at
   runtime exactly as specified, iterating all matching rules per DUO code. Verified
   API shape directly against a real `SchemaView` before writing (`ClassRule.preconditions
   /postconditions.slot_conditions`).
3. **Done.** Added `gov:ConditionShape` to `shapes/governance_graph.shacl.ttl`, added
   `gov:Condition`/`gov:hasCondition`/`gov:conditionType`/`gov:duoCode`/
   `gov:description`/`gov:conditionDetail` to `shapes/governance_graph.owl.ttl`, and
   added `gov:hasCondition` to the existing `AccessRequirementShape`.
4. **Done.** Added open design question #5 (Program/Site/template reuse) and a
   `Condition` row to `docs/governance-graph-sync.md`. Cross-checked
   `docs/knowledge-graph.md`: its one mermaid diagram is pipeline-level (which script
   produces which file), not class-level, so no diagram change was needed; its
   "what's hand-written" bullet list and worked-example section were updated instead
   for consistency with the `hasACL`/`hasAccessRequirement` precedent.
5. **Done.** Regenerated `governance_graph_export/governance_graph.ttl` (50 triples,
   up from 44) and the downstream umbrella artifacts (`make owl`, `make shacl`,
   `make docs-examples`, `make docs`) so `docs/reference/classes/Condition.md` etc.
   exist and nothing is stale.

Note: this plan no longer includes posting a comment on PR #54's thread — that step
was explicitly reviewed out; see `plans/governance_graph_open_questions.md` for how
the Program/Site question and the `AccessApproval`/`expiresAt` gap actually get
resolved instead.

Verification — all passed (2026-09-03)

1. `make linkml-lint` — exit 0, 0 errors, only the pre-existing/expected
   `standard_naming` warnings (same category `conditionType`/`duoCode`/etc. also
   trigger, no regression).
2. `make shacl-validate` — `Conforms: True` on both `shapes/governance_duo.owl.ttl`
   and `linkml/examples/rdf/all_examples.ttl`.
3. `make governance-graph-validate` — `Conforms: True` against the new
   `ConditionShape`/OWL declarations.
4. Confirmed by direct grep of the regenerated `governance_graph.ttl`:
   `gov:hasACL`/`gov:AccessGrant`/`gov:principal`/`gov:permission`/`gov:bindingType`/
   `gov:hasAccessRequirement` triples are unchanged from before this work.
5. Ran the exact smoke query from this plan:
   `SELECT ?duo WHERE { gov:AR-42 gov:hasCondition ?c . ?c gov:duoCode ?duo }` →
   returned `DUO:0000007`, confirming the new `Condition` node is reachable from the
   existing `gov:AR-42` stub.
