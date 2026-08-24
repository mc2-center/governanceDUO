---
search:
  boost: 5.0
---

# Slot: StudyKey 


_The Study id(s) associated with this object. Provide multiple values as a comma-separated list._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/StudyKey](https://w3id.org/sage-bionetworks/governance-duo/slot/StudyKey)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AccessRequirement](../classes/AccessRequirement.md) | Representation of a Synapse Access Requirement and its relationships to entit... |  no  |
| [Resource](../classes/Resource.md) | Information that is relevant to resource access conditions |  no  |
| [Schema](../classes/Schema.md) | Information that is relevant to resource access conditions |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [AccessRequirement](../classes/AccessRequirement.md), [Resource](../classes/Resource.md), [Schema](../classes/Schema.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |










## Identifier and Mapping Information



### Annotations

| property | value |
| --- | --- |
| foreign_key | True |




### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:StudyKey |
| native | governanceduo:StudyKey |




## LinkML Source

<details>
```yaml
name: StudyKey
annotations:
  foreign_key:
    tag: foreign_key
    value: true
description: The Study id(s) associated with this object. Provide multiple values
  as a comma-separated list.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- AccessRequirement
- Resource
- Schema
range: string
multivalued: true

```
</details></div>