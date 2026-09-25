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

**Decided: program-first**, not type-first. One folder per program/DCC at the
top level; record-type subfolders (`AccessRequirement`, `Study`, `Resource`,
`Schema`) are created within each program's folder to hold that class's Record
Set:

```
Folder(name="<program>", parent_id="<programs-parent-id>").store(synapse_client=syn)   # once per program
Folder(name="<class_name>", parent_id="<program-folder-id>").store(synapse_client=syn) # per program, per class
```

The trade-off this carries (discussed and accepted): layer 1 can no longer find
"every Record Set of type X" by listing the children of one known folder — it
has to discover *every program's* folder first, then find the matching
class-named subfolder within each. Layer 1, below, covers exactly how.

**Consistency with the existing production structure — resolved (2026-09-25).**
README's "Submitting metadata to the database" documents `Study`/`Resource`/
`Schema` folders that looked like existing production structure, type-first
(`requirements`/`resources`/`studies`, real ids like `syn71723125`). **Per the
user: these were placeholder content, never actually used in practice** — so
there's no live migration to perform, just cleanup. Decision: the same project
(`syn71723047`) is the basis for the new program-first folders for all four
classes (`AccessRequirement`, `Study`, `Resource`, `Schema`); the old
placeholder type-first folders are moved aside into an `ARCHIVED` folder within
that project rather than migrated or deleted outright. This removes the
two-hierarchies concern entirely — program-first now applies uniformly to
every curated class from the start, and the layer-1 `EntityView` folder index
applies the same way to all of them.

## Layer 3: provision a Record Set + curation task in that folder

Bootstrap an empty CSV from the schema's own property names (this repo's
`json_schemas/<Class>.json`, not a hardcoded template), then:

```
RecordSet(name=f"{class_name}_RecordSet", parent_id=class_folder_id,
          path=<bootstrapped empty csv>, upsert_keys=["id"]
).store(synapse_client=syn)

record_set.bind_schema(json_schema_uri=<registered schema uri>,
                       enable_derived_annotations=False)

CurationTask(data_type=class_name, project_id="syn71723047",
             instructions=<synthesized from this repo's own docs, see below>,
             task_properties=RecordBasedMetadataTaskProperties(record_set_id=...)
).store(synapse_client=syn)

Grid(record_set_id=...).create(synapse_client=syn)
```

`project_id`, confirmed: `syn71723047` (the one shared project every program's
folder lives under — same as `--programs-parent-id`, see Layer 2 and "Proposed
tool shape" below).

`instructions`, confirmed: synthesized from this repo's own docs rather than
hand-written per class or left as a placeholder — e.g. each LinkML class's
`description:` (already the source `gen-doc` renders into
`docs/reference/classes/<Class>.md`), so the curation task's instructions and
this repo's own generated documentation for that class stay in lockstep
automatically as the schema evolves.

Naming simplified from the type-first draft (`{program}_{class_name}_RecordSet`)
to just `{class_name}_RecordSet` -- under program-first, the parent folder
chain (`{program}/{class_name}/`) already encodes the program, so restating it
in the Record Set's own name would be redundant.

**`upsert_keys=["id"]`, confirmed** — the class's own `id` slot is the primary
key in the schema (per this class's `slot_usage` pattern), and is what a
curator actually fills in — not a separate Synapse-assigned row key. This is
also the join key `sync_governance_graph.py` will use to look up a specific
AR's row once it queries the layer-1 view.

## Layer 1: the unified view, and how "automatic wiring" actually works

**Important nuance the request's phrasing could be read to gloss over**: Synapse
doesn't automatically keep a `MaterializedView`'s `defining_sql` current when a
new Record Set is created elsewhere. There's no scope-based auto-inclusion for
Record Sets the way an `EntityView` has for files (confirmed: `ViewTypeMask` has
no `RECORDSET` value, so an `EntityView` can't be scoped to "every Record Set
under this folder" directly). "Automatically wired" has to mean **the
provisioning tool itself updates the view** as part of creating each new Record
Set, not that Synapse does it unprompted -- **confirmed as the intended design**:

1. **Discovery, under program-first: an `EntityView` folder index, not a single
   type-level folder listing.** Since a program-first hierarchy means every
   program's `{class_name}` Record Set lives one level down inside that
   program's own folder (`{program}/{class_name}/`), there's no single folder
   whose direct children are "every program's Record Set of this type" to list
   the way a type-first hierarchy would allow. Instead: one project-scoped
   `EntityView` per class, `scope_ids=[<programs-parent-id>]`,
   `view_type_mask=ViewTypeMask.FOLDER`, `add_default_columns=True` -- Synapse
   `EntityView`s search their scope recursively (confirmed via
   `EntityView.__doc__`: `scope_ids` are "container ids" the view indexes
   through, matching the existing `DatasetView`/`PublicationView` precedent in
   `create_id_folders.py`). Querying that view with `WHERE name = '{class_name}'`
   returns every program's matching subfolder in one call; for each, look up its
   child Record Set (`find_entity_id(name=f"{class_name}_RecordSet",
   parent=folder_id)`) to get the ids the `UNION` needs.
   **Confirmed live (2026-09-25), against `syn71723047`.** Created a throwaway
   `EntityView` (`view_type_mask=ViewTypeMask.FOLDER`,
   `scope_ids=["syn71723121"]` -- the `studies` folder, which has three real
   nested subfolders: `elite`, `example`, `mc2`), queried it
   (`Table(id=view.id).query("SELECT id, name, path FROM {view.id}")`), and got
   back exactly the three nested subfolders (correctly excluding the scope root
   itself):
   ```
        ROW_ID  ROW_VERSION           id     name                             path
   0  71723050            1  syn71723050  example  ADA-PSI Records/studies/example
   1  71723053            1  syn71723053    elite    ADA-PSI Records/studies/elite
   2  71723056            1  syn71723056      mc2      ADA-PSI Records/studies/mc2
   ```
   The recursive scan works as designed. The throwaway view (`syn77582818`) was
   deleted immediately after the query, leaving no trace in the project. One
   gotcha caught along the way: `EntityView`'s constructor arg is
   `include_default_columns`, not `add_default_columns`; and its default
   columns don't include `parentId` -- `path` (e.g.
   `"ADA-PSI Records/studies/example"`) is what's actually available to derive
   ancestry from, not a direct parent-id column.
2. Once the Record Set ids are known: `merge_tables.py`'s pattern applies as-is
   -- build the `UNION`, and
   `MaterializedView(name=, parent_id=, defining_sql=).store()` -- `store()` on
   an existing view (same name/id) regenerates it in place, confirmed by
   `merge_tables.py`'s own docstring ("if table already exists, scope will be
   updated and table will be regenerated in-place").
3. **Confirmed: the layer-3 provisioning step calls the layer-1 update as its
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
      --programs-parent-id <project/folder every program's folder lives under> \
      --schema-uri <registered JSON Schema URI, from make json-schemas + registration> \
      [--dry-run]
  ```
  `--programs-parent-id` replaces the earlier type-first draft's
  `--type-folder-id`: under program-first, the program folder is the top-level
  designation (created once, directly under this shared parent), and
  record-type subfolders are created *within* it, not the other way around --
  so there's no single "AccessRequirement folder" id to pass in; the class name
  instead names the subfolder this tool creates inside each program's folder.

  Steps, in order, each logged and each individually skippable if already done
  (idempotent -- re-running for a program that already has a folder/Record Set
  should warn and continue, not fail or duplicate):
  1. Layer 2: create (or find, if it already exists) `{program}` under
     `--programs-parent-id`, then create (or find) `{class_name}` within that
     program's folder.
  2. Layer 3: bootstrap an empty CSV from the schema's own property titles
     (this repo's own generated `json_schemas/{class_name}.json` -- reusing the
     property-title-extraction approach `create_record_based_metadata_task.py`
     already proved, not reimplementing it independently), create the
     `RecordSet`, bind the schema, create the `CurationTask` +
     `RecordBasedMetadataTaskProperties`, create the `Grid`.
  3. Layer 1: query (or create, if it doesn't exist yet) the `{class_name}`
     `EntityView` scoped to `--programs-parent-id` to discover every program's
     `{class_name}` subfolder (including the one just created), resolve each to
     its child Record Set id, rebuild the `MaterializedView`'s `defining_sql`,
     `store()` it in place.
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
3. ~~Folder hierarchy.~~ **Program-first**, confirmed: one folder per
   program/DCC directly under a shared parent; record-type subfolders
   (`AccessRequirement`, `Study`, `Resource`, `Schema`) created within each
   program's folder. Discovery of "every program's Record Set of type X" uses a
   project-scoped `EntityView` (`FOLDER` mask, queried by subfolder name), not a
   listing of one type-level folder's children -- see Layer 1.
4. ~~Whether layer-3 auto-triggers the layer-1 rebuild.~~ **Confirmed**: yes,
   one tool, ordered steps.
5. ~~The AR Record Set's upsert/join key.~~ **Confirmed: `id`** -- the class's
   own `id` slot is the schema's primary key and what a curator actually fills
   in, not a separate Synapse-assigned row key.
6. ~~Study/Resource/Schema folder migration.~~ **No migration needed** -- the
   existing type-first folders were placeholder content, never used in
   practice. Same project (`syn71723047`), old folders moved into an
   `ARCHIVED` folder, new program-first folders built fresh for all four
   classes uniformly.
7. ~~The `--programs-parent-id` value.~~ **Confirmed: `syn71723047`** -- the
   same project the placeholder folders live in.
8. ~~`CurationTask.instructions` text source.~~ **Confirmed: synthesized from
   this repo's own docs** (class docstrings / `docs/` content), not
   hand-written per class or left as a placeholder.

## Resolved (2026-09-25, continued)

9. ~~Live-verify the `EntityView` folder-index recursive scan.~~ **Confirmed
   live**, against `syn71723047`'s `studies` folder -- see Layer 1 above for
   the result and the `include_default_columns`/`path`-not-`parentId` gotchas
   caught along the way.

## Still open before implementation

1. **Archiving the old placeholder folders and creating the fresh program-first
   ones** -- not yet executed. Now that the `EntityView` discovery mechanism is
   confirmed live, this is the one remaining real, visible-to-others write:
   move `requirements`/`resources`/`studies`/`schemas` into an `ARCHIVED`
   folder under `syn71723047`, then build the new program-first tree. Needs a
   `--dry-run` review pass before anything is moved or created, same as any
   other live provisioning step -- this is the actual implementation work,
   covered by `scripts/provision_curator_infrastructure.py` once written.
