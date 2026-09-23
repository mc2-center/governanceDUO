"""
check_graph.py

Checks the governance graph layer's generated TBox and shapes
(scripts/build_graph_tbox.py) against the canonical example graph:

1. The example conforms to shapes/governance.shacl.ttl.
2. Each of a set of deliberate defects in the example is caught by SHACL: a
   value outside its vocabulary, a principal named twice or not at all, an
   unknown property on a closed shape, a missing required status, a link to a
   node of the wrong type, the abstract DUO:0000017 as a data-use term, and an
   epoch-millisecond timestamp.
3. The TBox keeps the layer's conventions:
   - every vocabulary concept has one skos:prefLabel, one skos:notation per
     scheme it's in, and at most one skos:definition;
   - no axiom is made about a term outside gov: (declarations only);
   - every gov: class and property has an rdfs:label;
   - the only blank nodes are the domain unions;
   - nothing refers to the pre-refactor namespace.
4. graph_rdf.to_rdf refuses blank nodes.

Usage:
    python scripts/check_graph.py

author: orion.banks
"""

import sys

from pyshacl import validate
from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SKOS, XSD

import graph_rdf

TBOX = "shapes/governance.owl.ttl"
SHAPES = "shapes/governance.shacl.ttl"
EXAMPLE = "linkml/examples/graph/governance_graph.example.yaml"
LEGACY_NS = "https://sagebionetworks.org/governance/"

GOV = Namespace("https://w3id.org/synapse/governance#")
GOVID = Namespace("https://w3id.org/synapse/governance/")
ACL = Namespace("http://www.w3.org/ns/auth/acl#")
SYN = Namespace("https://www.synapse.org/Synapse:")
USER = Namespace("https://www.synapse.org/Profile:")
DUO = Namespace("http://purl.obolibrary.org/obo/DUO_")

AUTHORIZATION = GOVID["authorization/syn10081783-9000001"]
APPROVAL = GOVID["approval/55001"]
CONDITION = GOVID["ar/42/condition/DUO_0000007"]
FILE = SYN.syn10081783


def conforms(data: Graph, ont: Graph, shapes: Graph) -> tuple[bool, str]:
    ok, _, text = validate(data, shacl_graph=shapes, ont_graph=ont, advanced=True)
    return ok, text


def defects():
    """(description, function that breaks a copy of the example graph)."""
    return [
        ("a permission outside the Permission scheme",
         lambda g: g.add((AUTHORIZATION, ACL.mode, GOV.Bogus))),
        ("an Authorization naming both an agent and a group",
         lambda g: g.add((AUTHORIZATION, ACL.agent, USER["2000001"]))),
        ("an Authorization naming no principal",
         lambda g: g.remove((AUTHORIZATION, ACL.agentGroup, None))),
        ("an unknown property on a closed shape",
         lambda g: g.add((FILE, GOV.bindingType, GOV.Direct))),
        ("an Approval with no status",
         lambda g: g.remove((APPROVAL, GOV.status, None))),
        ("requiresAR pointing at a node that isn't an AccessRequirement",
         lambda g: g.add((FILE, GOV.requiresAR, USER["2000001"]))),
        ("the abstract DUO:0000017 as a data-use term",
         lambda g: (g.remove((CONDITION, GOV.dataUseTerm, None)),
                    g.add((CONDITION, GOV.dataUseTerm, DUO["0000017"])))),
        ("an epoch-millisecond timestamp",
         lambda g: (g.remove((APPROVAL, GOV.expiresAt, None)),
                    g.add((APPROVAL, GOV.expiresAt, Literal(1786736000000, datatype=XSD.long))))),
    ]


def tbox_problems(tbox: Graph) -> list[str]:
    problems = []
    concept_classes = set(tbox.subjects(RDFS.subClassOf, SKOS.Concept))
    for cc in concept_classes:
        for concept in tbox.subjects(RDF.type, cc):
            labels = list(tbox.objects(concept, SKOS.prefLabel))
            notations = set(tbox.objects(concept, SKOS.notation))
            definitions = list(tbox.objects(concept, SKOS.definition))
            if len(labels) != 1 or len(notations) != 1 or len(definitions) > 1:
                problems.append(f"{concept}: {len(labels)} prefLabel, {len(notations)} notation, "
                                f"{len(definitions)} definition")
            if not any(tbox.objects(concept, SKOS.inScheme)):
                problems.append(f"{concept}: in no scheme")

    for s, p, o in tbox:
        if isinstance(s, URIRef) and not str(s).startswith(str(GOV)) and s != URIRef(str(GOV)[:-1]):
            if not (p == RDF.type and o in (OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty,
                                           OWL.AnnotationProperty)):
                problems.append(f"axiom about a term outside gov:: {s} {p} {o}")
        if LEGACY_NS in str(s) or LEGACY_NS in str(o):
            problems.append(f"legacy namespace: {s} {p} {o}")
        if isinstance(s, BNode) and not (tbox.value(s, OWL.unionOf) or any(tbox.subjects(RDF.rest, s))
                                         or any(tbox.subjects(OWL.unionOf, s))):
            problems.append(f"unexpected blank node: {s} {p} {o}")

    for t in (OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty):
        for term in tbox.subjects(RDF.type, t):
            if str(term).startswith(str(GOV)) and not (tbox.value(term, RDFS.label) or tbox.value(term, SKOS.prefLabel)):
                problems.append(f"{term}: no label")
    return problems


def main() -> int:
    failures = []
    tbox = Graph().parse(TBOX)
    shapes = Graph().parse(SHAPES)
    example = graph_rdf.to_rdf(graph_rdf.load(EXAMPLE))

    ok, text = conforms(example, tbox, shapes)
    if not ok:
        failures.append(f"the canonical example doesn't conform:\n{text}")

    for description, breaks in defects():
        broken = Graph()
        broken += example
        breaks(broken)
        ok, _ = conforms(broken, tbox, shapes)
        if ok:
            failures.append(f"SHACL missed {description}")

    failures += tbox_problems(tbox)

    container = graph_rdf.load(EXAMPLE)
    container.activities[0].qualifiedUsage[0].id = None
    try:
        graph_rdf.to_rdf(container)
        failures.append("to_rdf accepted a node with no IRI")
    except Exception:  # noqa: BLE001 -- any refusal (missing identifier, blank node) is right
        pass

    if failures:
        print("\n".join(f"FAIL: {f}" for f in failures))
        return 1
    print(f"Graph layer checks passed ({len(defects())} defects caught; TBox conventions hold).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
