---
search:
  boost: 5.0
---

# Slot: AccessRequirementKey 


_The Access Requirement id(s) associated with this object. Provide multiple values as a comma-separated list._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/AccessRequirementKey](https://w3id.org/sage-bionetworks/governance-duo/slot/AccessRequirementKey)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Resource](../classes/Resource.md) | Information that is relevant to resource access conditions |  no  |
| [Schema](../classes/Schema.md) | Information that is relevant to resource access conditions |  no  |
| [Study](../classes/Study.md) | Studies associated with a grant |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [Resource](../classes/Resource.md), [Schema](../classes/Schema.md), [Study](../classes/Study.md) |

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
| self | governanceduo:AccessRequirementKey |
| native | governanceduo:AccessRequirementKey |




## LinkML Source

<details>
```yaml
name: AccessRequirementKey
annotations:
  foreign_key:
    tag: foreign_key
    value: true
description: The Access Requirement id(s) associated with this object. Provide multiple
  values as a comma-separated list.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- Resource
- Schema
- Study
range: string
multivalued: true

```
</details></div>