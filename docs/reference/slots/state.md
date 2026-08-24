---
search:
  boost: 5.0
---

# Slot: state 

<div data-search-exclude markdown="1">



URI: [governanceduo:slot/state](https://w3id.org/sage-bionetworks/governance-duo/slot/state)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataAccessSubmissionStatus](../classes/DataAccessSubmissionStatus.md) | The approval-workflow state of a DataAccessSubmission |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [SubmissionStateEnum](../enums/SubmissionStateEnum.md) |
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
| self | governanceduo:state |
| native | governanceduo:state |




## LinkML Source

<details>
```yaml
name: state
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- DataAccessSubmissionStatus
range: SubmissionStateEnum
required: true

```
</details></div>