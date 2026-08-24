---
search:
  boost: 5.0
---

# Slot: studyInvestigator 


_Investigator(s) associated with the project. Multiple names should be provided as a comma-separated list._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/studyInvestigator](https://w3id.org/sage-bionetworks/governance-duo/slot/studyInvestigator)
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








## Comments

* NCIT:C19924 "Principal Investigator" — a role concept, not a name; this slot holds literal investigator name(s), so the mapping is close, not exact.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:studyInvestigator |
| native | governanceduo:studyInvestigator |
| close | NCIT:C19924 |




## LinkML Source

<details>
```yaml
name: studyInvestigator
description: Investigator(s) associated with the project. Multiple names should be
  provided as a comma-separated list.
comments:
- NCIT:C19924 "Principal Investigator" — a role concept, not a name; this slot holds
  literal investigator name(s), so the mapping is close, not exact.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
close_mappings:
- NCIT:C19924
rank: 1000
domain_of:
- Study
range: string
required: true

```
</details></div>