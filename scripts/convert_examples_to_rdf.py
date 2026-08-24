"""
convert_examples_to_rdf.py

Converts the instance examples under linkml/examples/*.example.yaml into RDF
individuals (Turtle), so they can be validated against shapes/governance_duo.shacl.ttl
with real instance data instead of just the schema-level OWL build.

This schema's ids are bare, colon-free dotted strings (e.g. `access_requirement.42`
— the SageCommonDataModel-style convention this schema deliberately follows).
linkml_runtime's RDF dumper can only mint a subject URI for such an id via a special
`"@base"` namespace entry, and that entry can *only* be supplied externally at dump
time (`prefix_map={"@base": ...}` on the dumper's own Python API) — the schema's own
`prefixes:` block cannot declare it at all (`Prefix('@base', ...)` raises
`ValueError: @base: Not a valid NCName`), and the CLI's `-P/--prefix` flag hits that
same crash trying to register it. An earlier version of this script supplied a
made-up `@base` IRI this way, which also required a second workaround: the dumper
binds every namespaces() entry — including the `"@base"` one it was just given — as
a Turtle `@prefix`, and `@prefix @base: <...> .` isn't valid Turtle, so the raw
output had to be rebuilt into a fresh graph that skipped that one invalid binding
before it could be re-parsed.

Both workarounds are unnecessary once an id contains a colon: `Namespaces.uri_for()`
then resolves it as a real CURIE against the schema's own already-declared
`governanceduo:` prefix directly — no `@base` involved at all (confirmed directly:
`sv.namespaces().uri_for("governanceduo:access_requirement.42")` resolves with no
`@base` entry present, while the bare `"access_requirement.42"` form does not). So
this script loads each instance exactly as before (its id is validated against the
class's own bare-dotted `pattern` at load time, unchanged), then temporarily
rewrites the loaded object's `id` to CURIE form — `governanceduo:access_requirement.42`
— only for the RDF-dump call, restoring the bare form afterward. The *stored* id in
every example YAML file, and every class's `slot_usage.id.pattern`, are completely
unaffected — this preserves interoperability with SageCommonDataModel's own bare-id
convention everywhere except this one transient export step.

Usage:
    python scripts/convert_examples_to_rdf.py [--schema linkml/governance_duo.linkml.yaml]
                                               [--examples-dir linkml/examples]
                                               [--out-dir linkml/examples/rdf]

author: orion.banks
"""

import argparse
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


def to_curie(bare_id: str, default_prefix: str) -> str:
    """`access_requirement.42` -> `governanceduo:access_requirement.42`. Raises if
    already CURIE-shaped (contains a colon) -- this schema's stored ids never do,
    so that would indicate a caller passed the wrong thing in."""
    if ":" in bare_id:
        raise ValueError(f"'{bare_id}' already contains a colon; expected a bare dotted id")
    return f"{default_prefix}:{bare_id}"


def from_curie(curie: str) -> str:
    """Inverse of to_curie -- `governanceduo:access_requirement.42` ->
    `access_requirement.42`. Not called by this script's own flow (the bare id is
    restored from a saved variable, not by re-deriving it), but kept alongside
    to_curie so the mapping is documented as invertible, not just one-directional."""
    if ":" not in curie:
        raise ValueError(f"'{curie}' has no colon; expected a CURIE")
    _prefix, local = curie.split(":", 1)
    return local


def convert_one(example_path: Path, class_name: str, module, schemaview: SchemaView) -> Graph:
    target_class = getattr(module, class_name)
    obj = yaml_loader.load(str(example_path), target_class=target_class)

    bare_id = obj.id
    obj.id = to_curie(bare_id, schemaview.schema.default_prefix)
    try:
        graph = RDFLibDumper().as_rdf_graph(obj, schemaview)
    finally:
        obj.id = bare_id  # defensive: restore in case the loaded object is reused

    return graph


def main():
    parser = argparse.ArgumentParser(
        description="Convert linkml/examples/*.example.yaml instances to RDF Turtle."
    )
    parser.add_argument("--schema", default="linkml/governance_duo.linkml.yaml")
    parser.add_argument("--examples-dir", default="linkml/examples")
    parser.add_argument("--out-dir", default="linkml/examples/rdf")
    args = parser.parse_args()

    schemaview = SchemaView(args.schema)
    module = compile_python(PythonGenerator(args.schema).serialize())

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    merged = Graph()

    for stem, class_name in EXAMPLE_CLASSES.items():
        example_path = Path(args.examples_dir) / f"{stem}.example.yaml"
        if not example_path.exists():
            continue
        graph = convert_one(example_path, class_name, module, schemaview)
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
