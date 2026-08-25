---
search:
  boost: 5.0
---

# Slot: bindingType 

<div data-search-exclude markdown="1">



URI: [sagegov:bindingType](https://sagebionetworks.org/governance/bindingType)
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
| Slot URI | [sagegov:bindingType](https://sagebionetworks.org/governance/bindingType) |

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
| self | sagegov:bindingType |
| native | governanceduo:bindingType |




## LinkML Source

<details>
```yaml
name: bindingType
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:bindingType
domain_of:
- AccessGrant
- AccessRequirementAssociation
range: BindingTypeEnum
required: true

```
</details></div>