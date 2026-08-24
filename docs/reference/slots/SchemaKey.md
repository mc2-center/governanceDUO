---
search:
  boost: 5.0
---

# Slot: SchemaKey 


_The Schema id corresponding to a registered JSON schema that describes the access conditions relevant to this Resource._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/SchemaKey](https://w3id.org/sage-bionetworks/governance-duo/slot/SchemaKey)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Resource](../classes/Resource.md) | Information that is relevant to resource access conditions |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [Resource](../classes/Resource.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










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
| self | governanceduo:SchemaKey |
| native | governanceduo:SchemaKey |




## LinkML Source

<details>
```yaml
name: SchemaKey
annotations:
  foreign_key:
    tag: foreign_key
    value: true
description: The Schema id corresponding to a registered JSON schema that describes
  the access conditions relevant to this Resource.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- Resource
range: string

```
</details></div>