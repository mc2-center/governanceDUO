---
search:
  boost: 2.0
---


# Enum: SubmissionState 




_A DataAccessSubmission's state (DataAccessSubmissionState), verified against SynapseWebClient's ACTDataAccessSubmissionWidget._



<div data-search-exclude markdown="1">

URI: [gov:SubmissionState](https://w3id.org/synapse/governance#SubmissionState)

**Enum URI:** [gov:SubmissionState](https://w3id.org/synapse/governance#SubmissionState)


## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| SUBMITTED | gov:Submitted | Submitted and awaiting review |
| APPROVED | gov:Approved | Approved |
| REJECTED | gov:Rejected | Reviewed and rejected |
| CANCELLED | gov:Cancelled | Cancelled by the submitter |













## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo






## LinkML Source

<details>
```yaml
name: SubmissionState
implements:
- skos:Concept
description: A DataAccessSubmission's state (DataAccessSubmissionState), verified
  against SynapseWebClient's ACTDataAccessSubmissionWidget.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
enum_uri: gov:SubmissionState
permissible_values:
  SUBMITTED:
    text: SUBMITTED
    description: Submitted and awaiting review.
    meaning: gov:Submitted
  APPROVED:
    text: APPROVED
    description: Approved. One concept in both the ApprovalStatus and SubmissionState
      schemes.
    meaning: gov:Approved
  REJECTED:
    text: REJECTED
    description: Reviewed and rejected.
    meaning: gov:Rejected
  CANCELLED:
    text: CANCELLED
    description: Cancelled by the submitter.
    meaning: gov:Cancelled

```
</details>

</div>