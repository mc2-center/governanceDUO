---
search:
  boost: 5.0
---

# Slot: approvedProjects 


_DID(s) of project(s) approved to use the data under this access requirement. Added to close a Policy Fabric gap: project-specific-restriction keys its Reference Values Schema on a multivalued approvedProjects list of DIDs, which no existing slot held._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/approvedProjects](https://w3id.org/sage-bionetworks/governance-duo/slot/approvedProjects)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [GovernanceMixin](../classes/GovernanceMixin.md) | DUO-based data-use-modifier vocabulary and its conditional-requirement rules,... |  no  |
| [AccessRequirement](../classes/AccessRequirement.md) | Representation of a Synapse Access Requirement and its relationships to entit... |  no  |
| [Resource](../classes/Resource.md) | Information that is relevant to resource access conditions |  no  |
| [Study](../classes/Study.md) | Studies associated with a grant |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [GovernanceMixin](../classes/GovernanceMixin.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |
### Value Constraints

| Property | Value |
| --- | --- |
| Regex Pattern | `^did:[a-z0-9]+:.+$` |










## Comments

* Required when dataUseModifiers contains DUO:0000027 — see GovernanceMixin rules.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:approvedProjects |
| native | governanceduo:approvedProjects |




## LinkML Source

<details>
```yaml
name: approvedProjects
description: 'DID(s) of project(s) approved to use the data under this access requirement.
  Added to close a Policy Fabric gap: project-specific-restriction keys its Reference
  Values Schema on a multivalued approvedProjects list of DIDs, which no existing
  slot held.'
comments:
- Required when dataUseModifiers contains DUO:0000027 — see GovernanceMixin rules.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- GovernanceMixin
range: string
multivalued: true
pattern: ^did:[a-z0-9]+:.+$

```
</details></div>