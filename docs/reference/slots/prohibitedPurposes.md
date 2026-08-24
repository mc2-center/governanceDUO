---
search:
  boost: 5.0
---

# Slot: prohibitedPurposes 


_Research purpose term(s) for which use is explicitly disallowed. Added to close a Policy Fabric gap: health-or-medical-or-biomedical-research, no-general-methods-research, non-commercial-use-only, not-for-profit-non-commercial-use-only, and population-origins-or-ancestry-research-prohibited all key their Reference Values Schema on a multivalued prohibitedPurposes list, which no existing slot held._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/prohibitedPurposes](https://w3id.org/sage-bionetworks/governance-duo/slot/prohibitedPurposes)
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

* Required when dataUseModifiers contains DUO:0000006, DUO:0000015, DUO:0000046, DUO:0000018, or DUO:0000044 — see GovernanceMixin rules.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:prohibitedPurposes |
| native | governanceduo:prohibitedPurposes |




## LinkML Source

<details>
```yaml
name: prohibitedPurposes
description: 'Research purpose term(s) for which use is explicitly disallowed. Added
  to close a Policy Fabric gap: health-or-medical-or-biomedical-research, no-general-methods-research,
  non-commercial-use-only, not-for-profit-non-commercial-use-only, and population-origins-or-ancestry-research-prohibited
  all key their Reference Values Schema on a multivalued prohibitedPurposes list,
  which no existing slot held.'
comments:
- Required when dataUseModifiers contains DUO:0000006, DUO:0000015, DUO:0000046, DUO:0000018,
  or DUO:0000044 — see GovernanceMixin rules.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- GovernanceMixin
range: string
multivalued: true

```
</details></div>