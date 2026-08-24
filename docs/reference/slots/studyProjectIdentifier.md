---
search:
  boost: 5.0
---

# Slot: studyProjectIdentifier 


_The Synapse Project identifier (synID) with which this Study is related._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/studyProjectIdentifier](https://w3id.org/sage-bionetworks/governance-duo/slot/studyProjectIdentifier)
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
### Value Constraints

| Property | Value |
| --- | --- |
| Regex Pattern | `syn[0-9]+` |












## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:studyProjectIdentifier |
| native | governanceduo:studyProjectIdentifier |




## LinkML Source

<details>
```yaml
name: studyProjectIdentifier
description: The Synapse Project identifier (synID) with which this Study is related.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- Study
range: string
multivalued: true
pattern: syn[0-9]+

```
</details></div>