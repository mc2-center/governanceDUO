---
search:
  boost: 5.0
---

# Slot: capabilityOperation 


_The "name" field of the Capability Granted this policy_card's Rego emits on success (every one of the 21 verified policy_cards emits "do_download" today — Policy Fabric has not yet diversified beyond dataset download)._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/capabilityOperation](https://w3id.org/sage-bionetworks/governance-duo/slot/capabilityOperation)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PolicyCardBinding](../classes/PolicyCardBinding.md) | One row per verified tmp-policies policy_cards/<name>/ folder: which DUO code... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [PolicyCardBinding](../classes/PolicyCardBinding.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
### Slot Characteristics

| Property | Value |
| --- | --- |
| If Absent | `string(do_download)` |










## Comments

* Related to, but intentionally not unified with, mixins.yaml's AccessTypeEnum (used by AccessGrant.permission and AccessRequirement.accessType): both describe "what operation is being granted," but AccessTypeEnum is Synapse's own closed ACL vocabulary while this slot is Policy Fabric's free-string Rego capability-name convention -- the two vocabularies belong to different external systems and may drift independently, so this stays a free string rather than being coerced into AccessTypeEnum.



## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:capabilityOperation |
| native | governanceduo:capabilityOperation |




## LinkML Source

<details>
```yaml
name: capabilityOperation
description: The "name" field of the Capability Granted this policy_card's Rego emits
  on success (every one of the 21 verified policy_cards emits "do_download" today
  — Policy Fabric has not yet diversified beyond dataset download).
comments:
- 'Related to, but intentionally not unified with, mixins.yaml''s AccessTypeEnum (used
  by AccessGrant.permission and AccessRequirement.accessType): both describe "what
  operation is being granted," but AccessTypeEnum is Synapse''s own closed ACL vocabulary
  while this slot is Policy Fabric''s free-string Rego capability-name convention
  -- the two vocabularies belong to different external systems and may drift independently,
  so this stays a free string rather than being coerced into AccessTypeEnum.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
ifabsent: string(do_download)
domain_of:
- PolicyCardBinding
range: string

```
</details></div>