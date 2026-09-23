"""
check_prov_alignment.py

Checks that every W3C PROV-O term this repo's OWL declares (prov:Activity,
prov:generated, prov:entity, ...) is declared with a type W3C PROV-O itself gives
it: owl:Class, owl:ObjectProperty, owl:DatatypeProperty or owl:AnnotationProperty
(plans/iri_valued_slots_as_object_properties.md). A term typed differently -- e.g.
prov:generated as owl:DatatypeProperty, as build_owl.py emitted it before
xsd_anyuri_as_iri -- is punned against PROV-O wherever both are loaded, which is
not OWL 2 DL. A prov: term PROV-O doesn't declare at all is reported too.

This compares declared types directly rather than DL-checking a union with
PROV-O: PROV-O has puns of its own (prov:specializationOf, prov:wasRevisionOf are
both annotation and object properties), which would make that check fail no
matter what this repo declares. `make owl-profile` runs it against the PROV-O
2013-04-30 Recommendation, fetched into build/; scripts/check_sagebrain_contract.py
reuses type_mismatches() against sagebrain-model's vendored prov.ttl.

The record OWL (shapes/governance_duo.owl.ttl) no longer asserts on prov: --
Activity/Usage moved to the graph layer (plans/model_refactor.md) -- so the one
TBox that declares prov: terms is the graph TBox, shapes/governance.owl.ttl.

Usage:
    python scripts/check_prov_alignment.py --prov-o PATH [--tbox PATH ...]

author: orion.banks
"""

import argparse
import sys
from pathlib import Path

from rdflib import Graph, Namespace
from rdflib.namespace import OWL, RDF

PROV = Namespace("http://www.w3.org/ns/prov#")
DECLARATION_TYPES = (OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty)
TBOXES = ["shapes/governance.owl.ttl"]


def declarations(graph: Graph) -> dict:
    """Each prov: term the graph declares, mapped to its declaration types."""
    declared = {}
    for declaration_type in DECLARATION_TYPES:
        for term in graph.subjects(RDF.type, declaration_type):
            if str(term).startswith(str(PROV)):
                declared.setdefault(term, set()).add(declaration_type)
    return declared


def type_mismatches(tbox_paths: list, prov_o: Graph) -> list[str]:
    """One message per prov: term a TBox declares with a type PROV-O doesn't give it."""
    reference = declarations(prov_o)
    failures = []
    for path in tbox_paths:
        for term, types in sorted(declarations(Graph().parse(path)).items()):
            name = f"prov:{term.removeprefix(str(PROV))}"
            if term not in reference:
                failures.append(f"{path}: {name} is not declared in PROV-O")
                continue
            for declaration_type in sorted(types - reference[term]):
                expected = ", ".join(sorted(f"owl:{t.removeprefix(str(OWL))}" for t in reference[term]))
                failures.append(
                    f"{path}: {name} is owl:{declaration_type.removeprefix(str(OWL))}, "
                    f"PROV-O declares it {expected}"
                )
    return failures


def main():
    parser = argparse.ArgumentParser(description="Check this repo's prov: declarations against W3C PROV-O.")
    parser.add_argument("--prov-o", required=True, help="PROV-O ontology file (Turtle)")
    parser.add_argument("--tbox", action="append", help=f"TBox to check (repeatable; default: {', '.join(TBOXES)})")
    args = parser.parse_args()

    tboxes = args.tbox or TBOXES
    failures = type_mismatches(tboxes, Graph().parse(Path(args.prov_o), format="turtle"))
    if failures:
        print(f"FAIL  {len(failures)} prov: term(s) typed differently from PROV-O:")
        for failure in failures:
            print(f"        - {failure}")
        sys.exit(1)
    print(f"PROV-O alignment: every prov: term in {', '.join(tboxes)} matches PROV-O's declared type.")


if __name__ == "__main__":
    main()
