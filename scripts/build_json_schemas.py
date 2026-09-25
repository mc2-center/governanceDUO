"""
build_json_schemas.py

Generates a Synapse Curator-compatible JSON Schema for each record-layer class
populated through curation (AccessRequirement, Study, Resource, Schema) -- one
schema per class, bindable to a folder to drive a Record Set/curation task.
Curator Record Sets built against these schemas are now the sole source of
curated data, including DUO conditions on AccessRequirement
(plans/ar_level_duo_annotations.md) -- replacing the archived schematic-driven
generator (archive/scripts/create_json_from_model.py,
archive/scripts/generate_duo_schema.py) and the `schematic` CLI submission
workflow, both deprecated (README's "Materials available in this repository").

Uses LinkML's own JsonSchemaGenerator directly against
linkml/governance_duo.linkml.yaml -- no dependency on schematic or the archived
model/*.model.csv (now archive/model/*.model.csv) it read from. GovernanceMixin's
DUO-conditional rules (the same `rules:` linkml-validate enforces, see
mixins.yaml) compile into this schema's own allOf/if/then conditionals, so a
Record Set built against it prompts for a companion field (e.g.
diseaseSpecificResearch) exactly when a curator selects the DUO code that
requires it.

Property names are this schema's own camelCase slot names (dataUseModifiers, not
DataUseModifiers) -- deliberately, since linkml-lint's --ignore-warnings
exception (Makefile) exists specifically because these names are also live
Synapse annotation keys.

Unconfirmed against live Synapse (no credentials in this environment): whether
Synapse's schema service accepts this schema's JSON Schema dialect as-is, and
whether derivedAnnotations conditional binding behaves the same way it did for
the old schematic-generated schemas. Bind one schema to a test folder and create
a Record Set from it before relying on this in production.

Usage:
    python scripts/build_json_schemas.py [--schema linkml/governance_duo.linkml.yaml]
        [--out-dir json_schemas]

author: orion.banks
"""

import argparse
import json
from pathlib import Path

from linkml.generators.jsonschemagen import JsonSchemaGenerator

SCHEMA = "linkml/governance_duo.linkml.yaml"
# The record-layer classes populated through curation (tree_root: true and
# curator-facing -- PolicyCardBindingCollection is also tree_root but is
# reference data, not a curation target, so it's left out).
CURATOR_CLASSES = ["AccessRequirement", "Study", "Resource", "Schema"]


def build(schema_path: str, class_name: str) -> dict:
    gen = JsonSchemaGenerator(schema_path, top_class=class_name)
    return json.loads(gen.serialize())


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--schema", default=SCHEMA)
    parser.add_argument("--out-dir", default="json_schemas")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for class_name in CURATOR_CLASSES:
        schema = build(args.schema, class_name)
        out_path = out_dir / f"{class_name}.json"
        out_path.write_text(json.dumps(schema, indent=2) + "\n")
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
