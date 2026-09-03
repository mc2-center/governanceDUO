# governance_duo

LinkML representation of the Sage Bionetworks governanceDUO data model (Access Requirement, Resource, Schema, Study), its Policy Fabric integration (policy_fabric.yaml), its RDF Governance Graph representation (governance_graph.yaml), and a design-only GA4GH Data Repository Service (DRS) interoperability crosswalk (drs_alignment.yaml). Architecturally aligned with SageCommonDataModel (https://github.com/Sage-Bionetworks/SageCommonDataModel — one file per entity, a shared BaseEntity + mixins, slot_usage narrowing, prefix/URI discipline). Shaped to interoperate with sagebrain-model (https://github.com/Sage-Bionetworks/sagebrain-model) and the Data Use Ontology (DUO): real DUO terms are reused by IRI via `meaning:` CURIEs rather than re-minted, and the `sagebrain`/`biolink` prefixes below are declared so scripts/build_owl.py's output lines up with sagebrain's own namespaces the moment cross-repo linking is in scope. This is the single entry point — import this file to get the whole model, or import an individual file below for partial use.

URI: https://w3id.org/sage-bionetworks/governance-duo/governance_duo

Name: governance_duo



## Classes

| Class | Description |
| --- | --- |
| [AssetBinding](classes/AssetBinding.md) | One (Synapse entity id -> Policy Fabric Asset DID) pairing |
| [BaseEntity](classes/BaseEntity.md) | Abstract root shared by every governanceDUO class |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[AccessApproval](classes/AccessApproval.md) | Records that a Principal has been approved for access under an AccessRequirem... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[AccessGrant](classes/AccessGrant.md) | A first-class ACL grant: resource, principal, permission(s), source, and whet... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[AccessRequirement](classes/AccessRequirement.md) | Representation of a Synapse Access Requirement and its relationships to entit... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[AccessRequirementAssociation](classes/AccessRequirementAssociation.md) | Binds an AccessRequirement to a resource, recording whether the binding is di... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[AccessRequirementTemplate](classes/AccessRequirementTemplate.md) | A reusable set of DUO-backed Conditions an IRBRequirement can extend |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[DataAccessRequest](classes/DataAccessRequest.md) | A user's draft/submitted request against an AccessRequirement, behind a DataA... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[DataAccessSubmission](classes/DataAccessSubmission.md) | A user's application against an AccessRequirement |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[IRBRequirement](classes/IRBRequirement.md) | A site/program-specific instantiation of an AccessRequirementTemplate, per th... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Program](classes/Program.md) | A multi-site research consortium (e |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ResearchProject](classes/ResearchProject.md) | Documents the research context/justification behind a DataAccessRequest (and,... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Resource](classes/Resource.md) | Information that is relevant to resource access conditions |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Schema](classes/Schema.md) | Information that is relevant to resource access conditions |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Study](classes/Study.md) | Studies associated with a grant |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[SynapseEntity](classes/SynapseEntity.md) | A concrete Synapse entity (project, folder, file, etc |
| [Condition](classes/Condition.md) | A single DUO-code-backed condition on an AccessRequirement, surfacing Governa... |
| [ContributionMixin](classes/ContributionMixin.md) | Contribution/authorship tracking |
| [CredentialRequirement](classes/CredentialRequirement.md) | One credential type a Policy Fabric policy_card requires the requester to pre... |
| [DataAccessSubmissionStatus](classes/DataAccessSubmissionStatus.md) | The approval-workflow state of a DataAccessSubmission |
| [DrsAuthorizationBinding](classes/DrsAuthorizationBinding.md) | Crosswalks one DUO code (or Sage DUOPlus extension) to the shape of the DRS A... |
| [DrsObjectMapping](classes/DrsObjectMapping.md) | How one Synapse entity maps onto a DRS DrsObject's id/self_uri/aliases |
| [GovernanceMixin](classes/GovernanceMixin.md) | DUO-based data-use-modifier vocabulary and its conditional-requirement rules,... |
| [PolicyCardBinding](classes/PolicyCardBinding.md) | One row per verified tmp-policies policy_cards/<name>/ folder: which DUO code... |
| [PolicyCardBindingCollection](classes/PolicyCardBindingCollection.md) | Container class for policy_fabric_bindings |
| [PolicyFabricMixin](classes/PolicyFabricMixin.md) | Fields needed to deploy an AccessRequirement's governed entities into Policy ... |
| [Principal](classes/Principal.md) | A Synapse user or team being granted access via an ACL |
| [ReferenceValueSource](classes/ReferenceValueSource.md) | One (referenceValueKey -> governanceDUO slot) mapping |
| [Site](classes/Site.md) | An institution real Synapse data associates with a ResearchProject, DataAcces... |
| [SynapseAccessRequirementMixin](classes/SynapseAccessRequirementMixin.md) | The real Synapse-native ACCESS_REQUIREMENT row fields (verified against "sage... |



## Slots

| Slot | Description |
| --- | --- |
| [accessorId](slots/accessorId.md) | Synapse numeric id of the Principal approved for access (AccessApproval |
| [accessRequirement](slots/accessRequirement.md) | The AccessRequirement this association binds to the resource |
| [accessRequirementId](slots/accessRequirementId.md) | The AccessRequirement this submission is an application against (DATA_ACCESS_... |
| [AccessRequirementKey](slots/AccessRequirementKey.md) | The Access Requirement id(s) associated with this object |
| [accessRequirementVersion](slots/accessRequirementVersion.md) | The version of the AccessRequirement this submission was made against (DATA_A... |
| [accessType](slots/accessType.md) | The kind of access this Access Requirement governs (ACCESS_REQUIREMENT |
| [activatedByAttribute](slots/activatedByAttribute.md) | The name of a Synapse annotation key that will be applied to entities release... |
| [activationValue](slots/activationValue.md) | The value of Synapse annotation recorded under activatedByAttribute that will... |
| [alias](slots/alias.md) | The Synapse entity's alias (NODE |
| [aliases](slots/aliases.md) | Secondary/external identifiers for this same Synapse entity, carried in DRS's... |
| [allowedAccountTypes](slots/allowedAccountTypes.md) | Account type(s) permitted to access the data (checked against UserPlatformCre... |
| [allowedPurposes](slots/allowedPurposes.md) | Research purpose term(s) for which use is allowed |
| [approvedProjects](slots/approvedProjects.md) | DID(s) of project(s) approved to use the data under this access requirement |
| [approvedUsers](slots/approvedUsers.md) | Identifier(s) of specifically approved users |
| [arType](slots/arType.md) | Free-text access requirement type, e |
| [assetBindings](slots/assetBindings.md) | Policy Fabric Asset-registry DID(s), each paired with the Synapse entity id i... |
| [assetDid](slots/assetDid.md) | The Policy Fabric Asset-registry DID for synapseId |
| [attribution](slots/attribution.md) | The attribution statement for the data associated with the access requirement |
| [bindings](slots/bindings.md) |  |
| [bindingType](slots/bindingType.md) |  |
| [capabilityOperation](slots/capabilityOperation.md) | The "name" field of the Capability Granted this policy_card's Rego emits on s... |
| [collaborationRequired](slots/collaborationRequired.md) | If collaboration is required for the access requirement, provide the PI email... |
| [company](slots/company.md) | Institution/company name, verbatim from Synapse's real UserProfile |
| [concreteType](slots/concreteType.md) | Which kind of Access Requirement this is (ACCESS_REQUIREMENT |
| [conditionDetail](slots/conditionDetail.md) | Zero or more companion-slot values from the source AccessRequirement, one per... |
| [conditionType](slots/conditionType.md) | A short label for this condition |
| [contributionDate](slots/contributionDate.md) | The date on which the access requirement was added |
| [contributorName](slots/contributorName.md) | The name of the person who added this access requirement |
| [createdBy](slots/createdBy.md) | Synapse numeric user id of the record's creator |
| [createdOn](slots/createdOn.md) | When the record was created (epoch milliseconds in the source Synapse tables) |
| [credentialType](slots/credentialType.md) |  |
| [currentRevNum](slots/currentRevNum.md) | The current revision number of the record |
| [dataPermission](slots/dataPermission.md) | The permissions associated with the data under the access requirement |
| [dataTier](slots/dataTier.md) | The tier of data access associated with the access requirement |
| [dataTypeKey](slots/dataTypeKey.md) | The annotation key applied to a Synapse entity that contains a data type iden... |
| [dataTypeValue](slots/dataTypeValue.md) | The value that will be assigned to the key provided under dataTypeKey |
| [dataUseModifier](slots/dataUseModifier.md) | The DUO code (or Sage DUOPlus extension) this binding documents |
| [dataUseModifiers](slots/dataUseModifiers.md) | A list of data use modifiers that apply to the access requirement |
| [deidentificationType](slots/deidentificationType.md) | The type of de-identification applied to the data associated with the access ... |
| [description](slots/description.md) | Human-readable description of this condition, taken directly from DataUseModi... |
| [diseaseSpecificResearch](slots/diseaseSpecificResearch.md) | The type(s) of disease research allowed by this access requirement |
| [domain](slots/domain.md) | Free-text research domain this template applies to, e |
| [drsId](slots/drsId.md) | The DRS DrsObject |
| [drsSelfUri](slots/drsSelfUri.md) | The DRS DrsObject |
| [duoCode](slots/duoCode.md) | The real DUO CURIE this condition represents, when one exists |
| [entityIdList](slots/entityIdList.md) | Synapse ID(s) for Synapse container(s) (e |
| [etag](slots/etag.md) | Entity tag for optimistic concurrency control (a 36-character UUID) |
| [expiredOn](slots/expiredOn.md) | When this approval will expire (epoch milliseconds; AccessApproval |
| [extendsTemplate](slots/extendsTemplate.md) | The AccessRequirementTemplate this IRBRequirement extends |
| [geographicalRestriction](slots/geographicalRestriction.md) | The specific geographic region(s) to which use is limited by the access requi... |
| [grantAnnotationKey](slots/grantAnnotationKey.md) | The annotation key applied to a Synapse entity that contains a grant identifi... |
| [grantAnnotationValue](slots/grantAnnotationValue.md) | The value that will be assigned to the key provided under grantAnnotationKey |
| [grantNumber](slots/grantNumber.md) | The identifier associated with the award funding this study |
| [guardianDataSource](slots/guardianDataSource.md) | The data path/source configured for this asset's Guardian |
| [guardianUrl](slots/guardianUrl.md) | The deployed Guardian service URL for this asset |
| [hasCondition](slots/hasCondition.md) | The DUO-backed Conditions this template reuses -- the same gov:Condition clas... |
| [id](slots/id.md) | A unique identifier for this record |
| [institution](slots/institution.md) | Institution/company name, verbatim from Synapse (ResearchProject |
| [institutionDids](slots/institutionDids.md) | Institutions with specific restrictions associated with the access requiremen... |
| [institutionSpecificRestriction](slots/institutionSpecificRestriction.md) | Institutions with specific restrictions associated with the access requiremen... |
| [intendedDataUseStatement](slots/intendedDataUseStatement.md) | A few short paragraphs explaining how the controlled data will be used (Resea... |
| [isTwoFaRequired](slots/isTwoFaRequired.md) | Whether two-factor authentication is required (ACCESS_REQUIREMENT |
| [keyIsMultivalued](slots/keyIsMultivalued.md) | True if this referenceValueKey's own policy_data_schema |
| [language](slots/language.md) | Free-text consent/IRB language for this requirement |
| [license](slots/license.md) | The license under which the data associated with the access requirement is sh... |
| [maxRevNum](slots/maxRevNum.md) | The maximum revision number of this Synapse entity (NODE |
| [modifiedBy](slots/modifiedBy.md) | Synapse numeric user id of who last modified this record |
| [modifiedOn](slots/modifiedOn.md) | When this record was last modified (epoch milliseconds) |
| [name](slots/name.md) | A Synapse-native display name |
| [nodeType](slots/nodeType.md) | The kind of Synapse entity (NODE |
| [nonprofitLegalForms](slots/nonprofitLegalForms.md) | Legal entity form(s) qualifying as not-for-profit, coded per ISO 20275:2017 (... |
| [notAfter](slots/notAfter.md) | ISO-8601 datetime after which use is no longer permitted |
| [notes](slots/notes.md) | Free-text notes — used in particular to record why sourceSlot is left unset (... |
| [parentId](slots/parentId.md) | The parent Synapse entity in the containment hierarchy (NODE |
| [participatesIn](slots/participatesIn.md) | The Program a Site participates in |
| [passportAuthIssuers](slots/passportAuthIssuers.md) | Mirrors DRS's Authorizations |
| [permission](slots/permission.md) | The permission(s) granted (ACL_RESOURCE_ACCESS_TYPE |
| [policyCardName](slots/policyCardName.md) | The literal tmp-policies policy_cards/<name>/ folder name, e |
| [policyContractDid](slots/policyContractDid.md) | The DID of the deployed rego_policy_agent/rego_token contract pair once this ... |
| [populationType](slots/populationType.md) | The population studied in the research associated with the access requirement |
| [principal](slots/principal.md) | The user or team this grant applies to |
| [principalId](slots/principalId.md) | The Synapse numeric id of the user or team (ACL_RESOURCE_ACCESS |
| [principalType](slots/principalType.md) |  |
| [prohibitedPurposes](slots/prohibitedPurposes.md) | Research purpose term(s) for which use is explicitly disallowed |
| [projectLead](slots/projectLead.md) | The person leading this research project (ResearchProject |
| [publication](slots/publication.md) | Link(s) to publications that used the controlled data (Renewal |
| [publicationMoratorium](slots/publicationMoratorium.md) | End date of the publication moratorium associated with the access requirement |
| [referenceValueKey](slots/referenceValueKey.md) | One of the containing binding's referenceValueKeys, e |
| [referenceValueKeys](slots/referenceValueKeys.md) | The policy_data_schema |
| [referenceValueSources](slots/referenceValueSources.md) |  |
| [registeredSchemaUrl](slots/registeredSchemaUrl.md) | URL associated with the annotation schema that will be applied to the resourc... |
| [rejectedReason](slots/rejectedReason.md) | The reason this submission was rejected, if it was |
| [requestConcreteType](slots/requestConcreteType.md) | Which kind of request this is -- literally "Request" or "Renewal" (RequestInt... |
| [requestId](slots/requestId.md) | The originating data access request |
| [requestPrincipalInvestigatorEmail](slots/requestPrincipalInvestigatorEmail.md) | Flattened from the live API's nested principalInvestigator |
| [requestPrincipalInvestigatorName](slots/requestPrincipalInvestigatorName.md) | Flattened from the live API's nested principalInvestigator |
| [requestSigningOfficialEmail](slots/requestSigningOfficialEmail.md) | Flattened from the live API's nested signingOfficial |
| [requestSigningOfficialName](slots/requestSigningOfficialName.md) | Flattened from the live API's nested signingOfficial |
| [requiredAgreementDocumentId](slots/requiredAgreementDocumentId.md) | DID of the terms/agreement document the requester must accept before this acc... |
| [requiredClaims](slots/requiredClaims.md) | Dot-path claim name(s) this policy_card's Rego logic actually reads, e |
| [requiredCredentials](slots/requiredCredentials.md) |  |
| [requiredProfileStatuses](slots/requiredProfileStatuses.md) | Profile status value(s) a requester's account must have (checked against User... |
| [requirementId](slots/requirementId.md) | The AccessRequirement this approval satisfies (AccessApproval |
| [requirementVersion](slots/requirementVersion.md) | The version of the AccessRequirement this approval satisfies (AccessApproval |
| [researchProjectId](slots/researchProjectId.md) | The research project this submission/request is associated with (DATA_ACCESS_... |
| [researchSpecificRestrictions](slots/researchSpecificRestrictions.md) | Research-specific restrictions associated with the access requirement |
| [resource](slots/resource.md) | The SynapseEntity this grant/association applies to |
| [ResourceKey](slots/ResourceKey.md) | The identifier(s) for the Resource(s) associated with this schema |
| [SchemaKey](slots/SchemaKey.md) | The Schema id corresponding to a registered JSON schema that describes the ac... |
| [schemaUrl](slots/schemaUrl.md) | The registered URL associated with the access requirement JSON schema |
| [scopedToProgram](slots/scopedToProgram.md) | The Program this IRBRequirement is scoped to |
| [scopedToSite](slots/scopedToSite.md) | The Site this IRBRequirement is scoped to |
| [source](slots/source.md) | The system this grant/association was derived from, e |
| [sourceAclId](slots/sourceAclId.md) | Traceability back to the literal ACL |
| [sourceAclResourceAccessId](slots/sourceAclResourceAccessId.md) | Traceability back to the literal ACL_RESOURCE_ACCESS |
| [sourceApprovalId](slots/sourceApprovalId.md) | Traceability back to the literal AccessApproval |
| [sourceField](slots/sourceField.md) | When sourceSlot names an inlined class (e |
| [sourceGeography](slots/sourceGeography.md) | The geographical source of the data associated with the access requirement |
| [sourceSlot](slots/sourceSlot.md) | The name of the governanceDUO slot (on GovernanceMixin, Study, or the PolicyF... |
| [speciesTypeKey](slots/speciesTypeKey.md) | The annotation key applied to a Synapse entity that contains a species identi... |
| [speciesTypeValue](slots/speciesTypeValue.md) | The value that will be assigned to the key provided under speciesTypeKey |
| [state](slots/state.md) |  |
| [status](slots/status.md) | The state of this approval (AccessApproval |
| [studyAnnotationKey](slots/studyAnnotationKey.md) | The annotation key applied to a Synapse entity that contains a study identifi... |
| [studyAnnotationValue](slots/studyAnnotationValue.md) | The value that will be assigned to the key provided under studyAnnotationKey |
| [studyDbgapAccessionId](slots/studyDbgapAccessionId.md) | A stable unique alphanumeric identifier assigned to a study and any objects b... |
| [studyDeidentificationMethodDescription](slots/studyDeidentificationMethodDescription.md) | Description of the process of removing potentially identifying data or data e... |
| [studyDeidentificationMethodSoftware](slots/studyDeidentificationMethodSoftware.md) | Software that was used to de-identify the data (if used) |
| [studyDeidentificationType](slots/studyDeidentificationType.md) | General description of the de-identification method |
| [studyDescription](slots/studyDescription.md) | Description of the study, including the types of experimental assays, model s... |
| [studyId](slots/studyId.md) | The Study (this repo's real governanceduo:Study class, study |
| [studyIndexDate](slots/studyIndexDate.md) | The reference event associated with timepoints in this study |
| [studyInvestigator](slots/studyInvestigator.md) | Investigator(s) associated with the project |
| [StudyKey](slots/StudyKey.md) | The Study id(s) associated with this object |
| [studyName](slots/studyName.md) | Name of the study |
| [studyParticipantNumber](slots/studyParticipantNumber.md) | The number of participant instances associated with systematic investigation ... |
| [studyProjectIdentifier](slots/studyProjectIdentifier.md) | The Synapse Project identifier (synID) with which this Study is related |
| [studySampleNumber](slots/studySampleNumber.md) | The number of specimens associated with systematic investigation into a subje... |
| [submissionId](slots/submissionId.md) | The DataAccessSubmission this status record applies to (DATA_ACCESS_SUBMISSIO... |
| [submittedBy](slots/submittedBy.md) | Synapse numeric user id of who submitted this record (`Submission |
| [submittedOn](slots/submittedOn.md) | When this record was submitted (epoch milliseconds; `Submission |
| [submitterId](slots/submitterId.md) | Synapse numeric user id of who performed the actions to gain this approval (A... |
| [summaryOfUse](slots/summaryOfUse.md) | Summary of how the data has been used (Renewal |
| [supportedAuthTypes](slots/supportedAuthTypes.md) | Mirrors DRS's Authorizations |
| [synapseId](slots/synapseId.md) | A Synapse entity id |
| [timeLimitOnUse](slots/timeLimitOnUse.md) | Time limit on the use of the data associated with the access requirement |
| [trustedIssuerDids](slots/trustedIssuerDids.md) | DID(s) of the Verifiable Credential issuer(s) this AccessRequirement's owner ... |
| [userSpecificRestriction](slots/userSpecificRestriction.md) | The user-specific restrictions associated with the access requirement |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [AccessRequirementConcreteTypeEnum](enums/AccessRequirementConcreteTypeEnum.md) | Synapse's real AccessRequirement subclasses, verified via Sage-Bionetworks/Sy... |
| [AccessTypeEnum](enums/AccessTypeEnum.md) | Synapse's real ACCESS_TYPE values, verified live via rest-docs |
| [ApprovalStateEnum](enums/ApprovalStateEnum.md) | Synapse's real AccessApproval state values (org |
| [BindingTypeEnum](enums/BindingTypeEnum.md) | Whether a governance relationship (an AccessGrant or AccessRequirementAssocia... |
| [CredentialTypeEnum](enums/CredentialTypeEnum.md) | The 15 Verifiable Credential types defined in tmp-policies/credentials/* |
| [DataPermissionEnum](enums/DataPermissionEnum.md) |  |
| [DataTierEnum](enums/DataTierEnum.md) |  |
| [DataUseModifierEnum](enums/DataUseModifierEnum.md) | Data Use Ontology (DUO) modifier codes, plus Sage-local DUOPlus1-7 extensions... |
| [DeidentificationTypeEnum](enums/DeidentificationTypeEnum.md) | De-identification method categories |
| [DrsAuthTypeEnum](enums/DrsAuthTypeEnum.md) | Mirrors DRS's Authorizations |
| [GeographicalRegionEnum](enums/GeographicalRegionEnum.md) | ISO 3166-1 alpha-2 country codes |
| [LicenseEnum](enums/LicenseEnum.md) | model/shared |
| [PrincipalTypeEnum](enums/PrincipalTypeEnum.md) | Whether a Principal is an individual user or a team — from the design doc: "P... |
| [StudyIndexDateEnum](enums/StudyIndexDateEnum.md) |  |
| [SubmissionStateEnum](enums/SubmissionStateEnum.md) | Synapse's real DataAccessSubmissionState values, verified via Sage-Bionetwork... |


## Types

| Type | Description |
| --- | --- |
| [Boolean](types/Boolean.md) | A binary (true or false) value |
| [Curie](types/Curie.md) | a compact URI |
| [Date](types/Date.md) | a date (year, month and day) in an idealized calendar |
| [DateOrDatetime](types/DateOrDatetime.md) | Either a date or a datetime |
| [Datetime](types/Datetime.md) | The combination of a date and time |
| [Decimal](types/Decimal.md) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [Double](types/Double.md) | A real number that conforms to the xsd:double specification |
| [Float](types/Float.md) | A real number that conforms to the xsd:float specification |
| [Integer](types/Integer.md) | An integer |
| [Jsonpath](types/Jsonpath.md) | A string encoding a JSON Path |
| [Jsonpointer](types/Jsonpointer.md) | A string encoding a JSON Pointer |
| [Ncname](types/Ncname.md) | Prefix part of CURIE |
| [Nodeidentifier](types/Nodeidentifier.md) | A URI, CURIE or BNODE that represents a node in a model |
| [Objectidentifier](types/Objectidentifier.md) | A URI or CURIE that represents an object in the model |
| [Sparqlpath](types/Sparqlpath.md) | A string encoding a SPARQL Property Path |
| [String](types/String.md) | A character string |
| [Time](types/Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](types/Uri.md) | a complete URI |
| [Uriorcurie](types/Uriorcurie.md) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
