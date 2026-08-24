---
search:
  boost: 5.0
---

# Slot: principalType 

<div data-search-exclude markdown="1">



URI: [governanceduo:slot/principalType](https://w3id.org/sage-bionetworks/governance-duo/slot/principalType)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Principal](../classes/Principal.md) | A Synapse user or team being granted access via an ACL |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [PrincipalTypeEnum](../enums/PrincipalTypeEnum.md) |
| Domain Of | [Principal](../classes/Principal.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:principalType |
| native | governanceduo:principalType |




## LinkML Source

<details>
```yaml
name: principalType
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- Principal
range: PrincipalTypeEnum
required: true

```
</details></div>