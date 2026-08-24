Align governanceDUO with Policy Fabric (Technical Policy Blueprint)

 Context

 Sage Bionetworks (a co-author on the position paper) and the wider MLCommons/decentralized-AI
 community have proposed Policy Fabric: a governance architecture that separates policy
 processing (a Policy Engine executing versioned "policy objects," coded in Rego/OPA, against a
 requester's W3C Verifiable Credentials) from capability enforcement (an Asset Guardian that
 gates access once it receives a signed "capability package"). The reference implementation lives
 at github.com/hasan7n/tmp-policies, documented at hasan7n.github.io/tmp-policies/, with the
 architecture described in the accompanying paper (2512.11878v3.pdf, "A Technical Policy
 Blueprint for Trustworthy Decentralized AI").

 Critically, Policy Fabric's reference policies (policy_cards/) are authored one per DUO
 code — the exact same Data Use Ontology this repo's GovernanceMixin already encodes
 (DataUseModifierEnum, meaning: DUO:00000xx). This is not a coincidence to design around; it's
 an existing, close alignment to exploit. The goal of this plan is to add the structured fields
 governanceDUO is currently missing — credential-type/claim requirements, trusted-issuer DIDs,
 asset DIDs, Guardian deployment metadata — so that a governanceDUO AccessRequirement record
 carries everything needed to literally construct Policy Fabric's real input artifacts: a
 policy_data.json (its "Reference Values Schema"), an associated-credentials list, and an Asset
 registration record. This is additive to the existing LinkML schema (no changes to the
 schematic CSV/Synapse JSON-schema pipeline, confirmed out of scope — Policy Fabric's Rego/OPA +
 DID/VC stack never reads either of those).

 Grounding: what was verified directly in hasan7n/tmp-policies (not the docs summary)

 - No formal Policy Card JSON Schema exists anywhere in the repo — the 10-section "Policy
 Card" (Identification/Scope & Target/Associated Credentials/Reference Values Schema/Capability
 Granted/Codified Representation/etc.) is a Markdown convention
 (policy_cards/<name>/policy_card.md),
 not a validated schema. The only real machine-readable artifacts per policy are
 policy_data_schema.json (the Reference Values Schema, informally typed) and policy.rego (the
 actual enforcement logic — "source of truth," per each policy's own README).
 - geographical-restriction (DUO:0000022) — fully verified:
   - policy_data_schema.json: {"allowedCountries": ["list of strings"]}
   - Associated Credentials: LocationCredential (claim locatedAt.country, required) +
 publicKeyCredential (claim key, required), both credentials must share the same subject.
   - Rego (package subpolicy) checks c.claims.locatedAt.country in
 input.policy_data.allowedCountries,
 then emits {"decision": ..., "verification_tasks": [...], "operation": {"name": "do_download",
 "parameters": {"channel_key": "<requester public key>"}}}.
 - institution-specific-restriction (DUO:0000028) — identical shape: policy_data_schema.json
 is {"allowedInstitutions": ["list of strings"]}; credentials are AffiliationCredential
 (claim isMemberOf, required — an organization DID, e.g. did:example:best_university) +
 publicKeyCredential (claim key).
 - 14 credential JSON Schemas exist in credentials/, each a real (if shallow) JSON Schema.
 Notably IntendedDataUseCredential.useOnlyFor.diseases is an array of MONDO codes — the
 exact same vocabulary GovernanceMixin.diseaseSpecificResearch (DUO:0000007) already uses.
 EthicsCommitteeAccreditationCredential/IRBApprovalCredential both hold a DID claim, relevant
 to DUO's ethics-approval-style codes.
 - Asset registration is minimal: the Django Asset model is only name, did (unique),
 metadata (free-form JSON). By convention (not schema) metadata accumulates
 data_source (Guardian's data path), guardian_url/guardian_port, policy_contract (the
 deployed rego_token DID), and policy_data (the reference values actually configured).
 - policy_cards/README.md classifies geographical-restriction, institution-specific-restriction,
 user-specific-restriction (DUO:0000026), and not-for-profit-organisation-use-only
 (DUO:0000045) together as the same "Requester-attribute constraint" family — i.e. this
 pattern (reference-values list + one or two required credentials + do_download capability)
 almost certainly generalizes across most/all of the 21 policy_cards/ folders, which map onto
 a subset of the ~24 real DUO codes DataUseModifierEnum already carries meaning: CURIEs for.
 - No CONTRIBUTING doc exists; adding a new reference policy is mechanical (a policy_cards/<name>/
 folder with at least policy.rego exposing requirements + result, picked up idempotently by
 seed_templates).

 Target LinkML additions (all additive; no existing slot renamed or removed)

 1. New file linkml/policy_fabric.yaml — the credential/binding schema

 imports: [linkml:types, mixins]   # for DataUseModifierEnum
 enums:
   CredentialTypeEnum:              # the 14 real credential schemas, verified from
 credentials/*.schema.json
     permissible_values: [AffiliationCredential, LocationCredential, publicKeyCredential,
       AgreementCredential, ComputeEnvironmentCredential, EmailCredential,
       EthicsCommitteeAccreditationCredential, IRBApprovalCredential, IntendedDataUseCredential,
       LegalDesignationCredential, ProjectOwnershipCredential, ScopedAgreementCredential,
       TeamCredential, UserPlatformCredential, WalletVerifyingKeyCredential]
 classes:
   CredentialRequirement:            # one required credential+claim, e.g.
 LocationCredential.locatedAt.country
     slots: [credentialType, requiredClaim]
   PolicyCardBinding:                 # static, per-DUO-code lookup — NOT per-AccessRequirement
 data
     slots: [dataUseModifier, policyCardName, referenceValueKey, sourceSlot, requiredCredentials]
     # dataUseModifier: range DataUseModifierEnum (the DUO CURIE this binding documents)
     # policyCardName: the literal policy_cards/<name>/ folder, e.g. "geographical-restriction"
     # referenceValueKey: the policy_data_schema.json key, e.g. "allowedCountries"
     # sourceSlot: which existing GovernanceMixin/Study slot already holds this data,
     #   e.g. "geographicalRestriction" — this is the load-bearing cross-reference: it says
     #   "governanceDUO already collects this reference value, right here"
     # requiredCredentials: multivalued, inlined CredentialRequirement list

 2. New data file linkml/policy_fabric_bindings.yaml

 One PolicyCardBinding instance per policy_cards/<name>/ folder that exists in the real repo,
 each verified by reading that folder's actual policy.rego + policy_data_schema.json (the same
 method already used for the 2 confirmed above — not inferred from naming similarity). Since
 all 21 policy_cards map to a subset of DUO codes this schema already has meaning: CURIEs for,
 every binding's dataUseModifier should resolve to an existing enum value — if one doesn't
 (a policy_cards folder for a DUO code not yet in DataUseModifierEnum), add that permissible
 value first rather than skip the binding. Two entries are already fully specified by this plan
 (geographical-restriction → geographicalRestriction; institution-specific-restriction →
 institutionSpecificRestriction); the remaining ~19 get the identical read-the-source treatment
 during execution.

 3. linkml/mixins.yaml — extend GovernanceMixin

 - Add institutionDids (multivalued, pattern: '^did:[a-z0-9]+:.+$') alongside the existing
 institutionSpecificRestriction (ROR pattern). Real, documented gap, not silently
 resolved: Policy Fabric's AffiliationCredential.isMemberOf and allowedInstitutions expect
 organization DIDs; this repo's existing field is ROR IDs. No standard ROR→DID resolution
 exists yet, so both fields are kept, with a comments: note explaining why, rather than forcing
 a fabricated ROR-to-DID mapping.

 4. New PolicyFabricMixin in linkml/mixins.yaml, applied to AccessRequirement only

 AccessRequirement is the right attachment point — it already carries entityIdList (the
 concrete Synapse containers governed) and dataUseModifiers (which DUO codes/policy_cards
 apply), making it the natural analog of a Policy-Fabric "Asset + exposed policy" pairing.
 New slots:
 - assetDids (multivalued, DID pattern) — Policy-Fabric Asset-registry DID(s), order-aligned
 with entityIdList.
 - guardianDataSource (string) — mirrors Asset.metadata.data_source.
 - guardianUrl (string) — mirrors Asset.metadata.guardian_url.
 - policyContractDid (string, DID pattern) — mirrors Asset.metadata.policy_contract, the
 deployed rego_token contract DID once "exposed."
 - trustedIssuerDids (multivalued, DID pattern) — varies per AccessRequirement (an AR's
 owner chooses which VC issuers they trust), unlike PolicyCardBinding.requiredCredentials
 which is static per DUO code. This is why it lives on AccessRequirement, not on
 CredentialRequirement.

 All five are optional (a governanceDUO record can exist before/without ever being deployed into
 Policy Fabric).

 5. linkml/governance_duo.linkml.yaml

 Add policy_fabric to the umbrella's imports: list.

 New export script: scripts/build_policy_fabric.py

 Given an AccessRequirement LinkML instance (e.g. one of linkml/examples/*.example.yaml),
 using linkml/policy_fabric_bindings.yaml as the crosswalk, emit the three artifacts Policy
 Fabric actually consumes:
 - policy_data.json — for each DUO code in the instance's dataUseModifiers, look up its
 PolicyCardBinding, read the value(s) off the named sourceSlot, and merge into one flat
 object keyed by referenceValueKey (e.g. {"allowedCountries": [...], "allowedInstitutions":
 [...]})
 — exactly Policy Fabric's own "merged schema when both policies are selected" shape.
 - associated_credentials.json — deduplicated list of {credentialType, requiredClaim} across
 the selected DUO codes' bindings.
 - asset_registration.json — {name, did, metadata: {data_source, guardian_url}}, literally
 shaped like the real Django Asset model.

 This mirrors the existing scripts/build_owl.py pattern in this repo (LinkML instance → external
 system's native format) rather than inventing a new convention.

 Execution task list

 1. Author linkml/policy_fabric.yaml (schema) and the 2 verified PolicyCardBinding entries in
 linkml/policy_fabric_bindings.yaml.
 2. Read the remaining ~19
 policy_cards/<name>/{policy.rego,policy_data_schema.json,policy_card.md}
 files in hasan7n/tmp-policies directly (same method as the 2 already verified — no
 inference from folder names) and add their PolicyCardBinding entries. Flag in the PR/summary
 any DUO code where governanceDUO has no matching existing slot to serve as sourceSlot (e.g.
 a policy_cards folder needing reference values this model doesn't collect at all yet) rather
 than forcing a weak fit.
 3. Add institutionDids, PolicyFabricMixin (assetDids, guardianDataSource, guardianUrl,
 policyContractDid, trustedIssuerDids) to linkml/mixins.yaml; apply the mixin to
 AccessRequirement in linkml/access_requirement.yaml.
 4. Add policy_fabric to the umbrella imports.
 5. Write scripts/build_policy_fabric.py.
 6. Add one new example instance (or extend linkml/examples/access_requirement.example.yaml)
 combining DUO:0000022 + DUO:0000028 with geographicalRestriction: [US] and
 institutionDids: [did:example:best_university], to directly exercise the tutorial's own
 golden example.
 7. Add a make policy-fabric Makefile target.

 Verification

 1. python3 -c "import yaml; yaml.safe_load(...)" on both new YAML files.
 2. make linkml-lint (--ignore-warnings, existing convention) on the updated umbrella —
 confirm no new errors, only the expected standard_naming warnings.
 3. linkml-validate against the extended/new example instance.
 4. Run scripts/build_policy_fabric.py against that instance and diff its policy_data.json
 output against the tutorial's literal {"allowedCountries": ["US"], "allowedInstitutions":
 ["did:example:best_university"]} — this is a concrete, ground-truth check pulled directly
 from the tutorial, not a self-consistency check.
 5. Re-run make shacl-validate to confirm the pre-existing OWL/SHACL pipeline has no regressions.
     4. Run scripts/build_policy_fabric.py against that instance and diff its policy_data.json
     output against the tutorial's literal {"allowedCountries": ["US"], "allowedInstitutions": 
     ["did:example:best_university"]} — this is a concrete, ground-truth check pulled directly
     from the tutorial, not a self-consistency check.
     5. Re-run make shacl-validate to confirm the pre-existing OWL/SHACL pipeline has no
     regressions.
     6. Update the README's "LinkML representation" section with a short "Policy Fabric alignment"
     paragraph analogous to the existing sagebrain/OLS ones — what's mapped, what's a documented
     gap (ROR-vs-DID), and that no changes were made to hasan7n/tmp-policies itself.