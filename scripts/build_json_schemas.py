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

LinkML's own JSON Schema dialect and Synapse's schema service diverge in four
separate ways, each hit and fixed in turn against a real live registration
attempt (`ADA.PSI-AccessRequirement-0.1.0`, 2026-09-25) rather than assumed:
nullable-type arrays (`include_null=False`, see `build()`), `$defs`/`$ref`
class composition (`_dereference()`), a boolean `additionalProperties`
(`_drop_boolean_additional_properties()`), and LinkML-specific root metadata
plus the 2019-09 `$schema` dialect (`_SYNAPSE_SUPPORTED_ROOT_KEYS`,
`_SYNAPSE_SCHEMA_DIALECT`). Each fix matches the shape of this ecosystem's
other already-working, already-registered schemas (e.g. `MC2Center-Study`,
fetched live for comparison) rather than guessing at what Synapse's parser
wants.

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


def _drop_boolean_additional_properties(node):
    """Synapse's schema service rejects a boolean `additionalProperties`
    ("is not a JSONObject") -- it only accepts an object schema there, or the
    key's absence. LinkML emits the boolean form throughout (closed `false` per
    class, open `true` at the schema root); none of this ecosystem's other
    working, already-registered schemas (e.g. MC2Center-Study) set
    `additionalProperties` at all, so dropping it here matches precedent rather
    than inventing an unverified object-schema equivalent."""
    if isinstance(node, dict):
        if isinstance(node.get("additionalProperties"), bool):
            del node["additionalProperties"]
        for value in node.values():
            _drop_boolean_additional_properties(value)
    elif isinstance(node, list):
        for item in node:
            _drop_boolean_additional_properties(item)


def _dereference(schema: dict) -> dict:
    """Fully flatten $ref/$defs. Synapse's schema service rejects the $defs
    keyword outright ("JSON Element in Entity is Unsupported: $defs") --
    LinkML's default multi-class $ref-based composition doesn't match what
    Synapse accepts. The reference, already-working schemas in this ecosystem
    (e.g. MC2Center-Study) are a single flat schema with no $defs/$ref at all,
    so this replaces every $ref with its target def's own content (local
    sibling keys, e.g. a slot-specific description, take precedence over the
    def's own), recursively, then drops $defs once nothing points at it
    anymore. `inline=True` on the generator removes the *root* class's $ref
    wrapper but still leaves every nested class/enum range as a $defs entry
    (confirmed: AssetBinding, DataTier, etc. all remain), so this step is
    still required even with that flag set."""
    defs = schema.get("$defs", {})

    def resolve(node, seen: frozenset):
        if isinstance(node, dict):
            ref = node.get("$ref")
            if isinstance(ref, str) and ref.startswith("#/$defs/"):
                def_name = ref[len("#/$defs/"):]
                if def_name in seen:
                    raise ValueError(
                        f"Circular $ref while flattening for Synapse: {' -> '.join(seen)} -> {def_name}"
                    )
                target = resolve(defs[def_name], seen | {def_name})
                # A def's own `title` names the *type* (e.g. the enum "Permission"),
                # not the *property* using it (e.g. the accessType slot). Confirmed as a
                # real bug live: it silently overwrote a property's title whenever that
                # property had no local title of its own, and Synapse's bootstrap CSV
                # picks the title as the column header -- "Permission" is not one of the
                # Record Set's actual column names, so a real live run failed with
                # "Permission is not a valid column name or id." Every other working
                # schema in this ecosystem titles a property after the slot, never the
                # range type, so the def's title is dropped here unconditionally.
                target = {k: v for k, v in target.items() if k != "title"}
                return {**target, **{k: resolve(v, seen) for k, v in node.items() if k != "$ref"}}
            return {k: resolve(v, seen) for k, v in node.items()}
        if isinstance(node, list):
            return [resolve(item, seen) for item in node]
        return node

    return {k: resolve(v, frozenset()) for k, v in schema.items() if k != "$defs"}


# The top-level keys the reference, already-working schemas in this ecosystem
# actually contain (checked live against MC2Center-Study, 2026-09-25). LinkML
# also emits `metamodel_version` and `version` at the schema root -- its own
# provenance metadata, not standard JSON Schema -- which Synapse's schema
# service rejects outright ("JSON Element in Entity is Unsupported:
# metamodel_version"). Stripping to this allowlist, rather than removing keys
# one at a time as each is discovered, matches the known-working shape exactly.
_SYNAPSE_SUPPORTED_ROOT_KEYS = {
    "$schema", "$id", "type", "properties", "title", "description", "allOf", "required",
}


# Synapse's schema service only accepts draft-07 ("Unsupported JSON schema
# version: https://json-schema.org/draft/2019-09/schema", confirmed live
# against the 2019-09 dialect LinkML's generator emits by default) -- matching
# the reference schemas' own $schema value. draft-07 supports allOf/if/then,
# so GovernanceMixin's conditionals are unaffected.
_SYNAPSE_SCHEMA_DIALECT = "http://json-schema.org/draft-07/schema#"


def build(schema_path: str, class_name: str) -> dict:
    gen = JsonSchemaGenerator(schema_path, top_class=class_name, include_null=False, inline=True)
    schema = json.loads(gen.serialize())
    schema = _dereference(schema)
    _drop_boolean_additional_properties(schema)
    schema = {k: v for k, v in schema.items() if k in _SYNAPSE_SUPPORTED_ROOT_KEYS}
    schema["$schema"] = _SYNAPSE_SCHEMA_DIALECT
    return schema


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
