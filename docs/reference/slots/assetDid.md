---
search:
  boost: 5.0
---

# Slot: assetDid 


_The Policy Fabric Asset-registry DID for synapseId._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/assetDid](https://w3id.org/sage-bionetworks/governance-duo/slot/assetDid)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AssetBinding](../classes/AssetBinding.md) | One (Synapse entity id -> Policy Fabric Asset DID) pairing |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [AssetBinding](../classes/AssetBinding.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
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
| self | governanceduo:assetDid |
| native | governanceduo:assetDid |




## LinkML Source

<details>
```yaml
name: assetDid
description: The Policy Fabric Asset-registry DID for synapseId.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- AssetBinding
range: string
required: true
pattern: ^did:[a-z0-9]+:.+$

```
</details></div>