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

Generator settings and repairs (plans/sagebrain_contract_and_owl_dl_fixes.md,
decisions D2 and step 13). The output must pass `robot validate-profile --profile
DL` (make owl-profile) and must use the IRIs the data uses, so it can be merged
with shapes/governance_graph.owl.ttl and imported by sagebrain-model:

- use_native_uris=False: classes/properties are emitted under their class_uri/
  slot_uri (prov:Activity, sagegov:wasExecuted, ...), not governanceduo:<name>.
- metaclasses=False, type_objects=False: no linkml:ClassDefinition/SlotDefinition
  typing and no LinkML types-as-classes, which made pattern-constrained slots
  (id, synapseId, the *Key slots) ObjectProperties restricted by xsd:string
  patterns -- illegal property punning in OWL 2 DL.
- `rules:` are removed from the schema before generation. owlgen's
  add_constraints() is called with is_literal=None for rule slot_conditions, so
  every `equals_string` precondition is dropped ("ignoring equals_string ...
  unable to tell if literal") and each rule became "any dataUseModifiers value
  implies <postcondition>" -- wrong entailments, and the source of the remaining
  puns. The rules stay enforced by linkml-validate; they are simply not in the
  OWL (approved decision D2).
- repair_generator_output() fills three owlgen gaps under use_native_uris=False,
  using only the schema (approved as a workaround; remove once fixed upstream):
    1. a slot_usage that gives a slot its own slot_uri (e.g. SynapseEntity.name ->
       sagegov:name) is used in restrictions but never declared -- declared here,
       typed from the induced range;
    2. a slot_usage with no slot_uri of its own (e.g. every per-class `id`
       pattern) is restricted under governanceduo:<name> instead of the slot's
       declared slot_uri (dcterms:identifier) -- retargeted here;
    3. slots mapped onto built-in vocabulary (owl:sameAs) are declared and
       restricted, which OWL 2 DL forbids -- those axioms are left out.
- declare_annotation_properties() declares every annotation predicate the output
  uses (skos:definition, skos:inScheme, ...); owlgen omits the declarations and
  OWL 2 DL requires them.

Usage:
    python scripts/build_owl.py [--schema linkml/governance_duo.linkml.yaml]
                                 [--out shapes/governance_duo.owl.ttl]
                                 [--version 0.1.0]

author: orion.banks
"""

import argparse

from linkml.generators.owlgen import OwlSchemaGenerator
from linkml_runtime.utils.schemaview import SchemaView
from rdflib import BNode, Graph, Namespace, Literal, URIRef
from rdflib.compare import to_canonical_graph
from rdflib.namespace import OWL, RDF, RDFS, SKOS, XSD

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


RESERVED_NAMESPACES = (str(RDF), str(RDFS), str(OWL), str(XSD))
PROPERTY_TYPES = (OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty)


def is_reserved(term) -> bool:
    return isinstance(term, URIRef) and str(term).startswith(RESERVED_NAMESPACES)


def schema_without_rules(schema_path: str) -> SchemaView:
    """The schema with imports merged into one SchemaDefinition and every class's
    `rules` removed -- see module docstring for why rules are not generated."""
    sv = SchemaView(schema_path)
    sv.merge_imports()
    for cls in sv.schema.classes.values():
        cls.rules = []
    sv.set_modified()
    return sv


def remove_node(graph: Graph, node):
    """Removes every triple about `node`, recursing into blank nodes it points at
    (restriction fillers, datatype restrictions, RDF lists)."""
    for p, o in list(graph.predicate_objects(node)):
        graph.remove((node, p, o))
        if isinstance(o, BNode) and not any(graph.subjects(None, o)):
            remove_node(graph, o)


def repair_generator_output(graph: Graph, sv: SchemaView) -> dict:
    """Fills owlgen's slot_usage gaps under use_native_uris=False, from the schema
    alone -- see module docstring. Returns counts of each repair, for the log."""
    declared = {s for t in PROPERTY_TYPES for s in graph.subjects(RDF.type, t)}
    counts = {"declared": 0, "retargeted": 0, "reserved_removed": 0}

    # 1. declare slot_usage slot_uri overrides, typed from the induced range
    for class_name in sv.all_classes():
        for slot_name in sv.class_slots(class_name):
            base = sv.get_slot(slot_name)
            induced = sv.induced_slot(slot_name, class_name)
            if not induced.slot_uri or induced.slot_uri == base.slot_uri:
                continue
            prop = URIRef(sv.expand_curie(induced.slot_uri))
            if prop in declared or is_reserved(prop):
                continue
            is_object = induced.range in sv.all_classes() or induced.range in sv.all_enums()
            graph.add((prop, RDF.type, OWL.ObjectProperty if is_object else OWL.DatatypeProperty))
            graph.add((prop, RDFS.label, Literal(slot_name)))
            declared.add(prop)
            counts["declared"] += 1

    # 2. retarget restrictions owlgen wrote under default_prefix:<slot name>
    default_ns = sv.namespaces()[sv.schema.default_prefix]
    for slot in sv.all_slots().values():
        if not slot.slot_uri:
            continue
        wrong = URIRef(f"{default_ns}{slot.name}")
        right = URIRef(sv.expand_curie(slot.slot_uri))
        if wrong == right or wrong in declared or right not in declared:
            continue
        for restriction in list(graph.subjects(OWL.onProperty, wrong)):
            graph.remove((restriction, OWL.onProperty, wrong))
            graph.add((restriction, OWL.onProperty, right))
            counts["retargeted"] += 1

    # 3. leave out declarations of, and restrictions on, built-in vocabulary
    for restriction in list(graph.subjects(OWL.onProperty, None)):
        if is_reserved(graph.value(restriction, OWL.onProperty)):
            for cls in list(graph.subjects(RDFS.subClassOf, restriction)):
                graph.remove((cls, RDFS.subClassOf, restriction))
            remove_node(graph, restriction)
            counts["reserved_removed"] += 1
    for t in PROPERTY_TYPES:
        for prop in list(graph.subjects(RDF.type, t)):
            if is_reserved(prop):
                remove_node(graph, prop)
                counts["reserved_removed"] += 1
    return counts


def declare_annotation_properties(graph: Graph) -> int:
    """Declares every predicate the output uses that isn't built-in vocabulary or
    an already-declared property as owl:AnnotationProperty. In this output those
    are all annotations (skos:definition, skos:inScheme, skos:exactMatch, ...)."""
    declared = {s for t in PROPERTY_TYPES for s in graph.subjects(RDF.type, t)}
    added = 0
    for predicate in set(graph.predicates()):
        if is_reserved(predicate) or predicate in declared:
            continue
        graph.add((predicate, RDF.type, OWL.AnnotationProperty))
        added += 1
    return added


def stable_graph(graph: Graph) -> Graph:
    """The same graph with blank nodes relabeled canonically (rdflib's RDFC
    canonicalization), so the Turtle serializer -- which orders nested blank nodes
    by label -- writes byte-identical output for identical input and rebuilds stop
    producing reordering-only diffs. Takes ~10 s on this schema's OWL."""
    canonical = Graph()
    for triple in to_canonical_graph(graph):
        canonical.add(triple)
    for prefix, namespace in graph.namespace_manager.namespaces():
        canonical.bind(prefix, namespace, override=True, replace=True)
    return canonical


def build(schema_path: str, version: str) -> Graph:
    sv = schema_without_rules(schema_path)
    gen = OwlSchemaGenerator(
        sv.schema,
        skip_vacuous_min_zero_cardinality_axioms=True,
        skip_vacuous_local_range_axioms=True,
        consolidate_cardinality_axioms=True,
        use_native_uris=False,
        metaclasses=False,
        type_objects=False,
    )
    ttl = gen.serialize(format="turtle")

    graph = Graph()
    graph.parse(data=ttl, format="turtle")

    counts = repair_generator_output(graph, sv)

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

    # last, so annotations added above (skos:scopeNote) are declared too
    counts["annotation_properties"] = declare_annotation_properties(graph)
    print(f"Repairs: {counts}")
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
    stable_graph(graph).serialize(destination=args.out, format="turtle")
    print(f"Wrote {len(graph)} triples to {args.out}")


if __name__ == "__main__":
    main()
