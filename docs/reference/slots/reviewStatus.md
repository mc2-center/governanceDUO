---
search:
  boost: 5.0
---

# Slot: reviewStatus 


_This review's workflow state. Deliberately not named `status`: that slot name is already bound to ApprovalStateEnum on AccessApproval in governance_graph.yaml — a distinct, unrelated enum; do not conflate._



<div data-search-exclude markdown="1">



URI: [governanceduo:reviewStatus](https://w3id.org/sage-bionetworks/governance-duo/reviewStatus)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DerivationReview](../classes/DerivationReview.md) | An auditable record minted whenever a derivation Activity's inputs carry Cont... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [DerivationReviewStatusEnum](../enums/DerivationReviewStatusEnum.md) |
| Domain Of | [DerivationReview](../classes/DerivationReview.md) |
| Slot URI | [governanceduo:reviewStatus](https://w3id.org/sage-bionetworks/governance-duo/reviewStatus) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:reviewStatus |
| native | governanceduo:reviewStatus |




## LinkML Source

<details>
```yaml
name: reviewStatus
description: 'This review''s workflow state. Deliberately not named `status`: that
  slot name is already bound to ApprovalStateEnum on AccessApproval in governance_graph.yaml
  — a distinct, unrelated enum; do not conflate.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: governanceduo:reviewStatus
domain_of:
- DerivationReview
range: DerivationReviewStatusEnum
required: true

```
</details></div>