---
search:
  boost: 2.0
---


# Enum: SubmissionStateEnum 




_Synapse's real DataAccessSubmissionState values, verified via Sage-Bionetworks/SynapseWebClient source (ACTDataAccessSubmissionWidget.java's exhaustive state switch) — the "sagebrain governance graph ACL_AR data - AR table schemas.csv" only says DATA_ACCESS_SUBMISSION_STATUS.STATE is TEXT, with no NOTES-column value list. Each value's meaning: is the gov: IRI scripts/build_governance_graph.py emits for gov:state (APPROVED is shared with ApprovalStateEnum -- see that enum)._



<div data-search-exclude markdown="1">

URI: [governanceduo:enum/SubmissionStateEnum](https://w3id.org/sage-bionetworks/governance-duo/enum/SubmissionStateEnum)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| SUBMITTED | sagegov:SUBMITTED |  |
| APPROVED | sagegov:APPROVED |  |
| REJECTED | sagegov:REJECTED |  |
| CANCELLED | sagegov:CANCELLED |  |




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
implements:
- owl:NamedIndividual
description: 'Synapse''s real DataAccessSubmissionState values, verified via Sage-Bionetworks/SynapseWebClient
  source (ACTDataAccessSubmissionWidget.java''s exhaustive state switch) — the "sagebrain
  governance graph ACL_AR data - AR table schemas.csv" only says DATA_ACCESS_SUBMISSION_STATUS.STATE
  is TEXT, with no NOTES-column value list. Each value''s meaning: is the gov: IRI
  scripts/build_governance_graph.py emits for gov:state (APPROVED is shared with ApprovalStateEnum
  -- see that enum).'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
permissible_values:
  SUBMITTED:
    text: SUBMITTED
    meaning: sagegov:SUBMITTED
  APPROVED:
    text: APPROVED
    meaning: sagegov:APPROVED
  REJECTED:
    text: REJECTED
    meaning: sagegov:REJECTED
  CANCELLED:
    text: CANCELLED
    meaning: sagegov:CANCELLED

```
</details>

</div>