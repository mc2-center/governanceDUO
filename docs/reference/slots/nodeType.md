---
search:
  boost: 5.0
---

# Slot: nodeType 


_The kind of Synapse entity (NODE.NODE_TYPE), e.g. project, folder, file, table. **Not independently verified** against a canonical enum in this pass — modeled as an open string rather than a fabricated enum, unlike AccessTypeEnum/AccessRequirementConcreteTypeEnum/SubmissionStateEnum above, all three of which were confirmed against a real source. Common Synapse entity types (project/folder/file/link/table/view/dockerrepo) are well known but not cited here as a closed, checked list._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/nodeType](https://w3id.org/sage-bionetworks/governance-duo/slot/nodeType)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [SynapseEntity](../classes/SynapseEntity.md) | A concrete Synapse entity (project, folder, file, etc |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [SynapseEntity](../classes/SynapseEntity.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:nodeType |
| native | governanceduo:nodeType |




## LinkML Source

<details>
```yaml
name: nodeType
description: The kind of Synapse entity (NODE.NODE_TYPE), e.g. project, folder, file,
  table. **Not independently verified** against a canonical enum in this pass — modeled
  as an open string rather than a fabricated enum, unlike AccessTypeEnum/AccessRequirementConcreteTypeEnum/SubmissionStateEnum
  above, all three of which were confirmed against a real source. Common Synapse entity
  types (project/folder/file/link/table/view/dockerrepo) are well known but not cited
  here as a closed, checked list.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- SynapseEntity
range: string

```
</details></div>