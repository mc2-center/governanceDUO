---
search:
  boost: 5.0
---

# Slot: parentId 


_The parent Synapse entity in the containment hierarchy (NODE.PARENT_ID) — used to resolve direct-vs-inherited governance (e.g. a file inheriting its parent study's Access Requirement, per the design doc's "Direct and Inherited Governance" section)._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/parentId](https://w3id.org/sage-bionetworks/governance-duo/slot/parentId)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [SynapseEntity](../classes/SynapseEntity.md) | A concrete Synapse entity (project, folder, file, etc |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [SynapseEntity](../classes/SynapseEntity.md) |
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
| self | governanceduo:parentId |
| native | governanceduo:parentId |
| exact | dcterms:isPartOf |




## LinkML Source

<details>
```yaml
name: parentId
description: The parent Synapse entity in the containment hierarchy (NODE.PARENT_ID)
  — used to resolve direct-vs-inherited governance (e.g. a file inheriting its parent
  study's Access Requirement, per the design doc's "Direct and Inherited Governance"
  section).
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
exact_mappings:
- dcterms:isPartOf
rank: 1000
domain_of:
- SynapseEntity
range: SynapseEntity

```
</details></div>