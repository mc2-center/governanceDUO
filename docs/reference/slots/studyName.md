---
search:
  boost: 5.0
---

# Slot: studyName 


_Name of the study._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/studyName](https://w3id.org/sage-bionetworks/governance-duo/slot/studyName)
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
| cde_id | 11459810 |




### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:studyName |
| native | governanceduo:studyName |




## LinkML Source

<details>
```yaml
name: studyName
annotations:
  cde_id:
    tag: cde_id
    value: '11459810'
description: Name of the study.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- Study
range: string
required: true

```
</details></div>