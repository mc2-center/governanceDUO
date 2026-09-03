---
search:
  boost: 5.0
---

# Slot: domain 


_Free-text research domain this template applies to, e.g. "genomics"._



<div data-search-exclude markdown="1">



URI: [sagegov:domain](https://sagebionetworks.org/governance/domain)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AccessRequirementTemplate](../classes/AccessRequirementTemplate.md) | A reusable set of DUO-backed Conditions an IRBRequirement can extend |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [AccessRequirementTemplate](../classes/AccessRequirementTemplate.md) |
| Slot URI | [sagegov:domain](https://sagebionetworks.org/governance/domain) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:domain |
| native | governanceduo:domain |




## LinkML Source

<details>
```yaml
name: domain
description: Free-text research domain this template applies to, e.g. "genomics".
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:domain
domain_of:
- AccessRequirementTemplate
range: string

```
</details></div>