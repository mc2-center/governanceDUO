---
search:
  boost: 2.0
---


# Enum: SourceSystemEnum 




_The system a governance relationship (AccessGrant, AccessRequirementAssociation) was derived from. Each value's meaning: is the gov: IRI scripts/build_governance_graph.py emits for gov:source, so this schema describes the graph as built. Only values the sync and examples actually produce are listed; the design doc's gov:SynapseACL (an ACL-specific source) is not used by this repo's pipeline and isn't declared._



<div data-search-exclude markdown="1">

URI: [governanceduo:enum/SourceSystemEnum](https://w3id.org/sage-bionetworks/governance-duo/enum/SourceSystemEnum)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| Synapse | sagegov:Synapse | Derived from Synapse's own ACL or AccessRequirement records |




## Slots

| Name | Description |
| ---  | --- |
| [source](../slots/source.md) | The system this grant/association was derived from, e |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo






## LinkML Source

<details>
```yaml
name: SourceSystemEnum
description: 'The system a governance relationship (AccessGrant, AccessRequirementAssociation)
  was derived from. Each value''s meaning: is the gov: IRI scripts/build_governance_graph.py
  emits for gov:source, so this schema describes the graph as built. Only values the
  sync and examples actually produce are listed; the design doc''s gov:SynapseACL
  (an ACL-specific source) is not used by this repo''s pipeline and isn''t declared.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
permissible_values:
  Synapse:
    text: Synapse
    description: Derived from Synapse's own ACL or AccessRequirement records.
    meaning: sagegov:Synapse

```
</details>

</div>