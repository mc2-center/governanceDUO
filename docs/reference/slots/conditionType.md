---
search:
  boost: 5.0
---

# Slot: conditionType 


_A short label for this condition. For the 24 real DUO codes in DataUseModifierEnum, this is that code's own duo_shorthand annotation (e.g. "GRU", "COL"); the 7 Sage-local DUOPlus1-7 extensions have no duo_shorthand/meaning: CURIE at all, so their bare enum key (e.g. "DUOPlus1") is used instead -- see scripts/build_governance_graph.py._



<div data-search-exclude markdown="1">



URI: [sagegov:conditionType](https://sagebionetworks.org/governance/conditionType)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Condition](../classes/Condition.md) | A single DUO-code-backed condition on an AccessRequirement, surfacing Governa... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [Condition](../classes/Condition.md) |
| Slot URI | [sagegov:conditionType](https://sagebionetworks.org/governance/conditionType) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:conditionType |
| native | governanceduo:conditionType |




## LinkML Source

<details>
```yaml
name: conditionType
description: 'A short label for this condition. For the 24 real DUO codes in DataUseModifierEnum,
  this is that code''s own duo_shorthand annotation (e.g. "GRU", "COL"); the 7 Sage-local
  DUOPlus1-7 extensions have no duo_shorthand/meaning: CURIE at all, so their bare
  enum key (e.g. "DUOPlus1") is used instead -- see scripts/build_governance_graph.py.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:conditionType
domain_of:
- Condition
range: string

```
</details></div>