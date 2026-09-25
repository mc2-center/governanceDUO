# Synapse curation infrastructure: folders, Record Sets, and a unified view

## Goal

Tooling to provision the Synapse-side infrastructure that Curator Record Set
curation depends on, for any LinkML class this repo (or a related one) generates
a JSON Schema for — not just `AccessRequirement`. Three layers, as specified:

1. **A single table or view** that combines all Record Sets of a given type
   (e.g. every program's `AccessRequirement` Record Set) into one queryable
   resource.
2. **Folders**, created within a Synapse project, to contain each program's
   Record Set for a given type.
3. **New Record Sets with their curation tasks**, created in those folders and
   wired into the layer-1 view.

This directly unblocks `plans/ar_level_duo_annotations.md`'s open question
("which Synapse resource holds a given AR's Record Set row, and how does a sync
find it") — the layer-1 view *is* the fixed, single queryable resource that
question was missing.

## What's already confirmed, from working code

Two sibling repos already do pieces of exactly this, checked directly rather
than guessed:

- **`nam-hub-models`** (`register_schema.py`, `update_bound_landscape_schema.py`):
  registers a JSON Schema with a Synapse organization
  (`JsonSchemaService.create_json_schema`) and binds it to existing Record Sets
  (`RecordSet(id=...).get()` then `.bind_schema(json_schema_uri=, enable_derived_annotations=)`).
- **`mc2-center-dcc`** (`curator_tools/create_record_based_metadata_task.py`,
  `portal_tables/merge_tables.py`, `utils/make_folders.py`): creates a folder
  (`Folder(name=, parent_id=).store()`), creates a Record Set bootstrapped from
  an empty CSV whose columns are the schema's own property titles
  (`RecordSet(name=, parent_id=, path=<tmp csv>, upsert_keys=).store()`), creates
  its curation task (`CurationTask(data_type=, project_id=, instructions=,
  task_properties=RecordBasedMetadataTaskProperties(record_set_id=)).store()`),
  and creates the curator-facing Grid (`Grid(record_set_id=).create()`,
  `.export_to_record_set()`). Separately, `merge_tables.py` builds exactly
  layer 1: locate each program's Record Set by name under a known parent
  (`operations.find_entity_id(name=, parent=)`), copy its current CSV rows into
  a companion real `Table` (`Table(...).store()` +
  `.store_rows(schema_storage_strategy=SchemaStorageStrategy.INFER_FROM_DATA)`),
  then build a `MaterializedView` whose `defining_sql` is a `UNION` of
  `SELECT * FROM {id}` over every one of those tables.

This confirms the `synapseclient.models` surface to use throughout: `Folder`,
`RecordSet`, `CurationTask`/`RecordBasedMetadataTaskProperties`, `Grid`,
`Table`/`SchemaStorageStrategy`, `MaterializedView`, and
`synapseclient.operations.find_entity_id`.

**One thing genuinely unconfirmed**: whether a Record Set is directly
SQL-queryable by its own id (`SELECT * FROM {recordSetId}`), or whether
`merge_tables.py`'s "copy into a companion `Table`" step is a required
conversion, not just that team's own convention. This changes whether layer 1's
`MaterializedView` unions Record Set ids directly or unions a set of
kept-in-sync companion `Table`s. Confirm with a live test before building either
way — don't assume.

## Layer 2: provision a program's folder

```
Folder(name="<program>", parent_id="<type-folder-id>").store(synapse_client=syn)
```

One type-level folder per curated class (e.g. one "AccessRequirement" folder,
mirroring the existing `requirements`/`resources`/`studies` folders README
already documents), with one subfolder per program/DCC underneath, matching the
existing convention exactly (`utils/make_folders.py`'s pattern, adapted to
nest under one project rather than one-per-project).

## Layer 3: provision a Record Set + curation task in that folder

Bootstrap an empty CSV from the schema's own property names (this repo's
`json_schemas/<Class>.json`, not a hardcoded template), then:

```
RecordSet(name=f"{program}_{class_name}_RecordSet", parent_id=folder_id,
          path=<bootstrapped empty csv>, upsert_keys=[<class's id slot>]
).store(synapse_client=syn)

record_set.bind_schema(json_schema_uri=<registered schema uri>,
                       enable_derived_annotations=False)

CurationTask(data_type=class_name, project_id=project_id,
             instructions=<from this repo's own class docstring?>,
             task_properties=RecordBasedMetadataTaskProperties(record_set_id=...)
).store(synapse_client=syn)

Grid(record_set_id=...).create(synapse_client=syn)
```

`upsert_keys`: for `AccessRequirement`, the natural key is whatever column
carries the real Synapse AR's numeric id (`id`, per this class's own
`slot_usage` pattern) -- confirm this is actually the column a curator fills in,
not a separate Synapse-assigned row key, before relying on it as the join key
`sync_governance_graph.py` would use to look up a specific AR's row.

## Layer 1: the unified view, and how "automatic wiring" actually works

**Important nuance the request's phrasing could be read to gloss over**: Synapse
doesn't automatically keep a `MaterializedView`'s `defining_sql` current when a
new Record Set is created elsewhere. There's no scope-based auto-inclusion for
Record Sets the way an `EntityView` has for files (confirmed: `ViewTypeMask` has
no `RECORDSET` value, so an `EntityView` can't be scoped to "every Record Set
under this folder" directly). "Automatically wired" has to mean **the
provisioning tool itself updates the view** as part of creating each new Record
Set, not that Synapse does it unprompted:

1. `merge_tables.py`'s pattern: find every existing Record Set of this type
   under the type-level folder (`find_entity_id` per program, or a table/view
   query if one already indexes them), build the `UNION`, and
   `MaterializedView(name=, parent_id=, defining_sql=).store()` -- `store()` on
   an existing view (same name/id) regenerates it in place, confirmed by
   `merge_tables.py`'s own docstring ("if table already exists, scope will be
   updated and table will be regenerated in-place").
2. **The layer-3 provisioning step should call the layer-1 update as its last
   step**, not leave it as a separate manual pass -- one tool, three ordered
   actions, not three independent tools a person has to remember to run in
   sequence.

## Proposed tool shape

Given how closely this mirrors `mc2-center-dcc`'s existing scripts, there's a
real question of **where this code should live** -- not answered here, flagged
for a decision:

- **In `mc2-center-dcc`**, alongside `curator_tools/`/`utils/`/`portal_tables/`,
  generalizing the existing per-script patterns to take a JSON Schema path/URI
  and a class name as parameters instead of being written per-datatype. This
  matches where the analogous, already-proven code lives today.
- **In this repo**, since it's specifically about provisioning
  `AccessRequirement` (and this repo's other curated classes') infrastructure,
  and already owns `json_schemas/` generation. Would need its own
  `synapseclient` dependency addition (not currently in `requirements.txt`) and
  its own live-Synapse-write posture, which this repo has not had before now --
  every existing Synapse-touching script here (`sync_governance_graph.py`,
  `sync_provenance_graph.py`) only *reads*.

Recommendation: **`mc2-center-dcc`**, generalized, since it already owns this
exact operational pattern for other datatypes and already carries the
live-write posture and any associated access-control conventions; this repo
stays read-only against Synapse, consistent with what it does today, and only
supplies the schema (`json_schemas/`) the provisioning tool consumes.

## Risks -- read before any live execution

This is genuinely different in kind from everything else scripted in this
session: every prior change was local (files, git commits). This creates real
entities in a live, shared Synapse project -- folders, tables, curation tasks
visible to ACT and other curators. Per this session's own standing
conventions: **never delegate live-write provisioning to a subagent**, run a
`--dry-run` pass and review its planned actions before any live call, and
confirm with the user before the first real folder/Record Set/view gets
created, the same way any destructive-or-shared-state action does. None of
this has been executed -- this is a plan only, as asked.

## Open questions to resolve before implementation

1. Record Set direct-SQL-query support (above) -- resolves whether layer 1
   unions Record Sets directly or needs the companion-`Table` copy step.
2. Where the tool lives (`mc2-center-dcc` vs. here).
3. The AR Record Set's actual upsert/join key, confirmed against a real created
   Record Set, not assumed from the schema alone.
4. Per-program folder naming/discovery convention (exact name pattern
   `find_entity_id` should search for), so a later sync can locate a specific
   AR's row without a hardcoded table id.
