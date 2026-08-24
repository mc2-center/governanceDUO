---
search:
  boost: 5.0
---

# Slot: credentialType 

<div data-search-exclude markdown="1">



URI: [governanceduo:slot/credentialType](https://w3id.org/sage-bionetworks/governance-duo/slot/credentialType)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [CredentialRequirement](../classes/CredentialRequirement.md) | One credential type a Policy Fabric policy_card requires the requester to pre... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [CredentialTypeEnum](../enums/CredentialTypeEnum.md) |
| Domain Of | [CredentialRequirement](../classes/CredentialRequirement.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:credentialType |
| native | governanceduo:credentialType |




## LinkML Source

<details>
```yaml
name: credentialType
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- CredentialRequirement
range: CredentialTypeEnum
required: true

```
</details></div>