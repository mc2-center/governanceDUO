"""
build_owl.py

Generates an OWL/Turtle representation of the governanceDUO LinkML schema
(linkml/governance_duo.linkml.yaml) and stamps it with the same conventions
sagebrain-model (https://github.com/Sage-Bionetworks/sagebrain-model) uses for its own
ontology and for reused external terms, so the output is close to drop-in-ready for
that repo's `ontology/governance/` folder whenever cross-repo linking is in scope:

- an owl:versionIRI on the ontology declaration (sagebrain stamps every merged build
  with one; here it is derived from --version)
- skos:scopeNote (not rdfs:comment, which sagebrain reserves for classes it mints
  itself) + owl:versionInfo on every reused external class — in this schema, the real
  DUO terms backing `meaning:` CURIEs on DataUseModifierEnum's permissible values

Which DUO terms get stamped is derived from the schema itself at build time (every
DataUseModifierEnum permissible_value with both a `meaning:` CURIE and a
description), not a hardcoded snapshot: an earlier version of this script hardcoded a
list of 8 terms ("the 8 terms this repo has authored curation text for" at the time),
which was already stale (the schema has descriptions for all 24 real DUO terms) and,
independently, never actually worked at all: its dict keys were shaped like
"DUO_0000007" and indexed directly into a Namespace whose base IRI already ends in
"DUO_" (`.../obo/DUO_`), producing a doubled ".../obo/DUO_DUO_0000007" that never
matched anything in the generated graph -- so `governance_duo.owl.ttl` has never
actually carried a single skos:scopeNote/owl:versionInfo stamp on any reused DUO term,
for any version of this script, despite the module and inline comments describing it
as working. Fixed here by deriving the term list from the schema (so it can't
under-cover again) and keying by the bare local suffix (e.g. "0000007") that actually
combines correctly with DUO_NS's already-suffixed base IRI.

Usage:
    python scripts/build_owl.py [--schema linkml/governance_duo.linkml.yaml]
                                 [--out shapes/governance_duo.owl.ttl]
                                 [--version 0.1.0]

author: orion.banks
"""

import argparse

from linkml.generators.owlgen import OwlSchemaGenerator
from linkml_runtime.utils.schemaview import SchemaView
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import OWL, RDFS, SKOS

DUO_NS = Namespace("http://purl.obolibrary.org/obo/DUO_")
GOVERNANCEDUO_NS = Namespace("https://w3id.org/sage-bionetworks/governance-duo/")


def reused_duo_terms(schema_path: str) -> dict:
    """Real DUO terms this schema reuses by IRI: every DataUseModifierEnum
    permissible_value with both a `meaning:` CURIE (so it's a real DUO term, not one
    of the Sage-local DUOPlus1-7 extensions or "Pending Annotation") and a
    description (the curation text to stamp as skos:scopeNote) -- see this module's
    docstring for why this is derived from the schema rather than hardcoded, and why
    the returned keys are the bare local suffix ("0000007", not "DUO_0000007")."""
    sv = SchemaView(schema_path)
    enum_def = sv.get_enum("DataUseModifierEnum")
    terms = {}
    for pv in enum_def.permissible_values.values():
        if pv.meaning and pv.meaning.startswith("DUO:") and pv.description:
            local_name = pv.meaning.split(":", 1)[1]
            terms[local_name] = pv.description
    return terms


def build(schema_path: str, version: str) -> Graph:
    gen = OwlSchemaGenerator(
        schema_path,
        skip_vacuous_min_zero_cardinality_axioms=True,
        skip_vacuous_local_range_axioms=True,
        consolidate_cardinality_axioms=True,
    )
    ttl = gen.serialize(format="turtle")

    graph = Graph()
    graph.parse(data=ttl, format="turtle")

    ontology_iri = GOVERNANCEDUO_NS["governance_duo"]
    version_iri = URIRef(f"{ontology_iri}/{version}")
    graph.add((ontology_iri, OWL.versionIRI, version_iri))
    graph.add((ontology_iri, OWL.versionInfo, Literal(version)))

    for local_name, description in reused_duo_terms(schema_path).items():
        term = DUO_NS[local_name]
        if (term, None, None) not in graph:
            continue
        graph.add((term, SKOS.scopeNote, Literal(description)))
        graph.add((term, OWL.versionInfo, Literal(version)))

    return graph


def main():
    parser = argparse.ArgumentParser(
        description="Generate an OWL/Turtle build of the governanceDUO LinkML schema."
    )
    parser.add_argument(
        "--schema",
        default="linkml/governance_duo.linkml.yaml",
        help="Path to the umbrella LinkML schema.",
    )
    parser.add_argument(
        "--out",
        default="shapes/governance_duo.owl.ttl",
        help="Path to write the generated Turtle file.",
    )
    parser.add_argument(
        "--version",
        default="0.1.0",
        help="Version stamped as owl:versionIRI/owl:versionInfo.",
    )
    args = parser.parse_args()

    graph = build(args.schema, args.version)
    graph.serialize(destination=args.out, format="turtle")
    print(f"Wrote {len(graph)} triples to {args.out}")


if __name__ == "__main__":
    main()
