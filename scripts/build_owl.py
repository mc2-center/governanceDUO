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

Usage:
    python scripts/build_owl.py [--schema linkml/governance_duo.linkml.yaml]
                                 [--out governance_duo.owl.ttl]
                                 [--version 0.1.0]

author: orion.banks
"""

import argparse

from linkml.generators.owlgen import OwlSchemaGenerator
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import OWL, RDFS, SKOS

# Real DUO terms this schema reuses by IRI (obo:DUO_<local>), with the description
# already carried on the matching DataUseModifierEnum permissible_value in
# linkml/mixins.yaml. Kept as a plain list here rather than re-parsed from the schema,
# since these are exactly the 8 terms this repo has authored curation text for.
REUSED_DUO_TERMS = {
    "DUO_0000007": (
        "Disease Specific Research - This data use permission indicates that use is "
        "allowed provided it is related to the specified disease. If providing this "
        "term, please provide the disease MONDO ID(s) in column diseaseSpecificResearch."
    ),
    "DUO_0000012": (
        "Research Specific Restrictions - This data use modifier indicates that use "
        "is limited to studies of a certain research type. If providing this term, "
        "please note the research type(s) in column researchSpecificRestrictions."
    ),
    "DUO_0000020": (
        "Collaboration Required - This data use modifier indicates that the "
        "requestor must agree to collaboration with the primary study "
        "investigator(s). If providing this term, please note the contact email in "
        "column collaborationRequired."
    ),
    "DUO_0000022": (
        "Geographical Restriction - This data use modifier indicates that use is "
        "limited to within a specific geographic region. If providing this term, "
        "please provide the applicable country code(s) in column "
        "geographicalRestriction."
    ),
    "DUO_0000024": (
        "Publication Moratorium - This data use modifier indicates that requestor "
        "agrees not to publish results of studies until a specific date. If "
        "providing this term, please provide the date in column "
        "publicationMoratorium."
    ),
    "DUO_0000025": (
        "Time Limit on Use - This data use modifier indicates that use is approved "
        "for a specific number of months. If providing this term, please provide the "
        "number of months in column timeLimitOnUse."
    ),
    "DUO_0000026": (
        "User Specific Restriction - This data use modifier indicates that use is "
        "limited to use by approved users. If providing this term, please describe "
        "the restrictions in column userSpecificRestriction."
    ),
    "DUO_0000028": (
        "Institution Specific Restriction - This data use modifier indicates that "
        "use is limited to use within an approved institution. If providing this "
        "term, please provide the institution ROR ID(s) in column "
        "institutionSpecificRestriction."
    ),
}

DUO_NS = Namespace("http://purl.obolibrary.org/obo/DUO_")
GOVERNANCEDUO_NS = Namespace("https://w3id.org/sage-bionetworks/governance-duo/")


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

    for local_name, description in REUSED_DUO_TERMS.items():
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
        default="governance_duo.owl.ttl",
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
