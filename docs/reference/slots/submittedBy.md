---
search:
  boost: 5.0
---

# Slot: submittedBy 


_Synapse numeric user id of who submitted this record (`Submission.submittedBy` in Synapse's live REST API). Emitted as an IRI reference to a sagegov:Principal node (looked up by this numeric id), not a literal -- see scripts/build_governance_graph.py._



<div data-search-exclude markdown="1">



URI: [sagegov:submittedBy](https://sagebionetworks.org/governance/submittedBy)
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
| Slot URI | [sagegov:submittedBy](https://sagebionetworks.org/governance/submittedBy) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:submittedBy |
| native | governanceduo:submittedBy |




## LinkML Source

<details>
```yaml
name: submittedBy
description: Synapse numeric user id of who submitted this record (`Submission.submittedBy`
  in Synapse's live REST API). Emitted as an IRI reference to a sagegov:Principal
  node (looked up by this numeric id), not a literal -- see scripts/build_governance_graph.py.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:submittedBy
domain_of:
- DataAccessSubmission
range: integer

```
</details></div>