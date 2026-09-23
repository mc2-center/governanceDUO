"""
check_release.py

Verifies that every published artifact (README "Release artifacts and IRI policy")
carries its own release version: exactly one owl:Ontology header whose
owl:versionInfo equals the artifact's version and whose owl:versionIRI ends with
it. With --tag, also checks the tag agrees with --version (the record layer's --
the graph layer versions independently, plans/model_refactor.md, and has no tag
of its own yet). Run by `make release-check` after `make validate-all`.

shapes/governance_duo.owl.ttl (the record layer, VERSION in the Makefile) and
shapes/governance.owl.ttl (the one graph TBox, GRAPH_VERSION) are versioned
independently -- they describe different namespaces on different release
cadences -- so each is checked against its own --version/--graph-version.

Usage:
    python scripts/check_release.py --version 0.1.0 --graph-version 0.2.0 [--tag v0.1.0]

author: orion.banks
"""

import argparse
import sys

from rdflib import Graph
from rdflib.namespace import OWL, RDF

ARTIFACTS = {
    "shapes/governance_duo.owl.ttl": "version",
    "shapes/governance.owl.ttl": "graph_version",
}


def check_artifact(path: str, version: str, failures: list) -> None:
    g = Graph().parse(path)
    ontologies = list(g.subjects(RDF.type, OWL.Ontology))
    if len(ontologies) != 1:
        failures.append(f"{path}: expected one owl:Ontology header, found {len(ontologies)}")
        return
    ontology = ontologies[0]
    info = [str(v) for v in g.objects(ontology, OWL.versionInfo)]
    iris = [str(v) for v in g.objects(ontology, OWL.versionIRI)]
    if info != [version]:
        failures.append(f"{path}: owl:versionInfo {info}, expected [{version!r}]")
    if len(iris) != 1 or not iris[0].endswith(f"/{version}"):
        failures.append(f"{path}: owl:versionIRI {iris}, expected one ending in /{version}")


def main():
    parser = argparse.ArgumentParser(description="Check published artifacts carry their release version.")
    parser.add_argument("--version", required=True, help="Record-layer version (shapes/governance_duo.owl.ttl).")
    parser.add_argument("--graph-version", required=True, help="Graph-layer version (shapes/governance.owl.ttl).")
    parser.add_argument("--tag", help="Checked against --version; the graph layer has no tag of its own yet.")
    args = parser.parse_args()

    versions = {"version": args.version, "graph_version": args.graph_version}
    failures = []
    if args.tag and args.tag != f"v{args.version}":
        failures.append(f"tag {args.tag!r} does not match version {args.version!r} (expected v{args.version})")

    for path, version_key in ARTIFACTS.items():
        check_artifact(path, versions[version_key], failures)

    if failures:
        print("release check FAILED:")
        for failure in failures:
            print(f"  - {failure}")
        sys.exit(1)
    print(
        f"release check passed: shapes/governance_duo.owl.ttl at {args.version}, "
        f"shapes/governance.owl.ttl at {args.graph_version}."
    )


if __name__ == "__main__":
    main()
