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








## Comments

* Deliberately an untyped string, not range: AccessRequirement: giving it a real typed range would require importing access_requirement.yaml into this file, but this file (like mixins.yaml) is a leaf that imports only linkml:types specifically so it can never import an entity file and risk an import cycle (see the schema-level description above). governance_graph.yaml can afford real typed ranges for its own cross-references (e.g. accessRequirement: range: AccessRequirement) because it is a single, later-loaded file that already imports everything it references -- this file cannot follow that pattern without breaking its own leaf-file guarantee. Same rationale applies to StudyKey below and to ResourceKey (schema.yaml)/SchemaKey (resource.yaml).



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
comments:
- 'Deliberately an untyped string, not range: AccessRequirement: giving it a real
  typed range would require importing access_requirement.yaml into this file, but
  this file (like mixins.yaml) is a leaf that imports only linkml:types specifically
  so it can never import an entity file and risk an import cycle (see the schema-level
  description above). governance_graph.yaml can afford real typed ranges for its own
  cross-references (e.g. accessRequirement: range: AccessRequirement) because it is
  a single, later-loaded file that already imports everything it references -- this
  file cannot follow that pattern without breaking its own leaf-file guarantee. Same
  rationale applies to StudyKey below and to ResourceKey (schema.yaml)/SchemaKey (resource.yaml).'
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