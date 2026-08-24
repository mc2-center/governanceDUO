---
search:
  boost: 5.0
---

# Slot: bindings 

<div data-search-exclude markdown="1">



URI: [governanceduo:slot/bindings](https://w3id.org/sage-bionetworks/governance-duo/slot/bindings)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PolicyCardBindingCollection](../classes/PolicyCardBindingCollection.md) | Container class for policy_fabric_bindings |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [PolicyCardBinding](../classes/PolicyCardBinding.md) |
| Domain Of | [PolicyCardBindingCollection](../classes/PolicyCardBindingCollection.md) |

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
| self | governanceduo:bindings |
| native | governanceduo:bindings |




## LinkML Source

<details>
```yaml
name: bindings
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
domain_of:
- PolicyCardBindingCollection
range: PolicyCardBinding
multivalued: true
inlined: true
inlined_as_list: true

```
</details></div>