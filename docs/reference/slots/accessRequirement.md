---
search:
  boost: 5.0
---

# Slot: accessRequirement 


_The AccessRequirement this association binds to the resource._



<div data-search-exclude markdown="1">



URI: [sagegov:accessRequirement](https://sagebionetworks.org/governance/accessRequirement)
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
| Slot URI | [sagegov:accessRequirement](https://sagebionetworks.org/governance/accessRequirement) |

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
| self | sagegov:accessRequirement |
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
slot_uri: sagegov:accessRequirement
domain_of:
- AccessRequirementAssociation
range: AccessRequirement
required: true

```
</details></div>