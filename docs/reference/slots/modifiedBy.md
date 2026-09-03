---
search:
  boost: 5.0
---

# Slot: modifiedBy 


_Synapse numeric user id of who last modified this submission's status (`Submission.modifiedBy` in Synapse's live REST API -- moved here from DataAccessSubmissionStatus, which does not carry this field live; see DataAccessSubmissionStatus's own description). Emitted as an IRI reference to a sagegov:Principal node, not a literal, mirroring submittedBy above._



<div data-search-exclude markdown="1">



URI: [sagegov:modifiedBy](https://sagebionetworks.org/governance/modifiedBy)
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
| Slot URI | [sagegov:modifiedBy](https://sagebionetworks.org/governance/modifiedBy) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:modifiedBy |
| native | governanceduo:modifiedBy |
| close | dcterms:contributor |




## LinkML Source

<details>
```yaml
name: modifiedBy
description: Synapse numeric user id of who last modified this submission's status
  (`Submission.modifiedBy` in Synapse's live REST API -- moved here from DataAccessSubmissionStatus,
  which does not carry this field live; see DataAccessSubmissionStatus's own description).
  Emitted as an IRI reference to a sagegov:Principal node, not a literal, mirroring
  submittedBy above.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
close_mappings:
- dcterms:contributor
rank: 1000
slot_uri: sagegov:modifiedBy
domain_of:
- DataAccessSubmission
range: integer

```
</details></div>