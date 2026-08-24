---
search:
  boost: 5.0
---

# Slot: isTwoFaRequired 


_Whether two-factor authentication is required (ACCESS_REQUIREMENT.IS_TWO_FA_REQUIRED)._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/isTwoFaRequired](https://w3id.org/sage-bionetworks/governance-duo/slot/isTwoFaRequired)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [SynapseAccessRequirementMixin](../classes/SynapseAccessRequirementMixin.md) | The real Synapse-native ACCESS_REQUIREMENT row fields (verified against "sage... |  no  |
| [AccessRequirement](../classes/AccessRequirement.md) | Representation of a Synapse Access Requirement and its relationships to entit... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Boolean](../types/Boolean.md) |
| Domain Of | [SynapseAccessRequirementMixin](../classes/SynapseAccessRequirementMixin.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:isTwoFaRequired |
| native | governanceduo:isTwoFaRequired |




## LinkML Source

<details>
```yaml
name: isTwoFaRequired
description: Whether two-factor authentication is required (ACCESS_REQUIREMENT.IS_TWO_FA_REQUIRED).
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- SynapseAccessRequirementMixin
range: boolean

```
</details></div>