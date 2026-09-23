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
  - exactly one Activity node, minted as sagegov:activity-<n>, with both outputs
    as prov:generated;
  - exactly two prov:Usage nodes (no per-output duplication, the unrecognized
    entry skipped with a warning), the URL one named with sagegov:name;
  - createdOn/modifiedOn converted to epoch-millisecond integers;
  - every IRI is absolute (none resolved against a file path);
  - exactly the two expected prov:wasDerivedFrom edges, and the script reports 2.

Usage:
    python scripts/check_sync_provenance.py

author: orion.banks
"""

import contextlib
import io
import sys
import tempfile
import types
from pathlib import Path

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD

sys.path.insert(0, str(Path(__file__).parent))

PROV = Namespace("http://www.w3.org/ns/prov#")
GOV = Namespace("https://sagebionetworks.org/governance/")
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

    activities = set(g.subjects(RDF.type, PROV.Activity))
    if activities != {GOV["activity-9606"]}:
        failures.append(f"expected one Activity gov:activity-9606, got {sorted(activities)}")
    generated = set(g.objects(GOV["activity-9606"], PROV.generated))
    if generated != {SYN[e] for e in OUTPUTS}:
        failures.append(f"expected prov:generated {OUTPUTS}, got {sorted(generated)}")

    usages = set(g.subjects(RDF.type, PROV.Usage))
    if len(usages) != 2:
        failures.append(f"expected 2 prov:Usage nodes, got {len(usages)}")
    if (None, GOV.name, Literal("nf-core/rnaseq v3.11.1")) not in g:
        failures.append("URL Usage is missing sagegov:name")
    if "unrecognized Used.concreteType" not in stderr.getvalue():
        failures.append(f"expected a warning for the unrecognized Used entry; stderr was: {stderr.getvalue()!r}")

    for predicate, millis in ((GOV.createdOn, 1709294400000), (GOV.modifiedOn, 1709368200000)):
        values = set(g.objects(GOV["activity-9606"], predicate))
        if {(v.toPython(), v.datatype) for v in values} != {(millis, XSD.integer)}:
            failures.append(f"expected {predicate.n3()} {millis} (xsd:integer), got {sorted(values)}")

    relative = sorted(
        str(t) for triple in g for t in triple if isinstance(t, URIRef) and str(t).startswith("file:")
    )
    if relative:
        failures.append(f"relative IRIs resolved against a file path: {relative}")

    derived = set(g.subject_objects(PROV.wasDerivedFrom))
    expected_derived = {(SYN[e], SYN["syn10081783"]) for e in OUTPUTS}
    if derived != expected_derived:
        failures.append(f"expected wasDerivedFrom {sorted(expected_derived)}, got {sorted(derived)}")
    if "Derived 2 prov:wasDerivedFrom triples." not in stdout.getvalue():
        failures.append(f"expected the script to report 2 derived edges; stdout was: {stdout.getvalue()!r}")

    if failures:
        print("sync_provenance_graph.py offline check FAILED:")
        for failure in failures:
            print(f"  - {failure}")
        sys.exit(1)
    print("sync_provenance_graph.py offline check passed.")


if __name__ == "__main__":
    main()
