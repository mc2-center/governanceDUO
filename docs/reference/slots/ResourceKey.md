---
search:
  boost: 5.0
---

# Slot: ResourceKey 


_The identifier(s) for the Resource(s) associated with this schema. Provide multiple values as a comma-separated list._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/ResourceKey](https://w3id.org/sage-bionetworks/governance-duo/slot/ResourceKey)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Schema](../classes/Schema.md) | Information that is relevant to resource access conditions |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [Schema](../classes/Schema.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |








## Comments

* Untyped string, not range: Resource -- see props.yaml's AccessRequirementKey comment for why (this file cannot import resource.yaml without risking a cycle).



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
| self | governanceduo:ResourceKey |
| native | governanceduo:ResourceKey |




## LinkML Source

<details>
```yaml
name: ResourceKey
annotations:
  foreign_key:
    tag: foreign_key
    value: true
description: The identifier(s) for the Resource(s) associated with this schema. Provide
  multiple values as a comma-separated list.
comments:
- 'Untyped string, not range: Resource -- see props.yaml''s AccessRequirementKey comment
  for why (this file cannot import resource.yaml without risking a cycle).'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- Schema
range: string
multivalued: true

```
</details></div>