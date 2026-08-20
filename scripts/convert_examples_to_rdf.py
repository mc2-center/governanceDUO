"""
convert_examples_to_rdf.py

Converts the instance examples under linkml/examples/*.example.yaml into RDF
individuals (Turtle), so they can be validated against shapes/governance_duo.shacl.ttl
with real instance data instead of just the schema-level OWL build.

This exists because `linkml-convert`'s `-P/--prefix` CLI flag cannot set the special
"@base" prefix map entry that linkml_runtime's RDF dumper needs to mint a subject URI
for a colon-free identifier (e.g. `access_requirement.42` — the dotted, SageCommonData
Model-style id this schema uses): the CLI passes every `-P` pair through
`schema.prefixes[k] = Prefix(k, v)`, and `Prefix()` rejects "@base" as "not a valid
NCName" before it ever reaches the dumper. The dumper's own `as_rdf_graph()`/`dumps()`
Python API *does* accept `prefix_map={"@base": ...}` directly (it special-cases that
key to call `namespaces._base = v`), so this script calls that API directly instead of
shelling out to the CLI.

It also works around a real linkml_runtime bug in that same code path:
`as_rdf_graph()` iterates every entry in `schemaview.namespaces()` — including the
special `"@base"` entry it just set — and calls `graph.bind("@base", ...)` on all of
them. rdflib's Turtle serializer then emits `@prefix @base: <...> .`, which is not
valid Turtle (`@base` is not a legal PN_PREFIX) and fails to re-parse. This script
copies the dumped graph's triples into a fresh Graph, binding only namespace prefixes
that are valid Turtle prefix names, before serializing.

Usage:
    python scripts/convert_examples_to_rdf.py [--schema linkml/governance_duo.linkml.yaml]
                                               [--examples-dir linkml/examples]
                                               [--out-dir linkml/examples/rdf]
                                               [--base-iri https://w3id.org/sage-bionetworks/governance-duo/individuals/]

author: orion.banks
"""

import argparse
import re
from pathlib import Path

from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.dumpers.rdflib_dumper import RDFLibDumper
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.schemaview import SchemaView
from rdflib import Graph

# example filename (without .example.yaml) -> target LinkML class name
EXAMPLE_CLASSES = {
    "access_requirement": "AccessRequirement",
    "study": "Study",
}

VALID_PREFIX_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_.-]*")


def convert_one(example_path: Path, class_name: str, module, schemaview: SchemaView, base_iri: str) -> Graph:
    target_class = getattr(module, class_name)
    obj = yaml_loader.load(str(example_path), target_class=target_class)

    dumper = RDFLibDumper()
    raw_graph = dumper.as_rdf_graph(obj, schemaview, prefix_map={"@base": base_iri})

    # Work around linkml_runtime binding the literal "@base" key as a Turtle prefix
    # (see module docstring) by rebuilding the graph with only valid prefix bindings.
    clean_graph = Graph()
    clean_graph.base = base_iri
    for prefix, namespace in raw_graph.namespace_manager.namespaces():
        if VALID_PREFIX_RE.fullmatch(prefix):
            clean_graph.bind(prefix, namespace)
    for triple in raw_graph:
        clean_graph.add(triple)
    return clean_graph


def main():
    parser = argparse.ArgumentParser(
        description="Convert linkml/examples/*.example.yaml instances to RDF Turtle."
    )
    parser.add_argument("--schema", default="linkml/governance_duo.linkml.yaml")
    parser.add_argument("--examples-dir", default="linkml/examples")
    parser.add_argument("--out-dir", default="linkml/examples/rdf")
    parser.add_argument(
        "--base-iri",
        default="https://w3id.org/sage-bionetworks/governance-duo/individuals/",
    )
    args = parser.parse_args()

    schemaview = SchemaView(args.schema)
    module = compile_python(PythonGenerator(args.schema).serialize())

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    merged = Graph()
    merged.base = args.base_iri

    for stem, class_name in EXAMPLE_CLASSES.items():
        example_path = Path(args.examples_dir) / f"{stem}.example.yaml"
        if not example_path.exists():
            continue
        graph = convert_one(example_path, class_name, module, schemaview, args.base_iri)
        out_path = out_dir / f"{stem}.ttl"
        graph.serialize(destination=str(out_path), format="turtle")
        print(f"Wrote {len(graph)} triples to {out_path}")
        for triple in graph:
            merged.add(triple)
        for prefix, namespace in graph.namespace_manager.namespaces():
            merged.bind(prefix, namespace, override=False)

    merged_path = out_dir / "all_examples.ttl"
    merged.serialize(destination=str(merged_path), format="turtle")
    print(f"Wrote merged {len(merged)} triples to {merged_path}")


if __name__ == "__main__":
    main()
