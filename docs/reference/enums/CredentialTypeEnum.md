---
search:
  boost: 2.0
---


# Enum: CredentialTypeEnum 




_The 14 Verifiable Credential types defined in tmp-policies/credentials/*.schema.json._



<div data-search-exclude markdown="1">

URI: [governanceduo:enum/CredentialTypeEnum](https://w3id.org/sage-bionetworks/governance-duo/enum/CredentialTypeEnum)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| AffiliationCredential | None | Claims: isMemberOf (DID of organization, required), typeOfMembership (string,... |
| LocationCredential | None | Claims: locatedAt (object: street, zipCode, state, country — all string, requ... |
| publicKeyCredential | None | Claims: key (string, PEM-encoded, required) |
| AgreementCredential | None | Claims: agreementInfo (object: documentID, documentVersion — both string, req... |
| ComputeEnvironmentCredential | None | Claims: hasComputeProfile (object: profile — object, required; claim shape is... |
| EmailCredential | None | Claims: emailAddress (string, email format, required) |
| EthicsCommitteeAccreditationCredential | None | Claims: ResponsibleFor (DID of institution, required) |
| IRBApprovalCredential | None | Claims: isApprovedByEthicsCommittee (DID of Ethics Committee, required) |
| IntendedDataUseCredential | None | Claims: useOnlyFor (object: purposes [array of string], diseases [array of MO... |
| LegalDesignationCredential | None | Claims: hasLegalForm (string, ISO 20275:2017 ELF code, required) |
| ProjectOwnershipCredential | None | Claims: Owns (DID of project, required) |
| ScopedAgreementCredential | None | Claims: agreementInfo (object: counterParty [DID string], scope [object: obli... |
| TeamCredential | None | Claims: MemberOfTeamOf (DID of PI, required) |
| UserPlatformCredential | None | Claims: userId, accountType, profileStatus (string) + isUser (boolean) — all ... |
| WalletVerifyingKeyCredential | None | Claims: verifying_key (string, PEM-encoded, required) |




## Slots

| Name | Description |
| ---  | --- |
| [credentialType](../slots/credentialType.md) |  |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo






## LinkML Source

<details>
```yaml
name: CredentialTypeEnum
description: The 14 Verifiable Credential types defined in tmp-policies/credentials/*.schema.json.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
permissible_values:
  AffiliationCredential:
    text: AffiliationCredential
    description: 'Claims: isMemberOf (DID of organization, required), typeOfMembership
      (string, required).'
  LocationCredential:
    text: LocationCredential
    description: 'Claims: locatedAt (object: street, zipCode, state, country — all
      string, required).'
  publicKeyCredential:
    text: publicKeyCredential
    description: 'Claims: key (string, PEM-encoded, required). The requester''s channel
      public key.'
  AgreementCredential:
    text: AgreementCredential
    description: 'Claims: agreementInfo (object: documentID, documentVersion — both
      string, required).'
  ComputeEnvironmentCredential:
    text: ComputeEnvironmentCredential
    description: 'Claims: hasComputeProfile (object: profile — object, required; claim
      shape is asset-specific).'
  EmailCredential:
    text: EmailCredential
    description: 'Claims: emailAddress (string, email format, required).'
  EthicsCommitteeAccreditationCredential:
    text: EthicsCommitteeAccreditationCredential
    description: 'Claims: ResponsibleFor (DID of institution, required).'
  IRBApprovalCredential:
    text: IRBApprovalCredential
    description: 'Claims: isApprovedByEthicsCommittee (DID of Ethics Committee, required).'
  IntendedDataUseCredential:
    text: IntendedDataUseCredential
    description: 'Claims: useOnlyFor (object: purposes [array of string], diseases
      [array of MONDO codes] — both required).'
  LegalDesignationCredential:
    text: LegalDesignationCredential
    description: 'Claims: hasLegalForm (string, ISO 20275:2017 ELF code, required).'
  ProjectOwnershipCredential:
    text: ProjectOwnershipCredential
    description: 'Claims: Owns (DID of project, required).'
  ScopedAgreementCredential:
    text: ScopedAgreementCredential
    description: 'Claims: agreementInfo (object: counterParty [DID string], scope
      [object: obligation, project, dataset — all string, required] — both required).'
  TeamCredential:
    text: TeamCredential
    description: 'Claims: MemberOfTeamOf (DID of PI, required).'
  UserPlatformCredential:
    text: UserPlatformCredential
    description: 'Claims: userId, accountType, profileStatus (string) + isUser (boolean)
      — all required.'
  WalletVerifyingKeyCredential:
    text: WalletVerifyingKeyCredential
    description: 'Claims: verifying_key (string, PEM-encoded, required).'

```
</details>

</div>