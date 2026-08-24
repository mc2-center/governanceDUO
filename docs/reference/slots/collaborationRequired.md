---
search:
  boost: 5.0
---

# Slot: collaborationRequired 


_If collaboration is required for the access requirement, provide the PI email address. Provide multiple as a comma-separated list._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/collaborationRequired](https://w3id.org/sage-bionetworks/governance-duo/slot/collaborationRequired)
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
| Range | [String](../types/String.md) |
| Domain Of | [GovernanceMixin](../classes/GovernanceMixin.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |








## Comments

* Required when dataUseModifiers contains DUO:0000020 — see GovernanceMixin rules.
* NCIT:C221739 "Consent for Use Requires Collaboration Agreement" carries the synonyms "COL"/"Collaboration required", the same shorthand this repo already uses for DUO:0000020 — verified live and non-obsolete via the OLS4 API.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:collaborationRequired |
| native | governanceduo:collaborationRequired |
| exact | NCIT:C221739 |




## LinkML Source

<details>
```yaml
name: collaborationRequired
description: If collaboration is required for the access requirement, provide the
  PI email address. Provide multiple as a comma-separated list.
comments:
- Required when dataUseModifiers contains DUO:0000020 — see GovernanceMixin rules.
- NCIT:C221739 "Consent for Use Requires Collaboration Agreement" carries the synonyms
  "COL"/"Collaboration required", the same shorthand this repo already uses for DUO:0000020
  — verified live and non-obsolete via the OLS4 API.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
exact_mappings:
- NCIT:C221739
rank: 1000
domain_of:
- GovernanceMixin
range: string

```
</details></div>