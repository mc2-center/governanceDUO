---
search:
  boost: 2.0
---


# Enum: DrsAuthTypeEnum 




_Mirrors DRS's Authorizations.supported_types enum (https://ga4gh.github.io/data-repository-service-schemas/docs/). More than one can be supported and tried in sequence, per the DRS spec._



<div data-search-exclude markdown="1">

URI: [governanceduo:enum/DrsAuthTypeEnum](https://w3id.org/sage-bionetworks/governance-duo/enum/DrsAuthTypeEnum)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| None | None | No authorization required — the object is fully public |
| BasicAuth | None | HTTP Basic authentication |
| BearerAuth | None | HTTP Bearer token authentication |
| PassportAuth | None | A GA4GH Passport (a signed JWT carrying one or more Visa claims) submitted as... |




## Slots

| Name | Description |
| ---  | --- |
| [supportedAuthTypes](../slots/supportedAuthTypes.md) | Mirrors DRS's Authorizations |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo






## LinkML Source

<details>
```yaml
name: DrsAuthTypeEnum
description: Mirrors DRS's Authorizations.supported_types enum (https://ga4gh.github.io/data-repository-service-schemas/docs/).
  More than one can be supported and tried in sequence, per the DRS spec.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
permissible_values:
  None:
    text: None
    description: No authorization required — the object is fully public.
  BasicAuth:
    text: BasicAuth
    description: HTTP Basic authentication.
  BearerAuth:
    text: BearerAuth
    description: HTTP Bearer token authentication.
  PassportAuth:
    text: PassportAuth
    description: A GA4GH Passport (a signed JWT carrying one or more Visa claims)
      submitted as a `passports[]` array in the request body. The realistic default
      for all DUO-governed access, given Policy Fabric already models Verifiable-Credential
      presentation for the same conditions.

```
</details>

</div>