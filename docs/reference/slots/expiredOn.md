---
search:
  boost: 5.0
---

# Slot: expiredOn 


_When this approval will expire (epoch milliseconds; AccessApproval.expiredOn in Synapse's live REST API). Maps onto the target ontology's gov:expiresAt -- the real field plans/rebac_governance_graph_alignment.md's first draft was wrong to call an unsourceable gap; see that plan's corrected Grounding section._



<div data-search-exclude markdown="1">



URI: [sagegov:expiresAt](https://sagebionetworks.org/governance/expiresAt)
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
| Slot URI | [sagegov:expiresAt](https://sagebionetworks.org/governance/expiresAt) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:expiresAt |
| native | governanceduo:expiredOn |




## LinkML Source

<details>
```yaml
name: expiredOn
description: When this approval will expire (epoch milliseconds; AccessApproval.expiredOn
  in Synapse's live REST API). Maps onto the target ontology's gov:expiresAt -- the
  real field plans/rebac_governance_graph_alignment.md's first draft was wrong to
  call an unsourceable gap; see that plan's corrected Grounding section.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:expiresAt
domain_of:
- AccessApproval
range: integer

```
</details></div>