"""
sync_governance_graph.py

Builds governance_graph_export/governance_graph_synced.ttl from *real* Synapse data,
for one or more explicitly-supplied entity ids -- the pull order, source-per-class
delineation, and every design decision this script follows are documented in
plans/governance_graph_ingestion.md; read that first if anything here is surprising.

This is deliberately NOT a rewrite of build_governance_graph.py: it imports and
reuses that script's add_*() graph-assembly functions, PREDICATE()/TYPE() schema
resolvers, gov_id()/site_node_for() helpers, and GOV/SYN/GOVERNANCEDUO namespaces
unchanged -- only the *instance-loading* step differs (Synapse REST calls here,
yaml.safe_load over linkml/examples/governance_graph/*.example.yaml there). Writes
to a separate output file by default (not governance_graph_export/governance_graph.ttl)
so it never clobbers the example-driven build `make governance-graph` produces and
`make governance-graph-validate` checks.

Auth: per plans/governance_graph_ingestion.md Section 2 item 4, the credential this
runs under must have ACT membership (or be a validated reviewer for the specific
ARs in scope) -- POST /accessRequirement/{id}/submissions and POST /accessApproval/
search both require it outright, and it's a superset of what the plain entity-level
endpoints need. Uses synapseclient's default credential resolution (cached session /
~/.synapseConfig / SYNAPSE_AUTH_TOKEN) -- nothing here manages credentials itself.

Scope: takes one or more Synapse entity ids as an explicit, required argument. No
recursive subtree walk, no "every entity under this AccessRequirement" enumeration
-- both are reasonable future additions behind an explicit flag, deliberately not
built here (see plans/governance_graph_ingestion.md Section 6 item 1).

DUO conditions: per plans/governance_graph_ingestion.md Section 3, dataUseModifiers
and every GovernanceMixin companion slot are 100% curator-authored -- this script
never tries to derive them from Synapse. It looks up a real, already-authored
governanceduo:AccessRequirement record for each Synapse AccessRequirement id
encountered (--access-requirement-dir, default linkml/examples/) and merges it in
via add_access_requirement(), exactly like build_governance_graph.py's single-example
path -- generalized here to scan a directory for whichever access_requirement.<id>
record exists, since a real sync will encounter more than one AR. Warns (does not
fail) when no curated record exists for an AR in scope, per the warn-don't-block
decision.

Warn, don't block (plans/governance_graph_ingestion.md Section 2 item 3): every
per-item Synapse call that can legitimately fail for reasons outside this script's
control (an entity with no submissions yet, an approval-search endpoint this
credential can't reach, a principal whose profile lookup 403s) is caught, warned to
stderr, and skipped -- never a hard failure of the whole run.

Grounding note -- what's confirmed vs. inferred: every endpoint path/response field
named below was checked directly against rest-docs.synapse.org this session, with
one exception flagged inline at its call site: POST /accessApproval/search's exact
request/response field names couldn't be pulled from a dedicated docs page (repeated
403s on AccessApprovalSearchRequest/AccessApprovalSearchResponse) and are inferred
from its own description text plus this API's established pagination convention
(SubmissionPage's results/nextPageToken shape) -- worth a live smoke test before
trusting it in production, the same way plans/governance_graph_ingestion.md already
flags two endpoints as needing a live check this environment couldn't do. One
simplification discovered while building this that the plan didn't anticipate:
GET /dataAccessSubmission/{submissionId} returns a full Submission object -- the
same type already embedded in POST .../submissions's own result list, state/
rejectedReason/modifiedOn included -- so that second per-submission call turned out
to be unnecessary; this script reads those fields directly off the list response.

Usage:
    python scripts/sync_governance_graph.py syn10081783 [syn2343195 ...]
                                             [--out governance_graph_export/governance_graph_synced.ttl]
                                             [--access-requirement-dir linkml/examples]
                                             [--schema linkml/governance_graph.yaml]

author: orion.banks
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml
from rdflib import Graph, OWL, RDF
from rdflib.namespace import NamespaceManager
from linkml_runtime.utils.schemaview import SchemaView
from synapseclient import Synapse
from synapseclient.core.exceptions import SynapseHTTPError

import build_governance_graph as bgg
from build_governance_graph import GOV, SYN, GOVERNANCEDUO

CURATED_AR_ID_PATTERN = re.compile(r"^access_requirement\.[A-Za-z0-9_-]+$")


def warn(message: str):
    print(f"WARNING: {message}", file=sys.stderr)


def to_millis(value) -> int | None:
    """Synapse's dataaccess-package objects (Submission, AccessApproval,
    ResearchProject, ...) return dates as ISO-8601 strings; entity bundles have
    historically used epoch milliseconds directly. Accept either."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return int(value)
    return int(datetime.fromisoformat(str(value).replace("Z", "+00:00")).timestamp() * 1000)


def node_type_from_concrete_type(concrete_type: str | None) -> str | None:
    """org.sagebionetworks.repo.model.FileEntity -> file,
    org.sagebionetworks.repo.model.Project -> project, etc. -- matches the plain
    lowercase strings linkml/examples/governance_graph/*.example.yaml already use
    for SynapseEntity.nodeType (see governance_graph.yaml: "Mirrors the NODE
    table")."""
    if not concrete_type:
        return None
    short_name = concrete_type.rsplit(".", 1)[-1]
    if short_name.endswith("Entity"):
        short_name = short_name[: -len("Entity")]
    return short_name.lower()


def fetch_synapse_entity(syn: Synapse, entity_id: str) -> dict:
    """GET /entity/{id} -- confirmed shape via rest-docs.synapse.org this session
    (see plans/governance_graph_ingestion.md Section 1's AccessControlList/
    ResourceAccess checks, which used the same doc site)."""
    bundle = syn.restGET(f"/entity/{entity_id}")
    return {
        "id": bundle["id"],
        "name": bundle.get("name"),
        "nodeType": node_type_from_concrete_type(bundle.get("concreteType")),
        "parentId": bundle.get("parentId"),
        "alias": bundle.get("alias"),
        # Synapse's basic entity GET only exposes the *current* version number, not
        # a distinct "max version" -- a real max would need paging through
        # GET /entity/{id}/version, not built here. Both fields point at the same
        # value; a known simplification, not a verified-distinct pair.
        "currentRevNum": bundle.get("versionNumber"),
        "maxRevNum": bundle.get("versionNumber"),
        "etag": bundle.get("etag"),
        # mixins.yaml's createdBy has range: integer, but Synapse's REST API
        # returns user/principal ids as JSON strings -- cast explicitly, or this
        # would emit an xsd:string literal where the shape expects xsd:integer.
        "createdBy": int(bundle["createdBy"]) if bundle.get("createdBy") is not None else None,
        "createdOn": to_millis(bundle.get("createdOn")),
    }


def fetch_benefactor_id(syn: Synapse, entity_id: str) -> str:
    """GET /entity/{id}/benefactor -- an entity is its own benefactor when it has
    local sharing settings; otherwise this returns the ancestor that actually owns
    the effective ACL/AR bindings. Direct vs. Inherited (both for AccessGrant and
    AccessRequirementAssociation) is resolved by comparing against this id."""
    return syn.restGET(f"/entity/{entity_id}/benefactor")["id"]


def fetch_acl_entries(syn: Synapse, benefactor_id: str) -> list[dict]:
    """GET /entity/{id}/acl -- call with the *benefactor* id, not the original
    entity id: an entity without its own local ACL 404s here (it inherits), so the
    benefactor -- which by definition owns its ACL -- is always the right subject to
    call. Returns AccessControlList.resourceAccess directly (each entry: bare
    principalId + accessType list -- confirmed neither carries its own row id, see
    plans/governance_graph_ingestion.md Section 1)."""
    return syn.restGET(f"/entity/{benefactor_id}/acl").get("resourceAccess", [])


def resolve_principal_types(syn: Synapse, principal_ids: set[int]) -> dict[int, dict]:
    """Batch-resolves User vs. Team via GET /userGroupHeaders/batch (isIndividual
    boolean -- confirmed field name), then, for individuals only, fetches
    UserProfile.company (Team has no such field at all -- see
    governance_graph.yaml's Principal.company description)."""
    if not principal_ids:
        return {}
    ids_param = ",".join(str(pid) for pid in principal_ids)
    headers = syn.restGET(f"/userGroupHeaders/batch?ids={ids_param}").get("children", [])
    resolved = {}
    for header in headers:
        principal_id = int(header["ownerId"])
        is_individual = header.get("isIndividual", False)
        company = None
        if is_individual:
            try:
                company = syn.restGET(f"/userProfile/{principal_id}").get("company")
            except SynapseHTTPError as exc:
                warn(f"Could not fetch UserProfile for principal {principal_id}: {exc}")
        resolved[principal_id] = {
            "principalId": principal_id,
            "principalType": "User" if is_individual else "Team",
            "company": company,
        }
    missing = principal_ids - resolved.keys()
    for principal_id in missing:
        warn(f"/userGroupHeaders/batch did not return principal {principal_id}; skipping type/company resolution.")
        resolved[principal_id] = {"principalId": principal_id, "principalType": "User", "company": None}
    return resolved


def is_direct_subject(ar_stub: dict, entity_id: str) -> bool:
    """Direct vs. Inherited for an AccessRequirementAssociation: Synapse's own
    GET /entity/{id}/accessRequirement already returns the effectively-applicable
    list (direct + inherited), but doesn't itself label which is which. Comparing
    the entity id against the AR's own subjectIds is the most direct signal
    available without a second endpoint -- if the entity IS one of the AR's
    explicitly-scoped subjects, that's Direct; if it only shows up because a
    subjectIds ancestor's binding propagates down to it, that's Inherited. Not
    independently confirmed against live data (this environment has none) -- worth
    a spot-check, per plans/governance_graph_ingestion.md's own acknowledged
    entity-endpoint uncertainty."""
    for subject in ar_stub.get("subjectIds", []):
        if subject.get("id") == entity_id and subject.get("type") == "ENTITY":
            return True
    return False


def fetch_access_requirement_ids(syn: Synapse, entity_id: str) -> list[dict]:
    """GET /entity/{id}/accessRequirement -- PaginatedResults<AccessRequirement>
    (results/totalNumberOfResults, Synapse's long-standing paging convention).
    Returns full AccessRequirement objects (subjectIds included, used by
    is_direct_subject() below), so no separate GET /accessRequirement/{id} call is
    needed per AR -- a further pull-order simplification beyond the one already
    noted on fetch_submissions()."""
    results = []
    offset = 0
    limit = 50
    while True:
        page = syn.restGET(f"/entity/{entity_id}/accessRequirement?limit={limit}&offset={offset}")
        page_results = page.get("results", [])
        results.extend(page_results)
        if len(page_results) < limit:
            break
        offset += limit
    return results


def fetch_submissions(syn: Synapse, requirement_id: str) -> list[dict]:
    """POST /accessRequirement/{requirementId}/submissions -- requires ACT
    membership (confirmed). Returns full Submission objects, including
    researchProjectSnapshot (a full embedded ResearchProject -- confirmed) and
    state/rejectedReason/modifiedOn directly (confirmed via GET
    /dataAccessSubmission/{id}'s own return type being the same Submission object
    -- so no second per-submission call is needed for those fields, unlike what
    plans/governance_graph_ingestion.md's pull order assumed before this was
    checked)."""
    results = []
    next_page_token = None
    while True:
        body = {"accessRequirementId": requirement_id}
        if next_page_token:
            body["nextPageToken"] = next_page_token
        page = syn.restPOST(
            f"/accessRequirement/{requirement_id}/submissions",
            body=json.dumps(body),
        )
        results.extend(page.get("results", []))
        next_page_token = page.get("nextPageToken")
        if not next_page_token:
            break
    return results


def fetch_access_approvals(syn: Synapse, requirement_id: str) -> list[dict]:
    """POST /accessApproval/search -- requires ACT membership (confirmed), filters
    by accessRequirementId (confirmed field, per the endpoint's own description:
    "filtering by accessor/submitter and optional by access requirement id").
    Request/response field names beyond that are INFERRED, not confirmed against a
    field-level docs page (AccessApprovalSearchRequest/Response both 403'd
    repeatedly this session) -- assumed to follow this API's own established
    results/nextPageToken pagination shape (confirmed elsewhere for SubmissionPage).
    Worth a live smoke test before relying on this in production."""
    results = []
    next_page_token = None
    while True:
        body = {"accessRequirementId": requirement_id}
        if next_page_token:
            body["nextPageToken"] = next_page_token
        try:
            page = syn.restPOST("/accessApproval/search", body=json.dumps(body))
        except SynapseHTTPError as exc:
            warn(f"/accessApproval/search failed for AR {requirement_id}: {exc}")
            return results
        page_results = page.get("results", [])
        results.extend(page_results)
        next_page_token = page.get("nextPageToken")
        if not next_page_token:
            break
    return results


def load_curated_access_requirements(directory: Path) -> dict[str, dict]:
    """Scans `directory` for curator-authored governanceduo:AccessRequirement
    records (any *.yaml file whose top-level `id` matches access_requirement.<n>),
    indexed by id. Generalizes build_governance_graph.py's single
    --access-requirement-example file to a directory, since a real sync will
    encounter more than one AR -- a stand-in for whatever authoring/storage
    mechanism the DCC ultimately uses, per
    plans/governance_graph_ingestion.md Section 3 (dataUseModifiers and every
    companion slot are 100% curator-authored, never derived from Synapse here)."""
    curated = {}
    if not directory.exists():
        return curated
    for path in directory.glob("*.yaml"):
        try:
            data = yaml.safe_load(path.read_text())
        except yaml.YAMLError:
            continue
        if isinstance(data, dict) and CURATED_AR_ID_PATTERN.match(str(data.get("id", ""))):
            curated[data["id"]] = data
    return curated


def sync_entity(syn: Synapse, entity_id: str, state: dict):
    """Runs the pull order for one entity (plans/governance_graph_ingestion.md
    Section 4, steps 1-6) against already-accumulated cross-entity `state`
    (principal_nodes/ar_nodes/condition_nodes/research_project_nodes -- shared
    across every entity id passed on the command line, since the same principal or
    AR can legitimately appear under more than one entity)."""
    g = state["graph"]

    try:
        entity_data = fetch_synapse_entity(syn, entity_id)
    except SynapseHTTPError as exc:
        warn(f"Could not fetch entity {entity_id}: {exc}; skipping it entirely.")
        return
    bgg.add_synapse_entity(g, entity_data)

    # add_synapse_entity() always emits a parentId edge when present, with no type
    # assertion on the target (fine for build_governance_graph.py's example set,
    # where every referenced parent also has its own example file and gets typed
    # elsewhere in the same run) -- but this sync's scope is explicit entity ids
    # only (plans/governance_graph_ingestion.md Section 6 item 1, no recursive
    # walk), so a parent outside that list would otherwise be a completely untyped
    # reference. Same thin-stub treatment as the DataAccessRequest case below.
    parent_id = entity_data.get("parentId")
    if parent_id and parent_id not in state["requested_entity_ids"]:
        g.add((SYN[parent_id], RDF.type, bgg.TYPE("SynapseEntity")))

    try:
        benefactor_id = fetch_benefactor_id(syn, entity_id)
    except SynapseHTTPError as exc:
        warn(f"Could not fetch benefactor for {entity_id}: {exc}; skipping ACL/AR binding-type resolution.")
        return
    is_direct_acl = benefactor_id == entity_id

    # -- AccessGrant / Principal (steps 2, 5) --
    try:
        acl_entries = fetch_acl_entries(syn, benefactor_id)
    except SynapseHTTPError as exc:
        warn(f"Could not fetch ACL for benefactor {benefactor_id} (of {entity_id}): {exc}")
        acl_entries = []

    new_principal_ids = {
        entry["principalId"] for entry in acl_entries if entry["principalId"] not in state["principal_nodes"]
    }
    for principal_id, principal_data in resolve_principal_types(syn, new_principal_ids).items():
        state["principal_nodes"][principal_id] = bgg.add_principal(g, principal_data)

    for index, entry in enumerate(acl_entries):
        principal_id = entry["principalId"]
        if principal_id not in state["principal_nodes"]:
            warn(f"Skipping AccessGrant for unresolved principal {principal_id} on {entity_id}.")
            continue
        grant_data = {
            "id": f"grant.{entity_id}-{index}",
            "resource": entity_id,
            "permission": entry.get("accessType", []),
            "source": "Synapse",
            "bindingType": "Direct" if is_direct_acl else "Inherited",
        }
        bgg.add_access_grant(g, grant_data, state["principal_nodes"][principal_id])

    # -- AccessRequirementAssociation / AccessRequirementReference (steps 3, 6a) --
    try:
        ar_stubs = fetch_access_requirement_ids(syn, entity_id)
    except SynapseHTTPError as exc:
        warn(f"Could not fetch AccessRequirements for {entity_id}: {exc}")
        ar_stubs = []

    for ar_stub in ar_stubs:
        requirement_id = str(ar_stub["id"])
        curated_key = f"access_requirement.{requirement_id}"
        association_data = {
            "id": f"ar_association.{entity_id}-{requirement_id}",
            "resource": entity_id,
            "accessRequirement": curated_key,
            "source": "Synapse",
            "bindingType": "Direct" if is_direct_subject(ar_stub, entity_id) else "Inherited",
        }
        ar_node = bgg.add_access_requirement_association(g, association_data)

        if requirement_id in state["ar_nodes"]:
            continue  # already fully processed (submissions/approvals/conditions) via another entity
        state["ar_nodes"][requirement_id] = ar_node

        curated_ar = state["curated_ars"].get(curated_key)
        if curated_ar is not None:
            bgg.add_access_requirement(g, curated_ar, ar_node)
        else:
            warn(
                f"No curator-authored AccessRequirement record found for {curated_key} "
                f"(searched {state['access_requirement_dir']}) -- gov:hasCondition data will be "
                "missing for this AR. Not a broken sync -- see plans/governance_graph_ingestion.md "
                "Section 3/7."
            )

        # -- DataAccessSubmission / DataAccessSubmissionStatus / ResearchProject (step 6b) --
        try:
            submissions = fetch_submissions(syn, requirement_id)
        except SynapseHTTPError as exc:
            warn(f"Could not fetch submissions for AR {requirement_id}: {exc}")
            submissions = []

        for submission in submissions:
            snapshot = submission.get("researchProjectSnapshot")

            # Every principal this submission (and its embedded ResearchProject
            # snapshot, which can have a *different* createdBy than the
            # submission's own submittedBy -- e.g. a coordinator submitting on a
            # PI's behalf) references must exist in principal_nodes *before*
            # add_research_project()/add_access_approval() below, which do a plain
            # dict lookup rather than constructing a gov:principal-<n> IRI directly
            # (unlike add_data_access_submission(), which doesn't need this).
            # Resolved one batch per submission rather than one call per id -- not
            # maximally efficient across a whole sync run, but simple and correct.
            submission_principal_ids = {int(submission["submittedBy"])}
            if submission.get("modifiedBy"):
                submission_principal_ids.add(int(submission["modifiedBy"]))
            if snapshot and snapshot.get("createdBy"):
                submission_principal_ids.add(int(snapshot["createdBy"]))
            for pid, pdata in resolve_principal_types(
                syn, submission_principal_ids - state["principal_nodes"].keys()
            ).items():
                state["principal_nodes"][pid] = bgg.add_principal(g, pdata)

            research_project_node = None
            if snapshot:
                research_project_node = bgg.add_research_project(g, {
                    "id": f"research_project.{snapshot['id']}",
                    "accessRequirementId": curated_key,
                    "institution": snapshot.get("institution"),
                    "projectLead": snapshot.get("projectLead"),
                    "intendedDataUseStatement": snapshot.get("intendedDataUseStatement"),
                    "createdBy": int(snapshot["createdBy"]) if snapshot.get("createdBy") else None,
                    "createdOn": to_millis(snapshot.get("createdOn")),
                    "etag": snapshot.get("etag"),
                }, state["principal_nodes"])
                state["research_project_nodes"][snapshot["id"]] = research_project_node

            submitted_by = int(submission["submittedBy"])
            modified_by = submission.get("modifiedBy")
            submission_data = {
                "id": f"data_access_submission.{submission['id']}",
                "accessRequirementId": curated_key,
                "requestId": f"data_access_request.{submission['requestId']}" if submission.get("requestId") else None,
                "researchProjectId": f"research_project.{snapshot['id']}" if snapshot else None,
                "submittedBy": submitted_by,
                "submittedOn": to_millis(submission.get("submittedOn")),
                "modifiedBy": int(modified_by) if modified_by else None,
            }
            approved = submission.get("state") == "APPROVED"
            bgg.add_data_access_submission(g, submission_data, ar_node, approved)
            submission_node = bgg.gov_id(submission_data["id"])
            status_data = {
                "state": submission.get("state"),
                "rejectedReason": submission.get("rejectedReason"),
                "modifiedOn": to_millis(submission.get("modifiedOn")),
            }
            bgg.add_data_access_submission_status(g, status_data, submission_node)

            # DataAccessRequest itself: no REST path exists for anyone else's
            # request (confirmed -- Submission carries only a bare requestId, no
            # embedded snapshot, and the only dedicated GET is owner-restricted).
            # publication/summaryOfUse are recoverable from Submission directly and
            # are already covered by DataAccessSubmission above; everything else on
            # DataAccessRequest is left unpopulated here, per
            # plans/governance_graph_ingestion.md Section 1's accepted-gap decision
            # -- not a bug to fix, not a spreadsheet candidate. The stub still needs
            # two things, though, both genuinely known (not fabricated) even without
            # REST access to the request itself:
            #   - an explicit rdf:type: shapes/governance_graph.shacl.ttl's
            #     DataAccessSubmissionShape declares `sh:path gov:requestId ;
            #     sh:class gov:DataAccessRequest`, so a completely untyped target
            #     would be a ClassConstraintComponent violation, not just a thin one.
            #   - its own accessRequirement edge: DataAccessRequestShape separately
            #     requires one (minCount 1), and we already know which AR this
            #     request belongs to -- it's the same ar_node this whole loop
            #     iteration is for.
            if submission.get("requestId"):
                request_node = bgg.gov_id(submission_data["requestId"])
                g.add((request_node, RDF.type, bgg.TYPE("DataAccessRequest")))
                g.add((request_node, bgg.PREDICATE("accessRequirementId", "DataAccessRequest"), ar_node))

        # -- AccessApproval (step 6c) --
        for approval in fetch_access_approvals(syn, requirement_id):
            submitter_id = int(approval["submitterId"])
            accessor_id = int(approval["accessorId"])
            for pid, pdata in resolve_principal_types(
                syn, {submitter_id, accessor_id} - state["principal_nodes"].keys()
            ).items():
                state["principal_nodes"][pid] = bgg.add_principal(g, pdata)
            approval_data = {
                "id": f"access_approval.{approval['id']}",
                "requirementId": curated_key,
                "requirementVersion": approval.get("requirementVersion"),
                "submitterId": submitter_id,
                "accessorId": accessor_id,
                # AccessApproval's real REST field is "state" (an ApprovalState
                # enum) -- governance_graph.yaml deliberately renames it "status"
                # to avoid colliding with DataAccessSubmissionStatus's unrelated
                # SubmissionStateEnum-typed "state" slot (see that slot's own
                # description).
                "status": approval.get("state"),
                "expiredOn": to_millis(approval.get("expiredOn")),
                "createdOn": to_millis(approval.get("createdOn")),
                "sourceApprovalId": approval.get("id"),
                "etag": approval.get("etag"),
            }
            bgg.add_access_approval(g, approval_data, state["principal_nodes"])


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Sync real Synapse ACL/AccessRequirement/DataAccessSubmission/AccessApproval "
            "state into the gov:/syn: Governance Graph shape, for one or more explicit "
            "entity ids. See plans/governance_graph_ingestion.md for the full design."
        )
    )
    parser.add_argument("entity_ids", nargs="+", help="Synapse entity ids to sync (e.g. syn10081783).")
    parser.add_argument("--out", default="governance_graph_export/governance_graph_synced.ttl")
    parser.add_argument("--schema", default="linkml/governance_graph.yaml")
    parser.add_argument(
        "--access-requirement-dir",
        default="linkml/examples",
        help=(
            "Directory scanned for curator-authored access_requirement.<id>.yaml-shaped "
            "records (any *.yaml file whose top-level id matches that pattern) -- see "
            "load_curated_access_requirements()."
        ),
    )
    args = parser.parse_args()

    bgg._schemaview = SchemaView(args.schema)

    syn = Synapse()
    syn.login()  # default credential resolution -- see module docstring's Auth note

    g = Graph()
    g.namespace_manager = NamespaceManager(g, bind_namespaces="none")
    g.bind("gov", GOV)
    g.bind("syn", SYN)
    g.bind("owl", OWL)
    g.bind("governanceduo", GOVERNANCEDUO)

    state = {
        "graph": g,
        "principal_nodes": {},
        "ar_nodes": {},
        "research_project_nodes": {},
        "curated_ars": load_curated_access_requirements(Path(args.access_requirement_dir)),
        "access_requirement_dir": args.access_requirement_dir,
        "requested_entity_ids": set(args.entity_ids),
    }

    for entity_id in args.entity_ids:
        sync_entity(syn, entity_id, state)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=str(out_path), format="turtle")
    print(f"Wrote {len(g)} triples to {out_path}")


if __name__ == "__main__":
    main()
