---
search:
  boost: 5.0
---

# Slot: dataPermission 


_The permissions associated with the data under the access requirement. Equivalent to DUOPlus4._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/dataPermission](https://w3id.org/sage-bionetworks/governance-duo/slot/dataPermission)
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
| Range | [DataPermissionEnum](../enums/DataPermissionEnum.md) |
| Domain Of | [GovernanceMixin](../classes/GovernanceMixin.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |








## Comments

* Required when dataUseModifiers contains DUOPlus4 — see GovernanceMixin rules.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:dataPermission |
| native | governanceduo:dataPermission |




## LinkML Source

<details>
```yaml
name: dataPermission
description: The permissions associated with the data under the access requirement.
  Equivalent to DUOPlus4.
comments:
- Required when dataUseModifiers contains DUOPlus4 — see GovernanceMixin rules.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- GovernanceMixin
range: DataPermissionEnum
multivalued: true

```
</details></div>