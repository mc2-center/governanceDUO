"""
check_sync_governance.py

Offline regression check for scripts/sync_governance_graph.py: runs its real
main() against a fake Synapse client -- no network, no credentials -- and asserts
the output graph's shape. Same approach as check_sync_provenance.py.

The fake client serves one file, syn50000001, whose ACL and AccessRequirement are
inherited from its parent syn50000000 (not requested, so it gets a typed stub):
  - the parent's ACL: user 3000001 with READ, DOWNLOAD and an unrecognized
    FUTURE_PERM; team 3000002 with READ; user 3000006 with only an unrecognized
    NEW_PERM_ONLY;
  - AR 9001 on the parent (curated record in tests/sync_governance/), with two
    Submissions -- 7001 APPROVED by user 3000005, 7002 in an unrecognized state --
    and three AccessApprovals: 8001 APPROVED and unexpired (accessor 3000003),
    8002 APPROVED but expired (accessor 3000001), 8003 in an unrecognized state.
Asserts:
  - the file and its parent stub are SynapseEntities; the grants are Inherited;
    3000001's grant carries gov:READ, gov:DOWNLOAD and the derived gov:ACCESS,
    and FUTURE_PERM is warned and skipped (no gov:FUTURE_PERM anywhere);
    3000006 gets no grant at all (it would have no gov:permission);
  - principal types are the classes gov:User / gov:Team;
  - the AR association is Inherited and gov:AR-9001 has its DUO Condition;
  - Submission 7001's state is gov:APPROVED; 7002 (unrecognized state) is
    warned and skipped whole;
  - gov:hasApproval exactly {3000003 -> AR-9001}: not from the expired approval,
    not from the APPROVED Submission, not from the unrecognized-state approval
    (warned, not minted);
  - ISO-8601 timestamps become epoch-ms literals, and the approval's
    sourceApprovalId (a JSON string here) an integer;
  - the output conforms to shapes/governance_graph.shacl.ttl, and every
    domain/range axiom (enum membership included) holds on it.

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

from rdflib import Graph, Literal, Namespace
from rdflib.namespace import OWL, RDF, XSD

sys.path.insert(0, str(Path(__file__).parent))

GOV = Namespace("https://sagebionetworks.org/governance/")
SYN = Namespace("https://www.synapse.org/Synapse:")
FIXTURE = Path("tests/sync_governance")
NOW_ISO_PAST = "2020-01-01T00:00:00.000Z"
FUTURE_ISO = "2099-01-01T00:00:00.000Z"

ENTITIES = {
    "syn50000001": {
        "id": "syn50000001", "name": "reads.bam", "parentId": "syn50000000",
        "concreteType": "org.sagebionetworks.repo.model.FileEntity", "versionNumber": 1,
        "etag": "e-1", "createdBy": "3000001", "createdOn": "2024-05-01T00:00:00.000Z",
    },
}
GETS = {
    "/entity/syn50000001/benefactor": {"id": "syn50000000"},
    "/entity/syn50000000/acl": {"resourceAccess": [
        {"principalId": 3000001, "accessType": ["READ", "DOWNLOAD", "FUTURE_PERM"]},
        {"principalId": 3000002, "accessType": ["READ"]},
        {"principalId": 3000006, "accessType": ["NEW_PERM_ONLY"]},
    ]},
    "/entity/syn50000001/accessRequirement?limit=50&offset=0": {"results": [
        {"id": 9001, "subjectIds": [{"id": "syn50000000", "type": "ENTITY"}]},
    ]},
}
SUBMISSIONS = [
    {"id": "7001", "requestId": "6001", "submittedBy": "3000005", "submittedOn": "2024-06-01T00:00:00.000Z",
     "state": "APPROVED", "modifiedOn": "2024-06-02T00:00:00.000Z"},
    {"id": "7002", "submittedBy": "3000005", "submittedOn": "2024-06-03T00:00:00.000Z", "state": "UNDER_REVIEW_NEW"},
]
APPROVALS = [
    {"id": "8001", "submitterId": "3000003", "accessorId": "3000003", "state": "APPROVED",
     "expiredOn": FUTURE_ISO, "createdOn": "2024-06-02T00:00:00.000Z"},
    {"id": "8002", "submitterId": "3000001", "accessorId": "3000001", "state": "APPROVED",
     "expiredOn": NOW_ISO_PAST, "createdOn": "2019-01-01T00:00:00.000Z"},
    {"id": "8003", "submitterId": "3000003", "accessorId": "3000003", "state": "PENDING_NEW"},
]
TEAMS = {3000002}


class FakeHTTPError(Exception):
    pass


class FakeSynapse:
    def login(self):
        pass

    def restGET(self, path):
        if path.startswith("/entity/") and path.count("/") == 2:
            entity = ENTITIES.get(path.split("/")[2])
            if entity:
                return entity
        if path in GETS:
            return GETS[path]
        if path.startswith("/userGroupHeaders/batch?ids="):
            ids = [int(i) for i in path.split("=", 1)[1].split(",")]
            return {"children": [{"ownerId": str(i), "isIndividual": i not in TEAMS} for i in ids]}
        if path.startswith("/userProfile/"):
            return {"company": "Mount Sinai"}
        raise FakeHTTPError(f"404 Not Found: {path}")

    def restPOST(self, path, body=None):
        if path == "/accessRequirement/9001/submissions":
            return {"results": SUBMISSIONS}
        if path == "/accessApproval/search":
            return {"results": APPROVALS}
        raise FakeHTTPError(f"404 Not Found: {path}")


def install_fake_synapseclient():
    client = types.ModuleType("synapseclient")
    client.Synapse = FakeSynapse
    exceptions = types.ModuleType("synapseclient.core.exceptions")
    exceptions.SynapseHTTPError = FakeHTTPError
    sys.modules["synapseclient"] = client
    sys.modules["synapseclient.core"] = types.ModuleType("synapseclient.core")
    sys.modules["synapseclient.core.exceptions"] = exceptions


def main():
    install_fake_synapseclient()
    import sync_governance_graph
    from check_domain_range import TBOXES, violations

    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "synced.ttl"
        sys.argv = [
            "sync_governance_graph.py", "syn50000001", "--out", str(out),
            "--access-requirement-dir", str(FIXTURE / "access_requirements"),
        ]
        stderr = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(stderr):
            sync_governance_graph.main()
        g = Graph().parse(out)
        shacl = subprocess.run(
            [sys.executable, "scripts/validate_graph.py", "--data", str(out),
             "--shapes", "shapes/governance_graph.shacl.ttl", "--ont", "shapes/governance_graph.owl.ttl"],
            capture_output=True, text=True,
        )
    warnings = stderr.getvalue()

    def expect(condition, message):
        if not condition:
            failures.append(message)

    principal = lambda n: GOV[f"principal-{n}"]  # noqa: E731
    ar = GOV["AR-9001"]

    for entity in ("syn50000001", "syn50000000"):
        expect((SYN[entity], RDF.type, GOV.SynapseEntity) in g, f"{entity} is not typed gov:SynapseEntity")

    grants = {p: set(g.subjects(GOV.principal, principal(p))) for p in (3000001, 3000002)}
    expect(all(len(v) == 1 for v in grants.values()), f"expected one grant per principal, got {grants}")
    user_grant = next(iter(grants[3000001]), None)
    expect(
        set(g.objects(user_grant, GOV.permission)) == {GOV.READ, GOV.DOWNLOAD, GOV.ACCESS},
        f"3000001's grant permissions: {sorted(g.objects(user_grant, GOV.permission))}",
    )
    expect(not any(GOV.FUTURE_PERM in t for t in g), "gov:FUTURE_PERM was minted")
    expect(
        not any(True for _ in g.subjects(GOV.principal, principal(3000006))),
        "3000006 (only unrecognized permissions) got an AccessGrant",
    )
    expect("'FUTURE_PERM' is not a AccessTypeEnum value" in warnings, "no warning for FUTURE_PERM")
    expect(
        {o for s in (grants[3000001] | grants[3000002]) for o in g.objects(s, GOV.bindingType)} == {GOV.Inherited},
        "grants are not all Inherited",
    )

    expect((principal(3000001), RDF.type, GOV.User) in g, "3000001 is not gov:User")
    expect((principal(3000002), RDF.type, GOV.Team) in g, "3000002 is not gov:Team")

    associations = set(g.subjects(GOV.accessRequirement, ar))
    expect(
        {o for s in associations for o in g.objects(s, GOV.bindingType)} == {GOV.Inherited},
        "the AR association is not Inherited",
    )
    expect(any(True for _ in g.objects(ar, GOV.hasCondition)), "gov:AR-9001 has no Condition")
    expect((ar, OWL.sameAs, None) in g, "gov:AR-9001 has no owl:sameAs to its curated record")

    expect(
        (GOV["data-access-submission-7001"], GOV.state, GOV.APPROVED) in g,
        "submission 7001 is not gov:APPROVED",
    )
    expect(
        (GOV["data-access-submission-7002"], None, None) not in g,
        "submission 7002 (unrecognized state) was minted",
    )
    expect("'UNDER_REVIEW_NEW' is not a SubmissionStateEnum value" in warnings, "no warning for UNDER_REVIEW_NEW")

    approvals = set(g.subject_objects(GOV.hasApproval))
    expect(approvals == {(principal(3000003), ar)}, f"gov:hasApproval: expected only 3000003 -> AR-9001, got {sorted(approvals)}")
    expect((GOV["access-approval-8003"], None, None) not in g, "approval 8003 (unrecognized state) was minted")
    expect("'PENDING_NEW' is not a ApprovalStateEnum value" in warnings, "no warning for PENDING_NEW")

    expect(
        (SYN["syn50000001"], GOV.createdOn, Literal(1714521600000, datatype=XSD.long)) in g
        or any(v.toPython() == 1714521600000 for v in g.objects(SYN["syn50000001"], GOV.createdOn)),
        f"syn50000001 createdOn: {list(g.objects(SYN['syn50000001'], GOV.createdOn))}",
    )

    expect(
        {(v.toPython(), v.datatype) for v in g.objects(GOV["access-approval-8001"], GOV.sourceApprovalId)}
        == {(8001, XSD.integer)},
        f"approval 8001 sourceApprovalId: {list(g.objects(GOV['access-approval-8001'], GOV.sourceApprovalId))}",
    )
    expect(shacl.returncode == 0, f"output does not conform to governance_graph.shacl.ttl:\n{shacl.stdout[-1500:]}")
    tbox = Graph()
    for path in TBOXES:
        tbox.parse(path)
    for violation in violations(tbox, g):
        failures.append(f"domain/range: {violation}")

    if failures:
        print("sync_governance_graph.py offline check FAILED:")
        for failure in failures:
            print(f"  - {failure}")
        sys.exit(1)
    print("sync_governance_graph.py offline check passed.")


if __name__ == "__main__":
    main()
