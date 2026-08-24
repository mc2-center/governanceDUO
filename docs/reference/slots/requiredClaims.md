---
search:
  boost: 5.0
---

# Slot: requiredClaims 


_Dot-path claim name(s) this policy_card's Rego logic actually reads, e.g. "locatedAt.country"._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/requiredClaims](https://w3id.org/sage-bionetworks/governance-duo/slot/requiredClaims)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [CredentialRequirement](../classes/CredentialRequirement.md) | One credential type a Policy Fabric policy_card requires the requester to pre... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [CredentialRequirement](../classes/CredentialRequirement.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
| Multivalued | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:requiredClaims |
| native | governanceduo:requiredClaims |




## LinkML Source

<details>
```yaml
name: requiredClaims
description: Dot-path claim name(s) this policy_card's Rego logic actually reads,
  e.g. "locatedAt.country".
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- CredentialRequirement
range: string
required: true
multivalued: true

```
</details></div>