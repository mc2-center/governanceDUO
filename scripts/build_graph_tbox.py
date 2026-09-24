"""
build_graph_tbox.py

Generates the governance graph layer's one TBox and one shape set from
linkml/graph/governance.yaml (plans/model_refactor.md, Phase 1):

    shapes/governance.owl.ttl     OWL 2 DL; what sagebrain-model imports
    shapes/governance.shacl.ttl   SHACL; what every graph export is validated against

Both come from LinkML's own generators (owlgen, shaclgen). This script only
applies the layer's conventions to their output:

- Vocabularies. An enum that `implements: [skos:Concept]` becomes a SKOS
  vocabulary, sagebrain-model's pattern: its enum_uri is a concept class
  (rdfs:subClassOf skos:Concept), <enum_uri>Scheme is a skos:ConceptScheme, and
  each value is a concept of that class with skos:prefLabel, skos:notation (the
  permissible value's text, i.e. the Synapse or source code), skos:definition,
  skos:inScheme and, when the value has a `rank`, gov:rank. A value's
  `implements:` becomes rdfs:subClassOf: a Web Access Control access mode is a
  subclass of acl:Access (WAC's extension mechanism), so a permission is both a
  concept and a class, which OWL 2 DL allows (punning).
- Class-valued enums. An enum that `implements: [owl:Class]` lists classes used
  as values (DUO terms, WAC agent classes). It gets no class of its own. Its
  gov: values are declared as classes under their `implements:` (DUOPlus terms
  under DUO:0000017); external values are only declared.
- Terms outside gov: get declarations only. The OWL never makes axioms about
  another vocabulary's terms (acl:Authorization, vcard:Group, prov:Activity,
  DUO classes); the SHACL carries every constraint on them. A reused term does
  get one annotation, skos:scopeNote, whenever this schema itself wrote a
  description for it (a class whose class_uri is external, e.g. Team's
  vcard:Group, or a permissible value's own `description`, e.g. a DUO term or
  AgentClass's PUBLIC/AUTHENTICATED_USERS) -- scopeNote is SKOS's own
  "how this vocabulary uses the concept" annotation, not a definition, so it
  doesn't claim to give the term its meaning.
- Every gov: term (class, property, vocabulary concept and concept scheme, and
  a gov: value of a class-valued enum) gets owl:versionInfo, the schema's own
  version -- not just the ontology header.
- The identifier slot is the subject, not a property, and the GovernanceGraph
  container is not graph content. Both are left out.
- IRI-valued slots (range uriorcurie/uri) are object properties.
- Every gov: property gets rdfs:range and rdfs:domain (a union when several
  classes use it) from the schema. Neptune doesn't infer, so these document the
  graph and feed the DL check; they can't disagree with the data, because the
  data is validated against closed shapes generated from the same schema.
- Shapes are named in their own namespace, <ns>shapes#<Class>Shape, not after
  the class they target.

Usage:
    python scripts/build_graph_tbox.py [--schema linkml/graph/governance.yaml]
        [--owl shapes/governance.owl.ttl] [--shacl shapes/governance.shacl.ttl]
        [--version 0.2.0]

author: orion.banks
"""

import argparse

from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.shaclgen import ShaclGenerator
from linkml_runtime.utils.schemaview import SchemaView
from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import OWL, RDF, RDFS, SH, SKOS, XSD

from build_owl import declare_annotation_properties, is_reserved, remove_node, stable_graph

GOV = Namespace("https://w3id.org/synapse/governance#")
SHAPES = Namespace("https://w3id.org/synapse/governance/shapes#")
CONTAINER = "GovernanceGraph"
IDENTIFIER = "id"
VOCABULARY = "skos:Concept"
CLASS_VALUED = "owl:Class"
IRI_RANGES = {"uriorcurie", "uri"}
DECLARATION_TYPES = (OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty)
XSD_FOR = {
    "string": XSD.string, "integer": XSD.integer, "boolean": XSD.boolean,
    "datetime": XSD.dateTime, "date": XSD.date, "float": XSD.float, "double": XSD.double,
}


def is_gov(term) -> bool:
    return isinstance(term, URIRef) and str(term).startswith(str(GOV))


class GraphLayer:
    """The schema facts the post-processing needs, resolved once."""

    def __init__(self, schema_path: str):
        self.sv = SchemaView(schema_path)
        self.sv.merge_imports()
        sv = self.sv
        self.enums = sv.all_enums()
        self.vocabularies = {n: e for n, e in self.enums.items() if VOCABULARY in (e.implements or [])}
        self.class_valued = {n: e for n, e in self.enums.items() if CLASS_VALUED in (e.implements or [])}
        # Classes that are graph content: all but the container and Node, the
        # abstract root that only carries the identifier (no class_uri of its own).
        self.graph_class_names = [
            n for n, c in sv.all_classes().items()
            if n != CONTAINER and not (c.abstract and not c.class_uri)
        ]
        # every slot, with the concrete classes that use it
        self.usage = {}
        for class_name in self.graph_class_names:
            for slot in sv.class_induced_slots(class_name):
                if slot.name == IDENTIFIER:
                    continue
                self.usage.setdefault(slot.name, (slot, set()))[1].add(class_name)

    def uri(self, curie: str) -> URIRef:
        return URIRef(self.sv.expand_curie(curie))

    def class_uri(self, name: str) -> URIRef:
        return URIRef(self.sv.get_uri(self.sv.get_class(name), expand=True))

    def enum_class(self, name: str):
        e = self.enums[name]
        return self.uri(e.enum_uri) if e.enum_uri else None

    def slot_uri(self, slot) -> URIRef:
        return URIRef(self.sv.get_uri(slot, expand=True))


def add_vocabulary(g: Graph, layer: GraphLayer, name: str, e, version: str) -> None:
    concept_class = layer.uri(e.enum_uri)
    scheme = URIRef(f"{concept_class}Scheme")
    g.add((concept_class, RDF.type, OWL.Class))
    g.add((concept_class, RDFS.subClassOf, SKOS.Concept))
    g.add((concept_class, RDFS.label, Literal(name)))
    g.add((concept_class, OWL.versionInfo, Literal(version)))
    if e.description:
        g.add((concept_class, SKOS.definition, Literal(e.description)))
    g.add((scheme, RDF.type, SKOS.ConceptScheme))
    g.add((scheme, RDFS.label, Literal(f"{name} scheme")))
    g.add((scheme, OWL.versionInfo, Literal(version)))
    for text, pv in e.permissible_values.items():
        concept = layer.uri(pv.meaning)
        g.add((concept, RDF.type, concept_class))
        g.add((concept, SKOS.prefLabel, Literal(pv.title or text)))
        g.add((concept, SKOS.notation, Literal(text)))
        g.add((concept, SKOS.inScheme, scheme))
        g.add((scheme, SKOS.hasTopConcept, concept))
        if is_gov(concept):
            g.add((concept, OWL.versionInfo, Literal(version)))
        if pv.description:
            existing = g.value(concept, SKOS.definition)
            if existing is not None and str(existing) != pv.description:
                raise SystemExit(f"{pv.meaning} is shared by several vocabularies with different descriptions")
            g.add((concept, SKOS.definition, Literal(pv.description)))
        if pv.rank is not None:
            g.add((concept, GOV.rank, Literal(pv.rank, datatype=XSD.integer)))
        for parent in pv.implements or []:
            g.add((concept, RDF.type, OWL.Class))
            g.add((concept, RDFS.subClassOf, layer.uri(parent)))


def add_class_valued(g: Graph, layer: GraphLayer, e, version: str) -> None:
    for text, pv in e.permissible_values.items():
        value = layer.uri(pv.meaning)
        g.add((value, RDF.type, OWL.Class))
        if not is_gov(value):
            # A reused term: not ours to label or define, but its own
            # description here is this schema's own note on how it's used.
            if pv.description:
                g.add((value, SKOS.scopeNote, Literal(pv.description)))
            continue
        g.add((value, RDFS.label, Literal(pv.title or text)))
        g.add((value, OWL.versionInfo, Literal(version)))
        if pv.description:
            g.add((value, SKOS.definition, Literal(pv.description)))
        for parent in pv.implements or []:
            parent_uri = layer.uri(parent)
            g.add((value, RDFS.subClassOf, parent_uri))
            g.add((parent_uri, RDF.type, OWL.Class))


def class_expression(g: Graph, classes: list) -> URIRef | BNode:
    if len(classes) == 1:
        return classes[0]
    union = BNode()
    g.add((union, RDF.type, OWL.Class))
    members = BNode()
    Collection(g, members, sorted(classes))
    g.add((union, OWL.unionOf, members))
    return union


def range_of(g: Graph, layer: GraphLayer, slot):
    """(owl property type, rdfs:range or None) for a slot."""
    r = slot.range
    if r in layer.sv.all_classes():
        return OWL.ObjectProperty, layer.class_uri(r)
    if r in layer.vocabularies:
        return OWL.ObjectProperty, layer.enum_class(r)
    if r in layer.class_valued:
        return OWL.ObjectProperty, None
    if r in IRI_RANGES:
        return OWL.ObjectProperty, None
    return OWL.DatatypeProperty, XSD_FOR.get(r, XSD.string)


def build_owl(layer: GraphLayer, version: str) -> Graph:
    gen = OwlSchemaGenerator(
        layer.sv.schema,
        metaclasses=False,
        type_objects=False,
        use_native_uris=False,
        skip_vacuous_min_zero_cardinality_axioms=True,
        skip_vacuous_local_range_axioms=True,
        consolidate_cardinality_axioms=True,
    )
    raw = Graph().parse(data=gen.serialize(format="turtle"), format="turtle")

    g = Graph()
    for prefix, ns in raw.namespace_manager.namespaces():
        g.bind(prefix, ns, override=True, replace=True)
    ontology = URIRef(layer.sv.schema.id)
    g.add((ontology, RDF.type, OWL.Ontology))
    g.add((ontology, RDFS.label, Literal(layer.sv.schema.title)))
    g.add((ontology, SKOS.definition, Literal(layer.sv.schema.description.strip())))
    g.add((ontology, OWL.versionIRI, URIRef(f"{ontology}/{version}")))
    g.add((ontology, OWL.versionInfo, Literal(version)))

    # Classes: gov: classes keep owlgen's label/definition and gain their gov:
    # superclass; everything else is declared only. owlgen's cardinality and
    # range restrictions aren't kept -- the SHACL carries those constraints.
    for name in layer.graph_class_names:
        cls = layer.class_uri(name)
        g.add((cls, RDF.type, OWL.Class))
        if not is_gov(cls):
            # A reused class_uri (Team's vcard:Group, Activity's prov:Activity,
            # ...): not ours to label or define, but this schema's own
            # description of it, if it wrote one, is our note on how we use it.
            description = layer.sv.get_class(name).description
            if description:
                g.add((cls, SKOS.scopeNote, Literal(description.strip())))
            continue
        for p in (RDFS.label, SKOS.definition, SKOS.closeMatch, SKOS.exactMatch):
            for o in raw.objects(cls, p):
                if o != cls:
                    g.add((cls, p, o))
        g.add((cls, OWL.versionInfo, Literal(version)))
        parent = layer.sv.get_class(name).is_a
        if parent in layer.graph_class_names:
            g.add((cls, RDFS.subClassOf, layer.class_uri(parent)))

    # Properties: one per slot_uri, typed from the range; gov: ones get
    # label, definition, domain and range.
    for slot_name, (slot, owners) in sorted(layer.usage.items()):
        prop = layer.slot_uri(slot)
        owl_type, rng = range_of(g, layer, slot)
        g.add((prop, RDF.type, owl_type))
        if not is_gov(prop):
            # A reused property (vcard:hasMember, ...): same scopeNote
            # treatment as a reused class, keyed on the slot's own description.
            if slot.description:
                g.add((prop, SKOS.scopeNote, Literal(slot.description.strip())))
            continue
        g.add((prop, RDFS.label, Literal(slot_name)))
        g.add((prop, OWL.versionInfo, Literal(version)))
        if slot.description:
            g.add((prop, SKOS.definition, Literal(slot.description.strip())))
        if rng is not None:
            g.add((prop, RDFS.range, rng))
        domain = [layer.class_uri(c) for c in owners if not layer.sv.get_class(c).abstract]
        if domain:
            g.add((prop, RDFS.domain, class_expression(g, domain)))

    for name, e in layer.vocabularies.items():
        add_vocabulary(g, layer, name, e, version)
    for e in layer.class_valued.values():
        add_class_valued(g, layer, e, version)
    if (None, GOV.rank, None) in g:
        g.add((GOV.rank, RDF.type, OWL.DatatypeProperty))
        g.add((GOV.rank, RDFS.label, Literal("rank")))
        g.add((GOV.rank, OWL.versionInfo, Literal(version)))
        g.add((GOV.rank, SKOS.definition, Literal("A concept's position in its scheme's order.")))
        g.add((GOV.rank, RDFS.range, XSD.integer))

    # external classes a gov: axiom or typing points at (skos:Concept,
    # skos:ConceptScheme, acl:Access, DUO:0000017), which OWL 2 DL requires declared
    for o in set(g.objects(None, RDFS.subClassOf)) | set(g.objects(None, RDF.type)):
        if isinstance(o, URIRef) and not is_reserved(o):
            g.add((o, RDF.type, OWL.Class))
    declare_annotation_properties(g)
    return g


def add_exactly_one_of(g: Graph, layer: GraphLayer, class_name: str, shape) -> None:
    """shaclgen leaves out exactly_one_of. Each alternative here is a set of
    required slots, so the constraint is sh:xone over "has those slots" --
    but "has those slots" alone only checks each branch's own minCount, not
    that the OTHER branches' slots are absent. A node that sets one
    alternative's required slot(s) plus another alternative's slot still
    satisfies exactly one sh:property group's minCount, so sh:xone reports
    exactly one match and passes, even though it straddles two alternatives.
    That's not "exactly one": the hand-written pre-refactor sh:xone this
    generator replaced also forbade a branch's slots from appearing under a
    different branch, and that mutual exclusion was lost in the rewrite. So
    each alternative's property-shape group also gets sh:maxCount 0 on every
    slot that belongs to one of the OTHER alternatives in the group."""
    for group in [layer.sv.get_class(class_name).exactly_one_of or []]:
        if not group:
            continue
        alternative_slots = []
        for alternative in group:
            required = [n for n, cond in (alternative.slot_conditions or {}).items() if cond.required]
            if not required or len(required) != len(alternative.slot_conditions):
                raise SystemExit(f"{class_name}: exactly_one_of alternatives must be required slots")
            alternative_slots.append(required)
        all_slots = {n for required in alternative_slots for n in required}

        alternatives = []
        for required in alternative_slots:
            node = BNode()
            for slot_name in required:
                prop = BNode()
                g.add((prop, SH.path, layer.slot_uri(layer.sv.get_slot(slot_name))))
                g.add((prop, SH.minCount, Literal(1)))
                g.add((node, SH.property, prop))
            for slot_name in sorted(all_slots - set(required)):
                prop = BNode()
                g.add((prop, SH.path, layer.slot_uri(layer.sv.get_slot(slot_name))))
                g.add((prop, SH.maxCount, Literal(0)))
                g.add((node, SH.property, prop))
            alternatives.append(node)
        members = BNode()
        Collection(g, members, alternatives)
        g.add((shape, SH.xone, members))


def build_shacl(layer: GraphLayer) -> Graph:
    raw = Graph().parse(data=ShaclGenerator(layer.sv.schema).serialize(), format="turtle")
    g = Graph()
    for prefix, ns in raw.namespace_manager.namespaces():
        g.bind(prefix, ns, override=True, replace=True)
    g.bind("shape", SHAPES)

    # Shapes are renamed where they're subjects or sh:node targets; sh:class and
    # sh:targetClass keep the class IRI.
    rename = {}
    for name in layer.sv.all_classes():
        cls = layer.class_uri(name)
        if (cls, RDF.type, SH.NodeShape) in raw:
            rename[cls] = SHAPES[f"{name}Shape"]
    for s, p, o in raw:
        g.add((rename.get(s, s), p, rename.get(o, o) if p == SH.node else o))

    # Not graph content, or no instances of their own: the container, Node and
    # other abstract classes (Agent).
    for name, c in layer.sv.all_classes().items():
        if name == CONTAINER or c.abstract:
            shape = SHAPES[f"{name}Shape"]
            for prop in list(g.objects(shape, SH.property)):
                remove_node(g, prop)
            remove_node(g, shape)

    for name in layer.graph_class_names:
        shape = SHAPES[f"{name}Shape"]
        if (shape, RDF.type, SH.NodeShape) not in g:
            continue
        for prop in list(g.objects(shape, SH.property)):
            if g.value(prop, SH.path) == GOV[IDENTIFIER]:
                g.remove((shape, SH.property, prop))
                remove_node(g, prop)
        # every graph node is an IRI
        g.add((shape, SH.nodeKind, SH.IRI))
        # shaclgen writes this list in set order; sort it so rebuilds are byte-stable
        ignored = g.value(shape, SH.ignoredProperties)
        if ignored is not None:
            members = sorted(Collection(g, ignored))
            Collection(g, ignored).clear()
            g.remove((shape, SH.ignoredProperties, ignored))
            fresh = BNode()
            Collection(g, fresh, members)
            g.add((shape, SH.ignoredProperties, fresh))
        add_exactly_one_of(g, layer, name, shape)
    return g


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--schema", default="linkml/graph/governance.yaml")
    parser.add_argument("--owl", default="shapes/governance.owl.ttl")
    parser.add_argument("--shacl", default="shapes/governance.shacl.ttl")
    parser.add_argument("--version", default="0.2.0")
    args = parser.parse_args()

    layer = GraphLayer(args.schema)
    owl = build_owl(layer, args.version)
    stable_graph(owl).serialize(destination=args.owl, format="turtle")
    print(f"Wrote {len(owl)} triples to {args.owl}")
    shacl = build_shacl(layer)
    stable_graph(shacl).serialize(destination=args.shacl, format="turtle")
    print(f"Wrote {len(shacl)} triples to {args.shacl}")


if __name__ == "__main__":
    main()
