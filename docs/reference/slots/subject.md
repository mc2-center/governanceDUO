---
search:
  boost: 5.0
---

# Slot: subject 


_The SynapseEntity this ControlLabel labels. range is uriorcurie, not SynapseEntity — see this schema's own description._



<div data-search-exclude markdown="1">



URI: [governanceduo:subject](https://w3id.org/sage-bionetworks/governance-duo/subject)
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
| Slot URI | [governanceduo:subject](https://w3id.org/sage-bionetworks/governance-duo/subject) |

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
| self | governanceduo:subject |
| native | governanceduo:subject |




## LinkML Source

<details>
```yaml
name: subject
description: The SynapseEntity this ControlLabel labels. range is uriorcurie, not
  SynapseEntity — see this schema's own description.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: governanceduo:subject
domain_of:
- ControlLabel
range: uriorcurie
required: true

```
</details></div>