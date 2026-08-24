---
search:
  boost: 2.0
---


# Enum: PrincipalTypeEnum 




_Whether a Principal is an individual user or a team — from the design doc: "Principals may represent either individual users or teams." ACL_RESOURCE_ACCESS.GROUP_ID itself doesn't distinguish the two; Synapse resolves that from the id's own type at runtime, so this is recorded explicitly here rather than inferred._



<div data-search-exclude markdown="1">

URI: [governanceduo:enum/PrincipalTypeEnum](https://w3id.org/sage-bionetworks/governance-duo/enum/PrincipalTypeEnum)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| User | None |  |
| Team | None |  |




## Slots

| Name | Description |
| ---  | --- |
| [principalType](../slots/principalType.md) |  |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo






## LinkML Source

<details>
```yaml
name: PrincipalTypeEnum
description: 'Whether a Principal is an individual user or a team — from the design
  doc: "Principals may represent either individual users or teams." ACL_RESOURCE_ACCESS.GROUP_ID
  itself doesn''t distinguish the two; Synapse resolves that from the id''s own type
  at runtime, so this is recorded explicitly here rather than inferred.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
permissible_values:
  User:
    text: User
  Team:
    text: Team

```
</details>

</div>