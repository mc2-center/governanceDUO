"""
build_governance_graph.py

Exports the governance_graph.yaml example instances
(linkml/examples/governance_graph/*.example.yaml) as Turtle using the exact `gov:`/
`syn:` predicates and shapes shown in "SageBrain-Governance Graph Design for
Authorization and Access Requirements" — not a generic LinkML-instance-to-RDF dump
(that's what scripts/convert_examples_to_rdf.py already does, in this schema's own
`sagegov:`-prefixed namespace). This script exists specifically to let the output be
compared structurally against the design doc's own snippets, e.g.:

    gov:grant-001
        a gov:AccessGrant ;
        gov:resource syn:syn10081783 ;
        gov:principal gov:Team-X ;
        gov:permission gov:READ, gov:DOWNLOAD ;
        gov:source gov:SynapseACL .

    gov:ar-association-001
        a gov:AccessRequirementAssociation ;
        gov:resource syn:syn10081783 ;
        gov:accessRequirement gov:AR-123 ;
        gov:source gov:Synapse ;
        gov:bindingType gov:Inherited .

The LinkML schema itself registers this same namespace under the prefix `sagegov:`,
not `gov:` — `gov:` collides with a different, canonical prefix
(`http://gov.genealogy.net/ontology.owl#`) that `linkml-lint`'s `canonical_prefixes`
check flagged, the same kind of collision `ebiswo:` (vs. the OBO Foundry `SWO:`)
resolved earlier. `gov:` is safe to use here because this script controls its own
Turtle serialization directly with rdflib, entirely independent of the LinkML
schema's own prefix registry.

A DataAccessSubmission's `gov:hasSignedAgreement`/`gov:hasApproval`-style triple
(the design doc's simplified way of saying "the user has satisfied this
requirement") is only emitted when its DataAccessSubmissionStatus.state is
APPROVED — mirroring the doc's own worked example, where an unapproved submission
means "AR = FAIL" and no such triple should exist yet.

Usage:
    python scripts/build_governance_graph.py [--examples-dir linkml/examples/governance_graph]
                                              [--out governance_graph_export/governance_graph.ttl]

author: orion.banks
"""

import argparse
from pathlib import Path

import yaml
from rdflib import Graph, Literal, Namespace, RDF, XSD
from rdflib.namespace import NamespaceManager

GOV = Namespace("https://sagebionetworks.org/governance/")
SYN = Namespace("https://www.synapse.org/Synapse:")

# file basename (without .example.yaml) -> LinkML class it represents. Same
# manifest-driven pattern as scripts/convert_examples_to_rdf.py's EXAMPLE_CLASSES.
EXAMPLE_CLASSES = {
    "synapse_entity_file": "SynapseEntity",
    "synapse_entity_study": "SynapseEntity",
    "principal_team_x": "Principal",
    "principal_user_2000001": "Principal",
    "access_grant": "AccessGrant",
    "access_requirement_association": "AccessRequirementAssociation",
    "data_access_submission": "DataAccessSubmission",
    "data_access_submission_status": "DataAccessSubmissionStatus",
}


def gov_id(value: str):
    """governanceDUO ids are dotted/underscored (e.g. `grant.001`,
    `ar_association.001`); the design doc's own ids are fully hyphenated
    (`gov:grant-001`, `gov:ar-association-001`). Convert both separators for a
    structurally faithful comparison against the doc's literal snippets."""
    return GOV[value.replace(".", "-").replace("_", "-")]


# Literal SynapseEntity slots emitted as-is (auto-typed by rdflib from the YAML's own
# Python type); createdBy/createdOn are handled separately below (createdBy as
# gov:createdByUserId -- see note in add_synapse_entity -- and createdOn to match the
# xsd:long datatype used for every other class's createdOn), and parentId is an IRI
# reference, not a literal.
SYNAPSE_ENTITY_LITERAL_SLOTS = (
    "name",
    "nodeType",
    "alias",
    "currentRevNum",
    "maxRevNum",
    "etag",
)


def add_synapse_entity(g: Graph, data: dict):
    subject = SYN[data["id"]]
    # Every SynapseEntity gets an explicit rdf:type, even one with no parentId of its
    # own (e.g. a top-level project) -- otherwise a node referenced only as another
    # entity's parentId (like syn2343195 below) would have no triples of its own and
    # be untargetable by a class-based SHACL shape.
    g.add((subject, RDF.type, GOV.SynapseEntity))
    for slot in SYNAPSE_ENTITY_LITERAL_SLOTS:
        if data.get(slot) is not None:
            g.add((subject, GOV[slot], Literal(data[slot])))
    if data.get("createdBy") is not None:
        # gov:createdByUserId, not gov:createdBy: the latter is reserved for IRI
        # references to a gov:Principal node (see add_data_access_submission and
        # add_data_access_submission_status) -- this is a raw NODE.CREATED_BY id with
        # no corresponding Principal record required.
        g.add((subject, GOV.createdByUserId, Literal(data["createdBy"])))
    if data.get("createdOn") is not None:
        g.add((subject, GOV.createdOn, Literal(data["createdOn"], datatype=XSD.long)))
    if data.get("parentId"):
        g.add((subject, GOV.parentId, SYN[data["parentId"]]))


def add_principal(g: Graph, data: dict):
    # Principals have no BaseEntity id in this schema (see governance_graph.yaml's
    # own note on Principal) -- mint a stable node from principalId directly.
    subject = GOV[f"principal-{data['principalId']}"]
    # Asserted explicitly alongside the Team/User subtype below, rather than relying
    # solely on shapes/governance_graph.owl.ttl's rdfs:subClassOf declarations -- a
    # plain SPARQL query for `?x a gov:Principal` (or any tool that doesn't load that
    # TBox and do subclass entailment) should still find every Principal individual.
    g.add((subject, RDF.type, GOV.Principal))
    g.add((subject, RDF.type, GOV[data["principalType"]]))
    g.add((subject, GOV.principalId, Literal(data["principalId"])))
    return subject


def add_access_grant(g: Graph, data: dict, principal_node):
    subject = gov_id(data["id"])
    g.add((subject, RDF.type, GOV.AccessGrant))
    g.add((subject, GOV.resource, SYN[data["resource"]]))
    g.add((subject, GOV.principal, principal_node))
    for perm in data.get("permission", []):
        g.add((subject, GOV.permission, GOV[perm]))
    g.add((subject, GOV.source, GOV[data["source"]]))
    g.add((subject, GOV.bindingType, GOV[data["bindingType"]]))
    if data.get("createdOn") is not None:
        g.add((subject, GOV.createdOn, Literal(data["createdOn"], datatype=XSD.long)))
    if data.get("sourceAclId") is not None:
        g.add((subject, GOV.sourceAclId, Literal(data["sourceAclId"])))
    if data.get("sourceAclResourceAccessId") is not None:
        g.add(
            (
                subject,
                GOV.sourceAclResourceAccessId,
                Literal(data["sourceAclResourceAccessId"]),
            )
        )
    # design doc: "syn10081783 -- hasACL --> ACL:syn10081783 -- (grants) --> ...";
    # this repo's AccessGrant *is* the grant record itself, so the derived
    # convenience triple points hasACL directly at it.
    g.add((SYN[data["resource"]], GOV.hasACL, subject))


def add_access_requirement_association(g: Graph, data: dict):
    subject = gov_id(data["id"])
    ar_node = GOV[data["accessRequirement"].replace("access_requirement.", "AR-")]
    g.add((subject, RDF.type, GOV.AccessRequirementAssociation))
    g.add((subject, GOV.resource, SYN[data["resource"]]))
    g.add((subject, GOV.accessRequirement, ar_node))
    g.add((subject, GOV.source, GOV[data["source"]]))
    g.add((subject, GOV.bindingType, GOV[data["bindingType"]]))
    g.add((SYN[data["resource"]], GOV.hasAccessRequirement, ar_node))
    g.add((ar_node, RDF.type, GOV.AccessRequirement))
    return ar_node


def add_data_access_submission(g: Graph, data: dict, ar_node, approved: bool):
    subject = gov_id(data["id"])
    g.add((subject, RDF.type, GOV.DataAccessSubmission))
    g.add((subject, GOV.accessRequirement, ar_node))
    g.add((subject, GOV.createdBy, GOV[f"principal-{data['createdBy']}"]))
    g.add((subject, GOV.createdOn, Literal(data["createdOn"], datatype=XSD.long)))
    if approved:
        # Mirrors the design doc's simplified gov:hasApproval predicate -- only
        # emitted once the real, richer submission-status workflow (below) says
        # APPROVED, not merely SUBMITTED.
        g.add((GOV[f"principal-{data['createdBy']}"], GOV.hasApproval, ar_node))


def add_data_access_submission_status(g: Graph, data: dict, submission_node) -> bool:
    # DataAccessSubmissionStatus has no independent node of its own (see
    # governance_graph.yaml) -- its state/reason/audit fields are merged onto the
    # DataAccessSubmission subject. Its own createdBy/modifiedBy use the distinct
    # gov:statusCreatedBy/gov:statusModifiedBy predicates (IRI references to a
    # Principal node, mirroring add_data_access_submission's gov:createdBy) rather
    # than gov:createdBy itself: DataAccessSubmission.createdBy already occupies that
    # predicate on this same subject, and the status row's creator/modifier can
    # legitimately be a different Principal (e.g. an ACT reviewer, not the requester).
    g.add((submission_node, GOV.state, GOV[data["state"]]))
    if data.get("reason"):
        g.add((submission_node, GOV.reason, Literal(data["reason"])))
    if data.get("createdBy") is not None:
        g.add(
            (submission_node, GOV.statusCreatedBy, GOV[f"principal-{data['createdBy']}"])
        )
    if data.get("createdOn") is not None:
        g.add(
            (submission_node, GOV.statusCreatedOn, Literal(data["createdOn"], datatype=XSD.long))
        )
    if data.get("modifiedBy") is not None:
        g.add(
            (submission_node, GOV.statusModifiedBy, GOV[f"principal-{data['modifiedBy']}"])
        )
    if data.get("modifiedOn") is not None:
        g.add(
            (submission_node, GOV.statusModifiedOn, Literal(data["modifiedOn"], datatype=XSD.long))
        )
    return data["state"] == "APPROVED"


def main():
    parser = argparse.ArgumentParser(
        description="Export governance_graph example instances as design-doc-shaped gov:/syn: Turtle."
    )
    parser.add_argument("--examples-dir", default="linkml/examples/governance_graph")
    parser.add_argument("--out", default="governance_graph_export/governance_graph.ttl")
    args = parser.parse_args()

    examples_dir = Path(args.examples_dir)
    instances = {}
    for stem, class_name in EXAMPLE_CLASSES.items():
        path = examples_dir / f"{stem}.example.yaml"
        if path.exists():
            instances[stem] = (class_name, yaml.safe_load(path.read_text()))

    g = Graph()
    g.namespace_manager = NamespaceManager(g, bind_namespaces="none")
    g.bind("gov", GOV)
    g.bind("syn", SYN)

    for stem, (class_name, data) in instances.items():
        if class_name == "SynapseEntity":
            add_synapse_entity(g, data)

    principal_nodes = {}
    for stem, (class_name, data) in instances.items():
        if class_name == "Principal":
            principal_nodes[data["principalId"]] = add_principal(g, data)

    ar_node = None
    for stem, (class_name, data) in instances.items():
        if class_name == "AccessGrant":
            add_access_grant(g, data, principal_nodes[data["principal"]])
        elif class_name == "AccessRequirementAssociation":
            ar_node = add_access_requirement_association(g, data)

    submission_node = None
    for stem, (class_name, data) in instances.items():
        if class_name == "DataAccessSubmission":
            submission_node = gov_id(data["id"])

    approved = False
    for stem, (class_name, data) in instances.items():
        if class_name == "DataAccessSubmissionStatus" and submission_node is not None:
            approved = add_data_access_submission_status(g, data, submission_node)

    for stem, (class_name, data) in instances.items():
        if class_name == "DataAccessSubmission" and ar_node is not None:
            add_data_access_submission(g, data, ar_node, approved)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=str(out_path), format="turtle")
    print(f"Wrote {len(g)} triples to {out_path}")


if __name__ == "__main__":
    main()
