"""
check_sync_governance.py

Offline regression check for scripts/sync_governance_graph.py: runs its real
main() against a fake Synapse client -- no network, no credentials -- and asserts
the canonical graph it writes. Same approach as check_sync_provenance.py.

The fake client serves one requested file, syn50000001, under project
syn50000000 (in its path, so fetched too), which is its benefactor:
  - the project's ACL: user 3000001 with READ, DOWNLOAD and an unrecognized
    FUTURE_PERM; team 3000002 (member 3000007) with READ; PUBLIC (273949) with
    READ; user 3000006 with only an unrecognized NEW_PERM_ONLY;
  - AR 9001, managed, attached to the project (curated record in
    tests/sync_governance/), with Submissions 7001 APPROVED and 7002 in an
    unrecognized state, and AccessApprovals 8001 APPROVED (unexpired), 8002
    APPROVED (expired), 8004 REVOKED and 8003 in an unrecognized state;
  - AR 9002, self-sign, attached to the file itself, with no curated record.
Asserts:
  - both entities, each with syn50000000 as benefactor, and the file's parent;
  - gov:requiresAR on each AR's own subject (9001 on the project, 9002 on the
    file), not on the entities that only inherit it;
  - one acl:Authorization per recognized ACL entry, on the benefactor: 3000001
    with gov:Read and gov:Download (FUTURE_PERM warned, not minted); the team as
    acl:agentGroup with its member; PUBLIC as acl:agentClass foaf:Agent; none
    for 3000006;
  - AR 9001's type, version and DUO condition (with its agreement document as
    conditionDetail); AR 9002 warned as uncurated, and its submissions never
    fetched, since it isn't managed;
  - Submission 7001 gov:Approved; 7002 warned and left out;
  - every recognized approval recorded with its status and expiry, expired and
    revoked ones included; 8003 warned and left out;
  - timestamps are xsd:dateTime, sourceApprovalId an integer, no blank nodes,
    and the output conforms to shapes/governance.shacl.ttl.

Usage:
    python scripts/check_sync_governance.py

author: orion.banks
"""

import contextlib
import io
import subprocess
import sys
import tempfile
import types
from pathlib import Path

from rdflib import BNode, Graph, Literal, Namespace
from rdflib.namespace import FOAF, RDF, XSD

GOV = Namespace("https://w3id.org/synapse/governance#")
ID = Namespace("https://w3id.org/synapse/governance/")
ACL = Namespace("http://www.w3.org/ns/auth/acl#")
VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")
SYN = Namespace("https://www.synapse.org/Synapse:")
USER = Namespace("https://www.synapse.org/Profile:")
TEAM = Namespace("https://www.synapse.org/Team:")
FIXTURE = Path("tests/sync_governance")
PAST = "2020-01-01T00:00:00.000Z"
FUTURE = "2099-01-01T00:00:00.000Z"
MANAGED = "org.sagebionetworks.repo.model.ManagedACTAccessRequirement"
SELF_SIGN = "org.sagebionetworks.repo.model.SelfSignAccessRequirement"

ENTITIES = {
    "syn50000000": {"id": "syn50000000", "name": "Fixture project", "parentId": "syn4489",
                    "concreteType": "org.sagebionetworks.repo.model.Project",
                    "etag": "e-0", "createdBy": "3000001", "createdOn": "2024-04-01T00:00:00.000Z"},
    "syn50000001": {"id": "syn50000001", "name": "reads.bam", "parentId": "syn50000000",
                    "concreteType": "org.sagebionetworks.repo.model.FileEntity", "versionNumber": 1,
                    "etag": "e-1", "createdBy": "3000001", "createdOn": "2024-05-01T00:00:00.000Z"},
}
PATH = {"path": [{"id": "syn4489"}, {"id": "syn50000000"}, {"id": "syn50000001"}]}
REQUIREMENTS = [
    {"id": 9001, "concreteType": MANAGED, "accessType": "DOWNLOAD", "versionNumber": 2,
     "subjectIds": [{"id": "syn50000000", "type": "ENTITY"}]},
    {"id": 9002, "concreteType": SELF_SIGN, "accessType": "DOWNLOAD", "versionNumber": 1,
     "subjectIds": [{"id": "syn50000001", "type": "ENTITY"}]},
]
GETS = {
    "/entity/syn50000001/benefactor": {"id": "syn50000000"},
    "/entity/syn50000000/benefactor": {"id": "syn50000000"},
    "/entity/syn50000001/path": PATH,
    "/entity/syn50000000/acl": {"resourceAccess": [
        {"principalId": 3000001, "accessType": ["READ", "DOWNLOAD", "FUTURE_PERM"]},
        {"principalId": 3000002, "accessType": ["READ"]},
        {"principalId": 273949, "accessType": ["READ"]},
        {"principalId": 3000006, "accessType": ["NEW_PERM_ONLY"]},
    ]},
    "/entity/syn50000001/accessRequirement?limit=50&offset=0": {"results": REQUIREMENTS},
    "/teamMembers/3000002?limit=50&offset=0": {"results": [
        {"teamId": "3000002", "member": {"ownerId": "3000007", "isIndividual": True}},
    ]},
}
SUBMISSIONS = [
    {"id": "7001", "requestId": "6001", "submittedBy": "3000005", "submittedOn": "2024-06-01T00:00:00.000Z",
     "state": "APPROVED", "modifiedOn": "2024-06-02T00:00:00.000Z", "accessRequirementVersion": 2},
    {"id": "7002", "submittedBy": "3000005", "submittedOn": "2024-06-03T00:00:00.000Z", "state": "UNDER_REVIEW_NEW"},
]
APPROVALS = [
    {"id": "8001", "submitterId": "3000003", "accessorId": "3000003", "state": "APPROVED",
     "expiredOn": FUTURE, "createdOn": "2024-06-02T00:00:00.000Z", "requirementVersion": 2},
    {"id": "8002", "submitterId": "3000001", "accessorId": "3000001", "state": "APPROVED",
     "expiredOn": PAST, "createdOn": "2019-01-01T00:00:00.000Z"},
    {"id": "8004", "submitterId": "3000008", "accessorId": "3000008", "state": "REVOKED"},
    {"id": "8003", "submitterId": "3000003", "accessorId": "3000003", "state": "PENDING_NEW"},
]
TEAMS = {3000002, 273949}
POSTS = []


class FakeHTTPError(Exception):
    pass


class FakeSynapse:
    def login(self):
        pass

    def restGET(self, path):
        if path.startswith("/entity/") and path.count("/") == 2:
            entity = ENTITIES.get(path.split("/")[2])
            if entity:
                return dict(entity)
        if path in GETS:
            return GETS[path]
        if path.startswith("/userGroupHeaders/batch?ids="):
            ids = [int(i) for i in path.split("=", 1)[1].split(",")]
            return {"children": [{"ownerId": str(i), "isIndividual": i not in TEAMS} for i in ids]}
        if path.startswith("/userProfile/"):
            return {"company": "Mount Sinai"}
        raise FakeHTTPError(f"404 Not Found: {path}")

    def restPOST(self, path, body=None):
        POSTS.append(path)
        if path == "/accessRequirement/9001/submissions":
            return {"results": SUBMISSIONS}
        if path == "/accessApproval/search":
            return {"results": APPROVALS if '"9001"' in body else []}
        raise FakeHTTPError(f"404 Not Found: {path}")


def install_fake_synapseclient():
    client = types.ModuleType("synapseclient")
    client.Synapse = FakeSynapse
    exceptions = types.ModuleType("synapseclient.core.exceptions")
    exceptions.SynapseHTTPError = FakeHTTPError
    sys.modules["synapseclient"] = client
    sys.modules["synapseclient.core"] = types.ModuleType("synapseclient.core")
    sys.modules["synapseclient.core.exceptions"] = exceptions


def run_sync(out: Path) -> str:
    """Runs the sync's main() against the fake client; returns its warnings."""
    install_fake_synapseclient()
    import sync_governance_graph

    sys.argv = ["sync_governance_graph.py", "syn50000001", "--out", str(out),
                "--access-requirement-dir", str(FIXTURE / "access_requirements")]
    stderr = io.StringIO()
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(stderr):
        sync_governance_graph.main()
    return stderr.getvalue()


def main():
    failures = []

    def expect(condition, message):
        if not condition:
            failures.append(message)

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "synced.ttl"
        warnings = run_sync(out)
        g = Graph().parse(out)
        shacl = subprocess.run(
            [sys.executable, "scripts/validate_graph.py", "--data", str(out),
             "--shapes", "shapes/governance.shacl.ttl", "--ont", "shapes/governance.owl.ttl"],
            capture_output=True, text=True,
        )

    project, file = SYN.syn50000000, SYN.syn50000001
    ar1, ar2 = ID["ar/9001"], ID["ar/9002"]

    for entity in (project, file):
        expect((entity, RDF.type, GOV.SynapseEntity) in g, f"{entity} is not a gov:SynapseEntity")
        expect((entity, GOV.benefactor, project) in g, f"{entity}'s benefactor is not {project}")
    expect((file, GOV.parent, project) in g, "the file's parent is not the project")
    expect(set(g.objects(project, GOV.requiresAR)) == {ar1}, f"project requiresAR: {set(g.objects(project, GOV.requiresAR))}")
    expect(set(g.objects(file, GOV.requiresAR)) == {ar2}, f"file requiresAR: {set(g.objects(file, GOV.requiresAR))}")

    authorizations = set(g.subjects(RDF.type, ACL.Authorization))
    expect(len(authorizations) == 3, f"expected 3 authorizations, got {len(authorizations)}")
    for a in authorizations:
        expect((a, ACL.accessTo, project) in g and (a, ACL.default, project) in g,
               f"{a} isn't on the benefactor")
    user_auth = set(g.subjects(ACL.agent, USER["3000001"]))
    expect(len(user_auth) == 1 and set(g.objects(next(iter(user_auth)), ACL.mode)) == {GOV.Read, GOV.Download},
           "3000001's authorization isn't exactly Read + Download")
    expect(not any("FUTURE_PERM" in str(t) for triple in g for t in triple), "FUTURE_PERM was minted")
    expect("'FUTURE_PERM' is not a Permission value" in warnings, "no warning for FUTURE_PERM")
    expect(not any(True for _ in g.subjects(ACL.agent, USER["3000006"])), "3000006 got an authorization")
    expect(any(True for _ in g.subjects(ACL.agentGroup, TEAM["3000002"])), "team 3000002 has no authorization")
    expect((TEAM["3000002"], RDF.type, VCARD.Group) in g, "3000002 is not a vcard:Group")
    expect((TEAM["3000002"], VCARD.hasMember, USER["3000007"]) in g, "team 3000002 doesn't list member 3000007")
    expect(any(True for _ in g.subjects(ACL.agentClass, FOAF.Agent)), "PUBLIC isn't acl:agentClass foaf:Agent")
    expect((TEAM["273949"], None, None) not in g and (USER["273949"], None, None) not in g,
           "PUBLIC was minted as a team or user")

    expect((ar1, GOV.requirementType, GOV.ManagedACTRequirement) in g, "AR 9001 isn't managed")
    expect((ar1, GOV.versionNumber, Literal(2)) in g, "AR 9001's version isn't 2")
    condition = ID["ar/9001/condition/DUO_0000042"]
    expect((ar1, GOV.hasCondition, condition) in g, "AR 9001 has no DUO:0000042 condition")
    expect((condition, GOV.conditionDetail, Literal("did:example:fixture-dua-9001")) in g,
           "the condition doesn't carry its agreement document")
    expect((ar2, GOV.requirementType, GOV.SelfSignRequirement) in g, "AR 9002 isn't self-sign")
    expect("No curated record for AR 9002" in warnings, "no warning for uncurated AR 9002")
    expect("/accessRequirement/9002/submissions" not in POSTS, "submissions were fetched for a self-sign AR")

    expect((ID["submission/7001"], GOV.state, GOV.Approved) in g, "submission 7001 isn't gov:Approved")
    expect((ID["submission/7002"], None, None) not in g, "submission 7002 (unrecognized state) was minted")
    expect("'UNDER_REVIEW_NEW' is not a SubmissionState value" in warnings, "no warning for UNDER_REVIEW_NEW")

    status = {a: g.value(ID[f"approval/{a}"], GOV.status) for a in ("8001", "8002", "8004")}
    expect(status == {"8001": GOV.Approved, "8002": GOV.Approved, "8004": GOV.Revoked},
           f"approval statuses: {status}")
    expect((ID["approval/8003"], None, None) not in g, "approval 8003 (unrecognized state) was minted")
    expect("'PENDING_NEW' is not a ApprovalStatus value" in warnings, "no warning for PENDING_NEW")
    expires = g.value(ID["approval/8002"], GOV.expiresAt)
    expect(expires is not None and expires.datatype == XSD.dateTime and str(expires).startswith("2020-01-01"),
           f"approval 8002 expiresAt: {expires!r}")
    source = g.value(ID["approval/8001"], GOV.sourceApprovalId)
    expect(source is not None and source.toPython() == 8001 and source.datatype == XSD.integer,
           f"approval 8001 sourceApprovalId: {source!r}")
    created = g.value(file, GOV.createdOn)
    expect(created is not None and created.datatype == XSD.dateTime, f"file createdOn: {created!r}")

    expect(not any(isinstance(t, BNode) for triple in g for t in triple), "the output has blank nodes")
    expect(shacl.returncode == 0, f"output does not conform to shapes/governance.shacl.ttl:\n{shacl.stdout[-1500:]}")

    if failures:
        print("sync_governance_graph.py offline check FAILED:")
        for failure in failures:
            print(f"  - {failure}")
        sys.exit(1)
    print("sync_governance_graph.py offline check passed.")


if __name__ == "__main__":
    main()
