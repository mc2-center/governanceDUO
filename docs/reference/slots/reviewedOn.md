---
search:
  boost: 5.0
---

# Slot: reviewedOn 


_When reviewStatus was last recorded (epoch milliseconds)._



<div data-search-exclude markdown="1">



URI: [governanceduo:reviewedOn](https://w3id.org/sage-bionetworks/governance-duo/reviewedOn)
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
| Slot URI | [governanceduo:reviewedOn](https://w3id.org/sage-bionetworks/governance-duo/reviewedOn) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:reviewedOn |
| native | governanceduo:reviewedOn |




## LinkML Source

<details>
```yaml
name: reviewedOn
description: When reviewStatus was last recorded (epoch milliseconds).
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: governanceduo:reviewedOn
domain_of:
- DerivationReview
range: integer

```
</details></div>