---
search:
  boost: 2.0
---


# Enum: SubmissionStateEnum 




_Synapse's real DataAccessSubmissionState values, verified via Sage-Bionetworks/SynapseWebClient source (ACTDataAccessSubmissionWidget.java's exhaustive state switch) — the "sagebrain governance graph ACL_AR data - AR table schemas.csv" only says DATA_ACCESS_SUBMISSION_STATUS.STATE is TEXT, with no NOTES-column value list._



<div data-search-exclude markdown="1">

URI: [governanceduo:enum/SubmissionStateEnum](https://w3id.org/sage-bionetworks/governance-duo/enum/SubmissionStateEnum)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| SUBMITTED | None |  |
| APPROVED | None |  |
| REJECTED | None |  |
| CANCELLED | None |  |




## Slots

| Name | Description |
| ---  | --- |
| [state](../slots/state.md) |  |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo






## LinkML Source

<details>
```yaml
name: SubmissionStateEnum
description: Synapse's real DataAccessSubmissionState values, verified via Sage-Bionetworks/SynapseWebClient
  source (ACTDataAccessSubmissionWidget.java's exhaustive state switch) — the "sagebrain
  governance graph ACL_AR data - AR table schemas.csv" only says DATA_ACCESS_SUBMISSION_STATUS.STATE
  is TEXT, with no NOTES-column value list.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
permissible_values:
  SUBMITTED:
    text: SUBMITTED
  APPROVED:
    text: APPROVED
  REJECTED:
    text: REJECTED
  CANCELLED:
    text: CANCELLED

```
</details>

</div>