---
search:
  boost: 5.0
---

# Slot: computedFrom 


_The Activity this label was (re)computed from. range is uriorcurie, not Activity — see this schema's own description. Also the staleness signal Section 7 of plans/prov_o_integration.md relies on: if an AR named in sourceAccessRequirements is later revoked, any label computed before that point is provably stale._



<div data-search-exclude markdown="1">



URI: [governanceduo:computedFrom](https://w3id.org/sage-bionetworks/governance-duo/computedFrom)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ControlLabel](../classes/ControlLabel.md) | A precomputed, per-SynapseEntity sensitivity label — the max DataTierEnum ran... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Uriorcurie](../types/Uriorcurie.md) |
| Domain Of | [ControlLabel](../classes/ControlLabel.md) |
| Slot URI | [governanceduo:computedFrom](https://w3id.org/sage-bionetworks/governance-duo/computedFrom) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:computedFrom |
| native | governanceduo:computedFrom |




## LinkML Source

<details>
```yaml
name: computedFrom
description: 'The Activity this label was (re)computed from. range is uriorcurie,
  not Activity — see this schema''s own description. Also the staleness signal Section
  7 of plans/prov_o_integration.md relies on: if an AR named in sourceAccessRequirements
  is later revoked, any label computed before that point is provably stale.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: governanceduo:computedFrom
domain_of:
- ControlLabel
range: uriorcurie

```
</details></div>