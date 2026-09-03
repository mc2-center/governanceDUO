---
search:
  boost: 5.0
---

# Slot: submittedOn 


_When this record was submitted (epoch milliseconds; `Submission.submittedOn` in Synapse's live REST API)._



<div data-search-exclude markdown="1">



URI: [sagegov:submittedOn](https://sagebionetworks.org/governance/submittedOn)
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
| Slot URI | [sagegov:submittedOn](https://sagebionetworks.org/governance/submittedOn) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:submittedOn |
| native | governanceduo:submittedOn |




## LinkML Source

<details>
```yaml
name: submittedOn
description: When this record was submitted (epoch milliseconds; `Submission.submittedOn`
  in Synapse's live REST API).
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:submittedOn
domain_of:
- DataAccessSubmission
range: integer

```
</details></div>