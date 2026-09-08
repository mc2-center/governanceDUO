---
search:
  boost: 5.0
---

# Slot: sourceAccessRequirements 


_Every AccessRequirement contributing to this label's dataTier, across the subject's full derivation ancestry — what lets a later composite-risk check tell whether two ControlLabels trace back to the same AR or to genuinely different ones (the note's paragraph-12 case). range is uriorcurie, not AccessRequirementReference — see this schema's own description._



<div data-search-exclude markdown="1">



URI: [governanceduo:sourceAccessRequirements](https://w3id.org/sage-bionetworks/governance-duo/sourceAccessRequirements)
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
| Slot URI | [governanceduo:sourceAccessRequirements](https://w3id.org/sage-bionetworks/governance-duo/sourceAccessRequirements) |

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
| self | governanceduo:sourceAccessRequirements |
| native | governanceduo:sourceAccessRequirements |




## LinkML Source

<details>
```yaml
name: sourceAccessRequirements
description: Every AccessRequirement contributing to this label's dataTier, across
  the subject's full derivation ancestry — what lets a later composite-risk check
  tell whether two ControlLabels trace back to the same AR or to genuinely different
  ones (the note's paragraph-12 case). range is uriorcurie, not AccessRequirementReference
  — see this schema's own description.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: governanceduo:sourceAccessRequirements
domain_of:
- ControlLabel
range: uriorcurie
multivalued: true

```
</details></div>