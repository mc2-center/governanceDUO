---
search:
  boost: 5.0
---

# Slot: wasExecuted 


_Mirrors Used.wasExecuted verbatim ("The enclosed entity was used and also executed in the Activity") — a Synapse-specific boolean flag distinguishing code/workflow inputs from data inputs within one qualifiedUsage list, with no exact PROV-O predicate equivalent found; left as a repo-local predicate rather than forced onto e.g. prov:hadRole, same as other slots this repo leaves unmapped when no confident match exists (see README's OLS-verification table)._



<div data-search-exclude markdown="1">



URI: [sagegov:wasExecuted](https://sagebionetworks.org/governance/wasExecuted)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Usage](../classes/Usage.md) | Flattens Synapse's real Used interface and its two implementations — UsedEnti... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Boolean](../types/Boolean.md) |
| Domain Of | [Usage](../classes/Usage.md) |
| Slot URI | [sagegov:wasExecuted](https://sagebionetworks.org/governance/wasExecuted) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:wasExecuted |
| native | governanceduo:wasExecuted |




## LinkML Source

<details>
```yaml
name: wasExecuted
description: Mirrors Used.wasExecuted verbatim ("The enclosed entity was used and
  also executed in the Activity") — a Synapse-specific boolean flag distinguishing
  code/workflow inputs from data inputs within one qualifiedUsage list, with no exact
  PROV-O predicate equivalent found; left as a repo-local predicate rather than forced
  onto e.g. prov:hadRole, same as other slots this repo leaves unmapped when no confident
  match exists (see README's OLS-verification table).
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:wasExecuted
domain_of:
- Usage
range: boolean
required: true

```
</details></div>