---
search:
  boost: 5.0
---

# Slot: bindingType 

<div data-search-exclude markdown="1">



URI: [governanceduo:slot/bindingType](https://w3id.org/sage-bionetworks/governance-duo/slot/bindingType)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AccessGrant](../classes/AccessGrant.md) | A first-class ACL grant: resource, principal, permission(s), source, and whet... |  no  |
| [AccessRequirementAssociation](../classes/AccessRequirementAssociation.md) | Binds an AccessRequirement to a resource, recording whether the binding is di... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [BindingTypeEnum](../enums/BindingTypeEnum.md) |
| Domain Of | [AccessGrant](../classes/AccessGrant.md), [AccessRequirementAssociation](../classes/AccessRequirementAssociation.md) |

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
| self | governanceduo:bindingType |
| native | governanceduo:bindingType |




## LinkML Source

<details>
```yaml
name: bindingType
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- AccessGrant
- AccessRequirementAssociation
range: BindingTypeEnum
required: true

```
</details></div>