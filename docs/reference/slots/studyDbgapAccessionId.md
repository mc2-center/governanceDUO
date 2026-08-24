---
search:
  boost: 5.0
---

# Slot: studyDbgapAccessionId 


_A stable unique alphanumeric identifier assigned to a study and any objects by the database of Genotypes and Phenotypes (dbGaP). Required for controlled access data being submitted to CDS/CRDC._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/studyDbgapAccessionId](https://w3id.org/sage-bionetworks/governance-duo/slot/studyDbgapAccessionId)
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








## Comments

* NCIT:C173940 "dbGaP Accession Number" — its OLS definition text is word-for- word this slot's description (the CSV description likely originates from this NCIT term already).



## Identifier and Mapping Information



### Annotations

| property | value |
| --- | --- |
| cde_id | 11524544 |




### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:studyDbgapAccessionId |
| native | governanceduo:studyDbgapAccessionId |
| exact | NCIT:C173940 |




## LinkML Source

<details>
```yaml
name: studyDbgapAccessionId
annotations:
  cde_id:
    tag: cde_id
    value: '11524544'
description: A stable unique alphanumeric identifier assigned to a study and any objects
  by the database of Genotypes and Phenotypes (dbGaP). Required for controlled access
  data being submitted to CDS/CRDC.
comments:
- NCIT:C173940 "dbGaP Accession Number" — its OLS definition text is word-for- word
  this slot's description (the CSV description likely originates from this NCIT term
  already).
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
exact_mappings:
- NCIT:C173940
rank: 1000
domain_of:
- Study
range: string

```
</details></div>