---
search:
  boost: 5.0
---

# Slot: rejectedReason 


_The reason this submission was rejected, if it was. Synapse's live API names this field `rejectedReason` (`org.sagebionetworks.repo.model.dataaccess.SubmissionStatus`), not `reason`; stored as DATA_ACCESS_SUBMISSION_STATUS.REASON (a BINARY column) in the underlying table._



<div data-search-exclude markdown="1">



URI: [sagegov:rejectedReason](https://sagebionetworks.org/governance/rejectedReason)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataAccessSubmissionStatus](../classes/DataAccessSubmissionStatus.md) | The approval-workflow state of a DataAccessSubmission |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [DataAccessSubmissionStatus](../classes/DataAccessSubmissionStatus.md) |
| Slot URI | [sagegov:rejectedReason](https://sagebionetworks.org/governance/rejectedReason) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:rejectedReason |
| native | governanceduo:rejectedReason |




## LinkML Source

<details>
```yaml
name: rejectedReason
description: The reason this submission was rejected, if it was. Synapse's live API
  names this field `rejectedReason` (`org.sagebionetworks.repo.model.dataaccess.SubmissionStatus`),
  not `reason`; stored as DATA_ACCESS_SUBMISSION_STATUS.REASON (a BINARY column) in
  the underlying table.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:rejectedReason
domain_of:
- DataAccessSubmissionStatus
range: string

```
</details></div>