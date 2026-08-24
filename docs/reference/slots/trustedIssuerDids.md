---
search:
  boost: 5.0
---

# Slot: trustedIssuerDids 


_DID(s) of the Verifiable Credential issuer(s) this AccessRequirement's owner trusts to attest the claims its selected DUO codes require (see policy_fabric_bindings.yaml's requiredCredentials per code). Unlike PolicyCardBinding.requiredCredentials (a static, per-DUO-code fact), this varies per AccessRequirement — different owners may trust different institutional VC issuers — so it lives here, not in the policy_fabric.yaml lookup schema._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/trustedIssuerDids](https://w3id.org/sage-bionetworks/governance-duo/slot/trustedIssuerDids)
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
| self | governanceduo:trustedIssuerDids |
| native | governanceduo:trustedIssuerDids |




## LinkML Source

<details>
```yaml
name: trustedIssuerDids
description: DID(s) of the Verifiable Credential issuer(s) this AccessRequirement's
  owner trusts to attest the claims its selected DUO codes require (see policy_fabric_bindings.yaml's
  requiredCredentials per code). Unlike PolicyCardBinding.requiredCredentials (a static,
  per-DUO-code fact), this varies per AccessRequirement — different owners may trust
  different institutional VC issuers — so it lives here, not in the policy_fabric.yaml
  lookup schema.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- PolicyFabricMixin
range: string
multivalued: true
pattern: ^did:[a-z0-9]+:.+$

```
</details></div>