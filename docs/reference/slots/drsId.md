---
search:
  boost: 5.0
---

# Slot: drsId 


_The DRS DrsObject.id component. Recommended to be identical to synapseId — see this schema's own header comment for why a fourth internal identifier scheme isn't introduced here._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/drsId](https://w3id.org/sage-bionetworks/governance-duo/slot/drsId)
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
| Required | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:drsId |
| native | governanceduo:drsId |




## LinkML Source

<details>
```yaml
name: drsId
description: The DRS DrsObject.id component. Recommended to be identical to synapseId
  — see this schema's own header comment for why a fourth internal identifier scheme
  isn't introduced here.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- DrsObjectMapping
range: string
required: true

```
</details></div>