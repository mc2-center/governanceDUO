"""
generate_duo_schema.py
This script generates a JSON schema defining access requirements based on a CSV file containing annotation-based access restrictions.

Usage:
python generate_duo_schema.py [CSV file path] [Output JSON schema file path] [Optional parameters]

author: orion.banks
"""

import argparse
import json
import os
import pandas as pd
import synapseclient
from collections import OrderedDict

def build_condition(row: pd.Series, col_names: list, condition_tuples: list[tuple], multi_condition: bool) -> dict:
    """
    Builds a conditional schema segment based on a row from the CSV file.
    Args:
        row (pd.Series): A row from the DataFrame representing access restrictions.
        col_names (list): List of additional column names to consider for conditions.
        multi_condition (bool): Flag indicating if multiple conditions should be included.
    Returns:
        dict: A dictionary representing the conditional schema segment.
    """

    info_tuples = [([duo for duo in row["DataUseModifiers"].split(", ")], "duo"), ([key for key in row["AccessRequirementKey"].split(", ")], "ar")]
    info_dict = {"duo" : None, "ar" : None}
    
    for list, name in info_tuples:
        if len(list) > 1:
            info_dict[name] = '"allOf": [' + ", ".join([f'"const": "{i}"' for i in list]) + " ]"
        else:
            info_dict[name] = f'"const": "{''.join(list)}"'


    condition = {
        "if": {
            "properties": {
                "DataUseModifiers": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },  
                    "contains": { info_dict["duo"] }
                }
            },
            "required": ["DataUseModifiers"]
        },
        "then": {
            "properties": {
                "_accessRequirementIds": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "contains": { info_dict["ar"] }
                }
            }
        }
    }

    # Optional conditional fields
    additional_conditions = {}
    required_fields = ["dataUseModifiers"]

    if multi_condition is not None:
        if "activatedByAttribute" in row and pd.notna(row["activatedByAttribute"]):
            additional_conditions[row["activatedByAttribute"]] = { "type": "array", "items": { "type": "string" }, "contains": { "const": row["activationValue"] } }
            required_fields.append(row["activatedByAttribute"])

        for key_col, value_col in condition_tuples:
            if (key_col and value_col in row) and (pd.notna(row[key_col]) and pd.notna(row[value_col])):
                additional_conditions[row[key_col]] = { "type": "array", "items": { "type": "string" }, "contains": { "const": row[value_col] } }
                required_fields.append(key_col)

    if additional_conditions:
        condition["if"]["properties"].update(additional_conditions)
        condition["if"]["required"] = required_fields

    return condition

def validate_references(resource_list: list[str], input: list[str], input_type: str, output_path, title, version, org_id, grant_id, study_id):

    if input_type == "paths":
        name_df_tuple_list = [(os.path.basename(file), pd.read_csv(file, header=0)) for file in input]

    if input_type == "folder":
        name_df_tuple_list = [(file, pd.read_csv(os.path.join(input, file), header=0)) for file in os.listdir(input)]
    
    if input_type == "syn_id":
        syn = synapseclient.login()
        df_list = [syn.tableQuery(f"SELECT * FROM {table_id}").asDataFrame().fillna("") for table_id in input]
        name_df_tuple_list = [(df.columns.to_list()[0], df) for df in df_list]
    
    validation_dict = {}
    study_list = None
    ar_list = None

    for name, df in name_df_tuple_list:
        if "Resource" in name:
            resource_df = df[df["Resource_id" in resource_list]]
            study_list = resource_df["StudyKey"].to_list()
            ar_list = resource_df["AccessRequirementKey"].to_list()
        elif "Study" in name and study_list is not None:
            study_df = df[df["Study_id" in study_list]]
        elif "AccessRequirement" in name and ar_list is not None:
            ar_df = df[df["AccessRequirement_id" in study_list]]
        
    for _, row in resource_df.iterrows():
        resource_name = row["Resource_id"]
        study_keys = row["StudyKey"]
        ar_keys = row["AccessRequirementKey"]
        resource_data_use_modifiers = row["dataUseModifiers"]
        validation_dict[resource_name] = (study_keys, ar_keys, resource_data_use_modifiers)
    
    for resource in validation_dict:
        study, ar, resource_duo = validation_dict[resource]
        study_duo = study_df.loc[df["Study_id"] in study, ["dataUseModifiers"]].to_list()
        study_ar_list = study_df.loc[df["Study_id"] in study, ["AccessRequirementKey"]].to_list()
        ar_duo = ar_df.loc[df["AccessRequirement_id"] in ar, ["dataUseModifiers"]].to_list()
        ar_study_list = ar_df.loc[df["AccessRequirement_id"] in ar, ["StudyKey"]].to_list()
        validation_dict[resource] = (study, ar, resource_duo, study_duo, ar_duo, study_ar_list, ar_study_list)
    
    for k, v in validation_dict.items():
        study, ar, resource_duo, study_duo, ar_duo, study_ar_list, ar_study_list = v

        study_ar_validation = [s for s in study if s not in ar_study_list]
        if study_ar_validation:
            print(f"\nThe following Study identifiers are not associated with relevant Access Requirements:\n{study_ar_validation}")
        else:
            print("\nStudy identifiers match those expected by Access Requirements.")
        
        ar_study_validation = [a for a in ar if a not in study_ar_list]
        if ar_study_validation:
            print(f"\nThe following Access Requirement identifiers are not associated with relevant Studies:\n{ar_study_validation}")
        else:
            print("\nAccess Requirement identifiers match those expected by Studies.")
        
        resource_study_duo_validation = [rd for rd in resource_duo if rd not in study_duo]
        if resource_study_duo_validation:
            print(f"\nThe following Data Use Modifiers for Resource {k} are not associated with relevant Studies:\n{resource_study_duo_validation}")
        else:
            print(f"\nData Use Modifiers for Resource {k} match those expected by Studies.")
        
        resource_ar_duo_validation = [rd for rd in resource_duo if rd not in ar_duo]
        if resource_ar_duo_validation:
            print(f"\nThe following Data Use Modifiers for Resource {k} are not associated with relevant Access Requirements:\n{resource_ar_duo_validation}")
        else:
            print(f"\nData Use Modifiers for Resource {k} match those expected by Access Requirements.")
        
        study_resource_duo_validation = [sd for sd in study_duo if sd not in resource_duo]
        if study_resource_duo_validation:
            print(f"\nThe following Data Use Modifiers for relevant Studies are not associated with Resource {k}:\n{resource_ar_duo_validation}")
        else:
            print(f"\nData Use Modifiers for relevant Studies match those associated with Resource {k}.")
        
        study_ar_duo_validation = [sd for sd in study_duo if sd not in ar_duo]
        if study_ar_duo_validation:
            print(f"\nThe following Data Use Modifiers for relevant Studies are not associated with a relevant Access Requirement for Resource {k}:\n{study_ar_duo_validation}")
        else:
            print(f"\nData Use Modifiers for relevant Studies match those associated with listed Access Requirements for Resource {k}.")
        
        ar_resource_duo_validation = [ad for ad in ar_duo if ad not in resource_duo]
        if ar_resource_duo_validation:
            print(f"\nThe following Data Use Modifiers for listed Access Requirements are not applicable to Resource {k}:\n{ar_resource_duo_validation}")
        else:
            print(f"\nData Use Modifiers for listed Access Requirements match those associated with Resource {k}.")
        
        ar_study_duo_validation = [ad for ad in ar_duo if ad not in study_duo]
        if ar_study_duo_validation:
            print(f"\nThe following Data Use Modifiers for listed Access Requirements are not associated with a relevant Study for Resource {k}:\n{study_ar_duo_validation}")
        else:
            print(f"\nData Use Modifiers for listed Access Requirements match those associated with relevant Studies for Resource {k}.")

    output_name = "-".join([key for key in validation_dict.keys()]) + "-AccessRequirementSchema"
    generate_json_schema(resource_df, source_type="validation", output_path=output_path, title=output_name, version=version, org_id=org_id, grant_id=grant_id, study_id=study_id)


def generate_json_schema(data, source_type, output_path, title, version, org_id, grant_id, study_id):
    """
    Generates a JSON schema defining access requirements based on a CSV file.
    Args:
        csv_path (str): Path to the input CSV file.
        output_path (str): Path to the output JSON schema file.
        title (str): Title of the JSON schema.
        version (str): Version of the JSON schema.
        org_id (str): Organization ID for the $id field.
        grant_id (str): Grant number to include in $id field.
        study_id (str): Study ID to include in $id field.
        
    Returns:
        None
    """
    if source_type == "csv":
        df = pd.read_csv(data, header=0, dtype=str)
    if source_type == "validation":
        df = data

    conditions = []
    
    condition_cols = [  # Columns from the Sage / Governance Data Model element 'Resource'
        "Resource_id",
        "AccessRequirementKey",
        "dataUseModifiers",
        "grantAnnotationKey",
        "grantAnnotationValue",
        "studyAnnotationKey",
        "studyAnnotationValue",
        "dataTypeKey",
        "dataTypeValue",
        "speciesTypeKey",
        "speciesTypeValue",
        "activatedByAttribute",
        "activationValue"
        ]
    
    condition_tuples = [
        ("grantAnnotationKey", "grantAnnotationValue"),
        ("studyAnnotationKey", "studyAnnotationValue"),
        ("dataTypeKey", "dataTypeValue"),
        ("speciesTypeKey", "speciesTypeValue")
    ]

    resource_types = "-".join(df["Resource_id"].tolist())
    col_names = df.columns.tolist()
    col_names = [col for col in col_names if col in condition_cols]
    for _, row in df.iterrows():
        condition = build_condition(row, col_names, condition_tuples, multi_condition=True)
        conditions.append(condition)

    schema = OrderedDict({
        "$schema": "http://json-schema.org/draft-07/schema",
        "title": title,
        "$id": f"{org_id}-{grant_id}-{study_id}-{resource_types}AccessRequirementSchema-{version}",
        "description": f"Auto-generated schema that defines access requirements for biomedical data. Organization: {org_id}, Grant number or Project designation: {grant_id}, Study ID: {study_id}, Data Type: {resource_types}",
        "allOf": conditions
    })

    with open(output_path, 'w') as f:
        json.dump(schema, f, indent=2)

    print(f"✅ JSON Schema written to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Access Requirement JSON Schema from Data Dictionary CSV")
    parser.add_argument("input_data", help="Path to directory, list of file paths, or list of Synapse Ids containing the required metadata package.", required=True)
    parser.add_argument("input_type", help="Type of input data. One of 'paths', 'folder', or 'syn_id'", required=True)
    parser.add_argument("output_path", help="Path to output directory for the JSON schema", default=".")
    parser.add_argument("-t", "--title", default="AccessRequirementSchema", help="Schema title")
    parser.add_argument("-v", "--version", default="v1.0.0", help="Schema version")
    parser.add_argument("-o", "--org_id", default="Sage", help="Organization ID for $id field")
    parser.add_argument("-g", "--grant_id", help="Grant number to include in schema$id field.", default="None")
    parser.add_argument("-s", "--study_id", help="Study ID to include in schema$id field.", default="None")
    parser.add_argument("-d", "--data_type", help="Data type to select conditions for from Resource reference table.", default=None, required=True)

    args = parser.parse_args()

    output_path = "".join([args.output_path, "/", args.org_id, ".", "AccessRequirement-", f"{args.grant_id}-" if args.grant_id != "None" else "", f"{args.study_id}-" if args.study_id != "None" else "", f"{args.data_type}-", args.version, "-schema.json"])
    validate_references(args.data_type, args.input_data, args.input_type, output_path, args.title, args.version, args.org_id, args.grant_id, args.study_id)
