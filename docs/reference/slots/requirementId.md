---
search:
  boost: 5.0
---

# Slot: requirementId 


_The AccessRequirement this approval satisfies (AccessApproval.requirementId in Synapse's live REST API). Distinct LinkML slot from AccessRequirementAssociation.accessRequirement/ DataAccessSubmission.accessRequirementId (which share sagegov:accessRequirement) -- this one maps onto the target ontology's gov:satisfies predicate instead, since AccessApproval specifically represents *satisfaction* of a requirement, not just a binding or an application against it._



<div data-search-exclude markdown="1">



URI: [sagegov:satisfies](https://sagebionetworks.org/governance/satisfies)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AccessApproval](../classes/AccessApproval.md) | Records that a Principal has been approved for access under an AccessRequirem... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [AccessRequirement](../classes/AccessRequirement.md) |
| Domain Of | [AccessApproval](../classes/AccessApproval.md) |
| Slot URI | [sagegov:satisfies](https://sagebionetworks.org/governance/satisfies) |

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
| self | sagegov:satisfies |
| native | governanceduo:requirementId |




## LinkML Source

<details>
```yaml
name: requirementId
description: The AccessRequirement this approval satisfies (AccessApproval.requirementId
  in Synapse's live REST API). Distinct LinkML slot from AccessRequirementAssociation.accessRequirement/
  DataAccessSubmission.accessRequirementId (which share sagegov:accessRequirement)
  -- this one maps onto the target ontology's gov:satisfies predicate instead, since
  AccessApproval specifically represents *satisfaction* of a requirement, not just
  a binding or an application against it.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:satisfies
domain_of:
- AccessApproval
range: AccessRequirement
required: true

```
</details></div>