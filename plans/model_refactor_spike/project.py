from rdflib import Graph, URIRef, Namespace
GOV = Namespace("https://w3id.org/synapse/governance#")
SYN = Namespace("https://www.synapse.org/Synapse:")
canon = Graph().parse("data.ttl")
canon.add((SYN.syn50000000, GOV.benefactor, SYN.syn50000000))
canon.add((SYN.syn50000001, GOV.benefactor, SYN.syn50000000))
g = canon + Graph().parse("spike.owl.ttl")
proj = g.query(open("authorizer_v1.rq").read()).graph + g.query(open("authorizer_v1_teams.rq").read()).graph
proj.bind("gov", "https://sagebionetworks.org/governance/")
print(proj.serialize(format="turtle"))
q = open("/Users/obanks/mc2-center/governanceDUO/tests/infra_contract/authorize_query.rq").read()
for ent in ("syn50000000", "syn50000001"):
    rows = proj.query(q.replace("{resource_iri}", str(SYN[ent])))
    print(ent, sorted((str(r.grantPrincipal).rsplit("/",1)[-1], str(r.permission).rsplit("/",1)[-1], str(r.bindingType).rsplit("/",1)[-1]) for r in rows))
