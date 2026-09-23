"""
check_domain_range.py

Checks that every rdfs:domain and class-valued rdfs:range axiom in this repo's
TBoxes already holds on this repo's own graphs (plans/pre_pr_review_fixes.md,
finding 3). An axiom that doesn't hold isn't an error SHACL can see -- the
validations run with inference off -- but any RDFS/OWL reasoner, sagebrain's
merged graph included, would use it to re-type nodes: a gov:etag domain of
SynapseEntity made every AccessApproval carrying an etag a SynapseEntity.

For each axiom `p rdfs:domain C` (or `p rdfs:range C`, C a class), every subject
(object) of p in the graphs must be asserted a C, or a subclass of C per the
TBoxes' rdfs:subClassOf. No other entailment is applied. A range over a LinkML
enum is checked by membership instead (plans/enum_values_match_owl.md), read from
what the OWL entails: an enum of individuals (owl:oneOf, e.g. GrantPermissionEnum)
must be given one of them, and a literal enum (a datatype defined by owl:oneOf) one
of its strings. An enum of classes (DUO codes, PrincipalTypeEnum), which enumerates
nothing in OWL, is checked against its linkml:permissible_values.
Other datatype ranges are not checked here; SHACL covers literal datatypes.

Usage:
    python scripts/check_domain_range.py [--tbox PATH ...] [--data PATH ...]

author: orion.banks
"""

import argparse
import sys
from collections import Counter

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import OWL, RDF, RDFS

LINKML = Namespace("https://w3id.org/linkml/")

TBOXES = ["shapes/governance_graph.owl.ttl", "shapes/governance_duo.owl.ttl"]
GRAPHS = [
    "governance_graph_export/governance_graph.ttl",
    "linkml/examples/rdf/all_examples.ttl",
    "linkml/examples/provenance/rdf/all_examples.ttl",
    "linkml/examples/derivation_policy/rdf/all_examples.ttl",
]


def superclasses(tbox: Graph, cls) -> set:
    found, stack = {cls}, [cls]
    while stack:
        for parent in tbox.objects(stack.pop(), RDFS.subClassOf):
            if isinstance(parent, URIRef) and parent not in found:
                found.add(parent)
                stack.append(parent)
    return found


def violations(tbox: Graph, data: Graph) -> list[str]:
    enums = set(tbox.subjects(LINKML.permissible_values, None))
    classes = (set(tbox.subjects(RDF.type, OWL.Class)) | set(tbox.subjects(RDF.type, RDFS.Class))) - enums
    types = {}

    def asserted_types(node) -> set:
        if node not in types:
            types[node] = set().union(set(), *(superclasses(tbox, t) for t in data.objects(node, RDF.type)))
        return types[node]

    name = tbox.namespace_manager.normalizeUri
    failures = []
    for axiom, position in ((RDFS.domain, 0), (RDFS.range, 2)):
        for prop, cls in sorted(tbox.subject_objects(axiom)):
            if cls not in classes:
                continue
            nodes = {triple[position] for triple in data.triples((None, prop, None))}
            wrong = Counter(
                ", ".join(sorted(name(t) for t in data.objects(node, RDF.type))) or "(untyped)"
                for node in nodes
                if cls not in asserted_types(node)
            )
            for node_types, count in sorted(wrong.items()):
                failures.append(
                    f"{name(prop)} rdfs:{name(axiom).split(':')[-1]} {name(cls)}: "
                    f"{count} node(s) typed {node_types}"
                )
    for prop, enum in sorted(tbox.subject_objects(RDFS.range)):
        if enum not in enums:
            continue
        definition = tbox.value(enum, OWL.equivalentClass)
        if definition is not None and tbox.value(definition, OWL.oneOf) is not None:
            allowed = {str(v) for v in Collection(tbox, tbox.value(definition, OWL.oneOf))}
            member = lambda v: isinstance(v, Literal) and str(v) in allowed  # noqa: E731
        elif tbox.value(enum, OWL.oneOf) is not None:
            allowed = set(Collection(tbox, tbox.value(enum, OWL.oneOf)))
            member = lambda v: v in allowed  # noqa: E731
        else:
            allowed = set(tbox.objects(enum, LINKML.permissible_values))
            member = lambda v: v in allowed  # noqa: E731
        wrong = sorted({v for v in data.objects(None, prop) if not member(v)}, key=str)
        if wrong:
            failures.append(
                f"{name(prop)} rdfs:range {name(enum)}: values not in the enum: "
                + ", ".join(v.n3(tbox.namespace_manager) for v in wrong)
            )
    return failures


def main():
    parser = argparse.ArgumentParser(description="Check TBox domain/range axioms against this repo's graphs.")
    parser.add_argument("--tbox", action="append", help=f"TBox (repeatable; default: {', '.join(TBOXES)})")
    parser.add_argument("--data", action="append", help="graph to check (repeatable; default: the exported and example graphs)")
    args = parser.parse_args()

    tbox = Graph()
    for path in args.tbox or TBOXES:
        tbox.parse(path)
    data = Graph()
    for path in args.data or GRAPHS:
        data.parse(path)

    failures = violations(tbox, data)
    if failures:
        print(f"FAIL  {len(failures)} domain/range axiom(s) contradicted by the graphs:")
        for failure in failures:
            print(f"        - {failure}")
        sys.exit(1)
    print("Domain/range check: every rdfs:domain and class rdfs:range holds on the exported and example graphs.")


if __name__ == "__main__":
    main()
