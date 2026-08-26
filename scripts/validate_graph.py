"""
validate_graph.py

Validates the governanceDUO OWL build (shapes/governance_duo.owl.ttl, produced by
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

Also reused (via --ont/--data, with --instances omitted) to validate
governance_graph_export/governance_graph.ttl against shapes/governance_graph.shacl.ttl,
using shapes/governance_graph.owl.ttl as the ont_graph -- see the `governance-graph-
validate` Makefile target. That ABox has no separate "schema build" file the way
shapes/governance_duo.owl.ttl doubles as one, so only a single validation pass is run.

Usage:
    python scripts/validate_graph.py [--data shapes/governance_duo.owl.ttl]
                                      [--shapes shapes/governance_duo.shacl.ttl]
                                      [--ont ONT_GRAPH]
                                      [--instances INSTANCES]

    --ont defaults to --data's value if omitted (not a separate hardcoded default —
    see --ont's own --help text). --instances defaults to None/skipped if omitted;
    the Makefile's `shacl-validate` target always passes it explicitly.

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
    parser.add_argument("--data", default="shapes/governance_duo.owl.ttl")
    parser.add_argument("--shapes", default="shapes/governance_duo.shacl.ttl")
    parser.add_argument(
        "--ont",
        default=None,
        help="ont_graph to pass to pySHACL. Defaults to --data (the original "
        "governance_duo.owl.ttl behavior, where the OWL build doubles as its own "
        "ontology graph).",
    )
    parser.add_argument(
        "--instances",
        default=None,
        help="Optional second data graph to validate against the same shapes/ont "
        "(e.g. linkml/examples/rdf/all_examples.ttl). Skipped if omitted.",
    )
    args = parser.parse_args()

    ont_path = args.ont or args.data
    all_conform = True

    all_conform &= run_validation(args.data, args.shapes, ont_path)

    if args.instances:
        if Path(args.instances).exists():
            all_conform &= run_validation(args.instances, args.shapes, ont_path)
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
