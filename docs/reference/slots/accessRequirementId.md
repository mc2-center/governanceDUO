---
search:
  boost: 5.0
---

# Slot: accessRequirementId 


_The AccessRequirement this submission is an application against (DATA_ACCESS_SUBMISSION.ACCESS_REQUIREMENT_ID)._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/accessRequirementId](https://w3id.org/sage-bionetworks/governance-duo/slot/accessRequirementId)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataAccessSubmission](../classes/DataAccessSubmission.md) | A user's application against an AccessRequirement |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [AccessRequirement](../classes/AccessRequirement.md) |
| Domain Of | [DataAccessSubmission](../classes/DataAccessSubmission.md) |

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
| self | governanceduo:accessRequirementId |
| native | governanceduo:accessRequirementId |
| close | dcterms:requires |




## LinkML Source

<details>
```yaml
name: accessRequirementId
description: The AccessRequirement this submission is an application against (DATA_ACCESS_SUBMISSION.ACCESS_REQUIREMENT_ID).
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
close_mappings:
- dcterms:requires
rank: 1000
domain_of:
- DataAccessSubmission
range: AccessRequirement
required: true

```
</details></div>