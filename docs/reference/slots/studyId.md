---
search:
  boost: 5.0
---

# Slot: studyId 


_The Study (this repo's real governanceduo:Study class, study.yaml) this IRBRequirement's language was authored for. slot_uri is owl:sameAs itself, not a domain-specific predicate: Study lives in a different namespace (governanceduo:), so this declares a co-reference rather than a same-namespace object property -- the same pattern AccessRequirement stubs need (see add_access_requirement_association()) but can't yet declare, since that stub has no governance_graph.yaml class of its own to hang a slot_uri off of. range is the untyped uriorcurie, not Study itself: the referenced Study individual is never asserted (type or otherwise) in this ABox -- its full definition lives only in the separately-built linkml/examples/rdf/ graph -- so an sh:class Study constraint would fail against this graph alone even when the reference is entirely correct._



<div data-search-exclude markdown="1">



URI: [owl:sameAs](http://www.w3.org/2002/07/owl#sameAs)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [IRBRequirement](../classes/IRBRequirement.md) | A site/program-specific instantiation of an AccessRequirementTemplate, per th... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Uriorcurie](../types/Uriorcurie.md) |
| Domain Of | [IRBRequirement](../classes/IRBRequirement.md) |
| Slot URI | [owl:sameAs](http://www.w3.org/2002/07/owl#sameAs) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:sameAs |
| native | governanceduo:studyId |




## LinkML Source

<details>
```yaml
name: studyId
description: 'The Study (this repo''s real governanceduo:Study class, study.yaml)
  this IRBRequirement''s language was authored for. slot_uri is owl:sameAs itself,
  not a domain-specific predicate: Study lives in a different namespace (governanceduo:),
  so this declares a co-reference rather than a same-namespace object property --
  the same pattern AccessRequirement stubs need (see add_access_requirement_association())
  but can''t yet declare, since that stub has no governance_graph.yaml class of its
  own to hang a slot_uri off of. range is the untyped uriorcurie, not Study itself:
  the referenced Study individual is never asserted (type or otherwise) in this ABox
  -- its full definition lives only in the separately-built linkml/examples/rdf/ graph
  -- so an sh:class Study constraint would fail against this graph alone even when
  the reference is entirely correct.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: owl:sameAs
domain_of:
- IRBRequirement
range: uriorcurie

```
</details></div>