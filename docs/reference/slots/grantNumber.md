---
search:
  boost: 5.0
---

# Slot: grantNumber 


_The identifier associated with the award funding this study._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/grantNumber](https://w3id.org/sage-bionetworks/governance-duo/slot/grantNumber)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Study](../classes/Study.md) | Studies associated with a grant |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [Study](../classes/Study.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |








## Comments

* EVORAO:grantNumber, "A formal reference or agreement number assigned by the funding body" — verified live and non-obsolete via the OLS4 API.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:grantNumber |
| native | governanceduo:grantNumber |
| exact | EVORAO:grantNumber |




## LinkML Source

<details>
```yaml
name: grantNumber
description: The identifier associated with the award funding this study.
comments:
- EVORAO:grantNumber, "A formal reference or agreement number assigned by the funding
  body" — verified live and non-obsolete via the OLS4 API.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
exact_mappings:
- EVORAO:grantNumber
rank: 1000
domain_of:
- Study
range: string
multivalued: true

```
</details></div>