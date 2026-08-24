---
search:
  boost: 2.0
---


# Enum: DataPermissionEnum 



<div data-search-exclude markdown="1">

URI: [governanceduo:enum/DataPermissionEnum](https://w3id.org/sage-bionetworks/governance-duo/enum/DataPermissionEnum)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| Agreement | None | Data use conditions are derived from a Data Use Agreement |
| Attestation | None | Data use conditions are derived from an Attestation |
| Award | None | Data use conditions are derived from an Award |
| Other | None | Other permissions may apply to the data access |




## Slots

| Name | Description |
| ---  | --- |
| [dataPermission](../slots/dataPermission.md) | The permissions associated with the data under the access requirement |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo






## LinkML Source

<details>
```yaml
name: DataPermissionEnum
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
permissible_values:
  Agreement:
    text: Agreement
    description: Data use conditions are derived from a Data Use Agreement.
  Attestation:
    text: Attestation
    description: Data use conditions are derived from an Attestation.
  Award:
    text: Award
    description: Data use conditions are derived from an Award.
  Other:
    text: Other
    description: Other permissions may apply to the data access.

```
</details>

</div>