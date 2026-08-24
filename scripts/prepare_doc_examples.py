"""
prepare_doc_examples.py

gen-doc only embeds an example on a class's generated reference page if the example
file is named <ClassName>-<ExampleName>.<ext> in its --example-directory. The real
example instances under linkml/examples/ don't follow that convention (and are
referenced by their current names elsewhere, e.g. the Makefile's example-rdf/
governance-graph/policy-fabric targets and scripts/*.py) — so this script copies each
one to a correctly-named file under a separate, build-time-only directory instead of
renaming it in place.

Usage:
    python scripts/prepare_doc_examples.py [--examples-dir linkml/examples]
                                            [--out-dir docs/example_instances]

author: orion.banks
"""

import argparse
import shutil
from pathlib import Path

# source path (relative to --examples-dir) -> destination filename (<ClassName>-<name>.yaml)
EXAMPLE_MAP = {
    "access_requirement.example.yaml": "AccessRequirement-001.yaml",
    "access_requirement_policy_fabric.example.yaml": "AccessRequirement-002-policy-fabric.yaml",
    "study.example.yaml": "Study-001.yaml",
    "governance_graph/access_grant.example.yaml": "AccessGrant-001.yaml",
    "governance_graph/access_requirement_association.example.yaml": "AccessRequirementAssociation-001.yaml",
    "governance_graph/data_access_submission.example.yaml": "DataAccessSubmission-001.yaml",
    "governance_graph/data_access_submission_status.example.yaml": "DataAccessSubmissionStatus-001.yaml",
    "governance_graph/principal_team_x.example.yaml": "Principal-001-team-x.yaml",
    "governance_graph/principal_user_2000001.example.yaml": "Principal-002-user.yaml",
    "governance_graph/synapse_entity_file.example.yaml": "SynapseEntity-001-file.yaml",
    "governance_graph/synapse_entity_study.example.yaml": "SynapseEntity-002-study.yaml",
}


def main():
    parser = argparse.ArgumentParser(
        description="Copy linkml/examples/*.yaml into gen-doc's <ClassName>-<name>.yaml convention."
    )
    parser.add_argument("--examples-dir", default="linkml/examples")
    parser.add_argument("--out-dir", default="docs/example_instances")
    args = parser.parse_args()

    examples_dir = Path(args.examples_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for src_rel, dest_name in EXAMPLE_MAP.items():
        src = examples_dir / src_rel
        dest = out_dir / dest_name
        shutil.copyfile(src, dest)
        print(f"{src} -> {dest}")


if __name__ == "__main__":
    main()
