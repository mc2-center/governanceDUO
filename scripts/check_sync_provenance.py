"""
check_sync_provenance.py

Offline regression check for scripts/sync_provenance_graph.py: runs its real
main() against a fake Synapse client -- no network, no credentials -- and asserts
the output graph's shape.

The fake client returns one Activity for two requested entities (Synapse lets one
Activity be the generatedBy of several entities), with one UsedURL input
(executed) and one versioned UsedEntity input (not executed); a third requested
entity has no Activity and must be skipped with a warning. The Activity carries
ISO-8601 createdOn/modifiedOn (as Synapse returns them) and a third, unrecognized
Used subtype. Asserts:
  - exactly one Activity node, .../activity/<n>, with both outputs as
    prov:generated;
  - exactly two prov:Usage nodes, .../activity/<n>/usage/1 and /2 (no
    per-output duplication; the unrecognized third entry left out with a
    warning), the URL one named with gov:name;
  - createdOn/modifiedOn as xsd:dateTime, createdBy a user IRI;
  - every IRI is absolute, and there are no blank nodes;
  - no prov:wasDerivedFrom (it's projections/provenance.rq's), and the output
    conforms to shapes/governance.shacl.ttl.

Usage:
    python scripts/check_sync_provenance.py

author: orion.banks
"""

import contextlib
import io
import subprocess
import sys
import tempfile
import types
from pathlib import Path

from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD

sys.path.insert(0, str(Path(__file__).parent))

PROV = Namespace("http://www.w3.org/ns/prov#")
GOV = Namespace("https://w3id.org/synapse/governance#")
ID = Namespace("https://w3id.org/synapse/governance/")
USER = Namespace("https://www.synapse.org/Profile:")
SYN = Namespace("https://www.synapse.org/Synapse:")

ACTIVITY = {
    "id": "9606",
    "name": "nf-core rnaseq run",
    "createdBy": "3321",
    # Synapse's Activity returns ISO-8601 date-times, not epoch milliseconds.
    "createdOn": "2024-03-01T12:00:00.000Z",
    "modifiedOn": "2024-03-02T08:30:00.000Z",
    "used": [
        {
            "concreteType": "org.sagebionetworks.repo.model.provenance.UsedURL",
            "url": "https://nf-co.re/rnaseq/3.11.1",
            "name": "nf-core/rnaseq v3.11.1",
            "wasExecuted": True,
        },
        {
            "concreteType": "org.sagebionetworks.repo.model.provenance.UsedEntity",
            "reference": {"targetId": "syn10081783", "targetVersionNumber": 2},
            "wasExecuted": False,
        },
        # An unrecognized Used subtype: warned and skipped, never a crash.
        {"concreteType": "org.sagebionetworks.repo.model.provenance.UsedSomethingNew"},
    ],
}
OUTPUTS = ["syn30000001", "syn30000002"]


class FakeHTTPError(Exception):
    pass


class FakeSynapse:
    def login(self):
        pass

    def restGET(self, path):
        if path in {f"/entity/{e}/generatedBy" for e in OUTPUTS}:
            return ACTIVITY
        raise FakeHTTPError("404 Not Found")


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
    import sync_provenance_graph

    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "synced.ttl"
        sys.argv = ["sync_provenance_graph.py", *OUTPUTS, "syn99999999", "--out", str(out)]
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            sync_provenance_graph.main()
        g = Graph().parse(out)
        shacl = subprocess.run(
            [sys.executable, "scripts/validate_graph.py", "--data", str(out),
             "--shapes", "shapes/governance.shacl.ttl", "--ont", "shapes/governance.owl.ttl"],
            capture_output=True, text=True,
        )

    activity = ID["activity/9606"]
    activities = set(g.subjects(RDF.type, PROV.Activity))
    if activities != {activity}:
        failures.append(f"expected one Activity {activity}, got {sorted(activities)}")
    generated = set(g.objects(activity, PROV.generated))
    if generated != {SYN[e] for e in OUTPUTS}:
        failures.append(f"expected prov:generated {OUTPUTS}, got {sorted(generated)}")
    usages = set(g.subjects(RDF.type, PROV.Usage))
    if usages != {ID["activity/9606/usage/1"], ID["activity/9606/usage/2"]}:
        failures.append(f"expected usages 1 and 2, got {sorted(usages)}")
    if (ID["activity/9606/usage/1"], GOV.name, Literal("nf-core/rnaseq v3.11.1")) not in g:
        failures.append("URL Usage is missing gov:name")
    if "unrecognized Used.concreteType" not in stderr.getvalue():
        failures.append(f"expected a warning for the unrecognized Used entry; stderr was: {stderr.getvalue()!r}")
    for predicate, moment in ((GOV.createdOn, "2024-03-01T12:00:00"), (GOV.modifiedOn, "2024-03-02T08:30:00")):
        values = [v for v in g.objects(activity, predicate)]
        if len(values) != 1 or values[0].datatype != XSD.dateTime or not str(values[0]).startswith(moment):
            failures.append(f"expected {predicate.n3()} {moment} (xsd:dateTime), got {values}")
    if (activity, GOV.createdBy, USER["3321"]) not in g:
        failures.append("createdBy is not the user IRI")
    relative = sorted(
        str(t) for triple in g for t in triple if isinstance(t, URIRef) and str(t).startswith("file:")
    )
    if relative:
        failures.append(f"relative IRIs resolved against a file path: {relative}")
    if any(isinstance(t, BNode) for triple in g for t in triple):
        failures.append("the output has blank nodes")
    if (None, PROV.wasDerivedFrom, None) in g:
        failures.append("prov:wasDerivedFrom is in the canonical graph (it's a projection)")
    if shacl.returncode != 0:
        failures.append(f"output does not conform to shapes/governance.shacl.ttl:\n{shacl.stdout[-1500:]}")

    if failures:
        print("sync_provenance_graph.py offline check FAILED:")
        for failure in failures:
            print(f"  - {failure}")
        sys.exit(1)
    print("sync_provenance_graph.py offline check passed.")


if __name__ == "__main__":
    main()
