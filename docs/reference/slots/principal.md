---
search:
  boost: 5.0
---

# Slot: principal 


_The user or team this grant applies to._



<div data-search-exclude markdown="1">



URI: [sagegov:principal](https://sagebionetworks.org/governance/principal)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AccessGrant](../classes/AccessGrant.md) | A first-class ACL grant: resource, principal, permission(s), source, and whet... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Principal](../classes/Principal.md) |
| Domain Of | [AccessGrant](../classes/AccessGrant.md) |
| Slot URI | [sagegov:principal](https://sagebionetworks.org/governance/principal) |

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
| self | sagegov:principal |
| native | governanceduo:principal |
| close | prov:agent |




## LinkML Source

<details>
```yaml
name: principal
description: The user or team this grant applies to.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
close_mappings:
- prov:agent
rank: 1000
slot_uri: sagegov:principal
domain_of:
- AccessGrant
range: Principal
required: true

```
</details></div>