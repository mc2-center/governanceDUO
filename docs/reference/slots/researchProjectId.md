---
search:
  boost: 5.0
---

# Slot: researchProjectId 


_The research project this submission/request is associated with (DATA_ACCESS_SUBMISSION.RESEARCH_PROJECT_ID / RequestInterface.researchProjectId). Range is now `ResearchProject` (was a bare integer literal until that class existed -- see plans/governance_graph_open_questions.md Section C) -- emitted as an IRI reference to the real `gov:research-project-<n>` node. Shared predicate across DataAccessSubmission and DataAccessRequest, both of which reference the same real-world ResearchProject._



<div data-search-exclude markdown="1">



URI: [sagegov:researchProject](https://sagebionetworks.org/governance/researchProject)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataAccessSubmission](../classes/DataAccessSubmission.md) | A user's application against an AccessRequirement |  no  |
| [DataAccessRequest](../classes/DataAccessRequest.md) | A user's draft/submitted request against an AccessRequirement, behind a DataA... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [ResearchProject](../classes/ResearchProject.md) |
| Domain Of | [DataAccessSubmission](../classes/DataAccessSubmission.md), [DataAccessRequest](../classes/DataAccessRequest.md) |
| Slot URI | [sagegov:researchProject](https://sagebionetworks.org/governance/researchProject) |

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
| self | sagegov:researchProject |
| native | governanceduo:researchProjectId |




## LinkML Source

<details>
```yaml
name: researchProjectId
description: The research project this submission/request is associated with (DATA_ACCESS_SUBMISSION.RESEARCH_PROJECT_ID
  / RequestInterface.researchProjectId). Range is now `ResearchProject` (was a bare
  integer literal until that class existed -- see plans/governance_graph_open_questions.md
  Section C) -- emitted as an IRI reference to the real `gov:research-project-<n>`
  node. Shared predicate across DataAccessSubmission and DataAccessRequest, both of
  which reference the same real-world ResearchProject.
comments:
- DATA_ACCESS_SUBMISSION.SUBMISSION_SERIALIZED (a BINARY blob, presumably the full
  submission form data) is not modeled as a structured field.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:researchProject
domain_of:
- DataAccessSubmission
- DataAccessRequest
range: ResearchProject

```
</details></div>