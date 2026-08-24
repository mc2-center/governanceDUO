
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


# Documentation

Deeper, example-backed docs on the LinkML model, its knowledge-graph representations,
and the Policy Fabric integration — including an auto-generated schema reference
(`make docs`) — live under [`docs/`](docs/index.md), starting at
[`docs/index.md`](docs/index.md). The LinkML/Policy Fabric/Governance Graph sections
below are unchanged and still apply; the docs/ pages add diagrams, worked examples,
and full per-class/slot/enum reference on top of them.

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
`scripts/convert_examples_to_rdf.py`. This schema's ids are dotted, colon-free
strings (`access_requirement.42` — the SageCommonDataModel-style convention this
schema deliberately follows), and linkml_runtime's RDF dumper can only mint a
subject URI for such an id via a special `"@base"` namespace entry that has to be
supplied externally at dump time — the schema's own `prefixes:` block can't declare
it at all (`Prefix('@base', ...)` is rejected as "not a valid NCName"), and
`linkml-convert`'s `-P/--prefix` CLI flag hits that same rejection trying to set it.
Rather than route around this with a made-up `@base` IRI (which also needs a
second workaround, since the dumper then binds the literal string `"@base"` itself
as an invalid Turtle prefix), `scripts/convert_examples_to_rdf.py` instead
temporarily rewrites each loaded instance's id to a real CURIE
(`governanceduo:access_requirement.42`) only for the dump call — which
`Namespaces.uri_for()` resolves directly via the schema's own already-declared
`governanceduo:` prefix, no `@base` involved — then restores the bare id
afterward. The *stored* id in every example YAML file and every class's
`slot_usage.id.pattern` are completely unaffected, preserving interoperability with
SageCommonDataModel's bare-id convention everywhere except this one transient
export step. See the script's docstring for the full explanation.

**Known follow-up, not yet done:**
- `make convert` and `scripts/create_json_from_model.py` must be re-run (they require
  `schematic` and an authenticated `synapseclient` session, unavailable in the
  environment this schema was built in) to refresh `sage-ar.model.jsonld` and the
  `*_validation_schema-updated.json` files after the `Pattern` additions to
  `model/*.model.csv`.

## Policy Fabric alignment

[Policy Fabric](https://github.com/hasan7n/tmp-policies) (docs:
[hasan7n.github.io/tmp-policies](https://hasan7n.github.io/tmp-policies/); architecture
paper: "A Technical Policy Blueprint for Trustworthy Decentralized AI") is a
decentralized-AI governance framework whose reference policies (`policy_cards/`) are
each authored against a specific DUO code — the same Data Use Ontology this repo's
`GovernanceMixin`/`DataUseModifierEnum` already encode. `linkml/policy_fabric.yaml`
and `linkml/policy_fabric_bindings.yaml` add the missing structured link: for every
one of the 21 `policy_cards/` in that repo (verified by reading each folder's actual
`policy.rego` and `policy_data_schema.json`, not inferred from naming), a
`PolicyCardBinding` records its DUO code, its Reference Values Schema key(s), which
Verifiable Credential type(s)/claim(s) it requires, and — critically — which existing
governanceDUO slot (if any) already collects that reference value.

Each `PolicyCardBinding` maps its `referenceValueKeys` to governanceDUO slots via
`referenceValueSources` (a list, not a single scalar — several bindings need two
keys from two different slots, e.g. `time-limit-on-use`'s `requiredDocumentID` and
`notAfter`), each tagged `keyIsMultivalued` since some Policy Fabric keys are lists
(`allowedCountries`) and some are scalars (`datasetID`, `requiredDocumentID`,
`notAfter`) — `scripts/build_policy_fabric.py` honors this per key rather than
uniformly wrapping every value in an array, which was a real bug caught and fixed
while closing the gaps below.

5 of the 21 bindings had a working `sourceSlot` from the start:
`geographicalRestriction` and `diseaseSpecificResearch` already collected exactly
what's needed (ISO country codes, MONDO codes); `institutionSpecificRestriction`
didn't — Policy Fabric's `AffiliationCredential.isMemberOf` and
`allowedInstitutions` expect organization **DIDs**, not ROR ids, so a new companion
slot `institutionDids` was added rather than reinterpreting the existing ROR-pattern
field; `collaboration-required` and `publication-required` both key on a `datasetID`
sourced from the new `PolicyFabricMixin.assetDids`. A new `PolicyFabricMixin`
(`assetDids`, `guardianDataSource`, `guardianUrl`, `policyContractDid`,
`trustedIssuerDids`), applied to `AccessRequirement`, mirrors the real (minimal)
Django `Asset` model's `did`/`metadata` fields and the per-record trust choices
Policy Fabric's "expose" step captures.

The remaining 16 were **documented gaps, not silent guesses**, and have since been
closed by adding 9 new, deliberately reusable `GovernanceMixin` slots — each with
its own DUO-conditional `rules:` entry, matching this repo's existing pattern —
rather than repurposing an existing narrative field into the wrong shape:
`allowedPurposes`/`prohibitedPurposes` (reused across 8 codes), `nonprofitLegalForms`
(ISO 20275 ELF codes, 2 codes), `requiredAgreementDocumentId` (4 codes),
`approvedProjects`, `notAfter`, and `approvedUsers`/`allowedAccountTypes`/
`requiredProfileStatuses` (all three for `user-specific-restriction` alone, since its
Reference Values Schema has three independent keys that don't decompose from the
pre-existing free-text `userSpecificRestriction` field). Two of these are real shape
corrections, not just additions: `publicationMoratorium` (an end-date) and
`timeLimitOnUse` (a number of months) are left as-is, and the new
`requiredAgreementDocumentId`/`notAfter` slots source those two `policy_cards/`
instead, since the old fields never held what those policies actually check. All 21
bindings now have every `referenceValueKey` mapped except
`ethics-approval-required`, whose Reference Values Schema is genuinely empty (a pure
credential-chain check) — nothing to source, not a gap.

`scripts/build_policy_fabric.py` exports an `AccessRequirement` instance into Policy
Fabric's actual input shape: `policy_data.json` (merged reference values),
`associated_credentials.json`, and `asset_registration.json`. Run against
`linkml/examples/access_requirement_policy_fabric.example.yaml` (DUO:0000022 +
DUO:0000028 together, mirroring the tutorial's own worked example) via
`make policy-fabric`, its `policy_data.json` output is byte-for-byte the tutorial's
literal `{"allowedCountries": ["US"], "allowedInstitutions":
["did:example:best_university"]}`. **No changes have been made to
`hasan7n/tmp-policies` itself.**

## Governance Graph alignment

`linkml/governance_graph.yaml` (plus `AccessTypeEnum`/`AccessRequirementConcreteTypeEnum`
and a new `SynapseAccessRequirementMixin`, in `linkml/mixins.yaml`) captures the
SageBrain **Governance Graph** design: a logically separate graph of ACLs and
Access Requirements, connected to the domain/scientific metadata graph only via
shared Synapse entity URIs. Its central point — an ACL answers "who has which
permission on this resource?", an Access Requirement answers "what additional
conditions must be satisfied?", and effective access needs both — is why
governanceDUO's existing `AccessRequirement`/DUO-condition model gets a genuinely
new **ACL/permission-grant** side (`AccessGrant`, `Principal`), not a
reinterpretation of what already existed.

Every new class/enum was verified against a real source, the same discipline as
the DUO/Policy-Fabric work above: the two "sagebrain governance graph ACL_AR data"
CSVs (Synapse's actual `ACCESS_REQUIREMENT`/`ACL`/`NODE`/... relational table
schemas) for column existence and type, and live lookups for the controlled
vocabularies those CSVs name but don't enumerate — `AccessTypeEnum` (18 real
values, shared by an ACL grant's permission *and* an AR's own governed access
kind — same underlying Synapse type) via `rest-docs.synapse.org`,
`AccessRequirementConcreteTypeEnum` (5 values) and `SubmissionStateEnum`
(SUBMITTED/APPROVED/REJECTED/CANCELLED) via Java source on
`Sage-Bionetworks/Synapse-Repository-Services`/`SynapseWebClient`. `NODE_TYPE`
(project/folder/file/...) was **not** independently verified and is left as an
open string rather than a fabricated enum.

New classes are additive and deliberately separate from existing ones with a
similar-sounding but different purpose: `SynapseEntity` (mirrors `NODE`, with real
`parentId` hierarchy for direct-vs-inherited resolution) is distinct from
`Resource` (a reusable resource-*type* pattern, not a concrete entity);
`AccessRequirementAssociation`/`DataAccessSubmission`/`DataAccessSubmissionStatus`
give the design doc's "direct vs. inherited" governance and "has the user
satisfied this AR?" concepts an explicit, auditable home (mirroring
`ACCESS_REQUIREMENT_PROJECT`/`DATA_ACCESS_SUBMISSION`/`DATA_ACCESS_SUBMISSION_STATUS`)
instead of a precomputed boolean.

Ontology mappings (verified via OLS where indexed) include `prov:Entity`/`prov:Agent`
for `SynapseEntity`/`Principal`, `dcterms:isPartOf`/`creator`/`created`/`modified`/
`contributor`/`source`/`requires` for the obvious provenance/hierarchy slots, and
`schema:DigitalDocumentPermissionType` + **`dpv:AuthorisationProtocols`** for
`AccessGrant` — the latter found via a documented **fallback to
[Linked Open Vocabularies](https://lov.linkeddata.es/)** after confirming OLS has no
entry at all for DPV (the Data Privacy Vocabulary); this fallback (validated
against DPV, PROV, and SKOS) is now built into the `ols-term-annotator` skill
itself as `lov-vocab-search`/`lov-term-search`. `bindingType`, submission `state`,
and `Principal.principalType` were checked and left unmapped rather than forced.

`scripts/build_governance_graph.py` exports the worked example under
`linkml/examples/governance_graph/` (recreating the design doc's own `syn10081783`/
`Team X`/`AR-123`/Alice scenario) as Turtle using the doc's own `gov:`/`syn:`
predicates — run via `make governance-graph`, its output is structurally the same
shape as the doc's own snippets (e.g. `gov:ar-association-001 a
gov:AccessRequirementAssociation ; gov:resource syn:syn10081783 ; gov:accessRequirement
gov:AR-123 ; gov:source gov:Synapse ; gov:bindingType gov:Inherited .`), including
correctly *not* emitting a `gov:hasApproval` triple while Alice's submission is only
`SUBMITTED`, not yet `APPROVED`. The LinkML schema itself registers this same
namespace under `sagegov:`, not `gov:` — `gov:` collides with a different,
canonical prefix (`http://gov.genealogy.net/ontology.owl#`) `linkml-lint` flagged,
same as `ebiswo:` vs. OBO Foundry `SWO:` earlier; the export script uses the literal
`gov:` in its own Turtle output regardless, since that's independent of the
schema's prefix registry.

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
