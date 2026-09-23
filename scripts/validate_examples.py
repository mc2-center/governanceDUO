"""
validate_examples.py

Runs LinkML validation (the same JSON Schema check `linkml-validate` runs) over
every example instance under linkml/examples/ (plans/pre_pr_review_fixes.md,
finding 8). This is the only place the schema's DUO conditional `rules:` are
enforced: gen-shacl doesn't compile them and build_owl.py leaves them out of the
OWL, so without this a rule-violating example would pass validate-all.

Each example's target class comes from the manifests the converters already use
-- convert_examples_to_rdf.EXAMPLE_CLASSES and
build_governance_graph.EXAMPLE_CLASSES -- plus EXTRA_CLASSES for examples no
converter reads. An example with no mapped class fails the check rather than
being skipped. The records the regression fixtures feed the builders
(FIXTURE_RECORDS) are validated too, so a fixture can't pass the builders a
record the schema rejects.

Usage:
    python scripts/validate_examples.py [--schema linkml/governance_duo.linkml.yaml]

author: orion.banks
"""

import argparse
import sys
from pathlib import Path

import yaml
from linkml.validator import Validator
from linkml.validator.plugins import JsonschemaValidationPlugin

sys.path.insert(0, str(Path(__file__).parent))
from build_governance_graph import EXAMPLE_CLASSES as GOVERNANCE_GRAPH_CLASSES  # noqa: E402
from convert_examples_to_rdf import EXAMPLE_CLASSES  # noqa: E402

EXAMPLES = Path("linkml/examples")
# Examples read by neither converter (build_policy_fabric.py takes this one by path).
EXTRA_CLASSES = {"access_requirement_policy_fabric": "AccessRequirement"}
# Fixture records (glob -> class) read by check_derivation_policy.py and
# check_sync_governance.py.
FIXTURE_RECORDS = {
    "linkml/examples/derivation_policy/fixture/access_requirements/*.yaml": "AccessRequirement",
    "linkml/examples/derivation_policy/fixture/derivation_rule.*.yaml": "DerivationRule",
    "tests/sync_governance/access_requirements/*.yaml": "AccessRequirement",
}


def target_class(path: Path) -> str | None:
    stem = path.name.removesuffix(".example.yaml")
    manifest = GOVERNANCE_GRAPH_CLASSES if path.parent.name == "governance_graph" else EXAMPLE_CLASSES
    return manifest.get(stem) or EXTRA_CLASSES.get(stem)


def main():
    parser = argparse.ArgumentParser(description="linkml-validate every example under linkml/examples/.")
    parser.add_argument("--schema", default="linkml/governance_duo.linkml.yaml")
    args = parser.parse_args()

    validator = Validator(args.schema, validation_plugins=[JsonschemaValidationPlugin(closed=True)])
    failures = []
    examples = [(path, target_class(path)) for path in sorted(EXAMPLES.rglob("*.example.yaml"))]
    for pattern, class_name in FIXTURE_RECORDS.items():
        matches = sorted(Path().glob(pattern))
        if not matches:
            failures.append(f"{pattern}: no fixture records found (moved?)")
        examples += [(path, class_name) for path in matches]
    for path, class_name in examples:
        if class_name is None:
            failures.append(f"{path}: no target class mapped (add it to a converter's EXAMPLE_CLASSES)")
            continue
        for result in validator.validate(yaml.safe_load(path.read_text()), class_name).results:
            failures.append(f"{path} ({class_name}): {result.message}")

    if failures:
        print(f"FAIL  {len(failures)} example validation error(s):")
        for failure in failures:
            print(f"        - {failure}")
        sys.exit(1)
    print(f"linkml-validate: all {len(examples)} examples and fixture records conform (including the DUO rules).")


if __name__ == "__main__":
    main()
