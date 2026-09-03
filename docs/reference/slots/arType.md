---
search:
  boost: 5.0
---

# Slot: arType 


_Free-text access requirement type, e.g. "IRB"._



<div data-search-exclude markdown="1">



URI: [sagegov:arType](https://sagebionetworks.org/governance/arType)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [IRBRequirement](../classes/IRBRequirement.md) | A site/program-specific instantiation of an AccessRequirementTemplate, per th... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [IRBRequirement](../classes/IRBRequirement.md) |
| Slot URI | [sagegov:arType](https://sagebionetworks.org/governance/arType) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:arType |
| native | governanceduo:arType |




## LinkML Source

<details>
```yaml
name: arType
description: Free-text access requirement type, e.g. "IRB".
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:arType
domain_of:
- IRBRequirement
range: string

```
</details></div>