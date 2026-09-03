---
search:
  boost: 5.0
---

# Slot: status 


_The state of this approval (AccessApproval.state in Synapse's live REST API -- renamed to "status" here specifically to avoid colliding with DataAccessSubmission/Status's own "state" slot, which ranges over the unrelated SubmissionStateEnum). Maps onto the target ontology's gov:status._



<div data-search-exclude markdown="1">



URI: [sagegov:status](https://sagebionetworks.org/governance/status)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AccessApproval](../classes/AccessApproval.md) | Records that a Principal has been approved for access under an AccessRequirem... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [ApprovalStateEnum](../enums/ApprovalStateEnum.md) |
| Domain Of | [AccessApproval](../classes/AccessApproval.md) |
| Slot URI | [sagegov:status](https://sagebionetworks.org/governance/status) |

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
| self | sagegov:status |
| native | governanceduo:status |




## LinkML Source

<details>
```yaml
name: status
description: The state of this approval (AccessApproval.state in Synapse's live REST
  API -- renamed to "status" here specifically to avoid colliding with DataAccessSubmission/Status's
  own "state" slot, which ranges over the unrelated SubmissionStateEnum). Maps onto
  the target ontology's gov:status.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:status
domain_of:
- AccessApproval
range: ApprovalStateEnum
required: true

```
</details></div>