---
search:
  boost: 5.0
---

# Slot: accessorId 


_Synapse numeric id of the Principal approved for access (AccessApproval.accessorId). Emitted as an IRI reference to a sagegov:Principal node, mapping onto the target ontology's gov:heldBy predicate._



<div data-search-exclude markdown="1">



URI: [sagegov:heldBy](https://sagebionetworks.org/governance/heldBy)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AccessApproval](../classes/AccessApproval.md) | Records that a Principal has been approved for access under an AccessRequirem... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Integer](../types/Integer.md) |
| Domain Of | [AccessApproval](../classes/AccessApproval.md) |
| Slot URI | [sagegov:heldBy](https://sagebionetworks.org/governance/heldBy) |

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
| self | sagegov:heldBy |
| native | governanceduo:accessorId |




## LinkML Source

<details>
```yaml
name: accessorId
description: Synapse numeric id of the Principal approved for access (AccessApproval.accessorId).
  Emitted as an IRI reference to a sagegov:Principal node, mapping onto the target
  ontology's gov:heldBy predicate.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:heldBy
domain_of:
- AccessApproval
range: integer
required: true

```
</details></div>