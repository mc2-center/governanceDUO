---
search:
  boost: 5.0
---

# Slot: concreteType 


_Which kind of Access Requirement this is (ACCESS_REQUIREMENT.CONCRETE_TYPE). The real Synapse column stores the full Java class name (e.g. "org.sagebionetworks.repo.model.ManagedACTAccessRequirement"); this vocabulary uses the short class name for readability. Range is the graph layer's own AccessRequirementType vocabulary (linkml/graph/vocabularies.yaml), the same one gov:AccessRequirement.requirementType uses._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/concreteType](https://w3id.org/sage-bionetworks/governance-duo/slot/concreteType)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [SynapseAccessRequirementMixin](../classes/SynapseAccessRequirementMixin.md) | The real Synapse-native ACCESS_REQUIREMENT row fields (verified against "sage... |  no  |
| [AccessRequirement](../classes/AccessRequirement.md) | Representation of a Synapse Access Requirement and its relationships to entit... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [AccessRequirementType](../enums/AccessRequirementType.md) |
| Domain Of | [SynapseAccessRequirementMixin](../classes/SynapseAccessRequirementMixin.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:concreteType |
| native | governanceduo:concreteType |




## LinkML Source

<details>
```yaml
name: concreteType
description: Which kind of Access Requirement this is (ACCESS_REQUIREMENT.CONCRETE_TYPE).
  The real Synapse column stores the full Java class name (e.g. "org.sagebionetworks.repo.model.ManagedACTAccessRequirement");
  this vocabulary uses the short class name for readability. Range is the graph layer's
  own AccessRequirementType vocabulary (linkml/graph/vocabularies.yaml), the same
  one gov:AccessRequirement.requirementType uses.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- SynapseAccessRequirementMixin
range: AccessRequirementType

```
</details></div>