---
search:
  boost: 5.0
---

# Slot: accessRequirement 


_The AccessRequirement this association binds to the resource._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/accessRequirement](https://w3id.org/sage-bionetworks/governance-duo/slot/accessRequirement)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AccessRequirementAssociation](../classes/AccessRequirementAssociation.md) | Binds an AccessRequirement to a resource, recording whether the binding is di... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [AccessRequirement](../classes/AccessRequirement.md) |
| Domain Of | [AccessRequirementAssociation](../classes/AccessRequirementAssociation.md) |

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
| self | governanceduo:accessRequirement |
| native | governanceduo:accessRequirement |
| close | dcterms:requires |




## LinkML Source

<details>
```yaml
name: accessRequirement
description: The AccessRequirement this association binds to the resource.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
close_mappings:
- dcterms:requires
rank: 1000
domain_of:
- AccessRequirementAssociation
range: AccessRequirement
required: true

```
</details></div>