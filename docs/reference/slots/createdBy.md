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
| [SynapseEntity](../classes/SynapseEntity.md) | A concrete Synapse entity (project, folder, file, etc |  yes  |
| [ResearchProject](../classes/ResearchProject.md) | Documents the research context/justification behind a DataAccessRequest (and,... |  yes  |
| [DataAccessRequest](../classes/DataAccessRequest.md) | A user's draft/submitted request against an AccessRequirement, behind a DataA... |  yes  |
| [AccessRequirement](../classes/AccessRequirement.md) | Representation of a Synapse Access Requirement and its relationships to entit... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Integer](../types/Integer.md) |
| Domain Of | [SynapseAccessRequirementMixin](../classes/SynapseAccessRequirementMixin.md), [SynapseEntity](../classes/SynapseEntity.md), [ResearchProject](../classes/ResearchProject.md), [DataAccessRequest](../classes/DataAccessRequest.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |








## Comments

* scripts/build_governance_graph.py emits this integer two different ways depending on which class it's on: as an IRI reference to a gov:Principal node (gov:createdBy) on DataAccessSubmission -- since a submission's creator can be looked up as a first-class Principal individual -- but as a plain literal (gov:createdByUserId, a distinct predicate, not gov:createdBy) on SynapseEntity, which has no corresponding Principal record to link to. This divergence is deliberate and documented in shapes/governance_graph.owl.ttl, not a schema/export mismatch to fix.



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
comments:
- 'scripts/build_governance_graph.py emits this integer two different ways depending
  on which class it''s on: as an IRI reference to a gov:Principal node (gov:createdBy)
  on DataAccessSubmission -- since a submission''s creator can be looked up as a first-class
  Principal individual -- but as a plain literal (gov:createdByUserId, a distinct
  predicate, not gov:createdBy) on SynapseEntity, which has no corresponding Principal
  record to link to. This divergence is deliberate and documented in shapes/governance_graph.owl.ttl,
  not a schema/export mismatch to fix.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
exact_mappings:
- dcterms:creator
rank: 1000
domain_of:
- SynapseAccessRequirementMixin
- SynapseEntity
- ResearchProject
- DataAccessRequest
range: integer

```
</details></div>