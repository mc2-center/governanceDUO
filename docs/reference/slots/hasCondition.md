---
search:
  boost: 5.0
---

# Slot: hasCondition 


_The DUO-backed Conditions this template reuses -- the same gov:Condition class add_access_requirement() already mints from real dataUseModifiers data (see plans/rebac_governance_graph_alignment.md), attached here to an AccessRequirementTemplate instead of (or in addition to) an AccessRequirement stub._



<div data-search-exclude markdown="1">



URI: [sagegov:hasCondition](https://sagebionetworks.org/governance/hasCondition)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AccessRequirementTemplate](../classes/AccessRequirementTemplate.md) | A reusable set of DUO-backed Conditions an IRBRequirement can extend |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Condition](../classes/Condition.md) |
| Domain Of | [AccessRequirementTemplate](../classes/AccessRequirementTemplate.md) |
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
description: The DUO-backed Conditions this template reuses -- the same gov:Condition
  class add_access_requirement() already mints from real dataUseModifiers data (see
  plans/rebac_governance_graph_alignment.md), attached here to an AccessRequirementTemplate
  instead of (or in addition to) an AccessRequirement stub.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:hasCondition
domain_of:
- AccessRequirementTemplate
range: Condition
multivalued: true

```
</details></div>