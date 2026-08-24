---
search:
  boost: 5.0
---

# Slot: guardianDataSource 


_The data path/source configured for this asset's Guardian. Mirrors Asset.metadata.data_source, set by convention (not schema) in tmp-policies/tools/pdo_client at asset-setup time._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/guardianDataSource](https://w3id.org/sage-bionetworks/governance-duo/slot/guardianDataSource)
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
| self | governanceduo:guardianDataSource |
| native | governanceduo:guardianDataSource |




## LinkML Source

<details>
```yaml
name: guardianDataSource
description: The data path/source configured for this asset's Guardian. Mirrors Asset.metadata.data_source,
  set by convention (not schema) in tmp-policies/tools/pdo_client at asset-setup time.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- PolicyFabricMixin
range: string

```
</details></div>