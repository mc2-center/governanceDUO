---
search:
  boost: 5.0
---

# Slot: notes 


_Free-text notes — used in particular to record why sourceSlot is left unset (which governanceDUO slot would need to be added, and its required shape) so a gap is documented rather than silently dropped._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/notes](https://w3id.org/sage-bionetworks/governance-duo/slot/notes)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PolicyCardBinding](../classes/PolicyCardBinding.md) | One row per verified tmp-policies policy_cards/<name>/ folder: which DUO code... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [PolicyCardBinding](../classes/PolicyCardBinding.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:notes |
| native | governanceduo:notes |




## LinkML Source

<details>
```yaml
name: notes
description: Free-text notes — used in particular to record why sourceSlot is left
  unset (which governanceDUO slot would need to be added, and its required shape)
  so a gap is documented rather than silently dropped.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- PolicyCardBinding
range: string
multivalued: true

```
</details></div>