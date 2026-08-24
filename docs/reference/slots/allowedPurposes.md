---
search:
  boost: 5.0
---

# Slot: allowedPurposes 


_Research purpose term(s) for which use is allowed. Added to close a Policy Fabric gap: genetic-studies-only, health-or-medical-or-biomedical-research, population-origins-or-ancestry-research-only, and research-specific-restrictions all key their Reference Values Schema on a multivalued allowedPurposes list; the existing researchSpecificRestrictions slot is free text and not multivalued, so this is a new, distinct slot rather than a reinterpretation of it (the two can coexist — one is a human-readable narrative, this one is the structured, machine-checkable list Policy Fabric's Rego logic actually reads)._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/allowedPurposes](https://w3id.org/sage-bionetworks/governance-duo/slot/allowedPurposes)
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

* Required when dataUseModifiers contains DUO:0000016, DUO:0000006, DUO:0000011, or DUO:0000012 — see GovernanceMixin rules.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:allowedPurposes |
| native | governanceduo:allowedPurposes |




## LinkML Source

<details>
```yaml
name: allowedPurposes
description: 'Research purpose term(s) for which use is allowed. Added to close a
  Policy Fabric gap: genetic-studies-only, health-or-medical-or-biomedical-research,
  population-origins-or-ancestry-research-only, and research-specific-restrictions
  all key their Reference Values Schema on a multivalued allowedPurposes list; the
  existing researchSpecificRestrictions slot is free text and not multivalued, so
  this is a new, distinct slot rather than a reinterpretation of it (the two can coexist
  — one is a human-readable narrative, this one is the structured, machine-checkable
  list Policy Fabric''s Rego logic actually reads).'
comments:
- Required when dataUseModifiers contains DUO:0000016, DUO:0000006, DUO:0000011, or
  DUO:0000012 — see GovernanceMixin rules.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- GovernanceMixin
range: string
multivalued: true

```
</details></div>