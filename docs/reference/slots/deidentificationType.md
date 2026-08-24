---
search:
  boost: 5.0
---

# Slot: deidentificationType 


_The type of de-identification applied to the data associated with the access requirement. Equivalent to DUOPlus3._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/deidentificationType](https://w3id.org/sage-bionetworks/governance-duo/slot/deidentificationType)
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
| Range | [DeidentificationTypeEnum](../enums/DeidentificationTypeEnum.md) |
| Domain Of | [GovernanceMixin](../classes/GovernanceMixin.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |








## Comments

* Required when dataUseModifiers contains DUOPlus3 — see GovernanceMixin rules.
* T4FS:0000414 "de-identification" (Terminology for Food Safety, but the term itself is a generic privacy concept) is a close, not exact, match — this slot names one of a specific set of methods (HIPPA_LDS/SafeHarbor/etc.), the OLS term describes the general technique.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:deidentificationType |
| native | governanceduo:deidentificationType |
| close | T4FS:0000414 |




## LinkML Source

<details>
```yaml
name: deidentificationType
description: The type of de-identification applied to the data associated with the
  access requirement. Equivalent to DUOPlus3.
comments:
- Required when dataUseModifiers contains DUOPlus3 — see GovernanceMixin rules.
- T4FS:0000414 "de-identification" (Terminology for Food Safety, but the term itself
  is a generic privacy concept) is a close, not exact, match — this slot names one
  of a specific set of methods (HIPPA_LDS/SafeHarbor/etc.), the OLS term describes
  the general technique.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
close_mappings:
- T4FS:0000414
rank: 1000
domain_of:
- GovernanceMixin
range: DeidentificationTypeEnum
multivalued: true

```
</details></div>