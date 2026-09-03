---
search:
  boost: 5.0
---

# Slot: company 


_Institution/company name, verbatim from Synapse's real UserProfile.company field ("This person's current affiliation"). Consumed by build_governance_graph.py's site_node_for() to derive a gov:affiliatedWith edge to a gov:Site node -- not independently re-emitted as its own literal predicate on the Principal subject. Only meaningful for `principalType: User`._



<div data-search-exclude markdown="1">



URI: [sagegov:company](https://sagebionetworks.org/governance/company)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Principal](../classes/Principal.md) | A Synapse user or team being granted access via an ACL |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [Principal](../classes/Principal.md) |
| Slot URI | [sagegov:company](https://sagebionetworks.org/governance/company) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:company |
| native | governanceduo:company |




## LinkML Source

<details>
```yaml
name: company
description: 'Institution/company name, verbatim from Synapse''s real UserProfile.company
  field ("This person''s current affiliation"). Consumed by build_governance_graph.py''s
  site_node_for() to derive a gov:affiliatedWith edge to a gov:Site node -- not independently
  re-emitted as its own literal predicate on the Principal subject. Only meaningful
  for `principalType: User`.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:company
domain_of:
- Principal
range: string

```
</details></div>