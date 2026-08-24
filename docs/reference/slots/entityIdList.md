---
search:
  boost: 5.0
---

# Slot: entityIdList 


_Synapse ID(s) for Synapse container(s) (e.g. Project, Dataset, Folder, Table, etc.) with which the Access Requirement is expected to be associated. Provide multiple values as a comma-separated list._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/entityIdList](https://w3id.org/sage-bionetworks/governance-duo/slot/entityIdList)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AccessRequirement](../classes/AccessRequirement.md) | Representation of a Synapse Access Requirement and its relationships to entit... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [AccessRequirement](../classes/AccessRequirement.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:entityIdList |
| native | governanceduo:entityIdList |




## LinkML Source

<details>
```yaml
name: entityIdList
description: Synapse ID(s) for Synapse container(s) (e.g. Project, Dataset, Folder,
  Table, etc.) with which the Access Requirement is expected to be associated. Provide
  multiple values as a comma-separated list.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- AccessRequirement
range: string
multivalued: true

```
</details></div>