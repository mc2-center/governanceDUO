---
search:
  boost: 5.0
---

# Slot: sourceSlot 


_The name of the governanceDUO slot (on GovernanceMixin, Study, or the PolicyFabricMixin) that collects the value for the paired referenceValueKey._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/sourceSlot](https://w3id.org/sage-bionetworks/governance-duo/slot/sourceSlot)
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
| Required | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:sourceSlot |
| native | governanceduo:sourceSlot |




## LinkML Source

<details>
```yaml
name: sourceSlot
description: The name of the governanceDUO slot (on GovernanceMixin, Study, or the
  PolicyFabricMixin) that collects the value for the paired referenceValueKey.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- ReferenceValueSource
range: string
required: true

```
</details></div>