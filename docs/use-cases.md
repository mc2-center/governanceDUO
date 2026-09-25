# Use cases and data sources

This page answers two questions this repo's other docs assume you already know:
**what is each part of this model for**, and **where does its data actually come
from**. The governing goal for the second question: every fact on the governance
graph should be populated by a script talking to Synapse's own API, not typed by
hand. Today there is exactly one exception to that — DUO conditions — and it's a
gap being closed, not a permanent design: ACT annotates the Access Requirement
itself, as a row in a Curator Record Set bound to this repo's own generated JSON
Schema (`scripts/provision_curator_infrastructure.py`, `scripts/build_json_schemas.py`),
not a separately maintained local file. That Record Set mechanism is implemented
and live-piloted (`plans/synapse_curation_infrastructure.md`); what's still
missing is the read side — a sync script that pulls a specific AR's row back out
(`plans/ar_level_duo_annotations.md`).

## What each part is for

### DUO-core model — gating access to Synapse data by DUO condition

DUO ("Data Use Ontology") tags let Sage Bionetworks programs semantically describe
*how* a dataset may be used, then have Synapse automatically gate access to that
data based on those tags. The **Access Requirement (AR)** is the authoritative
source for this: ACT annotates the AR directly with its DUO conditions, and every
entity the AR governs inherits the annotation the same way it inherits the AR
itself — not a per-entity annotation, and not derived from annotations on entities
beneath it (`plans/ar_level_duo_annotations.md`). ARs come in two flavors: a
**clickwrap** (the user just agrees to terms) or a **managed AR**, which can demand
evidence of Authentication (training certification, profile validation,
two-factor auth) and/or Authorization (an intended-data-use statement, a data use
certificate, an IRB/IEC ethics approval letter). `Study`/`Resource`/`Schema` give
an AR the context it needs — which grant/data source it belongs to, which Synapse
containers it governs, which registered JSON schema encodes it.

### Governance Graph — a queryable model of *effective* access

The graph layer's use case is different from the DUO-core model's: it's not about
authoring conditions, it's about **representing the resulting state** — who
actually has what permission on a resource (a W3C Web Access Control
`Authorization`) versus what additional conditions must separately be satisfied (an
`AccessRequirement`, attached directly to the entity it governs and inherited by
walking the container hierarchy, satisfied-or-not via a recorded `Approval`) — as
one RDF graph capable of answering "does this specific user have effective access to
this specific resource right now?" (ACL permits **AND** applicable ARs are
satisfied). See [Governance graph design](graph-design.md) for the model itself, and
[Knowledge graph representation](knowledge-graph.md) for the RDF shape.

### Policy Fabric integration — making DUO conditions programmatically enforceable

The DUO-core model captures conditions as metadata; it doesn't enforce anything by
itself. `policy_fabric.yaml`/`policy_fabric_bindings.yaml`'s use case is to translate
an `AccessRequirement`'s DUO-coded conditions into the literal input shape a real,
external decentralized-governance system —
[Policy Fabric](https://github.com/hasan7n/tmp-policies) — needs to actually evaluate
and gate access at request time, via Verifiable Credentials and Rego policy
evaluation. See [Policy Fabric integration](policy-fabric.md).

### DRS interoperability — a forward-looking design, not a running feature

[`docs/drs-interop.md`](drs-interop.md) maps this model onto the GA4GH Data
Repository Service API's object/authorization semantics, so that a future DRS-facing
integration wouldn't have to invent that mapping from scratch. It is explicitly a
**design document only** — this repo does not expose a DRS API today.

## Data sources

The target for every row below is Synapse's own REST API, or a computation over
data that itself came from that API — never a hand-typed file. Two rows aren't
there yet, and both are named explicitly rather than left implicit.

| Component | Target source | Populated how, today |
| --- | --- | --- |
| DUO conditions (`Condition`/`dataUseModifiers`) | The AR itself, annotated by ACT as a Curator Record Set row, bound to `json_schemas/AccessRequirement.json` | **Provisioned, sync pending.** The Record Set/schema mechanism is implemented and live-piloted (`plans/synapse_curation_infrastructure.md`); `scripts/sync_governance_graph.py` still merges in the older local curator-file record until the Record Set read side (`fetch_ar_record_set_row()`) is written — see `plans/ar_level_duo_annotations.md` |
| Governance Graph (`SynapseEntity`/`Authorization`/`User`/`Team`/`AccessRequirement`/`Approval`/`DataAccessSubmission`) | Synapse's REST API — `GET /entity/{id}/path`, `.../acl`, `.../accessRequirement`, `POST /accessRequirement/{id}/submissions`, `POST /accessApproval/search` | `scripts/sync_governance_graph.py` — implemented, tested offline; not yet run against live Synapse credentials |
| Provenance layer (`prov:Activity`/`prov:Usage`) | Synapse's provenance API, `GET /entity/{id}/generatedBy` | `scripts/sync_provenance_graph.py` — same status as above |
| Derivation policy layer (`ControlLabel`/`DerivationReview`) | Computed from the governance and provenance layers above, plus AR data tiers | `scripts/build_derivation_policy.py` — fully computed, no separate source of its own |
| Policy Fabric crosswalk table (`policy_fabric_bindings.yaml`) | Not a graph-population concern — a static, hand-verified lookup table (21 rows, one per Policy Fabric `policy_card`), checked directly against `hasan7n/tmp-policies`'s own files | Reference data, checked in once and updated only if Policy Fabric's own `policy_cards/` change |
| Policy Fabric per-record input (`scripts/build_policy_fabric.py`'s argument) | A single `AccessRequirement`'s `dataUseModifiers` and companion slots | Whichever `AccessRequirement` a maintainer points the script at |
| DRS alignment (`drs_alignment.yaml`) | N/A — design-only | No populated instances; one hand-written illustrative example in `docs/drs-interop.md` |

`plans/governance_graph_ingestion.md` has the full source-endpoint design (which
endpoint, in what order, under which credential) for every Governance Graph and
provenance field; the table above is the summary.

## Operational status

- **Governance Graph and provenance sync**: implemented, tested offline against
  fake Synapse clients, not yet run against real Synapse credentials — no
  live-populated export exists today, only the illustrative canonical example
  (`make governance-graph`).
- **DUO conditions**: the Curator Record Set mechanism is implemented and
  live-piloted; the one remaining gap against the API-sourcing goal is the sync
  script's read side, not yet written — see the table above and
  [`plans/ar_level_duo_annotations.md`](https://github.com/mc2-center/governanceDUO/blob/main/plans/ar_level_duo_annotations.md).
- **Policy Fabric**: `make policy-fabric` is a manual, repo-maintainer-run command
  against one `AccessRequirement` example at a time — nothing triggers it
  automatically.
- **DRS interoperability**: no pipeline, no server, no populated data — see
  [DRS interoperability](drs-interop.md)'s own "What this page is not" section.

## Summary

| Component | Use case | Source today | Status |
| --- | --- | --- | --- |
| DUO conditions | Gate Synapse data access by DUO condition | Curator Record Set, bound to this repo's own generated JSON Schema | **Provisioned, sync pending** — mechanism implemented and live-piloted (`plans/synapse_curation_infrastructure.md`); `plans/ar_level_duo_annotations.md` tracks the remaining read-side sync code |
| Governance Graph | Query "does this user have effective access to this resource?" | Synapse's REST API | **Implemented** — live sync tested offline only; contract-checked against sagebrain-infra's authorizer |
| Provenance and Derivation Policy layers | Carry access labels onto derived content | Synapse's provenance API; computed | **Implemented** — tested offline and against a fixture |
| Policy Fabric crosswalk | Make DUO conditions programmatically enforceable via an external system | One AR record + a static, verified binding table | **Operational, manual** — no automated trigger |
| DRS alignment | Forward-looking interoperability design | N/A | **Design-only** |
