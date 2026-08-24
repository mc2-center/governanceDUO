---
search:
  boost: 5.0
---

# Slot: diseaseSpecificResearch 


_The type(s) of disease research allowed by this access requirement. Provide the MONDO ID in format MONDO:id. Provide multiple values as a comma-separated list. MONDO terms can be found here: https://ols.monarchinitiative.org/ontologies/mondo_



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/diseaseSpecificResearch](https://w3id.org/sage-bionetworks/governance-duo/slot/diseaseSpecificResearch)
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
| Regex Pattern | `MONDO:\d{7}` |










## Comments

* Required when dataUseModifiers contains DUO:0000007 — see GovernanceMixin rules.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:diseaseSpecificResearch |
| native | governanceduo:diseaseSpecificResearch |




## LinkML Source

<details>
```yaml
name: diseaseSpecificResearch
description: 'The type(s) of disease research allowed by this access requirement.
  Provide the MONDO ID in format MONDO:id. Provide multiple values as a comma-separated
  list. MONDO terms can be found here: https://ols.monarchinitiative.org/ontologies/mondo'
comments:
- Required when dataUseModifiers contains DUO:0000007 — see GovernanceMixin rules.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- GovernanceMixin
range: string
multivalued: true
pattern: MONDO:\d{7}

```
</details></div>