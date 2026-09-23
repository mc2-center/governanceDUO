"""
project.py

Runs a projection (a SPARQL CONSTRUCT query in projections/) over the canonical
governance graph and writes the result as Turtle (plans/model_refactor.md). The
graph TBox is merged in by default: a projection like authorizer_v1.rq matches
permissions on the Permission concepts' skos:notation, which is asserted there,
not on any ABox.

A projection's --as-of cutoff (authorizer_v1.rq's "is this Approval still
valid") is bound into the query through rdflib's initBindings -- a pre-bound
?asOf solution, the SPARQL analogue of a VALUES row -- never by splicing the
value into the query text.

Usage:
    python scripts/project.py --graph GRAPH [--graph GRAPH ...]
                               --query projections/authorizer_v1.rq
                               [--as-of 2026-01-01T00:00:00Z]
                               --out governance_graph_export/authorizer_v1.ttl
                               [--tbox shapes/governance.owl.ttl]

author: orion.banks
"""

import argparse
from datetime import datetime
from pathlib import Path

from rdflib import Graph, Literal, Namespace
from rdflib.namespace import XSD

ACL = Namespace("http://www.w3.org/ns/auth/acl#")
DEFAULT_TBOX = "shapes/governance.owl.ttl"
# Readability only (doesn't affect the triples): a projection's output is old-
# namespace-heavy, so bind it the way tests/golden/governance_graph.ttl does,
# plus the Synapse entity namespace every projection also emits.
OUTPUT_PREFIXES = {
    "gov": "https://sagebionetworks.org/governance/",
    "syn": "https://www.synapse.org/Synapse:",
}


def load(graphs, tbox: str | None = DEFAULT_TBOX) -> Graph:
    """The given graphs, merged with the graph TBox (skos:notation -- what a
    projection matches permissions on -- lives there, not on the ABox)."""
    g = Graph()
    for path in list(graphs) + ([tbox] if tbox else []):
        g.parse(path, format="turtle")
    return g


def as_of_binding(as_of: str) -> Literal:
    """An ISO-8601 datetime string -> an xsd:dateTime Literal for initBindings.
    Raises on a malformed value rather than silently building a query that
    matches nothing."""
    datetime.fromisoformat(as_of.replace("Z", "+00:00"))
    return Literal(as_of, datatype=XSD.dateTime)


def project(graph: Graph, query: str, as_of: str | None = None) -> Graph:
    """Runs `query` (a CONSTRUCT) over `graph`, with ?asOf pre-bound via
    initBindings when given. Safe against a query that doesn't reference ?asOf
    at all (initBindings for an unused variable is simply unused)."""
    init_bindings = {"asOf": as_of_binding(as_of)} if as_of else {}
    result = graph.query(query, initBindings=init_bindings)
    return result.graph


def inexpressible_agent_classes(graph: Graph) -> int:
    """How many acl:Authorization entries name an acl:agentClass principal
    (PUBLIC/AUTHENTICATED_USERS): authorizer_v1(_teams) can't express these as a
    principal-keyed grant (WAC classes stand for "everyone"/"every signed-in
    user", not a listed member) -- plans/model_refactor.md's fidelity gaps,
    docs/downstream_changes.md."""
    return len(set(graph.subjects(ACL.agentClass, None)))


def main():
    parser = argparse.ArgumentParser(description="Runs a projection over the canonical governance graph.")
    parser.add_argument("--graph", dest="graphs", action="append", required=True,
                        help="Canonical governance graph Turtle (repeatable).")
    parser.add_argument("--query", required=True, help="Projection .rq file (projections/*.rq).")
    parser.add_argument("--as-of", default=None, help="ISO-8601 datetime, bound to ?asOf.")
    parser.add_argument("--out", required=True)
    parser.add_argument("--tbox", default=DEFAULT_TBOX,
                        help="Graph TBox merged into the input (skos:notation lives there); empty string to skip.")
    args = parser.parse_args()

    graph = load(args.graphs, args.tbox or None)
    query = Path(args.query).read_text()
    projected = project(graph, query, args.as_of)
    for prefix, namespace in OUTPUT_PREFIXES.items():
        projected.bind(prefix, namespace, override=True, replace=True)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    projected.serialize(destination=str(out_path), format="turtle")

    print(f"Wrote {len(projected)} triples to {out_path}")
    print(f"{inexpressible_agent_classes(graph)} acl:agentClass authorization(s) authorizer_v1 cannot express "
          f"(PUBLIC/AUTHENTICATED_USERS).")


if __name__ == "__main__":
    main()
