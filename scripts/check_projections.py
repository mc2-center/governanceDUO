"""
check_projections.py

Regression check for projections/authorizer_v1.rq, projections/authorizer_v1_teams.rq
and scripts/project.py (plans/model_refactor.md, Phase 2's "Projections"):

1. Golden diff: runs authorizer_v1.rq over the canonical example graph
   (linkml/examples/graph/rdf/governance_graph.ttl) at
   $GOVERNANCE_GRAPH_AS_OF_ISO and compares it with the pre-refactor
   tests/golden/governance_graph.ttl, restricted to the authorizer-relevant
   facts (AccessGrant, hasAccessRequirement, hasApproval -- extracted as
   semantic tuples, not raw triples, so grant IRIs are never compared; that's
   "grant IRIs" from the allowed-differences list). The allowed differences:
     - a bindingType of Inherited (the pre-refactor name) equals Inferred
       (decision 2 -- the AR-association in the golden file used the same
       BindingType vocabulary the AccessGrant did);
     - an extra hasAccessRequirement edge on the AR's own subject (an entity
       with a direct gov:requiresAR edge to that AR, read off the canonical
       graph) -- the golden export only recorded the edge on descendants;
   Any other difference (a missing grant, a missing/extra hasApproval, a
   hasAccessRequirement edge whose subject isn't the AR's own) fails.
2. Approval expiry (replaces check_approval_expiry.py): built at an --as-of one
   second before the canonical example's Approval's expiresAt, the holder gets
   gov:hasApproval; one second after, none does.
3. Team member grant: the canonical example's team member (synuser:2000001, via
   synteam:9000001) gets no gov:hasACL from authorizer_v1.rq alone, and gets
   exactly one (gov:viaTeam the team's old-namespace principal, same
   bindingType/permissions as the team's own grant) from authorizer_v1_teams.rq.
4. Descendant grant: an entity added in-memory with gov:benefactor pointing at
   syn10081783 (not itself) gets a materialized gov:AccessGrant with
   gov:bindingType gov:Inferred, while syn10081783's own grant stays gov:Direct.

Each assertion was confirmed able to fail by temporarily breaking its own
projection/script and re-running this check, then restoring (see the
implementation report).

Usage:
    python scripts/check_projections.py

author: orion.banks
"""

import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

from rdflib import Graph, Namespace
from rdflib.namespace import RDF

OLD = Namespace("https://sagebionetworks.org/governance/")
GOV = Namespace("https://w3id.org/synapse/governance#")
SYN = Namespace("https://www.synapse.org/Synapse:")

CANONICAL = "linkml/examples/graph/rdf/governance_graph.ttl"
GOLDEN = "tests/golden/governance_graph.ttl"
AUTHORIZER_QUERY = "projections/authorizer_v1.rq"
TEAMS_QUERY = "projections/authorizer_v1_teams.rq"
AS_OF = "2026-01-01T00:00:00Z"
# The canonical example's govid:approval/55001 gov:expiresAt (linkml/examples/
# graph/governance_graph.example.yaml).
APPROVAL_EXPIRES_AT = datetime(2026, 8, 14, 19, 33, 20, tzinfo=timezone.utc)

TEAM_MEMBER = OLD["principal-2000001"]
TEAM_PRINCIPAL = OLD["principal-9000001"]
DESCENDANT = SYN.syn99999998
BENEFACTOR = SYN.syn10081783

DESCENDANT_GRAPH = f"""
@prefix gov: <https://w3id.org/synapse/governance#> .
@prefix syn: <https://www.synapse.org/Synapse:> .
syn:syn99999998 a gov:SynapseEntity ; gov:benefactor syn:syn10081783 .
"""


def run_projection(graphs: list[str], query: str, as_of: str | None, out: Path) -> Graph:
    result = subprocess.run(
        [sys.executable, "scripts/project.py"]
        + [arg for g in graphs for arg in ("--graph", g)]
        + ["--query", query, "--out", str(out)]
        + (["--as-of", as_of] if as_of else []),
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"scripts/project.py failed for {query}:\n{result.stderr}")
        sys.exit(1)
    return Graph().parse(out)


# --- golden diff: semantic extraction, not raw triples -----------------------


def grants(g: Graph) -> set[tuple]:
    """(entity, principal, permission, bindingType) -- one tuple per permission
    on a grant, bindingType normalized Inherited -> Inferred."""
    out = set()
    for e, grant in g.subject_objects(OLD.hasACL):
        if (grant, RDF.type, OLD.AccessGrant) not in g:
            continue
        principal = g.value(grant, OLD.principal)
        binding = g.value(grant, OLD.bindingType)
        binding = OLD.Inferred if binding == OLD.Inherited else binding
        for perm in g.objects(grant, OLD.permission):
            out.add((str(e), str(principal), str(perm), str(binding)))
    return out


def has_ar(g: Graph) -> set[tuple]:
    return {(str(e), str(ar)) for e, ar in g.subject_objects(OLD.hasAccessRequirement)}


def has_approval(g: Graph) -> set[tuple]:
    return {(str(p), str(ar)) for p, ar in g.subject_objects(OLD.hasApproval)}


def old_ar_iri(ar_iri) -> str:
    return str(OLD[f"AR-{str(ar_iri).rsplit('/', 1)[-1]}"])


def direct_ar_subjects(canonical: Graph) -> set[tuple]:
    """(entity, old-namespace AR IRI) for every gov:requiresAR edge asserted
    directly in the canonical graph: an entity that requires the AR itself, not
    only through a gov:parent ancestor. authorizer_v1.rq emits
    hasAccessRequirement on these too (per its header); the golden export
    didn't, so an extra edge here is allowed."""
    return {(str(e), old_ar_iri(ar)) for e, ar in canonical.subject_objects(GOV.requiresAR)}


def golden_diff_failures(tmp: Path) -> list[str]:
    failures = []
    ours = run_projection([CANONICAL], AUTHORIZER_QUERY, AS_OF, tmp / "authorizer_v1.ttl")
    golden = Graph().parse(GOLDEN)
    canonical = Graph().parse(CANONICAL)

    g_grants, o_grants = grants(golden), grants(ours)
    if g_grants != o_grants:
        failures.append(
            f"AccessGrant golden diff: missing {sorted(g_grants - o_grants)}, "
            f"unexplained extra {sorted(o_grants - g_grants)}"
        )

    allowed_extra = direct_ar_subjects(canonical)
    g_ar, o_ar = has_ar(golden), has_ar(ours)
    missing_ar = g_ar - o_ar
    extra_ar = (o_ar - g_ar) - allowed_extra
    if missing_ar or extra_ar:
        failures.append(
            f"hasAccessRequirement golden diff: missing {sorted(missing_ar)}, "
            f"unexplained extra {sorted(extra_ar)}"
        )

    g_appr, o_appr = has_approval(golden), has_approval(ours)
    if g_appr != o_appr:
        failures.append(
            f"hasApproval golden diff: missing {sorted(g_appr - o_appr)}, "
            f"unexplained extra {sorted(o_appr - g_appr)}"
        )
    return failures


# --- approval expiry -----------------------------------------------------------


def approval_expiry_failures(tmp: Path) -> list[str]:
    failures = []
    one_second = timedelta(seconds=1)
    before_iso = (APPROVAL_EXPIRES_AT - one_second).isoformat().replace("+00:00", "Z")
    after_iso = (APPROVAL_EXPIRES_AT + one_second).isoformat().replace("+00:00", "Z")
    before = run_projection([CANONICAL], AUTHORIZER_QUERY, before_iso, tmp / "before.ttl")
    after = run_projection([CANONICAL], AUTHORIZER_QUERY, after_iso, tmp / "after.ttl")
    if (TEAM_MEMBER, OLD.hasApproval, OLD["AR-42"]) not in before:
        failures.append("before expiresAt: expected the holder to have gov:hasApproval gov:AR-42")
    lingering = sorted((s.n3(), o.n3()) for s, o in after.subject_objects(OLD.hasApproval))
    if lingering:
        failures.append(f"after expiresAt: expected no gov:hasApproval, got {lingering}")
    return failures


# --- team member grant ----------------------------------------------------------


def team_member_failures(tmp: Path) -> list[str]:
    failures = []
    base = run_projection([CANONICAL], AUTHORIZER_QUERY, AS_OF, tmp / "base.ttl")
    teams = run_projection([CANONICAL], TEAMS_QUERY, AS_OF, tmp / "teams.ttl")

    base_member_grants = list(base.subjects(OLD.principal, TEAM_MEMBER))
    if base_member_grants:
        failures.append(f"authorizer_v1.rq alone granted the team member: {base_member_grants}")

    teams_member_grants = [g for g in teams.subjects(OLD.principal, TEAM_MEMBER)
                            if (g, RDF.type, OLD.AccessGrant) in teams]
    if len(teams_member_grants) != 1:
        failures.append(f"expected exactly one flattened grant for the team member, got {teams_member_grants}")
    else:
        grant = teams_member_grants[0]
        if teams.value(grant, OLD.viaTeam) != TEAM_PRINCIPAL:
            failures.append(f"expected {grant} gov:viaTeam {TEAM_PRINCIPAL}, got {teams.value(grant, OLD.viaTeam)}")
        if teams.value(grant, OLD.bindingType) != OLD.Direct:
            failures.append("expected the flattened grant's bindingType to copy the team grant's (Direct)")
    return failures


# --- descendant grant -------------------------------------------------------------


def descendant_failures(tmp: Path) -> list[str]:
    failures = []
    extra = tmp / "descendant.ttl"
    extra.write_text(DESCENDANT_GRAPH)
    ours = run_projection([CANONICAL, str(extra)], AUTHORIZER_QUERY, AS_OF, tmp / "descendant_out.ttl")

    benefactor_grants = [g for g in ours.objects(BENEFACTOR, OLD.hasACL)]
    descendant_grants = [g for g in ours.objects(DESCENDANT, OLD.hasACL)]
    if len(benefactor_grants) != 1 or ours.value(benefactor_grants[0], OLD.bindingType) != OLD.Direct:
        failures.append(f"expected {BENEFACTOR}'s own grant to stay Direct")
    if len(descendant_grants) != 1 or ours.value(descendant_grants[0], OLD.bindingType) != OLD.Inferred:
        failures.append("expected the descendant's materialized grant to be Inferred")
    return failures


def main():
    failures = []
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp = Path(tmp_dir)
        failures += golden_diff_failures(tmp)
        failures += approval_expiry_failures(tmp)
        failures += team_member_failures(tmp)
        failures += descendant_failures(tmp)

    if failures:
        print("projections check FAILED:")
        for failure in failures:
            print(f"  - {failure}")
        sys.exit(1)
    print("projections check passed: golden diff, approval expiry, team-member and descendant grants.")


if __name__ == "__main__":
    main()
