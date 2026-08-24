---
search:
  boost: 10.0
---

# Class: BaseEntity 


_Abstract root shared by every governanceDUO class._



<div data-search-exclude markdown="1">


* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [governanceduo:class/BaseEntity](https://w3id.org/sage-bionetworks/governance-duo/class/BaseEntity)





```mermaid
 classDiagram
    class BaseEntity
    click BaseEntity href "../../classes/BaseEntity/"
      BaseEntity <|-- AccessRequirement
        click AccessRequirement href "../../classes/AccessRequirement/"
      BaseEntity <|-- Resource
        click Resource href "../../classes/Resource/"
      BaseEntity <|-- Schema
        click Schema href "../../classes/Schema/"
      BaseEntity <|-- Study
        click Study href "../../classes/Study/"
      BaseEntity <|-- SynapseEntity
        click SynapseEntity href "../../classes/SynapseEntity/"
      BaseEntity <|-- AccessGrant
        click AccessGrant href "../../classes/AccessGrant/"
      BaseEntity <|-- AccessRequirementAssociation
        click AccessRequirementAssociation href "../../classes/AccessRequirementAssociation/"
      BaseEntity <|-- DataAccessSubmission
        click DataAccessSubmission href "../../classes/DataAccessSubmission/"
      
      BaseEntity : id
        
      
```





## Inheritance
* **BaseEntity**
    * [AccessRequirement](../classes/AccessRequirement.md) [ [GovernanceMixin](../classes/GovernanceMixin.md) [ContributionMixin](../classes/ContributionMixin.md) [PolicyFabricMixin](../classes/PolicyFabricMixin.md) [SynapseAccessRequirementMixin](../classes/SynapseAccessRequirementMixin.md)]
    * [Resource](../classes/Resource.md) [ [GovernanceMixin](../classes/GovernanceMixin.md)]
    * [Schema](../classes/Schema.md)
    * [Study](../classes/Study.md) [ [GovernanceMixin](../classes/GovernanceMixin.md)]
    * [SynapseEntity](../classes/SynapseEntity.md)
    * [AccessGrant](../classes/AccessGrant.md)
    * [AccessRequirementAssociation](../classes/AccessRequirementAssociation.md)
    * [DataAccessSubmission](../classes/DataAccessSubmission.md)


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](../slots/id.md) | 1 <br/> [String](../types/String.md) | A unique identifier for this record | direct |















## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:BaseEntity |
| native | governanceduo:BaseEntity |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: BaseEntity
description: Abstract root shared by every governanceDUO class.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
abstract: true
slots:
- id

```
</details>

### Induced

<details>
```yaml
name: BaseEntity
description: Abstract root shared by every governanceDUO class.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
abstract: true
attributes:
  id:
    name: id
    description: 'A unique identifier for this record. Narrowed per class via `slot_usage`
      in access_requirement.yaml/resource.yaml/schema.yaml/study.yaml. The schematic
      CSV source (../model/*.model.csv) keeps class-prefixed attribute names (AccessRequirement_id,
      Resource_id, Schema_id, Study_id) instead: schematic''s model CSV has one flat,
      global Attribute namespace with no per-class scoping equivalent to slot_usage,
      so four classes cannot share a bare "id" attribute there without colliding.'
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    slot_uri: dcterms:identifier
    identifier: true
    owner: BaseEntity
    domain_of:
    - BaseEntity
    range: string
    required: true

```
</details></div>