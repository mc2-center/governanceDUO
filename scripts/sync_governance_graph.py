"""
sync_governance_graph.py

Builds the canonical governance graph from real Synapse data, for one or more
explicitly supplied entity ids (plans/governance_graph_ingestion.md for the pull
order and access requirements; plans/model_refactor.md for the model). It
describes what Synapse says through build_graph.GraphBuilder and writes it with
graph_rdf -- it records facts only. Per-entity inherited grants, team
expansion and "is this approval active" are the projections' job (projections/).

For each requested entity:
  1. the entity, its ancestor chain (GET /entity/{id}/path) and each one's
     benefactor, so an evaluator can follow ACL and AR inheritance itself;
  2. its benefactor's ACL, one acl:Authorization per entry. Users are
     acl:agent, teams acl:agentGroup (with their members, GET /teamMembers), and
     Synapse's PUBLIC and AUTHENTICATED_USERS groups acl:agentClass
     foaf:Agent / acl:AuthenticatedAgent;
  3. the Access Requirements that apply to it (GET /entity/{id}/accessRequirement),
     each attached by gov:requiresAR to the entities in the chain that are its
     subjectIds, with its concreteType, accessType and version. A curator-authored
     record (--access-requirement-dir) adds its data-use conditions and tier;
  4. for managed ARs only, their DataAccessSubmissions (POST
     /accessRequirement/{id}/submissions); for every AR, every AccessApproval
     (POST /accessApproval/search), whatever its state or expiry. A
     submission's or approval's own requirementVersion is compared against the
     AR's current versionNumber (both recorded, never dropped); a mismatch is
     warned, not corrected -- it means the AR changed since that submission or
     approval was made, which is exactly the situation a person, not this
     script, should judge.

Auth: the credential must have ACT membership (or be a validated reviewer for the
ARs in scope); the submission and approval searches require it. Uses
synapseclient's default credential resolution.

Warn, don't block: a per-item call that can fail for reasons outside this
script's control (no submissions yet, an unreachable approval search, a 403 on a
profile) is warned to stderr and skipped. A value outside its vocabulary (a new
ACCESS_TYPE, say) is warned and left out, never minted.

Unconfirmed against live Synapse (no credentials in this environment): the
request/response field names of POST /accessApproval/search, and the page shape
of GET /teamMembers/{id} (assumed PaginatedResults<TeamMember> with
member.ownerId). Smoke-test both before relying on them.

Usage:
    python scripts/sync_governance_graph.py syn10081783 [syn2343195 ...]
        [--out governance_graph_export/governance_graph_synced.ttl]
        [--access-requirement-dir linkml/examples]

author: orion.banks
"""

import argparse
import json
import re
from pathlib import Path

import yaml
from synapseclient import Synapse
from synapseclient.core.exceptions import SynapseHTTPError

import graph_iris
import graph_rdf
from build_graph import AGENT_CLASS_FOR_GROUP, GraphBuilder, record_rules, to_datetime, warn

CURATED_AR_ID_PATTERN = re.compile(r"^access_requirement\.[0-9]+$")
MANAGED = "ManagedACTAccessRequirement"
PAGE = 50


def short_type(concrete_type: str | None) -> str | None:
    """org.sagebionetworks.repo.model.ManagedACTAccessRequirement -> ManagedACTAccessRequirement."""
    return concrete_type.rsplit(".", 1)[-1] if concrete_type else None


def paged_get(syn: Synapse, path: str) -> list[dict]:
    """GET a PaginatedResults endpoint to exhaustion (limit/offset paging)."""
    results, offset = [], 0
    separator = "&" if "?" in path else "?"
    while True:
        page = syn.restGET(f"{path}{separator}limit={PAGE}&offset={offset}")
        batch = page.get("results", [])
        results.extend(batch)
        if len(batch) < PAGE:
            return results
        offset += PAGE


def token_post(syn: Synapse, path: str, body: dict) -> list[dict]:
    """POST a nextPageToken-paged search to exhaustion."""
    results, token = [], None
    while True:
        request = dict(body, **({"nextPageToken": token} if token else {}))
        page = syn.restPOST(path, body=json.dumps(request))
        results.extend(page.get("results", []))
        token = page.get("nextPageToken")
        if not token:
            return results


def load_curated_access_requirements(directory: Path) -> dict[str, dict]:
    """Curator-authored record-layer AccessRequirement records under `directory`
    (any *.yaml whose top-level id is access_requirement.<n>), by Synapse AR id."""
    curated = {}
    for path in sorted(directory.glob("*.yaml")) if directory.exists() else []:
        try:
            data = yaml.safe_load(path.read_text())
        except yaml.YAMLError:
            continue
        if isinstance(data, dict) and CURATED_AR_ID_PATTERN.match(str(data.get("id", ""))):
            curated[data["id"].split(".", 1)[1]] = data
    return curated


class Sync:
    def __init__(self, syn: Synapse, curated: dict, curated_dir: str):
        self.syn = syn
        self.graph = GraphBuilder()
        self.curated = curated
        self.curated_dir = curated_dir
        self.rules = record_rules()
        self.principals: dict[int, tuple[str, str]] = {}
        self.bundles: dict[str, dict] = {}
        self.roots: set[str] = set()
        self.ars_done: set[str] = set()

    # -- principals ----------------------------------------------------------

    def resolve_principals(self, ids) -> None:
        """User vs. team (GET /userGroupHeaders/batch), a user's company
        (GET /userProfile), a team's members (GET /teamMembers)."""
        ids = {int(i) for i in ids} - self.principals.keys()
        if not ids:
            return
        query = ",".join(str(i) for i in sorted(ids))
        headers = self.syn.restGET(f"/userGroupHeaders/batch?ids={query}").get("children", [])
        seen = set()
        for header in headers:
            pid = int(header["ownerId"])
            seen.add(pid)
            individual = bool(header.get("isIndividual", False))
            company = None
            if individual:
                try:
                    company = self.syn.restGET(f"/userProfile/{pid}").get("company")
                except SynapseHTTPError as exc:
                    warn(f"Could not fetch the profile of user {pid}: {exc}")
            self.principals[pid] = self.graph.principal(pid, individual, company)
            if not individual and pid not in AGENT_CLASS_FOR_GROUP:
                self.team_members(pid)
        for pid in ids - seen:
            warn(f"/userGroupHeaders/batch did not return principal {pid}; leaving it out.")

    def team_members(self, team_id: int) -> None:
        try:
            members = paged_get(self.syn, f"/teamMembers/{team_id}")
        except SynapseHTTPError as exc:
            warn(f"Could not fetch the members of team {team_id}: {exc}")
            return
        users = [self.graph.user(m["member"]["ownerId"]) for m in members if m.get("member")]
        self.graph.add("Team", id=graph_iris.team(team_id), hasMember=users)

    # -- entities ------------------------------------------------------------

    def add_entity(self, entity_id: str) -> dict | None:
        """The entity and its benefactor. Returns the entity bundle (with the
        benefactor id under "_benefactor"), or None if it couldn't be fetched."""
        if entity_id in self.bundles:
            return self.bundles[entity_id]
        try:
            bundle = self.syn.restGET(f"/entity/{entity_id}")
            benefactor = self.syn.restGET(f"/entity/{entity_id}/benefactor")["id"]
        except SynapseHTTPError as exc:
            warn(f"Could not fetch entity {entity_id} or its benefactor: {exc}; leaving it out.")
            return None
        self.graph.add(
            "SynapseEntity",
            id=graph_iris.entity(entity_id),
            name=bundle.get("name"),
            entityType=bundle.get("concreteType"),
            # a project's parent is Synapse's root, which isn't a governed entity
            parent=graph_iris.entity(bundle["parentId"])
            if bundle.get("parentId") and bundle["parentId"] not in self.roots else None,
            benefactor=graph_iris.entity(benefactor),
            versionNumber=bundle.get("versionNumber"),
            etag=bundle.get("etag"),
            createdBy=self.graph.user(bundle.get("createdBy")),
            createdOn=to_datetime(bundle.get("createdOn")),
            modifiedOn=to_datetime(bundle.get("modifiedOn")),
        )
        bundle["_benefactor"] = benefactor
        self.bundles[entity_id] = bundle
        return bundle

    def ancestors(self, entity_id: str) -> list[str]:
        """The entity's ancestors below Synapse's root, nearest last."""
        try:
            path = self.syn.restGET(f"/entity/{entity_id}/path").get("path", [])
        except SynapseHTTPError as exc:
            warn(f"Could not fetch the path of {entity_id}: {exc}; AR inheritance from its ancestors is lost.")
            return []
        if path:
            self.roots.add(path[0]["id"])  # path[0] is Synapse's root
        return [header["id"] for header in path[1:] if header["id"] != entity_id]

    def add_acl(self, entity_id: str, benefactor: str) -> None:
        try:
            entries = self.syn.restGET(f"/entity/{benefactor}/acl").get("resourceAccess", [])
        except SynapseHTTPError as exc:
            warn(f"Could not fetch the ACL of {benefactor} (benefactor of {entity_id}): {exc}")
            return
        self.resolve_principals(entry["principalId"] for entry in entries)
        for entry in entries:
            pid = int(entry["principalId"])
            if pid not in self.principals:
                continue
            modes = [m for m in entry.get("accessType", [])
                     if self.graph.known("Permission", m, f"ACL of {benefactor}, principal {pid}")]
            if not modes:
                warn(f"ACL of {benefactor}, principal {pid}: no recognized permission; leaving the entry out.")
                continue
            slot, value = self.principals[pid]
            self.graph.add(
                "Authorization",
                id=graph_iris.authorization(benefactor, pid),
                accessTo=graph_iris.entity(benefactor),
                default=graph_iris.entity(benefactor),
                mode=modes,
                **{slot: value},
            )

    # -- access requirements --------------------------------------------------

    def add_access_requirements(self, entity_id: str, chain: list[str]) -> None:
        try:
            requirements = paged_get(self.syn, f"/entity/{entity_id}/accessRequirement")
        except SynapseHTTPError as exc:
            warn(f"Could not fetch the Access Requirements of {entity_id}: {exc}")
            return
        for ar in requirements:
            rid = str(ar["id"])
            iri = graph_iris.access_requirement(rid)
            subjects = {s["id"] for s in ar.get("subjectIds", []) if s.get("type") == "ENTITY"}
            for subject in subjects & set(chain):
                self.graph.add("SynapseEntity", id=graph_iris.entity(subject), requiresAR=[iri])
            if not subjects & set(chain):
                warn(f"AR {rid} applies to {entity_id} but none of its subjects is in its path; "
                     "it's recorded, unattached.")
            if rid in self.ars_done:
                continue
            self.ars_done.add(rid)
            requirement_type = short_type(ar.get("concreteType"))
            if requirement_type and not self.graph.known("AccessRequirementType", requirement_type, f"AR {rid}"):
                requirement_type = None
            access_type = ar.get("accessType")
            if access_type and not self.graph.known("Permission", access_type, f"AR {rid} accessType"):
                access_type = None
            self.graph.add(
                "AccessRequirement", id=iri, name=ar.get("name"),
                requirementType=requirement_type, accessType=access_type,
                versionNumber=ar.get("versionNumber"), etag=ar.get("etag"),
                createdBy=self.graph.user(ar.get("createdBy")),
                createdOn=to_datetime(ar.get("createdOn")),
                modifiedOn=to_datetime(ar.get("modifiedOn")),
            )
            if rid in self.curated:
                self.graph.curated_access_requirement(self.curated[rid], self.rules)
            else:
                warn(f"No curated record for AR {rid} under {self.curated_dir}: it has no conditions or tier.")
            current_version = ar.get("versionNumber")
            if requirement_type == MANAGED:
                self.add_submissions(rid, iri, current_version)
            self.add_approvals(rid, iri, current_version)

    def add_submissions(self, rid: str, requirement: str, current_version) -> None:
        try:
            submissions = token_post(self.syn, f"/accessRequirement/{rid}/submissions",
                                     {"accessRequirementId": rid})
        except SynapseHTTPError as exc:
            warn(f"Could not fetch the submissions of AR {rid}: {exc}")
            return
        for s in submissions:
            if not self.graph.known("SubmissionState", s.get("state"), f"submission {s['id']}"):
                continue
            snapshot = s.get("researchProjectSnapshot")
            project = None
            if snapshot:
                project = self.graph.add(
                    "ResearchProject", id=graph_iris.research_project(snapshot["id"]),
                    accessRequirement=requirement, institution=snapshot.get("institution"),
                    affiliatedWith=[self.graph.site(snapshot.get("institution"))] if snapshot.get("institution") else None,
                    projectLead=snapshot.get("projectLead"),
                    intendedDataUseStatement=snapshot.get("intendedDataUseStatement"),
                    createdBy=self.graph.user(snapshot.get("createdBy")),
                    createdOn=to_datetime(snapshot.get("createdOn")), etag=snapshot.get("etag"),
                )
            request = None
            if s.get("requestId"):
                # Only the request's owner can read it, so the node carries what
                # the submission says about it.
                request = self.graph.add("DataAccessRequest", id=graph_iris.request(s["requestId"]),
                                         accessRequirement=requirement, researchProject=project)
            submission_version = s.get("accessRequirementVersion")
            if submission_version is not None and current_version is not None and submission_version != current_version:
                warn(f"submission {s['id']}: made against AR {rid} version {submission_version}, "
                     f"which is now at version {current_version}.")
            self.graph.add(
                "DataAccessSubmission", id=graph_iris.submission(s["id"]),
                accessRequirement=requirement,
                requirementVersion=submission_version,
                request=request, researchProject=project,
                submittedBy=self.graph.user(s.get("submittedBy")),
                submittedOn=to_datetime(s.get("submittedOn")),
                state=s.get("state"), rejectedReason=s.get("rejectedReason"),
                modifiedBy=self.graph.user(s.get("modifiedBy")),
                modifiedOn=to_datetime(s.get("modifiedOn")), etag=s.get("etag"),
            )

    def add_approvals(self, rid: str, requirement: str, current_version) -> None:
        try:
            approvals = token_post(self.syn, "/accessApproval/search", {"accessRequirementId": rid})
        except SynapseHTTPError as exc:
            warn(f"/accessApproval/search failed for AR {rid}: {exc}")
            return
        for a in approvals:
            if not self.graph.known("ApprovalStatus", a.get("state"), f"access approval {a['id']}"):
                continue
            approval_version = a.get("requirementVersion")
            if approval_version is not None and current_version is not None and approval_version != current_version:
                warn(f"approval {a['id']}: holds AR {rid} at version {approval_version}, "
                     f"which is now at version {current_version}.")
            self.graph.add(
                "Approval", id=graph_iris.approval(a["id"]),
                satisfies=requirement, requirementVersion=approval_version,
                heldBy=self.graph.user(a["accessorId"]),
                submittedBy=self.graph.user(a.get("submitterId")),
                status=a["state"],
                expiresAt=to_datetime(a.get("expiredOn")),
                createdOn=to_datetime(a.get("createdOn")),
                modifiedOn=to_datetime(a.get("modifiedOn")),
                sourceApprovalId=int(a["id"]), etag=a.get("etag"),
            )

    # -- one requested entity -------------------------------------------------

    def sync(self, entity_id: str) -> None:
        ancestors = self.ancestors(entity_id)
        bundle = self.add_entity(entity_id)
        if bundle is None:
            return
        chain = [entity_id]
        for ancestor in ancestors:
            if self.add_entity(ancestor) is not None:
                chain.append(ancestor)
        self.add_acl(entity_id, bundle["_benefactor"])
        self.add_access_requirements(entity_id, chain)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("entity_ids", nargs="+", help="Synapse entity ids to sync (e.g. syn10081783).")
    parser.add_argument("--out", default="governance_graph_export/governance_graph_synced.ttl")
    parser.add_argument("--access-requirement-dir", default="linkml/examples",
                        help="Directory of curated access_requirement.<id> records.")
    args = parser.parse_args()

    syn = Synapse()
    syn.login()  # default credential resolution; see the docstring's Auth note
    sync = Sync(syn, load_curated_access_requirements(Path(args.access_requirement_dir)),
                args.access_requirement_dir)
    for entity_id in args.entity_ids:
        sync.sync(entity_id)

    graph = graph_rdf.to_rdf(sync.graph.container())
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    graph.serialize(destination=str(out), format="turtle")
    print(f"Wrote {len(graph)} triples to {out}")


if __name__ == "__main__":
    main()
