---
search:
  boost: 5.0
---

# Slot: publication 


_Link(s) to publications that used the controlled data (Renewal.publication in Synapse's live REST API). Only present on renewal instances (requestConcreteType == "Renewal")._



<div data-search-exclude markdown="1">



URI: [sagegov:publication](https://sagebionetworks.org/governance/publication)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataAccessRequest](../classes/DataAccessRequest.md) | A user's draft/submitted request against an AccessRequirement, behind a DataA... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [DataAccessRequest](../classes/DataAccessRequest.md) |
| Slot URI | [sagegov:publication](https://sagebionetworks.org/governance/publication) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:publication |
| native | governanceduo:publication |




## LinkML Source

<details>
```yaml
name: publication
description: Link(s) to publications that used the controlled data (Renewal.publication
  in Synapse's live REST API). Only present on renewal instances (requestConcreteType
  == "Renewal").
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:publication
domain_of:
- DataAccessRequest
range: string

```
</details></div>