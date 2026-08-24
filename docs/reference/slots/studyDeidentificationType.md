---
search:
  boost: 5.0
---

# Slot: studyDeidentificationType 


_General description of the de-identification method. Maps to DUOPlus3._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/studyDeidentificationType](https://w3id.org/sage-bionetworks/governance-duo/slot/studyDeidentificationType)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Study](../classes/Study.md) | Studies associated with a grant |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [DeidentificationTypeEnum](../enums/DeidentificationTypeEnum.md) |
| Domain Of | [Study](../classes/Study.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |








## Comments

* T4FS:0000414 "de-identification" — see GovernanceMixin.deidentificationType for the same close (not exact) mapping and rationale.



## Identifier and Mapping Information



### Annotations

| property | value |
| --- | --- |
| cde_id | 14576319 |




### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:studyDeidentificationType |
| native | governanceduo:studyDeidentificationType |
| close | T4FS:0000414 |




## LinkML Source

<details>
```yaml
name: studyDeidentificationType
annotations:
  cde_id:
    tag: cde_id
    value: '14576319'
description: General description of the de-identification method. Maps to DUOPlus3.
comments:
- T4FS:0000414 "de-identification" — see GovernanceMixin.deidentificationType for
  the same close (not exact) mapping and rationale.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
close_mappings:
- T4FS:0000414
rank: 1000
domain_of:
- Study
range: DeidentificationTypeEnum
multivalued: true

```
</details></div>