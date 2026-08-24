---
search:
  boost: 5.0
---

# Slot: modifiedOn 


_When this status record was last modified (epoch milliseconds)._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/modifiedOn](https://w3id.org/sage-bionetworks/governance-duo/slot/modifiedOn)
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
| self | governanceduo:modifiedOn |
| native | governanceduo:modifiedOn |
| exact | dcterms:modified |




## LinkML Source

<details>
```yaml
name: modifiedOn
description: When this status record was last modified (epoch milliseconds).
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
exact_mappings:
- dcterms:modified
rank: 1000
domain_of:
- DataAccessSubmissionStatus
range: integer

```
</details></div>