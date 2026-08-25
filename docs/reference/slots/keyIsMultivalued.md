---
search:
  boost: 5.0
---

# Slot: keyIsMultivalued 


_True if this referenceValueKey's own policy_data_schema.json documents it as a list (e.g. "list of strings"); False if it's a single scalar value (e.g. requiredDocumentID, notAfter, datasetID — each documented as "DID of ..."/an ISO-8601 datetime, not a list). This is a property of the Policy Fabric key itself, independent of whether its governanceDUO sourceSlot happens to be multivalued — e.g. datasetID is scalar even though it is sourced from the multivalued assetBindings slot (build_policy_fabric.py takes assetBindings[0].assetDid)._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/keyIsMultivalued](https://w3id.org/sage-bionetworks/governance-duo/slot/keyIsMultivalued)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ReferenceValueSource](../classes/ReferenceValueSource.md) | One (referenceValueKey -> governanceDUO slot) mapping |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Boolean](../types/Boolean.md) |
| Domain Of | [ReferenceValueSource](../classes/ReferenceValueSource.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
### Slot Characteristics

| Property | Value |
| --- | --- |
| If Absent | `true` |












## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:keyIsMultivalued |
| native | governanceduo:keyIsMultivalued |




## LinkML Source

<details>
```yaml
name: keyIsMultivalued
description: True if this referenceValueKey's own policy_data_schema.json documents
  it as a list (e.g. "list of strings"); False if it's a single scalar value (e.g.
  requiredDocumentID, notAfter, datasetID — each documented as "DID of ..."/an ISO-8601
  datetime, not a list). This is a property of the Policy Fabric key itself, independent
  of whether its governanceDUO sourceSlot happens to be multivalued — e.g. datasetID
  is scalar even though it is sourced from the multivalued assetBindings slot (build_policy_fabric.py
  takes assetBindings[0].assetDid).
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
ifabsent: 'true'
domain_of:
- ReferenceValueSource
range: boolean
required: true

```
</details></div>