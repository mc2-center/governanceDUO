---
search:
  boost: 5.0
---

# Slot: institution 


_Institution/company name, verbatim from Synapse (ResearchProject.institution / DataAccessRequest.institution -- both real fields hold the same free-text shape as UserProfile.company above). On ResearchProject/DataAccessRequest, consumed by site_node_for() to derive a gov:affiliatedWith edge, not independently re-emitted; on Site itself, this is the node's own display name and IS emitted directly._



<div data-search-exclude markdown="1">



URI: [sagegov:institution](https://sagebionetworks.org/governance/institution)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ResearchProject](../classes/ResearchProject.md) | Documents the research context/justification behind a DataAccessRequest (and,... |  no  |
| [Site](../classes/Site.md) | An institution real Synapse data associates with a ResearchProject, DataAcces... |  no  |
| [DataAccessRequest](../classes/DataAccessRequest.md) | A user's draft/submitted request against an AccessRequirement, behind a DataA... |  no  |
| [IRBRequirement](../classes/IRBRequirement.md) | A site/program-specific instantiation of an AccessRequirementTemplate, per th... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](../types/String.md) |
| Domain Of | [ResearchProject](../classes/ResearchProject.md), [Site](../classes/Site.md), [DataAccessRequest](../classes/DataAccessRequest.md), [IRBRequirement](../classes/IRBRequirement.md) |
| Slot URI | [sagegov:institution](https://sagebionetworks.org/governance/institution) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sagegov:institution |
| native | governanceduo:institution |




## LinkML Source

<details>
```yaml
name: institution
description: Institution/company name, verbatim from Synapse (ResearchProject.institution
  / DataAccessRequest.institution -- both real fields hold the same free-text shape
  as UserProfile.company above). On ResearchProject/DataAccessRequest, consumed by
  site_node_for() to derive a gov:affiliatedWith edge, not independently re-emitted;
  on Site itself, this is the node's own display name and IS emitted directly.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: sagegov:institution
domain_of:
- ResearchProject
- Site
- DataAccessRequest
- IRBRequirement
range: string

```
</details></div>