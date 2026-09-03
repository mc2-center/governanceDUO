---
search:
  boost: 5.0
---

# Slot: id 


_A unique identifier for this record. Narrowed per class via `slot_usage` in access_requirement.yaml/resource.yaml/schema.yaml/study.yaml/governance_graph.yaml (SynapseEntity/AccessGrant/AccessRequirementAssociation/DataAccessSubmission). The schematic CSV source (../model/*.model.csv) keeps class-prefixed attribute names (AccessRequirement_id, Resource_id, Schema_id, Study_id) instead: schematic's model CSV has one flat, global Attribute namespace with no per-class scoping equivalent to slot_usage, so four classes cannot share a bare "id" attribute there without colliding._



<div data-search-exclude markdown="1">



URI: [dcterms:identifier](http://purl.org/dc/terms/identifier)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [BaseEntity](../classes/BaseEntity.md) | Abstract root shared by every governanceDUO class |  no  |
| [AccessRequirement](../classes/AccessRequirement.md) | Representation of a Synapse Access Requirement and its relationships to entit... |  yes  |
| [Resource](../classes/Resource.md) | Information that is relevant to resource access conditions |  yes  |
| [Schema](../classes/Schema.md) | Information that is relevant to resource access conditions |  yes  |
| [Study](../classes/Study.md) | Studies associated with a grant |  yes  |
| [SynapseEntity](../classes/SynapseEntity.md) | A concrete Synapse entity (project, folder, file, etc |  yes  |
| [AccessGrant](../classes/AccessGrant.md) | A first-class ACL grant: resource, principal, permission(s), source, and whet... |  yes  |
| [AccessRequirementAssociation](../classes/AccessRequirementAssociation.md) | Binds an AccessRequirement to a resource, recording whether the binding is di... |  yes  |
| [DataAccessSubmission](../classes/DataAccessSubmission.md) | A user's application against an AccessRequirement |  yes  |
| [AccessApproval](../classes/AccessApproval.md) | Records that a Principal has been approved for access under an AccessRequirem... |  yes  |
| [ResearchProject](../classes/ResearchProject.md) | Documents the research context/justification behind a DataAccessRequest (and,... |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [BaseEntity](../classes/BaseEntity.md) |
| Slot URI | [dcterms:identifier](http://purl.org/dc/terms/identifier) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
### Slot Characteristics

| Property | Value |
| --- | --- |
| Identifier | Yes |












## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dcterms:identifier |
| native | governanceduo:id |




## LinkML Source

<details>
```yaml
name: id
description: 'A unique identifier for this record. Narrowed per class via `slot_usage`
  in access_requirement.yaml/resource.yaml/schema.yaml/study.yaml/governance_graph.yaml
  (SynapseEntity/AccessGrant/AccessRequirementAssociation/DataAccessSubmission). The
  schematic CSV source (../model/*.model.csv) keeps class-prefixed attribute names
  (AccessRequirement_id, Resource_id, Schema_id, Study_id) instead: schematic''s model
  CSV has one flat, global Attribute namespace with no per-class scoping equivalent
  to slot_usage, so four classes cannot share a bare "id" attribute there without
  colliding.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: dcterms:identifier
identifier: true
domain_of:
- BaseEntity
range: string
required: true

```
</details></div>