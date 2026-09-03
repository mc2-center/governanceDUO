---
search:
  boost: 2.0
---


# Enum: ApprovalStateEnum 




_Synapse's real AccessApproval state values (org.sagebionetworks.repo.model.ApprovalState), verified directly against the OpenAPI spec -- APPROVED/REVOKED only. A distinct, smaller enum from SubmissionStateEnum above; do not conflate the two even though both happen to include "APPROVED"._



<div data-search-exclude markdown="1">

URI: [governanceduo:enum/ApprovalStateEnum](https://w3id.org/sage-bionetworks/governance-duo/enum/ApprovalStateEnum)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| APPROVED | None |  |
| REVOKED | None |  |




## Slots

| Name | Description |
| ---  | --- |
| [status](../slots/status.md) | The state of this approval (AccessApproval |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo






## LinkML Source

<details>
```yaml
name: ApprovalStateEnum
description: Synapse's real AccessApproval state values (org.sagebionetworks.repo.model.ApprovalState),
  verified directly against the OpenAPI spec -- APPROVED/REVOKED only. A distinct,
  smaller enum from SubmissionStateEnum above; do not conflate the two even though
  both happen to include "APPROVED".
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
permissible_values:
  APPROVED:
    text: APPROVED
  REVOKED:
    text: REVOKED

```
</details>

</div>