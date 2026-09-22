---
search:
  boost: 5.0
---

# Slot: duoCode 


_The IRI of the data-use code this condition represents, from DataUseModifierEnum's meaning: obo:DUO_<n> for real DUO codes (the same IRIs sagebrain-model imports), sagegov:DUOPlus<n> for the Sage-local extensions. Emitted as an IRI, never a string, by scripts/build_governance_graph.py. Not required: "Pending Annotation" has no meaning and gets no duoCode._



<div data-search-exclude markdown="1">



URI: [sagegov:duoCode](https://sagebionetworks.org/governance/duoCode)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Condition](../classes/Condition.md) | A single DUO-code-backed condition on an AccessRequirement, surfacing Governa... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [DataUseModifierEnum](../enums/DataUseModifierEnum.md) |
| Domain Of | [Condition](../classes/Condition.md) |
| Slot URI | [sagegov:duoCode](https://sagebionetworks.org/governance/duoCode) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:duoCode |
| native | governanceduo:duoCode |




## LinkML Source

<details>
```yaml
name: duoCode
description: 'The IRI of the data-use code this condition represents, from DataUseModifierEnum''s
  meaning: obo:DUO_<n> for real DUO codes (the same IRIs sagebrain-model imports),
  sagegov:DUOPlus<n> for the Sage-local extensions. Emitted as an IRI, never a string,
  by scripts/build_governance_graph.py. Not required: "Pending Annotation" has no
  meaning and gets no duoCode.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:duoCode
domain_of:
- Condition
range: DataUseModifierEnum

```
</details></div>