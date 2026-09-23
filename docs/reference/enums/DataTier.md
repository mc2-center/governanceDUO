---
search:
  boost: 2.0
---


# Enum: DataTier 




_How restricted data is, in increasing order. Each concept's gov:rank is its position: a derived output takes the highest rank among its inputs._



<div data-search-exclude markdown="1">

URI: [gov:DataTier](https://w3id.org/synapse/governance#DataTier)

**Enum URI:** [gov:DataTier](https://w3id.org/synapse/governance#DataTier)


## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| Anonymous | gov:AnonymousTier | Data can be viewed and downloaded anonymously by anyone on the internet |
| Open | gov:OpenTier | Users must have a Synapse account to download data |
| Controlled | gov:ControlledTier | Users must have a Synapse account and satisfy access conditions to download d... |
| Private | gov:PrivateTier | Users must be provided access to data in Synapse by a project administrator |
| Unclassified | gov:UnclassifiedTier | Tier not yet determined by a curator |




## Slots

| Name | Description |
| ---  | --- |
| [dataTier](../slots/dataTier.md) | The tier of data access associated with the access requirement |
| [inputDataTiers](../slots/inputDataTiers.md) | The combination of input DataTier values this rule governs |
| [resultingDataTier](../slots/resultingDataTier.md) | The DataTier the derived output carries when permitted |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo






## LinkML Source

<details>
```yaml
name: DataTier
implements:
- skos:Concept
description: 'How restricted data is, in increasing order. Each concept''s gov:rank
  is its position: a derived output takes the highest rank among its inputs.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
enum_uri: gov:DataTier
permissible_values:
  Anonymous:
    text: Anonymous
    description: Data can be viewed and downloaded anonymously by anyone on the internet.
    meaning: gov:AnonymousTier
    rank: 0
  Open:
    text: Open
    description: Users must have a Synapse account to download data.
    meaning: gov:OpenTier
    rank: 1
  Controlled:
    text: Controlled
    description: Users must have a Synapse account and satisfy access conditions to
      download data.
    meaning: gov:ControlledTier
    rank: 2
  Private:
    text: Private
    description: Users must be provided access to data in Synapse by a project administrator.
    meaning: gov:PrivateTier
    rank: 3
  Unclassified:
    text: Unclassified
    description: Tier not yet determined by a curator. Ranked above Private, so an
      entity bound to an Access Requirement with no recorded tier fails closed rather
      than reading as unrestricted.
    meaning: gov:UnclassifiedTier
    rank: 4

```
</details>

</div>