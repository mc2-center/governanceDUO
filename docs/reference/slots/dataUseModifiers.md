---
search:
  boost: 5.0
---

# Slot: dataUseModifiers 


_A list of data use modifiers that apply to the access requirement. Includes real Data Use Ontology (DUO) terms plus Sage-local DUOPlus1-7 extensions (see README) and the literal value "Pending Annotation"._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/dataUseModifiers](https://w3id.org/sage-bionetworks/governance-duo/slot/dataUseModifiers)
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
| Range | [DataUseModifierEnum](../enums/DataUseModifierEnum.md) |
| Domain Of | [GovernanceMixin](../classes/GovernanceMixin.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:dataUseModifiers |
| native | governanceduo:dataUseModifiers |




## LinkML Source

<details>
```yaml
name: dataUseModifiers
description: A list of data use modifiers that apply to the access requirement. Includes
  real Data Use Ontology (DUO) terms plus Sage-local DUOPlus1-7 extensions (see README)
  and the literal value "Pending Annotation".
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- GovernanceMixin
range: DataUseModifierEnum
multivalued: true

```
</details></div>