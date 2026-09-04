---
search:
  boost: 5.0
---

# Slot: hasCondition 


_The DUO-backed Conditions this attaches to -- gov:Condition individuals add_access_requirement() mints from real dataUseModifiers data (see plans/rebac_governance_graph_alignment.md). Shared by AccessRequirementReference (the AR stub these Conditions are minted onto in the first place) and AccessRequirementTemplate (which reuses the same real Condition nodes)._



<div data-search-exclude markdown="1">



URI: [sagegov:hasCondition](https://sagebionetworks.org/governance/hasCondition)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AccessRequirementReference](../classes/AccessRequirementReference.md) | The gov:AR-<n> stub build_governance_graph |  no  |
| [AccessRequirementTemplate](../classes/AccessRequirementTemplate.md) | A reusable set of DUO-backed Conditions an IRBRequirement can extend |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Condition](../classes/Condition.md) |
| Domain Of | [AccessRequirementReference](../classes/AccessRequirementReference.md), [AccessRequirementTemplate](../classes/AccessRequirementTemplate.md) |
| Slot URI | [sagegov:hasCondition](https://sagebionetworks.org/governance/hasCondition) |

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
| self | sagegov:hasCondition |
| native | governanceduo:hasCondition |




## LinkML Source

<details>
```yaml
name: hasCondition
description: The DUO-backed Conditions this attaches to -- gov:Condition individuals
  add_access_requirement() mints from real dataUseModifiers data (see plans/rebac_governance_graph_alignment.md).
  Shared by AccessRequirementReference (the AR stub these Conditions are minted onto
  in the first place) and AccessRequirementTemplate (which reuses the same real Condition
  nodes).
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:hasCondition
domain_of:
- AccessRequirementReference
- AccessRequirementTemplate
range: Condition
multivalued: true

```
</details></div>