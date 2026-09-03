---
search:
  boost: 5.0
---

# Slot: conditionDetail 


_Zero or more companion-slot values from the source AccessRequirement, one per GovernanceMixin.rules entry whose precondition matches this condition's duoCode/conditionType and whose postcondition slot is actually populated on the instance (e.g. the geographicalRestriction value(s) for DUO:0000022). Multivalued because GovernanceMixin.rules is genuinely many-to-many -- some codes have multiple companion slots, some companion slots serve multiple codes -- not because any single condition's own detail is inherently list-valued. See scripts/build_governance_graph.py._



<div data-search-exclude markdown="1">



URI: [sagegov:conditionDetail](https://sagebionetworks.org/governance/conditionDetail)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Condition](../classes/Condition.md) | A single DUO-code-backed condition on an AccessRequirement, surfacing Governa... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [Condition](../classes/Condition.md) |
| Slot URI | [sagegov:conditionDetail](https://sagebionetworks.org/governance/conditionDetail) |

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
| self | sagegov:conditionDetail |
| native | governanceduo:conditionDetail |




## LinkML Source

<details>
```yaml
name: conditionDetail
description: Zero or more companion-slot values from the source AccessRequirement,
  one per GovernanceMixin.rules entry whose precondition matches this condition's
  duoCode/conditionType and whose postcondition slot is actually populated on the
  instance (e.g. the geographicalRestriction value(s) for DUO:0000022). Multivalued
  because GovernanceMixin.rules is genuinely many-to-many -- some codes have multiple
  companion slots, some companion slots serve multiple codes -- not because any single
  condition's own detail is inherently list-valued. See scripts/build_governance_graph.py.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:conditionDetail
domain_of:
- Condition
range: string
multivalued: true

```
</details></div>