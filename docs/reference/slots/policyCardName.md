---
search:
  boost: 5.0
---

# Slot: policyCardName 


_The literal tmp-policies policy_cards/<name>/ folder name, e.g. "geographical-restriction"._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/policyCardName](https://w3id.org/sage-bionetworks/governance-duo/slot/policyCardName)
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
| Required | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:policyCardName |
| native | governanceduo:policyCardName |




## LinkML Source

<details>
```yaml
name: policyCardName
description: The literal tmp-policies policy_cards/<name>/ folder name, e.g. "geographical-restriction".
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- PolicyCardBinding
range: string
required: true

```
</details></div>