---
search:
  boost: 5.0
---

# Slot: referenceValueKeys 


_The policy_data_schema.json key(s) this policy_card's Reference Values Schema defines, e.g. "allowedCountries". Empty for policy_cards with no reference values at all (pure credential-chain checks, e.g. ethics-approval-required)._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/referenceValueKeys](https://w3id.org/sage-bionetworks/governance-duo/slot/referenceValueKeys)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PolicyCardBinding](../classes/PolicyCardBinding.md) | One row per verified tmp-policies policy_cards/<name>/ folder: which DUO code... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
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
| self | governanceduo:referenceValueKeys |
| native | governanceduo:referenceValueKeys |




## LinkML Source

<details>
```yaml
name: referenceValueKeys
description: The policy_data_schema.json key(s) this policy_card's Reference Values
  Schema defines, e.g. "allowedCountries". Empty for policy_cards with no reference
  values at all (pure credential-chain checks, e.g. ethics-approval-required).
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- PolicyCardBinding
range: string
multivalued: true

```
</details></div>