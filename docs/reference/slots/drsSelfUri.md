---
search:
  boost: 5.0
---

# Slot: drsSelfUri 


_The DRS DrsObject.self_uri — a hostname-based `drs://<hostname>/<drsId>` URI (DRS's other addressing style, compact-identifier URIs resolved via identifiers.org/n2t.net, is not used here since Synapse ids already resolve directly against a Synapse-operated DRS host)._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/drsSelfUri](https://w3id.org/sage-bionetworks/governance-duo/slot/drsSelfUri)
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
### Value Constraints

| Property | Value |
| --- | --- |
| Regex Pattern | `^drs://.+$` |












## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:drsSelfUri |
| native | governanceduo:drsSelfUri |




## LinkML Source

<details>
```yaml
name: drsSelfUri
description: The DRS DrsObject.self_uri — a hostname-based `drs://<hostname>/<drsId>`
  URI (DRS's other addressing style, compact-identifier URIs resolved via identifiers.org/n2t.net,
  is not used here since Synapse ids already resolve directly against a Synapse-operated
  DRS host).
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- DrsObjectMapping
range: string
required: true
pattern: ^drs://.+$

```
</details></div>