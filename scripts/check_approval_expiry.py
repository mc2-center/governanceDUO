"""
check_approval_expiry.py

Regression check for gov:hasApproval (plans/pre_pr_review_fixes.md, finding 9):
it must come only from an AccessApproval that still holds -- status APPROVED and
expiredOn not yet passed -- never from a Submission that was once APPROVED.

Builds the worked governance-graph example twice with
scripts/build_governance_graph.py, as of one millisecond before and one
millisecond after the example AccessApproval's expiredOn. It builds from a copy
of the examples whose DataAccessSubmissionStatus is set to APPROVED, so the
Submission path is exercised too. Asserts:
  - before: the accessor has gov:hasApproval to the approval's AR;
  - after: no gov:hasApproval triple exists at all -- the APPROVED Submission
    contributes none.

Usage:
    python scripts/check_approval_expiry.py

author: orion.banks
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
from rdflib import Graph, Namespace

GOV = Namespace("https://sagebionetworks.org/governance/")
EXAMPLES = Path("linkml/examples/governance_graph")
APPROVAL = EXAMPLES / "access_approval.example.yaml"
STATUS = "data_access_submission_status.example.yaml"


def build(examples: Path, as_of_ms: int, out: Path) -> Graph:
    subprocess.run(
        [
            sys.executable, "scripts/build_governance_graph.py",
            "--examples-dir", str(examples), "--out", str(out), "--as-of", str(as_of_ms),
        ],
        check=True,
        capture_output=True,
    )
    return Graph().parse(out)


def main():
    approval = yaml.safe_load(APPROVAL.read_text())
    accessor = GOV[f"principal-{approval['accessorId']}"]
    ar = GOV[approval["requirementId"].replace("access_requirement.", "AR-")]
    expired_on = approval["expiredOn"]

    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        examples = Path(tmp) / "examples"
        shutil.copytree(EXAMPLES, examples)
        status = yaml.safe_load((examples / STATUS).read_text())
        status["state"] = "APPROVED"
        (examples / STATUS).write_text(yaml.safe_dump(status))
        before = build(examples, expired_on - 1, Path(tmp) / "before.ttl")
        after = build(examples, expired_on + 1, Path(tmp) / "after.ttl")
    if (accessor, GOV.hasApproval, ar) not in before:
        failures.append(f"before expiredOn: expected {accessor.n3()} gov:hasApproval {ar.n3()}")
    lingering = sorted((s.n3(), o.n3()) for s, o in after.subject_objects(GOV.hasApproval))
    if lingering:
        failures.append(f"after expiredOn: expected no gov:hasApproval, got {lingering}")

    if failures:
        print("gov:hasApproval expiry check FAILED:")
        for failure in failures:
            print(f"  - {failure}")
        sys.exit(1)
    print("gov:hasApproval expiry check passed: present before the approval's expiredOn, absent after.")


if __name__ == "__main__":
    main()
