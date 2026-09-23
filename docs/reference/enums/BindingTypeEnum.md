---
search:
  boost: 2.0
---


# Enum: BindingTypeEnum 




_Whether a governance relationship (an AccessGrant or AccessRequirementAssociation) applies directly to a resource or is inherited from a parent (e.g. a file inheriting its parent study's Access Requirement) — from the design doc's own `gov:bindingType gov:Inherited` example. Not a Synapse database column; ACCESS_REQUIREMENT_PROJECT and the ACL tables record only the direct binding, so inheritance has to be resolved (via SynapseEntity.parentId) and recorded explicitly, per the design doc's "Direct and Inherited Governance" section. Each value's meaning: is the gov: IRI scripts/build_governance_graph.py emits for gov:bindingType._



<div data-search-exclude markdown="1">

URI: [governanceduo:enum/BindingTypeEnum](https://w3id.org/sage-bionetworks/governance-duo/enum/BindingTypeEnum)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| Direct | sagegov:Direct |  |
| Inherited | sagegov:Inherited |  |




## Slots

| Name | Description |
| ---  | --- |
| [bindingType](../slots/bindingType.md) |  |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo






## LinkML Source

<details>
```yaml
name: BindingTypeEnum
implements:
- owl:NamedIndividual
description: 'Whether a governance relationship (an AccessGrant or AccessRequirementAssociation)
  applies directly to a resource or is inherited from a parent (e.g. a file inheriting
  its parent study''s Access Requirement) — from the design doc''s own `gov:bindingType
  gov:Inherited` example. Not a Synapse database column; ACCESS_REQUIREMENT_PROJECT
  and the ACL tables record only the direct binding, so inheritance has to be resolved
  (via SynapseEntity.parentId) and recorded explicitly, per the design doc''s "Direct
  and Inherited Governance" section. Each value''s meaning: is the gov: IRI scripts/build_governance_graph.py
  emits for gov:bindingType.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
permissible_values:
  Direct:
    text: Direct
    meaning: sagegov:Direct
  Inherited:
    text: Inherited
    meaning: sagegov:Inherited

```
</details>

</div>