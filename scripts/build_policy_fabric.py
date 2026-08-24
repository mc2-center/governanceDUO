"""
build_policy_fabric.py

Given a governanceDUO AccessRequirement instance (e.g. one of
linkml/examples/*.example.yaml), emits the three artifacts Policy Fabric
(https://github.com/hasan7n/tmp-policies) actually consumes, using
linkml/policy_fabric_bindings.yaml as the DUO-code -> reference-value/credential
crosswalk (verified directly against that repo's policy.rego/policy_data_schema.json
files, not inferred):

- policy_data.json      — the merged "Reference Values Schema" across every DUO code
                          in the instance's dataUseModifiers, keyed by each binding's
                          referenceValueKeys and populated from the paired sourceSlot
                          in that binding's referenceValueSources (a binding can need
                          more than one key, each from a different slot — e.g.
                          time-limit-on-use's requiredDocumentID and notAfter).
- associated_credentials.json — deduplicated {credentialType, requiredClaims} list
                          across those same DUO codes' bindings.
- asset_registration.json — {name, did, metadata: {data_source, guardian_url}},
                          shaped exactly like the real Django Asset model
                          (tools/asset_registry/app/models.py: name, did, metadata).

A referenceValueKey with no matching entry in referenceValueSources (a documented
gap — see policy_fabric_bindings.yaml's `notes`) contributes no key to
policy_data.json and is reported on stderr rather than silently dropped. As of this
script's authoring, all 21 verified bindings have every key mapped.

Usage:
    python scripts/build_policy_fabric.py INSTANCE.yaml [--out-dir DIR]
                                           [--bindings linkml/policy_fabric_bindings.yaml]

author: orion.banks
"""

import argparse
import json
import sys
from pathlib import Path

import yaml


def load_bindings(path: str) -> dict:
    data = yaml.safe_load(open(path))
    return {b["dataUseModifier"]: b for b in data["bindings"]}


def build(instance: dict, bindings: dict) -> tuple[dict, list, dict]:
    policy_data = {}
    credentials = []
    seen_credentials = set()

    for duo_code in instance.get("dataUseModifiers", []):
        binding = bindings.get(duo_code)
        if binding is None:
            print(f"warning: no PolicyCardBinding for {duo_code}; skipping", file=sys.stderr)
            continue

        sources_by_key = {
            src["referenceValueKey"]: src
            for src in binding.get("referenceValueSources", [])
        }

        for key in binding.get("referenceValueKeys", []):
            source = sources_by_key.get(key)
            if source is None:
                print(
                    f"warning: {duo_code} ({binding['policyCardName']}) has no referenceValueSources "
                    f"entry for key '{key}' — left unpopulated (see policy_fabric_bindings.yaml notes "
                    "for the gap)",
                    file=sys.stderr,
                )
                continue

            source_slot = source["sourceSlot"]
            key_is_multivalued = source.get("keyIsMultivalued", True)
            values = instance.get(source_slot)
            if values is None:
                print(
                    f"warning: {duo_code} ({binding['policyCardName']}) sourceSlot "
                    f"'{source_slot}' is empty on this instance",
                    file=sys.stderr,
                )
                continue
            if not isinstance(values, list):
                values = [values]

            if key_is_multivalued:
                policy_data.setdefault(key, [])
                for v in values:
                    if v not in policy_data[key]:
                        policy_data[key].append(v)
            else:
                # This Policy Fabric key is a scalar (e.g. datasetID, requiredDocumentID,
                # notAfter) even where its governanceDUO sourceSlot is multivalued (e.g.
                # assetDids) — take the first value, per ReferenceValueSource.keyIsMultivalued.
                policy_data[key] = values[0]

        for cred in binding.get("requiredCredentials", []):
            dedup_key = (cred["credentialType"], tuple(cred["requiredClaims"]))
            if dedup_key not in seen_credentials:
                seen_credentials.add(dedup_key)
                credentials.append(cred)

    asset_registration = {
        "name": instance.get("id", ""),
        "did": (instance.get("assetDids") or [None])[0],
        "metadata": {
            "data_source": instance.get("guardianDataSource"),
            "guardian_url": instance.get("guardianUrl"),
        },
    }

    return policy_data, credentials, asset_registration


def main():
    parser = argparse.ArgumentParser(
        description="Export a governanceDUO AccessRequirement instance to Policy Fabric's input artifacts."
    )
    parser.add_argument("instance", help="Path to an AccessRequirement instance YAML.")
    parser.add_argument("--bindings", default="linkml/policy_fabric_bindings.yaml")
    parser.add_argument("--out-dir", default="policy_fabric_export")
    args = parser.parse_args()

    instance = yaml.safe_load(open(args.instance))
    bindings = load_bindings(args.bindings)
    policy_data, credentials, asset_registration = build(instance, bindings)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "policy_data.json").write_text(json.dumps(policy_data, indent=2) + "\n")
    (out_dir / "associated_credentials.json").write_text(json.dumps(credentials, indent=2) + "\n")
    (out_dir / "asset_registration.json").write_text(json.dumps(asset_registration, indent=2) + "\n")

    print(f"Wrote policy_data.json, associated_credentials.json, asset_registration.json to {out_dir}/")


if __name__ == "__main__":
    main()
