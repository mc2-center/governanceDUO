---
search:
  boost: 5.0
---

# Slot: createdBy 


_Synapse numeric user id of the record's creator. Shared the same way as `name` above. Distinct from ContributionMixin's contributorName, which is this repo's own free-text curator-provenance field, not Synapse's own numeric CREATED_BY column — both coexist on AccessRequirement without collision._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/createdBy](https://w3id.org/sage-bionetworks/governance-duo/slot/createdBy)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [SynapseAccessRequirementMixin](../classes/SynapseAccessRequirementMixin.md) | The real Synapse-native ACCESS_REQUIREMENT row fields (verified against "sage... |  no  |
| [SynapseEntity](../classes/SynapseEntity.md) | A concrete Synapse entity (project, folder, file, etc |  no  |
| [DataAccessSubmission](../classes/DataAccessSubmission.md) | A user's application against an AccessRequirement |  no  |
| [DataAccessSubmissionStatus](../classes/DataAccessSubmissionStatus.md) | The approval-workflow state of a DataAccessSubmission |  no  |
| [AccessRequirement](../classes/AccessRequirement.md) | Representation of a Synapse Access Requirement and its relationships to entit... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Integer](../types/Integer.md) |
| Domain Of | [SynapseAccessRequirementMixin](../classes/SynapseAccessRequirementMixin.md), [SynapseEntity](../classes/SynapseEntity.md), [DataAccessSubmission](../classes/DataAccessSubmission.md), [DataAccessSubmissionStatus](../classes/DataAccessSubmissionStatus.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:createdBy |
| native | governanceduo:createdBy |
| exact | dcterms:creator |




## LinkML Source

<details>
```yaml
name: createdBy
description: Synapse numeric user id of the record's creator. Shared the same way
  as `name` above. Distinct from ContributionMixin's contributorName, which is this
  repo's own free-text curator-provenance field, not Synapse's own numeric CREATED_BY
  column — both coexist on AccessRequirement without collision.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
exact_mappings:
- dcterms:creator
rank: 1000
domain_of:
- SynapseAccessRequirementMixin
- SynapseEntity
- DataAccessSubmission
- DataAccessSubmissionStatus
range: integer

```
</details></div>