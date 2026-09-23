---
search:
  boost: 2.0
---


# Enum: AccessTypeEnum 




_Synapse's real ACCESS_TYPE values, verified live via rest-docs.synapse.org (not inferred from the "sagebrain governance graph ACL_AR data" CSVs alone, which only name a handful of these as examples in a free-text NOTES column). Shared by AccessGrant.permission (an ACL grant's permission — ACL_RESOURCE_ACCESS_TYPE.STRING_ELE) in governance_graph.yaml and this file's own accessType slot (ACCESS_REQUIREMENT.ACCESS_TYPE) — the same underlying Synapse type in both places. Each value's meaning: is the gov: IRI scripts/build_governance_graph.py emits for gov:permission._



<div data-search-exclude markdown="1">

URI: [governanceduo:enum/AccessTypeEnum](https://w3id.org/sage-bionetworks/governance-duo/enum/AccessTypeEnum)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| CREATE | sagegov:CREATE | Permission to create a new entity or resource |
| READ | sagegov:READ | Permission to read or view the entity or resource |
| UPDATE | sagegov:UPDATE | Permission to modify or update the entity or resource |
| DELETE | sagegov:DELETE | Permission to delete the entity or resource |
| CHANGE_PERMISSIONS | sagegov:CHANGE_PERMISSIONS | Permission to change access permissions for the entity or resource |
| DOWNLOAD | sagegov:DOWNLOAD | Permission to download files or data from the entity or resource |
| UPLOAD | sagegov:UPLOAD | Deprecated; adding this to an ACL has no effect |
| PARTICIPATE | sagegov:PARTICIPATE | Permission to participate in activities related to the entity, such as discus... |
| SUBMIT | sagegov:SUBMIT | Permission to submit content or data to the entity or resource |
| READ_PRIVATE_SUBMISSION | sagegov:READ_PRIVATE_SUBMISSION | Permission to read private submissions associated with the entity |
| UPDATE_SUBMISSION | sagegov:UPDATE_SUBMISSION | Permission to update or modify a submission |
| DELETE_SUBMISSION | sagegov:DELETE_SUBMISSION | Permission to delete a submission |
| TEAM_MEMBERSHIP_UPDATE | sagegov:TEAM_MEMBERSHIP_UPDATE | Permission to update team membership, such as adding or removing members |
| SEND_MESSAGE | sagegov:SEND_MESSAGE | Permission to send messages related to the entity or resource |
| CHANGE_SETTINGS | sagegov:CHANGE_SETTINGS | Permission to change settings or configuration for the entity or resource |
| MODERATE | sagegov:MODERATE | Permission to moderate content or activity related to the entity or resource |
| REVIEW_SUBMISSIONS | sagegov:REVIEW_SUBMISSIONS | Enables reviewing submission groups (e |
| EXEMPTION_ELIGIBLE | sagegov:EXEMPTION_ELIGIBLE | Qualifies for exemption when granted on Access Requirement ACLs |




## Slots

| Name | Description |
| ---  | --- |
| [accessType](../slots/accessType.md) | The kind of access this Access Requirement governs (ACCESS_REQUIREMENT |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo






## LinkML Source

<details>
```yaml
name: AccessTypeEnum
implements:
- owl:NamedIndividual
description: 'Synapse''s real ACCESS_TYPE values, verified live via rest-docs.synapse.org
  (not inferred from the "sagebrain governance graph ACL_AR data" CSVs alone, which
  only name a handful of these as examples in a free-text NOTES column). Shared by
  AccessGrant.permission (an ACL grant''s permission — ACL_RESOURCE_ACCESS_TYPE.STRING_ELE)
  in governance_graph.yaml and this file''s own accessType slot (ACCESS_REQUIREMENT.ACCESS_TYPE)
  — the same underlying Synapse type in both places. Each value''s meaning: is the
  gov: IRI scripts/build_governance_graph.py emits for gov:permission.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
permissible_values:
  CREATE:
    text: CREATE
    description: Permission to create a new entity or resource.
    meaning: sagegov:CREATE
  READ:
    text: READ
    description: Permission to read or view the entity or resource.
    meaning: sagegov:READ
  UPDATE:
    text: UPDATE
    description: Permission to modify or update the entity or resource.
    meaning: sagegov:UPDATE
  DELETE:
    text: DELETE
    description: Permission to delete the entity or resource.
    meaning: sagegov:DELETE
  CHANGE_PERMISSIONS:
    text: CHANGE_PERMISSIONS
    description: Permission to change access permissions for the entity or resource.
    meaning: sagegov:CHANGE_PERMISSIONS
  DOWNLOAD:
    text: DOWNLOAD
    description: Permission to download files or data from the entity or resource.
    meaning: sagegov:DOWNLOAD
  UPLOAD:
    text: UPLOAD
    description: Deprecated; adding this to an ACL has no effect.
    meaning: sagegov:UPLOAD
    annotations:
      deprecated:
        tag: deprecated
        value: true
  PARTICIPATE:
    text: PARTICIPATE
    description: Permission to participate in activities related to the entity, such
      as discussions or challenges.
    meaning: sagegov:PARTICIPATE
  SUBMIT:
    text: SUBMIT
    description: Permission to submit content or data to the entity or resource.
    meaning: sagegov:SUBMIT
  READ_PRIVATE_SUBMISSION:
    text: READ_PRIVATE_SUBMISSION
    description: Permission to read private submissions associated with the entity.
    meaning: sagegov:READ_PRIVATE_SUBMISSION
  UPDATE_SUBMISSION:
    text: UPDATE_SUBMISSION
    description: Permission to update or modify a submission.
    meaning: sagegov:UPDATE_SUBMISSION
  DELETE_SUBMISSION:
    text: DELETE_SUBMISSION
    description: Permission to delete a submission.
    meaning: sagegov:DELETE_SUBMISSION
  TEAM_MEMBERSHIP_UPDATE:
    text: TEAM_MEMBERSHIP_UPDATE
    description: Permission to update team membership, such as adding or removing
      members.
    meaning: sagegov:TEAM_MEMBERSHIP_UPDATE
  SEND_MESSAGE:
    text: SEND_MESSAGE
    description: Permission to send messages related to the entity or resource.
    meaning: sagegov:SEND_MESSAGE
  CHANGE_SETTINGS:
    text: CHANGE_SETTINGS
    description: Permission to change settings or configuration for the entity or
      resource.
    meaning: sagegov:CHANGE_SETTINGS
  MODERATE:
    text: MODERATE
    description: Permission to moderate content or activity related to the entity
      or resource.
    meaning: sagegov:MODERATE
  REVIEW_SUBMISSIONS:
    text: REVIEW_SUBMISSIONS
    description: Enables reviewing submission groups (e.g., on Access Requirements)
      for specified objects.
    meaning: sagegov:REVIEW_SUBMISSIONS
  EXEMPTION_ELIGIBLE:
    text: EXEMPTION_ELIGIBLE
    description: Qualifies for exemption when granted on Access Requirement ACLs.
    meaning: sagegov:EXEMPTION_ELIGIBLE

```
</details>

</div>