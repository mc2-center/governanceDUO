---
search:
  boost: 2.0
---


# Enum: AccessTypeEnum 




_Synapse's real ACCESS_TYPE values, verified live via rest-docs.synapse.org (not inferred from the "sagebrain governance graph ACL_AR data" CSVs alone, which only name a handful of these as examples in a free-text NOTES column). Shared by AccessGrant.permission (an ACL grant's permission — ACL_RESOURCE_ACCESS_TYPE.STRING_ELE) in governance_graph.yaml and this file's own accessType slot (ACCESS_REQUIREMENT.ACCESS_TYPE) — the same underlying Synapse type in both places._



<div data-search-exclude markdown="1">

URI: [governanceduo:enum/AccessTypeEnum](https://w3id.org/sage-bionetworks/governance-duo/enum/AccessTypeEnum)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| CREATE | None | Permission to create a new entity or resource |
| READ | None | Permission to read or view the entity or resource |
| UPDATE | None | Permission to modify or update the entity or resource |
| DELETE | None | Permission to delete the entity or resource |
| CHANGE_PERMISSIONS | None | Permission to change access permissions for the entity or resource |
| DOWNLOAD | None | Permission to download files or data from the entity or resource |
| UPLOAD | None | Deprecated; adding this to an ACL has no effect |
| PARTICIPATE | None | Permission to participate in activities related to the entity, such as discus... |
| SUBMIT | None | Permission to submit content or data to the entity or resource |
| READ_PRIVATE_SUBMISSION | None | Permission to read private submissions associated with the entity |
| UPDATE_SUBMISSION | None | Permission to update or modify a submission |
| DELETE_SUBMISSION | None | Permission to delete a submission |
| TEAM_MEMBERSHIP_UPDATE | None | Permission to update team membership, such as adding or removing members |
| SEND_MESSAGE | None | Permission to send messages related to the entity or resource |
| CHANGE_SETTINGS | None | Permission to change settings or configuration for the entity or resource |
| MODERATE | None | Permission to moderate content or activity related to the entity or resource |
| REVIEW_SUBMISSIONS | None | Enables reviewing submission groups (e |
| EXEMPTION_ELIGIBLE | None | Qualifies for exemption when granted on Access Requirement ACLs |




## Slots

| Name | Description |
| ---  | --- |
| [accessType](../slots/accessType.md) | The kind of access this Access Requirement governs (ACCESS_REQUIREMENT |
| [permission](../slots/permission.md) | The permission(s) granted (ACL_RESOURCE_ACCESS_TYPE |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo






## LinkML Source

<details>
```yaml
name: AccessTypeEnum
description: Synapse's real ACCESS_TYPE values, verified live via rest-docs.synapse.org
  (not inferred from the "sagebrain governance graph ACL_AR data" CSVs alone, which
  only name a handful of these as examples in a free-text NOTES column). Shared by
  AccessGrant.permission (an ACL grant's permission — ACL_RESOURCE_ACCESS_TYPE.STRING_ELE)
  in governance_graph.yaml and this file's own accessType slot (ACCESS_REQUIREMENT.ACCESS_TYPE)
  — the same underlying Synapse type in both places.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
permissible_values:
  CREATE:
    text: CREATE
    description: Permission to create a new entity or resource.
  READ:
    text: READ
    description: Permission to read or view the entity or resource.
  UPDATE:
    text: UPDATE
    description: Permission to modify or update the entity or resource.
  DELETE:
    text: DELETE
    description: Permission to delete the entity or resource.
  CHANGE_PERMISSIONS:
    text: CHANGE_PERMISSIONS
    description: Permission to change access permissions for the entity or resource.
  DOWNLOAD:
    text: DOWNLOAD
    description: Permission to download files or data from the entity or resource.
  UPLOAD:
    text: UPLOAD
    description: Deprecated; adding this to an ACL has no effect.
    annotations:
      deprecated:
        tag: deprecated
        value: true
  PARTICIPATE:
    text: PARTICIPATE
    description: Permission to participate in activities related to the entity, such
      as discussions or challenges.
  SUBMIT:
    text: SUBMIT
    description: Permission to submit content or data to the entity or resource.
  READ_PRIVATE_SUBMISSION:
    text: READ_PRIVATE_SUBMISSION
    description: Permission to read private submissions associated with the entity.
  UPDATE_SUBMISSION:
    text: UPDATE_SUBMISSION
    description: Permission to update or modify a submission.
  DELETE_SUBMISSION:
    text: DELETE_SUBMISSION
    description: Permission to delete a submission.
  TEAM_MEMBERSHIP_UPDATE:
    text: TEAM_MEMBERSHIP_UPDATE
    description: Permission to update team membership, such as adding or removing
      members.
  SEND_MESSAGE:
    text: SEND_MESSAGE
    description: Permission to send messages related to the entity or resource.
  CHANGE_SETTINGS:
    text: CHANGE_SETTINGS
    description: Permission to change settings or configuration for the entity or
      resource.
  MODERATE:
    text: MODERATE
    description: Permission to moderate content or activity related to the entity
      or resource.
  REVIEW_SUBMISSIONS:
    text: REVIEW_SUBMISSIONS
    description: Enables reviewing submission groups (e.g., on Access Requirements)
      for specified objects.
  EXEMPTION_ELIGIBLE:
    text: EXEMPTION_ELIGIBLE
    description: Qualifies for exemption when granted on Access Requirement ACLs.

```
</details>

</div>