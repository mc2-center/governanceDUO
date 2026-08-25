---
search:
  boost: 5.0
---

# Slot: assetBindings 


_Policy Fabric Asset-registry DID(s), each paired with the Synapse entity id it registers. Replaces a pair of positionally order-aligned lists (dataUseModifiers-adjacent entityIdList and a since-removed flat assetDids list) with an explicit pairing, so which DID belongs to which Synapse entity is structural rather than convention-only. Each synapseId here should also appear in the containing record's entityIdList (documented, not schema-enforced). GovernanceMixin's own `rules:` are cross-slot too, but only in the simpler "value X on slot A requires slot B to be present" sense; this would need the harder kind -- a positional/arity correspondence between two multivalued lists -- which LinkML's `rules:` preconditions/postconditions don't express, so it's left as a documented, not enforced, invariant._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/assetBindings](https://w3id.org/sage-bionetworks/governance-duo/slot/assetBindings)
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
| Range | [AssetBinding](../classes/AssetBinding.md) |
| Domain Of | [PolicyFabricMixin](../classes/PolicyFabricMixin.md) |

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
| self | governanceduo:assetBindings |
| native | governanceduo:assetBindings |




## LinkML Source

<details>
```yaml
name: assetBindings
description: Policy Fabric Asset-registry DID(s), each paired with the Synapse entity
  id it registers. Replaces a pair of positionally order-aligned lists (dataUseModifiers-adjacent
  entityIdList and a since-removed flat assetDids list) with an explicit pairing,
  so which DID belongs to which Synapse entity is structural rather than convention-only.
  Each synapseId here should also appear in the containing record's entityIdList (documented,
  not schema-enforced). GovernanceMixin's own `rules:` are cross-slot too, but only
  in the simpler "value X on slot A requires slot B to be present" sense; this would
  need the harder kind -- a positional/arity correspondence between two multivalued
  lists -- which LinkML's `rules:` preconditions/postconditions don't express, so
  it's left as a documented, not enforced, invariant.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- PolicyFabricMixin
range: AssetBinding
multivalued: true
inlined: true
inlined_as_list: true

```
</details></div>