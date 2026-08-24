---
search:
  boost: 2.0
---


# Enum: DataTierEnum 



<div data-search-exclude markdown="1">

URI: [governanceduo:enum/DataTierEnum](https://w3id.org/sage-bionetworks/governance-duo/enum/DataTierEnum)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| Anonymous | None | Data can be viewed and downloaded anonymously by anyone on the internet |
| Open | None | Users must have a Synapse account to download data |
| Controlled | None | Users must have a Synapse account and satisfy access conditions to download d... |
| Private | None | Users must be provided access to data in Synapse by a project administrator |




## Slots

| Name | Description |
| ---  | --- |
| [dataTier](../slots/dataTier.md) | The tier of data access associated with the access requirement |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo






## LinkML Source

<details>
```yaml
name: DataTierEnum
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
permissible_values:
  Anonymous:
    text: Anonymous
    description: Data can be viewed and downloaded anonymously by anyone on the internet.
  Open:
    text: Open
    description: Users must have a Synapse account to download data.
  Controlled:
    text: Controlled
    description: Users must have a Synapse account and satisfy access conditions to
      download data.
  Private:
    text: Private
    description: Users must be provided access to data in Synapse by a project administrator.

```
</details>

</div>