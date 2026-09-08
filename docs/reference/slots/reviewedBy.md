---
search:
  boost: 5.0
---

# Slot: reviewedBy 


_Synapse numeric user id of who recorded reviewStatus, when it is Reviewed/Approved/Denied. range integer, mirroring createdBy/modifiedBy/submittedBy's own raw-id convention rather than a typed Principal reference — see provenance.yaml's own description for why._



<div data-search-exclude markdown="1">



URI: [governanceduo:reviewedBy](https://w3id.org/sage-bionetworks/governance-duo/reviewedBy)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DerivationReview](../classes/DerivationReview.md) | An auditable record minted whenever a derivation Activity's inputs carry Cont... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Integer](../types/Integer.md) |
| Domain Of | [DerivationReview](../classes/DerivationReview.md) |
| Slot URI | [governanceduo:reviewedBy](https://w3id.org/sage-bionetworks/governance-duo/reviewedBy) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:reviewedBy |
| native | governanceduo:reviewedBy |




## LinkML Source

<details>
```yaml
name: reviewedBy
description: Synapse numeric user id of who recorded reviewStatus, when it is Reviewed/Approved/Denied.
  range integer, mirroring createdBy/modifiedBy/submittedBy's own raw-id convention
  rather than a typed Principal reference — see provenance.yaml's own description
  for why.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: governanceduo:reviewedBy
domain_of:
- DerivationReview
range: integer

```
</details></div>