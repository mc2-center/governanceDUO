---
search:
  boost: 5.0
---

# Slot: studyDescription 


_Description of the study, including the types of experimental assays, model systems, types of analysis, description of cohort, associated vulnerable populations, special categories of data, rare diseases, etc. Maps to DUOPlus2._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/studyDescription](https://w3id.org/sage-bionetworks/governance-duo/slot/studyDescription)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Study](../classes/Study.md) | Studies associated with a grant |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [Study](../classes/Study.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |










## Identifier and Mapping Information



### Annotations

| property | value |
| --- | --- |
| cde_id | 03444002 |




### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:studyDescription |
| native | governanceduo:studyDescription |




## LinkML Source

<details>
```yaml
name: studyDescription
annotations:
  cde_id:
    tag: cde_id
    value: '03444002'
description: Description of the study, including the types of experimental assays,
  model systems, types of analysis, description of cohort, associated vulnerable populations,
  special categories of data, rare diseases, etc. Maps to DUOPlus2.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- Study
range: string
required: true

```
</details></div>