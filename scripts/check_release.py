"""
check_release.py

Verifies that every published artifact (README "Release artifacts and IRI policy")
carries the release version: exactly one owl:Ontology header whose owl:versionInfo
equals --version and whose owl:versionIRI ends with it. With --tag, also checks the
tag is `v<version>`. Run by `make release-check` after `make validate-all`.

Usage:
    python scripts/check_release.py --version 0.1.0 [--tag v0.1.0]

author: orion.banks
"""

import argparse
import sys

from rdflib import Graph
from rdflib.namespace import OWL, RDF

ARTIFACTS = [
    "shapes/governance_duo.owl.ttl",
    "shapes/governance_graph.owl.ttl",
    "shapes/governance_graph.shacl.ttl",
    "shapes/provenance_layer.shacl.ttl",
]


def main():
    parser = argparse.ArgumentParser(description="Check published artifacts carry the release version.")
    parser.add_argument("--version", required=True)
    parser.add_argument("--tag")
    args = parser.parse_args()

    failures = []
    if args.tag and args.tag != f"v{args.version}":
        failures.append(f"tag {args.tag!r} does not match version {args.version!r} (expected v{args.version})")

    for path in ARTIFACTS:
        g = Graph().parse(path)
        ontologies = list(g.subjects(RDF.type, OWL.Ontology))
        if len(ontologies) != 1:
            failures.append(f"{path}: expected one owl:Ontology header, found {len(ontologies)}")
            continue
        ontology = ontologies[0]
        info = [str(v) for v in g.objects(ontology, OWL.versionInfo)]
        iris = [str(v) for v in g.objects(ontology, OWL.versionIRI)]
        if info != [args.version]:
            failures.append(f"{path}: owl:versionInfo {info}, expected [{args.version!r}]")
        if len(iris) != 1 or not iris[0].endswith(f"/{args.version}"):
            failures.append(f"{path}: owl:versionIRI {iris}, expected one ending in /{args.version}")

    if failures:
        print("release check FAILED:")
        for failure in failures:
            print(f"  - {failure}")
        sys.exit(1)
    print(f"release check passed: {len(ARTIFACTS)} artifacts at version {args.version}.")


if __name__ == "__main__":
    main()
