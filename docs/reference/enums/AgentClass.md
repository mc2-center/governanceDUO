---
search:
  boost: 2.0
---


# Enum: AgentClass 




_Web Access Control agent classes, for Synapse's group principals that stand for everyone rather than for listed members._



<div data-search-exclude markdown="1">

URI: [governanceduo:enum/AgentClass](https://w3id.org/sage-bionetworks/governance-duo/enum/AgentClass)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| PUBLIC | foaf:Agent | Anyone, signed in or not (Synapse's PUBLIC group, 273949) |
| AUTHENTICATED_USERS | acl:AuthenticatedAgent | Any signed-in Synapse user (Synapse's AUTHENTICATED_USERS group, 273948) |













## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo






## LinkML Source

<details>
```yaml
name: AgentClass
implements:
- owl:Class
description: Web Access Control agent classes, for Synapse's group principals that
  stand for everyone rather than for listed members.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
permissible_values:
  PUBLIC:
    text: PUBLIC
    description: Anyone, signed in or not (Synapse's PUBLIC group, 273949).
    meaning: foaf:Agent
  AUTHENTICATED_USERS:
    text: AUTHENTICATED_USERS
    description: Any signed-in Synapse user (Synapse's AUTHENTICATED_USERS group,
      273948).
    meaning: acl:AuthenticatedAgent

```
</details>

</div>