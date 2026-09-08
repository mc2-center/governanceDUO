---
search:
  boost: 5.0
---

# Slot: inputDataTiers 


_The combination of input DataTierEnum values this rule governs._



<div data-search-exclude markdown="1">



URI: [governanceduo:inputDataTiers](https://w3id.org/sage-bionetworks/governance-duo/inputDataTiers)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DerivationRule](../classes/DerivationRule.md) | A policy row keyed by a combination of DataTierEnum values, answering "may th... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [DataTierEnum](../enums/DataTierEnum.md) |
| Domain Of | [DerivationRule](../classes/DerivationRule.md) |
| Slot URI | [governanceduo:inputDataTiers](https://w3id.org/sage-bionetworks/governance-duo/inputDataTiers) |

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
| self | governanceduo:inputDataTiers |
| native | governanceduo:inputDataTiers |




## LinkML Source

<details>
```yaml
name: inputDataTiers
description: The combination of input DataTierEnum values this rule governs.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: governanceduo:inputDataTiers
domain_of:
- DerivationRule
range: DataTierEnum
required: true
multivalued: true

```
</details></div>