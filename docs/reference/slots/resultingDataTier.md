---
search:
  boost: 5.0
---

# Slot: resultingDataTier 


_The DataTierEnum the derived output carries when permitted. Defaults to max(inputDataTiers) per the note's own recommendation, but a rule may explicitly override it for a specific combination (e.g. an aggregation that demonstrably reduces sensitivity below its inputs' max)._



<div data-search-exclude markdown="1">



URI: [governanceduo:resultingDataTier](https://w3id.org/sage-bionetworks/governance-duo/resultingDataTier)
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
| Slot URI | [governanceduo:resultingDataTier](https://w3id.org/sage-bionetworks/governance-duo/resultingDataTier) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:resultingDataTier |
| native | governanceduo:resultingDataTier |




## LinkML Source

<details>
```yaml
name: resultingDataTier
description: The DataTierEnum the derived output carries when permitted. Defaults
  to max(inputDataTiers) per the note's own recommendation, but a rule may explicitly
  override it for a specific combination (e.g. an aggregation that demonstrably reduces
  sensitivity below its inputs' max).
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: governanceduo:resultingDataTier
domain_of:
- DerivationRule
range: DataTierEnum

```
</details></div>