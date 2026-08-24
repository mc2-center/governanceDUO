---
search:
  boost: 5.0
---

# Slot: studySampleNumber 


_The number of specimens associated with systematic investigation into a subject._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/studySampleNumber](https://w3id.org/sage-bionetworks/governance-duo/slot/studySampleNumber)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Study](../classes/Study.md) | Studies associated with a grant |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Float](../types/Float.md) |
| Domain Of | [Study](../classes/Study.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |










## Identifier and Mapping Information



### Annotations

| property | value |
| --- | --- |
| cde_id | 11555663 |




### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:studySampleNumber |
| native | governanceduo:studySampleNumber |




## LinkML Source

<details>
```yaml
name: studySampleNumber
annotations:
  cde_id:
    tag: cde_id
    value: '11555663'
description: The number of specimens associated with systematic investigation into
  a subject.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- Study
range: float
required: true

```
</details></div>