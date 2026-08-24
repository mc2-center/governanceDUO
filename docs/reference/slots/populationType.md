---
search:
  boost: 5.0
---

# Slot: populationType 


_The population studied in the research associated with the access requirement. Equivalent to DUOPlus2._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/populationType](https://w3id.org/sage-bionetworks/governance-duo/slot/populationType)
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

* Required when dataUseModifiers contains DUOPlus2 — see GovernanceMixin rules.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:populationType |
| native | governanceduo:populationType |




## LinkML Source

<details>
```yaml
name: populationType
description: The population studied in the research associated with the access requirement.
  Equivalent to DUOPlus2.
comments:
- Required when dataUseModifiers contains DUOPlus2 — see GovernanceMixin rules.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- GovernanceMixin
range: string

```
</details></div>