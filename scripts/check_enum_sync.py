"""
check_enum_sync.py

GrantPermissionEnum (AccessGrant.permission's range) lists AccessTypeEnum's
values again, plus the derived ACCESS, because LinkML's `inherits:` isn't
expanded by linkml-validate, gen-owl or gen-shacl (plans/enum_values_match_owl.md).
This check keeps the copy exact: the same values with the same meaning: IRIs,
and ACCESS as the only addition. A Synapse ACCESS_TYPE added to one enum but not
the other fails here.

Usage:
    python scripts/check_enum_sync.py [--schema linkml/governance_duo.linkml.yaml]

author: orion.banks
"""

import argparse
import sys

from linkml_runtime.utils.schemaview import SchemaView

DERIVED = {"ACCESS"}


def meanings(sv: SchemaView, enum_name: str) -> dict:
    return {k: v.meaning for k, v in sv.get_enum(enum_name).permissible_values.items()}


def main():
    parser = argparse.ArgumentParser(description="Check GrantPermissionEnum mirrors AccessTypeEnum plus ACCESS.")
    parser.add_argument("--schema", default="linkml/governance_duo.linkml.yaml")
    args = parser.parse_args()

    sv = SchemaView(args.schema)
    synapse = meanings(sv, "AccessTypeEnum")
    grant = meanings(sv, "GrantPermissionEnum")
    failures = []
    for value in sorted(synapse.keys() - grant.keys()):
        failures.append(f"AccessTypeEnum.{value} is missing from GrantPermissionEnum")
    for value in sorted(grant.keys() - synapse.keys() - DERIVED):
        failures.append(f"GrantPermissionEnum.{value} is neither an AccessTypeEnum value nor derived ({', '.join(DERIVED)})")
    for value in sorted(DERIVED - grant.keys()):
        failures.append(f"GrantPermissionEnum is missing the derived {value}")
    for value in sorted(synapse.keys() & grant.keys()):
        if synapse[value] != grant[value]:
            failures.append(f"{value}: meaning {grant[value]} in GrantPermissionEnum, {synapse[value]} in AccessTypeEnum")

    if failures:
        print("FAIL  GrantPermissionEnum is out of step with AccessTypeEnum:")
        for failure in failures:
            print(f"        - {failure}")
        sys.exit(1)
    print(f"Enum sync: GrantPermissionEnum = AccessTypeEnum's {len(synapse)} values + {', '.join(sorted(DERIVED))}.")


if __name__ == "__main__":
    main()
