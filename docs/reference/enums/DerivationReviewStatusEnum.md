---
search:
  boost: 2.0
---


# Enum: DerivationReviewStatusEnum 




_Workflow state of a DerivationReview — the same enum-per-workflow-state convention ApprovalStateEnum/SubmissionStateEnum already use in governance_graph.yaml, deliberately a distinct enum from both (do not conflate)._



<div data-search-exclude markdown="1">

URI: [governanceduo:enum/DerivationReviewStatusEnum](https://w3id.org/sage-bionetworks/governance-duo/enum/DerivationReviewStatusEnum)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| Flagged | None | Minted automatically (scripts/build_derivation_policy |
| Reviewed | None | A person has looked at this combination but not yet recorded a decision |
| Approved | None | The combination was reviewed and judged safe to permit |
| Denied | None | The combination was reviewed and judged unsafe; access to the derived output ... |




## Slots

| Name | Description |
| ---  | --- |
| [reviewStatus](../slots/reviewStatus.md) | This review's workflow state |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo






## LinkML Source

<details>
```yaml
name: DerivationReviewStatusEnum
description: Workflow state of a DerivationReview — the same enum-per-workflow-state
  convention ApprovalStateEnum/SubmissionStateEnum already use in governance_graph.yaml,
  deliberately a distinct enum from both (do not conflate).
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
permissible_values:
  Flagged:
    text: Flagged
    description: Minted automatically (scripts/build_derivation_policy.py) because
      the source Activity's inputs carry disjoint sourceAccessRequirements sets —
      not yet looked at by a person.
  Reviewed:
    text: Reviewed
    description: A person has looked at this combination but not yet recorded a decision.
  Approved:
    text: Approved
    description: The combination was reviewed and judged safe to permit.
  Denied:
    text: Denied
    description: The combination was reviewed and judged unsafe; access to the derived
      output should be blocked.

```
</details>

</div>