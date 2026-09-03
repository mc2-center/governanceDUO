---
search:
  boost: 5.0
---

# Slot: requestId 


_The originating data access request id. Synapse's live API names this field `requestId` (`org.sagebionetworks.repo.model.dataaccess.Submission`), not `dataAccessRequestId`; the underlying DB column is DATA_ACCESS_SUBMISSION.DATA_ACCESS_REQUEST_ID._



<div data-search-exclude markdown="1">



URI: [sagegov:requestId](https://sagebionetworks.org/governance/requestId)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataAccessSubmission](../classes/DataAccessSubmission.md) | A user's application against an AccessRequirement |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Integer](../types/Integer.md) |
| Domain Of | [DataAccessSubmission](../classes/DataAccessSubmission.md) |
| Slot URI | [sagegov:requestId](https://sagebionetworks.org/governance/requestId) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:requestId |
| native | governanceduo:requestId |




## LinkML Source

<details>
```yaml
name: requestId
description: The originating data access request id. Synapse's live API names this
  field `requestId` (`org.sagebionetworks.repo.model.dataaccess.Submission`), not
  `dataAccessRequestId`; the underlying DB column is DATA_ACCESS_SUBMISSION.DATA_ACCESS_REQUEST_ID.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:requestId
domain_of:
- DataAccessSubmission
range: integer

```
</details></div>