---
search:
  boost: 5.0
---

# Slot: generated 


_The SynapseEntities this Activity produced, as syn: CURIEs. Multivalued: Synapse lets one Activity be the generatedBy of several entities (GET /activity/{id}/generated returns a paginated list; PUT /entity/{id}/generatedBy?generatedBy=<activityId> attaches an existing Activity to another entity -- both confirmed against Synapse's OpenAPI spec). range is the untyped uriorcurie, not SynapseEntity itself — see this schema's own description for why (the referenced individual is never asserted in this schema's own example-rdf ABox). The value is an IRI node, so the OWL types this slot owl:ObjectProperty, as W3C PROV-O does._



<div data-search-exclude markdown="1">



URI: [prov:generated](http://www.w3.org/ns/prov#generated)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Activity](../classes/Activity.md) | Mirrors Synapse's real Activity object (org |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Uriorcurie](../types/Uriorcurie.md) |
| Domain Of | [Activity](../classes/Activity.md) |
| Slot URI | [prov:generated](http://www.w3.org/ns/prov#generated) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | prov:generated |
| native | governanceduo:generated |




## LinkML Source

<details>
```yaml
name: generated
description: 'The SynapseEntities this Activity produced, as syn: CURIEs. Multivalued:
  Synapse lets one Activity be the generatedBy of several entities (GET /activity/{id}/generated
  returns a paginated list; PUT /entity/{id}/generatedBy?generatedBy=<activityId>
  attaches an existing Activity to another entity -- both confirmed against Synapse''s
  OpenAPI spec). range is the untyped uriorcurie, not SynapseEntity itself — see this
  schema''s own description for why (the referenced individual is never asserted in
  this schema''s own example-rdf ABox). The value is an IRI node, so the OWL types
  this slot owl:ObjectProperty, as W3C PROV-O does.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
slot_uri: prov:generated
domain_of:
- Activity
range: uriorcurie
multivalued: true

```
</details></div>