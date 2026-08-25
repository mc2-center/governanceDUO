---
search:
  boost: 5.0
---

# Slot: passportAuthIssuers 


_Mirrors DRS's Authorizations.passport_auth_issuers — the whitelisted set of Visa `iss` issuers a client must draw from. Not populated here from a fixed value: sourced, per governed AccessRequirement, from that record's own PolicyFabricMixin.trustedIssuerDids (or, for institution-scoped DUO codes, GovernanceMixin.institutionDids) — see mixins.yaml. GA4GH Passport Visa issuers are conventionally identified as DIDs or URLs the same way those slots already are._



<div data-search-exclude markdown="1">



URI: [governanceduo:slot/passportAuthIssuers](https://w3id.org/sage-bionetworks/governance-duo/slot/passportAuthIssuers)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DrsAuthorizationBinding](../classes/DrsAuthorizationBinding.md) | Crosswalks one DUO code (or Sage DUOPlus extension) to the shape of the DRS A... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [DrsAuthorizationBinding](../classes/DrsAuthorizationBinding.md) |

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
| self | governanceduo:passportAuthIssuers |
| native | governanceduo:passportAuthIssuers |




## LinkML Source

<details>
```yaml
name: passportAuthIssuers
description: 'Mirrors DRS''s Authorizations.passport_auth_issuers — the whitelisted
  set of Visa `iss` issuers a client must draw from. Not populated here from a fixed
  value: sourced, per governed AccessRequirement, from that record''s own PolicyFabricMixin.trustedIssuerDids
  (or, for institution-scoped DUO codes, GovernanceMixin.institutionDids) — see mixins.yaml.
  GA4GH Passport Visa issuers are conventionally identified as DIDs or URLs the same
  way those slots already are.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- DrsAuthorizationBinding
range: string
multivalued: true
pattern: ^did:[a-z0-9]+:.+$

```
</details></div>