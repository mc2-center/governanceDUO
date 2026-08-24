---
search:
  boost: 5.0
---

# Slot: institutionSpecificRestriction 


_Institutions with specific restrictions associated with the access requirement. Provide the institution ROR ID in format ROR:id. Provide multiple entries as a comma-separated list. ROR IDs can be found here: https://ror.org/search_



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/institutionSpecificRestriction](https://w3id.org/sage-bionetworks/governance-duo/slot/institutionSpecificRestriction)
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
| Multivalued | Yes |
### Value Constraints

| Property | Value |
| --- | --- |
| Regex Pattern | `ROR:[a-z0-9]{9}` |










## Comments

* Required when dataUseModifiers contains DUO:0000028 — see GovernanceMixin rules.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:institutionSpecificRestriction |
| native | governanceduo:institutionSpecificRestriction |




## LinkML Source

<details>
```yaml
name: institutionSpecificRestriction
description: 'Institutions with specific restrictions associated with the access requirement.
  Provide the institution ROR ID in format ROR:id. Provide multiple entries as a comma-separated
  list. ROR IDs can be found here: https://ror.org/search'
comments:
- Required when dataUseModifiers contains DUO:0000028 — see GovernanceMixin rules.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- GovernanceMixin
range: string
multivalued: true
pattern: ROR:[a-z0-9]{9}

```
</details></div>