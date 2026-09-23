"""
check_artifact_drift.py

Checks that the committed generated artifacts match what the current schema and
scripts produce (plans/pre_pr_review_fixes.md, finding 8;
plans/second_review_fixes.md, finding 5). Run it via `make artifact-drift-check`,
which clears the generated directories, regenerates every artifact (OWL, SHACL,
example RDF, the governance-graph export, docs/reference, the Policy Fabric
export), then runs this: each regenerated file is compared with its committed
version at HEAD, and in each generated directory a committed file that is no
longer produced, or a produced file that isn't committed, fails too. CI runs it
after validate-all, so a schema change committed without regenerating fails
instead of passing on fresh copies.

- shapes/governance_duo.owl.ttl is compared byte for byte: build_owl.py
  canonicalizes it, so rebuilds are byte-identical.
- The other artifacts (SHACL, example RDF, the governance-graph export) are
  compared as graphs, ignoring blank-node labels: their rebuilds reorder
  blank nodes (accepted churn, see
  plans/sagebrain_contract_and_owl_dl_fixes_report.md, open item 1), and full
  RDF canonicalization of the SHACL takes minutes. gen-shacl also writes the
  members of some RDF lists in a different order each run; for the lists SHACL
  reads as sets (sh:ignoredProperties, sh:in) members are sorted first. Each
  blank node is then labeled by iterated hashing of its neighborhood
  (Weisfeiler-Lehman refinement), and the two files' multisets of labeled
  triples must be equal.

Usage:
    python scripts/check_artifact_drift.py

author: orion.banks
"""

import hashlib
import subprocess
import sys
from collections import Counter
from pathlib import Path

from rdflib import BNode, Graph
from rdflib.collection import Collection
from rdflib.namespace import SH

BYTE_EXACT = [
    "shapes/governance_duo.owl.ttl",
    "docs/reference/**/*.md",
    "policy_fabric_export/*.json",
]
GRAPH_EQUAL = [
    "shapes/governance_duo.shacl.ttl",
    "governance_graph_export/governance_graph.ttl",
    "linkml/examples/rdf/*.ttl",
    "linkml/examples/provenance/rdf/*.ttl",
    "linkml/examples/derivation_policy/rdf/*.ttl",
]
# Directories whose whole contents are generated (the make target clears them
# first), so their file lists must match HEAD too.
GENERATED_DIRS = [
    "docs/reference",
    "policy_fabric_export",
    "linkml/examples/rdf",
    "linkml/examples/provenance/rdf",
    "linkml/examples/derivation_policy/rdf",
]
REFINEMENT_ROUNDS = 4
# SHACL list-valued parameters whose member order carries no meaning.
UNORDERED_LISTS = (SH.ignoredProperties, SH["in"])


def committed(path: str) -> bytes | None:
    result = subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True)
    return result.stdout if result.returncode == 0 else None


def sort_unordered_lists(graph: Graph) -> Graph:
    """The graph with each UNORDERED_LISTS list rebuilt in sorted member order."""
    for predicate in UNORDERED_LISTS:
        for subject, head in list(graph.subject_objects(predicate)):
            members = sorted(Collection(graph, head), key=lambda term: term.n3())
            Collection(graph, head).clear()
            graph.remove((subject, predicate, head))
            new_head = BNode()
            Collection(graph, new_head, members)
            graph.add((subject, predicate, new_head))
    return graph


def signature(graph: Graph) -> Counter:
    """The graph's triples with every blank node replaced by a label derived
    from its neighborhood, as a multiset."""
    graph = sort_unordered_lists(graph)
    labels = {node: "_" for triple in graph for node in triple if isinstance(node, BNode)}

    def label(term) -> str:
        return labels[term] if isinstance(term, BNode) else term.n3()

    for _ in range(REFINEMENT_ROUNDS):
        labels = {
            node: hashlib.sha256(
                repr(sorted(
                    [("out", p.n3(), label(o)) for p, o in graph.predicate_objects(node)]
                    + [("in", p.n3(), label(s)) for s, p in graph.subject_predicates(node)]
                )).encode()
            ).hexdigest()
            for node in labels
        }
    return Counter((label(s), p.n3(), label(o)) for s, p, o in graph)


def expand(patterns: list[str]) -> list[str]:
    paths = []
    for pattern in patterns:
        paths += sorted(str(p) for p in Path().glob(pattern)) if "*" in pattern else [pattern]
    return paths


def file_list_drift(directory: str) -> list[str]:
    tracked = set(subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "HEAD", directory], capture_output=True, text=True,
    ).stdout.split())
    present = {str(p) for p in Path(directory).rglob("*") if p.is_file()}
    return [f"{p}: committed but no longer generated" for p in sorted(tracked - present)] + [
        f"{p}: generated but not committed" for p in sorted(present - tracked)
    ]


def drifted(path: str, byte_exact: set) -> str | None:
    old = committed(path)
    if old is None:
        return "not committed"
    new = Path(path).read_bytes()
    if path in byte_exact:
        return None if new == old else "differs from HEAD"
    old_sig = signature(Graph().parse(data=old.decode(), format="turtle"))
    new_sig = signature(Graph().parse(data=new.decode(), format="turtle"))
    if old_sig == new_sig:
        return None
    only_new, only_old = new_sig - old_sig, old_sig - new_sig
    return f"differs from HEAD as a graph (+{sum(only_new.values())}/-{sum(only_old.values())} triples)"


def main():
    byte_exact = set(expand(BYTE_EXACT))
    paths = sorted(byte_exact) + expand(GRAPH_EQUAL)

    failures = [f"{path}: {reason}" for path in paths if (reason := drifted(path, byte_exact))]
    for directory in GENERATED_DIRS:
        failures += [f for f in file_list_drift(directory) if not any(f.startswith(p + ":") for p in paths)]
    if failures:
        print(f"FAIL  {len(failures)} generated artifact(s) don't match the committed version:")
        for failure in failures:
            print(f"        - {failure}")
        print("Regenerate them (make validate-all) and commit the result.")
        sys.exit(1)
    print(f"Artifact drift check: all {len(paths)} generated artifacts match HEAD.")


if __name__ == "__main__":
    main()
