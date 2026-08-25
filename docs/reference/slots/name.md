---
search:
  boost: 5.0
---

# Slot: name 


_A Synapse-native display name. Shared by SynapseAccessRequirementMixin (ACCESS_REQUIREMENT.NAME) and, via the transitive import chain governance_graph.yaml -> access_requirement.yaml -> mixins.yaml, SynapseEntity (NODE.NAME) in governance_graph.yaml — defined once here rather than in governance_graph.yaml itself, since mixins.yaml cannot import governance_graph.yaml back without creating a cycle (governance_graph.yaml already depends on mixins.yaml through access_requirement.yaml)._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/name](https://w3id.org/sage-bionetworks/governance-duo/slot/name)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [SynapseAccessRequirementMixin](../classes/SynapseAccessRequirementMixin.md) | The real Synapse-native ACCESS_REQUIREMENT row fields (verified against "sage... |  no  |
| [SynapseEntity](../classes/SynapseEntity.md) | A concrete Synapse entity (project, folder, file, etc |  yes  |
| [AccessRequirement](../classes/AccessRequirement.md) | Representation of a Synapse Access Requirement and its relationships to entit... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
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
| self | governanceduo:name |
| native | governanceduo:name |




## LinkML Source

<details>
```yaml
name: name
description: A Synapse-native display name. Shared by SynapseAccessRequirementMixin
  (ACCESS_REQUIREMENT.NAME) and, via the transitive import chain governance_graph.yaml
  -> access_requirement.yaml -> mixins.yaml, SynapseEntity (NODE.NAME) in governance_graph.yaml
  — defined once here rather than in governance_graph.yaml itself, since mixins.yaml
  cannot import governance_graph.yaml back without creating a cycle (governance_graph.yaml
  already depends on mixins.yaml through access_requirement.yaml).
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- SynapseAccessRequirementMixin
- SynapseEntity
range: string

```
</details></div>