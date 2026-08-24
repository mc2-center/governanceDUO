---
search:
  boost: 5.0
---

# Slot: studyParticipantNumber 


_The number of participant instances associated with systematic investigation into a subject._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/studyParticipantNumber](https://w3id.org/sage-bionetworks/governance-duo/slot/studyParticipantNumber)
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
| cde_id | 11555662 |




### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:studyParticipantNumber |
| native | governanceduo:studyParticipantNumber |




## LinkML Source

<details>
```yaml
name: studyParticipantNumber
annotations:
  cde_id:
    tag: cde_id
    value: '11555662'
description: The number of participant instances associated with systematic investigation
  into a subject.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- Study
range: float
required: true

```
</details></div>