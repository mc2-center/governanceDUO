"""
check_derivation_policy.py

Regression check for scripts/build_derivation_policy.py: runs it on the committed
fixture in linkml/examples/derivation_policy/fixture/ (see that directory's
README.md) and asserts the output with SPARQL ASK queries:
  - the Activity's output carries the max-rank label (Unclassified, from a
    Controlled input plus a tierless one), citing both ARs, computed from the
    Activity;
  - the tierless input keeps an Unclassified label with its
    sourceAccessRequirements (fail closed, not dropped);
  - syn70000013, bound directly to a Private AR and derived from two Controlled
    inputs a Controlled rule covers, stays Private (a rule never lowers an
    entity's own binding);
  - Flagged DerivationReviews for govid:activity/7001 (disjoint ARs),
    govid:activity/7002 (the rule, per its notes) and govid:activity/7003 (three
    inputs sharing one AR, flagged because the rule covers each pair), and for
    govid:activity/7005, whose notes lead with the Private+Private rule that
    forbids it ahead of the Controlled+Controlled review rule -- exactly four;
  - the Controlled+Private rule lowers unbound syn70000016 (from a Controlled
    and a Private input) to Controlled, and flags nothing;
  - syn70000019, whose only Access Requirement binding is its parent's
    (gov:parent syn70000011, bound to ar/7003), gets ar/7003's Controlled tier
    on its own ControlLabel -- the gov:parent ancestor walk
    (entity_access_requirements()) reaching a child through no binding of its
    own, not just a derivation (prov) ancestor;
  - the sagebrain-shaped Association inherits the output's label through
    sagebrain:derived_from (a declared sub-property of prov:wasDerivedFrom);
  - the output, merged with its three input graphs, conforms to
    shapes/governance.shacl.ttl (ont shapes/governance.owl.ttl) -- replacing the
    pre-refactor pipeline's domain/range check now that both TBoxes are one
    generated TBox and shape set.

Usage:
    python scripts/check_derivation_policy.py

author: orion.banks
"""

import subprocess
import sys
import tempfile
from pathlib import Path

from rdflib import Graph

FIXTURE = Path("linkml/examples/derivation_policy/fixture")
SHAPES = "shapes/governance.shacl.ttl"
ONT = "shapes/governance.owl.ttl"

PREFIXES = """
PREFIX gov: <https://w3id.org/synapse/governance#>
PREFIX syn: <https://www.synapse.org/Synapse:>
PREFIX association: <https://w3id.org/synapse/ad/association/>
"""

ASSERTIONS = {
    "output file syn70000003 is labeled Unclassified, citing both ARs, computed from govid:activity/7001": """
        ASK {
            ?label a gov:ControlLabel ;
                   gov:subject syn:syn70000003 ;
                   gov:dataTier gov:UnclassifiedTier ;
                   gov:sourceAccessRequirements <https://w3id.org/synapse/governance/ar/7001>, <https://w3id.org/synapse/governance/ar/7002> ;
                   gov:computedFrom <https://w3id.org/synapse/governance/activity/7001> .
        }""",
    "Controlled input syn70000001 is labeled Controlled, citing govid:ar/7001": """
        ASK {
            ?label gov:subject syn:syn70000001 ;
                   gov:dataTier gov:ControlledTier ;
                   gov:sourceAccessRequirements <https://w3id.org/synapse/governance/ar/7001> .
        }""",
    "tierless input syn70000002 keeps an Unclassified label citing govid:ar/7002": """
        ASK {
            ?label gov:subject syn:syn70000002 ;
                   gov:dataTier gov:UnclassifiedTier ;
                   gov:sourceAccessRequirements <https://w3id.org/synapse/governance/ar/7002> .
        }""",
    "a Flagged DerivationReview exists for govid:activity/7001, linking both input labels": """
        ASK {
            ?review a gov:DerivationReview ;
                    gov:activity <https://w3id.org/synapse/governance/activity/7001> ;
                    gov:reviewStatus gov:DerivationFlagged ;
                    gov:inputLabels ?l1, ?l2 .
            ?l1 gov:subject syn:syn70000001 .
            ?l2 gov:subject syn:syn70000002 .
        }""",
    "syn70000013 keeps its own Private tier despite the Controlled+Controlled rule": """
        ASK {
            ?label gov:subject syn:syn70000013 ;
                   gov:dataTier gov:PrivateTier ;
                   gov:sourceAccessRequirements <https://w3id.org/synapse/governance/ar/7003>, <https://w3id.org/synapse/governance/ar/7004> .
        }""",
    "govid:activity/7002 is flagged by the Controlled+Controlled rule, not disjointness": """
        ASK {
            ?review gov:activity <https://w3id.org/synapse/governance/activity/7002> ; gov:reviewStatus gov:DerivationFlagged ;
                    gov:reviewNotes ?notes .
            FILTER(CONTAINS(?notes, "derivation_rule.fixture-controlled-pair requires review"))
            FILTER(!CONTAINS(?notes, "disjoint"))
        }""",
    "three-input govid:activity/7003 is flagged by the pairwise rule, not disjointness": """
        ASK {
            ?review gov:activity <https://w3id.org/synapse/governance/activity/7003> ; gov:reviewStatus gov:DerivationFlagged ;
                    gov:reviewNotes ?notes .
            FILTER(CONTAINS(?notes, "derivation_rule.fixture-controlled-pair requires review"))
            FILTER(!CONTAINS(?notes, "disjoint"))
        }""",
    "the Controlled+Private rule lowers unbound syn70000016 from Private to Controlled": """
        ASK { ?label gov:subject syn:syn70000016 ; gov:dataTier gov:ControlledTier . }""",
    "govid:activity/7004 (Controlled+Private, not flagged, not disjoint) has no review": """
        ASK { FILTER NOT EXISTS { ?review gov:activity <https://w3id.org/synapse/governance/activity/7004> } }""",
    "govid:activity/7005's notes lead with the forbidding rule and keep the review one": """
        ASK {
            ?review gov:activity <https://w3id.org/synapse/governance/activity/7005> ; gov:reviewNotes ?notes .
            FILTER(STRSTARTS(?notes, "DerivationRule derivation_rule.fixture-private-pair forbids"))
            FILTER(CONTAINS(?notes, "derivation_rule.fixture-controlled-pair requires review"))
        }""",
    "syn70000019 has no requiresAR of its own but inherits ar/7003's Controlled tier through gov:parent syn70000011": """
        ASK {
            ?label gov:subject syn:syn70000019 ;
                   gov:dataTier gov:ControlledTier ;
                   gov:sourceAccessRequirements <https://w3id.org/synapse/governance/ar/7003> .
        }""",
    "the Association inherits syn70000003's label through sagebrain:derived_from": """
        ASK {
            ?label gov:subject association:fixture-assoc-01 ;
                   gov:dataTier gov:UnclassifiedTier ;
                   gov:sourceAccessRequirements <https://w3id.org/synapse/governance/ar/7001>, <https://w3id.org/synapse/governance/ar/7002> .
        }""",
}

REVIEW_COUNT = PREFIXES + "SELECT (COUNT(DISTINCT ?r) AS ?n) WHERE { ?r a gov:DerivationReview . }"

FIXTURE_INPUTS = (FIXTURE / "governance.ttl", FIXTURE / "provenance.ttl", FIXTURE / "sagebrain.ttl")


def main():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "derivation_policy.ttl"
        result = subprocess.run(
            [
                sys.executable,
                "scripts/build_derivation_policy.py",
                "--graph", str(FIXTURE / "governance.ttl"),
                "--graph", str(FIXTURE / "provenance.ttl"),
                "--extra-graph", str(FIXTURE / "sagebrain.ttl"),
                "--derivation-rules", str(FIXTURE),
                "--out", str(out),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print("build_derivation_policy.py failed:")
            print(result.stderr)
            sys.exit(1)
        g = Graph().parse(out)

        merged = Graph().parse(out)
        for path in FIXTURE_INPUTS:
            merged.parse(path)
        merged_path = Path(tmp) / "merged.ttl"
        merged.serialize(destination=str(merged_path), format="turtle")
        shacl = subprocess.run(
            [sys.executable, "scripts/validate_graph.py", "--data", str(merged_path),
             "--shapes", SHAPES, "--ont", ONT],
            capture_output=True, text=True,
        )

    failures = [name for name, query in ASSERTIONS.items() if not g.query(PREFIXES + query).askAnswer]
    reviews = int(next(iter(g.query(REVIEW_COUNT)))[0])
    if reviews != 4:
        failures.append(f"expected exactly 4 DerivationReviews, got {reviews}")
    if shacl.returncode != 0:
        failures.append(
            f"the output merged with its inputs does not conform to {SHAPES}:\n{shacl.stdout[-1500:]}"
        )

    if failures:
        print("build_derivation_policy.py fixture check FAILED:")
        for failure in failures:
            print(f"  - {failure}")
        sys.exit(1)
    print(f"build_derivation_policy.py fixture check passed ({len(ASSERTIONS) + 1} assertions).")


if __name__ == "__main__":
    main()
