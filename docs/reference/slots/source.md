---
search:
  boost: 5.0
---

# Slot: source 


_The system this grant/association was derived from, e.g. "Synapse"._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/source](https://w3id.org/sage-bionetworks/governance-duo/slot/source)
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
| Range | [String](../types/String.md) |
| Domain Of | [AccessGrant](../classes/AccessGrant.md), [AccessRequirementAssociation](../classes/AccessRequirementAssociation.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:source |
| native | governanceduo:source |
| exact | dcterms:source |




## LinkML Source

<details>
```yaml
name: source
description: The system this grant/association was derived from, e.g. "Synapse".
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
exact_mappings:
- dcterms:source
rank: 1000
domain_of:
- AccessGrant
- AccessRequirementAssociation
range: string

```
</details></div>