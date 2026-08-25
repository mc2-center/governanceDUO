---
search:
  boost: 5.0
---

# Slot: aliases 


_Secondary/external identifiers for this same Synapse entity, carried in DRS's own sanctioned DrsObject.aliases field — e.g. the governanceDUO dotted id(s) that reference this entity via entityIdList/assetBindings[].synapseId (see access_requirement.yaml/mixins.yaml), and/or the corresponding gov:-namespace SynapseEntity individual (see governance_graph.yaml). This is the DRS-forward-compatible resolution of governanceDUO's three-parallel- identifier-scheme gap (entityIdList / assetBindings.synapseId / SynapseEntity.id): rather than inventing a fourth internal crosswalk, Synapse's own id becomes the canonical DRS id and everything else rides in aliases._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/aliases](https://w3id.org/sage-bionetworks/governance-duo/slot/aliases)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DrsObjectMapping](../classes/DrsObjectMapping.md) | How one Synapse entity maps onto a DRS DrsObject's id/self_uri/aliases |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [DrsObjectMapping](../classes/DrsObjectMapping.md) |

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
| self | governanceduo:aliases |
| native | governanceduo:aliases |




## LinkML Source

<details>
```yaml
name: aliases
description: 'Secondary/external identifiers for this same Synapse entity, carried
  in DRS''s own sanctioned DrsObject.aliases field — e.g. the governanceDUO dotted
  id(s) that reference this entity via entityIdList/assetBindings[].synapseId (see
  access_requirement.yaml/mixins.yaml), and/or the corresponding gov:-namespace SynapseEntity
  individual (see governance_graph.yaml). This is the DRS-forward-compatible resolution
  of governanceDUO''s three-parallel- identifier-scheme gap (entityIdList / assetBindings.synapseId
  / SynapseEntity.id): rather than inventing a fourth internal crosswalk, Synapse''s
  own id becomes the canonical DRS id and everything else rides in aliases.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- DrsObjectMapping
range: string
multivalued: true

```
</details></div>