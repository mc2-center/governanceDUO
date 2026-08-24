---
search:
  boost: 5.0
---

# Slot: contributionDate 


_The date on which the access requirement was added._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/contributionDate](https://w3id.org/sage-bionetworks/governance-duo/slot/contributionDate)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ContributionMixin](../classes/ContributionMixin.md) | Contribution/authorship tracking |  yes  |
| [AccessRequirement](../classes/AccessRequirement.md) | Representation of a Synapse Access Requirement and its relationships to entit... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [ContributionMixin](../classes/ContributionMixin.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |








## Comments

* schematic Format: date
* prov:generatedAtTime ("The time at which an entity was completely created and is available for use") matches this slot's semantics closely, treating the AccessRequirement record itself as the generated prov:Entity.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:contributionDate |
| native | governanceduo:contributionDate |
| close | prov:generatedAtTime |




## LinkML Source

<details>
```yaml
name: contributionDate
description: The date on which the access requirement was added.
comments:
- 'schematic Format: date'
- prov:generatedAtTime ("The time at which an entity was completely created and is
  available for use") matches this slot's semantics closely, treating the AccessRequirement
  record itself as the generated prov:Entity.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
close_mappings:
- prov:generatedAtTime
rank: 1000
domain_of:
- ContributionMixin
range: string

```
</details></div>