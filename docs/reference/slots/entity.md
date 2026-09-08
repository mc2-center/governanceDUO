---
search:
  boost: 5.0
---

# Slot: entity 


_The SynapseEntity referenced by this Usage, when Used.concreteType is UsedEntity (Used.reference.targetId). range is uriorcurie, not SynapseEntity — same cross-ABox reasoning as Activity.generated above. Absent when this Usage instead carries url/name (a UsedURL)._



<div data-search-exclude markdown="1">



URI: [prov:entity](http://www.w3.org/ns/prov#entity)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Usage](../classes/Usage.md) | Flattens Synapse's real Used interface and its two implementations — UsedEnti... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Uriorcurie](../types/Uriorcurie.md) |
| Domain Of | [Usage](../classes/Usage.md) |
| Slot URI | [prov:entity](http://www.w3.org/ns/prov#entity) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | prov:entity |
| native | governanceduo:entity |




## LinkML Source

<details>
```yaml
name: entity
description: The SynapseEntity referenced by this Usage, when Used.concreteType is
  UsedEntity (Used.reference.targetId). range is uriorcurie, not SynapseEntity — same
  cross-ABox reasoning as Activity.generated above. Absent when this Usage instead
  carries url/name (a UsedURL).
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: prov:entity
domain_of:
- Usage
range: uriorcurie

```
</details></div>