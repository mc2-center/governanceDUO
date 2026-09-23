# Report: second_review_fixes.md

Nine of the 10 findings of the second pre-PR review (`067e780..d46224e`) are
fixed. Each fix that changes behavior has a check that fails when the bug comes
back. The tenth, #4, was implemented and then reverted (see below); it moves
into a broader refactor plan. This round also covered the plan's open items;
see the end of the report.

## Changes

| # | commit | change | proof the check bites |
|---|---|---|---|
| 1 | `29e3eaa` | `requirements.txt` pins `linkml==1.11.1`, `linkml-runtime==1.11.1`, `rdflib==7.6.0` and `pyshacl==0.40.1`, the versions the owlgen overrides and byte-exact drift check were tested with. A comment says an upgrade must be deliberate. | — |
| 2 | `1a744a3` | The sync skips, with a warning, an AccessGrant whose permissions are all unrecognized. | `check_sync_governance.py` adds user 3000006 with only `NEW_PERM_ONLY`. On the old sync the grant is minted and the SHACL fails. |
| 3 | `19f3d3a` | Repair 1 adds `rdfs:range` for a class or enum range (`sagegov:dataTier` → DataTierEnum, `sagegov:createdBy` → Principal). `check_derivation_policy.py` runs the domain/range check on the builder's output. | A planted `sagegov:dataTier "Confidential"` is reported. |
| 4 | `8bbb29c`, reverted in `b4b01ec` | **Reverted.** As implemented: GrantPermission, AccessType, ApprovalState, BindingType and SubmissionState are `implements: [owl:NamedIndividual]`. Each value is an `owl:NamedIndividual` and the enum `owl:oneOf` them, so a range over one entails "one of these values". This is plain LinkML, with no new workaround. PrincipalTypeEnum and the DUO codes stay classes. The domain/range check reads membership from `owl:oneOf`. | **Why reverted:** declaring the values `owl:NamedIndividual` makes pySHACL 0.40.1 (the latest) deep-clone each one through its enum's `owl:oneOf` when `governance_duo.owl.ttl` is the ont_graph. `shacl-validate` went from about 2 s to over 40 minutes (`inoculate()` → `clone_node(deep_clone=True)`). Two ways around it were considered: merging the OWL into the data graph (same violations, 0.2 s), or reverting. Instead, the graph vocabularies are to be remodeled as SKOS concept schemes, sagebrain-model's convention, together with a graph/record TBox split. |
| 5 | `3a120b4` | `make artifact-drift-check` clears the generated directories, regenerates everything (now including `docs/reference` and `policy_fabric_export`), then compares byte-for-byte or as graphs. It also fails on a committed file no generator produces. | It found two stale pages, `docs/reference/slots/sourceAclId.md` and `sourceAclResourceAccessId.md`, for slots removed in `146167e`. Deleted. 259 artifacts checked. |
| 6 | `42670c8` | Review notes list every flagging rule, forbidding ones first, with disjointness after them. | The new `gov:activity-7005` (Private+Private forbidden, Controlled+Controlled review) fails on the old builder. |
| 7 | `de6e26a` | `validate_examples.py` also validates the fixture records the builders read, and fails if a glob finds none. The five fixture ARs gain `contributorName`/`contributionDate`, and the sync fixture's DUO:0000042 AR gains its rule-required `requiredAgreementDocumentId`. | 29 records are validated (was 21). Removing that id from the sync fixture fails on the DUO rule. |
| 8 | `42670c8` | Derivation assertions 9 → 12. The 7002/7003 reviews must be attributed to the rule, not to disjointness. `gov:activity-7004` has a Controlled+Private rule lower an unbound output from Private to Controlled. 7005's notes must lead with the forbidding rule. | A mutant floor, `max(rule, default_rank)`, fails the lowering assertion. |
| 9, 10 | `848d6b0` | `domain-range-check`, `sync-governance-check` and `derivation-policy-check` depend on `owl`. The sync-provenance comment is back above its own target. | — |

## Open items from earlier plans

- **Offline governance-sync test:** done in `d46224e` (`check_sync_governance.py`,
  in `validate-all`). Writing it found two sync bugs:
  - a Submission in an unrecognized state was written without its required
    `gov:state` (now skipped whole);
  - `sourceApprovalId` was written as a string (now an integer).

  This round's #2 extends it.
- **`Pending Annotation`:** unchanged. Giving it a `meaning:` would make the
  builder mint a Condition for it, reversing the earlier decision to skip
  Conditions for it. No example uses it.
- **Shared `gov:APPROVED`:** the approved trade-off, unchanged by the #4 revert;
  the SKOS refactor plan revisits it.
- **sagebrain-model re-import:** needs this branch pushed and then a bump of
  `GOVERNANCEDUO_COMMIT` in sagebrain-model. Not done here: both are
  outward-facing and need a go-ahead.

## Incident during the revert

The first `git revert` aborted on a dirty working tree (an uncommitted SHACL
rebuild left by the interrupted `validate-all`). A chained
`git commit --amend` then relabeled the previous commit (the Makefile fix)
with the revert message; that commit's tree was unchanged. Its original
message was restored (now `848d6b0`), the tree cleaned, and the revert redone
as `b4b01ec`.

## Verification (on `b4b01ec`)

- `make validate-all`: exit 0. That covers every SHACL validation, the sync
  (provenance and governance), derivation-policy (12 assertions), infra-contract,
  domain/range, approval-expiry, example-validation (29 records) and enum-sync
  checks, plus `owl-profile` (with the PROV-O check) and `owl-profile-abox`.
- `make artifact-drift-check`: all 259 generated artifacts match HEAD.
- `make sagebrain-contract-check`: all four parts pass.
