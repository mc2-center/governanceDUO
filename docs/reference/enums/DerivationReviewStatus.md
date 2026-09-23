---
search:
  boost: 2.0
---


# Enum: DerivationReviewStatus 




_Where a DerivationReview stands._



<div data-search-exclude markdown="1">

URI: [gov:DerivationReviewStatus](https://w3id.org/synapse/governance#DerivationReviewStatus)

**Enum URI:** [gov:DerivationReviewStatus](https://w3id.org/synapse/governance#DerivationReviewStatus)


## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| Flagged | gov:DerivationFlagged | Minted automatically because a derivation rule or disjoint sourceAccessRequir... |
| Reviewed | gov:DerivationReviewed | A person has looked at this combination but not yet recorded a decision |
| Approved | gov:DerivationApproved | The combination was reviewed and judged safe to permit |
| Denied | gov:DerivationDenied | The combination was reviewed and judged unsafe; access to the derived output ... |













## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo






## LinkML Source

<details>
```yaml
name: DerivationReviewStatus
implements:
- skos:Concept
description: Where a DerivationReview stands.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
enum_uri: gov:DerivationReviewStatus
permissible_values:
  Flagged:
    text: Flagged
    description: Minted automatically because a derivation rule or disjoint sourceAccessRequirements
      need a person to look; not yet reviewed.
    meaning: gov:DerivationFlagged
  Reviewed:
    text: Reviewed
    description: A person has looked at this combination but not yet recorded a decision.
    meaning: gov:DerivationReviewed
  Approved:
    text: Approved
    description: The combination was reviewed and judged safe to permit.
    meaning: gov:DerivationApproved
  Denied:
    text: Denied
    description: The combination was reviewed and judged unsafe; access to the derived
      output should be blocked.
    meaning: gov:DerivationDenied

```
</details>

</div>