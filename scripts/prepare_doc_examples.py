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
# The pre-refactor governance_graph/ entries (AccessGrant, SynapseEntity, ...)
# are gone: those record-layer classes moved to the graph layer
# (linkml/graph/governance.yaml), which gen-doc doesn't render from this
# schema, and their facts now live in the canonical example
# (linkml/examples/graph/governance_graph.example.yaml) -- see
# plans/model_refactor.md.
EXAMPLE_MAP = {
    "access_requirement.example.yaml": "AccessRequirement-001.yaml",
    "access_requirement_policy_fabric.example.yaml": "AccessRequirement-002-policy-fabric.yaml",
    "study.example.yaml": "Study-001.yaml",
    "derivation_policy/derivation_rule.example.yaml": "DerivationRule-001.yaml",
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
