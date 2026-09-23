# Report: enum_values_match_owl.md

Every enum-valued slot in the OWL now agrees with the data. The two TBoxes
merged with the exported and example graphs are OWL 2 DL: 0 violations, down
from 29. The exported governance graph is byte-identical.

## Changes

| step | commit | change |
|---|---|---|
| 1 | `50c6c7a` | Schema: `meaning: sagegov:<value>` on every value of AccessType (18), ApprovalState, BindingType, SubmissionState and PrincipalType; `implements: [rdfs:Literal]` on the ten literal enums. The descriptions record the IRIs and the shared-`gov:APPROVED` trade-off. `linkml-lint` output is identical to the baseline. |
| 2 | `f8365f1` | `build_owl.py`: `IriRangeOwlGenerator` → `GovernanceOwlGenerator`. For a literal enum it drops `owl:Class`, moves `owl:oneOf` into an `owl:equivalentClass` datatype definition, and types its slots `owl:DatatypeProperty` (`slot_owl_type`, `slot_node_owltypes`). `repair_generator_output()` repair 1 types a slot_usage override ranging over a literal enum (`ControlLabel.dataTier` → `sagegov:dataTier`) as a data property; it had been an object property carrying strings. |
| 3 | `be2a2dd` | `build_governance_graph.py` resolves permission, bindingType, state, status and principalType through `enum_iri()` (the value's `meaning:`); the export is byte-identical. `sync_governance_graph.py` warns and skips a value outside its enum (e.g. a new Synapse ACCESS_TYPE), since `enum_iri()` would otherwise raise. |
| — | `4feae11` | **Added during implementation (approved):** `GrantPermissionEnum`, the range of `AccessGrant.permission`: AccessTypeEnum's 18 values plus the derived `ACCESS`. Also added `check_enum_sync.py` (`make enum-sync-check`) and `make owl-profile-abox`, both in `validate-all`. |
| 4 | `998ec19` | `check_domain_range.py` checks enum ranges by membership: member IRIs for class enums, `owl:oneOf` strings for literal enums. It reports 9 mismatches against the OWL from before this plan. |
| 5 | `a07c6dd`, `759a1eb` | Regenerated the OWL/SHACL/docs; the hand-written TBox and shapes comments describe the new ranges. |

### Why `GrantPermissionEnum`

The builder writes `gov:ACCESS` as a `gov:permission` value; sagebrain-infra's
authorizer checks it. It isn't a Synapse ACCESS_TYPE, and
AccessTypeEnum stays a pure mirror of Synapse (D8 of
`sagebrain_contract_and_owl_dl_fixes.md`). The new enum names what the
hand-written SHACL already allowed: the 18 Synapse values plus `gov:ACCESS`.
The values use the same `meaning:` IRIs, so a reasoner can derive
AccessTypeEnum ⊑ GrantPermissionEnum. `AccessRequirement.accessType` stays on
AccessTypeEnum, so an AR can't claim to gate ACCESS.

LinkML's `inherits:` can't express "AccessTypeEnum plus ACCESS". Tested on a
minimal schema:
- linkml-validate stopped enforcing the enum at all (it accepted `"BOGUS"`);
- gen-owl dropped the inherited values;
- gen-shacl allowed only `ACCESS`.

So the values are listed again, and `enum-sync-check` asserts the two lists
stay identical.

### What changed in the generated artifacts

- **OWL:** 5,072 → 3,874 triples. The ten literal enums (249 region codes, 11
  licenses, ...) are datatypes rather than one class per value. The 15 enums'
  `governanceduo:<Enum>#<value>` IRIs are gone; only `DataUseModifierEnum`'s
  `Pending Annotation` keeps one (out of scope). Slot typing:
  - 15 enum slots, `sagegov:dataTier` among them, are now
    `owl:DatatypeProperty`;
  - the graph-enum slots stay `owl:ObjectProperty`, ranging over unions of
    the `gov:` IRIs.
- **SHACL:** only the graph-enum `sh:in` lists changed, from strings (`"DOWNLOAD"`)
  to IRIs (`sagegov:DOWNLOAD`), plus `ACCESS` and the permission description.
  No other constraint changed (compared with blank nodes abstracted away).
- **Example RDF and export:** unchanged (drift check against HEAD).

## Verification (on `759a1eb`)

- **`make validate-all`:** exit 0. That covers every SHACL validation, the fixture
  checks and the domain/range check (now with enum membership). It also covers
  approval expiry, example validation, `enum-sync-check`, `owl-profile` (DL
  alone and merged, plus the PROV-O check) and the new `owl-profile-abox`.
- **DL with data (`owl-profile-abox`):** both TBoxes plus the exported,
  provenance, derivation-policy and record example graphs:
  - before this plan: 29 violations, all puns from literals on enum object
    properties (`dataTier`, `inputDataTiers`, `reviewStatus`, `sourceGeography`,
    ...);
  - now: 0.
- **`make artifact-drift-check`:** all 12 artifacts match HEAD.
- **Other checks:** `mkdocs build --strict` passes; `make sagebrain-contract-check`
  passes all four parts.

## Open items

1. **The sync's new enum filtering is untested offline.**
   `sync_governance_graph.py` has no offline fixture check, unlike the
   provenance sync, so the warn-and-skip path for unknown enum values (step 3)
   is compiled but never exercised. An offline check with a fake Synapse
   client, like `check_sync_provenance.py`, would cover it and the rest of the
   governance sync.
2. **`Pending Annotation`** (DataUseModifierEnum, no `meaning:`) would still be
   a literal on an object property if an example used it. None does, and the
   builder mints no Condition for it.
3. **Shared `gov:APPROVED`** (ApprovalState and SubmissionState): the approved
   trade-off, recorded in both enums' descriptions.
4. **sagebrain-model** still imports `240a162`. Its governance import covers
   the provenance terms, which this plan didn't change, but the enum and
   datatype changes reach its merged governance build only after a re-import.
