---
search:
  boost: 5.0
---

# Slot: entityVersionNumber 


_Mirrors UsedEntity.reference.targetVersionNumber. No PROV-O equivalent: PROV-O does not version-scope entities the way Synapse does._



<div data-search-exclude markdown="1">



URI: [sagegov:entityVersionNumber](https://sagebionetworks.org/governance/entityVersionNumber)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Usage](../classes/Usage.md) | Flattens Synapse's real Used interface and its two implementations — UsedEnti... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Integer](../types/Integer.md) |
| Domain Of | [Usage](../classes/Usage.md) |
| Slot URI | [sagegov:entityVersionNumber](https://sagebionetworks.org/governance/entityVersionNumber) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:entityVersionNumber |
| native | governanceduo:entityVersionNumber |




## LinkML Source

<details>
```yaml
name: entityVersionNumber
description: 'Mirrors UsedEntity.reference.targetVersionNumber. No PROV-O equivalent:
  PROV-O does not version-scope entities the way Synapse does.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:entityVersionNumber
domain_of:
- Usage
range: integer

```
</details></div>