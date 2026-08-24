---
search:
  boost: 2.0
---


# Enum: DeidentificationTypeEnum 




_De-identification method categories. Shared by Study.studyDeidentificationType and the shared/GovernanceMixin deidentificationType slot (DUOPlus3) — the source CSV duplicated this same value list under both attributes; this schema keeps one enum and points both slots at it._



<div data-search-exclude markdown="1">

URI: [governanceduo:enum/DeidentificationTypeEnum](https://w3id.org/sage-bionetworks/governance-duo/enum/DeidentificationTypeEnum)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| HIPPA_LDS | None | Data is de-identified according to the HIPAA Limited Data Set (LDS) standard |
| SafeHarbor | None | Data is de-identified according to the Safe Harbor standard |
| ExpertDetermination | None | Data is de-identified according to the Expert Determination standard |
| Pseudonymized | None | Data is pseudonymized, meaning that identifying information has been removed ... |
| Anonymized | None | Data is anonymized, meaning that it cannot be used to identify individuals |
| Other | None | Data is de-identified according to a different standard |




## Slots

| Name | Description |
| ---  | --- |
| [deidentificationType](../slots/deidentificationType.md) | The type of de-identification applied to the data associated with the access ... |
| [studyDeidentificationType](../slots/studyDeidentificationType.md) | General description of the de-identification method |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo






## LinkML Source

<details>
```yaml
name: DeidentificationTypeEnum
description: De-identification method categories. Shared by Study.studyDeidentificationType
  and the shared/GovernanceMixin deidentificationType slot (DUOPlus3) — the source
  CSV duplicated this same value list under both attributes; this schema keeps one
  enum and points both slots at it.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
permissible_values:
  HIPPA_LDS:
    text: HIPPA_LDS
    description: Data is de-identified according to the HIPAA Limited Data Set (LDS)
      standard.
  SafeHarbor:
    text: SafeHarbor
    description: Data is de-identified according to the Safe Harbor standard.
  ExpertDetermination:
    text: ExpertDetermination
    description: Data is de-identified according to the Expert Determination standard.
  Pseudonymized:
    text: Pseudonymized
    description: Data is pseudonymized, meaning that identifying information has been
      removed or replaced with pseudonyms.
  Anonymized:
    text: Anonymized
    description: Data is anonymized, meaning that it cannot be used to identify individuals.
  Other:
    text: Other
    description: Data is de-identified according to a different standard.

```
</details>

</div>