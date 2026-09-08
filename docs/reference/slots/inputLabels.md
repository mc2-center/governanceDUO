---
search:
  boost: 5.0
---

# Slot: inputLabels 


_The ControlLabels (one per input entity of the Activity above) whose disjoint sourceAccessRequirements triggered this review. Inlined, not referenced by id — ControlLabel has no independent identifier of its own (see that class's own description), so embedding is the only option, not a cross-ABox concern the way Activity/SynapseEntity references are._



<div data-search-exclude markdown="1">



URI: [governanceduo:inputLabels](https://w3id.org/sage-bionetworks/governance-duo/inputLabels)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DerivationReview](../classes/DerivationReview.md) | An auditable record minted whenever a derivation Activity's inputs carry Cont... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [ControlLabel](../classes/ControlLabel.md) |
| Domain Of | [DerivationReview](../classes/DerivationReview.md) |
| Slot URI | [governanceduo:inputLabels](https://w3id.org/sage-bionetworks/governance-duo/inputLabels) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
| Multivalued | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:inputLabels |
| native | governanceduo:inputLabels |




## LinkML Source

<details>
```yaml
name: inputLabels
description: The ControlLabels (one per input entity of the Activity above) whose
  disjoint sourceAccessRequirements triggered this review. Inlined, not referenced
  by id — ControlLabel has no independent identifier of its own (see that class's
  own description), so embedding is the only option, not a cross-ABox concern the
  way Activity/SynapseEntity references are.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: governanceduo:inputLabels
domain_of:
- DerivationReview
range: ControlLabel
required: true
multivalued: true

```
</details></div>