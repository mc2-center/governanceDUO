---
search:
  boost: 5.0
---

# Slot: requiredAgreementDocumentId 


_DID of the terms/agreement document the requester must accept before this access requirement's data use modifiers are satisfied. Added to close a Policy Fabric (https://github.com/hasan7n/tmp-policies) gap: its general-research-use, publication-moratorium, return-to-database-or-resource, and time-limit-on-use policy_cards all key their Reference Values Schema on a single requiredDocumentID, which no existing slot held — publicationMoratorium and timeLimitOnUse hold a date/duration, not a document identifier, so this is a new, distinct slot rather than a reinterpretation of either._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/requiredAgreementDocumentId](https://w3id.org/sage-bionetworks/governance-duo/slot/requiredAgreementDocumentId)
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
### Value Constraints

| Property | Value |
| --- | --- |
| Regex Pattern | `^did:[a-z0-9]+:.+$` |










## Comments

* Required when dataUseModifiers contains DUO:0000042, DUO:0000024, DUO:0000029, or DUO:0000025 — see GovernanceMixin rules.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:requiredAgreementDocumentId |
| native | governanceduo:requiredAgreementDocumentId |




## LinkML Source

<details>
```yaml
name: requiredAgreementDocumentId
description: 'DID of the terms/agreement document the requester must accept before
  this access requirement''s data use modifiers are satisfied. Added to close a Policy
  Fabric (https://github.com/hasan7n/tmp-policies) gap: its general-research-use,
  publication-moratorium, return-to-database-or-resource, and time-limit-on-use policy_cards
  all key their Reference Values Schema on a single requiredDocumentID, which no existing
  slot held — publicationMoratorium and timeLimitOnUse hold a date/duration, not a
  document identifier, so this is a new, distinct slot rather than a reinterpretation
  of either.'
comments:
- Required when dataUseModifiers contains DUO:0000042, DUO:0000024, DUO:0000029, or
  DUO:0000025 — see GovernanceMixin rules.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- GovernanceMixin
range: string
pattern: ^did:[a-z0-9]+:.+$

```
</details></div>