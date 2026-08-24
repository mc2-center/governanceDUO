---
search:
  boost: 5.0
---

# Slot: reason 


_The reason for the current state (e.g. a rejection reason). Stored as DATA_ACCESS_SUBMISSION_STATUS.REASON, a BINARY column in Synapse; modeled here as a plain string._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/reason](https://w3id.org/sage-bionetworks/governance-duo/slot/reason)
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

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:reason |
| native | governanceduo:reason |




## LinkML Source

<details>
```yaml
name: reason
description: The reason for the current state (e.g. a rejection reason). Stored as
  DATA_ACCESS_SUBMISSION_STATUS.REASON, a BINARY column in Synapse; modeled here as
  a plain string.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- DataAccessSubmissionStatus
range: string

```
</details></div>