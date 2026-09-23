"""Spike: owlgen subclass that emits enums marked `implements: [skos:Concept]` as
SKOS vocabularies (sagebrain-model's pattern) instead of a union of classes."""
import sys
from linkml.generators.owlgen import OwlSchemaGenerator
from rdflib import Literal, URIRef
from rdflib.collection import Collection
from rdflib.namespace import OWL, RDF, RDFS, SKOS

SKOS_CONCEPT = "skos:Concept"


class SkosOwlGenerator(OwlSchemaGenerator):
    def is_vocabulary(self, enum_def):
        return SKOS_CONCEPT in (enum_def.implements or [])

    def add_enum(self, e):
        if not self.is_vocabulary(e):
            return super().add_enum(e)
        sv = self.schemaview
        g = self.graph
        concept_class = URIRef(sv.expand_curie(e.enum_uri))
        scheme = URIRef(str(concept_class) + "Scheme")
        g.add((concept_class, RDF.type, OWL.Class))
        g.add((concept_class, RDFS.subClassOf, SKOS.Concept))
        g.add((concept_class, RDFS.label, Literal(e.name)))
        if e.description:
            g.add((concept_class, SKOS.definition, Literal(e.description)))
        g.add((scheme, RDF.type, SKOS.ConceptScheme))
        g.add((scheme, RDFS.label, Literal(f"{e.name} scheme")))
        for text, pv in e.permissible_values.items():
            value = URIRef(sv.expand_curie(pv.meaning))
            g.add((value, RDF.type, concept_class))
            g.add((value, SKOS.prefLabel, Literal(pv.title or text)))
            g.add((value, SKOS.notation, Literal(text)))
            g.add((value, SKOS.inScheme, scheme))
            g.add((scheme, SKOS.hasTopConcept, value))
            if pv.description:
                g.add((value, SKOS.definition, Literal(pv.description)))
            for mode in pv.implements or []:
                # WAC: a custom access mode is a subclass of an acl mode (punned:
                # the same IRI is a class and a concept individual).
                g.add((value, RDF.type, OWL.Class))
                g.add((value, RDFS.subClassOf, URIRef(sv.expand_curie(mode))))


if __name__ == "__main__":
    print(SkosOwlGenerator(sys.argv[1], type_objects=False, metaclasses=False).serialize())
