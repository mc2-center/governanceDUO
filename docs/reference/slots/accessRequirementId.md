---
search:
  boost: 5.0
---

# Slot: accessRequirementId 


_The AccessRequirement this submission is an application against (DATA_ACCESS_SUBMISSION.ACCESS_REQUIREMENT_ID)._



<div data-search-exclude markdown="1">



URI: [sagegov:accessRequirement](https://sagebionetworks.org/governance/accessRequirement)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataAccessSubmission](../classes/DataAccessSubmission.md) | A user's application against an AccessRequirement |  no  |
| [ResearchProject](../classes/ResearchProject.md) | Documents the research context/justification behind a DataAccessRequest (and,... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [AccessRequirement](../classes/AccessRequirement.md) |
| Domain Of | [DataAccessSubmission](../classes/DataAccessSubmission.md), [ResearchProject](../classes/ResearchProject.md) |
| Slot URI | [sagegov:accessRequirement](https://sagebionetworks.org/governance/accessRequirement) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |








## Comments

* slot_uri intentionally reuses sagegov:accessRequirement, the same predicate AccessRequirementAssociation.accessRequirement uses, even though this is a differently-named LinkML slot -- so "what AccessRequirement does this concern?" is a uniform gov:accessRequirement query regardless of subject class. See scripts/build_governance_graph.py.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:accessRequirement |
| native | governanceduo:accessRequirementId |
| close | dcterms:requires |




## LinkML Source

<details>
```yaml
name: accessRequirementId
description: The AccessRequirement this submission is an application against (DATA_ACCESS_SUBMISSION.ACCESS_REQUIREMENT_ID).
comments:
- slot_uri intentionally reuses sagegov:accessRequirement, the same predicate AccessRequirementAssociation.accessRequirement
  uses, even though this is a differently-named LinkML slot -- so "what AccessRequirement
  does this concern?" is a uniform gov:accessRequirement query regardless of subject
  class. See scripts/build_governance_graph.py.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
close_mappings:
- dcterms:requires
rank: 1000
slot_uri: sagegov:accessRequirement
domain_of:
- DataAccessSubmission
- ResearchProject
range: AccessRequirement
required: true

```
</details></div>