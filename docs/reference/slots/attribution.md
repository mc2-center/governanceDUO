---
search:
  boost: 5.0
---

# Slot: attribution 


_The attribution statement for the data associated with the access requirement. Equivalent to DUOPlus7._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/attribution](https://w3id.org/sage-bionetworks/governance-duo/slot/attribution)
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

* Required when dataUseModifiers contains DUOPlus7 — see GovernanceMixin rules.
* SWO:9000006 "Attribution clause" (Software Ontology term, reused via the mcro ontology) — a license-clause-shaped close mapping; this slot instead holds the free-text statement itself, not the clause concept.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:attribution |
| native | governanceduo:attribution |
| close | ebiswo:9000006 |




## LinkML Source

<details>
```yaml
name: attribution
description: The attribution statement for the data associated with the access requirement.
  Equivalent to DUOPlus7.
comments:
- Required when dataUseModifiers contains DUOPlus7 — see GovernanceMixin rules.
- SWO:9000006 "Attribution clause" (Software Ontology term, reused via the mcro ontology)
  — a license-clause-shaped close mapping; this slot instead holds the free-text statement
  itself, not the clause concept.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
close_mappings:
- ebiswo:9000006
rank: 1000
domain_of:
- GovernanceMixin
range: string

```
</details></div>