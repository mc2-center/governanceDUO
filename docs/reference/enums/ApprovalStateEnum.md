---
search:
  boost: 2.0
---


# Enum: ApprovalStateEnum 




_Synapse's real AccessApproval state values (org.sagebionetworks.repo.model.ApprovalState), verified directly against the OpenAPI spec -- APPROVED/REVOKED only. A distinct, smaller enum from SubmissionStateEnum above. Each value's meaning: is the gov: IRI scripts/build_governance_graph.py emits for gov:status. The two enums' APPROVED share one IRI, gov:APPROVED, as the graph has always written it; the predicate (gov:status on an AccessApproval, gov:state on a DataAccessSubmission) tells them apart. Should they ever need different definitions, or the enums be declared disjoint, APPROVED needs a distinct IRI per enum (plans/enum_values_match_owl.md)._



<div data-search-exclude markdown="1">

URI: [governanceduo:enum/ApprovalStateEnum](https://w3id.org/sage-bionetworks/governance-duo/enum/ApprovalStateEnum)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| APPROVED | sagegov:APPROVED |  |
| REVOKED | sagegov:REVOKED |  |




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
description: 'Synapse''s real AccessApproval state values (org.sagebionetworks.repo.model.ApprovalState),
  verified directly against the OpenAPI spec -- APPROVED/REVOKED only. A distinct,
  smaller enum from SubmissionStateEnum above. Each value''s meaning: is the gov:
  IRI scripts/build_governance_graph.py emits for gov:status. The two enums'' APPROVED
  share one IRI, gov:APPROVED, as the graph has always written it; the predicate (gov:status
  on an AccessApproval, gov:state on a DataAccessSubmission) tells them apart. Should
  they ever need different definitions, or the enums be declared disjoint, APPROVED
  needs a distinct IRI per enum (plans/enum_values_match_owl.md).'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
permissible_values:
  APPROVED:
    text: APPROVED
    meaning: sagegov:APPROVED
  REVOKED:
    text: REVOKED
    meaning: sagegov:REVOKED

```
</details>

</div>