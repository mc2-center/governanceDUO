---
search:
  boost: 2.0
---


# Enum: AccessRequirementType 




_An Access Requirement's Synapse concreteType, by its short class name._



<div data-search-exclude markdown="1">

URI: [gov:AccessRequirementType](https://w3id.org/synapse/governance#AccessRequirementType)

**Enum URI:** [gov:AccessRequirementType](https://w3id.org/synapse/governance#AccessRequirementType)


## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| TermsOfUseAccessRequirement | gov:TermsOfUseRequirement | Restricted by terms of use (AccessRequirementType |
| SelfSignAccessRequirement | gov:SelfSignRequirement | Restricted by terms of use, self-signed (AccessRequirementType |
| ACTAccessRequirement | gov:ACTRequirement | Controlled by the Access and Compliance Team (AccessRequirementType |
| ManagedACTAccessRequirement | gov:ManagedACTRequirement | Controlled by the Access and Compliance Team, with a managed data access subm... |
| LockAccessRequirement | gov:LockRequirement | Controlled by the Access and Compliance Team; locks an entity (AccessRequirem... |




## Slots

| Name | Description |
| ---  | --- |
| [concreteType](../slots/concreteType.md) | Which kind of Access Requirement this is (ACCESS_REQUIREMENT |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo






## LinkML Source

<details>
```yaml
name: AccessRequirementType
implements:
- skos:Concept
description: An Access Requirement's Synapse concreteType, by its short class name.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
enum_uri: gov:AccessRequirementType
permissible_values:
  TermsOfUseAccessRequirement:
    text: TermsOfUseAccessRequirement
    description: Restricted by terms of use (AccessRequirementType.TOU).
    meaning: gov:TermsOfUseRequirement
  SelfSignAccessRequirement:
    text: SelfSignAccessRequirement
    description: Restricted by terms of use, self-signed (AccessRequirementType.SELF_SIGNED).
    meaning: gov:SelfSignRequirement
  ACTAccessRequirement:
    text: ACTAccessRequirement
    description: Controlled by the Access and Compliance Team (AccessRequirementType.ATC).
    meaning: gov:ACTRequirement
  ManagedACTAccessRequirement:
    text: ManagedACTAccessRequirement
    description: Controlled by the Access and Compliance Team, with a managed data
      access submission workflow (AccessRequirementType.MANAGED_ATC). The only type
      with DataAccessSubmissions.
    meaning: gov:ManagedACTRequirement
  LockAccessRequirement:
    text: LockAccessRequirement
    description: Controlled by the Access and Compliance Team; locks an entity (AccessRequirementType.LOCK).
    meaning: gov:LockRequirement

```
</details>

</div>