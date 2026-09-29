---
search:
  boost: 5.0
---

# Slot: irbAssociatedProjects 


_Synapse Project id(s) this IRB approval covers directly, for cases not already reachable through a linked Study record. Provide multiple values as a comma-separated list._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/irbAssociatedProjects](https://w3id.org/sage-bionetworks/governance-duo/slot/irbAssociatedProjects)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [IRB](../classes/IRB.md) | An Institutional Review Board (or equivalent Ethics Review Board) approval re... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [IRB](../classes/IRB.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |
### Value Constraints

| Property | Value |
| --- | --- |
| Regex Pattern | `^syn\d+$` |












## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:irbAssociatedProjects |
| native | governanceduo:irbAssociatedProjects |




## LinkML Source

<details>
```yaml
name: irbAssociatedProjects
description: Synapse Project id(s) this IRB approval covers directly, for cases not
  already reachable through a linked Study record. Provide multiple values as a comma-separated
  list.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- IRB
range: string
multivalued: true
pattern: ^syn\d+$

```
</details></div>