# DUO conditions sourced from Access Requirement-level annotation

## Decision

DUO conditions will be sourced from an annotation ACT applies directly to the
Access Requirement, not from a separately curator-authored record fed through the
DUO-core submission pipeline (`plans/governance_graph_ingestion.md`'s Section 3,
"DUO conditions: 100% curator-authored"). **This decision is adopted** (user,
2026-09-24) as the target design; it partially supersedes that plan — see
"What this changes" below. It is not yet implementable end to end: the concrete
Synapse-side mechanism is still open (see "Blocked on" below).

## Context

An ACT/DUO discussion proposal (2026-09-24) identifies the current state of DUO
annotation as a source of "consistent[] fail[ure] for applying governance
annotations consistently and at scale": annotations are applied on individual
entities (file, folder, project) at various points during ingestion, by data
contributors and/or curators, creating accuracy and alignment risk against the ARs
actually governing those entities.

**The proposal:** apply DUO annotations to the AR itself, not to individual
entities. ARs are already exclusively created and managed by ACT, and entities
already inherit their governing AR(s); if the annotation lives on the AR, every
entity assigned that AR inherits the annotation the same way, automatically, with
no separate per-entity annotation step. When ACT updates an AR, every entity that
inherits it gets the updated annotation (versioned) — one edit, not N.

Rationale given: no new owner (ACT already owns AR create/update); no new trigger
(annotation changes ride along with an AR update ACT would make anyway); no
knowledge hand-off (the team that knows what uses are/aren't permissible sets the
annotation directly, instead of that knowledge passing through a separate curation
step).

**Open questions the proposal itself flags** (its own words: "for discussion, not
blockers"): whether one AR applied to multiple entities can need multiple or
conflicting DUO terms — the example given is a managed AR at a higher level
(folder/project) with individual clickwraps below it, where DK vs. US variants of
the same study need different `Research Specific Restriction` terms. The proposal
notes a "flexible AR schema currently under development" as the likely mechanism
for handling this (auto-tagging flex-AR components with DUO codes), but that
schema isn't built yet.

## What this changes

`plans/governance_graph_ingestion.md`'s Section 3 concluded, correctly, at the
time: "Synapse's native `AccessRequirement` interface has no data-use-condition
fields at all... this isn't a temporary sourcing gap, it's a structural fact about
what Synapse's `AccessRequirement` is" — and therefore designed
`scripts/sync_governance_graph.py` to merge in a separately-maintained
curator-authored record (`--access-requirement-dir`) as the only way to get
`Condition` data onto the graph.

That structural fact is exactly what this proposal changes: once ACT's annotation
mechanism exists, the AR object (or its new flex-schema form) *does* carry
DUO-condition data, fetchable in the same pull that already retrieves the AR
(`GET /entity/{id}/accessRequirement`, per `sync_governance_graph.py`'s existing
step 3). At that point:

- `build_graph.GraphBuilder.curated_access_requirement()` and the
  `--access-requirement-dir` curator-record merge stop being the DUO-condition
  source. `scripts/sync_governance_graph.py`'s `add_access_requirements()` reads
  conditions directly off the AR it's already iterating, instead of looking up a
  matching file under a curator directory.
- The conditional-JSON-schema mechanism `docs/use-cases.md`'s "submission
  pipeline" section describes (`generate_duo_schema.py`, a conditional schema bound
  to a folder, deriving an AR's annotation from matching entity annotations) was
  never actually put into practice — confirmed by the user, 2026-09-24, and
  consistent with `plans/governance_graph_ingestion.md`'s own ground rules calling
  the same framework "archived... a pilot process being superseded, not a design to
  stay compatible with." It should be documented as deprecated/never-shipped, not
  as an active in-development effort this decision now supersedes. This decision is
  simply the real path DUO conditions take once it exists — there was no prior
  working mechanism to replace. Curator Record Sets / CSV+`schematic` submission of
  `Study`/`Resource`/`Schema` records generally is a separate, unaffected concern.
- This is a straightforward net simplification for governanceDUO's own pipeline:
  we already fetch every AR an entity has; the change is fetching one more field
  (or set of fields) off an object we already hold, not adding a new class of
  entity to track down.

**Not changing:** the curated-record mechanism itself
(`build_graph.GraphBuilder.curated_access_requirement()`, `record_rules()`,
`GovernanceMixin`'s `rules:`) stays in place and functioning until the new source
is confirmed and wired in — there is currently no other way to get `Condition` data
onto the graph, and removing it first would leave a hole with nothing to fill it.

## Blocked on

The proposal names two possible mechanisms without settling on one:

1. Standard Synapse entity annotations (`GET /entity/{id}/annotations2`) applied
   directly to the `AccessRequirement` object — **unconfirmed whether
   `AccessRequirement` even supports the generic entity-annotations sub-resource**;
   it is not a `NODE`-table entity the way a File/Folder/Project is, so this cannot
   be assumed the way it can for `SynapseEntity`.
2. The "flexible AR schema currently under development" the proposal itself
   names — no design or API surface exists yet to inspect.

Real implementation (a code change to `sync_governance_graph.py`, a schema change
if the annotation shape needs a new slot) is blocked on knowing which of these it
is, and its exact field/endpoint shape. **Next step is confirming this with
whoever owns the AR-annotation mechanism on the Synapse/ACT side** — not something
resolvable from this repo alone.

## Once unblocked

1. Confirm the mechanism and its exact response shape against
   rest-docs.synapse.org or a live call (the same verification standard
   `plans/governance_graph_ingestion.md` used for every other endpoint).
2. Update `scripts/sync_governance_graph.py`'s `add_access_requirements()` to read
   `Condition` data from the confirmed source instead of
   `load_curated_access_requirements()`/`--access-requirement-dir`.
3. Retire `--access-requirement-dir` and the curated-record merge path once the
   new source covers every AR the sync needs (or keep both, warn-don't-block, for
   an AR the new mechanism hasn't been applied to yet — a migration-period
   decision to make at that time, not now).
4. Update `docs/use-cases.md`'s DUO-core/submission-pipeline sections,
   `docs/graph-design.md`/`graph-design-implementation.md`'s "Curators author..."
   framing, and this plan's own status, all of which currently describe the
   curator-authored-record design as current.
5. Report, the same way `plans/model_refactor_report.md` reports on
   `plans/model_refactor.md`: what changed, exact check results, anything left
   unverified against live Synapse.
