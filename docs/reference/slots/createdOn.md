---
search:
  boost: 5.0
---

# Slot: createdOn 


_When the record was created (epoch milliseconds in the source Synapse tables). Shared the same way as `name` above. Distinct from ContributionMixin's contributionDate for the same reason as createdBy above._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/createdOn](https://w3id.org/sage-bionetworks/governance-duo/slot/createdOn)
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
| Range | [Integer](../types/Integer.md) |
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
| self | governanceduo:createdOn |
| native | governanceduo:createdOn |
| exact | dcterms:created |




## LinkML Source

<details>
```yaml
name: createdOn
description: When the record was created (epoch milliseconds in the source Synapse
  tables). Shared the same way as `name` above. Distinct from ContributionMixin's
  contributionDate for the same reason as createdBy above.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
exact_mappings:
- dcterms:created
rank: 1000
domain_of:
- SynapseAccessRequirementMixin
range: integer

```
</details></div>