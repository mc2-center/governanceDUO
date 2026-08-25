---
search:
  boost: 5.0
---

# Slot: synapseId 


_A Synapse entity id. Reused across contexts that reference one specific Synapse entity: an AssetBinding registering it as a Policy Fabric Asset (this file), or a DrsObjectMapping crosswalking it to a DRS DrsObject (drs_alignment.yaml)._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/synapseId](https://w3id.org/sage-bionetworks/governance-duo/slot/synapseId)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AssetBinding](../classes/AssetBinding.md) | One (Synapse entity id -> Policy Fabric Asset DID) pairing |  no  |
| [DrsObjectMapping](../classes/DrsObjectMapping.md) | How one Synapse entity maps onto a DRS DrsObject's id/self_uri/aliases |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [AssetBinding](../classes/AssetBinding.md), [DrsObjectMapping](../classes/DrsObjectMapping.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
### Value Constraints

| Property | Value |
| --- | --- |
| Regex Pattern | `^syn\d+$` |












## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:synapseId |
| native | governanceduo:synapseId |




## LinkML Source

<details>
```yaml
name: synapseId
description: 'A Synapse entity id. Reused across contexts that reference one specific
  Synapse entity: an AssetBinding registering it as a Policy Fabric Asset (this file),
  or a DrsObjectMapping crosswalking it to a DRS DrsObject (drs_alignment.yaml).'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- AssetBinding
- DrsObjectMapping
range: string
required: true
pattern: ^syn\d+$

```
</details></div>