---
search:
  boost: 5.0
---

# Slot: url 


_The external URL used, when Used.concreteType is UsedURL (UsedURL.url — "The external URL of the file that was used"). Absent when this Usage instead carries entity/entityVersionNumber (a UsedEntity). Usage.name (UsedURL.name — the same field description, verbatim, despite the field being named `name`) reuses the shared display-name slot (mixins.yaml) directly rather than being redefined here._



<div data-search-exclude markdown="1">



URI: [sagegov:url](https://sagebionetworks.org/governance/url)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Usage](../classes/Usage.md) | Flattens Synapse's real Used interface and its two implementations — UsedEnti... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [Usage](../classes/Usage.md) |
| Slot URI | [sagegov:url](https://sagebionetworks.org/governance/url) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:url |
| native | governanceduo:url |




## LinkML Source

<details>
```yaml
name: url
description: The external URL used, when Used.concreteType is UsedURL (UsedURL.url
  — "The external URL of the file that was used"). Absent when this Usage instead
  carries entity/entityVersionNumber (a UsedEntity). Usage.name (UsedURL.name — the
  same field description, verbatim, despite the field being named `name`) reuses the
  shared display-name slot (mixins.yaml) directly rather than being redefined here.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:url
domain_of:
- Usage
range: string

```
</details></div>