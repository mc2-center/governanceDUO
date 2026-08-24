---
search:
  boost: 2.0
---


# Enum: AccessRequirementConcreteTypeEnum 




_Synapse's real AccessRequirement subclasses, verified via Sage-Bionetworks/Synapse-Repository-Services's AccessRequirementType.java (lib/jdomodels/.../org/sagebionetworks/repo/model/ar/AccessRequirementType.java). Permissible values use the short Java class name; the actual ACCESS_REQUIREMENT.CONCRETE_TYPE column stores the fully-qualified name (e.g. "org.sagebionetworks.repo.model.ManagedACTAccessRequirement")._



<div data-search-exclude markdown="1">

URI: [governanceduo:enum/AccessRequirementConcreteTypeEnum](https://w3id.org/sage-bionetworks/governance-duo/enum/AccessRequirementConcreteTypeEnum)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| TermsOfUseAccessRequirement | None | Restricted by terms of use (AccessRequirementType |
| SelfSignAccessRequirement | None | Restricted by terms of use, self-signed (AccessRequirementType |
| ACTAccessRequirement | None | Controlled by the Access and Compliance Team (AccessRequirementType |
| ManagedACTAccessRequirement | None | Controlled by the Access and Compliance Team, with a managed data access subm... |
| LockAccessRequirement | None | Controlled by the Access and Compliance Team; locks an entity (AccessRequirem... |




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
name: AccessRequirementConcreteTypeEnum
description: Synapse's real AccessRequirement subclasses, verified via Sage-Bionetworks/Synapse-Repository-Services's
  AccessRequirementType.java (lib/jdomodels/.../org/sagebionetworks/repo/model/ar/AccessRequirementType.java).
  Permissible values use the short Java class name; the actual ACCESS_REQUIREMENT.CONCRETE_TYPE
  column stores the fully-qualified name (e.g. "org.sagebionetworks.repo.model.ManagedACTAccessRequirement").
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
permissible_values:
  TermsOfUseAccessRequirement:
    text: TermsOfUseAccessRequirement
    description: Restricted by terms of use (AccessRequirementType.TOU).
  SelfSignAccessRequirement:
    text: SelfSignAccessRequirement
    description: Restricted by terms of use, self-signed (AccessRequirementType.SELF_SIGNED).
  ACTAccessRequirement:
    text: ACTAccessRequirement
    description: Controlled by the Access and Compliance Team (AccessRequirementType.ATC).
  ManagedACTAccessRequirement:
    text: ManagedACTAccessRequirement
    description: Controlled by the Access and Compliance Team, with a managed data
      access submission workflow (AccessRequirementType.MANAGED_ATC) — the type backing
      DataAccessSubmission/DataAccessSubmissionStatus in governance_graph.yaml.
  LockAccessRequirement:
    text: LockAccessRequirement
    description: Controlled by the Access and Compliance Team; locks an entity (AccessRequirementType.LOCK).

```
</details>

</div>