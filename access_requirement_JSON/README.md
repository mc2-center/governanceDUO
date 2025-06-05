# Data Dictionaries for managing Access Restrictions through Synapse Annotations

## Access Restriction Dictionary format
Stored as a CSV under `access_requirement_JSON/{DCC name}`

| **dataUseModifiers** | **accessRequirementId** | **activatedByAttribute** | **activationValue** | **grantNumber** | **dataType** | **speciesType** | **entityIdList** | 
| -------------------  | ----------------------- | ------------------------ | ------------------- | --------------- | ------------ | --------------- | ---------------- |
| IRB | 1000001 | activateRequirements | True | CA000001 | sequencingLevel1 | Human | syn66638835 |  
| NPU | 1000002 | activateRequirements | True | CA000002 | imagingLevel2 | Mouse | syn66638836 |  
| HMB | 1000003 | activateRequirements | True | CA000003 | proteomicsLevel2 | Human | syn66638837 |  

## Column Descriptions

<details>

<summary><b>Standard columns</b></summary>

  - The following columns **must be populated** before a JSON schema will be generated:
    - `dataUseModifiers`: The value of annotation **dataUseModifiers** that will be applied to Synapse entities released under this access requirement (AR)
    - `accessRequirementId`: The numeric identifier associated with a Synapse AR
    - `entityIdList`: A list of Synapse Ids corresponding to entities that should have the `accessRequirementId` applied

  - The following columns can be populated if desired, but the **column names should not be modified**:
    - `activatedByAttribute`: The name of a Synapse annotation key that will be applied to entities released under this AR and is intended to designate that the AR should be active
    - `activationValue`: The value of Synapse annotation recorded under `activatedByAttribute` that will be applied to entities released under this AR to indicate the AR should be active
  
</details>

<n></n>

<details>

<summary><b>Configurable columns</b></summary>
  
  - Column names can be modified to fit annotations used by the Project
  
  - Column names will be integrated into JSON schemas as an annotation key; column entries will be integrated as values
  
  - Default configurable columns:
  	- `grantNumber`: The value of annotation `grantNumber` that will be applied to Synapse entities released under this AR
    - `studyKey`: The value of annotation `studyKey` that will be applied to Synapse entities released under this AR
  	- `dataType`: The value of annotation `dataType` that will be applied to Synapse entities released under this AR
    - `speciesType`: The value of annotation `speciesType` that will be applied to Synapse entities released under this AR

</details>  

<n></n>  
<n></n>  

## Creating a JSON schema from table contents

JSON schemas can be auto-generated with [`generate_duo_schema.py`](https://github.com/mc2-center/mc2-center-dcc/blob/add-ARjson-build-script/utils/generate_duo_schema.py) (WIP)

<details>

<summary><b>Script usage</b></summary>

```
Generate DUO JSON Schema from Data Dictionary CSV
usage: generate_duo_schema.py [-h] [-t TITLE] [-v VERSION] [-o ORG_ID] [-g GRANT_ID] [-m] [-gc GRANT_COL] [-s STUDY_ID] [-sc STUDY_COL] [-d DATA_TYPE] [-dc DATA_COL] [-p SPECIES_TYPE] [-pc SPECIES_COL] csv_path output_path

positional arguments:
  csv_path: Path to the data_dictionary.csv
  output_path: Path to output directory for the JSON schema

options:
  -h, --help  
  show this help message and exit  

  -t TITLE, --title TITLE  
  Schema title. Default: "AccessRequirementSchema"

  -v VERSION, --version VERSION  
  Schema version. Default: "v1.0.0"

  -o ORG_ID, --org_id ORG_ID  
  Organization ID for $id field. Default: "Project"

  -g GRANT_ID, --grant_id GRANT_ID  
  Grant number to select conditions for from reference table. If nothing is provided, the JSON schema will include all conditions listed in the input table. Default: "Project"

  -m, --multi_condition  
  Boolean. Generate schema with multiple conditions defined in the CSV

  -gc, --grant_col  
  Name of the column in the DCC AR data dictionary that will contain the identifier for the grant. Default: "grantNumber"

  -s, --study_id  
  Study ID to select conditions for from reference table. If nothing is provided, the JSON schema will include all applicable studies listed in the input table. Default: None

  -sc, --study_col
  Name of the column in the DCC AR data dictionary that will contain the identifier for the study. Default: "studyKey"

  -d, --data_type
  Data type to select conditions for from reference table. If nothing is provided, the JSON schema will include all applicable data types listed in the input table. Default: None
  
  -dc, --data_col
  Name of the column in the DCC AR data dictionary that will contain the identifier for the data type. Default: "dataType"

  -p, --species_type
  Species to select conditions for from reference table. If nothing is provided, the JSON schema will include all applicable species listed in the input table. Default: None
  
  -pc, --species_col
  Name of the column in the DCC AR data dictionary that will contain the identifier for the species. Default: "speciesType"

```
</details>  

<n></n>  

<details>

<summary><b>Example 1</b></summary>  

Command:  
`python generate_duo_schema.py example_annotation_AR_reference.csv output_folder -o Project -g CA000002 -v v4.0.0 -m`

Generated JSON schema file name:  
`Project.AccessRequirement-CA000002-mc-v4.0.0-schema.json` 

Output:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema",
  "title": "AccessRequirementSchema",
  "$id": "Project-CA000002-AccessRequirementSchema-v4.0.0",
  "description": "Auto-generated schema defining DUO-based access restrictions.",
  "allOf": [
    {
      "if": {
        "properties": {
          "dataUseModifiers": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": "NPU"
            }
          },
          "grantNumber": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": "CA000002"
            }
          },
          "dataType": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": "imagingLevel2Mouse"
            }
          },
          "activateRequirements": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": "True"
            }
          }
        },
        "required": [
          "dataUseModifiers",
          "grantNumber",
          "dataType",
          "activateRequirements"
        ]
      },
      "then": {
        "properties": {
          "_accessRequirementIds": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": 1000002
            }
          }
        }
      }
    }
  ]
}
```  
</details>  

<n></n>  

<details>

<summary><b>Example 2</b></summary>

Command:  
`python generate_duo_schema.py example_annotation_AR_reference.csv output_folder -o Project -v v3.0.1 -m`  

Generated JSON schema file name:  
`Project.AccessRequirement-Project-mc-v3.0.1-schema.json` 

Output:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema",
  "title": "AccessRequirementSchema",
  "$id": "Project-Project-AccessRequirementSchema-v3.0.1",
  "description": "Auto-generated schema defining DUO-based access restrictions.",
  "allOf": [
    {
      "if": {
        "properties": {
          "dataUseModifiers": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": "IRB"
            }
          },
          "activateRequirements": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": "True"
            }
          },
          "grantNumber": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": "CA000001"
            }
          },
          "dataType": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": "sequencingLevel1Human"
            }
          }
        },
        "required": [
          "dataUseModifiers",
          "activateRequirements",
          "grantNumber",
          "dataType"
        ]
      },
      "then": {
        "properties": {
          "_accessRequirementIds": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": 1000001
            }
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "dataUseModifiers": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": "NPU"
            }
          },
          "activateRequirements": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": "True"
            }
          },
          "grantNumber": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": "CA000002"
            }
          },
          "dataType": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": "imagingLevel2Mouse"
            }
          }
        },
        "required": [
          "dataUseModifiers",
          "activateRequirements",
          "grantNumber",
          "dataType"
        ]
      },
      "then": {
        "properties": {
          "_accessRequirementIds": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": 1000002
            }
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "dataUseModifiers": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": "HMB"
            }
          },
          "activateRequirements": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": "True"
            }
          },
          "grantNumber": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": "CA000003"
            }
          },
          "dataType": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": "proteomicsLevel2Human"
            }
          }
        },
        "required": [
          "dataUseModifiers",
          "activateRequirements",
          "grantNumber",
          "dataType"
        ]
      },
      "then": {
        "properties": {
          "_accessRequirementIds": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": 1000003
            }
          }
        }
      }
    }
  ]
}
```  
</details>  
  
<n></n>  

<details>

<summary><b>Example 3</b></summary>

Command:  
`python generate_duo_schema.py example_annotation_AR_reference.csv output_folder -o Project -v v3.0.1`  

Generated JSON schema file name:  
`Project.AccessRequirement-Project-v3.0.1-schema.json`  

Output:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema",
  "title": "AccessRequirementSchema",
  "$id": "Project-Project-AccessRequirementSchema-v3.0.1",
  "description": "Auto-generated schema defining DUO-based access restrictions.",
  "allOf": [
    {
      "if": {
        "properties": {
          "dataUseModifiers": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": "IRB"
            }
          }
        },
        "required": [
          "dataUseModifiers"
        ]
      },
      "then": {
        "properties": {
          "_accessRequirementIds": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": 1000001
            }
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "dataUseModifiers": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": "NPU"
            }
          }
        },
        "required": [
          "dataUseModifiers"
        ]
      },
      "then": {
        "properties": {
          "_accessRequirementIds": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": 1000002
            }
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "dataUseModifiers": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": "HMB"
            }
          }
        },
        "required": [
          "dataUseModifiers"
        ]
      },
      "then": {
        "properties": {
          "_accessRequirementIds": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "contains": {
              "const": 1000003
            }
          }
        }
      }
    }
  ]
}
```  
</details>
</details>