---
search:
  boost: 5.0
---

# Slot: sourceField 


_When sourceSlot names an inlined class (e.g. PolicyFabricMixin.assetBindings, range AssetBinding), the sub-field of each element to extract — e.g. sourceSlot: assetBindings, sourceField: assetDid pulls AssetBinding.assetDid out of each entry. Unset when sourceSlot is a flat scalar/list slot._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/sourceField](https://w3id.org/sage-bionetworks/governance-duo/slot/sourceField)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ReferenceValueSource](../classes/ReferenceValueSource.md) | One (referenceValueKey -> governanceDUO slot) mapping |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [ReferenceValueSource](../classes/ReferenceValueSource.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:sourceField |
| native | governanceduo:sourceField |




## LinkML Source

<details>
```yaml
name: sourceField
description: 'When sourceSlot names an inlined class (e.g. PolicyFabricMixin.assetBindings,
  range AssetBinding), the sub-field of each element to extract — e.g. sourceSlot:
  assetBindings, sourceField: assetDid pulls AssetBinding.assetDid out of each entry.
  Unset when sourceSlot is a flat scalar/list slot.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- ReferenceValueSource
range: string

```
</details></div>