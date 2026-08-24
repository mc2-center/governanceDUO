---
search:
  boost: 5.0
---

# Slot: currentRevNum 


_The current revision number of the record. Shared the same way as `name` above, by SynapseAccessRequirementMixin (ACCESS_REQUIREMENT.CURRENT_REV_NUM) and SynapseEntity (NODE.CURRENT_REV_NUM)._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/currentRevNum](https://w3id.org/sage-bionetworks/governance-duo/slot/currentRevNum)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [SynapseAccessRequirementMixin](../classes/SynapseAccessRequirementMixin.md) | The real Synapse-native ACCESS_REQUIREMENT row fields (verified against "sage... |  no  |
| [SynapseEntity](../classes/SynapseEntity.md) | A concrete Synapse entity (project, folder, file, etc |  no  |
| [AccessRequirement](../classes/AccessRequirement.md) | Representation of a Synapse Access Requirement and its relationships to entit... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Integer](../types/Integer.md) |
| Domain Of | [SynapseAccessRequirementMixin](../classes/SynapseAccessRequirementMixin.md), [SynapseEntity](../classes/SynapseEntity.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:currentRevNum |
| native | governanceduo:currentRevNum |




## LinkML Source

<details>
```yaml
name: currentRevNum
description: The current revision number of the record. Shared the same way as `name`
  above, by SynapseAccessRequirementMixin (ACCESS_REQUIREMENT.CURRENT_REV_NUM) and
  SynapseEntity (NODE.CURRENT_REV_NUM).
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- SynapseAccessRequirementMixin
- SynapseEntity
range: integer

```
</details></div>