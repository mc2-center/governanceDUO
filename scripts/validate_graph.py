"""
validate_graph.py

Validates the governanceDUO OWL build (governance_duo.owl.ttl, produced by
scripts/build_owl.py) *and* the example instance data (RDF individuals produced by
scripts/convert_examples_to_rdf.py from linkml/examples/*.example.yaml) against the
generated SHACL shapes (shapes/governance_duo.shacl.ttl), using the same invocation
discipline sagebrain-model's tests/validate.py documents as required:

    pySHACL must run with inference OFF and the ontology passed via ont_graph
    (never -i entailment) — RDFS entailment on rdfs:range would manufacture the
    very types sh:class checks are supposed to verify, masking real violations.

Note on coverage: `gen-shacl` compiles cardinality/datatype/pattern/enum (sh:in)
constraints from the LinkML schema, but does NOT compile LinkML `rules:` (the DUO
conditional-requirement logic on GovernanceMixin, e.g. "DUO:0000007 requires
diseaseSpecificResearch") into SHACL — confirmed by inspecting
shapes/governance_duo.shacl.ttl, which has no sh:xone/sh:not construct tied to
dataUseModifiers. That enforcement is covered separately by `linkml-validate`
(compiled to JSON Schema `allOf`/`if`/`then`, which does carry the conditionals) —
see the examples under linkml/examples/. This script's SHACL pass covers everything
else: enum membership, required fields, regex patterns (e.g. the MONDO/ROR CURIE
patterns), datatypes, and cardinality.

Usage:
    python scripts/validate_graph.py [--data governance_duo.owl.ttl]
                                      [--shapes shapes/governance_duo.shacl.ttl]
                                      [--instances linkml/examples/rdf/all_examples.ttl]

author: orion.banks
"""

import argparse
import sys
from pathlib import Path

from pyshacl import validate


def run_validation(data_path: str, shapes_path: str, ont_path: str) -> bool:
    conforms, _results_graph, results_text = validate(
        data_graph=data_path,
        shacl_graph=shapes_path,
        ont_graph=ont_path,
        inference="none",
        abort_on_first=False,
        allow_warnings=True,
    )
    print(f"--- {data_path} ---")
    print(results_text)
    return conforms


def main():
    parser = argparse.ArgumentParser(
        description="Validate the governanceDUO OWL build and example instance data against the SHACL shapes."
    )
    parser.add_argument("--data", default="governance_duo.owl.ttl")
    parser.add_argument("--shapes", default="shapes/governance_duo.shacl.ttl")
    parser.add_argument("--instances", default="linkml/examples/rdf/all_examples.ttl")
    args = parser.parse_args()

    all_conform = True

    all_conform &= run_validation(args.data, args.shapes, args.data)

    if Path(args.instances).exists():
        all_conform &= run_validation(args.instances, args.shapes, args.data)
    else:
        print(
            f"Skipping instance-level validation: {args.instances} not found "
            "(run scripts/convert_examples_to_rdf.py first)."
        )

    if not all_conform:
        print("SHACL validation FAILED", file=sys.stderr)
        sys.exit(1)

    print("SHACL validation passed.")


if __name__ == "__main__":
    main()
