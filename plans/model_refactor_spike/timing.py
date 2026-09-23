import time
from pyshacl import validate
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF
ACL = Namespace("http://www.w3.org/ns/auth/acl#"); GOV = Namespace("https://w3id.org/synapse/governance#")
SYN = Namespace("https://www.synapse.org/Synapse:")
ont = Graph().parse("spike.owl.ttl"); shapes = Graph().parse("spike.shacl.ttl")

def run(data, label):
    t = time.time()
    ok, _, text = validate(data, shacl_graph=shapes, ont_graph=ont, advanced=True)
    print(f"{label}: conforms={ok} {time.time()-t:.2f}s")
    return ok, text

base = Graph().parse("data.ttl")
run(base, "fixture")

bad = Graph().parse("data.ttl")
a = URIRef("https://w3id.org/synapse/governance/authorization/syn50000000-3000001")
bad.add((a, ACL.mode, GOV.Bogus))
ok, text = run(bad, "bogus mode")
assert not ok and "Bogus" in text

big = Graph().parse("data.ttl")
for i in range(5000):
    s = URIRef(f"https://w3id.org/synapse/governance/authorization/b{i}")
    e = SYN[f"syn6{i:07d}"]
    big.add((e, RDF.type, GOV.SynapseEntity))
    big.add((s, RDF.type, ACL.Authorization)); big.add((s, ACL.accessTo, e))
    big.add((s, ACL.agent, URIRef("https://www.synapse.org/Profile:3000001")))
    big.add((s, ACL.mode, GOV.Read)); big.add((s, ACL.mode, GOV.Download))
run(big, f"5000 authorizations ({len(big)} triples)")
