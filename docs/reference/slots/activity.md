---
search:
  boost: 5.0
---

# Slot: activity 


_The derivation Activity being reviewed. range is uriorcurie, not Activity — see this schema's own description. The value is an IRI node, typed owl:ObjectProperty in the OWL._



<div data-search-exclude markdown="1">



URI: [sagegov:activity](https://sagebionetworks.org/governance/activity)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DerivationReview](../classes/DerivationReview.md) | An auditable record minted whenever a derivation Activity's inputs carry Cont... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Uriorcurie](../types/Uriorcurie.md) |
| Domain Of | [DerivationReview](../classes/DerivationReview.md) |
| Slot URI | [sagegov:activity](https://sagebionetworks.org/governance/activity) |

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
| self | sagegov:activity |
| native | governanceduo:activity |




## LinkML Source

<details>
```yaml
name: activity
description: The derivation Activity being reviewed. range is uriorcurie, not Activity
  — see this schema's own description. The value is an IRI node, typed owl:ObjectProperty
  in the OWL.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:activity
domain_of:
- DerivationReview
range: uriorcurie
required: true

```
</details></div>