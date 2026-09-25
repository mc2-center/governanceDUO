# DUO conditions sourced from Access Requirement-level annotation

## Decision

DUO conditions will be sourced from an annotation ACT applies directly to the
Access Requirement, not from a separately curator-authored record fed through the
DUO-core submission pipeline (`plans/governance_graph_ingestion.md`'s Section 3,
"DUO conditions: 100% curator-authored"). **This decision is adopted** (user,
2026-09-24) as the target design; it partially supersedes that plan — see
"What this changes" below.

**The mechanism is now resolved** (user, 2026-09-25): Curator tasks built with the
`AccessRequirement` LinkML class's own generated JSON Schema
(`json_schemas/AccessRequirement.json`, `make json-schemas`,
`scripts/build_json_schemas.py`) are used to document AR metadata, including DUO
conditions, as Curator Record Sets — the same mechanism already used for `Study`/
`Resource`/`Schema` (README's "Submitting metadata to the database"), just applied
to `AccessRequirement` too. The graph is populated by pulling from that Record Set;
no separately-maintained curator YAML file is needed. Which files/entities an AR
governs is unaffected and still comes from the existing API calls
(`GET /entity/{id}/accessRequirement`, `sync_governance_graph.py` step 3) — only
the *DUO-condition data itself* moves off local files and onto Synapse. See "What
this changes" and "Once unblocked" below for what's still genuinely open (the
Record Set's own query mechanics, not the overall design).

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
the same study need different `Research Specific Restriction` terms. The
proposal's own "flexible AR schema currently under development" idea for handling
this is superseded by the resolved mechanism below: the *same* Curator Record Set
approach already used for `Study`/`Resource`/`Schema`, applied to
`AccessRequirement` too — there's no separate flex-schema system to build.

## What this changes

`plans/governance_graph_ingestion.md`'s Section 3 concluded, correctly, at the
time: "Synapse's native `AccessRequirement` interface has no data-use-condition
fields at all... this isn't a temporary sourcing gap, it's a structural fact about
what Synapse's `AccessRequirement` is" — and therefore designed
`scripts/sync_governance_graph.py` to merge in a separately-maintained
curator-authored record (`--access-requirement-dir`) as the only way to get
`Condition` data onto the graph.

That structural fact about the *real* Synapse `AccessRequirement` object is still
true and unchanged. What changes is where the DUO data comes from instead: a
Curator Record Set, bound to `json_schemas/AccessRequirement.json`
(`make json-schemas`), is a Synapse table an ACT curator fills in one row per AR —
structurally, an instance of this repo's own `AccessRequirement` LinkML class,
just entered through Synapse's Curator UI instead of a local YAML file under
`linkml/examples/`. That's the key insight: **a Record Set row and a curator YAML
record are the same shape**, because both validate against the same
LinkML-generated JSON Schema. So:

- `build_graph.GraphBuilder.curated_access_requirement()`'s field-parsing logic
  (DUO codes, companion slots, tier) doesn't need to change at all — it already
  takes a plain `record: dict` in this class's shape. Only where that dict comes
  from changes: not `load_curated_access_requirements()`'s local-YAML load, but a
  Synapse Table Query result row, converted to the same shape.
- This is **not** literally the same API call `sync_governance_graph.py` already
  makes. The real `AccessRequirement` (`GET /entity/{id}/accessRequirement`, which
  entities it governs) and its Record Set row (a separate Synapse Table, queried by
  its own id) are two different Synapse resources, joined by the AR's id. The
  simplification is that both are now Synapse API calls, not "an API call plus a
  hand-maintained local file" — see "Blocked on" for the one thing not yet
  confirmed about the second call.
- The conditional-JSON-schema mechanism `docs/use-cases.md` used to describe under
  a "submission pipeline" section (`generate_duo_schema.py`, a conditional schema
  bound to a folder, deriving an AR's annotation from matching entity annotations)
  was never actually put into practice — confirmed by the user, 2026-09-24, and
  consistent with `plans/governance_graph_ingestion.md`'s own ground rules calling
  the same framework "archived... a pilot process being superseded, not a design to
  stay compatible with." It was never an active in-development effort this decision
  supersedes; there was no prior working mechanism to replace. `docs/use-cases.md`
  was rewritten (2026-09-25) to drop that section entirely and reframe around the
  AR as the authoritative DUO source with a 100%-API-sourcing goal, rather than
  leaving the deprecated mechanism documented as a still-current effort.
- **`schematic` is separately, fully deprecated** (user, 2026-09-25) — not just the
  conditional-schema mechanism above. Curator Record Sets, bound to LinkML-generated
  JSON Schema, are now the sole submission mechanism for every curated class,
  replacing the CSV+`schematic`-CLI path entirely (README's "Materials available in
  this repository"). `model/*.model.csv` (the schematic-style CSV data model)
  moved to `archive/model/`; LinkML is the sole source of truth.

**Not changing:** the curated-record mechanism itself
(`build_graph.GraphBuilder.curated_access_requirement()`, `record_rules()`,
`GovernanceMixin`'s `rules:`) stays in place and functioning until the new source
is confirmed and wired in — there is currently no other way to get `Condition` data
onto the graph, and removing it first would leave a hole with nothing to fill it.

## Blocked on

The overall mechanism is resolved (Curator Record Set bound to
`json_schemas/AccessRequirement.json`); what's left is narrower, and entirely
about how the sync reads that Record Set back out, not about what Record Sets are:

1. **Which Synapse resource a Record Set actually is, precisely.** It's created
   per curation task -- likely per program/DCC, the same per-program-folder
   pattern `Study`/`Resource`/`Schema` submissions already use (README's
   "Submitting metadata to the database": one subfolder per program under a
   shared project). That means AR curation is probably **not one single, fixed
   table** the way a per-entity API call is -- there may be one AR Record Set
   per program. **`plans/synapse_curation_infrastructure.md` plans exactly the
   fix for this**: a provisioning tool that keeps one unified `MaterializedView`
   (a `UNION` over every program's AR Record Set) always current as new Record
   Sets are created, so a sync run queries that one view, not per-program
   tables it would otherwise have to discover.
2. **The exact query.** Once the table(s) are known, reading a specific AR's row
   is a Synapse Table Query (`POST /entity/{tableId}/table/query`, `SELECT * FROM
   {tableId} WHERE <ar-id-column> = {id}`, or equivalent) -- a real, documented
   Synapse API, but the exact column that holds the AR's id (and its type) is
   unconfirmed, since Record Set columns come from the bound JSON Schema's own
   property names (this repo's own `id` slot, presumably, but not yet checked
   against a live-created Record Set).
3. Whether a curator-filled Record Set row's shape round-trips cleanly through
   `json_schemas/AccessRequirement.json` back into this class's own field names
   (camelCase slot names, enum `meaning:` values for `dataUseModifiers`) without
   translation -- likely yes, since the schema *is* generated from this class, but
   not yet checked against a real Table Query response.

None of these are design questions -- they're the same kind of "confirm the exact
endpoint/shape against a live call" verification every other Synapse integration
in this repo already went through (`plans/governance_graph_ingestion.md`'s own
"Corrections from the prior pass" section is the precedent). **Next step is a
live smoke test**: create one real (or sandboxed) AccessRequirement Record Set
from `json_schemas/AccessRequirement.json`, fill one row, and run a Table Query
against it.

## Code changes

What's implementable now, without live verification, versus what waits on it:

**Done, this session:**
- `scripts/build_json_schemas.py` / `make json-schemas` -- generates
  `json_schemas/AccessRequirement.json` (and `Study`/`Resource`/`Schema`), the
  schema an AR Record Set binds to. 35 `allOf`/`if`/`then` conditionals, matching
  `GovernanceMixin`'s 35 `rules:` exactly -- confirmed by count.

**Ready to write once the Table Query mechanics above are confirmed** (small,
isolated changes -- no design left to resolve):
1. A new function, e.g. `fetch_ar_record_set_row(syn, ar_id) -> dict | None`, in
   `scripts/sync_governance_graph.py` or a new small module: runs the Table Query,
   returns a dict shaped like a curator YAML record (or `None`, warned, if the AR
   has no Record Set row yet -- the existing "no curated record" warn-don't-block
   behavior, unchanged).
2. `Sync.add_access_requirements()`: replace the `self.curated` dict lookup
   (sourced from `load_curated_access_requirements(--access-requirement-dir)`)
   with a call to the function above. **No change needed** to
   `build_graph.GraphBuilder.curated_access_requirement()` itself -- it already
   takes a plain dict in this shape; only where the dict comes from changes.
3. Drop `--access-requirement-dir` and `load_curated_access_requirements()` once
   every AR the sync needs has a Record Set row (or keep both, warn-don't-block,
   for an AR the new mechanism hasn't been applied to yet -- a migration-period
   decision to make at that time, not now).
4. `scripts/check_sync_governance.py`'s offline fixture: replace its
   `--access-requirement-dir` fixture file with a fake Table Query response,
   same fake-Synapse-client pattern the rest of that fixture already uses.

**Already done as part of this decision, not waiting on the Table Query
mechanics** (pure documentation/schema-layer changes, 2026-09-25):
- `docs/use-cases.md`'s data-sources table and DUO-core section -- reframed
  around the AR as authoritative source and a 100%-API goal; still shows one
  "Gap" row, to close once the code changes above land.
- `docs/graph-design.md`/`graph-design-implementation.md`'s "Curators author..."
  framing -- forward-pointers added, not yet flipped to describe the new source
  as current (correctly -- it isn't, yet).
- `README.md` -- `schematic` deprecated throughout, `model/` archived,
  `make json-schemas` documented.

## Report

Once the code changes above land and are verified live, report the same way
`plans/model_refactor_report.md` reports on `plans/model_refactor.md`: what
changed, exact check results (including the live Table Query smoke test), and
anything still left unverified.
