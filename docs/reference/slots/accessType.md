---
search:
  boost: 5.0
---

# Slot: accessType 


_The kind of access this Access Requirement governs (ACCESS_REQUIREMENT.ACCESS_TYPE). Range is the same AccessTypeEnum used by AccessGrant.permission in governance_graph.yaml — one real Synapse ACCESS_TYPE type backs both an ACL grant's permission and an Access Requirement's own governed access kind._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/accessType](https://w3id.org/sage-bionetworks/governance-duo/slot/accessType)
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
| Range | [AccessTypeEnum](../enums/AccessTypeEnum.md) |
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
| self | governanceduo:accessType |
| native | governanceduo:accessType |




## LinkML Source

<details>
```yaml
name: accessType
description: The kind of access this Access Requirement governs (ACCESS_REQUIREMENT.ACCESS_TYPE).
  Range is the same AccessTypeEnum used by AccessGrant.permission in governance_graph.yaml
  — one real Synapse ACCESS_TYPE type backs both an ACL grant's permission and an
  Access Requirement's own governed access kind.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- SynapseAccessRequirementMixin
range: AccessTypeEnum

```
</details></div>