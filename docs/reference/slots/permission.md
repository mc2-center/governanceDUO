---
search:
  boost: 5.0
---

# Slot: permission 


_The permission(s) granted (ACL_RESOURCE_ACCESS_TYPE.STRING_ELE). Multivalued: a single ACL_RESOURCE_ACCESS row can carry more than one permission type._



<div data-search-exclude markdown="1">



URI: [sagegov:permission](https://sagebionetworks.org/governance/permission)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AccessGrant](../classes/AccessGrant.md) | A first-class ACL grant: resource, principal, permission(s), source, and whet... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [AccessTypeEnum](../enums/AccessTypeEnum.md) |
| Domain Of | [AccessGrant](../classes/AccessGrant.md) |
| Slot URI | [sagegov:permission](https://sagebionetworks.org/governance/permission) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
| Multivalued | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:permission |
| native | governanceduo:permission |




## LinkML Source

<details>
```yaml
name: permission
description: 'The permission(s) granted (ACL_RESOURCE_ACCESS_TYPE.STRING_ELE). Multivalued:
  a single ACL_RESOURCE_ACCESS row can carry more than one permission type.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:permission
domain_of:
- AccessGrant
range: AccessTypeEnum
required: true
multivalued: true

```
</details></div>