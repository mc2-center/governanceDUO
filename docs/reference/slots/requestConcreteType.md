---
search:
  boost: 5.0
---

# Slot: requestConcreteType 


_Which kind of request this is -- literally "Request" or "Renewal" (RequestInterface.concreteType in Synapse's live REST API). Deliberately not named/typed the same as AccessRequirement's own concreteType slot (mixins.yaml, range AccessRequirementConcreteTypeEnum) -- these are two unrelated real Synapse concreteType fields on two different objects._



<div data-search-exclude markdown="1">



URI: [sagegov:requestConcreteType](https://sagebionetworks.org/governance/requestConcreteType)
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
| Slot URI | [sagegov:requestConcreteType](https://sagebionetworks.org/governance/requestConcreteType) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:requestConcreteType |
| native | governanceduo:requestConcreteType |




## LinkML Source

<details>
```yaml
name: requestConcreteType
description: Which kind of request this is -- literally "Request" or "Renewal" (RequestInterface.concreteType
  in Synapse's live REST API). Deliberately not named/typed the same as AccessRequirement's
  own concreteType slot (mixins.yaml, range AccessRequirementConcreteTypeEnum) --
  these are two unrelated real Synapse concreteType fields on two different objects.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:requestConcreteType
domain_of:
- DataAccessRequest
range: string

```
</details></div>