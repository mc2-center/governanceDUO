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

**Resolved by a live test (2026-09-25), against real Record Sets** (read-only —
`nam-hub-models`' own `RECORD_SET_IDS`, e.g. `syn76403828`, no entities created;
using the current, non-deprecated `synapseclient.models.Table` query API, the
same one `merge_tables.py` itself uses elsewhere — not `syn.tableQuery()`/
`syn.get()`, both deprecated as of 4.9.0/4.11.0):

```python
from synapseclient.models import Table
Table(id="syn76403828").query(query="SELECT * FROM syn76403828 LIMIT 5", synapse_client=syn)
# -> succeeds, returns the Record Set's own rows/columns directly (plus ROW_ID/ROW_VERSION)
```

**A Record Set *is* directly SQL-queryable by its own id.** No companion `Table`
copy is required — this contradicts the initial hypothesis (that they couldn't
be queried), and doesn't match what `merge_tables.py` does either. Since the
direct query demonstrably works, `merge_tables.py`'s copy-into-a-`Table` step
looks like either a workaround for a since-fixed limitation, or a
schema-alignment step unrelated to bare queryability (its own Record Sets may
have had inconsistent columns across programs, needing normalization before a
`UNION` — not confirmed, and not this plan's concern to explain). **Layer 1's
`MaterializedView` can `UNION` Record Set ids directly**:
`defining_sql = " UNION ".join(f"SELECT * FROM {id}" for id in record_set_ids)`
— no intermediate `Table` needed.

## Layer 2: provision a program's folder

```
Folder(name="<program>", parent_id="<type-folder-id>").store(synapse_client=syn)
```

One type-level folder per curated class (e.g. one "AccessRequirement" folder,
mirroring the existing `requirements`/`resources`/`studies` folders README
already documents), with one subfolder per program/DCC underneath, matching the
existing convention exactly (`utils/make_folders.py`'s pattern, adapted to
nest under one project rather than one-per-project).

**Reviewed: program-first instead of type-first is possible, with one
trade-off.** Both are ordinary nested `Folder`s — Synapse doesn't prefer either
direction. The difference is entirely in how layer 1 finds "every Record Set of
type X":

- **Type-first** (above, matches the existing `requirements`/`resources`/
  `studies` convention): layer 1 enumerates the children of *one known folder*
  (the `AccessRequirement` type folder) to find every program's Record Set.
  Simplest discovery path, and consistent with what's already there.
- **Program-first** (`MC2/AccessRequirement`, `MC2/Study`, `ADKP/AccessRequirement`,
  ...): better for a curator managing one program's full set of record types in
  one place, but layer 1 now has to discover *every program's* folder first,
  then find the `AccessRequirement` subfolder within each. That's not a blocker
  — a project-scoped `EntityView` with `ViewTypeMask.FOLDER` gives a
  live-updating, queryable index of every folder's `id`/`name`/`parentId`
  project-wide (`SELECT id FROM {folderIndexView} WHERE name = 'AccessRequirement'`
  finds every program's AR folder in one query) — but it's an extra piece of
  infrastructure type-first doesn't need.

Recommendation stays type-first, for consistency with the existing convention
and because it needs no extra discovery infrastructure — but program-first is
fully workable if DCC-facing ergonomics (one place per program) matter more
than that consistency; the `EntityView` folder-index approach above is the way
to build it if so. This is a workflow-ergonomics call, not a technical one —
open for a decision either way.

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
Set, not that Synapse does it unprompted -- **confirmed as the intended design**:

1. `merge_tables.py`'s pattern: find every existing Record Set of this type
   under the type-level folder (`find_entity_id` per program, or a table/view
   query if one already indexes them), build the `UNION`, and
   `MaterializedView(name=, parent_id=, defining_sql=).store()` -- `store()` on
   an existing view (same name/id) regenerates it in place, confirmed by
   `merge_tables.py`'s own docstring ("if table already exists, scope will be
   updated and table will be regenerated in-place").
2. **Confirmed: the layer-3 provisioning step calls the layer-1 update as its
   last step**, not left as a separate manual pass -- one tool, three ordered
   actions, not three independent tools a person has to remember to run in
   sequence.

## Proposed tool shape

**Resolved: this lives in governanceDUO, not `mc2-center-dcc`.** Reviewed and
decided: this tooling is for a distinct purpose (provisioning *this repo's own*
curated classes' infrastructure, keyed to `json_schemas/`, this repo's own
generated artifact) from MC2's portal-metadata tooling, and may reasonably
diverge from how `mc2-center-dcc`'s scripts work as this repo's own needs
change -- coupling it to a different repo's per-datatype scripts risks exactly
the kind of drift this repo has spent this whole session cleaning up elsewhere
(stale cross-repo assumptions). This repo gains a live-Synapse-**write**
capability it hasn't had before (`sync_governance_graph.py`/
`sync_provenance_graph.py` only read) -- a real, deliberate expansion, not
incidental; the "Risks" section below governs it.

Concretely:

- **`requirements.txt`**: add `synapseclient>=4.9` (the version floor the
  non-deprecated `Table.query`/`Folder`/`RecordSet`/`MaterializedView` API
  needs; already `>=4.0` for the read-only sync scripts, so this is a floor
  bump, not a new dependency).
- **One script, `scripts/provision_curator_infrastructure.py`**, not three
  separate ones -- matching the "one tool, three ordered actions" design above.
  Follows this repo's existing script conventions (docstring-led, `warn()` for
  non-fatal issues, argparse), and this repo's `graph_iris.py`-style discipline
  of not hardcoding IRIs/ids inline:
  ```
  python scripts/provision_curator_infrastructure.py \
      --class-name AccessRequirement --program MC2 \
      --type-folder-id <existing "AccessRequirement" folder> \
      --schema-uri <registered JSON Schema URI, from make json-schemas + registration> \
      [--dry-run]
  ```
  Steps, in order, each logged and each individually skippable if already done
  (idempotent -- re-running for a program that already has a folder/Record Set
  should warn and continue, not fail or duplicate):
  1. Layer 2: create (or find, if it already exists) `{program}` under
     `--type-folder-id`.
  2. Layer 3: bootstrap an empty CSV from the schema's own property titles
     (this repo's own generated `json_schemas/{class_name}.json` -- reusing the
     property-title-extraction approach `create_record_based_metadata_task.py`
     already proved, not reimplementing it independently), create the
     `RecordSet`, bind the schema, create the `CurationTask` +
     `RecordBasedMetadataTaskProperties`, create the `Grid`.
  3. Layer 1: enumerate every program subfolder's Record Set under
     `--type-folder-id` (including the one just created), rebuild the
     `MaterializedView`'s `defining_sql`, `store()` it in place.
  - **`--dry-run`**: print every planned action (folder/Record Set/task/view
    names and parent ids) without calling `.store()`/`.create()` on any of
    them -- the read/plan phase and the write phase are cleanly separable, so a
    person can review before anything live happens. Required by the "Risks"
    section below, not optional.

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

## Resolved (2026-09-25)

1. ~~Record Set direct-SQL-query support.~~ **Confirmed live**: yes, directly
   queryable by id, no companion `Table` needed.
2. ~~Where the tool lives.~~ **This repo**, `scripts/provision_curator_infrastructure.py`.
3. ~~Folder hierarchy.~~ **Type-first** (matches the existing convention),
   program-first left open as a workflow-ergonomics choice, not a technical one.
4. ~~Whether layer-3 auto-triggers the layer-1 rebuild.~~ **Confirmed**: yes,
   one tool, ordered steps.

## Still open before implementation

1. The AR Record Set's actual upsert/join key, confirmed against a real created
   Record Set, not assumed from the schema alone -- needs a live-created test
   Record Set, not just a query against an existing unrelated one.
2. Per-program folder naming/discovery convention (exact name pattern
   `find_entity_id` should search for), so a later sync can locate a specific
   AR's row without a hardcoded id -- depends on the folder-hierarchy choice
   above being finalized.
3. Where `--type-folder-id` for `AccessRequirement` itself comes from the first
   time -- this plan assumes a type-level folder already exists to create
   program subfolders under; provisioning that top-level folder itself (once,
   manually or via this same tool with no `--program`) isn't yet described.
