---
search:
  boost: 5.0
---

# Slot: submitterId 


_Synapse numeric user id of who performed the actions to gain this approval (AccessApproval.submitterId). Reuses DataAccessSubmission's sagegov:submittedBy predicate -- same real-world concept (who acted on the governance workflow), emitted as an IRI reference to a sagegov:Principal node, not a literal._



<div data-search-exclude markdown="1">



URI: [sagegov:submittedBy](https://sagebionetworks.org/governance/submittedBy)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AccessApproval](../classes/AccessApproval.md) | Records that a Principal has been approved for access under an AccessRequirem... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Integer](../types/Integer.md) |
| Domain Of | [AccessApproval](../classes/AccessApproval.md) |
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
| native | governanceduo:submitterId |




## LinkML Source

<details>
```yaml
name: submitterId
description: Synapse numeric user id of who performed the actions to gain this approval
  (AccessApproval.submitterId). Reuses DataAccessSubmission's sagegov:submittedBy
  predicate -- same real-world concept (who acted on the governance workflow), emitted
  as an IRI reference to a sagegov:Principal node, not a literal.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:submittedBy
domain_of:
- AccessApproval
range: integer

```
</details></div>