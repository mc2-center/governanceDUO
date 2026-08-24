---
search:
  boost: 5.0
---

# Slot: approvedUsers 


_Identifier(s) of specifically approved users. Added to close a Policy Fabric gap: user-specific-restriction keys part of its Reference Values Schema on a multivalued approvedUsers list, checked against UserPlatformCredential.userId — the existing userSpecificRestriction slot is free text describing the restriction, not a structured list of identifiers, so this is a new, distinct slot (userSpecificRestriction, allowedAccountTypes, and requiredProfileStatuses together cover the three separate keys this one policy_card's Reference Values Schema defines)._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/approvedUsers](https://w3id.org/sage-bionetworks/governance-duo/slot/approvedUsers)
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








## Comments

* Required when dataUseModifiers contains DUO:0000026 — see GovernanceMixin rules.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:approvedUsers |
| native | governanceduo:approvedUsers |




## LinkML Source

<details>
```yaml
name: approvedUsers
description: 'Identifier(s) of specifically approved users. Added to close a Policy
  Fabric gap: user-specific-restriction keys part of its Reference Values Schema on
  a multivalued approvedUsers list, checked against UserPlatformCredential.userId
  — the existing userSpecificRestriction slot is free text describing the restriction,
  not a structured list of identifiers, so this is a new, distinct slot (userSpecificRestriction,
  allowedAccountTypes, and requiredProfileStatuses together cover the three separate
  keys this one policy_card''s Reference Values Schema defines).'
comments:
- Required when dataUseModifiers contains DUO:0000026 — see GovernanceMixin rules.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- GovernanceMixin
range: string
multivalued: true

```
</details></div>