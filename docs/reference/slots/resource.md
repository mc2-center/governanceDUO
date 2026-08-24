---
search:
  boost: 5.0
---

# Slot: resource 


_The SynapseEntity this grant/association applies to._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/resource](https://w3id.org/sage-bionetworks/governance-duo/slot/resource)
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
| Range | [SynapseEntity](../classes/SynapseEntity.md) |
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
| self | governanceduo:resource |
| native | governanceduo:resource |




## LinkML Source

<details>
```yaml
name: resource
description: The SynapseEntity this grant/association applies to.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- AccessGrant
- AccessRequirementAssociation
range: SynapseEntity
required: true

```
</details></div>