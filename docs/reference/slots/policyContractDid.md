---
search:
  boost: 5.0
---

# Slot: policyContractDid 


_The DID of the deployed rego_policy_agent/rego_token contract pair once this AccessRequirement's selected DUO codes have been "exposed" as a policy in Policy Fabric. Mirrors Asset.metadata.policy_contract._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/policyContractDid](https://w3id.org/sage-bionetworks/governance-duo/slot/policyContractDid)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PolicyFabricMixin](../classes/PolicyFabricMixin.md) | Fields needed to deploy an AccessRequirement's governed entities into Policy ... |  no  |
| [AccessRequirement](../classes/AccessRequirement.md) | Representation of a Synapse Access Requirement and its relationships to entit... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [PolicyFabricMixin](../classes/PolicyFabricMixin.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
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
| self | governanceduo:policyContractDid |
| native | governanceduo:policyContractDid |




## LinkML Source

<details>
```yaml
name: policyContractDid
description: The DID of the deployed rego_policy_agent/rego_token contract pair once
  this AccessRequirement's selected DUO codes have been "exposed" as a policy in Policy
  Fabric. Mirrors Asset.metadata.policy_contract.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- PolicyFabricMixin
range: string
pattern: ^did:[a-z0-9]+:.+$

```
</details></div>