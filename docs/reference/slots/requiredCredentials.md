---
search:
  boost: 5.0
---

# Slot: requiredCredentials 

<div data-search-exclude markdown="1">



URI: [governanceduo:slot/requiredCredentials](https://w3id.org/sage-bionetworks/governance-duo/slot/requiredCredentials)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PolicyCardBinding](../classes/PolicyCardBinding.md) | One row per verified tmp-policies policy_cards/<name>/ folder: which DUO code... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [CredentialRequirement](../classes/CredentialRequirement.md) |
| Domain Of | [PolicyCardBinding](../classes/PolicyCardBinding.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:requiredCredentials |
| native | governanceduo:requiredCredentials |




## LinkML Source

<details>
```yaml
name: requiredCredentials
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- PolicyCardBinding
range: CredentialRequirement
multivalued: true
inlined: true

```
</details></div>