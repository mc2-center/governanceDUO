---
search:
  boost: 5.0
---

# Slot: researchProjectId 


_The research project id this submission is associated with (DATA_ACCESS_SUBMISSION.RESEARCH_PROJECT_ID)._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/researchProjectId](https://w3id.org/sage-bionetworks/governance-duo/slot/researchProjectId)
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

### Cardinality and Requirements

| Property | Value |
| --- | --- |








## Comments

* DATA_ACCESS_SUBMISSION.SUBMISSION_SERIALIZED (a BINARY blob, presumably the full submission form data) is not modeled as a structured field.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:researchProjectId |
| native | governanceduo:researchProjectId |




## LinkML Source

<details>
```yaml
name: researchProjectId
description: The research project id this submission is associated with (DATA_ACCESS_SUBMISSION.RESEARCH_PROJECT_ID).
comments:
- DATA_ACCESS_SUBMISSION.SUBMISSION_SERIALIZED (a BINARY blob, presumably the full
  submission form data) is not modeled as a structured field.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- DataAccessSubmission
range: integer

```
</details></div>