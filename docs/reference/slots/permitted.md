---
search:
  boost: 5.0
---

# Slot: permitted 


_Whether this combination of inputDataTiers may be joined/derived from together at all._



<div data-search-exclude markdown="1">



URI: [governanceduo:permitted](https://w3id.org/sage-bionetworks/governance-duo/permitted)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DerivationRule](../classes/DerivationRule.md) | A policy row keyed by a combination of DataTierEnum values, answering "may th... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Boolean](../types/Boolean.md) |
| Domain Of | [DerivationRule](../classes/DerivationRule.md) |
| Slot URI | [governanceduo:permitted](https://w3id.org/sage-bionetworks/governance-duo/permitted) |

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
| self | governanceduo:permitted |
| native | governanceduo:permitted |




## LinkML Source

<details>
```yaml
name: permitted
description: Whether this combination of inputDataTiers may be joined/derived from
  together at all.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: governanceduo:permitted
domain_of:
- DerivationRule
range: boolean
required: true

```
</details></div>