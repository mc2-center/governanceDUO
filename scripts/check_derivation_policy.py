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
  - exactly one Flagged DerivationReview, for the Activity;
  - the sagebrain-shaped Association inherits the output's label through
    sagebrain:derived_from (a declared sub-property of prov:wasDerivedFrom).

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

PREFIXES = """
PREFIX sagegov: <https://sagebionetworks.org/governance/>
PREFIX syn: <https://www.synapse.org/Synapse:>
PREFIX association: <https://w3id.org/synapse/ad/association/>
"""

ASSERTIONS = {
    "output file syn70000003 is labeled Unclassified, citing both ARs, computed from gov:activity-7001": """
        ASK {
            ?label a sagegov:ControlLabel ;
                   sagegov:subject syn:syn70000003 ;
                   sagegov:dataTier "Unclassified" ;
                   sagegov:sourceAccessRequirements sagegov:AR-7001, sagegov:AR-7002 ;
                   sagegov:computedFrom sagegov:activity-7001 .
        }""",
    "Controlled input syn70000001 is labeled Controlled, citing gov:AR-7001": """
        ASK {
            ?label sagegov:subject syn:syn70000001 ;
                   sagegov:dataTier "Controlled" ;
                   sagegov:sourceAccessRequirements sagegov:AR-7001 .
        }""",
    "tierless input syn70000002 keeps an Unclassified label citing gov:AR-7002": """
        ASK {
            ?label sagegov:subject syn:syn70000002 ;
                   sagegov:dataTier "Unclassified" ;
                   sagegov:sourceAccessRequirements sagegov:AR-7002 .
        }""",
    "a Flagged DerivationReview exists for gov:activity-7001, linking both input labels": """
        ASK {
            ?review a sagegov:DerivationReview ;
                    sagegov:activity sagegov:activity-7001 ;
                    sagegov:reviewStatus "Flagged" ;
                    sagegov:inputLabels sagegov:control-label-syn70000001, sagegov:control-label-syn70000002 .
        }""",
    "the Association inherits syn70000003's label through sagebrain:derived_from": """
        ASK {
            ?label sagegov:subject association:fixture-assoc-01 ;
                   sagegov:dataTier "Unclassified" ;
                   sagegov:sourceAccessRequirements sagegov:AR-7001, sagegov:AR-7002 .
        }""",
}

REVIEW_COUNT = PREFIXES + "SELECT (COUNT(DISTINCT ?r) AS ?n) WHERE { ?r a sagegov:DerivationReview . }"


def main():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "derivation_policy.ttl"
        result = subprocess.run(
            [
                sys.executable,
                "scripts/build_derivation_policy.py",
                "--provenance-graph", str(FIXTURE / "provenance.ttl"),
                "--governance-graph", str(FIXTURE / "governance.ttl"),
                "--extra-graph", str(FIXTURE / "sagebrain.ttl"),
                "--derivation-rules", str(FIXTURE),
                "--access-requirement-dir", str(FIXTURE / "access_requirements"),
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

    failures = [name for name, query in ASSERTIONS.items() if not g.query(PREFIXES + query).askAnswer]
    reviews = int(next(iter(g.query(REVIEW_COUNT)))[0])
    if reviews != 1:
        failures.append(f"expected exactly 1 DerivationReview, got {reviews}")

    if failures:
        print("build_derivation_policy.py fixture check FAILED:")
        for failure in failures:
            print(f"  - {failure}")
        sys.exit(1)
    print(f"build_derivation_policy.py fixture check passed ({len(ASSERTIONS) + 1} assertions).")


if __name__ == "__main__":
    main()
