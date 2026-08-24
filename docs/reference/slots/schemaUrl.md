---
search:
  boost: 5.0
---

# Slot: schemaUrl 


_The registered URL associated with the access requirement JSON schema._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/schemaUrl](https://w3id.org/sage-bionetworks/governance-duo/slot/schemaUrl)
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








## Comments

* dcterms:conformsTo, "An established standard to which the described resource conforms" — see resource.yaml's registeredSchemaUrl for the same exact mapping and rationale.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:schemaUrl |
| native | governanceduo:schemaUrl |
| exact | dcterms:conformsTo |




## LinkML Source

<details>
```yaml
name: schemaUrl
description: The registered URL associated with the access requirement JSON schema.
comments:
- dcterms:conformsTo, "An established standard to which the described resource conforms"
  — see resource.yaml's registeredSchemaUrl for the same exact mapping and rationale.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
exact_mappings:
- dcterms:conformsTo
rank: 1000
domain_of:
- Schema
range: string

```
</details></div>