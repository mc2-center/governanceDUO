---
search:
  boost: 5.0
---

# Slot: modifiedBy 


_Synapse numeric user id of who last modified this status record._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/modifiedBy](https://w3id.org/sage-bionetworks/governance-duo/slot/modifiedBy)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataAccessSubmissionStatus](../classes/DataAccessSubmissionStatus.md) | The approval-workflow state of a DataAccessSubmission |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Integer](../types/Integer.md) |
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
| self | governanceduo:modifiedBy |
| native | governanceduo:modifiedBy |
| close | dcterms:contributor |




## LinkML Source

<details>
```yaml
name: modifiedBy
description: Synapse numeric user id of who last modified this status record.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
close_mappings:
- dcterms:contributor
rank: 1000
domain_of:
- DataAccessSubmissionStatus
range: integer

```
</details></div>