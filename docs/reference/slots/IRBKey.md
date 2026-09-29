---
search:
  boost: 5.0
---

# Slot: IRBKey 


_The IRB record id(s) associated with this object. Provide multiple values as a comma-separated list._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/IRBKey](https://w3id.org/sage-bionetworks/governance-duo/slot/IRBKey)
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
| Regex Pattern | `^irb\.[A-Za-z0-9_-]+$` |












## Identifier and Mapping Information



### Annotations

| property | value |
| --- | --- |
| foreign_key | True |




### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:IRBKey |
| native | governanceduo:IRBKey |




## LinkML Source

<details>
```yaml
name: IRBKey
annotations:
  foreign_key:
    tag: foreign_key
    value: true
description: The IRB record id(s) associated with this object. Provide multiple values
  as a comma-separated list.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- GovernanceMixin
range: string
multivalued: true
pattern: ^irb\.[A-Za-z0-9_-]+$

```
</details></div>