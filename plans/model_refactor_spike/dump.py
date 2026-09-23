from linkml_runtime.loaders import yaml_loader
from linkml_runtime.dumpers import rdflib_dumper
from linkml_runtime.utils.schemaview import SchemaView
from linkml.generators.pythongen import PythonGenerator
mod = PythonGenerator("spike.yaml").compile_module()
sv = SchemaView("spike.yaml")
obj = yaml_loader.load("data.yaml", target_class=mod.Graph)
g = rdflib_dumper.as_rdf_graph(obj, schemaview=sv)
# the Graph container is a tree root, not graph content
from rdflib import BNode
for s in {s for s in g.subjects() if isinstance(s, BNode)}:
    g.remove((s, None, None))
g.bind("gov", "https://w3id.org/synapse/governance#")
g.serialize("data.ttl", format="turtle")
print(g.serialize(format="turtle"))
