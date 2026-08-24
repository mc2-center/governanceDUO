---
search:
  boost: 5.0
---

# Slot: contributorName 


_The name of the person who added this access requirement._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/contributorName](https://w3id.org/sage-bionetworks/governance-duo/slot/contributorName)
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

* prov:wasAttributedTo relates a prov:Entity to a prov:Agent; this slot holds a literal name rather than an Agent reference, so the mapping is close, not exact.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:contributorName |
| native | governanceduo:contributorName |
| close | prov:wasAttributedTo |




## LinkML Source

<details>
```yaml
name: contributorName
description: The name of the person who added this access requirement.
comments:
- prov:wasAttributedTo relates a prov:Entity to a prov:Agent; this slot holds a literal
  name rather than an Agent reference, so the mapping is close, not exact.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
close_mappings:
- prov:wasAttributedTo
rank: 1000
domain_of:
- ContributionMixin
range: string

```
</details></div>