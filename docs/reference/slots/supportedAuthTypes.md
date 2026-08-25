---
search:
  boost: 5.0
---

# Slot: supportedAuthTypes 


_Mirrors DRS's Authorizations.supported_types for objects governed by this DUO code._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/supportedAuthTypes](https://w3id.org/sage-bionetworks/governance-duo/slot/supportedAuthTypes)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DrsAuthorizationBinding](../classes/DrsAuthorizationBinding.md) | Crosswalks one DUO code (or Sage DUOPlus extension) to the shape of the DRS A... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [DrsAuthTypeEnum](../enums/DrsAuthTypeEnum.md) |
| Domain Of | [DrsAuthorizationBinding](../classes/DrsAuthorizationBinding.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |
### Slot Characteristics

| Property | Value |
| --- | --- |
| If Absent | `PassportAuth` |












## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:supportedAuthTypes |
| native | governanceduo:supportedAuthTypes |




## LinkML Source

<details>
```yaml
name: supportedAuthTypes
description: Mirrors DRS's Authorizations.supported_types for objects governed by
  this DUO code.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
ifabsent: PassportAuth
domain_of:
- DrsAuthorizationBinding
range: DrsAuthTypeEnum
multivalued: true

```
</details></div>