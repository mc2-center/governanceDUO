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

Both workarounds are unnecessary once an id is rewritten to a full IRI:
`Namespaces.uri_for()` resolves a string that already looks like an absolute IRI
as-is, no `@base` involved. So this script loads each instance exactly as before
(its id is validated against the class's own bare-dotted `pattern` at load time,
unchanged), then temporarily rewrites the loaded object's `id` to its full IRI --
`scripts/graph_iris.record_iri()`, the one IRI minter (plans/model_refactor.md
R2/R5): a curated AccessRequirement shares its graph node's IRI
(`https://w3id.org/synapse/governance/ar/42`), every other record-layer id keeps
the record namespace (`https://w3id.org/sage-bionetworks/governance-duo/<id>`) --
only for the RDF-dump call, restoring the bare id afterward. The *stored* id in
every example YAML file, and every class's `slot_usage.id.pattern`, are completely
unaffected — this preserves interoperability with SageCommonDataModel's own bare-id
convention everywhere except this one transient export step. See the script's
docstring for the full explanation.

This converts record examples only -- AccessRequirement, Study, DerivationRule.
Graph-layer content (Activity, ControlLabel, DerivationReview, and everything else
in linkml/graph/governance.yaml) is built by scripts/graph_rdf.py from
linkml/examples/graph/*.example.yaml, not here (plans/model_refactor.md).

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

import graph_iris

# example filename (without .example.yaml) -> target LinkML class name
EXAMPLE_CLASSES = {
    "access_requirement": "AccessRequirement",
    "study": "Study",
    "derivation_rule": "DerivationRule",
}


def convert_one(example_path: Path, class_name: str, module, schemaview: SchemaView) -> Graph:
    target_class = getattr(module, class_name)
    obj = yaml_loader.load(str(example_path), target_class=target_class)

    bare_id = obj.id
    obj.id = graph_iris.record_iri(bare_id)
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
