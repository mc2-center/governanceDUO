"""
graph_rdf.py

Writes governance graph layer objects (linkml/graph/governance.yaml) as RDF: the
one path from graph-layer data to Turtle (plans/model_refactor.md). Examples,
the Synapse sync and the derivation builder all hand it a GovernanceGraph.

The GovernanceGraph container is a bundle, not graph content, so its members
are dumped and it is not. The output has no blank nodes: every node carries an
IRI, so Neptune reloads merge rather than duplicate.

Usage:
    python scripts/graph_rdf.py EXAMPLE.yaml [EXAMPLE.yaml ...] --out OUT.ttl

author: orion.banks
"""

import argparse
from functools import lru_cache

from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.dumpers import rdflib_dumper
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.schemaview import SchemaView
from rdflib import BNode, Graph

SCHEMA = "linkml/graph/governance.yaml"
CONTAINER = "GovernanceGraph"
PREFIXES = ("gov", "acl", "vcard", "foaf", "prov", "syn", "synuser", "synteam", "DUO", "MONDO", "xsd")


@lru_cache(maxsize=None)
def schema(path: str = SCHEMA):
    """(SchemaView, generated Python module) for the graph layer."""
    return SchemaView(path), PythonGenerator(path).compile_module()


def load(path: str, schema_path: str = SCHEMA):
    sv, module = schema(schema_path)
    return yaml_loader.load(path, target_class=getattr(module, CONTAINER))


def to_rdf(container, schema_path: str = SCHEMA) -> Graph:
    sv, _ = schema(schema_path)
    graph = Graph()
    for slot in sv.class_induced_slots(CONTAINER):
        for member in getattr(container, slot.name) or []:
            graph += rdflib_dumper.as_rdf_graph(member, schemaview=sv)
    blank = {s for s in graph.subjects() if isinstance(s, BNode)} | {
        o for o in graph.objects() if isinstance(o, BNode)
    }
    if blank:
        raise ValueError(f"{len(blank)} blank nodes in the graph; every node needs an IRI")
    return bind_prefixes(graph, schema_path)


def bind_prefixes(graph: Graph, schema_path: str = SCHEMA) -> Graph:
    namespaces = schema(schema_path)[0].namespaces()
    for prefix in PREFIXES:
        if prefix in namespaces:
            graph.bind(prefix, namespaces[prefix], override=True, replace=True)
    return graph


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("inputs", nargs="+", help="GovernanceGraph YAML files.")
    parser.add_argument("--out", required=True)
    parser.add_argument("--schema", default=SCHEMA)
    args = parser.parse_args()
    graph = Graph()
    for path in args.inputs:
        graph += to_rdf(load(path, args.schema), args.schema)
    bind_prefixes(graph, args.schema).serialize(destination=args.out, format="turtle")
    print(f"Wrote {len(graph)} triples to {args.out}")


if __name__ == "__main__":
    main()
