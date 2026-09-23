# Fix the second pre-PR review's findings

## Context

The pre-PR review of `067e780..d46224e` (2026-09-23; same expert framing as
the first, see `plans/pre_pr_review_fixes.md`) reported 10 findings. Each was
re-read against the code before this plan.

| # | finding | fix |
|---|---|---|
| 1 | `requirements.txt` pins only `linkml>=1.8`, but CI now byte-compares the OWL and `GovernanceOwlGenerator` overrides owlgen internals checked only on 1.11.1 | Pin the tested versions exactly (linkml, linkml-runtime, rdflib, pyshacl). |
| 2 | The sync writes an AccessGrant whose permissions were all unrecognized, so it has no `gov:permission` (AccessGrantShape `minCount 1`) | Skip that grant, with a warning. Add the case to `check_sync_governance.py`. |
| 3 | Repair 1 types `sagegov:dataTier` (ControlLabel) as a data property with no `rdfs:range`, so no check covers ControlLabel tiers; nor is the derivation builder's output checked | Repair 1 adds `rdfs:range` = the induced range. `check_derivation_policy.py` runs the domain/range check on its output. |
| 4 | Graph-enum values are OWL classes in a union, but the data uses them as individuals | **Decision (approved):** mark GrantPermission, AccessType, ApprovalState, BindingType and SubmissionState `implements: [owl:NamedIndividual]`, so each value is an `owl:NamedIndividual` and the enum `owl:oneOf` them (plain LinkML, no workaround). PrincipalTypeEnum stays a class union (`gov:User`/`gov:Team` are classes), as do the DUO codes. |
| 5 | The drift check misses `docs/reference/**` and `policy_fabric_export/*.json`, which `validate-all` doesn't regenerate, and misses stale outputs the converters no longer produce | `artifact-drift-check` regenerates both (`docs`, `policy-fabric`) and compares them. It also flags committed example-RDF files that no example produces. |
| 6 | Only the first flagging rule is reported, so a `permitted: false` rule can hide behind a `requiresReview` one | Report every flagging rule, forbidding ones first. |
| 7 | `validate_examples.py` only covers `*.example.yaml`, so the fixture records fed to the builders are never validated (and they don't conform) | Validate the fixture ARs and rules too, and make them conform. |
| 8 | The new derivation assertions only ASK that a review exists, and nothing exercises a rule *lowering* an inherited tier | Assert the review notes name the rule (not disjointness). Add a lowering case and a forbidden-plus-review case. |
| 9 | `domain-range-check` (and `sync-governance-check`) don't depend on `owl` | Add the prerequisite. |
| 10 | The sync-provenance comment in the Makefile now sits above the wrong target | Fix the comments. |

## Verification

- `make validate-all` passes, then `make artifact-drift-check`.
- Each new or strengthened check fails when its bug is reintroduced.
- The owl-profile checks, including `owl-profile-abox`, stay in profile after #4.
- `make sagebrain-contract-check` passes.

Report: `plans/second_review_fixes_report.md`.
