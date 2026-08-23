
The Data Use Ontology (DUO) provides a helpful framework for gating access to data managed by Sage Bionetworks on the Synapse platform. 

[DUO was developed by members of the Global Alliance for Genomic Health (GA4GH)](https://github.com/EBISPOT/DUO/blob/master/README.md): "DUO allows [users] to semantically tag datasets with restriction about their usage, making them discoverable automatically based on the authorization level of users, or intended usage".

At Sage, we extended DUO modifiers for our use cases and incorporated [derived annotations](https://sagebionetworks.jira.com/wiki/spaces/PLFM/pages/2597617665/API+Changes+to+support+Extension+of+Data+Access+Management+to+Users+outside+of+Sage+ACT) as a way of scaling governance support on projects by assigning access requirements (ARs)* to entities based on its DUO annotation.

_*ARs are applied in the form of a clickwrap (i.e., the user must agree to terms) and/or a managed access requirement (i.e., the user must provide evidence). Managed ARs may require evidence in the form of **Authentication** (e.g., training certification, profile validation, two-factor authorization) and/or **Authorization** (e.g., intended data use (IDU) statement, data use certificate (DUC), ethics approval letter from an institutional review board (IRB) or independent ethics committee (IEC))._


# Resources
 - [GA4GH Products](https://www.ga4gh.org/product/data-use-ontology-duo/)
 - [EBISPOT DUO](https://github.com/EBISPOT/DUO/blob/master/README.md)
 - [Extension of Data Access Management](https://sagebionetworks.jira.com/wiki/spaces/PLFM/pages/2597617665/API+Changes+to+support+Extension+of+Data+Access+Management+to+Users+outside+of+Sage+ACT)


# Related Publications
 - The Data Use Ontology to streamline responsible access to human biomedical datasets. Lawson, Jonathan et al., Cell Genomics, Volume 1, Issue 2, 100028, doi: https://doi.org/10.1016/j.xgen.2021.100028
 - Aligning NIH’s existing data use restrictions to the GA4GH DUO standard. Lawson, Jonathan et al., Cell Genomics, Volume 3, Issue 9, 100381, doi: https://doi.org/10.1016/j.xgen.2023.100381
 - Enhancing Data Use Ontology (DUO) for health-data sharing by extending it with ODRL and DPV. Pandit HJ, Esteves B., Semantic Web. 2024;15(4):1473-1498, doi: https://doi.org/10.3233/SW-243583
 - Getting your DUCs in a row - standardising the representation of Digital Use Conditions. Jeanson, F., Gibson, S.J., Alper, P. et al., Sci Data 11, 464 (2024), doi: https://doi.org/10.1038/s41597-024-03280-6


# LinkML representation

In addition to the schematic CSV model, this repository maintains a
[LinkML](https://github.com/linkml/linkml-model) representation under `linkml/`,
entry point `linkml/governance_duo.linkml.yaml`. It is architecturally aligned with
[SageCommonDataModel](https://github.com/Sage-Bionetworks/SageCommonDataModel): one
file per entity (`access_requirement.yaml`, `resource.yaml`, `schema.yaml`,
`study.yaml`), a shared abstract `BaseEntity` + `slot_usage`-narrowed `id` slot
(`base_entity.yaml`), and cross-cutting concerns factored into `props.yaml`
(generic cross-class slots/enums) and `mixins.yaml` (`GovernanceMixin` — the DUO data-
use-modifier vocabulary plus the conditional-requirement rules that enforce it;
`ContributionMixin` — contributor tracking).

The schematic CSV keeps class-prefixed identifier attribute names
(`AccessRequirement_id`, `Resource_id`, `Schema_id`, `Study_id`) because schematic's
model CSV has one flat, global `Attribute` namespace with no per-class scoping — four
classes can't share a bare `id` attribute there without colliding. The LinkML schema
uses one shared `id` slot on `BaseEntity`, narrowed per class via `slot_usage`
(including a `Pattern` also mirrored back onto the corresponding CSV row).

Real Data Use Ontology (DUO) terms are reused by IRI (`meaning: DUO:0000007`, etc.) —
never re-minted — matching the "reuse external terms by IRI" convention
[sagebrain-model](https://github.com/Sage-Bionetworks/sagebrain-model) documents for
its own ontology. `linkml/governance_duo.linkml.yaml` also declares `sagebrain:`
(`https://w3id.org/synapse/sagebrain#`) and `biolink:` prefixes so generated OWL
output's namespaces already line up with sagebrain-model's, and
`scripts/build_owl.py` stamps the same `skos:scopeNote`/`owl:versionInfo` annotations
on reused external terms that sagebrain-model's own convention uses for classes it
doesn't mint itself. **No changes have been made to the sagebrain-model or
SageCommonDataModel repositories in this pass** — these artifacts are shaped to slot
into sagebrain-model's (currently empty) `ontology/governance/` folder and to
interoperate with SageCommonDataModel, but that integration is not yet wired up.

Beyond DUO, several slots carry `exact_mappings`/`close_mappings` to other terms
found and verified live via the EBI OLS4 API (see the `ols-term-annotator` skill and
`comments` on each mapped slot for the verification rationale) — `exact_mappings`
where the concept genuinely matches, `close_mappings` where the shape differs (e.g. a
literal-valued slot mapped to an object property whose range is an ontology class):

| Slot | Mapping | Term |
|---|---|---|
| `ContributionMixin.contributorName` | close | `prov:wasAttributedTo` |
| `ContributionMixin.contributionDate` | close | `prov:generatedAtTime` |
| `GovernanceMixin.collaborationRequired` | exact | `NCIT:C221739` (synonyms include "COL", this repo's own DUO:0000020 shorthand) |
| `GovernanceMixin.dataTier` | exact | `NCIT:C175887` "Open or Controlled Data Access Indicator" |
| `GovernanceMixin.deidentificationType` / `Study.studyDeidentificationType` | close | `T4FS:0000414` "de-identification" |
| `GovernanceMixin.attribution` | close | `ebiswo:9000006` "Attribution clause" |
| `Study.studyInvestigator` | close | `NCIT:C19924` "Principal Investigator" |
| `Study.studyDbgapAccessionId` | exact | `NCIT:C173940` "dbGaP Accession Number" |
| `Study.grantNumber` | exact | `EVORAO:grantNumber` |
| `Resource.registeredSchemaUrl` / `Schema.schemaUrl` | exact | `dcterms:conformsTo` |

Note the `ebiswo:` prefix (`http://www.ebi.ac.uk/swo/SWO_`) is deliberately not
called `SWO:` — that would collide with the *canonical* OBO Foundry Software
Ontology namespace (`http://purl.obolibrary.org/obo/SWO_`), which is a different,
unrelated resolution for the same three letters; `linkml-lint`'s `canonical_prefixes`
check caught this during review. Slots checked against OLS with no confident match
(DUO-covered detail fields like `timeLimitOnUse`/`userSpecificRestriction`, Synapse
annotation-key/value mechanism slots, and `license`/`dataPermission`, whose SPDX/CC
identifiers aren't OLS ontology terms) were left unmapped rather than forced.

Build/validate targets (see `Makefile`; require `pip install -r requirements.txt`):
```
make linkml-lint      # lint the schema (--ignore-warnings: the camelCase attribute
                       # names are intentional, see above)
make owl              # generate governance_duo.owl.ttl (scripts/build_owl.py)
make shacl            # generate shapes/governance_duo.shacl.ttl (linkml gen-shacl)
make example-rdf      # convert linkml/examples/*.example.yaml to RDF individuals
                       # under linkml/examples/rdf/ (scripts/convert_examples_to_rdf.py)
make shacl-validate   # validate BOTH governance_duo.owl.ttl and the example RDF
                       # individuals against the SHACL shapes, via pyshacl with
                       # inference disabled and the ontology passed as ont_graph —
                       # the exact invocation discipline sagebrain-model's own
                       # tests/validate.py requires, since RDFS entailment on
                       # rdfs:range would otherwise manufacture the very types
                       # SHACL's sh:class checks are meant to verify
```
Example instances validating the DUO conditional-requirement rules live under
`linkml/examples/` (e.g. `linkml-validate -s linkml/governance_duo.linkml.yaml -C
AccessRequirement linkml/examples/access_requirement.example.yaml`). Note that
`gen-shacl` does not compile those `rules:` conditionals into SHACL — only
`linkml-validate`'s JSON Schema path enforces them; `make shacl-validate` covers
everything else (required fields, enum membership, regex patterns, datatypes,
cardinality) against real instance data, converted via
`scripts/convert_examples_to_rdf.py`. That script exists because `linkml-convert`'s
CLI can't mint RDF subject URIs for this schema's dotted, colon-free ids
(`access_requirement.42`) — its `-P/--prefix` flag can't set the special `"@base"`
prefix entry the RDF dumper needs, and passing it also hits a real linkml_runtime bug
(the dumper binds the literal string `"@base"` as a Turtle prefix, which isn't valid
Turtle and fails to re-parse). `scripts/convert_examples_to_rdf.py` calls the dumper's
Python API directly and filters that invalid binding out before serializing — see the
script's docstring for the full explanation.

**Known follow-up, not yet done:**
- `make convert` and `scripts/create_json_from_model.py` must be re-run (they require
  `schematic` and an authenticated `synapseclient` session, unavailable in the
  environment this schema was built in) to refresh `sage-ar.model.jsonld` and the
  `*_validation_schema-updated.json` files after the `Pattern` additions to
  `model/*.model.csv`.

# Materials available in this repository
 - The modular data model CSV source files are available under `model/schematic`
 - All model artifacts can be generated from the top-level directory using the included `Makefile`, provided the schematic python package is available in your environment. To run the `Makefile`, use the following command: 
   ```
   make CONFIG=path/to/your/config.yml
   ```
 - The entirety of the Sage Governance-related metadata model is available in two formats:
   - [CSV](https://github.com/mc2-center/governanceDUO/blob/ar-dictionary-schema/sage-ar.model.csv) (column format compatible with Curator tools / schematic)
   - [JSON-LD](https://github.com/mc2-center/governanceDUO/blob/ar-dictionary-schema/sage-ar.model.jsonld)


 - Empty CSV templates are available for each model type:
   - [Access Requirement](https://github.com/mc2-center/governanceDUO/blob/ar-dictionary-schema/sage-ar.AccessRequirement.manifest.csv)
   - [Resource](https://github.com/mc2-center/governanceDUO/blob/ar-dictionary-schema/sage-ar.Resource.manifest.csv)
   - [Study](https://github.com/mc2-center/governanceDUO/blob/ar-dictionary-schema/sage-ar.Study.manifest.csv)
   - [Schema](https://github.com/mc2-center/governanceDUO/blob/ar-dictionary-schema/sage-ar.Schema.manifest.csv)


 - Synapse-compatible JSON schemas are available for each model type. These can be associated or "bound" to a Synapse container and/or used to create views, Record Sets, Curator tasks, and working sessions. Current versions are linked below and numbered versions are available in the [sage-ar.model folder](https://github.com/mc2-center/governanceDUO/tree/ar-dictionary-schema/sage-ar.model)
   - [Access Requirement](https://github.com/mc2-center/governanceDUO/blob/ar-dictionary-schema/AccessRequirement_validation_schema-updated.json)
   - [Resource](https://github.com/mc2-center/governanceDUO/blob/ar-dictionary-schema/Resource_validation_schema-updated.json)
   - [Study](https://github.com/mc2-center/governanceDUO/blob/ar-dictionary-schema/Study_validation_schema-updated.json)
   - [Schema](https://github.com/mc2-center/governanceDUO/blob/ar-dictionary-schema/Schema_validation_schema-updated.json)

## Submitting metadata to the database
- A dedicated [Synapse Project](https://www.synapse.org/Synapse:syn71723047/files/) is available for programs at Sage Bionetworks to contribute Study, Resource, and AR information
- Records will be stored in the following folders on a per-program basis (one folder per program)
   - [requirements](https://www.synapse.org/Synapse:syn71723125)
   - [resources](https://www.synapse.org/Synapse:syn71723130)
   - [studies](https://www.synapse.org/Synapse:syn71723121)
   >**Note**: If a subfolder with the name of your program/DCC (e.g., "mc2", "elite") is not present in a folder linked above, please request that a new subfolder is created and configured to store your submissions.
- Curation tasks associated with your program's records will be listed in the project [Metadata tab](https://www.synapse.org/Synapse:syn71723047/metadata/)
  - task names will use the format `program.dataType` (e.g., mc2.Study, adkp.Resource)
  - after accessing a task, record the requested metadata in the grid and allow it to validate
    - add as many rows as necessary to represent your program records, using the `+ Add` button
    - alternatively, document your entries in a CSV and use the `Upload` button to populate the grid
  - once you've finished adding information, select `Apply Changes` to store the entries

- Any conditional JSON schemas generated from your inputs will be stored in the [schemas folder](https://www.synapse.org/Synapse:syn71723124) and registered in Synapse, where they can be easily accessed via their URI. 

  >**Note**: when binding schemas, derivedAnnotations <u>must</u> be set to TRUE for conditional JSON statements to function in Synapse.

## Creating conditional JSON schemas from database records
:construction: *Content in development* :construction:

## Using schemas to record governance metadata (Study example)
 - **Note**: It is recommended that separate tables, Record Sets, and/or curation tasks are created within each Synapse Project under consideration.
 - Implementation options:
   - <details>
     <summary>Using Curator to create Record Sets</summary>
	 
	 ### Example workflow
	 
	 - Bind the selected schema to the folder where you intend to store the associated Record Set
	 - Create a Record Set and record-based curation task using either the applicable schema URI or a path to a local version of the JSON schema
	 - Select the curation task from the `Metadata` tab
	 - Add Study information, one Study per row
	   - If it isn't clear how to define a Study for your project, the examples in section **What should be considered a Study?** may be helpful.
	</details>
   
   - <details>
     <summary>Create records externaly and upload to Synapse (via schematic)</summary>
	 
	 ### Example workflow
	 
	 - Download an empty CSV template, generate your own template, or make a Google sheet template copy, using the following link: [Study v4.1.0](https://docs.google.com/spreadsheets/d/1j5-JexPB3p767Vs7ITVuiSGDRWaSR1xDtGPyqn90evE/copy)
	 - Add Study information, one Study per row, *one sheet per Synapse Project*
	   - If it isn't clear how to define a Study for your Project(s), the examples in section **What should be considered a Study?** may be helpful.
	 - If your Study entries aren't already in CSV format, download or convert to CSV
	 - Validate your Study CSV
	   - (Suggested) Use schematic: `schematic model -c config.yml validate -mp /path/to/Study.csv -dt Study`
	 - Upload the validated Study CSV(s) to a folder in your Synapse Project(s)
	   - (Suggested) Use schematic: `schematic model -c config.yml submit -mp /path/to/Study.csv -d {target folder Synapse Id} -mrt table_and_file -tm upsert -tcn display_name`
	</details>

<n></n>

## Additional information

<details>
<summary><b>What should be considered a Study?</b></summary>

>**In this context, a Study can be considered any one grant, publication, data source, or other grouping(s) that apply to resources (files, code, etc.) stored in a Synapse Project.** 

**Note**: If you have previously defined Studies within your program (via a Data Landscape/intake process, governance review, etc.), it is recommended that you reuse the same groupings, to ensure consistency between records.  

</details>

<n></n>
   
  - <details>

    <summary><b>Example 1</b></summary>
	  
	  - Synapse Project A has data from lab 1, lab 2, and lab 3
		- Each lab is supported by the same grant, but each data submission represents a different sub-project within the parent grant
		- Each lab belongs to an independent institution. 
	  - Suggested Study grouping: Study entries should be created for each lab (1, 2, and 3), to represent distinct data types or sharing conditions associated with the independent labs
	  
	  </details>

<n></n>

  - <details>

    <summary><b>Example 2</b></summary>

      - Synapse Projects B, C, and D have data from lab 4, lab 5, and lab 6, respectively.
	  - Suggested Study grouping: A Study Record Set should be created in each Project and populated with an entry for the single associated Study.
	
	</details>

<n></n>
  
  - <details>

    <summary><b>Example 3</b></summary>

	  - Synapse Projects E and F have data from lab 7, lab 8, and lab 9.
	    - Project E has data from lab 7 and lab 8
	    - Project F has data from lab 8 and lab 9
	    - Project E and F store distinct kinds of data

	  - Suggested Study grouping:
	    - A Study Record Set should be created in each Project
		- Lab 8 is responsible for data in both Projects, but the data is distinct and intentionally stored separately, so independent Study entries should be captured in both Projects E and F, for the data submitted by lab 8
		- Study entries for labs 7 and 9 should only be created in Synapse Projects E and F, respectively
	
	</details>
