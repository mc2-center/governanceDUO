"""
build_governance_graph.py

Exports the governance_graph.yaml example instances
(linkml/examples/governance_graph/*.example.yaml) as Turtle using the `gov:`/`syn:`
predicates and shapes shown in "SageBrain-Governance Graph Design for Authorization
and Access Requirements". Every predicate/class URI this script emits is resolved
from governance_graph.yaml's own `class_uri`/`slot_uri` declarations (via
SchemaView.induced_slot()/get_class(), see PREDICATE()/TYPE() below) rather than
hardcoded as independent Python constants — so if the schema's URI for a class/slot
changes, this script's output follows automatically instead of silently drifting out
of sync with the schema (the two used to be maintained as two disconnected sources of
truth). This is *not*, however, a generic LinkML-instance-to-RDF dump (that's what
scripts/convert_examples_to_rdf.py does, for the governanceduo: namespace) — the
control flow below (which triples get emitted, in what order, and several
schema-undeclarable decisions) stays explicit and hand-written, because a generic
dump cannot reproduce it:

  - Principal individuals are identified by a bare integer (principalId) with no
    BaseEntity `id` slot at all, so their subject URIs (`gov:principal-<n>`) are
    minted directly from that integer, not via any CURIE-from-a-dotted-id mechanism.
  - `gov:hasApproval` is emitted only when a cross-object join holds
    (DataAccessSubmissionStatus.state == APPROVED) — this is join logic, not a
    per-slot mapping.
  - `gov:hasACL`/`gov:hasAccessRequirement` are derived convenience triples with no
    corresponding governance_graph.yaml slot at all.
  - `gov:AR-<n> owl:sameAs governanceduo:access_requirement.<n>` bridges the two
    namespaces' AccessRequirement individuals — see shapes/governance_graph.owl.ttl.
  - The `.`/`_` → `-` id-hyphenation display convention (`grant.001` → `gov:grant-001`,
    see gov_id() below) is a rename of an existing dotted id, not a mapping any
    class/slot URI declaration could express.

This script exists specifically to let the output be compared structurally against
the design doc's own snippets, e.g.:

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
Turtle serialization directly with rdflib and only *reads* URIs from the schema (via
SchemaView), never registers `gov:` as a schema-level prefix itself — the resolved
IRIs are identical either way (`sagegov:`/`gov:` are the same namespace; see
governance_graph.yaml's own prefix-block comment).

Permissible-value-typed slots (`permission`, `source`, `bindingType`, `state`,
`principalType`) mint one individual per enum value directly from the value string
(`gov:DOWNLOAD`, `gov:Direct`, etc.) rather than through a schema-declared mapping —
none of AccessTypeEnum/BindingTypeEnum/SubmissionStateEnum/PrincipalTypeEnum's
permissible values carry a `meaning:` URI in this namespace, so this is a
deterministic "value string -> gov:<value>" convention, not a second source of truth
that can drift independently of the schema the way a renamed slot could.

Usage:
    python scripts/build_governance_graph.py [--examples-dir linkml/examples/governance_graph]
                                              [--out governance_graph_export/governance_graph.ttl]
                                              [--schema linkml/governance_graph.yaml]

author: orion.banks
"""

import argparse
from functools import lru_cache
from pathlib import Path

import yaml
from rdflib import Graph, Literal, Namespace, OWL, RDF, URIRef, XSD
from rdflib.namespace import NamespaceManager
from linkml_runtime.utils.schemaview import SchemaView

SYN = Namespace("https://www.synapse.org/Synapse:")
GOV = Namespace("https://sagebionetworks.org/governance/")
GOVERNANCEDUO = Namespace("https://w3id.org/sage-bionetworks/governance-duo/")

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
    "access_approval": "AccessApproval",
}

_schemaview: SchemaView | None = None


@lru_cache(maxsize=None)
def PREDICATE(slot_name: str, class_name: str) -> URIRef:
    """Resolve slot_name's *effective* slot_uri for class_name (applying any
    class-scoped slot_usage override, e.g. createdBy differs between SynapseEntity
    and DataAccessSubmission) from governance_graph.yaml itself, rather than a
    hardcoded GOV.<name> Python constant."""
    induced = _schemaview.induced_slot(slot_name, class_name)
    if induced.slot_uri is None:
        raise ValueError(f"{class_name}.{slot_name} has no slot_uri declared in governance_graph.yaml")
    return URIRef(_schemaview.namespaces().uri_for(induced.slot_uri))


@lru_cache(maxsize=None)
def TYPE(class_name: str) -> URIRef:
    """Resolve class_name's class_uri from governance_graph.yaml."""
    cls = _schemaview.get_class(class_name)
    if cls.class_uri is None:
        raise ValueError(f"{class_name} has no class_uri declared in governance_graph.yaml")
    return URIRef(_schemaview.namespaces().uri_for(cls.class_uri))


def gov_id(value: str):
    """governanceDUO ids are dotted/underscored (e.g. `grant.001`,
    `ar_association.001`); the design doc's own ids are fully hyphenated
    (`gov:grant-001`, `gov:ar-association-001`). Convert both separators for a
    structurally faithful comparison against the doc's literal snippets. Not
    schema-declarable (see module docstring) -- a display-convention rename, not a
    distinct identifier scheme."""
    return GOV[value.replace(".", "-").replace("_", "-")]


# Literal SynapseEntity slots emitted as-is (auto-typed by rdflib from the YAML's own
# Python type); createdBy/createdOn are handled separately below (createdBy resolves
# to a different predicate per PREDICATE()'s class-scoped slot_usage override, and
# createdOn needs the xsd:long datatype), and parentId is an IRI reference, not a
# literal.
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
    g.add((subject, RDF.type, TYPE("SynapseEntity")))
    for slot in SYNAPSE_ENTITY_LITERAL_SLOTS:
        if data.get(slot) is not None:
            g.add((subject, PREDICATE(slot, "SynapseEntity"), Literal(data[slot])))
    if data.get("createdBy") is not None:
        # Resolves to sagegov:createdByUserId, not sagegov:createdBy: the latter is
        # reserved for IRI references to a gov:Principal node (see
        # add_data_access_submission/add_data_access_submission_status) -- this is a
        # raw NODE.CREATED_BY id with no corresponding Principal record required. See
        # the createdBy slot_usage override on SynapseEntity in governance_graph.yaml.
        g.add((subject, PREDICATE("createdBy", "SynapseEntity"), Literal(data["createdBy"])))
    if data.get("createdOn") is not None:
        g.add((subject, PREDICATE("createdOn", "SynapseEntity"), Literal(data["createdOn"], datatype=XSD.long)))
    if data.get("parentId"):
        g.add((subject, PREDICATE("parentId", "SynapseEntity"), SYN[data["parentId"]]))


def add_principal(g: Graph, data: dict):
    # Principal is deliberately not is_a: BaseEntity -- see its class description in
    # governance_graph.yaml for why (a real natural integer key already exists, so
    # there's nothing to synthesize, unlike AccessGrant/etc.) -- so there's no
    # dotted/underscored BaseEntity id to hyphenate here; mint a stable node from the
    # bare principalId integer directly instead. Not schema-declarable (see module
    # docstring): this id-minting shape has no LinkML pattern/id_prefixes equivalent.
    subject = GOV[f"principal-{data['principalId']}"]
    # Asserted explicitly alongside the Team/User subtype below, rather than relying
    # solely on shapes/governance_graph.owl.ttl's rdfs:subClassOf declarations -- a
    # plain SPARQL query for `?x a gov:Principal` (or any tool that doesn't load that
    # TBox and do subclass entailment) should still find every Principal individual.
    g.add((subject, RDF.type, TYPE("Principal")))
    # Permissible-value-typed: see module docstring's note on PrincipalTypeEnum.
    g.add((subject, RDF.type, GOV[data["principalType"]]))
    g.add((subject, PREDICATE("principalId", "Principal"), Literal(data["principalId"])))
    return subject


def add_access_grant(g: Graph, data: dict, principal_node):
    subject = gov_id(data["id"])
    g.add((subject, RDF.type, TYPE("AccessGrant")))
    g.add((subject, PREDICATE("resource", "AccessGrant"), SYN[data["resource"]]))
    g.add((subject, PREDICATE("principal", "AccessGrant"), principal_node))
    for perm in data.get("permission", []):
        g.add((subject, PREDICATE("permission", "AccessGrant"), GOV[perm]))
    g.add((subject, PREDICATE("source", "AccessGrant"), GOV[data["source"]]))
    g.add((subject, PREDICATE("bindingType", "AccessGrant"), GOV[data["bindingType"]]))
    if data.get("createdOn") is not None:
        g.add((subject, PREDICATE("createdOn", "AccessGrant"), Literal(data["createdOn"], datatype=XSD.long)))
    if data.get("sourceAclId") is not None:
        g.add((subject, PREDICATE("sourceAclId", "AccessGrant"), Literal(data["sourceAclId"])))
    if data.get("sourceAclResourceAccessId") is not None:
        g.add(
            (
                subject,
                PREDICATE("sourceAclResourceAccessId", "AccessGrant"),
                Literal(data["sourceAclResourceAccessId"]),
            )
        )
    # design doc: "syn10081783 -- hasACL --> ACL:syn10081783 -- (grants) --> ...";
    # this repo's AccessGrant *is* the grant record itself, so the derived
    # convenience triple points hasACL directly at it. No governance_graph.yaml slot
    # backs hasACL (see module docstring) -- kept as a bare GOV.hasACL constant.
    g.add((SYN[data["resource"]], GOV.hasACL, subject))


def add_access_requirement_association(g: Graph, data: dict):
    subject = gov_id(data["id"])
    ar_node = GOV[data["accessRequirement"].replace("access_requirement.", "AR-")]
    g.add((subject, RDF.type, TYPE("AccessRequirementAssociation")))
    g.add((subject, PREDICATE("resource", "AccessRequirementAssociation"), SYN[data["resource"]]))
    g.add((subject, PREDICATE("accessRequirement", "AccessRequirementAssociation"), ar_node))
    g.add((subject, PREDICATE("source", "AccessRequirementAssociation"), GOV[data["source"]]))
    g.add((subject, PREDICATE("bindingType", "AccessRequirementAssociation"), GOV[data["bindingType"]]))
    # Derived convenience triple; no governance_graph.yaml slot backs hasAccessRequirement.
    g.add((SYN[data["resource"]], GOV.hasAccessRequirement, ar_node))
    # NOT TYPE("AccessRequirement"): that class is defined in access_requirement.yaml
    # and its real class_uri is (correctly) governanceduo:AccessRequirement -- ar_node
    # is a local gov:-namespace stub type for the same real-world thing (bridged via
    # owl:sameAs below), not a use of AccessRequirement's own declared URI.
    g.add((ar_node, RDF.type, GOV.AccessRequirement))
    # data["accessRequirement"] (e.g. "access_requirement.42") is the pre-hyphenation
    # id already, in the exact form scripts/convert_examples_to_rdf.py dumps it under
    # the governanceduo: namespace -- asserting identity here, rather than leaving the
    # two namespaces' AccessRequirement individuals implicitly "the same thing" by
    # convention only (see shapes/governance_graph.owl.ttl).
    g.add((ar_node, OWL.sameAs, GOVERNANCEDUO[data["accessRequirement"]]))
    return ar_node


def add_access_requirement(g: Graph, data: dict, ar_node):
    """Mints one gov:Condition individual per data["dataUseModifiers"] entry on
    the existing gov:AR-<n> stub node (ar_node, from
    add_access_requirement_association() above) -- surfacing GovernanceMixin's
    DUO-condition data, already present in the real access_requirement.yaml
    AccessRequirement instance, as first-class graph nodes rather than leaving
    every AR stub with zero condition detail. See
    plans/rebac_governance_graph_alignment.md for the full rationale.

    gov:hasCondition itself is a derived convenience triple with no
    governance_graph.yaml slot backing it, same as gov:hasACL/
    gov:hasAccessRequirement above: the real AccessRequirement class lives in
    access_requirement.yaml, which governance_graph.yaml imports (not the
    other way around), so a slot declared there could never range over
    Condition (defined here) without an import cycle.

    GovernanceMixin.rules is read directly from the schema at runtime (via
    SchemaView, like PREDICATE()/TYPE() elsewhere in this script) rather than
    duplicated as a second hardcoded DUO-code-to-slot map. It's genuinely
    many-to-many -- e.g. DUO:0000026 alone has 4 postcondition slots, and
    requiredAgreementDocumentId is itself the postcondition for 4 different
    codes -- so every matching rule is iterated, not just the first.

    Returns the list of Condition nodes minted, so callers (e.g.
    add_access_requirement_template()) can reuse the same real Condition
    individuals elsewhere rather than re-deriving or duplicating them.
    """
    condition_nodes = []
    enum = _schemaview.get_enum("DataUseModifierEnum")
    rules = _schemaview.get_class("GovernanceMixin").rules
    for duo_code in data.get("dataUseModifiers", []):
        permissible_value = enum.permissible_values.get(duo_code)
        if permissible_value is None:
            continue
        shorthand = (
            permissible_value.annotations.get("duo_shorthand")
            if permissible_value.annotations
            else None
        )
        # Real DUO codes (meaning: set) use their own duo_shorthand ("GRU",
        # "DS", ...); the 7 Sage-local DUOPlus1-7 extensions have neither a
        # meaning: CURIE nor a duo_shorthand, so the bare enum key stands in
        # for conditionType instead -- see governance-graph-sync.md's own
        # documented DUOPlus-extension boundary.
        condition_type = shorthand.value if shorthand is not None else duo_code
        # Node minted from the raw duo_code (not the shorthand label, which
        # isn't guaranteed unique) plus the AR stub's own local name.
        condition_node = GOV[f"{ar_node.rsplit('/', 1)[-1]}-condition-{duo_code.replace(':', '-')}"]
        condition_nodes.append(condition_node)
        g.add((ar_node, GOV.hasCondition, condition_node))
        g.add((condition_node, RDF.type, TYPE("Condition")))
        g.add((condition_node, PREDICATE("conditionType", "Condition"), Literal(condition_type)))
        if permissible_value.meaning:
            g.add((condition_node, PREDICATE("duoCode", "Condition"), Literal(permissible_value.meaning)))
        if permissible_value.description:
            g.add(
                (
                    condition_node,
                    PREDICATE("description", "Condition"),
                    Literal(permissible_value.description),
                )
            )
        for rule in rules:
            if rule.preconditions is None:
                continue
            precondition = rule.preconditions.slot_conditions.get("dataUseModifiers")
            if precondition is None or precondition.equals_string != duo_code:
                continue
            for companion_slot in rule.postconditions.slot_conditions:
                values = data.get(companion_slot)
                if not values:
                    continue
                if not isinstance(values, list):
                    values = [values]
                for value in values:
                    g.add((condition_node, PREDICATE("conditionDetail", "Condition"), Literal(value)))
    return condition_nodes


def add_access_approval(g: Graph, data: dict, principal_nodes: dict) -> bool:
    """Mints a gov:AccessApproval node -- see governance_graph.yaml's own
    class description for why this is a *separate* real Synapse object from
    DataAccessSubmission/Status, not a rename or duplicate of it.

    Returns whether status == APPROVED, so the caller can emit gov:hasApproval
    from this node (the primary, authoritative source going forward -- see
    plans/governance_graph_open_questions.md Section B) alongside the
    existing DataAccessSubmissionStatus-derived edge, which is left as-is.
    """
    subject = gov_id(data["id"])
    ar_node = GOV[data["requirementId"].replace("access_requirement.", "AR-")]
    g.add((subject, RDF.type, TYPE("AccessApproval")))
    g.add((subject, PREDICATE("requirementId", "AccessApproval"), ar_node))
    if data.get("requirementVersion") is not None:
        g.add((subject, PREDICATE("requirementVersion", "AccessApproval"), Literal(data["requirementVersion"])))
    g.add((subject, PREDICATE("submitterId", "AccessApproval"), principal_nodes[data["submitterId"]]))
    accessor_node = principal_nodes[data["accessorId"]]
    g.add((subject, PREDICATE("accessorId", "AccessApproval"), accessor_node))
    g.add((subject, PREDICATE("status", "AccessApproval"), GOV[data["status"]]))
    if data.get("expiredOn") is not None:
        g.add((subject, PREDICATE("expiredOn", "AccessApproval"), Literal(data["expiredOn"], datatype=XSD.long)))
    if data.get("createdOn") is not None:
        g.add((subject, PREDICATE("createdOn", "AccessApproval"), Literal(data["createdOn"], datatype=XSD.long)))
    if data.get("sourceApprovalId") is not None:
        g.add((subject, PREDICATE("sourceApprovalId", "AccessApproval"), Literal(data["sourceApprovalId"])))
    if data.get("etag") is not None:
        g.add((subject, PREDICATE("etag", "AccessApproval"), Literal(data["etag"])))
    if data["status"] == "APPROVED":
        g.add((accessor_node, GOV.hasApproval, ar_node))
    return data["status"] == "APPROVED"


def add_data_access_submission(g: Graph, data: dict, ar_node, approved: bool):
    subject = gov_id(data["id"])
    g.add((subject, RDF.type, TYPE("DataAccessSubmission")))
    # accessRequirementId's slot_uri intentionally resolves to the same predicate
    # AccessRequirementAssociation.accessRequirement uses (see governance_graph.yaml).
    g.add((subject, PREDICATE("accessRequirementId", "DataAccessSubmission"), ar_node))
    # submittedBy/submittedOn (not createdBy/createdOn) -- Synapse's live
    # Submission REST object names these fields submittedBy/submittedOn; see
    # governance_graph.yaml's corrected DataAccessSubmission description.
    g.add((subject, PREDICATE("submittedBy", "DataAccessSubmission"), GOV[f"principal-{data['submittedBy']}"]))
    g.add((subject, PREDICATE("submittedOn", "DataAccessSubmission"), Literal(data["submittedOn"], datatype=XSD.long)))
    if data.get("modifiedBy") is not None:
        # Synapse's live API places modifiedBy on Submission itself, not on
        # DataAccessSubmissionStatus (which carries no such field live) -- see
        # add_data_access_submission_status below and governance_graph.yaml's
        # corrected description on both classes.
        g.add((subject, PREDICATE("modifiedBy", "DataAccessSubmission"), GOV[f"principal-{data['modifiedBy']}"]))
    if approved:
        # Mirrors the design doc's simplified gov:hasApproval predicate -- only
        # emitted once the real, richer submission-status workflow (below) says
        # APPROVED, not merely SUBMITTED. Cross-object join logic, not schema-declarable.
        g.add((GOV[f"principal-{data['submittedBy']}"], GOV.hasApproval, ar_node))


def add_data_access_submission_status(g: Graph, data: dict, submission_node) -> bool:
    # DataAccessSubmissionStatus has no independent node of its own (see
    # governance_graph.yaml) -- its state/rejectedReason/modifiedOn fields are
    # merged onto the DataAccessSubmission subject. Synapse's live
    # SubmissionStatus REST object carries no createdBy/createdOn/modifiedBy of
    # its own (that was this schema's earlier, DB-table-column-based guess,
    # since corrected) -- modifiedBy is real but lives on Submission itself,
    # handled in add_data_access_submission above, not here.
    # DataAccessSubmissionStatus has no class_uri (see governance_graph.yaml --
    # it's merged, not its own individual), so state/rejectedReason/etc. have no
    # PREDICATE() entry to resolve either; kept as bare GOV.<name> constants.
    g.add((submission_node, GOV.state, GOV[data["state"]]))
    if data.get("rejectedReason"):
        g.add((submission_node, GOV.rejectedReason, Literal(data["rejectedReason"])))
    if data.get("modifiedOn") is not None:
        g.add(
            (submission_node, GOV.statusModifiedOn, Literal(data["modifiedOn"], datatype=XSD.long))
        )
    return data["state"] == "APPROVED"


def main():
    global _schemaview

    parser = argparse.ArgumentParser(
        description="Export governance_graph example instances as design-doc-shaped gov:/syn: Turtle."
    )
    parser.add_argument("--examples-dir", default="linkml/examples/governance_graph")
    parser.add_argument(
        "--access-requirement-example",
        default="linkml/examples/access_requirement.example.yaml",
        help=(
            "The *real* access_requirement.yaml AccessRequirement instance to source "
            "gov:Condition data from -- deliberately outside --examples-dir, since it's "
            "a different namespace/source of truth being bridged (see "
            "add_access_requirement())."
        ),
    )
    parser.add_argument("--out", default="governance_graph_export/governance_graph.ttl")
    parser.add_argument("--schema", default="linkml/governance_graph.yaml")
    args = parser.parse_args()

    _schemaview = SchemaView(args.schema)

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
    g.bind("owl", OWL)
    g.bind("governanceduo", GOVERNANCEDUO)

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

    ar_example_path = Path(args.access_requirement_example)
    if ar_node is not None and ar_example_path.exists():
        add_access_requirement(g, yaml.safe_load(ar_example_path.read_text()), ar_node)

    for stem, (class_name, data) in instances.items():
        if class_name == "AccessApproval":
            add_access_approval(g, data, principal_nodes)

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
