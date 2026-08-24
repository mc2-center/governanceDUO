---
search:
  boost: 5.0
---

# Slot: institutionDids 


_Institutions with specific restrictions associated with the access requirement, as decentralized identifiers (DIDs) rather than ROR ids. Policy Fabric (https://github.com/hasan7n/tmp-policies)'s institution-specific-restriction policy_card expects its allowedInstitutions reference values, and the AffiliationCredential.isMemberOf claim it checks against them, to both be organization DIDs — not ROR ids. No standard ROR-to-DID resolution exists yet, so this is a separate, companion slot rather than a reinterpretation of institutionSpecificRestriction's existing pattern._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/institutionDids](https://w3id.org/sage-bionetworks/governance-duo/slot/institutionDids)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [GovernanceMixin](../classes/GovernanceMixin.md) | DUO-based data-use-modifier vocabulary and its conditional-requirement rules,... |  no  |
| [AccessRequirement](../classes/AccessRequirement.md) | Representation of a Synapse Access Requirement and its relationships to entit... |  no  |
| [Resource](../classes/Resource.md) | Information that is relevant to resource access conditions |  no  |
| [Study](../classes/Study.md) | Studies associated with a grant |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [GovernanceMixin](../classes/GovernanceMixin.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |
### Value Constraints

| Property | Value |
| --- | --- |
| Regex Pattern | `^did:[a-z0-9]+:.+$` |












## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:institutionDids |
| native | governanceduo:institutionDids |




## LinkML Source

<details>
```yaml
name: institutionDids
description: Institutions with specific restrictions associated with the access requirement,
  as decentralized identifiers (DIDs) rather than ROR ids. Policy Fabric (https://github.com/hasan7n/tmp-policies)'s
  institution-specific-restriction policy_card expects its allowedInstitutions reference
  values, and the AffiliationCredential.isMemberOf claim it checks against them, to
  both be organization DIDs — not ROR ids. No standard ROR-to-DID resolution exists
  yet, so this is a separate, companion slot rather than a reinterpretation of institutionSpecificRestriction's
  existing pattern.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- GovernanceMixin
range: string
multivalued: true
pattern: ^did:[a-z0-9]+:.+$

```
</details></div>