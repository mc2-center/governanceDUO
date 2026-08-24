---
search:
  boost: 5.0
---

# Slot: assetDids 


_Policy Fabric Asset-registry DID(s) for the Synapse entities in entityIdList (order-aligned — position N here corresponds to position N in entityIdList). Mirrors the Django Asset model's `did` field (unique per Asset) in tmp-policies/tools/asset_registry._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/assetDids](https://w3id.org/sage-bionetworks/governance-duo/slot/assetDids)
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
| Multivalued | Yes |
### Value Constraints

| Property | Value |
| --- | --- |
| Regex Pattern | `^did:[a-z0-9]+:.+$` |












## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:assetDids |
| native | governanceduo:assetDids |




## LinkML Source

<details>
```yaml
name: assetDids
description: Policy Fabric Asset-registry DID(s) for the Synapse entities in entityIdList
  (order-aligned — position N here corresponds to position N in entityIdList). Mirrors
  the Django Asset model's `did` field (unique per Asset) in tmp-policies/tools/asset_registry.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- PolicyFabricMixin
range: string
multivalued: true
pattern: ^did:[a-z0-9]+:.+$

```
</details></div>