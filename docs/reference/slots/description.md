---
search:
  boost: 5.0
---

# Slot: description 


_Human-readable description of this condition, taken directly from DataUseModifierEnum.permissible_values[code]'s own description: text, not re-authored here._



<div data-search-exclude markdown="1">



URI: [sagegov:description](https://sagebionetworks.org/governance/description)
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
| Slot URI | [sagegov:description](https://sagebionetworks.org/governance/description) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:description |
| native | governanceduo:description |
| exact | dcterms:description |




## LinkML Source

<details>
```yaml
name: description
description: 'Human-readable description of this condition, taken directly from DataUseModifierEnum.permissible_values[code]''s
  own description: text, not re-authored here.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
exact_mappings:
- dcterms:description
rank: 1000
slot_uri: sagegov:description
domain_of:
- Condition
range: string

```
</details></div>