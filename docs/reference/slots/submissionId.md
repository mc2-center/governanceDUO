---
search:
  boost: 5.0
---

# Slot: submissionId 


_The DataAccessSubmission this status record applies to (DATA_ACCESS_SUBMISSION_STATUS.SUBMISSION_ID)._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/submissionId](https://w3id.org/sage-bionetworks/governance-duo/slot/submissionId)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataAccessSubmissionStatus](../classes/DataAccessSubmissionStatus.md) | The approval-workflow state of a DataAccessSubmission |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [DataAccessSubmission](../classes/DataAccessSubmission.md) |
| Domain Of | [DataAccessSubmissionStatus](../classes/DataAccessSubmissionStatus.md) |

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
| self | governanceduo:submissionId |
| native | governanceduo:submissionId |




## LinkML Source

<details>
```yaml
name: submissionId
description: The DataAccessSubmission this status record applies to (DATA_ACCESS_SUBMISSION_STATUS.SUBMISSION_ID).
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- DataAccessSubmissionStatus
range: DataAccessSubmission
required: true

```
</details></div>