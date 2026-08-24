---
search:
  boost: 5.0
---

# Slot: notAfter 


_ISO-8601 datetime after which use is no longer permitted. Added to close a Policy Fabric gap: time-limit-on-use's Reference Values Schema key notAfter is an absolute datetime, whereas the existing timeLimitOnUse slot holds a number of months — a different shape entirely, so this is a new, distinct slot._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/notAfter](https://w3id.org/sage-bionetworks/governance-duo/slot/notAfter)
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








## Comments

* Required when dataUseModifiers contains DUO:0000025 — see GovernanceMixin rules.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:notAfter |
| native | governanceduo:notAfter |




## LinkML Source

<details>
```yaml
name: notAfter
description: 'ISO-8601 datetime after which use is no longer permitted. Added to close
  a Policy Fabric gap: time-limit-on-use''s Reference Values Schema key notAfter is
  an absolute datetime, whereas the existing timeLimitOnUse slot holds a number of
  months — a different shape entirely, so this is a new, distinct slot.'
comments:
- Required when dataUseModifiers contains DUO:0000025 — see GovernanceMixin rules.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- GovernanceMixin
range: string

```
</details></div>