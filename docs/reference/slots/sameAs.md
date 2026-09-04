---
search:
  boost: 5.0
---

# Slot: sameAs 


_Bridges this AccessRequirementReference stub to the real governanceduo:AccessRequirement individual with the same underlying id -- add_access_requirement_association() mints both from the same source id via gov_id()/the plain dotted form respectively. range is the untyped uriorcurie, not AccessRequirement itself, for the same reason IRBRequirement.studyId uses it: the referenced individual is never asserted (type or otherwise) in this ABox -- its full definition lives only in the separately-built linkml/examples/rdf/ graph -- so an sh:class AccessRequirement constraint would fail against this graph alone even when the reference is entirely correct._



<div data-search-exclude markdown="1">



URI: [owl:sameAs](http://www.w3.org/2002/07/owl#sameAs)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AccessRequirementReference](../classes/AccessRequirementReference.md) | The gov:AR-<n> stub build_governance_graph |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Uriorcurie](../types/Uriorcurie.md) |
| Domain Of | [AccessRequirementReference](../classes/AccessRequirementReference.md) |
| Slot URI | [owl:sameAs](http://www.w3.org/2002/07/owl#sameAs) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:sameAs |
| native | governanceduo:sameAs |




## LinkML Source

<details>
```yaml
name: sameAs
description: 'Bridges this AccessRequirementReference stub to the real governanceduo:AccessRequirement
  individual with the same underlying id -- add_access_requirement_association() mints
  both from the same source id via gov_id()/the plain dotted form respectively. range
  is the untyped uriorcurie, not AccessRequirement itself, for the same reason IRBRequirement.studyId
  uses it: the referenced individual is never asserted (type or otherwise) in this
  ABox -- its full definition lives only in the separately-built linkml/examples/rdf/
  graph -- so an sh:class AccessRequirement constraint would fail against this graph
  alone even when the reference is entirely correct.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: owl:sameAs
domain_of:
- AccessRequirementReference
range: uriorcurie
required: true

```
</details></div>