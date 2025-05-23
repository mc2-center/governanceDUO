# Data Dictionaries for managing Access Restrictions through Synapse Annotations

## Basic dictionary format

| **dataUseModifiers** | **accessRequirementId** | **activatedByAttribute** | **activationValue** | **grantNumber** | **dataType** | **entityIdList** | 
| -------------------  | ----------------------- | ------------------------ | ------------------- | --------------- | ------------ | ---------------- |
| IRB | 1000001 | activateRequirements | True | CA000001 | sequencingLevel1Human | syn66638835 |  
| NPU | 1000002 | activateRequirements | True | CA000002 | imagingLevel2Mouse | syn66638836 |  
| HMB | 1000003 | activateRequirements | True | CA000003 | proteomicsLevel2Human | syn66638837 |  

### Column Descriptions
- **Standard columns**
  - The following columns **must be populated** before a JSON schema will be generated:
    - `dataUseModifiers`: The value of annotation **dataUseModifiers** that will be applied to Synapse entities released under this access requirement (AR)
    - `accessRequirementId`: The numeric identifier associated with a Synapse AR
    - `entityIdList`: A list of Synapse Ids corresponding to entities that should have the `accessRequirementId` applied

  - The following columns can be populated if desired, but the **column names should not be modified**:
    - `activatedByAttribute`: The name of a Synapse annotation key that will be applied to entities released under this AR and is intended to designate that the AR should be active
    - `activationValue`: The value of Synapse annotation recorded under `activatedByAttribute` that will be applied to entities released under this AR to indicate the AR should be active 
  


- **Configurable columns**
  - Column names can be modified to fit annotations used by the Project
  	- `grantNumber`: The value of annotation `grantNumber` that will be applied to Synapse entities released under this AR
  	- `dataType`: The value of annotation `dataType` that will be applied to Synapse entities released under this AR