---
search:
  boost: 5.0
---

# Slot: registeredSchemaUrl 


_URL associated with the annotation schema that will be applied to the resource type._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/registeredSchemaUrl](https://w3id.org/sage-bionetworks/governance-duo/slot/registeredSchemaUrl)
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








## Comments

* dcterms:conformsTo, "An established standard to which the described resource conforms" — exact match: this URL points at the registered JSON schema the resource must conform to.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:registeredSchemaUrl |
| native | governanceduo:registeredSchemaUrl |
| exact | dcterms:conformsTo |




## LinkML Source

<details>
```yaml
name: registeredSchemaUrl
description: URL associated with the annotation schema that will be applied to the
  resource type.
comments:
- 'dcterms:conformsTo, "An established standard to which the described resource conforms"
  — exact match: this URL points at the registered JSON schema the resource must conform
  to.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
exact_mappings:
- dcterms:conformsTo
rank: 1000
domain_of:
- Resource
range: string

```
</details></div>