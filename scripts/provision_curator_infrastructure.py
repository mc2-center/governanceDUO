"""
provision_curator_infrastructure.py

Provisions the Synapse-side infrastructure that Curator Record Set curation
depends on, for one LinkML class this repo generates a JSON Schema for
(AccessRequirement, Study, Resource, Schema -- see build_json_schemas.py's
CURATOR_CLASSES), one program/DCC at a time
(plans/synapse_curation_infrastructure.md, which resolved every decision this
script implements). Three layers, always in this order, each individually
skippable if it already exists:

  1. Layer 2 (folders): find-or-create a `{program}` folder directly under
     `--programs-parent-id`, then find-or-create a `{class_name}` subfolder
     inside it -- program-first, so record-type subfolders live one level
     down inside each program's own folder, not the other way around.
  2. Layer 3 (Record Set + curation task): inside that `{class_name}` folder,
     bootstrap an empty CSV from this repo's own generated
     `json_schemas/{class_name}.json` property titles, create the
     `{class_name}_RecordSet` from it, bind the registered JSON Schema, create
     its `CurationTask` (instructions synthesized from this repo's own LinkML
     class description, so they stay in lockstep with the schema as it
     evolves) and its Grid. If the Record Set already exists, its
     CurationTask/Grid are assumed to exist too -- warned and skipped, not
     independently re-detected.
  3. Layer 1 (the unified view): program-first means there's no single folder
     whose direct children are "every program's Record Set of this type", so
     discovery goes through a project-scoped `EntityView` folder index
     (`{class_name}_FolderIndex`, scope_ids=[--programs-parent-id],
     view_type_mask=ViewTypeMask.FOLDER) queried for every program's
     `{class_name}` subfolder; each folder's child Record Set id is resolved,
     and the `{class_name}_RecordSets` MaterializedView is rebuilt as a UNION
     over all of them. This step always runs (it's the "automatic wiring"),
     not skipped when the view already exists.

Only non-deprecated synapseclient APIs: synapseclient.models
(Folder, RecordSet, CurationTask, RecordBasedMetadataTaskProperties, Grid,
Table, MaterializedView, EntityView, ViewTypeMask) and
synapseclient.operations.find_entity_id. Never syn.tableQuery(), syn.get(), or
syn.getUserProfile().

No hardcoded Synapse ids: --programs-parent-id is a required argument every
time, even though this deployment's value is resolved to syn71723047 in the
plan above -- that value belongs to the caller, not this script.

--dry-run: every read (find_entity_id, the EntityView query) still executes
normally -- only .store()/.create()/.bind_schema() calls are skipped. Each
layer's function first discovers the current state, prints what it would do,
and only then performs the write, guarded by a single `if not dry_run:`.

Usage:
    python scripts/provision_curator_infrastructure.py \\
        --class-name AccessRequirement --program MC2 \\
        --programs-parent-id syn71723047 \\
        --schema-uri org.sagebionetworks.governanceduo-AccessRequirement-1.0.0 \\
        [--dry-run]

author: orion.banks
"""

import argparse
import json
import sys
import tempfile
from pathlib import Path

import pandas as pd
from linkml_runtime.utils.schemaview import SchemaView
from synapseclient import Synapse, operations
from synapseclient.models import (
    CurationTask,
    EntityView,
    Folder,
    Grid,
    MaterializedView,
    RecordBasedMetadataTaskProperties,
    RecordSet,
    Table,
    ViewTypeMask,
)

from build_json_schemas import CURATOR_CLASSES

LINKML_SCHEMA = "linkml/governance_duo.linkml.yaml"
JSON_SCHEMA_DIR = "json_schemas"
UPSERT_KEYS = ["id"]  # the class's own `id` slot is this schema's primary key


def warn(message: str) -> None:
    print(f"WARNING: {message}", file=sys.stderr)


def extract_property_titles(schema_data: dict) -> list[str]:
    """A JSON Schema's own property titles, in declaration order (falling back
    to the property's own name if it has no title) -- the same extraction
    create_record_based_metadata_task.py uses to bootstrap a Record Set's
    starting columns."""
    titles = []
    for name, data in schema_data.get("properties", {}).items():
        titles.append(data.get("title", name) if isinstance(data, dict) else name)
    return titles


def bootstrap_csv(class_name: str, json_schema_dir: str) -> Path:
    """An empty CSV whose header is class_name's own JSON Schema property
    titles (this repo's generated json_schemas/{class_name}.json), to seed a
    new Record Set."""
    schema_path = Path(json_schema_dir) / f"{class_name}.json"
    schema_data = json.loads(schema_path.read_text())
    titles = extract_property_titles(schema_data)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    pd.DataFrame(columns=titles).to_csv(tmp.name, index=False)
    return Path(tmp.name)


def curation_instructions(class_name: str, linkml_schema: str) -> str:
    """The curation task's instructions, synthesized from this repo's own
    LinkML class description -- kept in lockstep with the schema as it
    evolves, never hand-written per class or left as a placeholder."""
    description = SchemaView(linkml_schema).get_class(class_name).description
    if not description:
        warn(f"{class_name} has no LinkML class description; the curation task's instructions will be empty.")
    return description or ""


# -- layer 2: folders ---------------------------------------------------------

def provision_folders(syn: Synapse, program: str, class_name: str, programs_parent_id: str, dry_run: bool) -> str | None:
    """Find-or-create `{programs_parent_id}/{program}/{class_name}/`. Returns
    the class folder's id, or None if dry-run and neither folder exists yet
    (nothing to point downstream layers at)."""
    program_folder_id = operations.find_entity_id(name=program, parent=programs_parent_id, synapse_client=syn)
    if program_folder_id:
        warn(f"[layer 2] Program folder '{program}' already exists ({program_folder_id}); reusing it.")
    else:
        print(f"PLAN [layer 2]: CREATE Folder(name={program!r}, parent_id={programs_parent_id})")
        if not dry_run:
            program_folder_id = Folder(name=program, parent_id=programs_parent_id).store(synapse_client=syn).id
            print(f"  -> created program folder '{program}': {program_folder_id}")

    class_folder_id = None
    if program_folder_id:
        class_folder_id = operations.find_entity_id(name=class_name, parent=program_folder_id, synapse_client=syn)
    if class_folder_id:
        warn(f"[layer 2] Class folder '{class_name}' already exists ({class_folder_id}) under program '{program}'; reusing it.")
    else:
        parent_label = program_folder_id or "<program folder, not yet created>"
        print(f"PLAN [layer 2]: CREATE Folder(name={class_name!r}, parent_id={parent_label})")
        if not dry_run:
            class_folder_id = Folder(name=class_name, parent_id=program_folder_id).store(synapse_client=syn).id
            print(f"  -> created class folder '{class_name}': {class_folder_id}")
    return class_folder_id


# -- layer 3: record set + curation task --------------------------------------

def provision_record_set(
    syn: Synapse,
    class_name: str,
    class_folder_id: str | None,
    schema_uri: str,
    programs_parent_id: str,
    dry_run: bool,
) -> str | None:
    """Bootstrap the `{class_name}_RecordSet` inside the class folder, bind
    the schema, create its CurationTask and Grid. If the Record Set already
    exists, its CurationTask/Grid are assumed to exist too and this is
    skipped entirely -- there's no clean lookup to independently re-detect
    them. Returns the Record Set's id, or None if nothing exists yet and
    dry-run prevents creating it."""
    record_set_name = f"{class_name}_RecordSet"
    if class_folder_id is None:
        print(f"PLAN [layer 3]: CREATE RecordSet(name={record_set_name!r}, parent_id=<class folder, not yet created>, "
              f"upsert_keys={UPSERT_KEYS})")
        print(f"PLAN [layer 3]: BIND schema {schema_uri!r} to the new Record Set (enable_derived_annotations=False)")
        print(f"PLAN [layer 3]: CREATE CurationTask(data_type={class_name!r}, project_id={programs_parent_id})")
        print("PLAN [layer 3]: CREATE Grid for the new Record Set, export_to_record_set()")
        return None

    existing_id = operations.find_entity_id(name=record_set_name, parent=class_folder_id, synapse_client=syn)
    if existing_id:
        warn(f"[layer 3] Record Set '{record_set_name}' already exists ({existing_id}); "
             "assuming its CurationTask and Grid already exist too, skipping the rest of layer 3.")
        return existing_id

    csv_path = bootstrap_csv(class_name, JSON_SCHEMA_DIR)
    instructions = curation_instructions(class_name, LINKML_SCHEMA)
    print(f"PLAN [layer 3]: CREATE RecordSet(name={record_set_name!r}, parent_id={class_folder_id}, "
          f"path={csv_path}, upsert_keys={UPSERT_KEYS})")
    print(f"PLAN [layer 3]: BIND schema {schema_uri!r} to the new Record Set (enable_derived_annotations=False)")
    print(f"PLAN [layer 3]: CREATE CurationTask(data_type={class_name!r}, project_id={programs_parent_id}, "
          f"instructions=<{class_name}'s LinkML class description>)")
    print("PLAN [layer 3]: CREATE Grid for the new Record Set, export_to_record_set()")
    if dry_run:
        return None

    record_set = RecordSet(
        name=record_set_name, parent_id=class_folder_id, path=str(csv_path), upsert_keys=UPSERT_KEYS,
    ).store(synapse_client=syn)
    print(f"  -> created Record Set '{record_set_name}': {record_set.id}")

    record_set.bind_schema(json_schema_uri=schema_uri, enable_derived_annotations=False, synapse_client=syn)
    print(f"  -> bound schema {schema_uri!r} to {record_set.id}")

    CurationTask(
        data_type=class_name, project_id=programs_parent_id, instructions=instructions,
        task_properties=RecordBasedMetadataTaskProperties(record_set_id=record_set.id),
    ).store(synapse_client=syn)
    print(f"  -> created CurationTask for {record_set.id}")

    grid = Grid(record_set_id=record_set.id)
    grid.create(synapse_client=syn)
    grid.export_to_record_set(synapse_client=syn)
    print(f"  -> created Grid for {record_set.id} and exported it to the Record Set")

    return record_set.id


# -- layer 1: the unified view ------------------------------------------------

def rebuild_unified_view(
    syn: Synapse,
    class_name: str,
    programs_parent_id: str,
    dry_run: bool,
    just_provisioned_record_set_id: str | None,
) -> None:
    """Discover every program's `{class_name}` folder via a project-scoped
    EntityView folder index, resolve each to its child Record Set id, and
    rebuild the `{class_name}_RecordSets` MaterializedView as a UNION over all
    of them. Always runs its store(), whether or not the view already
    existed -- this is the "automatic wiring" step, not an idempotency
    shortcut."""
    view_name = f"{class_name}_FolderIndex"
    view_id = operations.find_entity_id(name=view_name, parent=programs_parent_id, synapse_client=syn)
    if view_id:
        warn(f"[layer 1] EntityView '{view_name}' already exists ({view_id}); reusing it.")
    else:
        print(f"PLAN [layer 1]: CREATE EntityView(name={view_name!r}, parent_id={programs_parent_id}, "
              f"scope_ids=[{programs_parent_id}], view_type_mask=ViewTypeMask.FOLDER, include_default_columns=True)")
        if not dry_run:
            view_id = EntityView(
                name=view_name, parent_id=programs_parent_id, scope_ids={programs_parent_id},
                view_type_mask=ViewTypeMask.FOLDER, include_default_columns=True,
            ).store(synapse_client=syn).id
            print(f"  -> created EntityView '{view_name}': {view_id}")

    folder_ids: list[str] = []
    if view_id:
        rows = Table(id=view_id).query(
            query=f"SELECT id, name, path FROM {view_id} WHERE name = '{class_name}'", synapse_client=syn,
        )
        folder_ids = rows["id"].tolist()
    else:
        warn(f"[layer 1] '{view_name}' doesn't exist yet (dry-run); no folders to discover this pass.")

    record_set_ids = []
    for folder_id in folder_ids:
        rs_id = operations.find_entity_id(name=f"{class_name}_RecordSet", parent=folder_id, synapse_client=syn)
        if rs_id:
            record_set_ids.append(rs_id)
        else:
            warn(f"[layer 1] Folder {folder_id} has no {class_name}_RecordSet child yet; excluding it from the unified view.")

    if just_provisioned_record_set_id and just_provisioned_record_set_id not in record_set_ids:
        warn(f"[layer 1] The Record Set just provisioned ({just_provisioned_record_set_id}) wasn't among the "
             f"'{view_name}' discovery results yet (possible EntityView indexing lag); re-run to pick it up.")

    if not record_set_ids:
        warn(f"[layer 1] No {class_name} Record Sets discovered yet; skipping the unified view rebuild.")
        return

    defining_sql = " UNION ".join(f"SELECT * FROM {rid}" for rid in record_set_ids)
    mv_name = f"{class_name}_RecordSets"
    mv_id = operations.find_entity_id(name=mv_name, parent=programs_parent_id, synapse_client=syn)
    print(f"PLAN [layer 1]: STORE MaterializedView(id={mv_id or '<new>'}, name={mv_name!r}, "
          f"parent_id={programs_parent_id}, defining_sql={defining_sql!r})")
    if not dry_run:
        MaterializedView(
            id=mv_id, name=mv_name, parent_id=programs_parent_id, defining_sql=defining_sql,
        ).store(synapse_client=syn)
        print(f"  -> rebuilt unified view '{mv_name}' over {len(record_set_ids)} Record Set(s)")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--class-name", required=True, choices=CURATOR_CLASSES,
                        help="The LinkML class to provision curator infrastructure for.")
    parser.add_argument("--program", required=True, help="The program/DCC name (e.g. MC2).")
    parser.add_argument("--programs-parent-id", required=True,
                        help="Synapse id of the project/folder every program's folder lives under.")
    parser.add_argument("--schema-uri", required=True,
                        help="The registered JSON Schema URI to bind the new Record Set to.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print every planned action without creating or modifying anything in Synapse.")
    args = parser.parse_args()

    syn = Synapse()
    syn.login()  # default credential resolution

    class_folder_id = provision_folders(syn, args.program, args.class_name, args.programs_parent_id, args.dry_run)
    record_set_id = provision_record_set(
        syn, args.class_name, class_folder_id, args.schema_uri, args.programs_parent_id, args.dry_run,
    )
    rebuild_unified_view(syn, args.class_name, args.programs_parent_id, args.dry_run, record_set_id)


if __name__ == "__main__":
    main()
