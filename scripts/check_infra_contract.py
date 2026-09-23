"""
check_infra_contract.py

Contract check between this repo's exported governance graph and
sagebrain-infra's authorizer (src/lambda_rebac/authorize.py), which queries the
graph in Neptune to decide whether a principal may take the Cedar action ACCESS
on a Synapse resource. sagebrain-infra's query worker (src/lambda/query.py)
always asks for action "ACCESS" with the requesting user's numeric Synapse id.

Runs against governance_graph_export/authorizer_v1.ttl (projections/authorizer_v1.rq
over the canonical example, plans/model_refactor.md) plus one in-memory test
grant on syn10081783, and asserts:
  - principal 9000001 (the canonical example's team grant: DOWNLOAD, so also the
    derived ACCESS) is allowed, and gov:AR-42 comes back as the resource's
    AccessRequirement;
  - principal 8000001, holding only a READ grant, is denied;
  - principal 7777777, with no grant, is denied.

Two modes:
  - default: runs tests/infra_contract/authorize_query.rq (a verbatim, pinned copy
    of authorize.py's query) and re-implements only authorize.py's comparison
    rules (principal IRI suffix match, permission local name == action);
  - --infra PATH (or SAGEBRAIN_INFRA=PATH via make): imports sagebrain-infra's own
    authorize.py and calls its real _authorize_resource(), with Neptune replaced by
    a local SPARQL query built from infra's own _governance_query() and the Cedar
    policy call (Amazon Verified Permissions) stubbed to "allow when a grant
    matches" -- so drift between the copy and infra's code is caught, and the
    graph contract (does a matching grant exist?) is exercised by infra's logic.
    PATH is an infra checkout (with src/lambda_rebac/authorize.py present, i.e.
    the policy-engine branch) or the authorize.py file itself.

Usage:
    python scripts/check_infra_contract.py [--graph governance_graph_export/authorizer_v1.ttl]
                                           [--infra PATH]

author: orion.banks
"""

import argparse
import importlib.util
import os
import sys
import types
from pathlib import Path

from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF

QUERY_FILE = Path("tests/infra_contract/authorize_query.rq")
ACTION = "ACCESS"
RESOURCE_ID = "syn10081783"
EXPECTED_AR = "https://sagebionetworks.org/governance/AR-42"
SYNAPSE_PREFIX = "https://www.synapse.org/Synapse:"

GOV = Namespace("https://sagebionetworks.org/governance/")
SYN = Namespace(SYNAPSE_PREFIX)

# principal id -> expected decision
CASES = {
    "9000001": "ALLOW",
    "8000001": "DENY",
    "7777777": "DENY",
}


def load_graph(path: str) -> Graph:
    """The exported governance graph plus a READ-only grant for principal 8000001
    on the same resource, so the READ-vs-ACCESS rule is exercised."""
    g = Graph().parse(path)
    grant = GOV["grant-contract-check-read-only"]
    g.add((grant, RDF.type, GOV.AccessGrant))
    g.add((grant, GOV.principal, GOV["principal-8000001"]))
    g.add((grant, GOV.permission, GOV.READ))
    g.add((grant, GOV.bindingType, GOV.Direct))
    g.add((SYN[RESOURCE_ID], GOV.hasACL, grant))
    return g


def run_sparql(g: Graph, query: str) -> list[dict]:
    """Runs `query` locally and returns rows in SPARQL 1.1 JSON results shape
    (the shape authorize.py reads from Neptune's response)."""
    rows = []
    for row in g.query(query):
        rows.append({str(k): {"value": str(v)} for k, v in row.asdict().items() if v is not None})
    return rows


# --- default mode: pinned query copy + authorize.py's comparison rules ---------


def resource_iri(resource_id: str) -> str:
    if resource_id.startswith(("http://", "https://")):
        return resource_id
    if resource_id.startswith("syn:"):
        return f"{SYNAPSE_PREFIX}{resource_id[4:]}"
    if resource_id.startswith("syn"):
        return f"{SYNAPSE_PREFIX}{resource_id}"
    return resource_id


def local_name(uri: str) -> str:
    for sep in ("#", "/", ":"):
        if sep in uri:
            return uri.rsplit(sep, 1)[1]
    return uri


def principal_matches(grant_principal: str, principal_id: str) -> bool:
    return grant_principal == principal_id or grant_principal.endswith(f"principal-{principal_id}")


def decide_with_copy(g: Graph, principal_id: str) -> tuple[str, list[str]]:
    template = "\n".join(
        line for line in QUERY_FILE.read_text().splitlines() if not line.startswith("#")
    )
    rows = run_sparql(g, template.replace("{resource_iri}", resource_iri(RESOURCE_ID)))
    ars = sorted({r["accessRequirement"]["value"] for r in rows if "accessRequirement" in r})
    matching = [
        r
        for r in rows
        if all(k in r for k in ("grant", "grantPrincipal", "permission", "bindingType"))
        and local_name(r["permission"]["value"]) == ACTION
        and principal_matches(r["grantPrincipal"]["value"], principal_id)
    ]
    return ("ALLOW" if matching else "DENY"), ars


# --- --infra mode: infra's own authorize.py -------------------------------------


def load_infra_authorize(path: str):
    target = Path(path)
    if target.is_dir():
        target = target / "src" / "lambda_rebac" / "authorize.py"
    if not target.exists():
        sys.exit(
            f"{target} not found -- point --infra at a sagebrain-infra checkout on a branch "
            "that has src/lambda_rebac/authorize.py (e.g. policy-engine), or at the file itself."
        )
    for name in ("boto3", "botocore", "botocore.session", "botocore.auth", "botocore.awsrequest",
                 "botocore.exceptions", "requests"):
        sys.modules.setdefault(name, types.ModuleType(name))
    sys.modules["boto3"].client = lambda *args, **kwargs: None
    sys.modules["botocore.auth"].SigV4Auth = object
    sys.modules["botocore.awsrequest"].AWSRequest = object
    sys.modules["botocore.exceptions"].BotoCoreError = Exception
    sys.modules["botocore.exceptions"].ClientError = Exception
    for key in ("NEPTUNE_ENDPOINT", "AWS_REGION", "AVP_POLICY_STORE_ID"):
        os.environ.setdefault(key, "contract-check")
    spec = importlib.util.spec_from_file_location("infra_authorize", target)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def decide_with_infra(authorize, g: Graph, principal_id: str) -> tuple[str, list[str]]:
    authorize._query_governance = lambda iri: run_sparql(g, authorize._governance_query(iri))
    authorize._avp_is_allowed = lambda **kw: (
        kw["principal_matches_grant"] and kw["permission_matches_grant"],
        ["contract-check-stub"],
    )
    result = authorize._authorize_resource(principal_id, ACTION, RESOURCE_ID, None, "intersection")
    return result["decision"], sorted(result.get("access_requirements", []))


def main():
    parser = argparse.ArgumentParser(description="Governance graph <-> sagebrain-infra authorizer contract check.")
    parser.add_argument("--graph", default="governance_graph_export/authorizer_v1.ttl")
    parser.add_argument("--infra", default=os.environ.get("SAGEBRAIN_INFRA") or None)
    args = parser.parse_args()

    g = load_graph(args.graph)
    if args.infra:
        authorize = load_infra_authorize(args.infra)
        mode = f"sagebrain-infra authorize.py ({args.infra})"
        decide = lambda principal_id: decide_with_infra(authorize, g, principal_id)  # noqa: E731
    else:
        mode = f"pinned query copy ({QUERY_FILE})"
        decide = lambda principal_id: decide_with_copy(g, principal_id)  # noqa: E731

    failures = []
    for principal_id, expected in CASES.items():
        decision, ars = decide(principal_id)
        if decision != expected:
            failures.append(f"principal {principal_id}: expected {expected}, got {decision}")
        if EXPECTED_AR not in ars:
            failures.append(f"principal {principal_id}: expected {EXPECTED_AR} among ARs, got {ars}")

    if failures:
        print(f"infra contract check FAILED [{mode}]:")
        for failure in failures:
            print(f"  - {failure}")
        sys.exit(1)
    print(f"infra contract check passed [{mode}]: {len(CASES)} principals on {RESOURCE_ID}.")


if __name__ == "__main__":
    main()
