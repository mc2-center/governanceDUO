---
search:
  boost: 5.0
---

# Slot: qualifiedUsage 


_The Usage records (mirroring Activity.used) describing what this Activity consumed, and whether each was executed rather than merely used as input data._



<div data-search-exclude markdown="1">



URI: [prov:qualifiedUsage](http://www.w3.org/ns/prov#qualifiedUsage)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Activity](../classes/Activity.md) | Mirrors Synapse's real Activity object (org |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Usage](../classes/Usage.md) |
| Domain Of | [Activity](../classes/Activity.md) |
| Slot URI | [prov:qualifiedUsage](http://www.w3.org/ns/prov#qualifiedUsage) |

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
| self | prov:qualifiedUsage |
| native | governanceduo:qualifiedUsage |




## LinkML Source

<details>
```yaml
name: qualifiedUsage
description: The Usage records (mirroring Activity.used) describing what this Activity
  consumed, and whether each was executed rather than merely used as input data.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: prov:qualifiedUsage
domain_of:
- Activity
range: Usage
multivalued: true

```
</details></div>