---
search:
  boost: 5.0
---

# Slot: requestPrincipalInvestigatorName 


_Flattened from the live API's nested principalInvestigator.name (org.sagebionetworks.repo.model.dataaccess.PrincipalInvestigator) -- see DataAccessRequest's own class description for why this is flattened rather than given a nested class._



<div data-search-exclude markdown="1">



URI: [sagegov:requestPrincipalInvestigatorName](https://sagebionetworks.org/governance/requestPrincipalInvestigatorName)
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
| Slot URI | [sagegov:requestPrincipalInvestigatorName](https://sagebionetworks.org/governance/requestPrincipalInvestigatorName) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:requestPrincipalInvestigatorName |
| native | governanceduo:requestPrincipalInvestigatorName |




## LinkML Source

<details>
```yaml
name: requestPrincipalInvestigatorName
description: Flattened from the live API's nested principalInvestigator.name (org.sagebionetworks.repo.model.dataaccess.PrincipalInvestigator)
  -- see DataAccessRequest's own class description for why this is flattened rather
  than given a nested class.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:requestPrincipalInvestigatorName
domain_of:
- DataAccessRequest
range: string

```
</details></div>