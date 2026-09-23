---
search:
  boost: 2.0
---


# Enum: DataUseTerm 




_A Data Use Ontology term, or a Sage-local extension of DUO's data use modifier (DUO:0000017). DUO:0000017 itself is not a value: a condition names a specific term._



<div data-search-exclude markdown="1">

URI: [governanceduo:enum/DataUseTerm](https://w3id.org/sage-bionetworks/governance-duo/enum/DataUseTerm)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| DUO:0000042 | DUO:0000042 | General Research Use - This data use permission indicates that use is allowed... |
| DUO:0000027 | DUO:0000027 | Project Specific Restriction - This data use modifier indicates that use is l... |
| DUO:0000016 | DUO:0000016 | Genetic Studies Only - This data use modifier indicates that use is limited t... |
| DUO:0000029 | DUO:0000029 | Return to Database or Resource - This data use modifier indicates that the re... |
| DUO:0000043 | DUO:0000043 | Clinical Care Use - This data use modifier indicates that use is allowed for ... |
| DUO:0000015 | DUO:0000015 | No General Methods Research - This data use modifier indicates that use does ... |
| DUO:0000004 | DUO:0000004 | No Restriction - This data use permission indicates there is no restriction o... |
| DUO:0000045 | DUO:0000045 | Not-for-Profit Organisation Use Only - This data use modifier indicates that ... |
| DUO:0000011 | DUO:0000011 | Population Origins or Ancestry Research Only - This data use permission indic... |
| DUO:0000046 | DUO:0000046 | Non-Commercial Use Only - This data use modifier indicates that use of the da... |
| DUO:0000018 | DUO:0000018 | Not-for-Profit, Non-Commercial Use Only - This data use modifier indicates th... |
| DUO:0000044 | DUO:0000044 | Population Origins or Ancestry Research Prohibited - This data use modifier i... |
| DUO:0000021 | DUO:0000021 | Ethics Approval Required - This data use modifier indicates that the requesto... |
| DUO:0000006 | DUO:0000006 | Health or Medical or Biomedical Research - This data use permission indicates... |
| DUO:0000019 | DUO:0000019 | Publication Required - This data use modifier indicates that requestor agrees... |
| DUO:0000026 | DUO:0000026 | User Specific Restriction - This data use modifier indicates that use is limi... |
| DUO:0000020 | DUO:0000020 | Collaboration Required - This data use modifier indicates that the requestor ... |
| DUO:0000012 | DUO:0000012 | Research Specific Restrictions - This data use modifier indicates that use is... |
| DUO:0000025 | DUO:0000025 | Time Limit on Use - This data use modifier indicates that use is approved for... |
| DUO:0000024 | DUO:0000024 | Publication Moratorium - This data use modifier indicates that requestor agre... |
| DUO:0000028 | DUO:0000028 | Institution Specific Restriction - This data use modifier indicates that use ... |
| DUO:0000022 | DUO:0000022 | Geographical Restriction - This data use modifier indicates that use is limit... |
| DUO:0000007 | DUO:0000007 | Disease Specific Research - This data use permission indicates that use is al... |
| DUOPlus1 | gov:DUOPlus1 | Source geography is relevant to governance decisions |
| DUOPlus2 | gov:DUOPlus2 | Study population is relevant to governance decisions |
| DUOPlus3 | gov:DUOPlus3 | Data deidentification is relevant to governance decisions |
| DUOPlus4 | gov:DUOPlus4 | A data permission designation is associated with the Study |
| DUOPlus5 | gov:DUOPlus5 | A data tier designation is associated with the Study |
| DUOPlus6 | gov:DUOPlus6 | A license is associated with the Study |
| DUOPlus7 | gov:DUOPlus7 | Attribution conditions are associated with this Study |













## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo






## LinkML Source

<details>
```yaml
name: DataUseTerm
implements:
- owl:Class
description: 'A Data Use Ontology term, or a Sage-local extension of DUO''s data use
  modifier (DUO:0000017). DUO:0000017 itself is not a value: a condition names a specific
  term.'
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
permissible_values:
  DUO:0000042:
    text: DUO:0000042
    description: General Research Use - This data use permission indicates that use
      is allowed for general research use for any research purpose.
    meaning: DUO:0000042
  DUO:0000027:
    text: DUO:0000027
    description: Project Specific Restriction - This data use modifier indicates that
      use is limited to use within an approved project.
    meaning: DUO:0000027
  DUO:0000016:
    text: DUO:0000016
    description: Genetic Studies Only - This data use modifier indicates that use
      is limited to genetic studies only (i.e., studies that include genotype research
      alone or both genotype and phenotype research, but not phenotype research exclusively)
    meaning: DUO:0000016
  DUO:0000029:
    text: DUO:0000029
    description: Return to Database or Resource - This data use modifier indicates
      that the requestor must return derived/enriched data to the database/resource.
    meaning: DUO:0000029
  DUO:0000043:
    text: DUO:0000043
    description: Clinical Care Use - This data use modifier indicates that use is
      allowed for clinical use and care.
    meaning: DUO:0000043
  DUO:0000015:
    text: DUO:0000015
    description: No General Methods Research - This data use modifier indicates that
      use does not allow methods development research (e.g., development of software
      or algorithms).
    meaning: DUO:0000015
  DUO:0000004:
    text: DUO:0000004
    description: No Restriction - This data use permission indicates there is no restriction
      on use.
    meaning: DUO:0000004
  DUO:0000045:
    text: DUO:0000045
    description: Not-for-Profit Organisation Use Only - This data use modifier indicates
      that use of the data is limited to not-for-profit organizations.
    meaning: DUO:0000045
  DUO:0000011:
    text: DUO:0000011
    description: Population Origins or Ancestry Research Only - This data use permission
      indicates that use of the data is limited to the study of population origins
      or ancestry.
    meaning: DUO:0000011
  DUO:0000046:
    text: DUO:0000046
    description: Non-Commercial Use Only - This data use modifier indicates that use
      of the data is limited to not-for-profit use.
    meaning: DUO:0000046
  DUO:0000018:
    text: DUO:0000018
    description: Not-for-Profit, Non-Commercial Use Only - This data use modifier
      indicates that use of the data is limited to not-for-profit organizations and
      not-for-profit use, non-commercial use.
    meaning: DUO:0000018
  DUO:0000044:
    text: DUO:0000044
    description: Population Origins or Ancestry Research Prohibited - This data use
      modifier indicates use for purposes of population, origin, or ancestry research
      is prohibited.
    meaning: DUO:0000044
  DUO:0000021:
    text: DUO:0000021
    description: Ethics Approval Required - This data use modifier indicates that
      the requestor must provide documentation of local IRB/ERB approval.
    meaning: DUO:0000021
  DUO:0000006:
    text: DUO:0000006
    description: Health or Medical or Biomedical Research - This data use permission
      indicates that use is allowed for health/medical/biomedical purposes; does not
      include the study of population origins or ancestry.
    meaning: DUO:0000006
  DUO:0000019:
    text: DUO:0000019
    description: Publication Required - This data use modifier indicates that requestor
      agrees to make results of studies using the data available to the larger scientific
      community.
    meaning: DUO:0000019
  DUO:0000026:
    text: DUO:0000026
    description: User Specific Restriction - This data use modifier indicates that
      use is limited to use by approved users. If providing this term, please describe
      the restrictions in column userSpecificRestriction.
    meaning: DUO:0000026
  DUO:0000020:
    text: DUO:0000020
    description: Collaboration Required - This data use modifier indicates that the
      requestor must agree to collaboration with the primary study investigator(s).
      If providing this term, please note the contact email in column collaborationRequired.
    meaning: DUO:0000020
  DUO:0000012:
    text: DUO:0000012
    description: Research Specific Restrictions - This data use modifier indicates
      that use is limited to studies of a certain research type. If providing this
      term, please note the research type(s) in column researchSpecificRestrictions.
    meaning: DUO:0000012
  DUO:0000025:
    text: DUO:0000025
    description: Time Limit on Use - This data use modifier indicates that use is
      approved for a specific number of months. If providing this term, please provide
      the number of months in column timeLimitOnUse.
    meaning: DUO:0000025
  DUO:0000024:
    text: DUO:0000024
    description: Publication Moratorium - This data use modifier indicates that requestor
      agrees not to publish results of studies until a specific date. If providing
      this term, please provide the date in column publicationMoratorium.
    meaning: DUO:0000024
  DUO:0000028:
    text: DUO:0000028
    description: Institution Specific Restriction - This data use modifier indicates
      that use is limited to use within an approved institution. If providing this
      term, please provide the institution ROR ID(s) in column institutionSpecificRestriction.
    meaning: DUO:0000028
  DUO:0000022:
    text: DUO:0000022
    description: Geographical Restriction - This data use modifier indicates that
      use is limited to within a specific geographic region. If providing this term,
      please provide the applicable country code(s) in column geographicalRestriction.
    meaning: DUO:0000022
  DUO:0000007:
    text: DUO:0000007
    description: Disease Specific Research - This data use permission indicates that
      use is allowed provided it is related to the specified disease. If providing
      this term, please provide the disease MONDO ID(s) in column diseaseSpecificResearch.
    meaning: DUO:0000007
  DUOPlus1:
    text: DUOPlus1
    description: Source geography is relevant to governance decisions. If providing
      this term, please provide the applicable country code(s) in column sourceGeography.
    meaning: gov:DUOPlus1
    implements:
    - DUO:0000017
  DUOPlus2:
    text: DUOPlus2
    description: Study population is relevant to governance decisions. If providing
      this term, please provide the applicable population type(s) in column populationType.
    meaning: gov:DUOPlus2
    implements:
    - DUO:0000017
  DUOPlus3:
    text: DUOPlus3
    description: Data deidentification is relevant to governance decisions. If providing
      this term, please provide the applicable deidentification type(s) in column
      deidentificationType.
    meaning: gov:DUOPlus3
    implements:
    - DUO:0000017
  DUOPlus4:
    text: DUOPlus4
    description: A data permission designation is associated with the Study. If providing
      this term, please provide the applicable permission type(s) in column dataPermission.
    meaning: gov:DUOPlus4
    implements:
    - DUO:0000017
  DUOPlus5:
    text: DUOPlus5
    description: A data tier designation is associated with the Study. If providing
      this term, please provide the applicable data tier designation(s) in column
      dataTier.
    meaning: gov:DUOPlus5
    implements:
    - DUO:0000017
  DUOPlus6:
    text: DUOPlus6
    description: A license is associated with the Study. If providing this term, please
      provide the applicable license in column license.
    meaning: gov:DUOPlus6
    implements:
    - DUO:0000017
  DUOPlus7:
    text: DUOPlus7
    description: Attribution conditions are associated with this Study. If providing
      this term, please provide the attribution statement in column attribution.
    meaning: gov:DUOPlus7
    implements:
    - DUO:0000017

```
</details>

</div>