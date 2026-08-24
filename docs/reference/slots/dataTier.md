---
search:
  boost: 5.0
---

# Slot: dataTier 


_The tier of data access associated with the access requirement. Equivalent to DUOPlus5._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/dataTier](https://w3id.org/sage-bionetworks/governance-duo/slot/dataTier)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [GovernanceMixin](../classes/GovernanceMixin.md) | DUO-based data-use-modifier vocabulary and its conditional-requirement rules,... |  no  |
| [AccessRequirement](../classes/AccessRequirement.md) | Representation of a Synapse Access Requirement and its relationships to entit... |  no  |
| [Resource](../classes/Resource.md) | Information that is relevant to resource access conditions |  no  |
| [Study](../classes/Study.md) | Studies associated with a grant |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [DataTierEnum](../enums/DataTierEnum.md) |
| Domain Of | [GovernanceMixin](../classes/GovernanceMixin.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |








## Comments

* Required when dataUseModifiers contains DUOPlus5 — see GovernanceMixin rules.
* NCIT:C175887 "Open or Controlled Data Access Indicator" (synonym: "Data Access Level") is defined as "Specifies whether the data in a repository is open access or controlled access" — a direct match for this slot's Anonymous/Open/Controlled/Private tiers.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:dataTier |
| native | governanceduo:dataTier |
| exact | NCIT:C175887 |




## LinkML Source

<details>
```yaml
name: dataTier
description: The tier of data access associated with the access requirement. Equivalent
  to DUOPlus5.
comments:
- Required when dataUseModifiers contains DUOPlus5 — see GovernanceMixin rules.
- 'NCIT:C175887 "Open or Controlled Data Access Indicator" (synonym: "Data Access
  Level") is defined as "Specifies whether the data in a repository is open access
  or controlled access" — a direct match for this slot''s Anonymous/Open/Controlled/Private
  tiers.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
exact_mappings:
- NCIT:C175887
rank: 1000
domain_of:
- GovernanceMixin
range: DataTierEnum
multivalued: true

```
</details></div>