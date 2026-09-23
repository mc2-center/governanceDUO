---
search:
  boost: 2.0
---


# Enum: Permission 




_A Synapse ACCESS_TYPE (org.sagebionetworks.repo.model.ACCESS_TYPE), as a Web Access Control access mode. Each value is also rdfs:subClassOf the WAC mode it amounts to (acl:Read, acl:Write, acl:Append, acl:Control), or of acl:Access when it has no WAC counterpart. The authorizer's derived ACCESS action isn't a value here; the authorizer_v1 projection derives it._



<div data-search-exclude markdown="1">

URI: [gov:Permission](https://w3id.org/synapse/governance#Permission)

**Enum URI:** [gov:Permission](https://w3id.org/synapse/governance#Permission)


## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| CREATE | gov:Create | Permission to create a new entity or resource |
| READ | gov:Read | Permission to read or view the entity or resource |
| UPDATE | gov:Update | Permission to modify or update the entity or resource |
| DELETE | gov:Delete | Permission to delete the entity or resource |
| CHANGE_PERMISSIONS | gov:ChangePermissions | Permission to change access permissions for the entity or resource |
| DOWNLOAD | gov:Download | Permission to download files or data from the entity or resource |
| UPLOAD | gov:Upload | Deprecated; adding this to an ACL has no effect |
| PARTICIPATE | gov:Participate | Permission to participate in activities related to the entity, such as discus... |
| SUBMIT | gov:Submit | Permission to submit content or data to the entity or resource |
| READ_PRIVATE_SUBMISSION | gov:ReadPrivateSubmission | Permission to read private submissions associated with the entity |
| UPDATE_SUBMISSION | gov:UpdateSubmission | Permission to update or modify a submission |
| DELETE_SUBMISSION | gov:DeleteSubmission | Permission to delete a submission |
| TEAM_MEMBERSHIP_UPDATE | gov:TeamMembershipUpdate | Permission to update team membership, such as adding or removing members |
| SEND_MESSAGE | gov:SendMessage | Permission to send messages related to the entity or resource |
| CHANGE_SETTINGS | gov:ChangeSettings | Permission to change settings or configuration for the entity or resource |
| MODERATE | gov:Moderate | Permission to moderate content or activity related to the entity or resource |
| REVIEW_SUBMISSIONS | gov:ReviewSubmissions | Enables reviewing submission groups (e |
| EXEMPTION_ELIGIBLE | gov:ExemptionEligible | Qualifies for exemption when granted on Access Requirement ACLs |




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
name: Permission
implements:
- skos:Concept
description: A Synapse ACCESS_TYPE (org.sagebionetworks.repo.model.ACCESS_TYPE), as
  a Web Access Control access mode. Each value is also rdfs:subClassOf the WAC mode
  it amounts to (acl:Read, acl:Write, acl:Append, acl:Control), or of acl:Access when
  it has no WAC counterpart. The authorizer's derived ACCESS action isn't a value
  here; the authorizer_v1 projection derives it.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
enum_uri: gov:Permission
permissible_values:
  CREATE:
    text: CREATE
    description: Permission to create a new entity or resource.
    meaning: gov:Create
    implements:
    - acl:Write
  READ:
    text: READ
    description: Permission to read or view the entity or resource.
    meaning: gov:Read
    implements:
    - acl:Read
  UPDATE:
    text: UPDATE
    description: Permission to modify or update the entity or resource.
    meaning: gov:Update
    implements:
    - acl:Write
  DELETE:
    text: DELETE
    description: Permission to delete the entity or resource.
    meaning: gov:Delete
    implements:
    - acl:Write
  CHANGE_PERMISSIONS:
    text: CHANGE_PERMISSIONS
    description: Permission to change access permissions for the entity or resource.
    meaning: gov:ChangePermissions
    implements:
    - acl:Control
  DOWNLOAD:
    text: DOWNLOAD
    description: Permission to download files or data from the entity or resource.
    meaning: gov:Download
    implements:
    - acl:Read
  UPLOAD:
    text: UPLOAD
    description: Deprecated; adding this to an ACL has no effect.
    meaning: gov:Upload
    implements:
    - acl:Append
  PARTICIPATE:
    text: PARTICIPATE
    description: Permission to participate in activities related to the entity, such
      as discussions or challenges.
    meaning: gov:Participate
    implements:
    - acl:Access
  SUBMIT:
    text: SUBMIT
    description: Permission to submit content or data to the entity or resource.
    meaning: gov:Submit
    implements:
    - acl:Access
  READ_PRIVATE_SUBMISSION:
    text: READ_PRIVATE_SUBMISSION
    description: Permission to read private submissions associated with the entity.
    meaning: gov:ReadPrivateSubmission
    implements:
    - acl:Access
  UPDATE_SUBMISSION:
    text: UPDATE_SUBMISSION
    description: Permission to update or modify a submission.
    meaning: gov:UpdateSubmission
    implements:
    - acl:Access
  DELETE_SUBMISSION:
    text: DELETE_SUBMISSION
    description: Permission to delete a submission.
    meaning: gov:DeleteSubmission
    implements:
    - acl:Access
  TEAM_MEMBERSHIP_UPDATE:
    text: TEAM_MEMBERSHIP_UPDATE
    description: Permission to update team membership, such as adding or removing
      members.
    meaning: gov:TeamMembershipUpdate
    implements:
    - acl:Access
  SEND_MESSAGE:
    text: SEND_MESSAGE
    description: Permission to send messages related to the entity or resource.
    meaning: gov:SendMessage
    implements:
    - acl:Access
  CHANGE_SETTINGS:
    text: CHANGE_SETTINGS
    description: Permission to change settings or configuration for the entity or
      resource.
    meaning: gov:ChangeSettings
    implements:
    - acl:Access
  MODERATE:
    text: MODERATE
    description: Permission to moderate content or activity related to the entity
      or resource.
    meaning: gov:Moderate
    implements:
    - acl:Access
  REVIEW_SUBMISSIONS:
    text: REVIEW_SUBMISSIONS
    description: Enables reviewing submission groups (e.g., on Access Requirements)
      for specified objects.
    meaning: gov:ReviewSubmissions
    implements:
    - acl:Access
  EXEMPTION_ELIGIBLE:
    text: EXEMPTION_ELIGIBLE
    description: Qualifies for exemption when granted on Access Requirement ACLs.
    meaning: gov:ExemptionEligible
    implements:
    - acl:Access

```
</details>

</div>