---
search:
  boost: 5.0
---

# Slot: nonprofitLegalForms 


_Legal entity form(s) qualifying as not-for-profit, coded per ISO 20275:2017 (Entity Legal Form Code List). Added to close a Policy Fabric gap: not-for-profit-organisation-use-only and not-for-profit-non-commercial-use-only both key their Reference Values Schema on a multivalued nonprofitLegalForms list, which no existing slot held._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/nonprofitLegalForms](https://w3id.org/sage-bionetworks/governance-duo/slot/nonprofitLegalForms)
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

* Required when dataUseModifiers contains DUO:0000045 or DUO:0000018 — see GovernanceMixin rules.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:nonprofitLegalForms |
| native | governanceduo:nonprofitLegalForms |




## LinkML Source

<details>
```yaml
name: nonprofitLegalForms
description: 'Legal entity form(s) qualifying as not-for-profit, coded per ISO 20275:2017
  (Entity Legal Form Code List). Added to close a Policy Fabric gap: not-for-profit-organisation-use-only
  and not-for-profit-non-commercial-use-only both key their Reference Values Schema
  on a multivalued nonprofitLegalForms list, which no existing slot held.'
comments:
- Required when dataUseModifiers contains DUO:0000045 or DUO:0000018 — see GovernanceMixin
  rules.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- GovernanceMixin
range: string
multivalued: true

```
</details></div>