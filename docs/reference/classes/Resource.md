---
search:
  boost: 10.0
---

# Class: Resource 


_Information that is relevant to resource access conditions._



<div data-search-exclude markdown="1">



URI: [governanceduo:class/Resource](https://w3id.org/sage-bionetworks/governance-duo/class/Resource)





```mermaid
 classDiagram
    class Resource
    click Resource href "../../classes/Resource/"
      GovernanceMixin <|-- Resource
        click GovernanceMixin href "../../classes/GovernanceMixin/"
      BaseEntity <|-- Resource
        click BaseEntity href "../../classes/BaseEntity/"
      
      Resource : AccessRequirementKey
        
      Resource : activatedByAttribute
        
      Resource : activationValue
        
      Resource : allowedAccountTypes
        
      Resource : allowedPurposes
        
      Resource : approvedProjects
        
      Resource : approvedUsers
        
      Resource : attribution
        
      Resource : collaborationRequired
        
      Resource : dataPermission
        
          
    
        
        
        Resource --> "*" DataPermissionEnum : dataPermission
        click DataPermissionEnum href "../../enums/DataPermissionEnum/"
    

        
      Resource : dataTier
        
          
    
        
        
        Resource --> "*" DataTierEnum : dataTier
        click DataTierEnum href "../../enums/DataTierEnum/"
    

        
      Resource : dataTypeKey
        
      Resource : dataTypeValue
        
      Resource : dataUseModifiers
        
          
    
        
        
        Resource --> "*" DataUseModifierEnum : dataUseModifiers
        click DataUseModifierEnum href "../../enums/DataUseModifierEnum/"
    

        
      Resource : deidentificationType
        
          
    
        
        
        Resource --> "*" DeidentificationTypeEnum : deidentificationType
        click DeidentificationTypeEnum href "../../enums/DeidentificationTypeEnum/"
    

        
      Resource : diseaseSpecificResearch
        
      Resource : geographicalRestriction
        
          
    
        
        
        Resource --> "*" GeographicalRegionEnum : geographicalRestriction
        click GeographicalRegionEnum href "../../enums/GeographicalRegionEnum/"
    

        
      Resource : grantAnnotationKey
        
      Resource : grantAnnotationValue
        
      Resource : id
        
      Resource : institutionDids
        
      Resource : institutionSpecificRestriction
        
      Resource : license
        
          
    
        
        
        Resource --> "*" LicenseEnum : license
        click LicenseEnum href "../../enums/LicenseEnum/"
    

        
      Resource : nonprofitLegalForms
        
      Resource : notAfter
        
      Resource : populationType
        
      Resource : prohibitedPurposes
        
      Resource : publicationMoratorium
        
      Resource : registeredSchemaUrl
        
      Resource : requiredAgreementDocumentId
        
      Resource : requiredProfileStatuses
        
      Resource : researchSpecificRestrictions
        
      Resource : SchemaKey
        
      Resource : sourceGeography
        
          
    
        
        
        Resource --> "*" GeographicalRegionEnum : sourceGeography
        click GeographicalRegionEnum href "../../enums/GeographicalRegionEnum/"
    

        
      Resource : speciesTypeKey
        
      Resource : speciesTypeValue
        
      Resource : studyAnnotationKey
        
      Resource : studyAnnotationValue
        
      Resource : StudyKey
        
      Resource : timeLimitOnUse
        
      Resource : userSpecificRestriction
        
      
```





## Inheritance
* [BaseEntity](../classes/BaseEntity.md)
    * **Resource** [ [GovernanceMixin](../classes/GovernanceMixin.md)]


## Class Properties

| Property | Value |
| --- | --- |
| Tree Root | Yes |


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [StudyKey](../slots/StudyKey.md) | * <br/> [String](../types/String.md) | The Study id(s) associated with this object | direct |
| [AccessRequirementKey](../slots/AccessRequirementKey.md) | * <br/> [String](../types/String.md) | The Access Requirement id(s) associated with this object | direct |
| [SchemaKey](../slots/SchemaKey.md) | 0..1 <br/> [String](../types/String.md) | The Schema id corresponding to a registered JSON schema that describes the ac... | direct |
| [grantAnnotationKey](../slots/grantAnnotationKey.md) | 0..1 <br/> [String](../types/String.md) | The annotation key applied to a Synapse entity that contains a grant identifi... | direct |
| [grantAnnotationValue](../slots/grantAnnotationValue.md) | 0..1 <br/> [String](../types/String.md) | The value that will be assigned to the key provided under grantAnnotationKey | direct |
| [studyAnnotationKey](../slots/studyAnnotationKey.md) | 0..1 <br/> [String](../types/String.md) | The annotation key applied to a Synapse entity that contains a study identifi... | direct |
| [studyAnnotationValue](../slots/studyAnnotationValue.md) | 0..1 <br/> [String](../types/String.md) | The value that will be assigned to the key provided under studyAnnotationKey | direct |
| [dataTypeKey](../slots/dataTypeKey.md) | 0..1 <br/> [String](../types/String.md) | The annotation key applied to a Synapse entity that contains a data type iden... | direct |
| [dataTypeValue](../slots/dataTypeValue.md) | 0..1 <br/> [String](../types/String.md) | The value that will be assigned to the key provided under dataTypeKey | direct |
| [speciesTypeKey](../slots/speciesTypeKey.md) | 0..1 <br/> [String](../types/String.md) | The annotation key applied to a Synapse entity that contains a species identi... | direct |
| [speciesTypeValue](../slots/speciesTypeValue.md) | 0..1 <br/> [String](../types/String.md) | The value that will be assigned to the key provided under speciesTypeKey | direct |
| [activatedByAttribute](../slots/activatedByAttribute.md) | 0..1 <br/> [String](../types/String.md) | The name of a Synapse annotation key that will be applied to entities release... | direct |
| [activationValue](../slots/activationValue.md) | 0..1 <br/> [String](../types/String.md) | The value of Synapse annotation recorded under activatedByAttribute that will... | direct |
| [registeredSchemaUrl](../slots/registeredSchemaUrl.md) | 0..1 <br/> [String](../types/String.md) | URL associated with the annotation schema that will be applied to the resourc... | direct |
| [dataUseModifiers](../slots/dataUseModifiers.md) | * <br/> [DataUseModifierEnum](../enums/DataUseModifierEnum.md) | A list of data use modifiers that apply to the access requirement | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [collaborationRequired](../slots/collaborationRequired.md) | 0..1 <br/> [String](../types/String.md) | If collaboration is required for the access requirement, provide the PI email... | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [diseaseSpecificResearch](../slots/diseaseSpecificResearch.md) | * <br/> [String](../types/String.md) | The type(s) of disease research allowed by this access requirement | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [geographicalRestriction](../slots/geographicalRestriction.md) | * <br/> [GeographicalRegionEnum](../enums/GeographicalRegionEnum.md) | The specific geographic region(s) to which use is limited by the access requi... | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [institutionSpecificRestriction](../slots/institutionSpecificRestriction.md) | * <br/> [String](../types/String.md) | Institutions with specific restrictions associated with the access requiremen... | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [institutionDids](../slots/institutionDids.md) | * <br/> [String](../types/String.md) | Institutions with specific restrictions associated with the access requiremen... | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [publicationMoratorium](../slots/publicationMoratorium.md) | 0..1 <br/> [String](../types/String.md) | End date of the publication moratorium associated with the access requirement | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [researchSpecificRestrictions](../slots/researchSpecificRestrictions.md) | 0..1 <br/> [String](../types/String.md) | Research-specific restrictions associated with the access requirement | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [timeLimitOnUse](../slots/timeLimitOnUse.md) | 0..1 <br/> [Float](../types/Float.md) | Time limit on the use of the data associated with the access requirement | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [userSpecificRestriction](../slots/userSpecificRestriction.md) | 0..1 <br/> [String](../types/String.md) | The user-specific restrictions associated with the access requirement | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [sourceGeography](../slots/sourceGeography.md) | * <br/> [GeographicalRegionEnum](../enums/GeographicalRegionEnum.md) | The geographical source of the data associated with the access requirement | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [populationType](../slots/populationType.md) | 0..1 <br/> [String](../types/String.md) | The population studied in the research associated with the access requirement | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [deidentificationType](../slots/deidentificationType.md) | * <br/> [DeidentificationTypeEnum](../enums/DeidentificationTypeEnum.md) | The type of de-identification applied to the data associated with the access ... | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [dataPermission](../slots/dataPermission.md) | * <br/> [DataPermissionEnum](../enums/DataPermissionEnum.md) | The permissions associated with the data under the access requirement | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [dataTier](../slots/dataTier.md) | * <br/> [DataTierEnum](../enums/DataTierEnum.md) | The tier of data access associated with the access requirement | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [license](../slots/license.md) | * <br/> [LicenseEnum](../enums/LicenseEnum.md) | The license under which the data associated with the access requirement is sh... | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [attribution](../slots/attribution.md) | 0..1 <br/> [String](../types/String.md) | The attribution statement for the data associated with the access requirement | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [requiredAgreementDocumentId](../slots/requiredAgreementDocumentId.md) | 0..1 <br/> [String](../types/String.md) | DID of the terms/agreement document the requester must accept before this acc... | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [notAfter](../slots/notAfter.md) | 0..1 <br/> [String](../types/String.md) | ISO-8601 datetime after which use is no longer permitted | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [allowedPurposes](../slots/allowedPurposes.md) | * <br/> [String](../types/String.md) | Research purpose term(s) for which use is allowed | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [prohibitedPurposes](../slots/prohibitedPurposes.md) | * <br/> [String](../types/String.md) | Research purpose term(s) for which use is explicitly disallowed | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [nonprofitLegalForms](../slots/nonprofitLegalForms.md) | * <br/> [String](../types/String.md) | Legal entity form(s) qualifying as not-for-profit, coded per ISO 20275:2017 (... | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [approvedProjects](../slots/approvedProjects.md) | * <br/> [String](../types/String.md) | DID(s) of project(s) approved to use the data under this access requirement | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [approvedUsers](../slots/approvedUsers.md) | * <br/> [String](../types/String.md) | Identifier(s) of specifically approved users | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [allowedAccountTypes](../slots/allowedAccountTypes.md) | * <br/> [String](../types/String.md) | Account type(s) permitted to access the data (checked against UserPlatformCre... | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [requiredProfileStatuses](../slots/requiredProfileStatuses.md) | * <br/> [String](../types/String.md) | Profile status value(s) a requester's account must have (checked against User... | [GovernanceMixin](../classes/GovernanceMixin.md) |
| [id](../slots/id.md) | 1 <br/> [String](../types/String.md) | A unique identifier for the resource type (schematic source attribute: Resour... | [BaseEntity](../classes/BaseEntity.md) |















## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | governanceduo:Resource |
| native | governanceduo:Resource |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Resource
description: Information that is relevant to resource access conditions.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
is_a: BaseEntity
mixins:
- GovernanceMixin
slots:
- StudyKey
- AccessRequirementKey
- SchemaKey
- grantAnnotationKey
- grantAnnotationValue
- studyAnnotationKey
- studyAnnotationValue
- dataTypeKey
- dataTypeValue
- speciesTypeKey
- speciesTypeValue
- activatedByAttribute
- activationValue
- registeredSchemaUrl
slot_usage:
  id:
    name: id
    description: 'A unique identifier for the resource type (schematic source attribute:
      Resource_id). Examples: mc2Res1, adkpRes1, adkpRes2.'
    examples:
    - value: resource.mc2Res1
    pattern: ^resource\.[A-Za-z0-9]+$
tree_root: true

```
</details>

### Induced

<details>
```yaml
name: Resource
description: Information that is relevant to resource access conditions.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
is_a: BaseEntity
mixins:
- GovernanceMixin
slot_usage:
  id:
    name: id
    description: 'A unique identifier for the resource type (schematic source attribute:
      Resource_id). Examples: mc2Res1, adkpRes1, adkpRes2.'
    examples:
    - value: resource.mc2Res1
    pattern: ^resource\.[A-Za-z0-9]+$
attributes:
  StudyKey:
    name: StudyKey
    annotations:
      foreign_key:
        tag: foreign_key
        value: true
    description: The Study id(s) associated with this object. Provide multiple values
      as a comma-separated list.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - AccessRequirement
    - Resource
    - Schema
    range: string
    multivalued: true
  AccessRequirementKey:
    name: AccessRequirementKey
    annotations:
      foreign_key:
        tag: foreign_key
        value: true
    description: The Access Requirement id(s) associated with this object. Provide
      multiple values as a comma-separated list.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - Resource
    - Schema
    - Study
    range: string
    multivalued: true
  SchemaKey:
    name: SchemaKey
    annotations:
      foreign_key:
        tag: foreign_key
        value: true
    description: The Schema id corresponding to a registered JSON schema that describes
      the access conditions relevant to this Resource.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - Resource
    range: string
  grantAnnotationKey:
    name: grantAnnotationKey
    description: The annotation key applied to a Synapse entity that contains a grant
      identifier.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - Resource
    range: string
  grantAnnotationValue:
    name: grantAnnotationValue
    description: The value that will be assigned to the key provided under grantAnnotationKey.
      Value should be applied to Synapse entities released with this AR.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - Resource
    range: string
  studyAnnotationKey:
    name: studyAnnotationKey
    description: The annotation key applied to a Synapse entity that contains a study
      identifier.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - Resource
    range: string
  studyAnnotationValue:
    name: studyAnnotationValue
    description: The value that will be assigned to the key provided under studyAnnotationKey.
      Value should be applied to Synapse entities released with this AR.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - Resource
    range: string
  dataTypeKey:
    name: dataTypeKey
    description: The annotation key applied to a Synapse entity that contains a data
      type identifier.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - Resource
    range: string
  dataTypeValue:
    name: dataTypeValue
    description: The value that will be assigned to the key provided under dataTypeKey.
      Value should be applied to Synapse entities released with this AR.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - Resource
    range: string
  speciesTypeKey:
    name: speciesTypeKey
    description: The annotation key applied to a Synapse entity that contains a species
      identifier.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - Resource
    range: string
  speciesTypeValue:
    name: speciesTypeValue
    description: The value that will be assigned to the key provided under speciesTypeKey.
      Value should be applied to Synapse entities released with this AR.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - Resource
    range: string
  activatedByAttribute:
    name: activatedByAttribute
    description: The name of a Synapse annotation key that will be applied to entities
      released under this AR. Setting this attribute to activationValue designates
      that the AR should be active.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - Resource
    range: string
  activationValue:
    name: activationValue
    description: The value of Synapse annotation recorded under activatedByAttribute
      that will be applied to entities released under this AR to indicate the AR should
      be active.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - Resource
    range: string
  registeredSchemaUrl:
    name: registeredSchemaUrl
    description: URL associated with the annotation schema that will be applied to
      the resource type.
    comments:
    - 'dcterms:conformsTo, "An established standard to which the described resource
      conforms" — exact match: this URL points at the registered JSON schema the resource
      must conform to.'
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    exact_mappings:
    - dcterms:conformsTo
    rank: 1000
    owner: Resource
    domain_of:
    - Resource
    range: string
  dataUseModifiers:
    name: dataUseModifiers
    description: A list of data use modifiers that apply to the access requirement.
      Includes real Data Use Ontology (DUO) terms plus Sage-local DUOPlus1-7 extensions
      (see README) and the literal value "Pending Annotation".
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: DataUseModifierEnum
    multivalued: true
  collaborationRequired:
    name: collaborationRequired
    description: If collaboration is required for the access requirement, provide
      the PI email address. Provide multiple as a comma-separated list.
    comments:
    - Required when dataUseModifiers contains DUO:0000020 — see GovernanceMixin rules.
    - NCIT:C221739 "Consent for Use Requires Collaboration Agreement" carries the
      synonyms "COL"/"Collaboration required", the same shorthand this repo already
      uses for DUO:0000020 — verified live and non-obsolete via the OLS4 API.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    exact_mappings:
    - NCIT:C221739
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: string
  diseaseSpecificResearch:
    name: diseaseSpecificResearch
    description: 'The type(s) of disease research allowed by this access requirement.
      Provide the MONDO ID in format MONDO:id. Provide multiple values as a comma-separated
      list. MONDO terms can be found here: https://ols.monarchinitiative.org/ontologies/mondo'
    comments:
    - Required when dataUseModifiers contains DUO:0000007 — see GovernanceMixin rules.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: string
    multivalued: true
    pattern: MONDO:\d{7}
  geographicalRestriction:
    name: geographicalRestriction
    description: The specific geographic region(s) to which use is limited by the
      access requirement.
    comments:
    - Required when dataUseModifiers contains DUO:0000022 — see GovernanceMixin rules.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: GeographicalRegionEnum
    multivalued: true
  institutionSpecificRestriction:
    name: institutionSpecificRestriction
    description: 'Institutions with specific restrictions associated with the access
      requirement. Provide the institution ROR ID in format ROR:id. Provide multiple
      entries as a comma-separated list. ROR IDs can be found here: https://ror.org/search'
    comments:
    - Required when dataUseModifiers contains DUO:0000028 — see GovernanceMixin rules.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: string
    multivalued: true
    pattern: ROR:[a-z0-9]{9}
  institutionDids:
    name: institutionDids
    description: Institutions with specific restrictions associated with the access
      requirement, as decentralized identifiers (DIDs) rather than ROR ids. Policy
      Fabric (https://github.com/hasan7n/tmp-policies)'s institution-specific-restriction
      policy_card expects its allowedInstitutions reference values, and the AffiliationCredential.isMemberOf
      claim it checks against them, to both be organization DIDs — not ROR ids. No
      standard ROR-to-DID resolution exists yet, so this is a separate, companion
      slot rather than a reinterpretation of institutionSpecificRestriction's existing
      pattern.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: string
    multivalued: true
    pattern: ^did:[a-z0-9]+:.+$
  publicationMoratorium:
    name: publicationMoratorium
    description: End date of the publication moratorium associated with the access
      requirement.
    comments:
    - 'schematic Format: date'
    - Required when dataUseModifiers contains DUO:0000024 — see GovernanceMixin rules.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: string
  researchSpecificRestrictions:
    name: researchSpecificRestrictions
    description: Research-specific restrictions associated with the access requirement.
    comments:
    - Required when dataUseModifiers contains DUO:0000012 — see GovernanceMixin rules.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: string
  timeLimitOnUse:
    name: timeLimitOnUse
    description: Time limit on the use of the data associated with the access requirement.
    comments:
    - Required when dataUseModifiers contains DUO:0000025 — see GovernanceMixin rules.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: float
  userSpecificRestriction:
    name: userSpecificRestriction
    description: The user-specific restrictions associated with the access requirement.
    comments:
    - Required when dataUseModifiers contains DUO:0000026 — see GovernanceMixin rules.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: string
  sourceGeography:
    name: sourceGeography
    description: The geographical source of the data associated with the access requirement.
      Equivalent to DUOPlus1.
    comments:
    - Required when dataUseModifiers contains DUOPlus1 — see GovernanceMixin rules.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: GeographicalRegionEnum
    multivalued: true
  populationType:
    name: populationType
    description: The population studied in the research associated with the access
      requirement. Equivalent to DUOPlus2.
    comments:
    - Required when dataUseModifiers contains DUOPlus2 — see GovernanceMixin rules.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: string
  deidentificationType:
    name: deidentificationType
    description: The type of de-identification applied to the data associated with
      the access requirement. Equivalent to DUOPlus3.
    comments:
    - Required when dataUseModifiers contains DUOPlus3 — see GovernanceMixin rules.
    - T4FS:0000414 "de-identification" (Terminology for Food Safety, but the term
      itself is a generic privacy concept) is a close, not exact, match — this slot
      names one of a specific set of methods (HIPPA_LDS/SafeHarbor/etc.), the OLS
      term describes the general technique.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    close_mappings:
    - T4FS:0000414
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: DeidentificationTypeEnum
    multivalued: true
  dataPermission:
    name: dataPermission
    description: The permissions associated with the data under the access requirement.
      Equivalent to DUOPlus4.
    comments:
    - Required when dataUseModifiers contains DUOPlus4 — see GovernanceMixin rules.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: DataPermissionEnum
    multivalued: true
  dataTier:
    name: dataTier
    description: The tier of data access associated with the access requirement. Equivalent
      to DUOPlus5.
    comments:
    - Required when dataUseModifiers contains DUOPlus5 — see GovernanceMixin rules.
    - 'NCIT:C175887 "Open or Controlled Data Access Indicator" (synonym: "Data Access
      Level") is defined as "Specifies whether the data in a repository is open access
      or controlled access" — a direct match for this slot''s Anonymous/Open/Controlled/Private
      tiers.'
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    exact_mappings:
    - NCIT:C175887
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: DataTierEnum
    multivalued: true
  license:
    name: license
    description: The license under which the data associated with the access requirement
      is shared. Equivalent to DUOPlus6.
    comments:
    - Required when dataUseModifiers contains DUOPlus6 — see GovernanceMixin rules.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: LicenseEnum
    multivalued: true
  attribution:
    name: attribution
    description: The attribution statement for the data associated with the access
      requirement. Equivalent to DUOPlus7.
    comments:
    - Required when dataUseModifiers contains DUOPlus7 — see GovernanceMixin rules.
    - SWO:9000006 "Attribution clause" (Software Ontology term, reused via the mcro
      ontology) — a license-clause-shaped close mapping; this slot instead holds the
      free-text statement itself, not the clause concept.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    close_mappings:
    - ebiswo:9000006
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: string
  requiredAgreementDocumentId:
    name: requiredAgreementDocumentId
    description: 'DID of the terms/agreement document the requester must accept before
      this access requirement''s data use modifiers are satisfied. Added to close
      a Policy Fabric (https://github.com/hasan7n/tmp-policies) gap: its general-research-use,
      publication-moratorium, return-to-database-or-resource, and time-limit-on-use
      policy_cards all key their Reference Values Schema on a single requiredDocumentID,
      which no existing slot held — publicationMoratorium and timeLimitOnUse hold
      a date/duration, not a document identifier, so this is a new, distinct slot
      rather than a reinterpretation of either.'
    comments:
    - Required when dataUseModifiers contains DUO:0000042, DUO:0000024, DUO:0000029,
      or DUO:0000025 — see GovernanceMixin rules.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: string
    pattern: ^did:[a-z0-9]+:.+$
  notAfter:
    name: notAfter
    description: 'ISO-8601 datetime after which use is no longer permitted. Added
      to close a Policy Fabric gap: time-limit-on-use''s Reference Values Schema key
      notAfter is an absolute datetime, whereas the existing timeLimitOnUse slot holds
      a number of months — a different shape entirely, so this is a new, distinct
      slot.'
    comments:
    - Required when dataUseModifiers contains DUO:0000025 — see GovernanceMixin rules.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: string
  allowedPurposes:
    name: allowedPurposes
    description: 'Research purpose term(s) for which use is allowed. Added to close
      a Policy Fabric gap: genetic-studies-only, health-or-medical-or-biomedical-research,
      population-origins-or-ancestry-research-only, and research-specific-restrictions
      all key their Reference Values Schema on a multivalued allowedPurposes list;
      the existing researchSpecificRestrictions slot is free text and not multivalued,
      so this is a new, distinct slot rather than a reinterpretation of it (the two
      can coexist — one is a human-readable narrative, this one is the structured,
      machine-checkable list Policy Fabric''s Rego logic actually reads).'
    comments:
    - Required when dataUseModifiers contains DUO:0000016, DUO:0000006, DUO:0000011,
      or DUO:0000012 — see GovernanceMixin rules.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: string
    multivalued: true
  prohibitedPurposes:
    name: prohibitedPurposes
    description: 'Research purpose term(s) for which use is explicitly disallowed.
      Added to close a Policy Fabric gap: health-or-medical-or-biomedical-research,
      no-general-methods-research, non-commercial-use-only, not-for-profit-non-commercial-use-only,
      and population-origins-or-ancestry-research-prohibited all key their Reference
      Values Schema on a multivalued prohibitedPurposes list, which no existing slot
      held.'
    comments:
    - Required when dataUseModifiers contains DUO:0000006, DUO:0000015, DUO:0000046,
      DUO:0000018, or DUO:0000044 — see GovernanceMixin rules.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: string
    multivalued: true
  nonprofitLegalForms:
    name: nonprofitLegalForms
    description: 'Legal entity form(s) qualifying as not-for-profit, coded per ISO
      20275:2017 (Entity Legal Form Code List). Added to close a Policy Fabric gap:
      not-for-profit-organisation-use-only and not-for-profit-non-commercial-use-only
      both key their Reference Values Schema on a multivalued nonprofitLegalForms
      list, which no existing slot held.'
    comments:
    - Required when dataUseModifiers contains DUO:0000045 or DUO:0000018 — see GovernanceMixin
      rules.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: string
    multivalued: true
  approvedProjects:
    name: approvedProjects
    description: 'DID(s) of project(s) approved to use the data under this access
      requirement. Added to close a Policy Fabric gap: project-specific-restriction
      keys its Reference Values Schema on a multivalued approvedProjects list of DIDs,
      which no existing slot held.'
    comments:
    - Required when dataUseModifiers contains DUO:0000027 — see GovernanceMixin rules.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: string
    multivalued: true
    pattern: ^did:[a-z0-9]+:.+$
  approvedUsers:
    name: approvedUsers
    description: 'Identifier(s) of specifically approved users. Added to close a Policy
      Fabric gap: user-specific-restriction keys part of its Reference Values Schema
      on a multivalued approvedUsers list, checked against UserPlatformCredential.userId
      — the existing userSpecificRestriction slot is free text describing the restriction,
      not a structured list of identifiers, so this is a new, distinct slot (userSpecificRestriction,
      allowedAccountTypes, and requiredProfileStatuses together cover the three separate
      keys this one policy_card''s Reference Values Schema defines).'
    comments:
    - Required when dataUseModifiers contains DUO:0000026 — see GovernanceMixin rules.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: string
    multivalued: true
  allowedAccountTypes:
    name: allowedAccountTypes
    description: Account type(s) permitted to access the data (checked against UserPlatformCredential.accountType).
      Added to close the same user-specific-restriction gap as approvedUsers.
    comments:
    - Required when dataUseModifiers contains DUO:0000026 — see GovernanceMixin rules.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: string
    multivalued: true
  requiredProfileStatuses:
    name: requiredProfileStatuses
    description: Profile status value(s) a requester's account must have (checked
      against UserPlatformCredential.profileStatus). Added to close the same user-specific-restriction
      gap as approvedUsers.
    comments:
    - Required when dataUseModifiers contains DUO:0000026 — see GovernanceMixin rules.
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    owner: Resource
    domain_of:
    - GovernanceMixin
    range: string
    multivalued: true
  id:
    name: id
    description: 'A unique identifier for the resource type (schematic source attribute:
      Resource_id). Examples: mc2Res1, adkpRes1, adkpRes2.'
    examples:
    - value: resource.mc2Res1
    from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
    rank: 1000
    slot_uri: dcterms:identifier
    identifier: true
    owner: Resource
    domain_of:
    - BaseEntity
    range: string
    required: true
    pattern: ^resource\.[A-Za-z0-9]+$
tree_root: true

```
</details></div>