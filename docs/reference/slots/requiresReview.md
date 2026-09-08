---
search:
  boost: 5.0
---

# Slot: requiresReview 


_Whether this combination is only conditionally permitted, pending a human DerivationReview, rather than flatly permitted/denied._



<div data-search-exclude markdown="1">



URI: [governanceduo:requiresReview](https://w3id.org/sage-bionetworks/governance-duo/requiresReview)
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
| Slot URI | [governanceduo:requiresReview](https://w3id.org/sage-bionetworks/governance-duo/requiresReview) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:requiresReview |
| native | governanceduo:requiresReview |




## LinkML Source

<details>
```yaml
name: requiresReview
description: Whether this combination is only conditionally permitted, pending a human
  DerivationReview, rather than flatly permitted/denied.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: governanceduo:requiresReview
domain_of:
- DerivationRule
range: boolean

```
</details></div>