---
search:
  boost: 5.0
---

# Slot: studyId 


_The Study (this repo's real governanceduo:Study class, study.yaml) this IRBRequirement's language was authored for. A plain relation, not owl:sameAs: the IRB requirement is not the Study, and a co-reference would give the Study every IRBRequirement property and merge two IRB requirements authored for the same study into one individual (plans/pre_pr_review_fixes.md, finding 4). range is the untyped uriorcurie, not Study itself: the referenced Study individual is never asserted (type or otherwise) in this ABox -- its full definition lives only in the separately-built linkml/examples/rdf/ graph -- so an sh:class Study constraint would fail against this graph alone even when the reference is entirely correct._



<div data-search-exclude markdown="1">



URI: [sagegov:forStudy](https://sagebionetworks.org/governance/forStudy)
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
| Slot URI | [sagegov:forStudy](https://sagebionetworks.org/governance/forStudy) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:forStudy |
| native | governanceduo:studyId |




## LinkML Source

<details>
```yaml
name: studyId
description: 'The Study (this repo''s real governanceduo:Study class, study.yaml)
  this IRBRequirement''s language was authored for. A plain relation, not owl:sameAs:
  the IRB requirement is not the Study, and a co-reference would give the Study every
  IRBRequirement property and merge two IRB requirements authored for the same study
  into one individual (plans/pre_pr_review_fixes.md, finding 4). range is the untyped
  uriorcurie, not Study itself: the referenced Study individual is never asserted
  (type or otherwise) in this ABox -- its full definition lives only in the separately-built
  linkml/examples/rdf/ graph -- so an sh:class Study constraint would fail against
  this graph alone even when the reference is entirely correct.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:forStudy
domain_of:
- IRBRequirement
range: uriorcurie

```
</details></div>