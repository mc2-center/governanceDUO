---
search:
  boost: 5.0
---

# Slot: modifiedOn 


_When this record was last modified (epoch milliseconds). On DataAccessSubmissionStatus this is emitted under the distinct gov:statusModifiedOn predicate instead (a bare constant in build_governance_graph.py, not resolved via this slot_uri -- see that class's own description); DataAccessRequest resolves it via this slot's own sagegov:modifiedOn directly._



<div data-search-exclude markdown="1">



URI: [sagegov:modifiedOn](https://sagebionetworks.org/governance/modifiedOn)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataAccessSubmissionStatus](../classes/DataAccessSubmissionStatus.md) | The approval-workflow state of a DataAccessSubmission |  no  |
| [DataAccessRequest](../classes/DataAccessRequest.md) | A user's draft/submitted request against an AccessRequirement, behind a DataA... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Integer](../types/Integer.md) |
| Domain Of | [DataAccessSubmissionStatus](../classes/DataAccessSubmissionStatus.md), [DataAccessRequest](../classes/DataAccessRequest.md) |
| Slot URI | [sagegov:modifiedOn](https://sagebionetworks.org/governance/modifiedOn) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:modifiedOn |
| native | governanceduo:modifiedOn |
| exact | dcterms:modified |




## LinkML Source

<details>
```yaml
name: modifiedOn
description: When this record was last modified (epoch milliseconds). On DataAccessSubmissionStatus
  this is emitted under the distinct gov:statusModifiedOn predicate instead (a bare
  constant in build_governance_graph.py, not resolved via this slot_uri -- see that
  class's own description); DataAccessRequest resolves it via this slot's own sagegov:modifiedOn
  directly.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
exact_mappings:
- dcterms:modified
rank: 1000
slot_uri: sagegov:modifiedOn
domain_of:
- DataAccessSubmissionStatus
- DataAccessRequest
range: integer

```
</details></div>