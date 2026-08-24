---
search:
  boost: 5.0
---

# Slot: principalId 


_The Synapse numeric id of the user or team (ACL_RESOURCE_ACCESS.GROUP_ID)._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/principalId](https://w3id.org/sage-bionetworks/governance-duo/slot/principalId)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Principal](../classes/Principal.md) | A Synapse user or team being granted access via an ACL |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Integer](../types/Integer.md) |
| Domain Of | [Principal](../classes/Principal.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
### Slot Characteristics

| Property | Value |
| --- | --- |
| Identifier | Yes |












## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:principalId |
| native | governanceduo:principalId |




## LinkML Source

<details>
```yaml
name: principalId
description: The Synapse numeric id of the user or team (ACL_RESOURCE_ACCESS.GROUP_ID).
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
identifier: true
domain_of:
- Principal
range: integer
required: true

```
</details></div>