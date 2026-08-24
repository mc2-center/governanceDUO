---
search:
  boost: 5.0
---

# Slot: studyIndexDate 


_The reference event associated with timepoints in this study. One of Diagnosis Date, Enrollment Date, Collection Date, or Birth Date._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/studyIndexDate](https://w3id.org/sage-bionetworks/governance-duo/slot/studyIndexDate)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Study](../classes/Study.md) | Studies associated with a grant |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [StudyIndexDateEnum](../enums/StudyIndexDateEnum.md) |
| Domain Of | [Study](../classes/Study.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:studyIndexDate |
| native | governanceduo:studyIndexDate |




## LinkML Source

<details>
```yaml
name: studyIndexDate
description: The reference event associated with timepoints in this study. One of
  Diagnosis Date, Enrollment Date, Collection Date, or Birth Date.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- Study
range: StudyIndexDateEnum
multivalued: true

```
</details></div>