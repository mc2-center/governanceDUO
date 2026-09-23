---
search:
  boost: 2.0
---


# Enum: ApprovalStatus 




_An AccessApproval's state (org.sagebionetworks.repo.model.ApprovalState), verified against Synapse's OpenAPI spec._



<div data-search-exclude markdown="1">

URI: [gov:ApprovalStatus](https://w3id.org/synapse/governance#ApprovalStatus)

**Enum URI:** [gov:ApprovalStatus](https://w3id.org/synapse/governance#ApprovalStatus)


## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| APPROVED | gov:Approved | Approved |
| REVOKED | gov:Revoked | The approval was revoked |













## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo






## LinkML Source

<details>
```yaml
name: ApprovalStatus
implements:
- skos:Concept
description: An AccessApproval's state (org.sagebionetworks.repo.model.ApprovalState),
  verified against Synapse's OpenAPI spec.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
enum_uri: gov:ApprovalStatus
permissible_values:
  APPROVED:
    text: APPROVED
    description: Approved. One concept in both the ApprovalStatus and SubmissionState
      schemes.
    meaning: gov:Approved
  REVOKED:
    text: REVOKED
    description: The approval was revoked.
    meaning: gov:Revoked

```
</details>

</div>