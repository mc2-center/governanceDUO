---
search:
  boost: 5.0
---

# Slot: referencedRequirementId 


_The id of the real AccessRequirement record this gov:AR-<n> stub stands in for (e.g. access_requirement.42) -- the stub's key. As a LinkML identifier it names the node rather than adding a triple: scripts/build_governance_graph.py mints the stub's IRI from it via gov_id() (access_requirement.42 -> gov:AR-42) and bridges it to the real record with sameAs._



<div data-search-exclude markdown="1">



URI: [governanceduo:referencedRequirementId](https://w3id.org/sage-bionetworks/governance-duo/referencedRequirementId)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AccessRequirementReference](../classes/AccessRequirementReference.md) | The gov:AR-<n> stub build_governance_graph |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [AccessRequirementReference](../classes/AccessRequirementReference.md) |
| Slot URI | [governanceduo:referencedRequirementId](https://w3id.org/sage-bionetworks/governance-duo/referencedRequirementId) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
### Slot Characteristics

| Property | Value |
| --- | --- |
| Identifier | Yes |


### Value Constraints

| Property | Value |
| --- | --- |
| Regex Pattern | `^access_requirement\.\d+$` |












## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:referencedRequirementId |
| native | governanceduo:referencedRequirementId |




## LinkML Source

<details>
```yaml
name: referencedRequirementId
description: 'The id of the real AccessRequirement record this gov:AR-<n> stub stands
  in for (e.g. access_requirement.42) -- the stub''s key. As a LinkML identifier it
  names the node rather than adding a triple: scripts/build_governance_graph.py mints
  the stub''s IRI from it via gov_id() (access_requirement.42 -> gov:AR-42) and bridges
  it to the real record with sameAs.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: governanceduo:referencedRequirementId
identifier: true
domain_of:
- AccessRequirementReference
range: string
required: true
pattern: ^access_requirement\.\d+$

```
</details></div>