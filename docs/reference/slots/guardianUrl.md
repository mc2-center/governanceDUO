---
search:
  boost: 5.0
---

# Slot: guardianUrl 


_The deployed Guardian service URL for this asset. Mirrors Asset.metadata.guardian_url, set by the same asset-setup convention._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/guardianUrl](https://w3id.org/sage-bionetworks/governance-duo/slot/guardianUrl)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PolicyFabricMixin](../classes/PolicyFabricMixin.md) | Fields needed to deploy an AccessRequirement's governed entities into Policy ... |  no  |
| [AccessRequirement](../classes/AccessRequirement.md) | Representation of a Synapse Access Requirement and its relationships to entit... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [PolicyFabricMixin](../classes/PolicyFabricMixin.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:guardianUrl |
| native | governanceduo:guardianUrl |




## LinkML Source

<details>
```yaml
name: guardianUrl
description: The deployed Guardian service URL for this asset. Mirrors Asset.metadata.guardian_url,
  set by the same asset-setup convention.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- PolicyFabricMixin
range: string

```
</details></div>