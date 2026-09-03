---
search:
  boost: 5.0
---

# Slot: studyId 


_The Study (this repo's real governanceduo:Study class, study.yaml) this IRBRequirement's language was authored for. Bridged via owl:sameAs in build_governance_graph.py, not this slot's own slot_uri -- Study lives in a different namespace already bridged the same way AccessRequirement stubs are (see add_access_requirement_association())._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/studyId](https://w3id.org/sage-bionetworks/governance-duo/slot/studyId)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [IRBRequirement](../classes/IRBRequirement.md) | A site/program-specific instantiation of an AccessRequirementTemplate, per th... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [IRBRequirement](../classes/IRBRequirement.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:studyId |
| native | governanceduo:studyId |




## LinkML Source

<details>
```yaml
name: studyId
description: The Study (this repo's real governanceduo:Study class, study.yaml) this
  IRBRequirement's language was authored for. Bridged via owl:sameAs in build_governance_graph.py,
  not this slot's own slot_uri -- Study lives in a different namespace already bridged
  the same way AccessRequirement stubs are (see add_access_requirement_association()).
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- IRBRequirement
range: string

```
</details></div>